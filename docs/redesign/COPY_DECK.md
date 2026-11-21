# v103 copy deck (Claude, design/content lead)

Codex integrates this copy into `content/*.json` and the templates. Codex does not rewrite it. If copy does not fit a component, log it in `DEFECT_REGISTER.md` and Claude revises.
Voice: company-first ("we", "the shop"), plain, specific, calm. No founder-centric CTAs. No invented staff, customers, results, approvals or turnaround times.
**Source rule:** every case-study statement traces to the owner's PR #2 steering (comment IDs given) or to a visible published image. Anything else is marked `[OWNER CONFIRM]`. Case records are `state: draft` until the owner fact-checks them.

---
## Global
- Primary nav: Services · ROTAX · E-PROPS · Our Work · About · **Request Service**
- Utility (desktop): `KAKH · Gastonia, NC · By appointment` | `Call 980.382.1344` · `Text the Shop`
- Footer tagline: `Precision · Reliability · Traceability`
- Notice bar (while the turbocharger or gearbox notice is active): `ROTAX owner notices: gearbox (ASB-2026-001) and 915/916 turbocharger valve housing (ASB-2026-002).` → link `Check applicability` (`/owner-notices`)

## Home
- Eyebrow: `KAKH · Gastonia, North Carolina`
- H1: `Light-sport & experimental aircraft, worked as a complete system.` (the highlight span is "worked as a complete system.")
- Lede: `Hands-on maintenance, ROTAX troubleshooting and E-PROPS installation planning, backed by the records, manufacturer data and documentation the aircraft needs.`
- CTAs: `Request Service` · `Call 980.382.1344`
- Trust strip: `ROTAX 9-Series: 912 · 914 · 915 · 916` | `E-PROPS dealer: Fitment, installation, balance` | `LSRM-A: FAA-certificated repairman` | `By appointment: Gastonia & the Charlotte region`
- Problem tiles. H2: `Bring the aircraft and what you noticed.` Intro: `No diagnosis needed. Tell us what changed or what is due, and we'll help work out where to start.`

| Tile | Title | Line | Destination | Image |
|---|---|---|---|---|
| 1 | ROTAX service & troubleshooting | 912, 914, 915 and 916: rough running, fuel pressure, cooling, ignition, five-year rubber. | `/rotax-engine-systems-support` | `rotax-installed-hoses-overview` |
| 2 | E-PROPS | Selection, fitment, installation planning and dealer support. | `/e-props-dealer-support` | `eprops-aircraft-closeup-sky-ranger` |
| 3 | Inspections & scheduled work | Condition inspections, 100-hour, calendar items and planning downtime. | `/s-lsa-e-lsa-maintenance` | `aircraft-open-cowling-under-canopy` |
| 4 | Vibration & balancing | Measured, corrected, re-measured. | `/rotax-gearbox-propeller-vibration` | `dynavibe-kit-secured-seat` |
| 5 | Prebuy & records | The logbooks checked against the aircraft. | `/light-sport-prebuy-evaluation` | `skyreach-bushcat-tailwheel-prebuy` |
| 6 | Avionics & electrical | Power, grounds, connectors and displays traced as one system. | `/light-sport-experimental-avionics` | `garmin-g5-installed-panel-wide` (**not** `-close`) |

- System band. Eyebrow `The LCA Standard`. H2 `We don't stop at the part that failed.` Body: `An aircraft is a system of systems. A fuel symptom can be a cooling problem; a vibration can be a propeller, a gearbox or a mount. We trace how the systems interact, check the records and the approval path, and work the problem until the next step is supportable.` Chips: Engine, Propeller, Fuel, Cooling, Electrical, Avionics, Airframe, Controls, Records, Approvals. Link: `How we work →` `/the-lima-charlie-aero-standard`
- Our Work. H2 `Real aircraft. The whole paper trail.` Intro: `Each example follows the same path: problem, configuration, evidence, evaluation, action, verification and documentation. Work that is still pending says so.` Shows CS-1 and CS-2 cards (public build: only published cases; if none are published, show the section with the method and a link to service evidence instead).
- How it works. H2 `Simple to start. Careful from there.`
  1. **Tell us.** The aircraft, the engine, and what changed or what is due. A phone photo helps.
  2. **We scope it.** We clarify records, access and the approval path, then agree an estimate and schedule.
  3. **We document it.** Findings, measurements and work entries that you and the next mechanic can follow.
- Founder band. Eyebrow `About`. H2 `Built on maintenance and engineering discipline.` Body: `Lima Charlie Aero was founded by Joseph Helminiak, an FAA-certificated light-sport repairman with a maintenance rating (LSRM-A) and ROTAX iRMT training, with a background in systems engineering, logistics and quality assurance.` Link `About the shop →`
- Final CTA. H2 `Tell us what your aircraft is doing.` Line `We'll help you work out the next supportable step.` Triad.

