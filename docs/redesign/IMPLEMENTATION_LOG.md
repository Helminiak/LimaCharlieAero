# Implementation log · v103 owner preview

## Recovery checkpoint

The local preview branch fast-forwarded from df5a3af to ad24972. Its tree matched the backup branch exactly. The saved remaining content was committed as 6ae8a47. The reconstructed index matched the saved tree object before that commit. The worktree-private index still has a read-only mount. The ordinary index reflects the old branch tip. Reconcile it to HEAD with a mixed reset in this worktree when writable, preserving working files.

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

Build and routing changes live in tools. Content, cases and registry records live in content. Markup, navigation, interactions and layout live in templates. Images and the self-hosted font live in assets-src. The review, license and evidence files document the preview. See the full per-file inventory below.

## Counts

Counts use whitespace-separated main-element text nodes, including disclosure contents, without the shared header or footer. Images count actual main-element placements. RC3 comparison files matched all 134 frozen hashes.

| Route | RC3 words | Public words | Preview words | Public change | RC3 images | Public images | Preview images |
|---|---:|---:|---:|---:|---:|---:|---:|
| / | 991 | 482 | 580 | -51.4% | 6 | 13 | 12 |
| /404 | 76 | 50 | 50 | -34.2% | 0 | 0 | 0 |
| /about-credentials | 115 | 100 | 100 | -13.0% | 0 | 1 | 1 |
| /aircraft-records-review | 916 | 865 | 865 | -5.6% | 1 | 3 | 3 |
| /card | 40 | 40 | 40 | +0.0% | 0 | 0 | 0 |
| /contact | 391 | 364 | 364 | -6.9% | 1 | 2 | 2 |
| /e-props-dealer-support | 1383 | 1331 | 1356 | -3.8% | 4 | 8 | 8 |
| /faq | 1225 | 1222 | 1222 | -0.2% | 0 | 0 | 0 |
| /image-credits | 128 | 105 | 105 | -18.0% | 0 | 0 | 0 |
| /joseph-helminiak-bio | 825 | 731 | 731 | -11.4% | 1 | 2 | 2 |
| /light-sport-experimental-avionics | 859 | 788 | 788 | -8.3% | 6 | 8 | 8 |
| /light-sport-prebuy-evaluation | 1000 | 929 | 929 | -7.1% | 2 | 3 | 3 |
| /our-work | 0 | 215 | 1415 | new | 0 | 5 | 8 |
| /owner-notices | 298 | 298 | 298 | +0.0% | 0 | 0 | 0 |
| /planning-service-downtime | 264 | 264 | 264 | +0.0% | 0 | 0 | 0 |
| /prebuy-first-inquiry | 273 | 273 | 273 | +0.0% | 0 | 0 | 0 |
| /privacy | 216 | 192 | 192 | -11.1% | 0 | 0 | 0 |
| /rotax-9-series-912-914-915-916-support | 856 | 804 | 804 | -6.1% | 2 | 3 | 3 |
| /rotax-912-carb-sync | 724 | 739 | 739 | +2.1% | 1 | 4 | 4 |
| /rotax-912-high-oil-temperature | 673 | 669 | 669 | -0.6% | 1 | 3 | 3 |
| /rotax-912-mag-drop-troubleshooting | 699 | 711 | 711 | +1.7% | 0 | 3 | 3 |
| /rotax-915-916-turbo-ems-support | 741 | 761 | 761 | +2.7% | 0 | 3 | 3 |
| /rotax-cooling-oil-temperature-problems | 713 | 706 | 706 | -1.0% | 1 | 3 | 3 |
| /rotax-engine-systems-support | 1060 | 1164 | 1164 | +9.8% | 2 | 18 | 18 |
| /rotax-fuel-pressure-fuel-delivery-problems | 850 | 779 | 785 | -8.4% | 3 | 4 | 4 |
| /rotax-gearbox-notice | 224 | 224 | 224 | +0.0% | 0 | 0 | 0 |
| /rotax-gearbox-propeller-vibration | 984 | 880 | 880 | -10.6% | 6 | 7 | 7 |
| /rotax-ignition-ecu-electrical-faults | 836 | 797 | 797 | -4.7% | 3 | 5 | 5 |
| /rotax-installation-review | 953 | 879 | 887 | -7.8% | 6 | 7 | 7 |
| /rotax-rubber-hose-replacement-fluid-leaks | 971 | 920 | 920 | -5.3% | 2 | 3 | 3 |
| /rotax-turbocharger-notice | 170 | 202 | 202 | +18.8% | 0 | 0 | 0 |
| /s-lsa-e-lsa-maintenance | 995 | 993 | 997 | -0.2% | 0 | 3 | 3 |
| /security-disclosure | 107 | 82 | 82 | -23.4% | 0 | 0 | 0 |
| /service-area | 868 | 773 | 773 | -10.9% | 1 | 2 | 2 |
| /services | 1179 | 1326 | 1326 | +12.5% | 4 | 11 | 11 |
| /start-with-the-symptom | 275 | 275 | 275 | +0.0% | 0 | 0 | 0 |
| /support-request | 368 | 379 | 379 | +3.0% | 0 | 1 | 1 |
| /thank-you | 95 | 70 | 70 | -26.3% | 0 | 0 | 0 |
| /the-lima-charlie-aero-standard | 1226 | 1242 | 1242 | +1.3% | 3 | 7 | 7 |
| /updates | 489 | 489 | 489 | +0.0% | 0 | 0 | 0 |

Distinct main-content photographic sources or subjects, RC3 / public / preview: 39 / 53 / 54.

- / (-51.4%). The copy deck moves five service descriptions and their link rows to /services and replaces duplicate founder material with a single founder band. Draft case copy is available in preview.

## Verification

| Build | Routes | Files | Checks | Internal references | Errors |
|---|---:|---:|---:|---:|---:|
| dist | 40 | 192 | 3416 | 1892 | 0 |
| dist-preview | 40 | 195 | 3436 | 1904 | 0 |

Simulated mobile Lighthouse, 0 of 9 routes measured on this candidate. Home, Services, E-PROPS, ROTAX, vibration, installation, prebuy, request and Our Work have no candidate scores. Runtime, overlay contrast, focus, height, screenshot matrix and frozen design review remain open. Current-date review found 12 overdue draft-backlog entries and zero overdue published notices.

The screenshot and browser invocations both stopped during Wrangler startup at the sandbox config-directory write. No updated screenshots were produced. The prior ten images in /tmp/lca-first-shots are pre-correction. The final height and performance numbers must be measured on the corrected build. The next run needs a writable Wrangler config directory such as a task-local XDG_CONFIG_HOME under /tmp.

## Changed source and evidence inventory

Changes through the code and test commits, relative to the redesign brief baseline. This table excludes this report and its sibling evidence registers.

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
| A | docs/redesign/REVIEW_CLAUDE_INTERIM_1.md |
| A | docs/redesign/licenses/Archivo-OFL.txt |
| A | docs/redesign/licenses/Archivo-source.md |
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
| A | tools/metadata.py |
| M | tools/package_release.py |
| M | tools/performance.mjs |
| A | tools/render_site.py |
| M | tools/verify_auxiliary.mjs |
| M | tools/verify_browser.mjs |
| M | tools/verify_release_features.mjs |
| M | tools/verify_static.py |
