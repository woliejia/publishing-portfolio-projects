# Publishing Portfolio Projects｜发布作品集项目

一个遵循通用 `SKILL.md` 结构的 Agent Skill，用于把已经完成的网页项目作为**作品卡片和独立子页面**加入现有个人网站，并完成构建、部署与线上验收。

本技能覆盖子路径构建、本地封面、首页作品卡片、返回入口、站点地图、生产环境浏览器检查、WebGL 导出验证，以及阿里云 ESA Pages 的路径级 CSP 配置。

## 中文说明

### 适用场景

- 将 React、Vue、Vite 或普通静态网页加入现有作品集。
- 把项目发布到 `/project-slug/` 形式的子路径。
- 为首页增加封面、标题、简介、标签和项目入口。
- 保留项目页面返回 `/#projects` 的导航。
- 检查静态资源、移动端、WebGL、PNG 导出和生产环境报错。
- 排查 HTML 能打开但 JavaScript 被 CSP 阻止的问题。
- 在阿里云 ESA Pages 中为单个子项目配置精确的响应头规则。

### 前置条件

建议准备：

1. 已经可以独立运行的网页项目。
2. 现有个人网站或作品集仓库。
3. 网站构建目录，例如 `public`、`dist` 或 `out`。
4. 只包含小写字母、数字和连字符的子路径名称，例如 `design-studio`。
5. 对部署平台和 Git 仓库的正常访问权限。

技能会先从仓库、配置文件和部署设置中自动发现这些信息，只在无法确定时询问用户。

### 平台兼容性

| 平台 | 兼容方式 | 推荐入口 |
|---|---|---|
| Codex | 原生读取 `SKILL.md` | `~/.codex/skills/` |
| WorkBuddy | 上传技能包或复制技能目录 | `~/.workbuddy/skills/`、`.workbuddy/skills/` |
| CodeBuddy | 用户级或项目级 Skill | `~/.codebuddy/skills/`、`.codebuddy/skills/` |
| 扣子 Coze | 上传自定义技能包 | 编程技能面板的“创建技能 → 本地上传” |
| 豆包工作流 | 通过使用豆包模型的扣子 Agent/工作流 | 在扣子中添加本技能 |
| 其他 Agent | Agent Skills 或提示词降级 | 导入技能目录，或附加 `SKILL.md` |

普通豆包聊天界面不一定提供文件型 Skill 导入入口。“豆包可用”指通过扣子中配置豆包模型的 Agent/工作流使用，或将本技能作为任务说明交给具备文件和命令工具的智能体。详细边界见 [`references/platform-compatibility.md`](references/platform-compatibility.md)。

### 安装方法

#### Codex

复制或克隆到：

```text
~/.codex/skills/publishing-portfolio-projects/
```

#### WorkBuddy

在技能界面上传一个以 `SKILL.md` 为根文件的 ZIP，或者复制到：

```text
~/.workbuddy/skills/publishing-portfolio-projects/
```

项目级安装可使用：

```text
.workbuddy/skills/publishing-portfolio-projects/
```

#### CodeBuddy

用户级安装：

```text
~/.codebuddy/skills/publishing-portfolio-projects/
```

项目级安装：

```text
.codebuddy/skills/publishing-portfolio-projects/
```

#### 扣子 / 豆包模型工作流

在扣子编程的技能面板选择“创建技能 → 本地上传”，上传符合页面要求的技能包。如果页面要求 `.skill` 文件，应通过扣子创建或导入本技能后，由扣子生成 `.skill`，不要仅修改 ZIP 扩展名。之后把技能添加到使用豆包模型的 Agent 或工作流。

#### 无原生 Skill 功能的平台

将 `SKILL.md`、`references/verification.md` 和需要的参考文件附加到对话，并要求智能体严格执行其中流程。Node.js 可用时仍可运行确定性检查脚本。

#### 构建通用 ZIP

仓库提供跨平台 Python 打包脚本。生成的 ZIP 根目录直接包含 `SKILL.md`，不携带 Codex 专属适配文件：

```bash
python scripts/build-package.py
```

输出文件位于 `dist/publishing-portfolio-projects-universal.zip`，命令同时打印 SHA-256 校验值。该 ZIP 适合 WorkBuddy 上传，也可作为其他支持通用 Agent Skill 包的平台输入。扣子页面要求 `.skill` 时仍应由扣子生成该格式。

目录结构：

