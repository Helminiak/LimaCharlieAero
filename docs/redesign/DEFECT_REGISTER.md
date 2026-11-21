# v103 redesign defect register

## Engineering disposition

The engineering retest closed the 25 findings from the two interim design reviews and the existing Codex register, plus two verification defects found during this loop. Counts include overlapping findings when reviewers assigned separate IDs.

| Severity | Closed | Open engineering |
|---|---:|---:|
| P0 | 0 | 0 |
| P1 | 4 | 0 |
| P2 | 15 | 0 |
| P3 | 8 | 0 |

The independent design and SEO decisions belong to Phase 9. The owner retains the publication and case-fact gates. The frozen inputs to this review are [interim review 1](REVIEW_CLAUDE_INTERIM_1.md) and [interim review 2](REVIEW_CLAUDE_INTERIM_2.md).

## Interim review 2

Review 2 inspected `8be6714`, which was also the starting HEAD of this session. The prior session left working files and measurements. Its report file was empty. Only the newly built and tested artifacts support the dispositions below.

| ID | Severity | At session start | Correction and retest |
|---|---|---|---|
| R2-01 | P1 | A partial width cap remained in the dirty CSS. Stage evidence still escaped a consistent grid. | Evidence captions identify their stage. Desktop case photos use one of three columns with 4:3 crops and a 560 px cap. The five expanded records fit under 8,000 px. |
| R2-02 | P2 | Four document flags and caption links were present in the working tree. The desktop excerpt still defaulted to a 300 px image. | The complete document and its visible “Open full size” label are a single link to the redacted original. Width is capped at source pixels. Related documents share a desktop row and use the mobile row width. |
| R2-03 | P2 | 18 of 40 preview pages repeated a subject, including the weld in the Our Work hero. | Our Work opens with the canopy photo. Changed conflicting context images and directory thumbnails while retaining the underlying case and service evidence. All 80 generated pages pass. Verification compares both subject IDs and hashes of fallback and responsive assets across placements. A fixture using a real alternate subject ID and the same photo bytes failed solely on the duplicate-image check. |
| R2-04 | P2 | Four draft cases repeated the page-level limits text. | All five stage narratives remain. Only the TL-2000 case carries a case-specific limits box. The page-level limits appear once. |
| R2-05 | P2 | Expanded records alternated narrow left-aligned copy with oversized images. | Each record uses the centered 72ch narrative option, with a split introductory summary on desktop and a wider photo grid. Copy, stage order and status survive the layout change. |
| R2-06 | P3 | Auto-fit columns left uneven final rows. | Seven short legend items share one desktop row. The Standard’s longer method entries use an explicit 4+3 arrangement. The gallery pairs document figures, top-aligns rows and uses 4:3 crops for ordinary photographs. Instrument readouts retain their natural aspect. |
| R2-07 | P3 | Only the text-only card showed progress and its left column was largely empty. | Both home cards have seven status dots. The Sling case pairs its status and stepper in a navy panel at the mosaic height on desktop. No speculative case image was added. |
| R2-08 | P3 | Both desktop utility links measured 19 px high. | Inline-flex targets have a 24 px minimum and vertical padding. Neither utility link appears in the final matrix’s under-24 px list. |
| R2-09 | P3 | Standard repeated three TL-2000 photographs. | The paper trail shows the refinished mount, masked logbooks, NDT excerpt and E-PROPS packet. The mount caption identifies the visible condition. |

## Earlier findings and retest

