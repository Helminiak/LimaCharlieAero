# REVIEW_RESOLUTION: Phase 9 exchange for frozen candidate `7d2e68e`

Inputs, written independently:
- `REVIEW_CLAUDE.md`: Claude Opus 5.5. SHA-256 `a9b6633a…`, hashed 2026-11-21 ~02:20 EST, before Codex's review ran.
- `REVIEW_CODEX.md`: Codex GPT-6.2 Astra, xhigh, 06:52–07:11 EST. Its first attempt at 02:05 hit the usage limit with no output.

Both verdicts: **approve with conditions for the private owner preview.**

Neither reviewer may close a regulatory, rights, privacy or production-safety gate by consensus. Those gates stay with the owner and are listed at the end.

## Where the reviews agree independently
- Public and preview builds reproduce: same file counts (318/324) and same byte totals (8,461,869 / 8,509,397).
- Draft isolation holds in the frozen public build: zero case text, markers or correspondence assets.
- No registration patterns or image metadata. The G5 mask and the correspondence crop are pixel-verified by both reviewers.
- The AD 2026-22-03 turbo notice is factually correct.
- Lab performance meets budget.
- Both reviewers found that the public build has zero cases. Codex reported it as passing isolation; Claude reported it as a copy problem (CR-01). The observations are consistent.
- Case status vs stepper integrity: Claude's CR-02 (visual inversion) and Codex's X-10 (the model allows the status and stages to disagree) are two sides of the same requirement.

## Disposition of every finding

| ID | Sev | Class | Disposition | Owner of fix |
|---|---|---|---|---|
| **X-01** unsupported before/after vibration claim | P1 | factual | **ACCEPTED. Claude's error.** Spec §3 and the copy deck prescribed "Measured 1.27 IPS → 0.04 IPS after correction", but the registry disclaims any pairing. The sequence is withdrawn. Copy is below. | Claude copy, Codex implements |
| **X-02** limits box omits §65.109(b) restrictions | P1 | factual | **ACCEPTED. Claude's copy deck line 105 was incomplete.** State the regulation's limits generally and make **no claim about the holder's trained scope** until the owner confirms it. Copy is below. | Claude copy, Codex implements |
| **X-03** full-size E-PROPS documents expose config/TC reference and RPM targets; G5 box label | P2 | factual (privacy/rights) | **ACCEPTED.** Default to masking: mask the configuration identifier, TC/approval reference, aircraft type line and RPM targets in the linked full-size derivatives, then correct the registry text. Add the G5 box purchasing label and barcodes to the owner rights review. Publishing the unmasked documents is an **owner decision** (CS-2 default: withhold). | Codex; owner gate |
| **X-04** gearbox notice leaves the AD/ASTM distinction implicit | P2 | factual | **ACCEPTED. Claude's register said "already explicit", which was wrong for the rendered page.** Copy is below. | Claude copy, Codex implements |
| **X-05** `?topic=toString` half-initializes intake | P2 | methodological | ACCEPTED (inherited from RC3). Use an own-key closed mapping, and keep native behavior until initialization succeeds. | Codex |
| **X-06** 33 RC3 FAQ `#question-N` anchors lost | P2 | acceptance | ACCEPTED. Restore the IDs, and add an inbound-anchor regression against RC3. | Codex |
| **X-07** social card can publish a case-only image | P1 | methodological | ACCEPTED. One eligibility gate for every raster output, social cards included. | Codex |
| **X-08** an unregistered original plus ICC text passes the build | P1 | methodological | ACCEPTED. Use an allowlist proof pool. Strip or reject metadata, including ICC text, on every output. | Codex |
| **X-09** an editor save drops `internal`/`placeholder` | P1 | methodological | ACCEPTED (inherited from RC3). Preserve flags on round-trip and add a test. | Codex |
| **X-10** case model accepts `"false"` confirmation, null sources, and status/stage conflict | P2 | methodological | ACCEPTED. Use typed confirmation and non-empty sources, and derive status consistency in the model. Pairs with CR-02. | Codex |
| **X-11** suite passes four draft leaks at once | P2 | acceptance | ACCEPTED. Use exact sitemap equality and a unique draft canary across every publication surface; the suite must fail on injected leaks. | Codex |
| **X-12** packaging names and verifies against RC3 | P2 | acceptance | ACCEPTED. Use release-scoped manifest, routes and filenames. | Codex |
| **X-13** a misspelled perf route exits 0 with no runs | P3 | acceptance | ACCEPTED. | Codex |
| **X-14** "Lima Charlie Aero technical review" attribution not evidenced | P3 | factual | **ACCEPTED. Claude's copy deck prescribed the label without evidence.** Replace it with a source-check line that names no reviewer until the owner signs. Copy is below. | Claude copy, Codex implements; owner gate |
| **X-15** Miniflare cold-start fetched Cloudflare `cf.json` | P2 | methodological | ACCEPTED. Set `CLOUDFLARE_CF_FETCH_ENABLED=false` in `tools/test-server.mjs` and in every harness. Disclosure: an uncredentialed metadata GET with no site or form data. No `cf.json` cache exists in the shared `repo/node_modules`, so whether the earlier implementation sessions made the same request is **UNVERIFIED**. | Codex |
| **CR-01** public copy promises cases that the public build does not contain | P1 | factual / acceptance | ACCEPTED (Codex made no objection). Data-driven zero-case variant. Copy is below. Whether to show Our Work in the nav at all while no case is approved remains an **owner option**; the default is to keep it with the evidence copy. | Codex |
| **CR-02** stepper inverted on the navy panel | P2 | factual (visual) | ACCEPTED. Fix together with X-10. | Codex |
| **CR-03** legacy labels glued to paragraphs (3 pages, from RC3) | P2 | factual (copy) | ACCEPTED. Add a static check for it. | Codex |
| **CR-04** legend breaks "Documentatio/n" | P3 | aesthetic | ACCEPTED. | Codex |
| **CR-05** canopy photo leads Our Work | P3 | aesthetic | ACCEPTED. | Codex |
| **CR-06** NDT excerpt small | P3 | aesthetic | ACCEPTED, optional. | Codex |
| **CR-07** cautious RC3 body copy | Info | tone | Owner copy pass. No engineering change. | Owner |

