# Verification matrix

Use the checks that match the project. A green build alone is insufficient.

| Layer | Required evidence |
|---|---|
| Source | Clean pre-change status recorded; existing instructions and stack respected |
| Child build | Production build succeeds with the final subpath base; no `/src/`, Vite client, or `node_modules` references |
| Static release | Homepage links to `/<slug>/`; child `index.html` and every local asset resolve; sitemap contains the child URL when present |
| Cover/card | Cover loads at non-zero natural dimensions; aspect ratio, alt text, CTA, focus state, and mobile layout are usable |
| Navigation | Homepage card opens the child page; child return control restores `/#projects` |
| Product | Primary interactions change real application state; persistence survives reload if promised |
| Export | Download event fires; file signature, dimensions, minimum resolution, and non-black/non-empty pixels pass; UI state recovers |
| Resilience | WebGL/fallback behavior and missing-resource errors are checked where applicable |
| Production | Public URL returns 200; expected CSP is present; scripts/styles/images load; no functional console/page errors |
| Mobile | Narrow viewport has no horizontal overflow; essential controls remain reachable |

## Browser-test shape

Prefer separate production-browser runs for:

1. Homepage navigation and ordinary interactions.
2. High-resolution WebGL export.
3. Mobile WebGL layout.

This isolates GPU-heavy contexts and makes a failure attributable. Wait for images with `decode()` or a natural-dimension condition; DOM visibility alone does not prove a lazy image loaded.

For PNG export, inspect the PNG signature and width/height bytes, then sample a downscaled canvas. Reject all-black, transparent, or very low-color output. Preserve the app's interactive state after export.

## Reporting failed checks

Name the failed check and the observed evidence. Separate an application defect from a test-environment limitation. Re-run a WebGL failure in a fresh browser process before classifying it as an application defect.
