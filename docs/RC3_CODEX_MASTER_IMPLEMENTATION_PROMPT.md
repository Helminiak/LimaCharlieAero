# Lima Charlie Aero RC3
## Codex Master Implementation Prompt
### Proof-of-work architecture, warmer company voice, technical depth, SEO/local search, maintainable source, and closed-loop verification

---

# 0. EXECUTION DIRECTIVE

Execute this specification as a complete implementation task on the existing GitHub branch:

rc3-proof-of-work-seo

Repository:

Helminiak/LimaCharlieAero

Target branch for eventual review:

main

Do not treat this as an audit, concept exercise, design proposal, partial patch, or one-pass coding task.

The product direction has already been decided. Codex is the implementation engineer. ChatGPT/design/SEO remains the independent product, human-factors, search, visual, and release-review authority.

Your job is to implement the complete RC3 candidate, test it, inspect the generated site yourself, correct implementation defects, repeat the relevant test cycle, freeze a candidate, and return a review-ready pull request and evidence package.

Do not merge the pull request. Do not deploy to Cloudflare. Do not change DNS. Do not change paid services. Do not contact customers. Do not create reviews, testimonials, case histories, or business claims.

The only acceptable terminal status for this task is:

ENGINEERING CANDIDATE COMPLETE — DESIGN/SEO SIGN-OFF REQUIRED

If an external dependency blocks a required test, report it explicitly as NOT RUN — EXTERNAL VALIDATION REQUIRED. Never convert an unrun test into PASS.

---

# 1. GIT AND SOURCE-OF-TRUTH CONTEXT

The verified current-live website was imported into main and independently reviewed before RC3 work began.

The permanent pre-redesign merge commit is:

3d48ea6ec3785bc1faf67a5826eb678c3d14cc58

The live baseline archive identity recorded in the repository is:

LCA_SOURCE_OF_TRUTH_BASELINE_v100_2_5F_DEPLOYABLE(1).zip

Archive SHA-256:

e160c234b86aac2076db101c1b2e1acd27c46ed010866fd1aa6b21ff8214710a

Verified live website:

- 214 public files
- 14,184,009 uncompressed bytes
- byte comparison PASS
- 1,301 local references checked with zero missing targets

The current RC3 branch was created from that approved main baseline.

The live baseline is therefore the authoritative historical content and proof reservoir for this Git task.

This RC3 specification is authoritative for the desired product direction.

When this specification conflicts with existing generated copy, layout, or architecture, this specification controls.

Do not modify main directly.

Do not force-push main.

Do not merge this branch.

Commit only to rc3-proof-of-work-seo.

Use meaningful commits. Keep the branch reviewable.

---

# 2. OPERATING MODEL

Design/SEO authority owns:

- business positioning
- brand hierarchy
- human factors
- owner journeys
- information architecture
- visual hierarchy
- proof-of-work strategy
- content-retention policy
- page purpose
- local SEO
- structured data strategy
- AI-search/citation readiness
- conversion architecture
- final acceptance

Codex owns:

- repository implementation
- source architecture
- templates/components
- build tooling
- content integration
- asset processing
- accessibility implementation
- SEO implementation
- automated tests
- screenshots
- performance checks
- defect discovery
- defect correction
- clean rebuild
- packaging
- Git commits and branch updates
- review evidence

Codex must not independently redefine the business, simplify the product strategy, convert the company into a personal brand, or delete substantive content because a page feels long.

---

# 3. PRIMARY PRODUCT OBJECTIVE

The current live site has substantial technical material and real maintenance imagery. The redesign work that followed improved engineering discipline but at times became too cold, too generic, or too weak at presenting actual work as evidence.

RC3 must synthesize the strongest characteristics:

1. live-site technical credibility and work evidence;
2. modern static-site engineering discipline;
3. company-first scalable brand architecture;
4. warmer natural organizational voice;
5. clear owner-first navigation;
6. strong proof of actual maintenance work;
7. strong page-level SEO and local signals;
8. clean structured data;
9. excellent accessibility and responsive behavior;
10. high performance without stripping useful content or imagery.

Do not create another sterile redesign.

Do not create another founder-centric redesign.

The target impression is:

A technically serious, modern light-aircraft maintenance business that clearly works on real aircraft, documents what it sees, explains technical problems in owner-readable language, and makes it easy to request service.

---

# 4. BUSINESS AND BRAND TRUTH

Primary business identity:

Lima Charlie Aero LLC

Primary operating identity in copy:

Lima Charlie Aero

Base:

KAKH / Gastonia, North Carolina

Regional relevance:

Charlotte and the Carolinas where factually appropriate

Primary service positioning:

- Light-Sport aircraft maintenance
- S-LSA / E-LSA / Experimental support
- ROTAX 9-Series specialty
- E-PROPS dealer/support
- light-aircraft avionics/electrical support
- prebuy / records / inspection support

Founder:

Joseph “Joe” Helminiak

Founder role:

founder / owner / technical lead where factually supported

Use person-specific language only where the subject is actually the person:

- biography
- personal certifications/training
- founder background
- a person-specific vCard/contact identity
- one restrained founder/technical-lead trust section
- real photographs showing him performing work

Do not use the founder as the default site actor.

The company should be able to add employees later without rewriting the entire site.

---

# 5. COMPANY-FIRST BUT NOT CORPORATE-COLD

Use natural organization voice.

Preferred actors:

- Lima Charlie Aero
- we
- us
- our
- the shop

Do not falsely imply a staff size.

Do not invent:

- “our technicians”
- “our mechanics”
- dispatch staff
- front-office staff
- multiple locations
- large-shop capacity
- fleet volume
- turnaround guarantees

Use “we / us / our” naturally even if the company presently has one primary technical lead. The company is the entity providing the service.

