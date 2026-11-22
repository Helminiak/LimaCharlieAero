# v103 copy deck (Claude, design/content lead)

Codex integrates this copy into `content/*.json` and the templates. Codex does not rewrite it. If copy does not fit a component, log it in `DEFECT_REGISTER.md` and Claude revises.
Voice: company-first ("we", "the shop"), plain, specific, calm. No founder-centric CTAs. No invented staff, customers, results, approvals or turnaround times.
**Case sources.** The six published cases reflect the November 21 owner directive, the cited PR #2 comments and the documented aircraft evidence. New cases require confirmed facts and publication permission.

---
## Global
- Primary nav: Services · ROTAX · E-PROPS · Our Work · About · **Request Service**
- Utility (desktop): `KAKH · Gastonia, NC · By appointment` | `Call 980.382.1344` · `Text the Shop`
- Footer tagline: `Precision · Reliability · Traceability`
- Safety bar. “Two FAA airworthiness directives are in effect for certain certified ROTAX engines. Check applicability” links to `/owner-notices#in-effect`.

## Home
- Eyebrow: `KAKH · Gastonia, North Carolina`
- H1: `Light-sport & experimental aircraft, worked as a complete system.` (the highlight span is "worked as a complete system.")
- Lede: `Hands-on maintenance, ROTAX troubleshooting and E-PROPS installation planning, backed by the records, manufacturer data and documentation the aircraft needs.`
- CTAs: `Request Service` · `Call 980.382.1344`
- Trust strip. ROTAX 9-Series · ROTAX iRMT · E-PROPS dealer · FAA LSRM-A · By appointment. The iRMT item links directly to listing 7534.
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

## Our Work · owner-approved case copy, 2026-11-21

Six aircraft cases follow the evidence from the first question through the work, checks and records. Each identifies the decisions and tests still pending.

Each case follows one aircraft configuration. The records show which checks were completed and which decisions still belong to the owner or manufacturer.

### CS-1 · TL-2000 Sting Sport: engine-mount crack, repair or replace

Completed · repair inspected and confirmed by the aircraft designer

- **Problem · done** A crack was found at a joint of the steel-tube engine mount.
- **Configuration · done** TL-2000 Sting Sport (2005), ROTAX 912.
- **Evidence · done** The crack was photographed in place before any work, to record its location and extent.
- **Evaluation · done** Repair and replacement were weighed. The repair path was taken to the aircraft designer for review.
- **Action · done** The joint was weld-repaired.
- **Verification · done** On 28 October 2025 an outside facility used wet fluorescent magnetic-particle inspection with a yoke to ASTM E1444. All four areas were accepted: the lower right and lower left diagonal weld toes and the bottom and left cross-tube heat-affected zones. On 8 December 2025 the aircraft designer confirmed in writing that the weldment is good and asked that the inspection protocol be added to the aircraft documentation.
- **Documentation · done** The NDT report and the designer's confirmation are kept with the aircraft records. The mount was refinished before reinstallation.

### CS-2 · Sling 2 / ROTAX 912 iS: qualifying an E-PROPS propeller with the airframe manufacturer

Engineering and manufacturer coordination substantially complete · awaiting Sling Aircraft manufacturer testing in South Africa · final approval pending

- **Problem · done** An owner wants an E-PROPS propeller on a Sling 2 with a ROTAX 912 iS. The airframe manufacturer's position decides whether that is an approved configuration.
- **Configuration · done** Sling 2 (also relevant to the Sling LSA / NGT family), ROTAX 912 iS, applicable E-PROPS DURANDAL-3 configuration.
- **Evidence · done** E-PROPS supplied technical package EP-2026-712 Rev A, DUR-3-175-C4-T configuration data and supporting EASA TCDS P.512, along with Sling-specific technical material and an offer of a propeller for testing.
- **Evaluation · done** Instead of treating one installation as automatically approved, we asked for a configuration-level review.
- **Action · done** Lima Charlie Aero submitted the package to Sling's technical, airworthiness and engineering staff.
- **Verification · pending** Manufacturer testing by Sling Aircraft in South Africa is the next step; expected validation covers configuration, installation, weight and balance, pitch and RPM, vibration, performance, temperatures, fuel flow and a post-test inspection.
- **Documentation · done** The submittal and correspondence are kept with the job file.