Remove from home: the duplicate "Technical Leadership" and "Technical leadership, company responsibility" sections, the "supplied source" sentence and the malformed name. The five RC3 service-summary sections ("Scheduled aircraft and ROTAX maintenance" etc.) move to `/services` where they are not already present. Their link rows are preserved on that page. Report word counts.

## Our Work (`/our-work`, new)
- Title: `Our Work: Light-Sport & Experimental Aircraft Case Studies | Lima Charlie Aero`
- H1: `Our Work`. Lede: `Real aircraft, identified by type. Each case shows what was found, the evidence, what was decided, how it was verified and what was documented. Pending work is labelled as pending.`
- Legend: the stage rail with a one-line definition of each stage.
- "What these cases do and don't show" box: `These are records of process on specific aircraft. They are not a promise of the same finding or outcome on yours, and they are not a substitute for the manufacturer instructions and approvals that apply to your aircraft.`

## Case drafts (all `state: draft`)

### CS-1: TL-2000 Sting Sport: engine-mount crack, repair or replace
Source: PR #2 comments 6019840432 and 6019938344. Images: `engine-cage-crack-closeup-before-repair`, `engine-cage-weld-repair-detail`, `engine-cage-weld-joint-detail`, `engine-cage-ndt-facility`, `ndt-magnetic-particle-report` (**redact** identifiers and registration), `tl-ultralight-designer-correspondence` (**redact** names, addresses and signature; keep the message body), `engine-cage-painted-finished`.
- **Problem:** A crack was found at a joint of the steel-tube engine mount.
- **Aircraft configuration:** TL-2000 Sting Sport, ROTAX 912. `[OWNER CONFIRM: engine model; S-LSA or E-LSA]`
- **Evidence:** The crack was photographed in place before any work, to record its location and extent.
- **Evaluation:** Repair and replacement were weighed. The repair path was taken to the aircraft designer instead of being decided on the shop floor. `[OWNER CONFIRM: what repair instruction or data was used]`
- **Action:** The joint was weld-repaired. `[OWNER CONFIRM: who performed the weld, if not LCA]`
- **Verification:** The repaired mount was inspected by magnetic-particle NDT at an outside testing facility. After the inspection, the aircraft designer confirmed in writing that the weldment is good and asked that the inspection protocol be added to the aircraft's documentation (correspondence shown with names and contact details redacted). Had the inspection not accepted the repair, the path was rework and re-test.
- **Documentation:** The NDT report and the designer's confirmation are kept with the aircraft records. The mount was refinished before reinstallation.
- Status pill: `Documented process`
- Limits: `Repair data and acceptance are specific to this aircraft and this finding.`

### CS-2: Sling 2 / ROTAX 912 iS: qualifying an E-PROPS propeller with the airframe manufacturer
Source: PR #2 comment 6019938344. Images: `eprops-engineering-packet-fanout` / `eprops-install-checklist-fanout` **only if** they belong to this package `[OWNER CONFIRM]`; otherwise text only.
- **Problem:** An owner wants an E-PROPS propeller on a Sling 2 with a ROTAX 912 iS. The airframe manufacturer's position decides whether that is an approved configuration.
- **Aircraft configuration:** Sling 2 (also relevant to the Sling LSA / NGT family), ROTAX 912 iS, applicable E-PROPS DURANDAL-3 configuration.
- **Evidence:** An E-PROPS technical package with the propeller's configuration data and supporting type-certificate data. E-PROPS also supplied Sling-specific technical material and offered a propeller for testing.
- **Evaluation:** Instead of treating one installation as automatically approved, we asked for a configuration-level review.
- **Action:** Lima Charlie Aero submitted the package to Sling's technical, airworthiness and engineering staff.
- **Verification (pending):** Expected validation covers configuration, installation, weight and balance, pitch and RPM, vibration, performance, temperatures, fuel flow and a post-test inspection.
- **Documentation:** The submittal and correspondence are kept. `[OWNER DECIDE: publish package reference numbers? default no]`
- Status pill: `In progress · pending manufacturer review`

### CS-3: TL-2000 Sting Sport / ROTAX 912: E-PROPS qualification and installation verification
Source: PR #2 comment 6019938344.
- **Problem:** Fit an E-PROPS DURANDAL-3 to a specific TL-2000 / ROTAX 912 configuration with a controlled, documented process.
- **Configuration:** Exact engine, gearbox and propeller configuration, with serialized components identified.
- **Evidence:** E-PROPS application package. Mass, inertia, operating-limit and interface review. Vibration and torsional-compatibility background, including manufacturer test background.
- **Evaluation:** The manufacturer authorization / LOA path was identified as a gate before installation was treated as settled.
- **Action:** Installation to the planned criteria: pitch, tracking, torque and clearance checks. WOT/static-RPM target planning.
- **Verification:** Dynamic balancing from recorded IPS, phase and RPM, with corrections toward a final balance target of about 0.07 IPS or less where applicable. Operational verification across the RPM range.
- **Documentation:** Weight and balance, equipment list and maintenance-record updates.
- Status pill: `[OWNER CONFIRM: "Documented process" or "Authorization pending"]`. **No final-authorization claim without the record.**