Do not solve founder-centric language by repeating “Lima Charlie Aero” in every sentence. That created a cold, legalistic tone.

Target voice:

- competent
- technically precise
- calm
- owner-readable
- factual
- warm enough to feel human
- never sales-hype
- never macho
- never corporate boilerplate

---

# 6. BANNED BRAND REGRESSIONS

Generated public HTML must contain zero case-insensitive occurrences of these phrases unless they appear inside a historical/verification document that is not deployed:

Tell Joe
Contact Joe
Call Joe
Text Joe
Meet Joe
Joe reviews
owner-operated

Create an automated test that fails the build if any deployed public HTML contains them.

Also produce a non-blocking voice-frequency report for:

Joe
Joseph
we
our
us
team
technician
shop
Lima Charlie Aero

The report exists to catch overcorrection in either direction.

---

# 7. REPETITION REGRESSION

The prior candidate became visually and verbally repetitive.

Flag these visible phrases if they exceed the listed page counts:

Owner information: more than 3 pages
Unsure where to start?: more than 10 pages
What happens next: more than 12 pages
Inspection context: more than 5 pages
The repeated generic diagnosis/serviceability caution sentence: more than 2 pages

Do not create one universal template paragraph that appears everywhere.

Shared UI may be consistent; page copy should be contextual.

---

# 8. MAINTAINABLE SOURCE ARCHITECTURE

GitHub source, not ZIP files, must be the authoritative product record.

The current branch began from a deployable static baseline. RC3 must establish a maintainable authoring architecture.

Use this architecture unless the repository already contains an equivalent or a documented technical reason requires a small variation:

content/
  pages.json
  site.json
  updates.json
  editorial-backlog.json

templates/
  page.html
  site.css
  site.js
  menu.js

assets-src/

tools/
  build.py
  preview.py
  verify_static.py
  verify_browser.mjs
  verify_auxiliary.mjs
  verify_release_features.mjs
  performance.mjs
  package_release.py
  package_source.py

docs/
evidence/
dist/

package.json
package-lock.json
README.md
.gitignore
AGENTS.md

Requirements:

- source files are authoritative;
- dist is generated;
- the build is deterministic;
- public pages are generated from structured content rather than duplicated manually;
- shared header/footer/navigation are templated;
- shared CSS/JS are centralized;
- image transforms are deterministic;
- site metadata and structured data are generated consistently;
- verification tooling runs from a clean checkout;
- docs, baselines, evidence, source, and release tooling are not accidentally exposed in dist.

Do not adopt React, Next.js, WordPress, a headless CMS, or another heavy framework for this release.

This should remain a lightweight static site suitable for Cloudflare Pages later.

Cloudflare deployment itself is out of scope for this task.

---

# 9. PUBLIC ROUTE ARCHITECTURE

Target the 39-route v102 architecture. Preserve useful live routes and add/retain the newer owner-entry and notice routes.

Expected generated routes:

404.html
about-credentials.html
aircraft-records-review.html
card.html
contact.html
e-props-dealer-support.html
faq.html
image-credits.html
index.html
joseph-helminiak-bio.html
light-sport-experimental-avionics.html
light-sport-prebuy-evaluation.html
owner-notices.html
planning-service-downtime.html
prebuy-first-inquiry.html
privacy.html
rotax-9-series-912-914-915-916-support.html
rotax-912-carb-sync.html
rotax-912-high-oil-temperature.html
rotax-912-mag-drop-troubleshooting.html
rotax-915-916-turbo-ems-support.html
rotax-cooling-oil-temperature-problems.html
rotax-engine-systems-support.html
rotax-fuel-pressure-fuel-delivery-problems.html
rotax-gearbox-notice.html
rotax-gearbox-propeller-vibration.html
rotax-ignition-ecu-electrical-faults.html
rotax-installation-review.html
rotax-rubber-hose-replacement-fluid-leaks.html
rotax-turbocharger-notice.html
s-lsa-e-lsa-maintenance.html
security-disclosure.html
service-area.html
services.html
start-with-the-symptom.html
support-request.html
thank-you.html
the-lima-charlie-aero-standard.html
updates.html

Do not add thin city doorway pages.

Do not create a case-study route yet merely to look larger.

Documented work should be embedded into technically relevant pages first.

---

# 10. OWNER JOURNEYS AND HUMAN FACTORS

A visitor should understand within seconds:

1. what the shop supports;
2. where it is located;
3. whether the page relates to the visitor’s situation;
4. whether the shop actually performs the kind of work being described;
5. what information the visitor should gather;
6. how to request service.

Primary owner entry paths:

A. Something feels wrong / symptom
B. Scheduled service or inspection is due
C. Buying an aircraft / prebuy / records
D. ROTAX engine-system concern
E. E-PROPS / propeller support
F. Avionics / electrical support
G. Records / documentation review
H. Not sure where to start

Do not require a visitor to know an exact engine model, diagnosis, or technical vocabulary before beginning an inquiry.

Use progressive disclosure.

Technical pages can be deep, but their opening section must be understandable to a non-mechanic owner.

---

# 11. HOMEPAGE REQUIREMENTS

The homepage is the highest-priority design surface.

The hero must establish:

- Lima Charlie Aero
- KAKH / Gastonia / Charlotte-Carolinas context
- Light-Sport & Experimental Aircraft Maintenance
- ROTAX 9-Series Specialty
- a real aircraft / engine / maintenance context image
- primary CTA: Request Service
- secondary direct contact options if already factual and supported

Do not make the founder the hero.

Do not use a founder portrait as the dominant homepage image.

Recommended H1 direction:

Light-Sport & Experimental Aircraft Maintenance

Supporting phrase:

ROTAX 9-Series Specialty

Owner-routing section should follow early, with paths such as:

- Something feels wrong
- Service or inspection is due
- I’m buying an aircraft
- I need propeller / avionics / electrical help