### CS-3 · TL-2000 Sting Sport / ROTAX 912: E-PROPS DURANDAL-3 engineering and installation control

Propeller-manufacturer engineering complete · installation and verification controlled by checklist

- **Problem · done** Fit an E-PROPS DURANDAL-3 to a specific TL-2000 / ROTAX 912 configuration with a controlled, documented process.
- **Configuration · done** TL-2000 Sting Sport, ROTAX 912 (80 hp), 2.27 gearbox and 175 cm DUR-3-175-C4-T propeller.
- **Evidence · done** E-PROPS engineering package EP-2026-398 includes the configuration data and an Engineering Compatibility Statement dated 31 March 2026.
- **Evaluation · done** The review covered mass, inertia, operating limits, interfaces and vibration and torsional background. Airframe-manufacturer authorization through the LOA process is a separate gate.
- **Action · done** Criteria defined. The installation checklist calls for component identification, pre-installation inspection, torque of 24 N·m at the hub flange, 11 N·m at the hub clamp and 5 N·m at the spinner plate. Pitch is 23° with a blade-to-blade tolerance of ≤0.3°.
- **Verification · done** Criteria defined. The checklist specifies a ground run at 5,000–5,800 rpm, dynamic balance acceptance at ≤0.10 IPS with a ≤0.07 IPS target, and wide-open-throttle flight RPM of 5,500 ± 50. It also calls for post-installation re-torque and pitch checks.
- **Documentation · done** The checklist calls for weight and balance, equipment-list and logbook entries alongside the installation record.

### CS-4 · Vashon Ranger R7 / Continental O-200-D: manufacturer-coordinated fuel evaluation

Evaluation submitted September 2026 · manufacturer disposition pending

- **Problem · done** An owner asked whether a controlled-specification automotive gasoline could be used in a Vashon Ranger R7 with a Continental O-200-D.
- **Configuration · done** Client aircraft baseline, fuel-system architecture, engine limitations and the existing approval gaps.
- **Evidence · done** An 11-page engineering evaluation covering detonation and preignition margin, vapor lock and hot-fuel behaviour, wetted-material compatibility, fuel density and metering, contamination and misfueling controls, placards and POH implications, instrumentation, a risk register and go/no-go decision gates.
- **Evaluation · done** It treats two hazards separately: engine detonation suitability, and the installed aircraft's fuel-delivery and vapor margin. Passing one does not establish the other.
- **Action · done** The 11-page packet LCA-ENGINEERING-2026-006 Rev A was sent on 6 September 2026 to the aircraft owner and, at the same time, to the airframe manufacturer’s engineering staff and the engine manufacturer’s technical services.
- **Verification · pending** Manufacturer disposition pending. The evaluation's decision gates keep the two hazards separate: passing a detonation test does not establish the installed fuel-delivery and vapor margin.
- **Documentation · done** The packet, its data requests to the airframe and engine manufacturers and the follow-up correspondence are kept with the job file.

### CS-5 · SeaRey (2002): return-to-service systems evaluation

Evaluation plan complete · inspection findings not yet reported

