# 部署平台兼容说明

发布前先识别托管类型，再选择对应适配方式。不要把某个平台的配置文件或控制台路径套用到另一个平台。

兼容信息最后核对日期为 2026-09-20，主要参考：

- [腾讯云 EdgeOne Pages 构建指南](https://edgeone.cloud.tencent.com/pages/document/162936788693114880)
- [腾讯云 EdgeOne Pages `edgeone.json`](https://edgeone.cloud.tencent.com/pages/document/162936771610066944)
- [腾讯云 EdgeOne 修改 HTTP 节点响应头](https://cloud.tencent.com/document/product/1552/71011)
- [腾讯云 CloudBase 静态网站托管](https://cloud.tencent.com/document/product/876/46900)
- [腾讯云 COS 设置静态网站](https://cloud.tencent.com/document/product/436/32670)
- [腾讯云 COS 静态网站常见问题](https://cloud.tencent.com/document/faq/436/56555)

## 统一发布契约

无论使用哪个平台，都必须确认：

1. 构建命令使用最终子路径，例如 Vite 的 `--base=/<slug>/`。
2. 发布目录与构建产物目录一致，不上传源码目录代替生产构建。
3. `/<slug>/index.html`、脚本、样式、图片和字体全部可访问。
4. HTML 使用短缓存或协商缓存；带内容哈希的静态资源可以使用长期缓存。
5. 自定义域名、HTTPS、CSP、MIME 类型和下载响应头符合预期。
6. 首页、子页面、直接刷新、返回入口和导出功能都在正式域名验证。
7. 平台有传播或 CDN 缓存时，等待合理时间并执行一次明确刷新，不重复创建规则。
8. 记录公开 URL、部署标识、响应头和验证时间。

## 平台识别

优先检查仓库文件和现有部署设置：

| 线索 | 可能的平台 |
|---|---|
| `edgeone.json`、EdgeOne Pages 项目 | 腾讯云 EdgeOne Pages |
| `cloudbaserc.json`、CloudBase 配置或 `*.tcloudbaseapp.com` | 腾讯云 CloudBase |
| COS 上传脚本、`cos-website` 域名或 CDN 回源配置 | 腾讯云 COS 静态网站 |
| `esa.jsonc` | 阿里云 ESA Pages |
| `vercel.json` | Vercel |
| `netlify.toml`、`_headers`、`_redirects` | Netlify |
| GitHub Actions Pages 工作流、`*.github.io` | GitHub Pages |
| `nginx.conf`、Apache 配置、自建服务器 | 通用静态服务器 |

如果本地配置与控制台设置冲突，以平台明确规定的优先级和线上实际响应为准。

## 腾讯云 EdgeOne Pages

适合 Git 仓库持续部署和静态前端项目。

### 构建配置

- 确认根目录、安装命令、构建命令和输出目录。
- `edgeone.json` 可声明 `buildCommand`、`installCommand`、`outputDirectory`、`nodeVersion`、`headers`、`redirects`、`rewrites` 和缓存规则。
- 环境变量变更只对后续部署生效，应触发新部署后再验证。

示例骨架：

```json
{
  "buildCommand": "npm run build",
  "installCommand": "npm ci",
  "outputDirectory": "dist",
  "headers": [
    {
      "source": "/project-slug/*",
      "headers": [
        {
          "key": "Content-Security-Policy",
          "value": "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; object-src 'none'; base-uri 'self'"
        }
      ]
    }
  ]
}
```

只复制项目实际需要的 CSP 指令。`edgeone.json` 的 header 值不支持中文，且 header 数量和值长度存在平台限制。

### 路由注意事项

- 本技能默认生成真实的 `/<slug>/index.html`，不依赖 SPA 回退即可打开作品页。
- EdgeOne Pages 文档说明静态资源 `rewrites` 不支持 SPA 前端路由回退。需要多级客户端路由时，应使用前端路由方案、平台函数或调整项目路由模式，并实际测试直接刷新。
- 路径级安全响应头可直接写入 `edgeone.json`；使用完整 EdgeOne 站点加速时，也可以在规则引擎中按 URL Path 修改 HTTP 节点响应头。

### 验收

检查部署日志、输出目录、正式域名、`/<slug>/`、静态资源、实际响应头和缓存命中情况。

## 腾讯云 CloudBase 静态网站托管

CloudBase 支持本地上传、模板部署和 Git 仓库部署，并集成 CDN、HTTPS 和自定义域名。

- Git 部署时确认安装命令、构建命令和输出目录。
- 生产环境绑定自定义域名；平台默认域名更适合开发测试。
- 首页文档通常为 `index.html`，可按需要配置重定向规则。
- 节点缓存和浏览器缓存是两套独立规则，应分别设置。
- HTML 建议短缓存；带哈希的 JS、CSS 和图片可以长期缓存。
- 缓存规则变更通常需要传播时间；控制台上传文件会触发 CDN 刷新，Git 部署后仍需检查实际响应。
- CloudBase HTTP 访问服务支持统一域名、路径映射和自定义响应头；需要路径级 CSP 时优先使用该能力并验证线上头部。

## 腾讯云 COS 静态网站与 CDN

COS 只托管静态内容，不执行服务端代码。

- 开启静态网站功能，并配置 `index.html` 和错误文档。
- 将作品部署到 `<slug>/index.html` 及其资源目录；某些目录访问模式要求每个目录层级存在索引文档。
- 2024 年 1 月 1 日以后创建的存储桶，默认域名访问存在直接预览限制；生产环境应使用已配置的自定义域名。
- 使用 CDN 时，源站类型应选择“静态网站源站”，并根据存储桶公有读或私有读状态配置回源鉴权。
- 上传时确认 `Content-Type`、`Cache-Control` 和需要的自定义响应头元数据。
- 前端路由使用 History 模式时，直接刷新可能返回 404。优先发布真实目录入口，或明确配置错误页／路由回退并验证状态码和内容。
- 开启强制 HTTPS，验证自定义域名证书和 CNAME 生效。

## 腾讯云 EdgeOne 站点加速

当源站托管在 COS、CloudBase 或自建服务器，前面再接入 EdgeOne 时：

- 在规则引擎中按 HOST 和 URL Path 匹配 `/<slug>/`。
- 使用“修改 HTTP 节点响应头”设置路径级 CSP、缓存或安全头。
- 使用访问 URL 重定向处理旧地址跳转；使用回源 URL 重写处理公开路径与源站路径不同的情况。
- 修改节点响应头不会改变节点缓存内容，但规则是否生效仍应以客户端收到的真实响应为准。
- 避免同时在源站、CDN 和 EdgeOne 配置相互冲突的 CSP 或缓存规则。

## 阿里云 ESA Pages

读取 `esa.jsonc` 和 [ESA Pages 与 CSP](esa-pages.md)。确认构建目录、路径级响应头规则、规则顺序和传播状态。

## Vercel、Netlify 与 GitHub Pages

- **Vercel**：检查构建命令、输出目录、`vercel.json` 的 headers/redirects/rewrites，以及子路径资源前缀。
- **Netlify**：检查发布目录、`netlify.toml`、`_headers` 和 `_redirects`。路径级 CSP 应只匹配目标作品目录。
- **GitHub Pages**：确认项目站点的仓库基础路径、自定义域名和 Pages 工作流产物。GitHub Pages 不提供任意服务端响应头配置时，应避免依赖必须由服务端设置的功能，或在前面接入支持响应头规则的 CDN。

这些平台的配置字段可能更新；修改前读取仓库现有配置和平台当前官方文档。

## Nginx、Apache 与其他静态服务器

- Nginx 使用 `location /<slug>/` 指向实际构建目录，并在该范围内设置响应头和缓存。
- Apache 使用对应目录、`.htaccess` 或虚拟主机规则设置索引、响应头和缓存。
- 确认 MIME 类型、目录索引、压缩、HTTPS 和 404 行为。
- SPA 回退不得覆盖真实静态资源，也不得把资源 404 伪装成 HTML 200。

## 平台迁移

迁移时先建立映射表：构建命令、输出目录、环境变量、自定义域名、路径规则、响应头、缓存、重定向和错误页。迁移完成后使用新平台正式域名重新执行完整验收，不沿用旧平台的成功结论。
