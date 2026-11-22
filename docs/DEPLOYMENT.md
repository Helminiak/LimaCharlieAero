# Production deployment and rollback

## How production works

| Item | Value |
|---|---|
| Production source | GitHub `Helminiak/LimaCharlieAero`, branch `main` |
| Cloudflare Pages project | `limacharlieaero`, connected to GitHub (the Cloudflare Pages GitHub App) |
| Build command | `pip install -r requirements-dev.txt && python3 tools/build.py` |
| Build output | `dist` |
| Build environment | `PYTHON_VERSION=3.13` |
| Custom domain | `limacharlieaero.com` |
| Preview deployments | Disabled. Feature branches never build or deploy. |

A push or merge to `main` starts a production build. When it succeeds, Pages publishes it to `limacharlieaero.com`. If a build fails, nothing is published and the previous deployment stays live.

The workflow is:
1. Work on a feature branch.
2. Verify locally (see README, "Build and verify locally").
3. Review.
4. Merge to `main`.
5. Confirm the deployment in Cloudflare: Pages → `limacharlieaero` → Deployments. It shows the commit SHA.

## Retained rollback points

| Rollback point | Location |
|---|---|
| Previous `main` (before v103) | Git tag `rollback/main-pre-v103` → `6d9f82c` |
| Original live site (before v103) | The Direct Upload Pages project `lima-charlie-aero`, production deployment `971421a0` (2026-07-09). It is still reachable at https://971421a0.lima-charlie-aero.pages.dev. **Do not delete this project.** |
| v103 release | Git tag `v103.0.0` |

Email is handled by iCloud. Its MX, SPF, DMARC and verification TXT records are unrelated to Pages. No step below touches them.

## Roll back a bad v103-or-later deployment (fastest)

Do one of these:
- **In the dashboard.** Go to Pages → `limacharlieaero` → Deployments. Choose an earlier successful production deployment → `⋯` → **Rollback to this deployment**. This takes effect immediately, with no DNS change.
- **In Git.** Revert the bad commit (`git revert <sha>`) and push to `main`. Pages rebuilds and deploys the reverted source. Do not force-push `main`.

## Return to the original pre-v103 site (full recovery)

This moves the domain back to the retained Direct Upload project.

1. Pages → `limacharlieaero` → Custom domains → remove `limacharlieaero.com`.
2. Pages → `lima-charlie-aero` → Custom domains → add `limacharlieaero.com`.
3. DNS → `limacharlieaero.com`: the apex record must be a proxied `CNAME` to `lima-charlie-aero.pages.dev`. It is currently a proxied CNAME to `limacharlieaero.pages.dev`.
4. Confirm that https://limacharlieaero.com/ serves the July 2026 site. Its homepage title differs from v103. The domain status must show **Active**.

Every step is reversible. Repeat it in the opposite direction to return to v103.

## Post-deployment checks

Run these after any production change:
- `curl -sI https://limacharlieaero.com/`
  - expect 200;
  - `http://` must redirect 301 to `https://`.
- Spot-check:
  - `/`
  - `/services`
  - `/our-work`
  - `/owner-notices`
  - `/rotax-turbocharger-notice`
- Old `.html` paths must return a 308 or 301 redirect to the clean URL.
- Submit one test message through `/support-request` and confirm it reaches the shop inbox.