- **Problem · done** An amphibian returning to service after downtime: more than a routine annual or an engine-only check.
- **Configuration · done** 2002 SeaRey amphibian, ROTAX 912 UL, out of service since 2020.
- **Evidence · done** Six years without a current inspection: calendar-limited rubber, fuel left in the system and corrosion exposure all had to be assumed until checked.
- **Evaluation · done** The plan crossed system boundaries: ROTAX calendar items, hoses and rubber, carburetors, fuel pump, cooling, gearbox, compression and leak-down, fuel contamination, propeller, corrosion and downtime effects, wing-attachment hardware, amphibious-airframe systems, records and inspection status, and sale readiness. With the wings already off, the plan used the opportunity to inspect the attachment hardware and the surrounding structure.
- **Action · done** The return-to-service scope was written and sent to the seller's broker before any work was quoted, so the aircraft was evaluated as a whole rather than as a routine annual.
- **Verification · pending** Compression and leak-down, fuel-system cleanliness, oil-system and gearbox condition, and attachment-hardware inspection are the planned gates.
- **Documentation · pending** Findings and any return to service are recorded against that scope.

### CS-6 · Flight Design CTSW / ROTAX 912: forensic records audit against as-found condition

Records audit and return-to-service plan complete · physical inspection gates pending

- **Problem · done** An aircraft whose maintenance claims could not be taken at face value: records had to be reconciled with the aircraft before any release decision.
- **Configuration · done** Flight Design CTSW, carbureted ROTAX 912, ballistic recovery system.
- **Evidence · done** A bulletin-by-bulletin audit against 54 manufacturer publications — 7 airframe safety alerts, 17 service bulletins, 6 service notifications and 24 ROTAX publications — with each claim traced to an entry, a document or a gap.
- **Evaluation · done** Gaps and contradictions were separated from confirmed items: component identities, calendar and TBO status, gearbox applicability, carburetor float and circlip actions, rubber isolators, the recovery system and an inconsistency in the fuel-system record.
- **Action · done** A return-to-service plan of 144 traceable tasks with 6 hold points, configuration-verification steps, measured fuel-flow forms and an evidence register.
- **Verification · pending** Physical inspection and measurement against the hold points; the release decision follows the evidence, not the logbook alone.
- **Documentation · done** The audit report, compliance tracker and evidence requests are kept with the job file.

## Service-page "Authorization & limits" standard texts
- ROTAX pages: `A family name alone does not establish whether a bulletin or directive applies. Applicability depends on the exact engine, gearbox or component identification and its service history. Certified-engine airworthiness directives and the ROTAX bulletins for non-certified engines are separate documents.`
- Inspections page: `Light-sport-category aircraft can be returned to service by an LSRM-A after maintenance and inspection within the rating's limits. Experimental aircraft condition inspections follow the aircraft's operating limitations. Major repairs and alterations follow the applicable manufacturer or FAA-approved data.` The trained category/class and major-repair training still require owner documentation.
- E-PROPS: `Product compatibility and a dealer quote do not authorize an installation. The aircraft's category and the airframe manufacturer's position decide the approval path.`

## Owner notices (content update, Codex)
- `rotax-turbocharger-notice`: add source `https://www.govinfo.gov/content/pkg/FR-2026-11-02/pdf/2026-22307.pdf` and the sentence `FAA AD 2026-22-03 (effective November 23, 2026) applies to listed certified 915 iSc and 916 iSc engines and requires the action before further flight; non-certified 915/916 iS engines remain under the ROTAX bulletin.` Set `last_modified`/`last_review` to the build date and `next_review` 30 days later. Reviewer: `Lima Charlie Aero technical review`.
- `rotax-gearbox-notice`: content verified accurate on 2026-11-20 against FR 2026-08-13 (AD 2026-16-11, effective 2026-08-28). Update `last_review` and `next_review` only.

**Erratum, 2026-11-21.** The gearbox Table 1 pairing and type-certification condition apply to the listed A-series models. Both engine groups require a listed installed gearbox. FAA AD 2026-22-03 took effect November 4, 2026. Use A1-02 and Amendment 1a of [Resolution Addendum 1](REVIEW_RESOLUTION_ADDENDUM_1.md) for the regulatory wording, source references and attribution. Owner sign-off is pending.
- `site.json` `date`: set to the preview build date and record it.