Immediately after the owner-routing section, add a major proof block.

Preferred section title:

Work, documented

The homepage proof block must include at least four meaningful actual-work examples from real site assets, such as:

- dynamic vibration measurement / mechanical evidence;
- engine-cage crack / repair evidence;
- fuel-system borescope evidence;
- avionics / electrical installation or connector evidence.

Each item must answer in concise factual language:

- what is shown;
- what was observed;
- why it matters;
- what type of evidence or next step is relevant.

Do not make unsupported outcome claims.

Do not label two photos “before” and “after” unless the evidence clearly establishes they are the same documented maintenance sequence.

Later homepage sections should include:

- service group overview
- ROTAX specialty
- E-PROPS
- prebuy / records
- the Lima Charlie Aero Standard
- local KAKH/Gastonia context
- restrained founder/technical-lead authority
- clear final request-service CTA

Target visible homepage depth:

approximately 850 to 1,050 useful words after proof modules and captions.

This is an editorial guardrail, not an SEO quota.

---

# 12. PROOF-OF-WORK ARCHITECTURE

Proof is a release requirement, not decoration.

The site already contains or historically contained useful actual-work subjects. Inventory the baseline assets and preserve only useful, permission-cleared subjects.

Target deployed photographic proof subjects:

approximately 35 to 45 unique meaningful subjects.

Do not restore every old image.

Do not use stock aviation imagery.

Do not use AI-generated aircraft, mechanics, hangars, components, or maintenance scenes.

Strong existing evidence categories include:

- DynaVibe equipment and displayed measurements
- gearbox / mechanical wear
- engine on hoist
- engine cage crack
- cage repair / weld detail
- NDT / facility context
- finished cage condition
- dirty fuel tank borescope
- clean fuel tank borescope
- fuel-pump context
- differential-pressure tester
- carb / sync tooling
- oil / filter service
- installed hose routing
- coolant residue / fitting evidence
- Garmin G5 installed panel
- D-sub wiring
- connector closeups
- damaged / frayed electrical connector
- soft-start connector
- logbook / work-sticker evidence
- E-PROPS installed aircraft / propeller
- E-PROPS blade condition
- engineering packet / checklist evidence
- actual aircraft at KAKH / open-cowling work context

Asset filenames alone are not proof of what happened.

Use only claims supported by the visible image and verified surrounding content.

---

# 13. REQUIRED PROOF PLACEMENTS

Implement contextual evidence, not a giant generic gallery.

Homepage:
- four-card Work, documented module after early owner/service routing;
- later local aircraft/shop context image.

services.html:
- four-image capability/proof strip after the main service groups;
- examples may include pressure testing, oil/filter work, hose/service tooling, carb/sync tooling.

rotax-gearbox-propeller-vibration.html:
- documented evidence sequence using the real vibration measurement image(s), mechanical wear images, and later documented measurement if supported;
- explain what a vibration measurement tells the owner and what it does not establish by itself.

rotax-installation-review.html:
- engine/installation sequence: engine on hoist, cage/installation concern, repair/detail, final documented condition/NDT context where factual.

rotax-fuel-pressure-fuel-delivery-problems.html:
- dirty/clean borescope and fuel-delivery evidence sequence where supportable.

light-sport-experimental-avionics.html:
- installed G5 plus behind-panel wiring / connector evidence;
- show both visible finished installation and hidden workmanship.

e-props-dealer-support.html:
- engineering packet/checklist evidence in the fitment/process section;
- installed propeller and blade-condition evidence in support/condition context.

aircraft-records-review.html:
- logbook / work-record proof;
- use redaction where identifying information appears.

the-lima-charlie-aero-standard.html:
- one real documented maintenance sequence illustrating the method in practice.

light-sport-prebuy-evaluation.html:
- permission-cleared aircraft inspection evidence plus a factual representation of findings/report structure.

contact.html:
- one warm actual aircraft / airport / work-context image.

service-area.html:
- KAKH / Gastonia aircraft context, not a generic city skyline.

joseph-helminiak-bio.html:
- founder working around aircraft, not glamor photography.

---

# 14. CAPTION STANDARD

Captions must be written as useful evidence.

Bad pattern:

Inspection context; diagnosis and serviceability require aircraft-specific evidence and applicable instructions.

Do not repeat that sentence mechanically.

Better pattern:

Behind-panel evidence matters. This connector view documents conductor routing and termination condition during electrical troubleshooting.

For a displayed measurement, state only what the image itself supports.

For example:

Documented vibration measurement: the displayed reading is 1.27 IPS.

Do not say that a later 0.04 IPS image proves a specific corrective action caused the change unless the records establish that relationship.

Each important caption should preferably communicate one or more of:

- observation
- measurement
- condition
- process
- traceability
- why the evidence matters

Avoid legalistic filler.

---

# 15. ASSET RIGHTS AND PRIVACY

Create:

evidence/ASSET_PERMISSIONS_REGISTER.md

For every proof asset record:

- source path
- current deployed path
- description
- provenance if known
- identifying information present
- owner/customer identifiers present
- aircraft registration visible
- document/logbook identifiers visible
- redaction needed
- permission status
- disposition: deploy / redact then deploy / hold / exclude

Historical presence on the website does not automatically prove publication rights.

If permission status is not established from repository evidence, mark the asset:

REVIEW REQUIRED

Do not invent permission.

For any image showing logbooks, invoices, N-numbers, names, addresses, serial numbers, or other identifying data, inspect for redaction need.

No rights confirmation must be treated as an external release gate, not silently assumed.

---

# 16. PAGE CONTENT TARGETS

These are editorial guardrails for useful visible content, not keyword quotas.

404:
retain concise utility role.

about-credentials:
preferred approach is noindex,follow unless it is expanded into a genuinely distinct credential-verification page.
Do not compete with the founder biography.
If kept indexable, make it meaningfully distinct and approximately 350–500 useful words.

