# LCA v103 redesign: design specification (Direction B "Flight Line" + A evidence components)

Owner: Claude (design lead). Implementer: Codex. Status: **DRAFT FOR CODEX FEASIBILITY AND OWNER APPROVAL**.
Reference prototype: `design/proto/b/index.html`, with corrections D-B1 to D-B5 from `02-DESIGN-DIRECTIONS.md`.
Architecture: RC3 static build (`tools/build.py`, `content/*.json`, `templates/`) is retained. No framework, no CMS.

---
## 1. Design principles
1. **A working shop first, engineering discipline second, and both visible.** Real aircraft and hands at work come before documents.
2. **Problem-first discovery.** An owner who does not know the diagnosis finds a starting point within one screen.
3. **Evidence is shown, not asserted.** Measured values, redacted documents and status labels sit next to the claim they support.
4. **Every image earns its place.** Each one has a page-specific purpose and caption. There is no stock imagery, no AI imagery and no decorative-only photos in proof slots.
5. **Calm interface.** No carousels, auto-play, parallax, scroll-jacking, decorative gradients or dashboards.

## 2. Tokens

| Token | Value | Use / contrast (checked against stated background) |
|---|---|---|
| `--night` | `#08182a` | hero/footer/final CTA background |
| `--navy` | `#0e2a47` | bands, header plate; white text 14.6:1 |
| `--sand` | `#f3eee5` | alternate section background; `--ink` on sand 14.9:1 |
| `--white` | `#ffffff` | default background |
| `--ink` | `#111c27` | body text on white 17.2:1 |
| `--ink-2` | `#44515e` | secondary text on white 8.1:1, on sand 7.0:1 |
| `--orange` | `#d9531e` | primary CTA fill. White text on it is **4.0:1, which fails for normal text**. **Use `--orange-d #b6400f` (5.6:1) as the CTA fill for 16–18 px labels.** `--orange` is used only for large display text or non-text accents |
| `--orange-d` | `#b6400f` | CTA fill, link accent on white 5.6:1, on sand 4.9:1 |
| `--amber` | `#f2b134` | display highlight on dark only (9.5:1 on `--night`); focus ring |
| `--line` | `#e1d9cb` | rules on sand/white |
| success / pending | `#1d5c33` on `#e6f1e9` (6.9:1); `#7a4c00` on `#fbefd6` (6.4:1) | case status pills |

Codex must re-measure every pair with the built CSS. These values were computed at design time.

**Type**
- Display: **Archivo**, variable, `wdth` 75–100 and `wght` 600–800. Self-host one Latin-subset woff2 of **40 KB or less** (Codex budget). Use `font-display: swap` and a metric-matched fallback (`size-adjust`) so it causes no CLS.
- Body: system UI stack. No body web font.
- Mono (evidence labels only): `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace` from the system. No web font.

| Scale | Size |
|---|---|
| H1 | clamp(2.4rem, 6vw, 5rem), 800, stretch 85% |
| H2 | clamp(1.9rem, 3.8vw, 3.2rem) |
| H3 | clamp(1.35rem, 2.2vw, 1.8rem) |
| Body | 17 px (16 px at 560 px or below) with line-height 1.65 |
| Eyebrow | 0.8rem, 700, letter-spacing 0.14em |

Maximum line length is 68 ch for running text.

**Spacing and grid**
- Spacing scale: 4/8/12/16/24/32/48/64/96/112.
- Container: 1240 px max with gutter `clamp(16px, 4vw, 48px)`.
- Grid: 12 columns at 1024 px and above; single column below 760 px.
- Section padding: `clamp(64px, 9vw, 112px)`.

## 3. Components

