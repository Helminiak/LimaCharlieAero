# Implementation log · v103 owner preview

## Engineering handoff

Branch `redesign/v103-owner-preview`. The final rendered source is `4aa14c1`. The verification harness through `311f6d9` distinguishes both build roots and allocates separate local inspector ports. The final evidence and this log are recorded in the branch history after these commits. Both builds ran locally from committed source with the pinned packages and the existing Python environment. The engineering candidate is ready to freeze for Phase 9 independent design and SEO reviews. PREVIEW READY — USER REVIEW REQUIRED.

## Commit inventory

| Commit | Change |
|---|---|
| 57cc644 | Assess v103 preview feasibility and acceptance criteria |
| 549c5e1 | Isolate build artifacts and split RC3 renderers with 134-file parity |
| 7a786be | Mask panel placard and correct intake, editorial dates and baseline copy defects |
| ad24972 | Compose Flight Line pages, case stages and local photographic design system |
| 6ae8a47 | Repair preview verification and capture tools |
| 1ee41dd | Record Claude interim design review for v103 |
| 03e8600 | Apply interim design corrections to photography, service details and case records |
| 8e4896e | Extend native form, case disclosure and reproducibility checks |
| 8be6714 | Record interim defect status, placement inventory and measured build comparisons |
| 7362c9c | Preserve Claude interim design review 2 verbatim |
| 70b5925 | Correct case layouts and evidence placements across both build modes |
| b1f722a | Measure photo contrast, capture responsive geometry and audit both lab profiles |
| 185b992 | Tighten expanded case records and paint lazy photos before visual review |
| 9bc9509 | Preload the mobile hero crop and improve document and method grids |
| 216bcbb | Bind browser receipts to the selected public or private build |
| 4aa14c1 | Limit interior hero candidates by their encoded byte size |
| 311f6d9 | Give each local Pages verifier its own inspector port |

Build and routing changes live in tools. Content, cases and registry records live in content. Markup, navigation, interactions and layout live in templates. Images and the self-hosted font live in assets-src. The review, license and evidence files document the preview. See the full per-file inventory below.

## Counts

Counts use whitespace-separated main-element text nodes, including disclosure contents, without the shared header or footer. Images count actual main-element placements. RC3 comparison files matched all 134 frozen hashes.