aircraft-records-review:
850–1,050 words.
Explain what records can reveal, chronology, missing entries, maintenance history, aircraft-specific context, and how records inform prebuy/service planning.

card:
utility route only.
Keep visible business identity company-first.
A person-specific vCard may identify Joseph Helminiak if that is the real business contact record.

contact:
350–500 words.
Warm, concise, local, clear.
Do not turn it into a legal notice.
Make it easy to understand location, what to send, and how to request service.

e-props-dealer-support:
1,250–1,500 words.
Restore useful fitment/process depth.
Include:
- actual support scope
- propeller/aircraft/engine fit context
- documentation/engineering packet
- installation/support boundaries
- inspection/condition concerns
- real installed-prop and blade-condition proof
- factual dealer/support language only

faq:
1,100–1,400 words.
Answer actual owner questions directly.
Avoid generic SEO questions.
Use visible Q&A that can support FAQ structured data.
Do not promise rich results.

image-credits:
factual utility page.

index:
850–1,050 words after proof module.

joseph-helminiak-bio:
approximately 750–900 words.
Founder authority belongs here.
Keep factual certifications/training only.
Do not use this page to imply unrelated authorization.

light-sport-experimental-avionics:
750–950 words.
Owner-friendly scope, electrical troubleshooting, installation context, documentation, real installed/behind-panel evidence.

light-sport-prebuy-evaluation:
900–1,100 words.
Explain scope, aircraft-specific limitations, records, condition evidence, what is and is not represented, and tangible deliverable/process.

owner-notices:
250–450 words when substantive.
Keep notices dated, sourced, and restrained.

planning-service-downtime:
250–450 words.
Owner planning, parts/logistics/records/aircraft access considerations.
No turnaround guarantees.

prebuy-first-inquiry:
250–450 words.
Tell owners exactly what to send first without demanding complete technical knowledge.

privacy:
retain and update only as needed for actual data handling.

rotax-9-series-912-914-915-916-support:
700–900 words.
This is a meaningful ROTAX hub, not a thin route list.
Explain supported problem categories, system thinking, model differences only where supportable, and how to start.

rotax-912-carb-sync:
650–800 words.
Explain symptoms, synchronization context, prerequisites, evidence, and why sync is not a universal cure.

rotax-912-high-oil-temperature:
600–800 words if content remains useful.
Cover conditions, instrumentation, cooling/oil system context, recent maintenance, and evidence to send.

rotax-912-mag-drop-troubleshooting:
600–800 words.
Explain what a mag-drop concern can represent, why the symptom is not a diagnosis, and the role of ignition/fuel/plugs/installation evidence where appropriate.

rotax-915-916-turbo-ems-support:
650–850 words.
Keep installation/system context and data/evidence orientation.
Do not imply unsupported ECU authorization or factory status.

rotax-cooling-oil-temperature-problems:
650–850 words.
Owner-readable cooling/oil troubleshooting context, recent work, operating conditions, instrumentation, residue/leak evidence.

rotax-engine-systems-support:
950–1,150 words.
Broad systems page.
Explain that engine symptoms can involve fuel, ignition, electrical, cooling, lubrication, controls, propeller/load, installation, and records.

rotax-fuel-pressure-fuel-delivery-problems:
750–900 words plus proof sequence.
Include:
- symptom versus source
- fuel supply / restriction / contamination / venting / pump / installation context
- recent maintenance
- borescope/fuel evidence where factual
- disciplined diagnosis before parts replacement

rotax-gearbox-notice:
retain as a dated/sourced notice.
Do not rewrite official applicability without current source verification.

rotax-gearbox-propeller-vibration:
850–1,050 words plus documented evidence.
This should become one of the strongest proof pages.
Discuss:
- symptom framing
- measurement
- propeller / gearbox / mount / installation context
- mechanical evidence
- why a single measurement is not a complete diagnosis
- real documented measurement images
- factual next-step process

rotax-ignition-ecu-electrical-faults:
750–900 words.
Reinforce:
- intermittent or misleading electrical symptoms
- evidence before diagnosis
- failed connection versus expensive component replacement
- timeline and recent maintenance
- wiring/fuel overlap where relevant
- exact warnings/conditions
Do not recommend swapping expensive ECUs casually.

rotax-installation-review:
850–1,050 words plus proof sequence.
Explain:
- many problems originate outside the engine
- surrounding systems influence symptoms
- access / support / organization / inspection / records
- small installation details can have large effects
- aircraft-specific review
- real engine/cage/repair evidence

rotax-rubber-hose-replacement-fluid-leaks:
850–1,000 words.
Treat the rubber package as multiple systems:
- fuel
- cooling
- lubrication
- intake rubber/sockets
- leak-source tracing
- run/leak-check/sync/records where applicable
- age and maintenance-manual/current-instruction basis
- staining is not automatically the leak source

rotax-turbocharger-notice:
retain dated/sourced notice.

s-lsa-e-lsa-maintenance:
900–1,100 words.
Explain regulatory/maintenance context carefully.
Do not overstate authority.
Keep owner-readable.

security-disclosure:
retain concise factual utility page.

service-area:
750–950 words.
Strong local intent without doorway spam.
Use KAKH/Gastonia, Charlotte, and regional language naturally and truthfully.
Explain practical service geography without inventing mobile/onsite service promises.

services:
1,050–1,300 words.
Strong commercial hub with owner paths, service groups, proof strip, contextual internal links, and clear request-service actions.

start-with-the-symptom:
250–450 words.
Reassure owners they do not need a diagnosis before requesting service.
Give a simple evidence-gathering path.

support-request:
300–450 visible words around the form.
Do not restore an essay.
Form should be visible/actionable early.

thank-you:
retain concise truthful confirmation language.