| Component | Spec | Accessibility |
|---|---|---|
| **Header** | Desktop: transparent over the dark hero on the home page only, solid `--night` everywhere else. Mobile at 1020 px or below: solid bar, 64 px high, wordmark, a compact "Request" button and a Menu button. Sticky: no. | Disclosure-pattern nav with `aria-expanded`; Esc closes and focus returns. Visible without JS: a `<details>` or `:target` fallback |
| **Primary nav** | Services · ROTAX · E-PROPS · Our Work · About · **Request Service** (CTA). Phone and Text move to a utility row on desktop and into the menu on mobile. | Current page marked with `aria-current="page"` |
| **Hero, home** | Full-bleed `hero-rotax`, LCP image. Separate AVIF/WebP crops for 640, 1024 and 1600 px (the source is 1600×900; no upscaling). The scrim gradient keeps text at 4.5:1 or better. The 390 px crop is art-directed (`<picture>` with `object-position` 80%). Holds an eyebrow, H1, lede and 2 CTAs. | `alt=""` because the image is decorative behind the text. A nearby evidence figure carries the real alt text |
| **Hero, interior** | Split layout: copy on the left and one page-specific photo on the right (4:3). Breadcrumb above the H1. Light sand background. | |
| **Problem tiles** | Photo with text over it plus a scrim. Desktop: 12-column mosaic (7/5, then 4/4/4). At 560 px or below: 2-column compact tiles, min-height 180 px, title only (fixes D-B2). Each tile is a single link. | The whole tile is one `<a>` with heading text. Contrast is checked on the darkest and lightest crop |
| **System band** | Split layout: full-bleed photo plus a navy panel holding the statement and system chips. Chips are static text, not buttons. | |
| **System map** | Inline SVG from A, with the aircraft at the centre and 10 systems. Used on the LCA Standard and Services. | `<title>` plus an ordered list equivalent next to it |
| **Evidence figure** | A photo with a mono label ("FIG. n"), a measured value where one exists, a one-sentence caption, and a privacy note if redacted. | Alt text describes the subject. The caption carries the meaning |
| **Before/after pair** | Two evidence figures with a shared caption: "Measured 1.27 IPS → 0.04 IPS after correction". | |
| **Case story card** | Mosaic of 3 images (finding, action, document), eyebrow (aircraft type), H3, step list, status pill and link. | Status is in text, not colour alone |
| **Case stage rail** | Problem → Configuration → Evidence → Evaluation → Action → Verification → Documentation. Completed stages are filled; pending stages are outlined and include the word "pending". | `<ol>` with visually-hidden status text |
| **Notice bar** | Amber bar under the header, shown only while an owner notice is active. One sentence plus a "Check applicability" link. No dismiss requirement. | Not `role=alert`, because it is static |
| **CTA triad** | Request Service (primary), Call, Text. On mobile, full width and stacked. | 48 px minimum target |
| **Request form** | Existing RC3 form and validation retained. Restyled only: 48 px inputs, labels above fields, error text below fields with `aria-describedby`, and a summary at the top on submit. A server-side fallback is required (see the defect register). | |
| **Footer** | Night background with 4 columns: company/address, services, company, contact. Legal row below. | |

Removed or forbidden:
- the production carousel;
- `!important` order overrides;
- RC3's generic bordered proof-card grid as the default image treatment (allowed only on dense evidence pages);
- any founder-centric CTA.

## 4. Information architecture

```
Home
├─ Services (hub)                 /services
│   ├─ ROTAX (hub)                /rotax-engine-systems-support
│   │   ├─ 9-Series overview, carb sync, high oil temp, mag drop, 915/916 turbo & EMS,
│   │   │  cooling/oil temp, fuel pressure, gearbox/prop vibration, ignition/ECU,
│   │   │  installation review, rubber/hose          (all existing routes retained)
│   ├─ Inspections & S-LSA/E-LSA  /s-lsa-e-lsa-maintenance
│   ├─ Prebuy                     /light-sport-prebuy-evaluation
│   ├─ Records review             /aircraft-records-review
│   ├─ Avionics & electrical      /light-sport-experimental-avionics
│   └─ Vibration & balancing      → anchor in /rotax-gearbox-propeller-vibration (no new route)
├─ E-PROPS                        /e-props-dealer-support
├─ Our Work (NEW hub)             /our-work
│   └─ cases render as anchored sections /our-work#<slug> (per-case routes deferred until owner fact-check)
├─ About                          /the-lima-charlie-aero-standard  (About + The LCA Standard)
│   ├─ Founder                    /joseph-helminiak-bio
│   ├─ Training & qualifications  /about-credentials
│   └─ Service area               /service-area
├─ Owner notices & answers        /owner-notices, /updates (+ records)   (footer + notice bar, not top nav)
├─ FAQ                            /faq  (footer)
└─ Request Service                /support-request  → /thank-you
```