| Route | RC3 words | Public words | Preview words | Public change | RC3 images | Public images | Preview images |
|---|---:|---:|---:|---:|---:|---:|---:|
| / | 991 | 482 | 608 | -51.4% | 6 | 13 | 12 |
| /404 | 76 | 50 | 50 | -34.2% | 0 | 0 | 0 |
| /about-credentials | 115 | 100 | 100 | -13.0% | 0 | 1 | 1 |
| /aircraft-records-review | 916 | 869 | 869 | -5.1% | 1 | 3 | 3 |
| /card | 40 | 40 | 40 | +0.0% | 0 | 0 | 0 |
| /contact | 391 | 366 | 366 | -6.4% | 1 | 2 | 2 |
| /e-props-dealer-support | 1383 | 1337 | 1362 | -3.3% | 4 | 8 | 8 |
| /faq | 1225 | 1222 | 1222 | -0.2% | 0 | 0 | 0 |
| /image-credits | 128 | 105 | 105 | -18.0% | 0 | 0 | 0 |
| /joseph-helminiak-bio | 825 | 731 | 731 | -11.4% | 1 | 2 | 2 |
| /light-sport-experimental-avionics | 859 | 788 | 788 | -8.3% | 6 | 8 | 8 |
| /light-sport-prebuy-evaluation | 1000 | 929 | 929 | -7.1% | 2 | 3 | 3 |
| /our-work | 0 | 213 | 1249 | new | 0 | 5 | 8 |
| /owner-notices | 298 | 298 | 298 | +0.0% | 0 | 0 | 0 |
| /planning-service-downtime | 264 | 264 | 264 | +0.0% | 0 | 0 | 0 |
| /prebuy-first-inquiry | 273 | 273 | 273 | +0.0% | 0 | 0 | 0 |
| /privacy | 216 | 192 | 192 | -11.1% | 0 | 0 | 0 |
| /rotax-9-series-912-914-915-916-support | 856 | 806 | 806 | -5.8% | 2 | 3 | 3 |
| /rotax-912-carb-sync | 724 | 739 | 739 | +2.1% | 1 | 4 | 4 |
| /rotax-912-high-oil-temperature | 673 | 671 | 671 | -0.3% | 1 | 3 | 3 |
| /rotax-912-mag-drop-troubleshooting | 699 | 711 | 711 | +1.7% | 0 | 3 | 3 |
| /rotax-915-916-turbo-ems-support | 741 | 759 | 759 | +2.4% | 0 | 3 | 3 |
| /rotax-cooling-oil-temperature-problems | 713 | 706 | 706 | -1.0% | 1 | 3 | 3 |
| /rotax-engine-systems-support | 1060 | 1164 | 1164 | +9.8% | 2 | 18 | 18 |
| /rotax-fuel-pressure-fuel-delivery-problems | 850 | 781 | 787 | -8.1% | 3 | 4 | 4 |
| /rotax-gearbox-notice | 224 | 224 | 224 | +0.0% | 0 | 0 | 0 |
| /rotax-gearbox-propeller-vibration | 984 | 883 | 883 | -10.3% | 6 | 7 | 7 |
| /rotax-ignition-ecu-electrical-faults | 836 | 799 | 799 | -4.4% | 3 | 5 | 5 |
| /rotax-installation-review | 953 | 879 | 887 | -7.8% | 6 | 7 | 7 |
| /rotax-rubber-hose-replacement-fluid-leaks | 971 | 920 | 920 | -5.3% | 2 | 3 | 3 |
| /rotax-turbocharger-notice | 170 | 202 | 202 | +18.8% | 0 | 0 | 0 |
| /s-lsa-e-lsa-maintenance | 995 | 993 | 997 | -0.2% | 0 | 3 | 3 |
| /security-disclosure | 107 | 82 | 82 | -23.4% | 0 | 0 | 0 |
| /service-area | 868 | 775 | 775 | -10.7% | 1 | 2 | 2 |
| /services | 1179 | 1326 | 1326 | +12.5% | 4 | 11 | 11 |
| /start-with-the-symptom | 275 | 275 | 275 | +0.0% | 0 | 0 | 0 |
| /support-request | 368 | 379 | 379 | +3.0% | 0 | 1 | 1 |
| /thank-you | 95 | 70 | 70 | -26.3% | 0 | 0 | 0 |
| /the-lima-charlie-aero-standard | 1226 | 1227 | 1227 | +0.1% | 3 | 6 | 6 |
| /updates | 489 | 489 | 489 | +0.0% | 0 | 0 | 0 |

Distinct main-content photographic sources or subjects, RC3 / public / preview: 39 / 53 / 54.

- / (-51.4%). The copy deck moves five service descriptions and their link rows to /services and replaces duplicate founder material with a single founder band. Draft case copy is available in preview.

## Verification

| Build | Routes | Files | Checks | Internal references | Errors |
|---|---:|---:|---:|---:|---:|
| dist | 40 | 318 | 4196 | 2251 | 0 |
| dist-preview | 40 | 324 | 4231 | 2270 | 0 |

## Closed-loop engineering verification

| Gate | Status | Result |
|---|---|---|
| Public and preview, reproducibility | VERIFIED | 40 routes each. The independent public rebuild matched every output hash. All draft-case copy was excluded from public, and all 40 preview pages carry noindex. |
| Static image integrity | VERIFIED | Zero repeated subjects or asset files across placements on each of 80 pages. Registration and EXIF/XMP checks returned zero errors. The negative duplicate fixture was rejected. |
| Service template and case structure | VERIFIED | All 17 service pages have the six required section headings in both builds and one limits section per service, five validated seven-stage draft cases, one case-specific limits note and one page-wide note on Our Work. |
| Browser and axe | VERIFIED | Chromium 153.0.8010.12, 127 route/header scenarios per build, 240 layouts per build, zero broken images, page errors or axe violations on 40 public and 40 preview routes. Expanded desktop Our Work also passed axe. |
| Keyboard and forms | VERIFIED | Skip target, menu Escape and focus return, FAQ, scrollable prebuy comparison, case disclosure and 200% text checked. Each build passed 24 form scenarios including three native reply paths with local POST interception. Four auxiliary and three release-feature checks passed. |
| Six-width visual review | VERIFIED | 240 WebP captures at quality 58. Native mobile resolution, maximum 960 stored pixels wide. Geometry agreed with all 240 encoded dimensions. Reviewed route contact sheets and enlarged priority sections. All 240 final captures were byte-identical to the visually reviewed set after the hero byte-cap change. |
| First viewport | VERIFIED | Home shows location, aircraft work and a Request Service button ending at y=567 in a 390×844 viewport. The 320 px header is 64 px on all 40 routes. |
| Motion and focus | VERIFIED | Reduced-motion browser contexts, static photo layouts, 3 px amber focus outline with navy outer ring. Visually checked keyboard focus at the skip link and expanded case disclosure. |
| Other engines | BLOCKED | 0 Firefox and 0 WebKit runs. Both Playwright executables are absent. Exact launch errors are in the defect register. |
| Independent sign-off and real-world coverage | UNTESTED | Phase 9 design and SEO, physical devices, screen reader, actual delivery and field p75 measurements await separate review. |

