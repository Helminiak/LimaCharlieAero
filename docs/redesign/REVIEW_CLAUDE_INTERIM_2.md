# Claude interim design review #2: v103 candidate `8be6714`

Reviewer: Claude Opus 5.5 (design lead). This is still an interim review (spec §11), not the Phase 9 frozen review.

Method:
- Exported `8be6714` with `git archive` into an isolated copy and built it with `tools/build.py --preview` (40 HTML pages, 195 files, no review warnings).
- Served it with `tools/preview.py` on 127.0.0.1:8093.
- Captured 8 pages at 320/375/390/768/1024/1440 in Chromium (48 full-page captures in `review-shots/c2/`) and inspected the 390 and 1440 captures segment by segment.
- Ran an automated overflow, target-size and broken-image check on 12 routes at 6 widths.
- Grepped the built HTML for registration patterns.

## Interim #1 status

| ID | Status | Evidence |
|---|---|---|
| CD-01 letterboxing | **Closed on mobile and on home/E-PROPS/Standard. Regressed on Our Work desktop** (see R2-01) | No grey frames remain. Cover crops keep cracks and welds in frame |
| CD-02 defensive captions | Closed | Captions are factual |
| CD-03 disclosure piles | Closed | E-PROPS has 4 themed disclosures, sentence case |
| CD-04 E-PROPS repeat and chips | Closed | 6 chips, new FIG. 04 subject |
| CD-05 Our Work stepper and length | Closed on mobile: 6,155 px at 390, stepper with collapsed records. Desktop is 13,809 px (R2-01, R2-05) | |
| CD-06 notice bar, home height | Closed | Two-line notice. Home is 6,667 px at 390 (target ≤7,000) |
| CD-07 mosaic | Mostly closed | 1+2 cover mosaic. Text-only card is lopsided (R2-07) |
| CD-08 FIG on context photo | Closed | |
| CD-09 targets | Partial | Header utility links are 19 px at ≥1024 (R2-08) |
| CD-10 footer email | Closed | "Email the shop" |
| CD-11 prebuy table | Closed | `.table-wrap` has tabindex=0, role=region and aria-label; no page overflow at 320 |
| CD-12 overlay contrast | Open (Codex measurement) | Looks fine by eye |

Heights at 390: home 6,667, services 4,725, E-PROPS 5,423, Our Work 6,155, Standard 6,997, ROTAX hub 6,466, prebuy 5,607, support-request 3,326. **All are within the spec §9 targets.** There is no horizontal page overflow at any width, no broken images, and no registration pattern in the preview HTML.

## New findings

| ID | Sev | Where | Finding | Required correction |
|---|---|---|---|---|
| R2-01 | **P1** | Our Work ≥768, inside the expanded "Full case record" (TL-2000 Action stage, and any single figure in a stage) | A single **portrait photo renders at full container width and natural aspect**: about 760 px wide by 1,000+ px tall at 1440. It dominates the page, and Our Work is 12,499 px at 1024 and 13,809 px at 1440. | Stage figures always sit in the figure grid (2-up, or 3-up at ≥1024). A single figure takes one grid column (≤50% width) and `max-height: 560px`. Portrait images never span the full content width. Target Our Work ≤8,000 px at 1440 with records expanded. |
| R2-02 | P2 | E-PROPS "From the work" FIG. 01/02. Standard "The paper trail" FIG. 04/05 | **Document excerpts are too small to read.** The NDT findings excerpt is about 30 px tall in a 180 px column. The packet fan-out and checklist are thumbnails. A document figure that cannot be read does not work as evidence. | Document figures span the full row (or 2 columns) at a width where body text in the excerpt is ≥11 px rendered, **or** link to the full-size redacted derivative (`<a href>` around the figure, with the caption noting "Open full size"). Do not upscale beyond the source. |
| R2-03 | P2 | Our Work | The hero image (`weld bead follows the joint`) is the same image as TL-2000 FIG. 02 on the same page. | Use a different subject for the Our Work hero: e.g. the refinished mount (FIG. 07), the E-PROPS packet, or a wide shop context photo not used elsewhere on the page. No image appears twice on one page. Add a build check for this. |
| R2-04 | P2 | Our Work | **"What this does and does not show" appears 5 times**: 4 per-case boxes plus the page-level box. Three of the per-case boxes repeat the generic page text verbatim. This is the defensive tone the owner rejected, by repetition. | Keep the single page-level box. Keep a per-case box **only** when its text is case-specific (TL-2000's "Repair data and acceptance are specific to this aircraft and this finding" qualifies). Remove the generic duplicates. |
| R2-05 | P2 | Our Work ≥1024 | Case content sits in a ~540 px left column with the right half empty for screen after screen. The stage text then alternates with full-width images. | At ≥1024, use a two-column case layout: stages on the left (≤62ch), and that case's evidence figures in a right column (sticky top or flowing). Alternatively, center a single 72ch column with the figure grid at full container width. Pick one and apply it to all cases. |
| R2-06 | P3 | Our Work "How we document the work" (5+2), Standard "How we work" (4+3) and "The paper trail" (4+1), E-PROPS "From the work" (uneven heights) | Grid widows and ragged figure rows. | Steps: use a 7-column compact row at ≥1200, or 4+3 with a balanced explicit template. Figures: `align-items: start` with a uniform aspect for photos (4:3 cover) and documents on their own row (R2-02). |
| R2-07 | P3 | Home "Real aircraft" (desktop) | The Sling (text-only) case shows a lone stepper floating in an empty left column. It is lopsided against the TL-2000 mosaic. The TL-2000 card has no stepper, so the cards are inconsistent. | Both cards get the stepper. A text-only case uses a navy panel matching the mosaic height, with the stepper and the status pill inside. Alternatively, use a 2-card row with an image strip on top only where images exist. |
| R2-08 | P3 | Header utility bar ≥1024 | "Call 980.382.1344" and "Text the Shop" are 19 px tall standalone links (WCAG 2.5.8). | `min-height: 24px; display: inline-flex; align-items: center` (padding-block). |
| R2-09 | P3 | Standard paper trail captions | "The painted cage view records its visible finish and condition." and "This view documents the weld and joint condition." are awkward, and FIG. 01–03 repeat the home and Our Work TL-2000 images. | Caption = what is shown: "The engine mount after refinishing." Prefer one TL-2000 image plus non-TL subjects here (e.g. rotax records or the E-PROPS packet), so the Standard page shows breadth instead of a third copy of the same case. |

## Not defects (confirmed)
- The turbo notice page includes AD 2026-22-03 (eff. 2026-11-23, certified 915/916 iSc, before further flight). The site-wide notice bar names the two ASBs and links to "Check applicability". This is acceptable.
- E-PROPS FIG. 04 (`eprops-blade-damage-closeup`) is an RC3 subject with the owner rights attestation. The caption matches its RC3 description.
- `[OWNER CONFIRM]` markers and the PRIVATE PREVIEW pills appear in preview only.

## Acceptance to request the frozen review
- R2-01 through R2-05 are corrected, together with Codex's own closed-loop findings.
- The six-width matrix has been re-captured.
- Our Work at 1440 is ≤8,000 px with the records expanded, or the deviation is justified in the register.
