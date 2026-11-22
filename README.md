# Lima Charlie Aero Website

Version-controlled source repository for the Lima Charlie Aero website.

## Repository purpose

This repository is the authoritative source of truth for the public Lima Charlie Aero website: site source, content, assets, build tooling, validation tooling, SEO controls, accessibility checks, release manifests, and deployable release artifacts where appropriate.

The repository is intended to make every website release reproducible from a specific Git commit or tag.

## Repository scope

Appropriate contents include:

- Website source code and templates
- Public images and static assets
- Public marketing copy
- SEO metadata and structured-data definitions
- Accessibility and static-site validation tooling
- Build scripts and deployment packaging
- Release manifests and checksums
- Test fixtures that contain no customer or credential data
- Design and implementation documentation
- GitHub Actions used to validate or package the site

## Do not commit

Do not store:

- Customer records, work orders, invoices, logbooks, or BUDS reports
- Personal identifying information that is not intentionally public
- Passwords, API tokens, private keys, Cloudflare secrets, or .env files containing secrets
- Proprietary third-party material without redistribution rights
- Litigation, medical, banking, or unrelated private records

Use environment variables or GitHub encrypted secrets for deployment credentials.

## Branch policy

- `main` = production-approved website source only.
- Substantial work is performed on named development branches.
- Codex or another implementation agent makes code changes on development branches.
- Implementation must complete its closed-loop verification cycle before review.
- ChatGPT or another independent reviewer may perform design, SEO, accessibility, and human-factors review.
- Changes merge to `main` only after review and acceptance.

Expected flow:

```text
main
  -> development branch
  -> implementation
  -> closed-loop QA
  -> pull request
  -> independent design/SEO/accessibility review
  -> corrections if required
  -> merge to main
  -> tag/release
  -> deployment
```

## Current production release

- Release: **v103** (tag `v103.0.0`), deployed from `main` by the Cloudflare Pages project `limacharlieaero` (Git integration, production branch `main`).
- Every push to `main` builds (`pip install -r requirements-dev.txt && python3 tools/build.py`, output `dist/`) and deploys to production automatically. Other branches do not deploy.
- Pre-v103 rollback points: tag `rollback/main-pre-v103` (previous `main`) and the original Direct Upload Pages project `lima-charlie-aero` (production deployment `971421a0`, retained). Recovery steps: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).

The live baseline originally imported for controlled change was `live-v100.2.5F` (`LCA_SOURCE_OF_TRUTH_BASELINE_v100_2_5F_DEPLOYABLE(1).zip`, SHA-256 `e160c234b86aac2076db101c1b2e1acd27c46ed010866fd1aa6b21ff8214710a`). Historical ZIP artifacts are release evidence, not working copies.

## Change-control rule

Do not perform a major redesign directly on `main`.

A release should be traceable to:

```text
issue / requirement
       ↓
development branch
       ↓
commits
       ↓
automated validation
       ↓
pull request
       ↓
review
       ↓
merge
       ↓
version tag
       ↓
release artifact
```

## Long-term objective

Eliminate ambiguous local folders and ZIP-based working copies. A commit SHA should uniquely identify the source being reviewed, tested, packaged, or deployed.

## Build and verify locally

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

Set `LCA_CHROMIUM_EXECUTABLE` only when using an existing compatible Chromium binary. Browser checks use local Cloudflare Wrangler Pages emulation. No command here deploys; production deploys only from `main` through the Cloudflare Pages Git integration. Performance checks use the local route/header preview model. Tests mock Formspree; they never submit customer messages.

```sh
python3 tools/preview.py --root dist --port 8080
node tools/capture_review.mjs dist final
```

For before screenshots, export the approved rollback commit into a separate temporary directory and pass that directory to `capture_review.mjs` with label `before`. This baseline is reference material, not a second authoring source.

## Editorial model

`pages.json` stores route-specific content and proof placements. `proof-assets.json` records source mapping, factual caption, privacy treatment and rights status. `hubs.json` contains updates/notice hub explanations. `updates.json` contains dated notices and owner answers; unpublished/internal records are excluded. Build dates come from `site.json`, not the wall clock. Assets receive content hashes and deterministic responsive WebP variants. Preserve the image subject when changing a source asset.