The public and preview browser receipts are [final-checks.json](../../evidence/redesign/final-checks.json) and [preview-checks.json](../../evidence/redesign/preview-checks.json). Axe marked some color-contrast decisions incomplete on five public and six preview routes. Engineering checked the photographic scrims, stepper colors, diagram foregrounds and intake placeholder separately. The counts above refer to reported violations.

## Preview heights

| Page | 390 px | 1440 px |
|---|---:|---:|
| Home | 6,784 | 6,078 |
| Services | 4,625 | 4,010 |
| E-PROPS | 5,729 | 5,222 |
| Our Work | 6,000 | 7,873 |
| Standard | 6,774 | 5,663 |

Our Work went from 13,809 px in interim review 2 to 9,524 px on the first session-4 pass, then 7,873 px with all five records expanded. Home clears the 7,000 px mobile ceiling. E-PROPS clears both its 8,000 px ceiling and its 6,093 px stretch target. All six widths are in [measurements.json](../../evidence/redesign/candidate/measurements.json).

## CD-12 contrast

Contrast ratios use a screenshot with glyph paint suppressed. Each worst value is the smallest pixel-level contrast across the rendered text boxes. Deciles use the mean luminance of the brightest 10% of pixels in each box, then the minimum across boxes.

| Width | Hero worst | Hero lightest decile | Tile worst | Tile lightest decile |
|---:|---:|---:|---:|---:|
| 320 | 5.05:1 | 5.63:1 | 14.69:1 | 15.15:1 |
| 375 | 5.04:1 | 5.63:1 | 14.88:1 | 15.79:1 |
| 390 | 5.12:1 | 5.63:1 | 15.06:1 | 15.78:1 |
| 768 | 5.63:1 | 5.63:1 | 14.50:1 | 14.61:1 |
| 1024 | 5.63:1 | 5.63:1 | 14.50:1 | 14.58:1 |
| 1440 | 5.63:1 | 5.63:1 | 14.50:1 | 14.64:1 |

The amber second line of the home heading at 375 px sets the 5.04:1 minimum. The complete per-label sample is in [photo-contrast.json](../../evidence/redesign/photo-contrast.json).

## Lighthouse lab measurements

Cold public navigations on local Wrangler Pages, Chromium 153.0.8010.12 and Lighthouse 13.5.0. Mobile uses simulated throttling at 412×823 and DPR 1.75. Desktop uses the Lighthouse desktop configuration. Columns use LCP milliseconds, unitless CLS, TBT milliseconds and decimal transfer bytes. One run per route and profile.

