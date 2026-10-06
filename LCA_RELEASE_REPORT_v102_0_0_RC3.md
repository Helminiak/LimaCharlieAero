# Lima Charlie Aero v102.0.0 RC3 — final release freeze

FINAL RC3 RELEASE FREEZE COMPLETE — READY FOR RELEASE-INTEGRITY REVIEW

## Release identity and approval

- Approved corrected source HEAD: `abd0eb5a053d9cf6799782c3d08d4b9098fbb642` on `rc3-proof-of-work-seo`, Helminiak/LimaCharlieAero.
- Independent Design/SEO approval: [PR #2 comment 6010107244](https://github.com/Helminiak/LimaCharlieAero/pull/2#issuecomment-6010107244), approved for final release freeze. Independent weighted score approximately 96/100; this is not merge/deployment approval.
- Approved production rollback main remains `3d48ea6ec3785bc1faf67a5826eb678c3d14cc58`.
- Final branch SHA appears in the PR #2 freeze handoff; the final evidence commit cannot embed its own SHA. The approved application/build inputs are unchanged and listed by SHA-256 in `evidence/SOURCE_PACKAGE_VERIFICATION.json`. The final commit adds release report/verification evidence only.
- This freeze supersedes the former `17500ca...` ZIPs and includes the Design/SEO-approved caption, heading and mobile scanability corrections. No approved copy, route, form, schema, image, CSS/template, links or tooling changed during this freeze.

## Fresh verification

| Check | Actual result |
|---|---|
| Clean source | 367 Git blob-verified files copied from the approved remote tree into a new directory; no untracked local input, previous dist or node_modules copied |
| Dependencies | Fresh lockfile npm install: 156 packages; fresh isolated Python installation: Pillow 12.3.0 / lxml 6.1.1; Node v24.19.0, Python 3.12.14 |
| Build | PASS — `python tools/build.py`; 39 HTML routes / 134 public files / 4,866,579 bytes |
| Static/reference/schema/brand | PASS — 2189 assertions / 1282 references / zero errors; one H1, unique indexable metadata, canonicals, page-class schemas/stable IDs and repetition gates |
| Reproducibility | All 134 generated SHA-256 values match the approved corrected output; independent output-directory build also matches |
| Browser | Chromium 153 PASS — 124 route/header cases, 234 layouts, 20 local mocked form checks |
| Accessibility | All 39 routes freshly scanned with axe: zero violations; keyboard/focus/menu/text-enlargement checks in browser evidence |
| Deployable extraction | Exact 134-file payload set, ZIP CRC and every SHA-256 PASS; index.html at ZIP root; no source/docs/evidence exposure |
| Extracted-site smoke | PASS — 39 routes, six layouts, three axe scans; zero violations; local Wrangler only |
| Source extraction/rebuild | CRC/exact payload set/all payload SHA-256; independently extracted source with fresh pinned dependencies builds/static verifies; all 134 output hashes equal |
| Deterministic archives | Final source and deployable ZIP repeat hashes checked; final verification receipt is external to source ZIP |

Firefox and WebKit were **NOT RUN in the fresh freeze pass**: their pinned Playwright browser executables are unavailable on this host. Prior Firefox 155 results remain historical evidence, not a fresh PASS. Prior WebKit native-library limitation remains an external validation gate. Chromium binary provisioned separately; browser binaries are not included in source ZIP. Browser verification mocks Formspree and makes no actual inbox-delivery claim.

Performance and visual Design/SEO work were not reopened. Approved prior laboratory performance evidence is retained: eight representative routes P/A/SEO 100, home LCP 1.657 s, final E-PROPS 1.214 s, CLS/TBT 0, home transfer 202676 bytes. No fresh performance measurement or field Core Web Vitals is claimed.

## Content and proof retained

39-route architecture, 38 proof subjects, 55 contextual/distinct placement captions, 30/30 tracked content bands retained. Services 1094 words and Service Area 811. Privacy masks, rights gates, technical/authorization/chronology boundaries, page-specific captions, natural headings and mobile input lists are exactly the approved source. Existing Design/SEO correction and visual-review evidence is preserved; the independent sign-off is saved as `evidence/final-design-seo-signoff.json`.

## Delivered artifacts and hash scope

1. `LCA_SITE_v102_0_0_RC3_DEPLOYABLE.zip` — SHA-256 `7173c73c78b1d1f5d364d0bf16071d30994ecb4ff7e099c7b265ee7d9995ec7d`.
2. `LCA_SITE_v102_0_0_RC3_SOURCE_AND_VERIFICATION.zip` — current final SHA-256 is in external `SHA256SUMS.txt` and `evidence/final-source-package-checks.json`.
3. `LCA_RELEASE_REPORT_v102_0_0_RC3.md` — this report; SHA-256 in external `SHA256SUMS.txt`.
4. `SHA256SUMS.txt` — the three artifact SHA-256 values; its own SHA-256 is supplied in the PR handoff.

The source ZIP contains authoring/build/test inputs, pinned dependency declarations, this report, registers, visual evidence, fresh build/static/browser/preflight verification and `SOURCE_PACKAGE_MANIFEST.json`. That manifest lists every payload hash except its self-description. External `SHA256SUMS.txt` and `evidence/final-source-package-checks.json` are deliberately omitted from source payload to avoid self-referential hashes. Final extraction/rebuild results and both current ZIP hashes are in that external receipt. The final Git commit preserves the receipt and checksum file.

Clean-room/source preflight used cached pinned package distributions to avoid network dependence; it did not reuse a pre-existing node_modules or Python dependency installation. Final source extraction is independently rebuilt and compared again. Unchanged pinned dependencies may be reused only for the final repeat-archive comparison after the fresh extracted install succeeds.

## Evidence

- `evidence/final-freeze-source-audit.json`, `final-freeze-reproducibility.json`, `SOURCE_PACKAGE_VERIFICATION.json`: approved tree/input identity and clean output parity.
- `evidence/final-freeze-*-install.log`, `final-freeze-build.log`, `final-freeze-static.log`, `final-freeze-features.log`.
- `evidence/final-freeze-browser-checks.json`, `final-freeze-browser.log`, `final-freeze-browser-wrangler.log`.
- `evidence/final-freeze-source-preflight.json` and pinned-install/build/static logs.
- `evidence/packaging.json`, `package-browser-checks.json`, `final-source-package-checks.json`.
- `evidence/FINAL_FREEZE_CHANGED_FILES.md`, `WORK_RESUME_CHECKPOINT.md`.
- Previous full engineering/visual/design correction evidence is historical context; fresh final-freeze receipts govern this release candidate.

## External gates and governance

Design/SEO approval for the corrected source is COMPLETE. Final release-integrity approval remains required. External production gates remain NOT PASS: rights confirmation for all 38 proof subjects marked REVIEW REQUIRED; actual Formspree inbox delivery; production Cloudflare/DNS/edge behavior; Firefox/WebKit/Safari host/browser provision and physical-device/actual screen-reader validation; records for stronger chronology/causal claims.

Main was not modified. PR #2 remains open/draft/unmerged. No Cloudflare deployment, DNS change, production-service modification or customer contact occurred. No merge or deployment is authorized by this freeze.
