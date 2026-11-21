# Production vs RC3 baseline audit (Claude design review)

Reviewer: Claude Opus 5.5 (claude-opus-5-5) in Claude Code. Effort set by the harness and not self-reportable; see the effort note in `README.md`.
Date: 2026-11-20. Method: read-only. Live site rendered with Chromium 153 (Playwright 1.63) at 390 px and 1440 px. RC3 rebuilt from `1521869` and served locally with `tools/preview.py`. Screenshots are in `evidence/redesign/baseline/`.
This review was written before Codex's Phase 1 engineering audit was read.

## 1. Baseline identity (VERIFIED)

| Item | Result |
|---|---|
| `main` | `6d9f82c`: 4 governance-only commits on top of `3d48ea6` (v100.2.5F import). No site bytes changed. |
| Rollback reference `3d48ea6` | Present on `main`. |
| RC3 `1521869` | Head of `rc3-proof-of-work-seo`. PR #2 is open, draft and unmerged. |
| RC3 rebuild | `python tools/build.py` gives 39 HTML / 134 files. **All 134 SHA-256 match `evidence/deployment-manifest.json`.** |
| Production vs `main` | **Not identical.** Live serves **v101.1.5i**: a different `styles.min.css` with appended `!important` mobile-order hotfixes, an inline `<style id="lca-mobile-trust-common-order-hotfix-v101-1-5h">` on the home page, and a new OG image (`lca-social-rotax-specialist-v101-1-5I-1200x630.png`). Cloudflare email obfuscation is injected at the edge. *Correction after the Codex audit (finding accepted): the raw HTML diffs on privacy, security-disclosure, prebuy, contact and faq are presentation and metadata only. Normalized `<main>` text matches rollback on all 27 captured pages.* None of these production changes are in Git. |
| Live headers | HSTS preload, `X-Frame-Options: SAMEORIGIN`, `CSP: upgrade-insecure-requests` only, `Permissions-Policy`, `Referrer-Policy`. |

Consequence: the production rollback point `3d48ea6` is **not** what is live. Rolling back to it would revert the v101.1.5i hotfixes and the new OG image. This is recorded as risk R-01.

## 2. What each baseline does well and badly

### Production (v101.1.5i)
Strengths
- Strong first-screen identity. The dark header, ROTAX lockup, orange CTA and a visible **ASB alert bar** make it read as a working shop.
- Photo-led "Most Common Problems We See" grid. Owners find their problem quickly by picture. This is the best service-discovery pattern in either baseline.
- Rich real photography, about 70 distinct subjects in the asset pool, including the hangar, people at work and the engineering paperwork.

Weaknesses
- The founder-centric voice ("Owner-operated aircraft support", Joe in the hero carousel) is prohibited by AGENTS.md and the brand rules.
- Hero carousel (5 slides) costs accessibility and performance, and most visitors never see slides 2 to 5.
- Mobile layout is held together by stacked `!important` `order:` overrides. This is fragile and not maintainable.
- Long pages: E-PROPS is about 16,700 px at 390 px wide.
- Hand-edited HTML, not a source of truth in Git.
- Systems-of-systems positioning and engineering case studies are absent.

### RC3 (v102.0.0-RC3, frozen)
Strengths
- Engineering discipline: deterministic build, structured content, schema, canonical tags, zero axe violations historically, lab performance 100, consistent Request/Call/Text CTA triad.
- Company-first voice, honest proof captions and privacy masks.
- Good intent-based entry: "Something feels wrong / Service is due / Buying / Propeller or avionics".

