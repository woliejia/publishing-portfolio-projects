# Alibaba Cloud ESA Pages and CSP

Read this reference only for ESA-hosted portfolios or when the public page loads HTML but JavaScript is blocked.

## Deployment discovery

Check `esa.jsonc` first. Its build and `assets.directory` settings override corresponding console build settings. A common static portfolio configuration publishes `./public`.

After pushing, verify the deployed HTML before changing security rules. A successful 200 response can still show only the boot fallback when CSP blocks the module script.

## Path-scoped CSP override

Keep a strict general portfolio rule. Add a later ESA-to-client response-header rule that matches the project only, for example:

```text
(http.host eq "www.example.com" and starts_with(http.request.uri.path, "/project-slug/"))
```

Set `Content-Security-Policy` to the narrowest policy the child needs. A self-contained Vite/WebGL app with one dynamic inline style may use:

```text
default-src 'self'; script-src 'self'; style-src 'self'; style-src-attr 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self'; connect-src 'self'; worker-src 'none'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'none'; upgrade-insecure-requests
```

Remove directives the app does not need. Add external origins only after observing a required blocked request and confirming the dependency is intentional.

In the ESA console, use **Site management → site → Rules → Transform rules → Modify response headers → ESA to client**. Place the project rule after the general rule when later matching rules win. Saving a public header rule is an external mutation; follow the active computer-use confirmation policy.

## Live verification

Read the public response header and open the page in a clean production browser. Confirm:

- the homepage retains its strict CSP;
- the child response receives the path-specific CSP;
- the module script loads and the boot placeholder disappears;
- CSS, images, fonts, and downloads are permitted only as intended;
- there are no CSP violations or functional page errors.

Rule propagation can take time. Poll with bounded retries and evidence; do not create duplicate rules because the first change is still propagating.