the-lima-charlie-aero-standard:
1,150–1,350 words plus one real “standard in practice” evidence sequence.
This is an institutional methodology page, not founder mythology.

updates:
400–600 useful words as a hub plus actual update entries.
Do not pad if there are not enough substantive updates.

---

# 17. THE LIMA CHARLIE AERO STANDARD

Present the Standard as the organization’s operating method.

The page should describe a disciplined sequence such as:

1. identify the aircraft/problem context;
2. gather records and owner observations;
3. inspect the relevant system and surrounding installation;
4. document actual evidence and measurements;
5. define work scope from evidence and applicable instructions;
6. perform/record work within applicable authority and documentation requirements.

Do not create unsupported guarantees.

Add a real, factual “Standard in practice” module showing one maintenance sequence with actual site imagery and restrained captions.

The point is to prove that “documented evidence” is a method, not a slogan.

---

# 18. SUPPORT REQUEST FORM

Preserve a low-friction owner-first intake.

The form should allow an owner to begin even if they do not know:

- exact engine model
- exact diagnosis
- exact component
- tail number
- complete records

Required principles:

- short intro;
- form visible/actionable early;
- neutral topic selection;
- “not sure” path;
- name;
- message;
- contact method;
- email-only path;
- phone-only path;
- technical aircraft details optional;
- no fake file-upload promise if upload is not actually implemented;
- no fake appointment booking;
- no fake queue position;
- no fake response-time promise;
- no fake “copy sent” claim unless a copy is actually sent;
- no claim that browser navigation to thank-you proves inbox delivery.

Keep provider/form-delivery verification separate from client-side validation.

Actual inbox delivery is an external validation gate.

---

# 19. NAVIGATION AND CTA ARCHITECTURE

Primary CTA:

Request Service

Use contextual secondary CTAs such as:

- Start With the Symptom
- Prebuy First Inquiry
- Review Aircraft Records
- ROTAX Support
- E-PROPS Support
- Avionics / Electrical Support

Do not repeat every CTA on every page.

Phone/text/email presentation should use business language:

Call the Shop
Text the Shop
Email Lima Charlie Aero
Contact Lima Charlie Aero

Use natural variants to avoid template monotony.

Navigation should prioritize owner tasks, not internal mechanic taxonomy.

---

# 20. LOCAL SEO

Do not create thin location pages.

Use one strong service-area page plus naturally localized service pages.

Core truthful location/entity signals:

- Lima Charlie Aero
- KAKH
- Gastonia, North Carolina
- Charlotte regional relevance where appropriate
- Carolinas regional relevance where appropriate

Do not claim coverage, pickup, travel, mobile service, or response radius unless supported.

Keep business name, phone, website, and address/location data internally consistent.

Create:

docs/LOCAL_SEO_HANDOFF.md

Include:

- canonical business name
- canonical phone
- canonical site URL
- KAKH/Gastonia representation
- Google Business Profile consistency checklist
- suggested truthful service/category mapping for later manual verification
- photo-update strategy using permission-cleared real work
- review-request policy: legitimate and neutral, never fabricated/incentivized

Do not edit Google Business Profile in this task.

---

# 21. SEO METADATA

Every indexable page must have:

- one unique title
- one page-specific meta description
- one H1
- one canonical
- canonical matching preferred sitemap URL
- Open Graph URL matching canonical
- useful Open Graph image where appropriate
- meaningful internal links
- indexability consistent with route purpose

Generate a route-level matrix:

evidence/SEO_ROUTE_MAP.md

For every route record:

- intent
- index/noindex
- title
- description
- H1
- canonical
- sitemap inclusion
- structured-data types
- key internal links
- primary proof image
- local intent where relevant

Do not use arbitrary keyword density.

Do not stuff “Charlotte” into every title.

---

# 22. INDEXABILITY

Preferred decision:

joseph-helminiak-bio.html remains the primary indexable founder authority page.

about-credentials.html should be noindex,follow unless RC3 makes it truly distinct and substantial.

Utility pages such as:

404
thank-you
card

should not become search-entry pages merely because they exist.

Generate sitemap.xml from route metadata rather than manually maintaining it.

Canonical, sitemap, internal link, Open Graph URL, and schema URL signals must agree.

---

# 23. STRUCTURED DATA

Restore page semantics without recreating an oversized duplicative schema graph.

Use stable entity IDs.

Recommended stable entities:

https://limacharlieaero.com/#business
https://limacharlieaero.com/#organization
https://limacharlieaero.com/#joseph-helminiak

Homepage should represent, where truthful:

- Organization
- LocalBusiness or the most specific truthful supported subtype
- WebSite
- WebPage

Service pages:

- WebPage
- Service
- BreadcrumbList

FAQ:

- FAQPage
- Question
- Answer

Only for Q&A visibly present on the page.

Founder bio:

- ProfilePage
- Person
- worksFor linking to business entity

Updates/notices where suitable:

- Article or BlogPosting
- headline
- datePublished
- dateModified
- author
- publisher
- image
- mainEntityOfPage

Do not add structured data that claims:

- reviews that do not exist;
- aggregate ratings;
- prices that are not public;
- employee counts;
- unsupported service areas;
- unsupported credentials.

Structured data must match visible content.

Add automated schema validation checks for JSON parsing, expected types, canonical URL consistency, and duplicate entity ID errors.

---

# 24. AI-SEARCH / GENERATIVE-SEARCH READINESS

Do not create speculative hidden AI text.

Do not create machine-only summaries.

Do not mass-produce AI-generated question pages.

Build extractable factual passages into visible content.

Examples of useful patterns:

What Lima Charlie Aero supports:
A concise factual statement of aircraft/service scope and location.

What information to send:
A concise list of aircraft, engine, operating-condition, recent-maintenance, indication, photo, and records context appropriate to the page.