### CS-4: Vashon Ranger R7: manufacturer-coordinated fuel evaluation
Source: PR #2 comment 6019588967. **BLOCKED for publication** until the owner supplies a redacted packet excerpt and permission to describe the manufacturer correspondence.
- **Problem:** An owner asked whether a controlled-specification automotive gasoline could be used in a Vashon Ranger R7 with a Continental O-200-D.
- **Configuration:** Client aircraft baseline, fuel-system architecture, engine limitations and the existing approval gaps.
- **Evidence and evaluation:** An 11-page engineering evaluation covering detonation and preignition margin, vapor lock and hot-fuel behaviour, wetted-material compatibility, fuel density and metering, contamination and misfueling controls, placards and POH implications, instrumentation, a risk register and go/no-go decision gates. It treats two hazards separately: engine detonation suitability, and the installed aircraft's fuel-delivery and vapor margin. **Passing one does not establish the other.**
- **Action:** The packet went to the aircraft owner and, at the same time, to the airframe and engine manufacturers' technical staff so they could evaluate the question together.
- **Verification / Documentation:** Manufacturer disposition pending. `[OWNER CONFIRM]`
- Status pill: `Evaluation submitted · manufacturer disposition pending`

### CS-5: SeaRey: return-to-service systems evaluation
Source: PR #2 comment 6019588967. Text only unless the owner supplies photos.
- **Problem:** An amphibian returning to service after downtime: more than a routine annual or an engine-only check.
- **Configuration:** SeaRey amphibian, ROTAX 912 UL.
- **Evaluation (plan):** The plan crossed system boundaries: ROTAX calendar items, hoses and rubber, carburetors, fuel pump, cooling, gearbox, compression and leak-down, fuel contamination, propeller, corrosion and downtime effects, wing-attachment hardware, amphibious-airframe systems, records and inspection status, and sale readiness. With the wings already off, the plan used the opportunity to inspect the attachment hardware and the surrounding structure.
- Status pill: `Evaluation plan` `[OWNER CONFIRM: any completed work to report]`

### CS-6: forensic maintenance (records against as-found condition)
**BLOCKED:** the aircraft type is unknown. The owner must supply the type and confirm publication. No record is created.

## Service-page "Authorization & limits" standard texts
- ROTAX pages: `A family name alone does not establish whether a bulletin or directive applies. Applicability depends on the exact engine, gearbox or component identification and its service history. Certified-engine airworthiness directives and the ROTAX bulletins for non-certified engines are separate documents.`
- Inspections page: `Light-sport-category aircraft can be returned to service by an LSRM-A after maintenance and inspection within the rating's limits. Experimental aircraft condition inspections follow the aircraft's operating limitations. Major repairs and alterations follow the applicable manufacturer or FAA-approved data.` `[OWNER CONFIRM trained category/class and any major-repair training]`
- E-PROPS: `Product compatibility and a dealer quote do not authorize an installation. The aircraft's category and the airframe manufacturer's position decide the approval path.`

## Owner notices (content update, Codex)
- `rotax-turbocharger-notice`: add source `https://www.govinfo.gov/content/pkg/FR-2026-11-02/pdf/2026-22307.pdf` and the sentence `FAA AD 2026-22-03 (effective November 23, 2026) applies to listed certified 915 iSc and 916 iSc engines and requires the action before further flight; non-certified 915/916 iS engines remain under the ROTAX bulletin.` Set `last_modified`/`last_review` to the build date and `next_review` 30 days later. Reviewer: `Lima Charlie Aero technical review`.
- `rotax-gearbox-notice`: content verified accurate on 2026-11-20 against FR 2026-08-13 (AD 2026-16-11, effective 2026-08-28). Update `last_review` and `next_review` only.

**Erratum, 2026-11-21.** The gearbox Table 1 pairing and type-certification condition apply to the listed A-series models. Both engine groups require a listed installed gearbox. FAA AD 2026-22-03 took effect November 4, 2026. Use A1-02 and Amendment 1a of [Resolution Addendum 1](REVIEW_RESOLUTION_ADDENDUM_1.md) for the regulatory wording, source references and attribution. Owner sign-off is pending.
- `site.json` `date`: set to the preview build date and record it.