```text
publishing-portfolio-projects/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── esa-pages.md
│   ├── platform-compatibility.md
│   └── verification.md
└── scripts/
    ├── build-package.py
    ├── check-portability.mjs
    └── check-release.mjs
```

安装后重新启动或刷新对应 Agent，使技能目录重新加载。

### 调用方式

```text
使用 publishing-portfolio-projects 技能，将这个网页项目加入我的个人网站作品集，并完成上线验证。
```

也可以指定子路径和验收要求：

```text
使用 publishing-portfolio-projects 技能发布这个项目。
子路径使用 /design-studio/，封面从实际应用截图生成，并检查移动端和 CSP。
```

### 完整工作流程

#### 1. 检查现有项目

- 阅读 `README`、`AGENTS.md`、构建脚本和部署配置。
- 确认网站技术栈、静态输出目录和部署分支。
- 记录修改前的 Git 状态，避免覆盖无关改动。
- 检查现有作品卡片的结构、字体、颜色和响应式规则。

#### 2. 确定子路径

选择稳定、简短的 slug，例如 `design-studio`，最终路径为：

```text
/design-studio/
```

避免空格、中文、临时版本号和本机目录名称。

#### 3. 按子路径构建应用

Vite 项目可以使用：

```bash
vite build --base=/design-studio/
```

资源路径应使用框架提供的基础路径，例如 Vite 的 `import.meta.env.BASE_URL`。构建后的 HTML 不应残留：

```text
/src/
/@vite/client
/node_modules/
```

#### 4. 制作作品封面

- 从验证通过的真实应用画面生成封面。
- 使用本地图片，避免远程资源失效或跨域。
- 保持宽高比，不裁掉核心界面。
- 添加准确的 `alt` 文本。
- 对懒加载图片检查 `decode()` 或 `naturalWidth`，不能只判断元素是否可见。

#### 5. 添加首页作品卡片

卡片至少包括：

- 项目封面
- 项目名称
- 简短说明
- 技术或类型标签
- 指向 `/<slug>/` 的真实链接
- 鼠标、键盘焦点和移动端状态

沿用原网站的视觉语言，避免改动无关导航、字体和元数据。

#### 6. 添加入口与返回导航

- 将生产构建复制到 `<public>/<slug>/`。
- 首页卡片打开 `/<slug>/`。
- 子页面提供返回 `/#projects` 的入口。
- 如果存在 `sitemap.xml`，加入完整子页面 URL。
- 确认直接刷新子页面时所有资源仍能加载。

#### 7. 运行静态发布检查

```bash
node scripts/check-release.mjs path/to/public design-studio
```

脚本检查：首页链接、子页面入口、本地资源、开发环境引用、站点地图，以及资源是否越过发布目录边界。

#### 8. 使用生产方式验证

使用普通静态服务器打开最终输出目录。框架开发服务器可能自动重写路径或暴露只在开发环境存在的全局对象。

至少验证：

1. 首页能显示封面和卡片。
2. 卡片能进入子页面。
3. 子页面能返回作品集区域。
4. 主要交互会改变真实状态。
5. 刷新后没有关键资源 404。
6. 移动端没有横向溢出，按钮可以触达。
7. 控制台没有影响功能的错误。

#### 9. 验证 WebGL 和图片导出

- 分别使用新的浏览器进程验证桌面高清导出和移动端。
- 避免多个 WebGL 上下文引起着色器报错或上下文丢失。
- 检查 PNG 文件签名、宽高和最低分辨率。
- 对缩小后的画布取样，排除全黑、全透明或空白图片。
- 确认导出后相机、材质和交互状态恢复。

#### 10. 部署并检查线上环境

- 提交经过审查的文件并推送部署分支。
- 等待部署完成后访问公开域名。
- 检查首页和子页面状态、实际响应头、CSP 和控制台。
- 再次执行首页 → 子页面 → 返回入口的完整路径。
- 不把本地构建成功当作生产环境成功。

### 阿里云 ESA Pages 与 CSP

如果 HTML 返回成功，但应用停留在加载占位符，应检查控制台和 `Content-Security-Policy`。

路径级规则条件示例：

```text
(http.host eq "www.example.com" and starts_with(http.request.uri.path, "/project-slug/"))
```

原则：

- 保留网站的严格全局 CSP。
- 只为确实需要的项目路径增加权限。
- 让路径规则位于会覆盖它的通用规则之后。
- 保存后读取公开页面的实际响应头。
- 规则传播需要时间时有限重试，避免重复创建。

