# 阿里云 ESA Pages 与 CSP

仅在作品集托管于 ESA，或公开页面能返回 HTML 但 JavaScript 被阻止时阅读本文件。

## 识别部署配置

先检查 `esa.jsonc`。其中的构建命令和 `assets.directory` 会覆盖控制台对应设置。静态作品集常见的发布目录是 `./public`。

推送后先验证线上 HTML，再修改安全规则。HTTP 200 只表示 HTML 返回成功；模块脚本被 CSP 阻止时，页面仍可能一直显示启动占位符。

发布大体积媒体前，在控制台或当前文档中重新确认单文件上限。ESA Pages 曾出现 25 MB 单文件限制，应将视频压缩到限制以内并留余量，不能把 25 MB 当作 25 MiB。完整视频流程见 [视频作品发布](video-publishing.md)。

## 测试分支与生产分支

测试环境能够构建某个分支，不代表该版本一定能直接发布到生产环境。生产发布选择框只显示旧版本或看不到已验证版本时，先确认 Pages 应用的生产分支。

- 不要重复创建相同测试构建。
- 把已经验证的提交合并或快进到生产分支，通常是 `main`。
- 等待 ESA 从生产分支生成新版本，再核对生产环境版本号、提交 ID 和 100% 发布比例。
- 以正式域名返回的 HTML 和响应头判断是否生效。

## 路径级 CSP 规则

保留严格的作品集通用规则，再增加只匹配目标项目的“ESA 到客户端”响应头规则，例如：

```text
(http.host eq "www.example.com" and starts_with(http.request.uri.path, "/project-slug/"))
```

将 `Content-Security-Policy` 设置为子项目所需的最小权限。一个自包含的 Vite/WebGL 应用如果只有动态行内样式，可参考：

```text
default-src 'self'; script-src 'self'; style-src 'self'; style-src-attr 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self'; connect-src 'self'; worker-src 'none'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'none'; upgrade-insecure-requests
```

删除应用不需要的指令。只有观察到确实需要的阻止请求，并确认依赖可信时，才增加外部来源。

同源 MP4 使用 `media-src 'self'`。如果通用 CSP 仍只有旧的视频域名，即使 MP4 本身返回 200，浏览器也会拒绝播放。保存规则后必须重新读取公网 CSP。

在 ESA 控制台进入：**站点管理 → 目标站点 → 规则 → 转换规则 → 修改响应头 → ESA 到客户端**。当后匹配规则优先时，把项目规则放在通用规则之后。保存公开响应头属于外部操作，应遵循当前智能体平台的确认规则。

## 线上验证

读取公开页面的真实响应头，并在新的生产浏览器中确认：

- 首页仍使用严格的通用 CSP；
- 子页面收到路径级 CSP；
- 模块脚本成功加载，启动占位符消失；
- CSS、图片、字体和下载只获得预期权限；
- 没有 CSP 违规或影响功能的页面错误。

规则传播可能需要时间。使用有次数上限的重试并保存证据，不要因为尚未传播就重复创建同一规则。
