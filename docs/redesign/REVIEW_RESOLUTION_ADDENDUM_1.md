# REVIEW_RESOLUTION Addendum 1: regulatory copy corrections (Claude, 2026-11-21 12:40 EST)

**Trigger.** The Astra High final review of `1467a22` (interim notes, `reviews/astra-final-review.log`) flagged two regulatory problems before the session hit its usage limit at 12:23. Claude checked both against the primary sources and **confirmed both**. In both cases the error is Claude's: the design spec §7 table, COPY_DECK line 109 and the REVIEW_RESOLUTION X-04 copy block.

This addendum supersedes the affected copy blocks. The original documents are kept unchanged as the record.

## A1-01 · P1 · factual: the X-04 gearbox copy misstates who the AD applies to

**Source:** FAA AD 2026-16-11, Amendment 39-23441, 91 FR (August 13, 2026), paragraph (c), read from the local PDF of FR doc 2026-16512:

> "This AD applies to … Model 912 F2, 912 F3, 912 F4, 912 iSc2 Sport, 912 iSc3 Sport, 912 S2, 912 S3, 912 S4, 914 F2, 914 F3, and 914 F4 engines; and Model 912 A1, 912 A2, and 912 A3 engines installed on the aircraft identified in Table 1 to paragraph (c) of this AD that were included as part of the aircraft's type certification basis; with an installed propeller gearbox that meets the criteria of paragraphs (c)(1) or (2) of this AD."

The criteria in (c)(1) and (c)(2) are a gearbox serial number listed in ROTAX ASB-2026-001R00, Chapter 4 Appendix, at:
- §4.1, gearbox installed on delivery; or
- §4.2, gearbox supplied as a spare part.

**Error.** The binding copy attaches the Table 1 aircraft condition to every listed engine. In the AD, it applies **only to 912 A1/A2/A3**.

**Replacement copy for `/rotax-gearbox-notice`. Binding, verbatim:**

"FAA AD 2026-16-11 (effective August 28, 2026) applies to certified ROTAX 912 F2/F3/F4, 912 S2/S3/S4, 912 iSc2/iSc3 Sport and 914 F2/F3/F4 engines, and to 912 A1/A2/A3 engines installed on the type-certificated aircraft listed in the AD's Table 1, where the engine's propeller gearbox serial number is listed in ROTAX ASB-2026-001R00. It does not apply to ASTM-standard 912 UL, ULS or iS Sport engines. Owners of those engines should check ROTAX ASB-2026-001 and the aircraft manufacturer's instructions for applicability. Check your engine model, gearbox serial number and aircraft against the official documents linked below."

## A1-02 · P1 · factual: AD 2026-22-03 effective date is November 4, 2026, not November 23

**Sources:**
- FR doc 2026-22307, 91 FR 68882 (November 2, 2026):
  - the DATES heading reads "effective November 23, 2026";
  - paragraph (a) reads "effective November 4, 2026";
  - the incorporation by reference is approved "as of November 4, 2026".
- **Correction C1-2026-22307, 91 FR 74086 (November 18, 2026):** "On page 68882, in the third column, in the DATES section, 'November 23, 2026' should read 'November 4, 2026'." Read from thefederalregister.org's copy. The official copy is https://www.federalregister.gov/documents/2026/11/18/C1-2026-22307/airworthiness-directives-brp-rotax-gmbh-and-co-kg-formerly-brp-powertrain-gmbh-and-co-kg-and.
- The FAA DRS listing also shows an effective date of 11/04/2026.

**Error.** The rendered turbo notice says "effective November 23, 2026". The source line also says dates were checked on November 21. Both statements are false at `1467a22`. The AD **is already in effect**.