详细说明见 [`references/esa-pages.md`](references/esa-pages.md)。

### 验收清单

| 范围 | 验收要求 |
|---|---|
| 构建 | 使用最终子路径完成生产构建，没有开发环境引用 |
| 封面 | 图片成功解码、比例正确、替代文本清晰 |
| 卡片 | 链接、焦点、悬停和移动端布局正常 |
| 导航 | 首页能进入项目，项目能返回作品集区域 |
| 资源 | 本地资源全部存在，无关键 404 |
| 交互 | 主要按钮和状态切换真实影响应用 |
| 导出 | 文件可下载，尺寸正确，不是黑图或空图 |
| 移动端 | 无横向溢出，核心控制可以操作 |
| 生产环境 | 公开 URL、响应头、CSP 和控制台均经过检查 |

完整矩阵见 [`references/verification.md`](references/verification.md)。

### 常见问题

#### 子页面没有样式或脚本

检查构建 `base`、HTML 绝对路径，以及发布目录是否与公开 slug 一致。

#### 页面只有加载提示

检查 CSP 错误和实际响应头。HTTP 200 不代表模块脚本已经执行。

#### 导出的 PNG 是黑图

在新的浏览器进程中复现并做像素检查。若超大尺寸触发显存问题，可降低到规定的最低高清尺寸。

#### 封面可见但尺寸为零

等待图片 `decode()` 完成，或要求 `naturalWidth > 0`。元素可见不代表图片已经解码。

### 隐私与安全

公开内容不应包含：

- 个人域名、邮箱、真实姓名或账号凭据。
- Windows、macOS 或 Linux 的个人绝对路径。
- 电脑品牌、设备名称或本机用户名。
- Token、密码、API Key、私钥或内部站点 ID。
- 只适用于私人项目的名称和部署数据。

示例统一使用 `www.example.com`、`project-slug`、`<public>` 等占位符。发布前应扫描 Git 已跟踪文件。

### 许可证

MIT，详见 [`LICENSE`](LICENSE)。

---

## English Documentation

### Overview

This vendor-neutral Agent Skill publishes an existing web project as a portfolio card and hosted child page. It uses a portable `SKILL.md` core and covers subpath builds, local cover images, homepage entries, return navigation, sitemap updates, production browser checks, WebGL export validation, and path-scoped CSP rules for Alibaba Cloud ESA Pages.

### Use cases

- Add a React, Vue, Vite, or static project to an existing portfolio.
- Publish under a path such as `/project-slug/`.
- Add a cover, title, description, tags, and project entry.
- Preserve return navigation to `/#projects`.
- Verify assets, mobile layout, WebGL, PNG export, and production errors.
- Diagnose CSP-blocked applications and configure a scoped ESA rule.

### Prerequisites

Prepare a runnable web project, an existing portfolio repository, its static output directory, a lowercase slug, and deployment access. The skill discovers available details before asking questions.

### Platform compatibility

| Host | Native path or method |
|---|---|
| Codex | `~/.codex/skills/publishing-portfolio-projects/` |
| WorkBuddy | ZIP upload, `~/.workbuddy/skills/`, or `.workbuddy/skills/` |
| CodeBuddy | `~/.codebuddy/skills/` or `.codebuddy/skills/` |
| Coze | Custom skill upload in the programming skill panel |
| Doubao workflows | Add the skill to a Coze Agent or workflow using a Doubao model |
| Other agents | Agent Skills installation or prompt-only fallback |

A regular Doubao chat interface may not expose file-based skill installation. Doubao compatibility means using the skill through Coze with a Doubao model, or supplying the portable instructions to a tool-capable agent. See [`references/platform-compatibility.md`](references/platform-compatibility.md).

### Installation

#### Codex

```text
~/.codex/skills/publishing-portfolio-projects/
```

#### WorkBuddy

Upload a ZIP with `SKILL.md` at its root, or copy the folder to:

```text
~/.workbuddy/skills/publishing-portfolio-projects/
```

Use `.workbuddy/skills/publishing-portfolio-projects/` for project scope.

#### CodeBuddy

Use `~/.codebuddy/skills/publishing-portfolio-projects/` for user scope or `.codebuddy/skills/publishing-portfolio-projects/` for project scope.

#### Coze and Doubao-model workflows

Use **Create skill → Local upload** in the Coze programming skill panel. If the UI requires a `.skill` artifact, let Coze create or import the skill and generate that artifact; do not rename a ZIP. Add the installed skill to an Agent or workflow configured with a Doubao model.

