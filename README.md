# Publishing Portfolio Projects

A reusable Codex skill for publishing an existing web project as a portfolio card and hosted subpage.

It covers subpath builds, local cover images, homepage cards, return navigation, sitemap updates, production browser checks, WebGL export validation, and path-scoped Content Security Policy rules for Alibaba Cloud ESA Pages.

## Install

Copy this repository into your Codex skills directory:

```text
~/.codex/skills/publishing-portfolio-projects/
```

Restart or reload Codex so the skill catalog refreshes.

## Use

Invoke the skill in your request:

```text
Use $publishing-portfolio-projects to add this web project to my portfolio and verify the public deployment.
```

The skill expects an existing web project and portfolio repository. It discovers the current stack and deployment configuration before making changes.

## Static release check

Run the included checker against a portfolio public directory and child-page slug:

```bash
node scripts/check-release.mjs path/to/public project-slug
```

The command verifies the homepage link, child entry page, local assets, development-only references, and sitemap entry.

## Privacy

This repository contains no personal domains, usernames, machine-specific paths, credentials, project names, or deployment identifiers. Examples use generic placeholders.

## License

MIT