**Unresolved disagreements: none.** All four of Codex's factual findings on copy (X-01, X-02, X-04, X-14) are upheld against Claude's own spec and copy deck. Each correction is recorded here so the design documents are not silently superseded.

## Copy authority corrections (Claude, binding for implementation)

**X-01, `/rotax-gearbox-propeller-vibration`:**
- Remove the shared before/after caption and any "after correction" or "→" sequence.
- Captions:
  - FIG. 01: "A DynaVibe reading of 1.27 IPS."
  - FIG. 02: "A DynaVibe reading of 0.04 IPS."
- Section heading: "Measured, not guessed". Never "Before and after".
- Keep the page sentence saying the records do not establish a paired repair result. The two figures must not be visually joined by an arrow.

**X-02, `/s-lsa-e-lsa-maintenance` limits box:**
- Heading: **What a light-sport repairman can sign off**
- Body: "Under 14 CFR 65.109(b), a light-sport repairman certificate with a maintenance rating allows approval for return to service of light-sport-category aircraft, except a major repair or major alteration of a product produced under an FAA approval. For experimental aircraft certificated under §21.191(g), (i), (k) or (l), it allows the annual condition inspection. Work is limited to the aircraft category and class the repairman is trained for, and a major repair requires additional FAA-accepted training. If a job falls outside those limits, we tell you before work starts."
- Do not add any sentence that states this shop's trained category or class. That waits for owner confirmation.

**X-04, `/rotax-gearbox-notice`, summary paragraph:**
"FAA AD 2026-16-11 (effective August 28, 2026) applies to certified ROTAX 912 F2/F3/F4, 912 S2/S3/S4, 912 A1/A2/A3, 912 iSc2/iSc3 Sport and 914 F2/F3/F4 engines installed in the type-certificated aircraft listed in the AD's Table 1, where the gearbox serial number is listed in ROTAX ASB-2026-001. It does not apply to ASTM-standard 912 UL, ULS or iS Sport engines. Owners of those engines should check ROTAX ASB-2026-001 and the aircraft manufacturer's instructions for applicability. Check your engine model, gearbox serial number and aircraft against the official documents linked below."
Keep the existing official links.

**X-14, turbo notice reviewer line:** "Prepared from the FAA AD and ROTAX bulletin linked below; dates and engine scope checked against those documents on November 21, 2026." Name no reviewer. The owner may add a sign-off later.

**CR-01, zero public cases** (used when the public case count is 0):
- `/our-work`:
  - Title: "Our Work: Evidence from Light-Sport & Experimental Aircraft | Lima Charlie Aero"
  - H1: "Our Work"
  - Lead: "Photographs and measurements from aircraft we have worked on: what was found and how it was documented. Detailed case records are published after the aircraft owner has reviewed them."
  - Keep the meta description in step with the lead.
- Home section:
  - Heading: "From the hangar floor."
  - Intro: "Readings, findings and records from real aircraft."
  - Link: "See more of our work".
- Keep the 7-stage legend on Our Work. Its intro line stays accurate in both variants: "How we document the work".

## Gates that remain with the owner (not closed by this resolution)
1. Fact-check and publication consent for CS-1…CS-6. Vashon and the forensic example are BLOCKED. The correspondence image needs permission.
2. Rights and consent:
   - restored images (14 REVIEW REQUIRED subjects in the public HTML);
   - third-party faces;
   - the G5 box label;
   - whether the unmasked E-PROPS documents may be published (X-03).
3. LSRM-A trained category and class, and major-repair training. Current E-PROPS dealer status. iRMT listing currency.
4. Reviewer sign-off for the notices (X-14).
5. The live production site still serves the unmasked G5 placard image. Remediating production needs separate owner authorization.
6. External tests: Formspree inbox delivery, Cloudflare edge, physical devices, screen readers, Firefox/WebKit (no executables) and field CWV.