- **No route is deleted.** RC3's 39 routes are retained. `start-with-the-symptom` keeps its URL and becomes the home page's problem-tile destination.
- New route: `/our-work` only (route contract 39 → 40). Per-case routes come later, after owner fact-check. Sitemap and schema follow the RC3 conventions (`CreativeWork`/`Article` for cases, with no `Review` and no `AggregateRating`).
- Top-nav "Owner answers" is removed. It stays reachable from the footer, the notice bar, the ROTAX hub and contextual links.

### Service-page template (applies to every important service page)
1. Hero: H1 naming the problem or service, one-sentence lede, CTA triad, page-specific photo.
2. **"Is this you?"**: the symptoms or situations this page covers.
3. **"Aircraft & systems involved"**: chips plus a short paragraph.
4. **"What to send us"**: a checklist of the information to provide. This replaces repeated prose.
5. **"How we approach it"**: 3–5 numbered steps.
6. **"From the work"**: 2–4 evidence figures specific to this page.
7. **"Authorization & limits"**: a short, plain-language box. Text comes from the regulatory register (§7) and the page's existing boundary text.
8. Related case story (if one exists) and related pages.
9. Closing CTA.

**Repetition rule:** boilerplate boundary sentences ("a website description is not approval…") appear **once per page** in the limits box. Existing RC3 prose is mapped into this template, de-duplicated and kept substantive. Codex should report word counts before and after for each page. A drop of more than 35% on any page needs an explicit reason, per the RC3 content-retention register.

## 5. Page compositions (priority pages)

| Page | Hero image | Key modules |
|---|---|---|
| Home | `hero-rotax` full-bleed | trust strip → problem tiles (6) → system band (`cowling`) → Our Work (2 case stories) → how it works → owner notice card (if active) → founder band (`founder`) → final CTA |
| Services | `hoses` | intro → system map → service index with thumbnails → "you don't need a diagnosis" → CTA |
| ROTAX hub | `eng-green` | symptom index (11 routes as compact thumbnail list) → notices → evidence (`coolant`, `fuel-dirty`, `diffpress`, `gearbox`) → CTA |
| E-PROPS | `eprops-close` | goal → fitment picture → **authorization path stage rail** → evidence (`eprops-packet`, `eprops-checklist`, blade damage) → Sling 2 / TL-2000 case links → limits → CTA. **Target: 50% or less of the current RC3 scroll height at 390 px** |
| LCA Standard / About | `cowling` | statement → system map → 5-step method → paper trail (logbook, NDT report, redacted packet) → founder → qualifications → service area |
| Our Work | `cage-weld` | intro + case-structure legend → case cards (status visible) → "how we document" |
| Case page | case-specific | breadcrumb → H1 (aircraft type + process) → status pill → stage rail → 7 sections (Problem…Documentation), each with 0–2 evidence figures → "what this does and does not show" box → related service → CTA |
| Request Service | `founder` or `hangar-two` (owner consent pending) | short reassurance → form → what happens next |

## 6. Engineering case-study register

Publication rule: a case is published only after the **owner confirms the facts against the source records**. Until then it is built behind a `"state": "draft"` flag (RC3 already excludes drafts from public output) and shown only in the private preview.

