# Claude interim design review #1: v103 candidate (Codex review history `ad24972` plus uncommitted worktree edits, snapshot 2026-11-20 21:02)

Reviewer: Claude Opus 5.5 (design lead). This is a mid-implementation review (spec §11, "Claude may inspect rendered screenshots"). It is **not** the Phase 9 frozen-candidate review.
Method: `tools/build.py --preview` built in an isolated copy (40 routes, 193 files). Served with `tools/preview.py`. Chromium 153 captures at 320/375/390/768/1024/1440 for 8 pages (48 full-page captures), plus an automated overflow/target/image check on 12 routes × 6 widths.

## Overall
**Strong direction match.** Compared with RC3 and production:
- The home page reads as a working shop: full-bleed ROTAX hero, photo tiles, system band.
- The system map works on the Standard page.
- The case stage model is implemented.
- Draft isolation and noindex are correct.
- 390 px heights: home 7,104 (RC3 12,524), services 6,076 (RC3 11,618), E-PROPS 6,528 (RC3 12,187).
- No horizontal page overflow at any width. No broken images.

The candidate is **not yet visually acceptable**. One systemic image-presentation defect and one content-structure defect hold it back.

## Findings (fix in this order)

| ID | Sev | Where | Finding | Required correction |
|---|---|---|---|---|
| CD-01 | **P1** | Interior heroes (Standard, Our Work, E-PROPS, others), case figures, paper trail, home case mosaic | **Portrait photos are letterboxed in wide grey frames** (`object-fit: contain` on a fixed-aspect box). Up to about 60% of each frame is empty grey. Small documents (the NDT table excerpt, the packet fan-out) become tiny bands inside tall boxes. The result looks unfinished and undoes the photographic gain. | Interior hero: a 4:3 `cover` crop with a per-image `focal` (object-position) field in `proof-assets.json`, **or** the image at its natural aspect with `max-height: 560px` and no frame background. Case and evidence figures: natural aspect in a 2- or 3-up grid with `align-items: start`. **No grey padding.** Use `contain` only for document excerpts, and size the box to the excerpt's own aspect. Keep `cover` crops away from cracks, readings and document fields (Codex's crop-policy rule). |
| CD-02 | **P1** | All figure captions, notably Our Work FIG. 01/05/08, Standard FIG. 03/04/06, home FIG. 03 | **Defensive, legalistic captions return**: "The image does not independently establish the repair approval or inspection result", "A facility photograph is not a test report", "a record of appearance, not proof of structural acceptance", "not approval for another aircraft". The owner rejected exactly this tone in PR #2 (Design/SEO correction 1). The "What this does and does not show" box already carries the boundary once per case/page. | Captions state **what the image shows**, in one factual sentence: "Crack at the lower-left diagonal joint, photographed before any work." Remove the negations from captions. The single limits box per page or case remains. |
| CD-03 | **P2** | Standard (17 items), E-PROPS (22 items: "Service details" plus a second list), other service pages | **Legacy RC3 sections are piled into long `<details>` lists.** The content is retained but not designed: titles mix Title Case and sentence case, some end in periods, and one is "01 — authorization first". Owners will not open 22 disclosures. | Consolidate per COPY_DECK/spec §4: map each legacy section into a template slot (Is this you / What to send / How we approach it / Limits) or into **at most 4 themed disclosures** per page. E-PROPS themes: *Fitment & ordering · Authorization path · Installation & verification · Warranty, damage & returns*. Standard themes: *Method in detail · Records & traceability · Certificate boundary*. Sentence case, no trailing periods. Report word counts per page (the >35% reduction rule from the spec still applies, with reasons). |
| CD-04 | P2 | E-PROPS | Hero photo repeated as FIG. 04 in "From the work" (also noted by Codex). "Aircraft & systems involved" shows only Propeller and Approvals. | Replace FIG. 04 with `eprops-blades-box-documents` or `eprops-customs-spinner-documents` from the pool. Chips: Propeller, Engine & gearbox, Airframe, Vibration, Records, Approvals. |
| CD-05 | P2 | Our Work | Stage rail renders as underlined link chips wrapping onto 2 rows. Done and pending differ only by border style. At 390 px the page is 13,902 px. | Rail = a compact stepper: `<ol>`, numbered dots (filled = done, outlined = pending, visually-hidden status text), **not links**. Optional: an anchor list above the cases. Each case shows a summary (title, pill, rail, Problem, a 2-image strip) with the remaining stages in one `<details>` "Full case record", **open by default on desktop ≥1024 px and closed on mobile**. Target ≤7,000 px at 390. |
| CD-06 | P2 | Home 390 | Notice bar takes 3 lines (about 80 px) on mobile. Home is 7,104 px against a ≤7,000 target. | Mobile notice copy: "ROTAX gearbox & 915/916 turbo notices · Check applicability" (one or two lines). That plus the CD-01 mosaic fix should clear the target. |
| CD-07 | P2 | Home case mosaic (desktop) | The TL-2000 card's 3-image mosaic has empty grey cells. The Sling card has no images, so the section is lopsided. | With CD-01 applied: mosaic = 1 large plus 2 small in `cover` crops with focal points. Text-only cases use a consistent text card with the stage rail as its visual element. |
| CD-08 | P3 | Home system band | "FIG. 01" mono label on a context photo. The caption "Coordinate aircraft location and access before planning work" reads as an instruction. | Use FIG labels only on evidence figures. Context photo caption: "Field work under a canopy at the ramp." |
| CD-09 | P3 | Notice bar, "Read the case", "How we work →", footer lists, breadcrumb | Standalone links are 18–23 px tall (WCAG 2.5.8 needs 24 px minimum unless the inline/spacing exception applies). | `min-height: 24px` (44 px preferred on mobile) with inline-flex padding for standalone links. Footer list items get a `0.35rem` block padding. |
| CD-10 | P3 | Footer at 375/390 | Email wraps mid-address ("support@limacharlieae / ro.com"), also noted by Codex. | `overflow-wrap: anywhere` is not acceptable here. Let the contact column span the full width at ≤420 px, or use the link text "Email the shop" with the address in `title` and `vCard`. |
| CD-11 | P3 | Prebuy at 320 | The table is wider than the viewport inside its wrapper. | Confirm the wrapper is `overflow-x: auto` with `tabindex=0`, `role=region` and an `aria-label`. Alternatively, stack the rows as definition lists at ≤480 px. |
| CD-12 | Info | Tiles, hero | Text over photo looks well-scrimmed by eye. | Codex: measure the worst-case contrast of tile title text against the lightest 10% of pixels under the text box at each breakpoint, and record it. |

## Not defects (confirmed)
- Draft cases display `[OWNER CONFIRM …]` markers and the ribbon in preview only. Public build isolation was reported VERIFIED by Codex. Claude will re-check this in the frozen review.
- The CS-1 stage status "Verification · done" is supported by the designer's written confirmation. The rest of the CS-1 facts remain owner-gated.

## Acceptance to request the frozen review
CD-01 through CD-07 are corrected and re-captured at all six widths. The spec §9 height targets are met, or deviations are justified in the defect register.