Weaknesses (owner-confirmed in PR #2 comment 6019369438)
- **Sterile, "documentation portal" feel.** Long stacks of H2 plus a paragraph plus a link row, with uniform proof-card grids. Home is about 12,500 px tall at 390 px.
- Fewer photos (38 subjects), most shown at small card size. The intent cards have no imagery.
- One generic header style and one hero pattern. There is no full-bleed photography and no visual rhythm.
- **Editorial defects verified in source** (`content/pages.json`, `index`):
  - The founder name is malformed: `Joseph “the shop” Helminiak`.
  - Authoring text leaks into public copy: "The RFSC listing **in the supplied source** shows…".
  - Duplicate leadership sections: "Technical Leadership" and "Technical leadership, company responsibility" on the same page.
- The owner notices `rotax-gearbox-notice` and `rotax-turbocharger-notice` are past their `next_review` (2026-10-12). The build reports this as a warning.
- The owner-directed case studies (SeaRey, Vashon R7, TL-2000, Sling 2, the forensic-maintenance example) are **not implemented**.
- Nav has 6 items plus a CTA, including "Owner answers". "Our Work" and "About / The LCA Standard" do not appear as top-level destinations.

## 3. Scored comparison (design and IA view; 0–10)

| Criterion | Weight | Production | RC3 | Note |
|---|---:|---:|---:|---|
| Trust & technical credibility | 15 | 6.0 | 7.5 | RC3 is more precise; prod has the ASB bar but a founder-centric voice |
| Brand differentiation (systems-of-systems) | 15 | 3.5 | 5.0 | Neither shows the method visually |
| Visual composition & hierarchy | 12 | 6.5 | 5.0 | RC3 is uniform text stacks; prod is busy but alive |
| Authentic photography | 10 | 8.0 | 5.0 | Prod pool about 70 subjects; RC3 38, mostly at small size |
| Mobile readability | 10 | 5.0 | 6.5 | Prod depends on `!important` hotfixes; both are very long |
| Service discovery | 10 | 7.5 | 6.5 | Prod photo problem-grid works best |
| Inquiry conversion path | 10 | 6.5 | 7.5 | RC3 has a consistent CTA triad and a support form |
| Accessibility (design-level) | 8 | 5.0 | 7.5 | Prod carousel; RC3 axe 0 (historical) |
| Performance feasibility | 5 | 5.5 | 9.0 | RC3 lab 100 (historical); prod not measured in this pass |
| Maintainability | 5 | 2.5 | 7.0 | Prod hand-edited and diverged from Git |
| **Weighted total** | 100 | **5.6** | **6.4** | |

Neither baseline meets the success criteria. RC3 wins on engineering and truthfulness. Production wins on warmth, photography and problem-first discovery. The redesign keeps RC3's architecture and evidence discipline and brings back production's photographic, problem-first character. It also adds what neither has: a visible systems method and real case studies.

## 4. Privacy and authenticity observations on the image pool

| Asset | Observation | Disposition |
|---|---|---|
| `proof-light-sport-aircraft` | Legible foreign registration **SE-VAK**. Nothing shows this is LCA work. | **Exclude** (tail-number rule plus authenticity) |
| `tl-ultralight-designer-correspondence` | Email screenshot shows correspondent names and contact lines | Use only redacted. Owner to confirm |
| `ndt-radioactive-material-license` | Third-party license document with addresses | Exclude from the redesign; low value |
| `hangar-prop-two-person-inspection` | Identifiable faces of people other than the founder | Owner to confirm consent before use |
| `contact-owner-aircraft-hero-blend-v2` | Identifiable person, not the founder | Owner to confirm consent before use |
| `eprops-aircraft-installed-sky-ranger-hero` | Blurred-background composite of a small source image; low quality | Do not use as a hero |
| `garmin-g5-installed-panel-close` | **Registration `[registration redacted]` legible on panel placard** (found by Codex) | **Mask before any use**; regenerate all derivatives |
| `rotax-support-hero-original-photo` | High-quality dark studio ROTAX image, 1600×900, with clear space for text | **Primary hero candidate** |

The owner attestation (PR #2 comment 6019001980) clears publication **rights**. It does not clear **privacy** of third parties or the tail-number rule (comment 6019938344). Codex must verify EXIF and XMP for registrations.

## 5. Reconciliation with the Codex Phase 1 audit (read after this review was recorded)

| Codex finding | Disposition |
|---|---|
| **P1: `[registration redacted]` legible on the placard in `garmin-g5-installed-panel-close`** (RC3 and production) | **Accepted. Missed in this review.** Added to the privacy table: mask before any use. `garmin-g5-installed-panel-wide` was inspected at full size and has no placard |
| Production page diffs are presentation-only | **Accepted.** Factual correction made in §1 |
| SEO regressions: 7 → 1 share images, less specific titles, contact/service-area schema loss | **Accepted** into the design spec §10 |
| Image placement density: home 19 → 6, services 11 → 4, E-PROPS 11 → 4 | **Consistent** with this review's "sterile" finding |
| Privacy grammar "So We can respond" | **Accepted**: new defect not in this review |
| Native form allows a reply-less inquiry | **Accepted** (P1 intake) |
| Budgets: font 40 KB or less; hero 75 KB mobile / 150 KB desktop; home and E-PROPS LCP 1.8 s or less | **Adopted.** These are stricter than this review's draft, which allowed 45 KB of font and 2.5 s |
| Case pages need a route-contract change | **Resolved:** one new hub route `/our-work`. Cases render as sections there and as summaries on service pages. Per-case routes are deferred until owner fact-check (see spec §6) |
