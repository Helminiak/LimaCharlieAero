# Lima Charlie Aero RC3 engineering candidate

The authoritative product specification is `docs/RC3_CODEX_MASTER_IMPLEMENTATION_PROMPT.md`. Work is limited to `rc3-proof-of-work-seo` and PR #2. No production deployment or merge is authorized.

The approved live rollback commit is `3d48ea6ec3785bc1faf67a5826eb678c3d14cc58`. RC2 is a comparison/engineering reference, not the approved live baseline. The RC3 authoring source is `content/`, `templates/`, and `assets-src/`; `dist/` is generated and excluded from Git.

## Reproduce

Use Node 22 or later, Python 3.11 or later and the pinned dependencies:

```sh
npm ci
python3 -m pip install -r requirements-dev.txt
npx playwright install chromium firefox webkit
npm run build
npm test
npm run verify:performance
npm run package
```

Set `LCA_CHROMIUM_EXECUTABLE` only when using an existing compatible Chromium binary. Browser checks use local Cloudflare Wrangler Pages emulation. No command here deploys to Cloudflare. Performance checks use the local route/header preview model. Tests mock Formspree; they never submit customer messages.

```sh
python3 tools/preview.py --root dist --port 8080
node tools/capture_review.mjs dist final
```

For before screenshots, export the approved rollback commit into a separate temporary directory and pass that directory to `capture_review.mjs` with label `before`. This baseline is reference material, not a second authoring source.

## Editorial model

`pages.json` stores route-specific content and proof placements. `proof-assets.json` records source mapping, factual caption, privacy treatment and rights status. `hubs.json` contains updates/notice hub explanations. `updates.json` contains dated notices and owner answers; unpublished/internal records are excluded. Build dates come from `site.json`, not the wall clock. Assets receive content hashes and deterministic responsive WebP variants. Preserve the image subject when changing a source asset.

## Release gate

Asset-specific rights marked `REVIEW REQUIRED` require owner confirmation before public publication. The private engineering candidate does not confer that permission. Source history and prior publication are not a substitute for rights evidence. Actual inbox delivery, live edge behavior, physical-device checks and independent Design/SEO acceptance remain separate validation gates. Read `evidence/` before considering release.