What a symptom does not prove:
A concise boundary statement preventing overdiagnosis.

These blocks should improve humans first.

Check robots.txt so it does not unintentionally block normal search crawling or OpenAI search crawling.

Do not alter training-crawler policy without explicit product direction. Search visibility and model-training policy are separate decisions.

---

# 25. INTERNAL LINKING

Build contextual links based on owner intent.

Examples:

High oil temperature:
link to cooling/oil temperature problems, installation review, support request.

Vibration:
link to gearbox/propeller vibration, installation review, records, support request.

Fuel pressure:
link to fuel-delivery page, engine-systems hub, start-with-symptom.

Prebuy:
link to records review, prebuy first inquiry, service area, support request.

E-PROPS:
link to vibration support where relevant, services, contact/request service.

Do not create footer-scale link spam.

Do not create identical “related links” blocks on every route.

---

# 26. IMAGE PROCESSING

Implement a deterministic responsive image pipeline.

Preferred generated formats:

- AVIF when practical
- WebP
- fallback PNG/JPEG only where needed

Generate useful width variants.

Use width/height or aspect-ratio information to prevent layout shift.

Use lazy loading below the fold.

Do not lazy-load the LCP hero image.

Use fetch priority/preload only when measured and justified.

Do not ship huge originals merely because they exist.

Preserve enough image quality to make technical evidence useful.

Image optimization must not crop away the actual defect, measurement, connector, crack, wear, logbook detail, or other proof subject.

---

# 27. VISUAL DESIGN

Preserve the professional Lima Charlie Aero visual identity unless a small adjustment improves usability.

Do not redesign the brand from scratch.

Avoid:

- generic SaaS aesthetic
- all-white sterile cards with no visual evidence
- oversized founder branding
- excessive gradients
- animation for animation’s sake
- generic aviation stock-photo hero
- carousel dependency
- tiny captions
- low-contrast gray-on-gray copy
- giant empty spacing that pushes evidence below the fold

Use:

- stable visual hierarchy
- restrained dark/aviation technical accents
- real work photography
- clear section rhythm
- varied but coherent layouts
- readable line lengths
- strong heading hierarchy
- clear CTA hierarchy
- visual evidence close to the claim it supports

The site should feel maintained and current, not “old static HTML,” while remaining technically lightweight.

---

# 28. RESPONSIVE / MOBILE

Mobile-first verification widths:

320
375
390
768
1024
1440

Key requirements:

- no horizontal overflow;
- touch targets usable;
- navigation usable with keyboard and touch;
- no clipped proof captions;
- no image subject cropped out at mobile;
- forms usable without zoom;
- primary CTA obvious;
- proof modules remain understandable in one-column form;
- headings wrap intentionally;
- no hero text/image collision;
- tables transform or scroll accessibly where necessary.

---

# 29. ACCESSIBILITY

Target WCAG 2.2 AA.

Requirements include:

- semantic landmarks;
- logical heading hierarchy;
- keyboard navigation;
- visible focus states;
- skip link;
- meaningful alt text;
- decorative images empty-alt where appropriate;
- labels and instructions for form controls;
- accessible validation;
- sufficient contrast;
- reduced-motion support;
- no keyboard traps;
- no required information conveyed only by color;
- proper language attribute;
- accessible menu state;
- accessible error/success messages.

Automated axe serious/critical failures:

0

Representative Lighthouse Accessibility:

98 or higher

Do manual keyboard checks in addition to automation.

---

# 30. PERFORMANCE GATES

Performance must remain a first-class engineering constraint.

Representative routes:

- homepage
- services
- E-PROPS
- ROTAX engine systems
- vibration
- installation review
- prebuy
- support request

Controlled lab gates:

Lighthouse Performance: 95 or higher
Lighthouse Accessibility: 98 or higher
Lighthouse SEO: 100 unless a documented tool false positive
Homepage / E-PROPS LCP: 1.8 seconds or lower in the controlled test environment
CLS: 0.05 or lower
TBT: 100 ms or lower
Homepage comparable initial transfer target: 350 KB or lower
Serious/critical axe failures: 0
Images causing layout shift: 0

Do not claim field Core Web Vitals from laboratory measurements.

If a proof image causes a measurable regression, optimize it rather than deleting the proof requirement.

---

# 31. TECHNICAL TRUTH AND AVIATION BOUNDARIES

Do not invent technical claims.

Do not invent ROTAX document identifiers.

Do not change applicability of a service bulletin or notice from memory.

Do not imply manufacturer authorization or factory status unless documented.

Do not imply a maintenance privilege beyond the supported credential/aircraft category.

Do not imply that one symptom proves one failed component.

Do not advise indiscriminate expensive-component swapping.

Use wording such as:

- evidence
- inspection
- measurement
- aircraft-specific context
- installation context
- applicable current instructions
- records
- troubleshooting sequence

where technically appropriate.

Technical caution should be contextual, not repeated boilerplate.

---

# 32. SPECIFIC OWNER-FACING TECHNICAL THEMES

Preserve these useful concepts where relevant:

- symptoms are not diagnoses;
- recent maintenance matters;
- configuration and installation matter;
- surrounding systems can imitate an engine fault;
- records help establish chronology;
- a measured value needs context;
- stains/residue may not identify the source;
- electrical connection faults can imitate expensive component failures;
- propeller/load/gearbox/installations interact;
- fuel contamination/restriction/venting/pump/installations need evidence;
- owners can begin with what they observe rather than a diagnosis.

---

# 33. UPDATES / FRESHNESS

The site should not require fake “freshness.”

Create a maintainable update system through content/updates.json or equivalent.

Updates should support:

- date
- title
- short summary
- relevant route/category
- source/reference where needed
- dateModified
- author/publisher identity

Do not auto-publish meaningless weekly filler.