| Route | Profile | P | A | BP | SEO | LCP ms | CLS | TBT ms | Transfer bytes | Hero bytes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| / | mobile | 100 | 100 | 100 | 100 | 1,307 | 0.0073 | 0 | 325,609 | 19,324 |
| / | desktop | 100 | 100 | 100 | 100 | 476 | 0.0439 | 0 | 535,478 | 52,643 |
| /services | mobile | 100 | 100 | 100 | 100 | 1,613 | 0.0006 | 0 | 254,204 | 63,616 |
| /services | desktop | 100 | 100 | 100 | 100 | 355 | 0.0007 | 0 | 225,066 | 34,520 |
| /e-props-dealer-support | mobile | 100 | 100 | 100 | 100 | 1,381 | 0.0006 | 0 | 197,345 | 30,780 |
| /e-props-dealer-support | desktop | 100 | 100 | 100 | 100 | 410 | 0.0007 | 0 | 231,206 | 17,068 |
| /rotax-engine-systems-support | mobile | 100 | 100 | 100 | 100 | 1,534 | 0.0006 | 0 | 191,382 | 42,546 |
| /rotax-engine-systems-support | desktop | 100 | 100 | 100 | 100 | 398 | 0.0007 | 0 | 262,921 | 42,546 |
| /rotax-gearbox-propeller-vibration | mobile | 100 | 100 | 100 | 100 | 1,536 | 0.0009 | 0 | 244,344 | 30,780 |
| /rotax-gearbox-propeller-vibration | desktop | 100 | 100 | 100 | 100 | 344 | 0.0009 | 0 | 354,311 | 17,068 |
| /rotax-installation-review | mobile | 100 | 100 | 100 | 100 | 1,472 | 0.0006 | 0 | 185,475 | 35,042 |
| /rotax-installation-review | desktop | 100 | 100 | 100 | 100 | 416 | 0.0008 | 0 | 185,438 | 35,042 |
| /light-sport-prebuy-evaluation | mobile | 100 | 100 | 100 | 100 | 1,617 | 0.0006 | 0 | 149,841 | 34,746 |
| /light-sport-prebuy-evaluation | desktop | 100 | 100 | 100 | 100 | 392 | 0.0290 | 0 | 214,446 | 34,746 |
| /support-request | mobile | 100 | 100 | 100 | 100 | 1,376 | 0.0039 | 8 | 112,401 | 17,292 |
| /support-request | desktop | 100 | 100 | 100 | 100 | 405 | 0.0015 | 0 | 104,633 | 9,556 |
| /our-work | mobile | 100 | 100 | 100 | 100 | 1,612 | 0.0003 | 0 | 176,147 | 25,028 |
| /our-work | desktop | 100 | 100 | 100 | 100 | 498 | 0.0005 | 0 | 229,246 | 77,978 |

### Transfer and LCP diagnosis

The preserved session-3 Python-server run measured home at 582,378 bytes and 2,407 ms mobile LCP, and E-PROPS at 2,033 ms. Final Wrangler values are 325,609 bytes and 1,307 ms on home, and 1,381 ms on E-PROPS. Local server compression and timing differ between those runs. The final budget verdict uses the final measurements directly.

Earlier Services mobile transfer was 684,661 bytes and ROTAX hub desktop transfer was 818,876 bytes. Final measurements are 254,204 and 262,921 bytes. The earlier waterfalls fetched 400 px or original proof assets for 76 px index thumbnails. New 160 px and 352 px derivatives, lazy-image auto sizing, a 640 px intermediate source, a 76 px thumbnail slot and the indexed manifest icon reduce those requests. Each interior hero now offers source candidates within the 75,000/150,000-byte mobile/desktop limits. This also addresses the intermediate 81,806-byte prebuy and 77,978-byte Our Work mobile requests.

Home requests one art-directed AVIF early with a matching media-specific preload and high fetch priority. The 640 px AVIF is 19,324 bytes, and the 1600 px AVIF is 52,643 bytes. The 35,328-byte Archivo subset uses swap and normal stylesheet discovery. The waterfall showed one hero request, and below-fold proof retains native lazy loading. The full per-run metrics are in [artifact-performance.json](../../evidence/redesign/artifact-performance.json).

## Reproduction and provenance

Use the pinned Node dependencies and the existing Python environment. Build with `python3 tools/build.py` and `python3 tools/build.py --preview`. Run `npm test`, `python3 tools/verify_static.py dist-preview`, `node tools/verify_browser.mjs dist-preview preview`, `node tools/capture_candidate.mjs`, `node tools/measure_photo_contrast.mjs` and `npm run verify:performance`. The latter runs the nine public routes on both profiles. Local Wrangler logs for this run are retained in the ignored .build-evidence/runtime directory.