| ID | Public title (no registration) | Source of record | Evidence images available | Status claim permitted | Gate |
|---|---|---|---|---|---|
| CS-1 | TL-2000 Sting Sport: engine-mount crack, repair-vs-replace and NDT | Owner steering (PR #2 comments 6019840432 and 6019938344); live images `engine-cage-*`, `ndt-magnetic-particle-report`, `tl-ultralight-designer-correspondence` | crack, weld, joint, NDT facility, NDT report (redacted), painted, designer correspondence (**redact names**) | "Documented repair process: finding → designer coordination → repair → magnetic-particle inspection → records" | **OWNER FACT-CHECK**: repair instruction source, re-work/re-test occurrence, return-to-service wording. **Mask registration in all images** |
| CS-2 | Sling 2 / ROTAX 912 iS: E-PROPS qualification with the airframe manufacturer | Owner steering (comment 6019938344) | Generic redacted E-PROPS packet and checklist images; **confirm they belong to this job, otherwise use text only** | "In progress: pending manufacturer review and validation" | OWNER FACT-CHECK. Document numbers (EP-2026-712, DUR-3-175-C4-T, TCDS P.512) default to **not published**; owner decides |
| CS-3 | TL-2000 Sting Sport / ROTAX 912: E-PROPS DURANDAL-3 qualification and installation verification | Owner steering (comment 6019938344) | `eprops-install-checklist-*`, `dyna-*` (only if from this aircraft) | "Controlled qualification and verification process". **No final-authorization claim** unless the record shows one | OWNER FACT-CHECK on authorization status and on which balance readings belong to this aircraft |
| CS-4 | Vashon Ranger R7: manufacturer-coordinated fuel evaluation | Owner steering (comment 6019588967); packet LCA-ENGINEERING-2026-006 Rev A **not available locally** | none in pool; owner may supply a redacted packet cover | "Engineering evaluation submitted to the airframe and engine manufacturers; disposition pending." Must state that the two hazards (detonation margin; installed fuel-delivery/vapor margin) are evaluated separately | **BLOCKED on owner** supplying the redacted packet excerpt and confirming manufacturer-correspondence publication permission |
| CS-5 | SeaRey: return-to-service systems evaluation | Owner steering (comment 6019588967) | none in pool | "Return-to-service evaluation plan." **Not** a completed return to service | OWNER FACT-CHECK; photos needed or text-only |
| CS-6 | Forensic maintenance: records against as-found condition | Owner steering (comment 6019840432) | none identified | — | **BLOCKED**: aircraft type unknown. The public copy must identify the type, not the registration |

The case template enforces "What this does and does not show". Pending work is never shown with a filled "Verification" stage.

## 7. Regulatory and authorization register (verified 2026-11-20)

| Claim area | Verified source | Site wording rule |
|---|---|---|
| ROTAX gearbox ASB | Rotax ASB-2026-001R00 (22 Jun 2026) and R01 (2 Jul 2026), as cited in RC3 `updates.json` | Existing RC3 notice is accurate. Keep it and update `last_review` |
| FAA AD 2026-16-11 (Amdt 39-23441, Docket FAA-2026-7235, **eff. 28 Aug 2026**) | GovInfo FR 2026-08-13 (text read) | Applies to **type-certificated** 912 F/S/A/iSc and 914 F engines on listed TC aircraft (Table 1) with listed gearbox serials. **It does not cover ASTM 912 UL/ULS/iS Sport engines.** For those the Rotax ASB applies through the LSA/engine manufacturer path. RC3 wording already says this; keep it |
| ROTAX turbo valve-housing ASB | Rotax ASB-2026-002 (3 Sep 2026), R01 (11 Sep 2026) | RC3 notice OK for the ASB |
| **FAA AD 2026-22-03 (Amdt 39-23505), eff. 23 Nov 2026**, via EASA Emergency AD 2026-0178-E | GovInfo FR 2026-11-02 PDF (text read) | **NEW, not in RC3.** Applies to 915 iSc2 C24, 915 iSc3 C24, 916 iSc2 A, 916 iSc2 C24, 916 iSc3 A, 916 iSc3 C24 engines (certified). Required before further flight after the effective date. Add it to `rotax-turbocharger-notice` sources and body. Non-certified 915/916 iS remain under the ASB |
| LSRM-A privileges | **14 CFR 65.109(b)** as amended by MOSAIC (Amdt 65-66, 90 FR 35220; eCFR 2026-11-18) | May approve for return to service **light-sport-category** aircraft after maintenance, including annual condition and 100-hour inspections, **excluding major repair or major alteration on a product produced under an FAA approval**. May perform the **annual condition inspection on experimental aircraft certificated under §21.191(g), (i), (k), (l)**. Maintenance is limited to the trained category/class. **Major repair requires additional FAA-acceptable training** (65.109(b)(3)). The owner must confirm the trained category/class and any major-repair training before the site claims structural repair capability |
| ROTAX iRMT / RFSC training | RC3 cites `rotaxirmt.com/irmt-place/7534` (not re-fetched this pass) | Wording: "ROTAX iRMT training: 9 Series Service, Maintenance and 912 iS installation, current through 16 Sep 2027 per the iRMT listing." **External re-check required** before publication |
| E-PROPS dealer status | Owner statement; RC3 copy | "E-PROPS dealer" is kept. Manufacturer-level decisions remain with E-PROPS. **Owner confirms dealer status is current** |
| Manufacturer coordination | Owner steering | Approved phrase: "We work directly with manufacturers and their engineering departments on aircraft-specific technical and authorization questions." No "approved by", "partner" or "certified by" language |

**Erratum, 2026-11-21.** The gearbox Table 1 pairing and type-certification condition apply to the listed A-series models. Both engine groups require a listed installed gearbox. FAA AD 2026-22-03 took effect November 4, 2026. Use A1-02 and Amendment 1a of [Resolution Addendum 1](REVIEW_RESOLUTION_ADDENDUM_1.md) for the regulatory wording, source references and attribution. Owner sign-off is pending.

## 8. Photography plan
- Target: **50–55 distinct useful subjects** across the site (owner guidance), up from RC3's 38. All come from the live/RC3 pool. None are excluded except those in the privacy table in `01-BASELINE-AUDIT-CLAUDE.md`.
- Every placement has: subject id, page, purpose (hero / context / evidence / case), page-specific caption, alt text, a crop focal point and a privacy check (registration, faces, documents).
- **Registration check:** every image used is visually inspected and EXIF/XMP-stripped by the build. Codex adds an automated metadata strip plus a manifest assertion.
- Responsive derivatives: 400/800/1200/1600 widths. AVIF plus WebP for heroes, WebP for others. Explicit `width`/`height`. `loading=lazy` except the LCP image.

## 9. Acceptance criteria (design)
1. At 390 px, a first-time visitor sees the business type, the location and a Request Service action without scrolling.
2. Home at 390 px is **at most 7,000 px** tall (RC3 12,524; production 8,005). E-PROPS at 390 px is at most 8,000 px (RC3 12,187; production 16,740).
3. Every important service page follows the §4 template, and no boilerplate boundary sentence appears more than once per page.
4. At least 4 distinct case structures are visible in the private preview. Pending cases show pending status in text.
5. No public tail numbers in copy, captions, alt text, filenames or metadata.
6. Contrast: all text at 4.5:1 or better (3:1 for large text); focus ring 3 px amber/navy, visible on all backgrounds.
7. No carousels, no auto-motion, and `prefers-reduced-motion` is respected.
8. RC3 master gates retained on the eight representative routes plus `/our-work` (controlled lab Lighthouse, simulated mobile): P 95 or better, A 98 or better, SEO 100, CLS 0.05 or less, TBT 100 ms or less, **home and E-PROPS LCP 1.8 s or less**, initial home transfer 350 KB or less. Hero caps: 75 KB mobile / 150 KB desktop. Field CWV are not available, so the targets are LCP 2.5 s, INP 200 ms and CLS 0.1 at p75 once data exists.
9. Claude's independent visual review at 320/375/390/768/1024/1440 reports no P0/P1 visual defects.

## 10. SEO restorations (from the Codex audit, accepted)
- Route-family social cards at 1200×630, reviewed with no registrations, with `og:image:width/height/type/alt`. Restore `max-image-preview:large` on indexable pages.
- Restore accurate search intent in titles: e.g. "Light-Sport Aircraft Prebuy & Records Review", "ROTAX 9 Series Support near Charlotte", "Light-Sport & ROTAX FAQ".
- Restore `ContactPage` on contact, `Service` on service-area, and the business-graph `areaServed`, `logo` and `sameAs` fields wherever current business evidence supports them.
- Map the legacy query `?request=rotax-asb-review` to the `notice` topic prefill.

## 11. Preview vs public build
- Case records with `state: draft` render **only** when the build is run with `--preview`. Preview output gets `noindex`, a visible "PRIVATE PREVIEW: owner fact-check required" ribbon on draft case sections, and is never packaged for deployment.
- The default (public) build must be identical in route set and draft exclusion to what verify_static expects.
