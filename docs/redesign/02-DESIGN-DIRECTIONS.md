# Design directions A and B: comparison and recommendation

Both directions use the existing wordmark and the same set of authentic shop photographs. Prototypes are home pages only: `design/proto/a/index.html` and `design/proto/b/index.html`. Renders at 390 px and 1440 px are in `evidence/redesign/directions/`.

## Direction A: "Technical Logbook" (refined aviation technical)
- **Surface:** warm paper `#f5f3ee`, navy ink, hairline rules, a single safety-orange accent.
- **Type:** IBM Plex Sans with IBM Plex Mono for labels, figure numbers and measured values.
- **Hero:** split layout. The headline sits beside an evidence plate set (Fig. 1 installation, Fig. 2 measured 1.27 IPS, Fig. 3 logbook entry).
- **Signature modules:**
  - a line-drawn **system map** with the aircraft at the centre and ten surrounding systems;
  - an indexed service list (SVC-01…06);
  - "case files" with a stage rail (Problem → … → Records) and status stamps;
  - a before/after measurement strip.
- **Character:** reads like a disciplined maintenance manual: precise and credible.

## Direction B: "Flight Line" (premium aviation service)
- **Surface:** full-bleed dark photographic hero, deep navy and night, warm sand sections, orange pill CTAs.
- **Type:** Archivo (condensed width axis) for display, system UI for body text.
- **Hero:** the studio ROTAX photograph full-bleed. The headline reads "Light-sport & experimental aircraft, *worked as a complete system*."
- **Signature modules:**
  - photo service tiles with text over the image;
  - a full-bleed split band carrying the systems-of-systems statement and system chips;
  - editorial **case stories**, each with a three-image mosaic (finding, repair, document), step list and status pill;
  - a three-step "How it works";
  - a founder band and a closing dark CTA.
- **Character:** approachable, confident, clearly a working shop.

## Evaluation (0–10)

| Criterion | A | B | Notes |
|---|---:|---:|---|
| Trust & technical credibility | 9 | 8 | A's figure captions and measured values are the strongest credibility device |
| Brand differentiation | 8 | 8 | A's system map is explicit. B's band statement and case mosaics are more memorable |
| Visual composition | 7 | 9 | B has rhythm: full-bleed, split, mosaic, tiles |
| Mobile readability | 7 | 8 | A's mono text is small at 390 px and its header CTA wraps. B stacks cleanly, but its tiles add length |
| Service discovery | 7 | 9 | B's photo tiles restore production's best pattern |
| Inquiry conversion | 7 | 8 | B gives a larger CTA presence and a clear three-step path |
| Authenticity | 9 | 8 | Both use only real photos. A labels evidence more rigorously |
| Accessibility | 8 | 7 | B's text-over-photo needs scrim and contrast control on every tile. A is simpler |
| Performance feasibility | 9 | 7 | B's full-bleed hero is the LCP element, so it needs responsive AVIF/WebP of 120 KB or less |
| Implementation/maintenance | 8 | 7 | A needs fewer layout primitives |
| **Owner steering fit** (PR #2: "too sterile", "documentation portal", "restore photographic richness") | 5 | 9 | A risks repeating the RC3 critique |
| **Total** | **84** | **88** | |

## Recommendation: Direction B, carrying three components from A

B directly answers the owner's documented objection to RC3 and restores production's strongest pattern, the photo problem-grid. A's strengths are its evidence components, not its overall atmosphere. These carry over without making the site look like a manual:

1. **Evidence figures:** monospace figure labels with measured values ("Measured 1.27 IPS → 0.04 IPS after correction") for proof images on service and case pages.
2. **Case stage rail:** Problem → Configuration → Evidence → Evaluation → Action → Verification → Documentation, with completed stages filled and pending stages outlined. This is the accessible status model for case studies.
3. **System map diagram:** inline SVG with no JavaScript, used on The LCA Standard and Services. The home page keeps B's lighter chip list.

## Mandatory corrections to B before implementation (found in the renders)

| ID | Defect in prototype | Correction |
|---|---|---|
| D-B1 | At 390 px the hero eyebrow collides with the overlaid header | The header becomes a solid bar on mobile, or the hero gets top padding of at least the header height plus 24 px |
| D-B2 | Five stacked service tiles at 390 px add about 1,400 px | Tiles become a 2-column compact grid at 560 px or below with min-height 180 px, or a single "problem" list with thumbnails |
| D-B3 | Wordmark is too small over the photo | Wordmark at least 180 px on desktop, on a subtle navy plate |
| D-B4 | Text over photos | Gradient scrim tested to at least 4.5:1 for body text and at least 3:1 for large text at every breakpoint; never rely on photo darkness |
| D-B5 | Hover zoom on tiles | Keep it subtle. Disable under `prefers-reduced-motion` (already done) |
| D-A1 (if A is chosen) | Header "Request Service" wraps at 390 px | Use a shorter label ("Request") or icon plus label at 360 px or below |

Codex must independently assess feasibility before implementation. See `docs/redesign/CODEX_FEASIBILITY.md`.
The owner keeps final design approval. Direction A remains available as a prototype for comparison.