| Artifact | SHA-256 of deployment manifest |
|---|---|
| dist | `ae0037557c9bd1145fc7b3f1cf393023247bb903e3738dd255ca0c31aa1e04f3` |
| dist-preview | `aa298e2623f03e6c5e7be9dcf482c4642e7a43e640a8f57bbe34a10cf9a9ff2f` |

## Changed source and evidence inventory

Changes against the original redesign brief baseline through the engineering commits. The final matrix and companion receipts are indexed above.

| Git status | Path |
|---|---|
| M | .gitignore |
| M | assets-src/dimensions.json |
| A | assets-src/fonts/OFL.txt |
| A | assets-src/fonts/archivo-latin.woff2 |
| A | assets-src/images/proof/bing64-carburetor-rebuild-float-check.webp |
| A | assets-src/images/proof/eprops-blades-box-documents.webp |
| A | assets-src/images/proof/eprops-durandal.webp |
| A | assets-src/images/proof/eprops-glorieuse-912.webp |
| A | assets-src/images/proof/eprops-glorieuse-916.webp |
| A | assets-src/images/proof/exhaust-marking-hydra-detail.webp |
| A | assets-src/images/proof/garmin-g5-box-unit.webp |
| M | assets-src/images/proof/garmin-g5-installed-panel-close-800.webp |
| A | assets-src/images/proof/garmin-g5-installed-panel-wide.webp |
| A | assets-src/images/proof/ndt-magnetic-particle-report.webp |
| A | assets-src/images/proof/proof-owner-joe-airfield.webp |
| A | assets-src/images/proof/rotax-airbox-focus.webp |
| A | assets-src/images/proof/rotax-installed-hoses-overview.webp |
| A | assets-src/images/proof/rotax-support-hero-original-photo.webp |
| A | assets-src/images/proof/skyreach-bushcat-tailwheel-prebuy.webp |
| A | assets-src/images/proof/tl-ultralight-designer-correspondence.webp |
| A | content/cases.json |
| M | content/pages.json |
| M | content/proof-assets.json |
| M | content/site.json |
| M | content/updates.json |
| A | docs/redesign/CODEX_FEASIBILITY.md |
| A | docs/redesign/DEFECT_REGISTER.md |
| A | docs/redesign/IMPLEMENTATION_LOG.md |
| A | docs/redesign/REVIEW_CLAUDE_INTERIM_1.md |
| A | docs/redesign/REVIEW_CLAUDE_INTERIM_2.md |
| A | docs/redesign/licenses/Archivo-OFL.txt |
| A | docs/redesign/licenses/Archivo-source.md |
| A | evidence/redesign/IMAGE_PLACEMENTS.md |
| A | evidence/redesign/privacy/garmin-masked-400.png |
| A | evidence/redesign/privacy/garmin-masked-native.png |
| M | templates/page.html |
| A | templates/prebuy-table.html |
| A | templates/records-table.html |
| M | templates/site.css |
| M | templates/site.js |
| A | templates/system-map.html |
| M | tools/build.py |
| A | tools/build_assets.py |
| A | tools/build_common.py |
| A | tools/capture_candidate.mjs |
| A | tools/cases.py |
| A | tools/check_editorial.py |
| A | tools/compositions.py |
| A | tools/editorial.py |
| A | tools/image_layouts.py |
| A | tools/intake.py |
| A | tools/measure_photo_contrast.mjs |
| A | tools/metadata.py |
| M | tools/package_release.py |
| M | tools/performance.mjs |
| A | tools/prepare_capture.mjs |
| A | tools/render_site.py |
| M | tools/test-server.mjs |
| M | tools/verify_auxiliary.mjs |
| M | tools/verify_browser.mjs |
| M | tools/verify_release_features.mjs |
| M | tools/verify_static.py |

## 2026-11-21 · Post-review corrections to 7d2e68e

The three independent review inputs matched the supplied files with cmp before the first commit. A grouped Git command encountered a read-only worktree index. Standalone Git commands succeeded on redesign/v103-owner-preview. The sibling review worktree supplied a separate build and verification run.

Using the project virtual environment and both requested offline environment settings, the implementation checkout and sibling produced identical SHA-256 manifests for all 318 public and 324 preview files. Each build contains 40 HTML routes. Public output totals 8,497,509 bytes and preview totals 8,545,144 bytes. The public sitemap has 36 entries and the noindex preview sitemap has zero. The independent public repro-dist build also matched.