| ID | Severity | Final disposition |
|---|---|---|
| CD-01 | P1 | Interior context and case photos use focal crops. Documents and readouts keep their natural proportions. Inspected the mosaic, stage grid, instrument pairs and redacted document links. |
| CD-02 | P1 | Factual captions describe the visible evidence. The limits are confined to the page or the case-specific record. |
| CD-03 | P2 | E-PROPS and Services each use four themed disclosures. The Standard uses three. Per-route counts and the home copy reduction are in the implementation log. |
| CD-04 | P2 | E-PROPS has six system chips and distinct pictures of the propeller, packet, checklist, shipping carton and blade damage. |
| CD-05 | P2 | All five records start collapsed at 390 px and expanded at 1440 px. Verified keyboard close/reopen and expanded-state axe. |
| CD-06 | P2 | The shortened notice fits in two lines at 390. Home clears its height ceiling and its first service action is visible without scrolling. |
| CD-07 | P2 | The photographed card has a 1+2 mosaic. The text-only case has the navy status panel. |
| CD-08 | P3 | The canopy band uses its field-work caption. Figure numbers are reserved for evidence and case figures. |
| CD-09 | P3 | Notice, breadcrumb, section, utility and footer targets were measured at six widths. The capture inventory also flags inline form-helper text and the separately spaced vCard page email link. |
| CD-10 | P3 | Small-screen footer reads “Email the shop.” The full address is present in the destination and vCard. |
| CD-11 | P3 | The named prebuy comparison region accepts focus and scrolls via ArrowRight at 320 px in both builds. |
| CD-12 | P1 | Initial desktop minima were 2.39, 2.74 and 2.05. The retained scrim change passed all six widths on the final hero crops. See the six-width pixel table in the implementation log. |
| CD-13 | P2 | The footer telephone link previously exceeded the 320 px viewport by 38 px at 200% text. Both browser suites passed the enlarged-text check. |
| CD-14 | P2 | The mobile Menu previously wrapped at 320 px. The wordmark and utility padding now keep the normal header on one row. |
| CD-15 | P2 | Document evidence uses linked originals and mobile row width. Singleton portraits are capped on desktop. See R2-01 and R2-02. |
| CD-16 | P2 | Optimized the image candidates and mobile hero. The final Lighthouse table and transfer diagnosis are in the implementation log. |
| QA-01 | P2 | In a ten-capture intermediate pass, 15 photo regions had a uniform fill even after decode. The capture and contrast tools now scroll through the page, request synchronous image paint, return to the top and wait for compositor frames. Rechecked encoded screenshots as well as DOM geometry. The final matrix had zero suspect blank regions in 715 visible photo placements and zero dimension mismatches across 240 files. |
| QA-02 | P2 | Concurrent public and preview runners contended for port 8788. One preview form run stopped after eight checks with `net::ERR_CONNECTION_REFUSED`. A concurrent capture later reported `failed: bind(): Address already in use (os error 98)` at the shared inspector. Concurrent startup on the shared ports was BLOCKED. Dedicated HTTP and inspector ports resolved the collisions. Browser tests also verify served HTML and case count against the selected build. The final suites exercise all form branches. |

## Scope of independent review

No factual, methodological, aesthetic or acceptance-criteria dispute with Claude’s findings. The session-3 backup and later on-disk results described different points in the test run. The handoff uses fresh final receipts.

Owner review covers the five draft histories, image-to-case associations, the Vashon excerpt and correspondence permission, 15 restored subjects with rights marked REVIEW REQUIRED, current dealer/training evidence and authorization scope. Current-date editorial verification found 12 overdue draft backlog entries and zero overdue published notices. Real-device and assistive-technology testing, independent design/SEO sign-off, live provider delivery and field CWV remain external gates.


## Infrastructure record

| Boundary | Status | Evidence |
|---|---|---|
| Worktree index during grouped commands | BLOCKED in two invocations | `fatal: Unable to create '/home/joe/work/lca-redesign/repo/.git/worktrees/codex-impl/index.lock': Read-only file system`. Initial commits used the existing separate-index workflow. Later standalone Git add and commit invocations succeeded, bringing the ordinary index up to date. |
| Firefox | BLOCKED in both build suites | `Error: browserType.launch: Executable doesn't exist at /home/joe/.cache/ms-playwright/firefox-1543/firefox/firefox` |
| WebKit | BLOCKED in both build suites | `Error: browserType.launch: Executable doesn't exist at /home/joe/.cache/ms-playwright/webkit-2359/pw_run.sh` |
| Wrangler local Request.cf cache | PARTIAL | Wrangler logged `Error: ENOENT: no such file or directory, mkdir '/home/joe/work/lca-redesign/codex-impl/node_modules/.mf'` and used its default placeholder. The static site uses no Functions. Asset serving, routes, redirects and headers ran locally. |
