# DESIGN_ROTAX_NOTICES v1: ROTAX owner-notice redesign (Claude, design lead, 2026-11-21)

**Status:** design spec plus static mockup, awaiting **owner approval**. Implementation goes to Codex (Astra Medium) **after** the Phase 9 correction checkpoint: the Astra High review and the fixes for Addendum 1. It must not interrupt or alter the running correction workflow.

**Mockup:**
- Generator: `design/notices-mockup/make_mockup.py`. It rewrites a copy of the `1467a22` public build and is never committed as implementation.
- Screenshots: `review-shots/notices/`
  - `home-notice-1440.png` and `home-notice-390.png` (crops of the home module);
  - `mock-*-390.png` and `mock-*-1440.png` (full pages).
- Zero horizontal overflow at 390 and 1440 on all three pages.

## 1. Source verification (done 2026-11-21, ROTAX publication library `rotax.my.salesforce-sites.com/DocumentsSearch`)

| Field | SB-2026-003 | SB_A-2026-003 |
|---|---|---|
| Title | Optional extension of Time Between Overhaul (TBO) from 1200 h to 2000 h on ROTAX 915 iSc (Series) Aircraft Engines | … on ROTAX 915 iS (Series) Aircraft Engines |
| Engines | Certified: 915 iSc A from S/N 10006805; 915 iSc C24 from S/N 10012483 | ASTM: 915 iS A from S/N 10006742; 915 iS C24 from S/N 10010510 |
| Issue / revision | 10 November 2026, Initial Issue (library rev 0) | same |
| ROTAX category | **OPTIONAL** ("no unsafe condition, advancement but no need to implement") | same |
| Approval | DOA ref. EASA.21J.048 | BRP-Rotax QMS (ASTM) |
| Library file | d07277.pdf · `…/download/068Mm00000gKyW5IAK?asPdf=false` | d07275.pdf · `…/download/068Mm00000gKpJ8IAK?asPdf=false` |

Conditions (§1.1, §3.1), all required **since hour 0**:
- XPS AIRCRAFT 5W50 oil for the life of the engine;
- a maximum oil temperature of 120 °C from initial entry into service;
- maintenance per the approved instructions.

Otherwise the 1200 h TBO applies.

Other requirements:
- §3.2: the aircraft OEM must establish the 120 °C limit and the XPS-only oil rule for the aircraft type.
- §1.7: the measures may affect aircraft certification.
- §3.3: additional gearbox and rocker-arm-bushing items apply to 2000 h engines.
- §3.4: execution must be confirmed in the logbook.
- §3: only authorized persons may carry out the work (iRMT Line/Heavy, distributors and service centres, or authority-approved persons).

**Latest publication check.** A library search (ASB/SB/SL/SI, Oct–Dec 2026) covered 912 UL, ULS, S, iS Sport, 914 UL, 915 iS A, 915 iSc A, 916 iS A and 916 iSc A. Nothing is newer than 10.11.2026. The only other recent item is SI-912-037 / SI-912 i-034 / SI-914-042 R1, issued 14.10.2026 (round-neck nut, informational). The owner's identification of SB-2026-003 / SB_A-2026-003 as the latest is **confirmed**.

**Secondary-source discrepancy (record only, do not publish).** AvBrief gives the 915 iSc A serial as "100006805". The ROTAX PDF says **10006805**. Use the PDF.

**Re-verify at implementation time:**
- the ASB-2026-001 / ASB_A-2026-001 current revision (site says R01, 2026-07-02; the AD cites R00);
- the ASB-2026-002 / ASB_A-2026-002 revision (library shows rev 1, 11.09.2026);
- the ROTAX category on each.

## 2. Information architecture

1. **Home, one featured module**, replacing the current two-link `notice-strip`:
   - **Latest ROTAX Technical Update**: publication date, engine-family chips, ROTAX category chip, an FAA AD chip ("No FAA AD" / "FAA AD nnnn"), a plain-language explanation, an amber applicability box, **Request Applicability Review** (primary), "What it means for your engine" (secondary) and the original-bulletin links;
   - photo from the approved proof pool;
   - below it, a compact **"In effect: FAA airworthiness directives"** list (one line per AD in effect), which keeps safety items discoverable without competing visually;
   - then a link to the archive.
2. **Site-wide notice bar**: shows only safety-critical items in effect (FAA ADs / mandatory ASBs flagged `prominence: safety`). Copy: "Two FAA airworthiness directives are in effect for certain certified ROTAX engines. Check applicability" → `/owner-notices#in-effect`. It never advertises routine or optional bulletins.
3. **`/owner-notices`, the hub and archive**, in this order:
   - "Airworthiness directives in effect" (cards);
   - "Latest ROTAX technical update";
   - "Reference archive" table with columns Document · Rev/issued · Engines · Category · Status · Source checked;
   - the "maintained selection, not a complete database" line with a library link.

   Older notices stay reachable and indexable. Nothing legally relevant is removed.