The architecture should make legitimate short shop updates, owner notices, technical notes, and documentation changes easy to publish later.

---

# 34. CONTENT RETENTION REGISTER

Create:

evidence/CONTENT_RETENTION_REGISTER.md

For all 39 routes record:

- live baseline route present?
- live baseline approximate useful content
- RC3 purpose
- substantive concepts retained
- substantive concepts added
- concepts removed
- reason for removal
- proof assets used
- indexability
- target word band
- final word count
- reviewer notes

No major content deletion should occur without a documented reason.

---

# 35. PROOF-OF-WORK REGISTER

Create:

evidence/PROOF_OF_WORK_REGISTER.md

For each deployed proof sequence record:

- page
- section
- source asset(s)
- optimized asset(s)
- visible caption
- alt text
- factual claim supported
- permission-register reference
- whether sequence implies chronology
- evidence supporting chronology if applicable

This register is mandatory.

---

# 36. HUMAN-FACTORS / DESIGN MATRIX

Create:

evidence/HUMAN_FACTORS_DESIGN_MATRIX.md

For each major page record:

- visitor question
- answer visible in first screen / early content?
- location visible?
- service scope clear?
- proof visible?
- CTA clear?
- technical jargon explained?
- mobile behavior checked?
- main cognitive burden
- correction made

Major pages:

homepage
services
ROTAX hub
engine systems
vibration
installation review
fuel pressure
E-PROPS
avionics
prebuy
records
LCA Standard
contact
support request
service area

---

# 37. REQUIRED AUTOMATED CHECKS

Build or extend automated verification to check:

1. all expected routes generated;
2. no unexpected public route removed;
3. unique title per indexable route;
4. unique meta description per indexable route where appropriate;
5. exactly one H1;
6. canonical present and valid;
7. canonical matches route metadata;
8. sitemap/canonical consistency;
9. internal broken links;
10. local asset references;
11. missing images;
12. image dimensions/aspect metadata;
13. banned founder-centric phrases;
14. repetition thresholds;
15. public word-count report;
16. schema JSON parse;
17. expected schema types by route class;
18. stable entity IDs;
19. no fake review/rating markup;
20. form semantics;
21. direct thank-you behavior;
22. 404 behavior;
23. redirects;
24. keyboard menu;
25. reduced motion;
26. axe;
27. representative screenshots;
28. horizontal overflow;
29. proof requirements;
30. asset permission register coverage;
31. source-to-dist determinism;
32. clean checkout build reproducibility.

A test is not PASS because the test file exists.

Run it.

---

# 38. CODEX MANDATORY CLOSED LOOP

This task is not complete after the first successful build.

Execute this loop:

PHASE A — BASELINE AUDIT
- record starting branch SHA;
- inventory public routes;
- inventory assets;
- inventory content;
- inventory metadata/schema;
- run current reference checks;
- identify reusable proof images;
- record starting state.

PHASE B — SOURCE ARCHITECTURE
- create/restore maintainable structured source;
- centralize templates/CSS/JS;
- build deterministic generation into dist;
- preserve current live baseline only through Git history/baseline evidence, not duplicate uncontrolled pseudo-source.

PHASE C — IMPLEMENTATION
- implement company-first warm voice;
- implement proof architecture;
- restore/add target routes;
- implement page content requirements;
- implement SEO/schema/internal links;
- implement responsive images;
- implement accessibility;
- implement owner-first navigation/form behavior.

PHASE D — FIRST BUILD
- perform clean build;
- record generated file manifest and hashes.

PHASE E — AUTOMATED VERIFICATION
- static/reference checks;
- route checks;
- content regression;
- brand regression;
- proof regression;
- schema checks;
- accessibility;
- browser checks;
- responsive checks;
- performance checks.

PHASE F — CODEX VISUAL SELF-REVIEW
Render and inspect the actual generated site.

At minimum inspect:

homepage desktop
homepage mobile
services desktop/mobile
E-PROPS desktop/mobile
ROTAX hub desktop/mobile
vibration desktop/mobile
installation review desktop/mobile
fuel page desktop/mobile
prebuy desktop/mobile
LCA Standard desktop/mobile
contact desktop/mobile
support request desktop/mobile

Do not merely verify that screenshots were created.

Inspect them for:

- cold/sterile sections;
- proof buried too low;
- wrong images;
- generic captions;
- awkward image crops;
- repetitive sections;
- founder overexposure;
- weak CTA hierarchy;
- long unbroken text walls;
- excessive card repetition;
- mobile overflow;
- cramped captions;
- visual imbalance;
- misleading sequence;
- missing technical context.

PHASE G — DEFECT REGISTER
Create:

evidence/DEFECT_CORRECTION_REGISTER.md

Classify:

P0 release blocker
P1 major
P2 meaningful
P3 polish

Log:

- defect
- page
- evidence
- cause
- correction
- retest result

PHASE H — CORRECTION
Fix:

- every specification failure;
- every P0;
- every P1;
- practical P2 defects that materially affect UX, proof, SEO, accessibility, or trust.

Do not leave a known locally-correctable P1 because the first build “mostly works.”

PHASE I — REBUILD AND FULL RELEVANT RETEST
Repeat the relevant suite after corrections.

If a correction changes shared templates, navigation, schema, CSS, JS, or image processing, rerun all affected route checks, not only the page where the defect was noticed.

PHASE J — CLEAN-ROOM REPRODUCIBILITY
From a fresh checkout/copy of the final branch:

- install pinned dependencies;
- build;
- verify;
- compare generated manifest/hashes where deterministic;
- ensure no hidden local files are required.

PHASE K — FREEZE
Record final candidate commit SHA.

Do not modify the candidate after final evidence without rerunning affected tests.

---

# 39. RELEASE / REVIEW ARTIFACTS

Produce, but do not merge or deploy:

LCA_SITE_v102_0_0_RC3_DEPLOYABLE.zip
LCA_SITE_v102_0_0_RC3_SOURCE_AND_VERIFICATION.zip
LCA_RELEASE_REPORT_v102_0_0_RC3.md
SHA256SUMS.txt

If committing large ZIP artifacts would pollute permanent Git history, do not add them to the mergeable source tree. Keep them as Codex task artifacts or a clearly excluded temporary release-artifacts location and report exact hashes.

The source branch itself must contain enough tooling to reproduce them.

The source/verification package must include or be reproducible from:

- CONTENT_RETENTION_REGISTER
- PROOF_OF_WORK_REGISTER
- ASSET_PERMISSIONS_REGISTER
- SEO_ROUTE_MAP
- LOCAL_SEO_HANDOFF
- HUMAN_FACTORS_DESIGN_MATRIX
- DESIGN_SEO_REVIEW_CHECKLIST
- DEFECT_CORRECTION_REGISTER
- first-pass test evidence
- final-pass test evidence
- representative mobile/desktop screenshots
- performance evidence
- route manifest
- release manifest

---

# 40. DESIGN/SEO HANDOFF PACKAGE

The independent reviewer must be able to review the site without trusting Codex’s summary.

Provide:

1. starting branch SHA;
2. final branch SHA;
3. all meaningful commits;
4. full changed-file inventory;
5. route inventory;
6. before/after homepage screenshots mobile and desktop;
7. before/after screenshots for representative service journeys;
8. proof-of-work screenshots;
9. image source → optimized file → page placement matrix;
10. content retention matrix;
11. per-route SEO matrix;
12. structured-data matrix;
13. human-factors matrix;
14. accessibility results;
15. broken-link/reference results;
16. performance results;
17. founder-language/repetition report;
18. defect/correction register;
19. unresolved external blockers;
20. package hashes.

Do not claim “looks good” as evidence.

---

# 41. INDEPENDENT REVIEW ORDER

Prepare the branch so the Design/SEO reviewer can review in this order:

1. homepage mobile as a visitor;
2. homepage desktop;
3. services;
4. E-PROPS;
5. LCA Standard;
6. ROTAX hub;
7. vibration;
8. installation review;
9. fuel-delivery;
10. prebuy;
11. avionics;
12. records review;
13. contact;
14. support request;
15. service area;
16. only then read Codex’s release report and automated evidence.

The purpose is to prevent automated PASS results from biasing the human-facing design judgment.

---

# 42. WEIGHTED RELEASE SCORE TARGET

Prepare evidence for this independent scoring model:

Human factors / UX: 15%
Proof-of-work / trust: 20%
Content depth / technical usefulness: 15%
SEO / local / AI-search readiness: 15%
Performance: 12%
Accessibility: 10%
Brand voice / scalability: 13%

Target:

Weighted total at least 92/100
No category below 85
Proof-of-work at least 92
Brand voice/scalability at least 92
SEO at least 90
0 P0 defects
0 P1 defects

Codex may self-assess for defect discovery, but Codex does not grant final approval.

---

# 43. GIT WORKFLOW

Work only on:

rc3-proof-of-work-seo

Do not create a competing redesign branch.

Do not modify main.

Do not merge.

Use meaningful commits, for example:

- establish maintainable source architecture
- implement company voice and owner navigation
- implement proof-of-work evidence components
- restore route content and internal linking
- implement structured data and SEO route metadata
- implement image pipeline and accessibility
- add verification suite
- correct first-pass defects
- finalize RC3 evidence and release report

The existing draft PR is the review vehicle.

Push changes to the same RC3 branch.

Do not open a second competing PR.

When complete, update the existing PR description or add a final PR comment summarizing:

- final SHA
- test status
- evidence locations
- external blockers
- terminal status

Do not merge.

---

# 44. OUT-OF-SCOPE ITEMS

Do not:

- deploy to Cloudflare;
- modify DNS;
- change domain registration;
- change email/Workspace settings;
- alter Formspree account configuration;
- publish Google Business Profile changes;
- send customer communications;
- create fake reviews;
- buy services;
- add tracking/advertising systems without explicit approval;
- add a CMS;
- add a heavy JS framework;
- change pricing/rates unless source truth explicitly supports it.

Cloudflare integration will be handled separately after RC3 design/SEO approval.

---

# 45. STOP CONDITIONS

You may stop before engineering-candidate completion only for a genuine blocker such as:

- missing repository permission;
- missing required source file that cannot be reconstructed;
- dependency install impossibility;
- an external service credential required for a test;
- unresolved asset-rights decision that prevents publication of a required image;
- contradictory specification that cannot be resolved from repository truth.

If blocked:

1. preserve completed work;
2. commit safe progress;
3. state the exact blocker;
4. state what is complete;
5. state the smallest user action required;
6. do not claim candidate completion.

---

# 46. FINAL RESPONSE FORMAT

When all locally correctable work is complete, post to the pull request:

ENGINEERING CANDIDATE COMPLETE — DESIGN/SEO SIGN-OFF REQUIRED

Then report:

- final branch SHA
- build command
- test commands
- performance summary
- accessibility summary
- route count
- proof-subject count
- key proof modules implemented
- content-retention status
- SEO/schema status
- unresolved external validations
- release artifact hashes
- evidence directory locations
- confirmation that main was not modified
- confirmation that Cloudflare was not deployed

---

# 47. FINAL EXECUTION COMMAND

Execute this entire specification now.

Do not stop after planning.

Do not stop after the first build.

Do not stop after automated tests pass.

Implement, inspect, correct, rebuild, retest, package, commit, push to rc3-proof-of-work-seo, and leave the pull request ready for independent Design/SEO review.

Do not merge.

Final status must remain:

ENGINEERING CANDIDATE COMPLETE — DESIGN/SEO SIGN-OFF REQUIRED