**Replacement copy for `/rotax-turbocharger-notice`. Binding, verbatim:**
- Regulatory sentence: "FAA AD 2026-22-03 (effective November 4, 2026) applies to listed certified 915 iSc and 916 iSc engines and requires the action before further flight; non-certified 915/916 iS engines remain under the ROTAX bulletin."
- Source line: "Prepared from the FAA AD, its November 18, 2026 Federal Register correction and the ROTAX bulletin linked below; dates and engine scope checked against those documents on November 21, 2026."
- Add the correction as an official source link, next to the existing AD link: https://www.federalregister.gov/documents/2026/11/18/C1-2026-22307/airworthiness-directives-brp-rotax-gmbh-and-co-kg-formerly-brp-powertrain-gmbh-and-co-kg-and

## Required engineering
- A static check must fail if the public or preview build contains "November 23, 2026" or "2026-11-23" together with "2026-22-03".
- A static check must fail if the superseded X-04 wording ("engines installed in the type-certificated aircraft listed in the AD's Table 1") reappears in either build. It must also fail if the A1-01 sentence is absent from `/rotax-gearbox-notice`.
- Each check needs an injected-failure record.
- Record the design-spec and copy-deck errors in DEFECT_REGISTER. Do not silently edit `03-DESIGN-SPEC.md` or `COPY_DECK.md`; add a dated erratum note that points to this addendum.

## Gate
Owner sign-off on the regulatory notices (Gate 4) remains open. Claude's source check does not close it.

---

## Amendment 1a (Claude, 2026-11-21 17:15 EST), following REVIEW_ASTRA_FINAL.md §2

The text above is kept as the record. Where this amendment conflicts with it, **this amendment governs**.

### A1-01, corrected again: the replacement gearbox copy dropped the type-certification-basis condition and named the wrong ASTM bulletin
- **Accepted.** The Astra High finding was confirmed against the AD's paragraph (c) quoted above. The 912 A1/A2/A3 condition is the **specific engine model paired with a specific aircraft model in Table 1**, where the engine was included in that aircraft's type-certification basis. The gearbox serial test applies to **both** groups.
- **ROTAX library check, 2026-11-21:**
  - ASB-2026-001 (certified, 912 S row) is rev 0, dated 22.06.2026. This is the R00 the FAA incorporated.
  - ASB_A-2026-001 (ASTM, 912 UL / 912 iS SPORT rows) is rev 1, dated 02.07.2026, file d07280.pdf. This is the R01 linked on the notice.

**Replacement copy for `/rotax-gearbox-notice` and every surface that renders its summary (`/owner-notices`, `/updates`, meta descriptions). Binding, verbatim:**

"FAA AD 2026-16-11 (effective August 28, 2026) applies to certified ROTAX 912 F2/F3/F4, 912 S2/S3/S4, 912 iSc2/iSc3 Sport and 914 F2/F3/F4 engines, and to 912 A1/A2/A3 engines installed on the aircraft models paired with them in the AD's Table 1 where the engine was part of that aircraft's type certification. In both cases it applies only if the installed propeller gearbox has a serial number listed in ROTAX ASB-2026-001R00. It does not apply to ASTM-standard 912 UL, ULS or iS Sport engines. Owners of those engines should check ROTAX ASB_A-2026-001R01 and the aircraft manufacturer's instructions for applicability. Check your engine model, gearbox serial number and aircraft against the official documents linked below."

The static guard requires this exact sentence on `/rotax-gearbox-notice`. It fails on the superseded phrase "engines installed in the type-certificated aircraft listed in the AD's Table 1" **and** on the A1-01 v1 phrase "912 A1/A2/A3 engines installed on the type-certificated aircraft listed in the AD's Table 1, where the engine's propeller gearbox serial number".

### A1-02: no change to the copy
The reviewer verified the November 4 date and the scope sentence. Apply them as written above.

### Record corrections, accepted
- The log the addendum's "Trigger" line refers to was renamed to `reviews/astra-final-review-1.log` after the addendum was written.
- A1-02's sentence "Both statements are false at `1467a22`" overstates the evidence. The correct reading: the stated date is wrong, and the November 21 source check did not catch it. The evidence does not show that no check was performed.