- Static verification completed 4,800 public checks and 4,840 preview checks. The preserved RC3 FAQ artifact has SHA-256 50a63e136a7e9ca191eac7dc48f0ba64dc5edb7739c125b313eec3e00ba3f544. The fixture and both correction builds matched its 33 ID/question pairs.
- Both Chromium suites exercised 40 axe routes, 240 route/width combinations, 127 route checks and 24 intake checks apiece. Form requests were intercepted. No provider delivery was attempted. Firefox and WebKit reported missing executables in both builds.
- The updated publication suite observed 21 rejected faults and passing clean controls. Two additional injected copy regressions failed independently with the expected static diagnostics. The authoritative publication receipt is evidence/redesign/negative-tests.json and the copy receipt is v103-owner-preview/copy-negative-tests.json under the same evidence directory. The earlier publication-checks.json is retained as an inherited checkpoint.
- Captures cover only the eight requested pages at 320, 375, 390, 768, 1024 and 1440 CSS pixels in both builds. All 96 measurements recorded zero horizontal overflow. The 210 images include full pages, focused changes and additional Our Work/stepper views. Visual inspection covered mobile and desktop copy, document masks, the two independent readings, notice paragraphs, the Our Work hero, legend and preview stepper. The five native document crops remain under evidence/redesign/privacy.
- Lighthouse 13.5.0 measured nine routes on mobile and desktop. All 18 performance, accessibility and SEO scores were 100. Maximum mobile LCP was 1,743 ms, maximum mobile CLS was 0.00734, and all mobile TBT values were zero. These are local simulated measurements.
- The public ZIP was extracted and checked against evidence/redesign/v103-owner-preview/deployment-manifest.json. All 318 hashes and all 40 served HTML bodies matched. The extracted browser smoke covered six layouts and three axe scans.
- First-run exception: the Wrangler npm version cache refreshed at 16:59:12 UTC despite both Cloudflare switches. This lookup concerned the Wrangler package version. The corrected harness's fresh-cache trace is in evidence/redesign/v103-owner-preview/cold-wrangler.json.
- Listener exception: the interrupted original package smoke left 127.0.0.1:8798 and :9798 listening. Its owning command session exited 130. Scoped pgrep and pkill in the subsequent command namespace returned exit 1. The owner was notified. The corrected harness passed occupied-port rejection, interruption and release of its own HTTP/inspector listeners.

Independent design/SEO review and the six owner gates in REVIEW_RESOLUTION.md remain open.

## 2026-11-21 targeted correction pass

The supplied branch started clean at 1467a2297a9d39c8301817f874bd7ed0e443bcb0. The linked worktree index rejected creation of index.lock on a read-only mount. Implementation and verification used an independent local clone on the same branch. The first commit contains only the two binding documents, compared byte-for-byte with the originals. The review transcripts remain at ../reviews/astra-final-review-1.log and ../reviews/astra-final-review-2.log relative to the implementation workspace.

Applied A1-02 and Amendment 1a, annotated both historical specifications, validated attribution and exercised unsigned and synthetic signed saves. The four-route correction captures cover 320, 375, 390, 768, 1024 and 1440 CSS pixels in both builds. The source lines and long hub cards wrapped within their containers. Captures and browser receipts are in evidence/redesign/corrections-2. The first capture attempt exposed an axe browser-context error. The corrected runner completed both builds with zero overflow and zero axe violations on the four routes at 390 px.

The first complete paired performance run met both median thresholds. An experimental E-PROPS CSS change was committed and reverted during analysis. Its incomplete timing run encountered a 404 during a rebuild and contributes no samples to the paired receipt. The delivered artifact has no stylesheet change. See DEFECT_REGISTER for the spreads and the reviewer's adapter observations.

Verification used the repository Python environment and pinned Node dependencies, Chromium 153, and the two offline Cloudflare environment switches. The requested npm suite ran with LCA_NOTICE_RETEST=1 to scope its route layout and axe loop. Both public and preview SHA-256 file manifests matched fresh checkout builds. The package check verified all 318 extracted hashes and 40 served HTML bodies. Firefox/WebKit executables, physical-device and field metrics, live provider delivery, notice owner sign-off, and independent design/SEO approval remain outside the verified engineering gates.