4. **Detail page per update**, new route `/rotax-915-tbo-extension`. It has a fact panel (dl) and six numbered sections that answer the owner's questions verbatim:
   - What changed?
   - Does it affect my engine? (serial-number table, hour-0 conditions, and an OEM-adoption note)
   - What records or identification are needed?
   - What should I do next?
   - Where can I read the original bulletin?
   - How can Lima Charlie Aero help? (navy help box with CTA)

   It also carries a **"This bulletin does not replace any directive"** callout.

## 3. Data model (extend `content/updates.json` notice records; build-validated)

Required on every `type: notice` record:

| Field | Description |
|---|---|
| `documents[]` | `{number, variant: certified\|astm, revision, issue_date, url, library_file}` |
| `engine_families[]` | e.g. `["915 iS", "915 iSc"]` |
| `serial_ranges[]` | `{engine_type, from_sn}` (optional) |
| `rotax_category` | `mandatory\|obligatory\|recommended\|optional` |
| `faa_ad` | `{number, effective_date, applicability_note, url, corrections[]}`, or `null` |
| `severity` | `safety\|routine\|optional`. Derived: `safety` iff an FAA AD is present or `rotax_category == mandatory` |
| `status` | `current\|ad_in_effect\|superseded\|archived` |
| `prominence` | `featured\|safety\|archive`. Exactly one `featured` record. Every `faa_ad` with `status: ad_in_effect` must be `safety` (it cannot be `archive`) |
| `source_verified` | ISO date |
| `next_review` | ISO date |
| `owner_question` | |

Build rules (each needs a negative test):
- R1: exactly one `featured`.
- R2: no record with an FAA AD in effect may have `prominence: archive`.
- R3: a featured record whose `severity` is `optional` or `routine` must not hide `safety` records. Home must render every `safety` record in the "In effect" list.
- R4: `source_verified` must not be older than `next_review` at build time; if it is, fail or warn.
- R5: every `documents[].url` must be an official ROTAX or FAA/FR host.
- R6: no copy may say "compliant", "airworthy", "safe to fly", "cleared" or "eligible" unconditionally on a notice page. The allowlisted phrase is "can be considered".
- R7: the newest bulletin must never carry `supersedes` pointing at an AD or ASB of a different subject.

## 4. Copy and governance rules
- Plain-language, factual, no defensive captions. Applicability is stated once per surface: the amber box on home and section 2 on the detail page.
- Never mark an engine compliant or give flight-readiness guidance from the family name.
- No "reviewed by" or technical-review attribution. Use the source line only: "Prepared from the ROTAX bulletins linked above. Published … · Source checked …"
- **LCA help copy** is limited to reviewing records against the bulletin. It must **not** claim that LCA may perform or sign the bulletin (that is iRMT/authorization currency, owner gate 3) until the owner confirms.
- For a split SB/SB_A pair, label certified and ASTM explicitly everywhere. In the archive table, a row's FAA AD reference applies to the certified variant only, so show "FAA AD 2026-22-03 (certified)". The mockup merges this and implementation must split it.
- Form: keep `topic=notice`. Rename the option label from "ROTAX owner notice" to **"ROTAX bulletin or notice: applicability review"**, so owners need no document number. Keep the existing legacy mapping and the X-05 own-key guard.

## 5. Presentation (v103 system)
- Featured module: white card on sand, 5/7 photo/text split at ≥900 px, stacked below. Chips use existing tokens. The amber applicability box uses `--amber`. The "In effect" list uses a light terracotta tint (`#fff4ee` / `#f0b89c` / text `#7a2a08`). Contrast must be measured as ≥4.5:1 (CD-12 method).
- Implementation notes from the mockup review:
  - at ≥1200 px, put the two CTAs on one row (they stack at 1440 in the mockup because of column width);
  - the serial-number table at 390 should keep "from 10006805" on one line (`white-space: nowrap` on the S/N cell);
  - the "In effect" chip in the mockup uses display-font tracking that is too tight; use the body font.
- Photo: `xps-oil-rotax-filter-service` (proof pool, already public). Caption: "Oil type is one of the records this bulletin depends on."
- No new fonts and no JS. Lighthouse budgets unchanged. Add the new route to the sitemap, canonical, OG and JSON-LD (`Article` + `about` the engine family). Add the detail route to the axe and six-width matrix.

## 6. Dependencies and gates
- Depends on Addendum 1. The AD 2026-22-03 effective date is **November 4, 2026**, and the AD 2026-16-11 applicability wording is corrected. The "In effect" lines in this design already use the corrected facts.
- Owner gates:
  1. approval of this design and the copy;
  2. LCA's authority to perform or sign SB work (iRMT currency);
  3. the photo already has public rights in the pool, so no new gate.
- No merge or deploy.