#### Prompt-only fallback

Attach `SKILL.md`, `references/verification.md`, and any required reference files, then instruct the agent to follow them. The deterministic Node.js checker remains usable when command execution is available.

#### Build a universal ZIP

Use the cross-platform Python packager:

```bash
python scripts/build-package.py
```

It creates `dist/publishing-portfolio-projects-universal.zip` with `SKILL.md` at the archive root and prints its SHA-256 digest. The archive is suitable for WorkBuddy and other generic Agent Skill importers. Let Coze generate a `.skill` artifact when that format is required.

Restart or reload the host after a filesystem installation.

### Usage

```text
Use the publishing-portfolio-projects skill to add this web project to my portfolio and verify the public deployment.
```

You may include a slug and acceptance requirements:

```text
Use the publishing-portfolio-projects skill to publish this project under /design-studio/.
Create the cover from the verified application and check mobile layout and CSP.
```

### End-to-end workflow

#### 1. Inspect the repositories

Read instructions, build scripts, and deployment configuration. Identify the stack, output directory, and deployment branch. Record the initial Git status and inspect the existing card design.

#### 2. Select the child path

Use a stable lowercase slug containing letters, numbers, and hyphens, such as `/design-studio/`. Avoid spaces, temporary versions, and machine-specific names.

#### 3. Build for the final base path

For Vite:

```bash
vite build --base=/design-studio/
```

Use `import.meta.env.BASE_URL` or the framework equivalent. Confirm production HTML does not reference `/src/`, `/@vite/client`, or `/node_modules/`.

#### 4. Create the cover

Capture a verified application render, store it locally, preserve its aspect ratio, add descriptive alt text, and verify lazy images with `decode()` or `naturalWidth`.

#### 5. Add the portfolio card

Include the cover, name, description, tags, and a real `/<slug>/` link. Preserve existing visual conventions and verify hover, keyboard focus, and narrow-screen behavior.

#### 6. Publish navigation and assets

Copy the bundle to `<public>/<slug>/`, link the card, add a `/#projects` return control, update `sitemap.xml`, and verify direct refreshes.

#### 7. Run the static checker

```bash
node scripts/check-release.mjs path/to/public design-studio
```

It validates the homepage link, child entry, local assets, development references, sitemap entry, and output boundaries.

#### 8. Test the exact production output

Serve the final static directory with a plain server. Verify navigation, primary interactions, direct refreshes, mobile overflow, reachable controls, and functional console errors.

#### 9. Verify WebGL and exports

Use fresh browser processes for GPU-heavy desktop export and mobile checks. Confirm PNG signatures, dimensions, minimum resolution, non-empty pixels, and state recovery after export.

#### 10. Deploy and verify production

Commit reviewed files, push the deployment branch, and verify public URLs, live response headers, CSP, console output, and the full homepage → project → return path.

### Alibaba Cloud ESA Pages and CSP

If HTML loads but the application remains on its boot placeholder, inspect the live CSP header. Use a scoped condition:

```text
(http.host eq "www.example.com" and starts_with(http.request.uri.path, "/project-slug/"))
```

Keep the strict global policy, grant only required capabilities, order the specific rule correctly, and verify the live header after propagation. See [`references/esa-pages.md`](references/esa-pages.md).

### Acceptance checklist

| Area | Required evidence |
|---|---|
| Build | Final base path and no development references |
| Cover | Decoded image, correct ratio, descriptive alt text |
| Card | Working link, focus, hover, and mobile layout |
| Navigation | Homepage opens the project and the project returns |
| Assets | Local references resolve without functional 404s |
| Product | Primary controls change real application state |
| Export | Valid dimensions and non-empty pixels |
| Mobile | No horizontal overflow and reachable controls |
| Production | Public URLs, headers, CSP, and console checked |

See [`references/verification.md`](references/verification.md) for the complete matrix.

### Troubleshooting

- **Missing scripts or styles:** check the build base and deployed directory name.
- **Permanent loading placeholder:** inspect CSP errors and the live response header.
- **Black PNG export:** retry in a fresh browser process and inspect pixels.
- **Lazy image with zero dimensions:** wait for `decode()` or `naturalWidth > 0`.

### Privacy and security

Do not publish personal domains, email addresses, real names, credentials, machine paths, device names, usernames, tokens, private keys, internal site IDs, or private-project identifiers. Use placeholders and scan the tracked Git tree before publishing.

### License

MIT. See [`LICENSE`](LICENSE).
