# 平台兼容说明

根目录的 `SKILL.md` 是唯一核心定义，只使用通用的 `name`、`description` 字段和相对资源链接。

兼容信息最后核对日期为 2026-09-20，参考以下官方文档：

- [WorkBuddy 技能说明](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)
- [CodeBuddy Code Skills](https://www.codebuddy.cn/docs/cli/skills)
- [扣子：使用技能](https://docs.coze.cn/guides_using_skill)
- [扣子：开发技能](https://docs.coze.cn/guides_vibe_coding_skill)

## 兼容矩阵

| 平台 | 原生使用 | 安装方式 |
|---|---|---|
| Codex | 支持 | 复制到 `~/.codex/skills/publishing-portfolio-projects/`；`agents/openai.yaml` 只是可选界面适配层 |
| WorkBuddy | 支持 | 上传根目录包含 `SKILL.md` 的 ZIP，或复制到 `~/.workbuddy/skills/`；项目级可使用 `.workbuddy/skills/` |
| CodeBuddy | 支持 | 复制到 `~/.codebuddy/skills/` 或 `.codebuddy/skills/`；核心文件不加入 CodeBuddy 专属 `allowed-tools` |
| 扣子 Coze | 支持自定义技能上传 | 上传至少包含 `SKILL.md` 和引用资源的平台兼容技能包；页面要求 `.skill` 时由扣子生成，不要仅修改 ZIP 扩展名 |
| 豆包工作流 | 通过扣子或提示词降级 | 在使用豆包模型的扣子 Agent 或工作流中添加本技能；普通豆包聊天界面可能没有文件型 Skill 导入入口 |
| 其他 Agent Skills 平台 | 通常支持 | 按平台文档安装技能目录；无法自动发现时，附加目录或把 `SKILL.md` 作为任务说明 |

## 技能包结构

目录或 ZIP 导入时，在包根目录保留：

```text
SKILL.md
references/
scripts/
```

`agents/` 是可选目录，不识别它的平台应直接忽略。不得压平 `references/` 或 `scripts/`，因为核心文件使用相对路径。不得打包 `.git`、构建产物、凭据、环境变量文件或本机专属路径。

## 能力映射

本技能依赖功能能力，不依赖固定工具名称：

| 能力 | 用途 |
|---|---|
| 文件读取和搜索 | 识别仓库说明、构建配置和首页结构 |
| 文件编辑 | 添加子项目构建、卡片、导航、站点地图和文档 |
| 命令执行 | 构建、测试、运行检查脚本和读取 Git 状态 |
| 浏览器或 HTTP 访问 | 验证公开页面、响应头、控制台错误和真实交互 |
| Git 与网络发布 | 用户授权后提交并推送经过审查的版本 |

缺少某项能力时，完成不依赖它的工作，并明确列出无法取得的证据。

## 无技能系统时的使用方式

1. 在任务开始时附加或粘贴 `SKILL.md`。
2. 附加 `references/verification.md`；使用 ESA 时再附加 `references/esa-pages.md`。
3. 提供网页项目、作品集仓库、目标 slug 和正式域名。
4. 要求智能体遵循工作流程，并逐项报告没有实际验证的生产检查。

有 Node.js 时仍可运行确定性检查：

```bash
node scripts/check-release.mjs path/to/public project-slug
```

## 平台专属元数据

平台专属配置应放在核心 `SKILL.md` 之外，避免某个平台的字段、工具名或调用语法破坏其他平台的解析。

- Codex 界面元数据位于 `agents/openai.yaml`。
- CodeBuddy 权限应在安装时配置；组织必须使用 `allowed-tools` 时，可维护平台专属副本。
- 扣子要求 `.skill` 时，应由扣子生成相应包格式。
