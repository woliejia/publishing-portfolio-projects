---
name: publishing-portfolio-projects
description: 用于将现有网页项目发布为个人网站作品卡片和经过验证的独立子页面，并完成子路径构建、封面、导航、CSP、WebGL 导出及生产环境验收。适用于 Codex、WorkBuddy、CodeBuddy、扣子等支持 SKILL.md 的智能体平台。
---

# Publishing Portfolio Projects

Publish the project as a real child page while preserving the portfolio's existing identity, stack, security, and deployment path. Completion means the homepage entry, deployed subpage, production headers, and user-visible interactions all work on the public domain.

## Host portability

Treat this file as the canonical, vendor-neutral skill definition. Use capabilities by purpose rather than by a vendor-specific tool name: inspect files, run commands, edit files, control a browser, and read live HTTP responses with whatever equivalent tools the current host provides.

- Do not require `agents/openai.yaml`; it is an optional Codex presentation adapter.
- Do not add host-specific frontmatter fields to this canonical file. Keep only the portable `name` and `description` fields.
- If the host cannot execute a bundled script, reproduce the same checks with its available shell or explain the exact manual command.
- If browser automation is unavailable, complete all local work, then provide precise production checks without claiming they passed.
- Follow the current host's authorization rules before publishing, changing cloud configuration, or performing other external mutations.

Read [references/platform-compatibility.md](references/platform-compatibility.md) when installing or adapting this skill for Codex, WorkBuddy, CodeBuddy, Coze, Doubao-based workflows, or another agent host.

## Required inputs

Infer these from the workspace and hosting console before asking the user: portfolio repository, deploy provider, public/build directory, intended slug, project build command, cover source, and canonical domain. Ask only for information that cannot be discovered.

## Workflow

1. Read repository instructions, deployment config, homepage structure, tests, and current response headers. Record the pre-change Git status.
2. Choose a stable lowercase slug. Build the child app for `/<slug>/`; for Vite use `vite build --base=/<slug>/`. Replace root-absolute application assets with `BASE_URL` or equivalent. Add a return link to `/#projects` when embedded.
3. Produce the cover from a verified application render. Keep its aspect ratio and descriptive alt text. Do not depend on a remote image host.
4. Copy the production bundle into the portfolio's static output directory at `<public>/<slug>/`. Add a real homepage card, CTA, responsive styling, and sitemap entry. Preserve existing typography, metadata, navigation, and unrelated content.
5. Run `node scripts/check-release.mjs <public-dir> <slug>`, repository tests, and the project's production build. Serve the exact static directory with a plain static server for integration checks; a framework development server can rewrite paths or expose development-only globals.
6. Verify homepage → card → subpage → return navigation in a production browser. Exercise representative interactions, mobile layout, local assets, console errors, and downloadable output. Validate downloaded image dimensions and non-empty pixels where export exists.
7. Commit only reviewed files, push the deployment branch, and verify the public domain. Do not report local success as deployment success.

Read [references/verification.md](references/verification.md) for the acceptance matrix. For Alibaba Cloud ESA Pages or CSP failures, read [references/esa-pages.md](references/esa-pages.md).

## Release invariants

- Keep app data/config separate from rendering when future edits depend on it.
- Never globally weaken a portfolio security header to make one project work. Scope overrides to the project hostname and path.
- Ensure a later path-specific rule actually overrides an earlier general rule; confirm the live header rather than assuming rule order.
- If WebGL export is black at a large size, reproduce with pixel checks and lower only to the documented minimum acceptable resolution.
- Use fresh browser processes for GPU-heavy desktop export and mobile checks when concurrent WebGL contexts cause shader or context-loss noise.
- Stop before the final external mutation when the active computer-use confirmation policy requires action-time approval.

## Delivery

Return the public subpage and portfolio URLs, commit/deployment identity, source/config locations, assumptions, verification evidence, and only material limitations.
