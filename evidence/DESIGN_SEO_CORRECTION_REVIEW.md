# Focused independent Design/SEO correction pass

ENGINEERING CANDIDATE COMPLETE — DESIGN/SEO SIGN-OFF REQUIRED

Requested by [PR #2 independent review](https://github.com/Helminiak/LimaCharlieAero/pull/2#issuecomment-6009835609). Starting HEAD: `17500ca79944ac7b7ee66843eb4e189f1bc3abd3`. Implementation phase pushed as `c6c3059c65044b5f59c586fdc51d468b54de9775`. Final evidence commit is the branch commit containing this report.

## Four requested corrections

| Defect | Correction | Verification |
|---|---|---|
| DSEO-01: defensive proof captions | 37 placements rewritten observation first, meaning second, applicable record/instructions boundary last | Caption before/after ledger; actual mobile and desktop proof inspection |
| DSEO-02: reused imagery had universal captions | All 55 placement captions distinct; open cowling, cage, DynaVibe, electrical, oil and records imagery explain the page-specific purpose | Source invariants and rendered proof screenshots |
| DSEO-03: stacked headings and machine copy | 89 section headings normalized or rewritten; Service Area search-term lists replaced by owner questions and factual regional context | Heading ledger; static SEO/schema; visual wrapping review |
| DSEO-04: mobile planning text walls | Services planning inputs/intake/start paths use existing lists; Service Area scope/access/travel inputs use lists, with technical and feasibility content retained | 1094 Services words; 811 Service Area words; 30/30 bands within limits |

## Actual visual self-review and correction cycle

Inspected mobile and desktop entry views for all 21 changed routes, plus all affected proof figures at both sizes. Used full-page screenshots and enlarged proof/reading-rhythm views, rather than inferring review from file existence. Services inputs now separate records, airframe, systems and calendar tasks. Service Area headings describe owner decisions; regional copy is prose rather than a search-keyword string. Existing typography, CTA priority and proof placement remain intact. Images retain the same crop behavior and subjects; captions are readable and not clipped.

Review found two further copy defects and corrected them: long Service Area base/access paragraphs were reorganized into existing bullet lists; masked logbook captions were narrowed to visible logbook/work-entry context instead of claiming the hidden entry structure was legible. The records, prebuy and Service Area routes were rebuilt, recaptured and retested at all six widths. Dated records still determine chronology; no fabricated repair acceptance, causal improvement, customer result, publication rights or travel promise was added. No known locally correctable P0/P1 in this focused pass remains. Independent brand/Design/SEO scoring is pending.

## Verification actually run

- Build: `python3 tools/build.py` — PASS, 39 HTML routes / 134 public files.
- Static/brand/repetition: `python3 tools/verify_static.py` — PASS, 2189 assertions / 1282 references / zero errors.
- Registers/content: `python3 tools/review_registers.py` — 38 proof subjects / 55 placements; 30/30 tracked bands met.
- Browser: `LCA_CHROMIUM_EXECUTABLE=/tmp/lca-baseline-chromium node tools/verify_design_seo_correction.mjs` — Chromium PASS, 21 routes, 126 layouts at 320/375/390/768/1024/1440, 21 axe scans, zero violations; 42 full-page screenshots.
- Final correction retest: same command with `LCA_FOCUSED_ROUTES=aircraft-records-review,light-sport-prebuy-evaluation,service-area` — PASS, 18 layouts, three axe scans, zero violations; six screenshots replaced with corrected final views.
- The first browser attempt failed because the new verification script used Playwright's convenience page API; corrected to explicit browser context before the complete successful run. Retained first-run log, no site defect or false PASS.
- Source/generated invariants: page sets, H1s/titles/descriptions/intros, proof IDs/src/alt/order, section counts, links, legacy anchors, all DOM IDs, form actions/field names and schema architecture unchanged. Editorial dateModified reflects this copy revision. Shared CSS/templates/JS and image behavior unchanged.
- Performance not rerun under the requested conditional rule: no shared CSS/template/image behavior changed. Prior eight-route P/A/SEO 100 measurements remain historical engineering evidence; no fresh performance measurement is claimed.

## Evidence and comparison

- `design-seo-caption-changes.json`, `design-seo-heading-changes.json`: exact before/after copy.
- `design-seo-changed-routes.json`: 21-route focused change matrix.
- `design-seo-static.log`, `design-seo-browser.json`, `design-seo-browser-scan-retest.json`, `design-seo-invariants.json`, `design-seo-generated-invariants.json`.
- `screenshots/design-seo-correction/`: final mobile/desktop full-page views; proof is visible within these captures. Before views for major routes remain under `screenshots/final/` at the starting SHA. Older full RC3 visual evidence remains preserved.
- Updated `WORD_COUNT_REPORT.md`, `CONTENT_RETENTION_REGISTER.md`, `PROOF_OF_WORK_REGISTER.md`, deployment manifest and static route audit.

## Scope, release integrity and external gates

Only `content/pages.json` changes application behavior, through copy and existing lists. No source architecture, route, proof strategy, image, form, schema architecture, links, CSS/template/runtime, performance/accessibility fix or release tool changed. Added only focused verification tooling and evidence. Main remains `3d48ea6ec3785bc1faf67a5826eb678c3d14cc58`. PR #2 stays open/draft/unmerged. No Cloudflare deployment or DNS/external production change.

Previous ZIPs, release report and SHA256SUMS identify the **prior 17500ca snapshot**, not this corrected copy candidate. They are preserved; packaging was not rerun in this focused correction scope. Review the current branch/generated source for re-review, not the earlier ZIP contents. Release packaging must be refreshed when a new release freeze is requested.

EXTERNAL / NOT PASS: rights for all 38 proof subjects REVIEW REQUIRED; actual Formspree delivery; production Cloudflare/DNS; WebKit host libraries; physical-device/screen-reader validation; records supporting stronger chronology; independent Design/SEO approval. This is not production approval.
