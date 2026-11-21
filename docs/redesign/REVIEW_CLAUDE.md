# REVIEW_CLAUDE: Phase 9 independent design review of frozen candidate `7d2e68e`

**Reviewer.** Claude Opus 5.5, design lead. The session's reasoning effort is set by the harness and cannot be self-verified, so it is not claimed as xhigh. This review was written **without reading REVIEW_CODEX.md**.

**Candidate.** `7d2e68eb8bbf401df023424203d896ecaefd5e2f` on `redesign/v103-owner-preview`, frozen. Codex xhigh is reviewing it independently in a detached worktree.

**Method.**
- Exported the candidate with `git archive` into an isolated copy and built it both ways:
  - public: 40 HTML pages, 318 files, no review warnings;
  - `--preview`: 40 HTML pages, 324 files.
- Served both locally with `tools/preview.py`.
- Captured Chromium 153 full-page screenshots:
  - preview build: 10 pages × 320/375/390/768/1024/1440;
  - public build: home and Our Work at 390/1440.
- Inspected the 390, 1440 and 320 captures segment by segment.
- Automated checks on 12 routes × 6 widths: overflow, target size and broken images.
- Grepped the public build for leaks.
- Did a pixel check of the restored G5 wide image.
- Did not re-run Lighthouse or axe myself. Codex's numbers are cited as Codex's.

## Verified independently

| Check | Result | Status |
|---|---|---|
| Page heights reproduce Codex's report exactly | 390: home 6,784, services 4,625, E-PROPS 5,729, Our Work 6,000, Standard 6,774. 1440: Our Work 7,873 (≤8,000) | VERIFIED |
| Horizontal page overflow | None at any of 6 widths on 12 routes. The prebuy table scrolls inside its labelled region | VERIFIED |
| Small targets | Header utility links now pass (R2-08 closed). The only hit is the honeypot input, which is clipped with `clip-path: inset(50%)` and 1 px wide, so it is invisible and not a defect | VERIFIED |
| Broken images | 0 | VERIFIED |
| Draft leakage into the public build | 0 pages containing `OWNER CONFIRM`, `OWNER DECIDE` or `PRIVATE PREVIEW`. No Vashon, SeaRey or Sling case text. No correspondence image in `dist/assets` | VERIFIED |
| Registration patterns | None in the preview HTML (regex `N[0-9]{1,5}[A-Z]{0,2}`). The restored `garmin-g5-installed-panel-wide` (1600×900) was inspected at full size: no placard or registration visible, and no EXIF/XMP | VERIFIED |
| Interim #1 and #2 findings | CD-01…CD-11 and R2-01…R2-09 closed by visual inspection. Document figures have "Open full size". Our Work uses a centred column with a wider figure grid. No same-page image repeats | VERIFIED |
| Regulatory text | The turbo notice cites AD 2026-22-03 (eff. 2026-11-23, certified 915/916 iSc, before further flight). The notice bar's wording is acceptable | VERIFIED |

## Findings

| ID | Sev | Class | Where | Finding | Required correction |
|---|---|---|---|---|---|
| CR-01 | **P1** | factual / acceptance | **Public build**: `/our-work` (title "Our Work: Light-Sport & Experimental Aircraft Case Studies"; lead "Each case shows what was found…") and home "Real aircraft. The whole paper trail. Each example follows the same path…" | All five cases are drafts, so **the public build contains no case**. Both pages promise case records and then show a generic 4-photo evidence grid. If shipped as-is, the copy claims content that does not exist. That falls under the master prompt's "do not invent… repair results" spirit and is misleading to owners and to search. | Add a zero-approved-case variant, driven by data, with no hand edits per page. Our Work title becomes "Our Work: Evidence from Light-Sport & Experimental Aircraft". The lead describes the photographs and measurements, plus one line: "Detailed case records are published after owner review." Home section heading becomes "From the hangar floor" with no "each example follows" sentence. Keep the 7-stage legend, which is a method description and is accurate. Add a test that public copy contains no "each case"/"each example" when the public case count is 0. Alternative, as an owner decision: remove `/our-work` from the primary nav until ≥1 case is approved (route kept). |
| CR-02 | P2 | factual (visual semantics) | Home preview "Real aircraft", Sling navy panel. `templates/site.css:212-213` | **The stepper's done/pending encoding is inverted on navy.** `.done` is a navy fill on a navy panel, so it reads as an empty outline. `.pending` keeps its white fill, so it reads as the highlighted step. The Sling case shows only "6 · Verification · pending" as filled, which is the opposite of the truth and the opposite of Our Work. | `.case-panel .stage-rail .done { background: white; color: var(--navy); }` and `.case-panel .stage-rail .pending { background: transparent; color: white; }`. Add a visual or computed-style assertion that done ≠ pending fill on every rail context. |
| CR-03 | P2 (pre-existing RC3) | factual (copy) | `light-sport-experimental-avionics` ("…understandable. Avionics / Electrical"), `joseph-helminiak-bio` ("…Credentials / Boundaries"), `rotax-installation-review` ("…Propeller / Gearbox Interface") | A legacy section label is glued onto the end of a body paragraph in `content/pages.json`. This is present in RC3 `1521869`. | Remove the trailing label text from those three paragraphs. Add a static check for a paragraph ending in `Title / Title` with no terminal punctuation. |
| CR-04 | P3 | aesthetic | Our Work "How we document the work" at 1024–1440 (public and preview) | The legend renders as 7 narrow columns. "Documentation" breaks mid-word ("Documentatio / n") with no hyphen, and "Configuration" nearly does too. | Use a 4+3 layout (`repeat(4, 1fr)` at ≥1024), or keep 7 across only when each column is ≥150 px, with `hyphens: manual` and `overflow-wrap: normal` on `b`. |
| CR-05 | P3 | aesthetic | Home system band, Standard hero, Our Work hero (both builds) | The canopy field-work photo is the lead image on three prominent placements. On Our Work it is the first image an owner sees, yet it is context, not evidence. | Lead Our Work with an evidence subject not otherwise used on the page, e.g. the DynaVibe reading or the refinished mount. Keep the canopy photo on home and Standard. |
| CR-06 | P3 | aesthetic | Our Work TL-2000 Verification FIG. 05 (NDT excerpt) | The excerpt is still a small strip in a 3-column grid. "Open full size" keeps it acceptable. | Optional: span 2 columns for `document` figures at ≥1024. |
| CR-07 | Info (owner copy pass) | aesthetic / tone | Contact and some service pages, long-form RC3 body copy | Lines such as "An online description or photograph is not a flight-readiness decision" and "A message starts an inquiry; it does not book an appointment or authorize maintenance" remain in body text. They are reasonable and not captions, but they keep the cautious register the owner pushed back on. | No action for Codex. List them for the owner's copy review. |

No P0. Release status: **Approve as owner-preview candidate with conditions**, conditional on CR-01 (P1) and CR-02/CR-03 (P2) being corrected and re-verified. The P3 items are recommended but do not block the owner preview.

## Gates outside this review (unchanged; not overridable by consensus)
- Owner fact-check of all case records (CS-1…CS-6). Vashon and the forensic case are BLOCKED on owner input or permission.
- Photo permissions: third-party faces, the correspondence image, restored-image rights.
- LSRM-A trained category/class, E-PROPS dealer status and iRMT listing currency.
- The live site still serves the unmasked G5 placard image. That needs an owner action on production; it is outside this branch.
- Firefox and WebKit (BLOCKED: no executables), physical devices, screen readers, Formspree inbox delivery and field CWV: UNTESTED or external.
