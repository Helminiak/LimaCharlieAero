# LCA v103 Phase 9 independent engineering review

**Decision — approve with conditions for a private owner fact-check.** The frozen candidate reproduces, serves the RC3 routes, and keeps the five draft narratives out of its public artifact. The owner should receive the vibration, maintenance-privilege, and document-image findings with the preview. Those findings affect what a reader could reasonably believe about work performed or authorized. Several publication safeguards also pass inputs they should reject.

Reviewed 2026-11-21. Candidate `7d2e68eb8bbf401df023424203d896ecaefd5e2f`, detached. Comparison `1521869e0bc1e7136459404d2f16232bb69d045a`. All build, browser, package, and fault-injection work ran in independent exports under `/tmp/lca-phase9-AaMOxn`. File and line references below refer to the frozen source. Commands using `dist/` run in the candidate export `c/`. Review helpers and logs run from its parent. The regulatory comparison uses the verified facts supplied for this review and the frozen §7 register. All site and form probes targeted loopback or used local interception. Miniflare itself made an external bootstrap request on first start, documented in X-15.

To reproduce in an independent export, run the following with the pinned dependencies installed. The final browser command targets the actual preview root.

```sh
export CLOUDFLARE_CF_FETCH_ENABLED=false WRANGLER_SEND_METRICS=false
python3 tools/build.py
python3 tools/build.py --output repro-dist
diff -qr dist repro-dist
python3 tools/build.py --preview
npm test
python3 tools/verify_static.py dist-preview
node tools/verify_browser.mjs dist-preview independent-preview
```

## What passed on the frozen bytes

| Check | Independent result |
|---|---|
| Public reproducibility | `npm run build` and `python3 tools/build.py --output repro-dist` each produced 318 files, 40 HTML pages, and 8,461,869 bytes. Independently enumerated, path-sorted SHA-256 lists matched with `cmp`. The lists both hash to `b3dedff06710d8c4e4b2d7745842d53d3bf8edac46857d729ea939fd6a66f3dc`. |
| Private preview | `python3 tools/build.py --preview` produced 324 files, 40 HTML pages, and 8,509,397 bytes. The build's SHA-256 JSON manifest digests were `ae0037557c9bd1145fc7b3f1cf393023247bb903e3738dd255ca0c31aa1e04f3` for public and `aa298e2623f03e6c5e7be9dcf482c4642e7a43e640a8f57bbe34a10cf9a9ff2f` for preview. |
| Candidate suites | `npm test` exited 0. Static checks passed 4,196 public and 4,231 preview assertions. The preview static and browser suites ran separately. Each browser run covered 127 route scenarios, 240 layouts, 40 axe scans, and 24 form checks. Chromium 153.0.8010.12 reported zero axe violations. Axe left color-contrast decisions incomplete on five public and six preview pages. Firefox and WebKit executables were absent. |
| RC3 routes and redirects | Rebuilt RC3 yielded 39 HTML files. v103 retained every one and added only `/our-work`. `python httpcheck.py` checked response **bodies** against disk over local HTTPS. All 40 canonical paths served the right bytes. All 79 alternate spellings returned one 308 followed by 200. All nine explicit legacy aliases returned the specified 301, preserved a test query, and reached the correct route. Missing paths returned 404. Requests for the two configuration files redirected to a real 404. |
| Crawling and metadata | Independently parsed XML, HTML and JSON-LD for 80 pages. Public sitemap contained exactly 36 unique indexable URLs. The four exclusions were `/404`, `/thank-you`, `/card`, and `/about-credentials`. Preview had 40 noindex pages and an empty sitemap. Canonical, OG URL and WebPage-family JSON-LD URLs agreed on every route. All six social cards resolved to local 1200×630 JPEGs with OG alt text. All internal links with fragments in the newly built pages resolved. The RC3 inbound fragment regression is X-06. |
| Headers and CSP | `_headers`, `_redirects`, and `robots.txt` matched RC3 byte for byte. Local HTTPS with the production Host header returned HSTS with subdomains and preload, `nosniff`, `SAMEORIGIN`, strict-origin-when-cross-origin, and the device restrictions. Clean HTML revalidated. Hashed CSS was immutable for one year. The production-host CSP consists of `upgrade-insecure-requests`. It provides transport upgrading and imposes no script, connection, or form-destination allowlist. The inline menu and native/enhanced Formspree paths are compatible with this policy. The bare loopback host omitted both host-specific headers as configured. |
| Intake | Enhanced legacy `?request=rotax-asb-review` selected `notice` and removed the query. The nine supported topic paths, retry, duplicate click, timeout, offline, rejected and unconfirmed responses passed local mocks. Without JS, navigation and the native email, phone, and text paths worked. Invalid contact details were blocked and valid payloads were captured locally. The no-JS form leaves the topic for the user to select. A separate stale-query failure is X-05. Provider validation, delivery, and the inbox remain unverified. |
| Frozen draft isolation | `python audit.py` found 0 of 40 distinct draft slugs, titles, and stage strings in the public text corpus, and 40 of 40 in preview. Public had zero case articles, CreativeWork case nodes, owner markers, or draft ribbons. Preview had five ordered seven-stage records, five CreativeWork nodes, and ribbons on home and Our Work. No case text appeared in public OG, updates, or sitemap. There is no shipped site-search index. The only public JSON-formatted data file was the web manifest, alongside inline JSON-LD. Public contains zero correspondence files and preview contains six. Normal deployment packaging contained only the 318 public files. |
| Registration and redactions | Scanned filenames, decoded HTML including alt/captions and meta attributes, JSON-LD, manifest, and other text. No US registration-pattern hits or hits for the selected international patterns. Independent image/container scans found zero EXIF, XMP, ICC or textual metadata indicators across 266 public and 272 preview rasters. I inspected the pixels of the G5 close and wide views, correspondence, NDT excerpt, E-PROPS documents, and an overview of the proof subjects. The 600×800 close-up has an opaque mask above the G5. The 925×141 correspondence crop shows only the two-line message body. `python redactions.py` regenerated the derivatives from those inspected pixels and matched all 3 G5 and all 5 correspondence variants byte for byte. X-03 covers different information still visible in document pixels. |
| Regulatory facts and business claims | The turbocharger notice gives November 23, 2026, the listed certified 915/916 iSc scope and action before further flight, with non-certified iS covered separately by the bulletin. It links the official rule. E-PROPS copy reserves manufacturer-level decisions and disclaims installation authority from a dealer quote. The RFSC credentials are attributed to the supplied listing through September 16, 2027. Current dealer status, training currency, trained category/class, and photo rights still require owner evidence. Of 15 registry subjects marked REVIEW REQUIRED, 14 appear in the public-mode HTML and all 15 in preview. |

### Performance spot check

`LCA_PERF_ROUTES=/,/e-props-dealer-support,/support-request,/our-work npm run verify:performance` exited 0. Lighthouse 13.5.0 used local Wrangler and cold mobile and desktop runs. These four routes cover the two special LCP budgets, intake, and the new hub. Node was 22.23.3, Playwright 1.63.0, Wrangler 4.147.0, Python 3.14.4, Pillow 12.3.0 and lxml 6.1.1. The initial public npm suite took about 65 seconds and the eight performance runs took about 51 seconds, measured from the fresh logs. The table uses the second performance run, with the emulator metadata lookup explicitly disabled.

| Route | Mobile P / A / SEO | Mobile LCP | Mobile CLS | Mobile TBT | Transfer bytes | Desktop P / LCP |
|---|---|---:|---:|---:|---:|---|
| `/` | 100 / 100 / 100 | 1,293 ms | 0.00733 | 0 ms | 325,665 | 100 / 471 ms |
| `/e-props-dealer-support` | 100 / 100 / 100 | 1,519 ms | 0.00060 | 0 ms | 197,353 | 100 / 394 ms |
| `/support-request` | 100 / 100 / 100 | 1,367 ms | 0.00388 | 0 ms | 112,408 | 100 / 372 ms |
| `/our-work` | 100 / 100 / 100 | 1,288 ms | 0.00032 | 0 ms | 176,147 | 100 / 494 ms |

The 1,800 ms LCP ceiling applies to home and E-PROPS. Both met it. These are lab measurements for four routes. At 390 CSS px, the public home and E-PROPS pages measured 6,312 and 5,599 px tall with JS enabled.

## Findings on the frozen pages

### X-01 · P1 · VERIFIED · Factual — the vibration page asserts an unsupported repair result

`tools/compositions.py:110`, `content/pages.json:1292`, `/rotax-gearbox-propeller-vibration`. An owner comparing shops sees two instrument displays labeled as a before/after correction. The same page says the records do not establish a paired repair result. The proof registry explicitly disclaims a before/after relationship for both subjects. Design §3 requests the shared caption, in direct conflict with the evidence rule in the RC3 master prompt at line 636. Keep the individual readings and remove the claimed sequence unless the owner supplies the dated job record tying configuration, conditions and corrective action together.

Evidence — `rg -o 'the supplied evidence does not prove a paired repair result|Measured 1.27 IPS → 0.04 IPS after correction\.' dist/rotax-gearbox-propeller-vibration.html` returned **both** sentences.

### X-02 · P1 · VERIFIED · Factual — the inspection limits omit material restrictions on return to service

`content/pages.json:417`, `/s-lsa-e-lsa-maintenance`. An owner considering a major repair to an FAA-approved product can read the limits box as saying the shop may sign it off if the appropriate data exists. The box never states the exclusion. Its experimental-aircraft sentence mentions operating limitations without identifying the restricted annual condition-inspection privilege. The copy follows the deck at line 105 but omits the substantive boundaries in design §7.

Evidence — `python copycheck.py` extracted “Major repairs and alterations follow the applicable manufacturer or FAA-approved data.” The full public corpus returned `21.191 0` and `65.109 0`. State the §65.109(b) limits in the box. Light-sport-category return to service excludes major repair or alteration on a product produced under an FAA approval. The experimental annual condition-inspection privilege covers §21.191(g), (i), (k) and (l). Maintenance is limited to trained category/class, and major repair requires the applicable additional FAA-acceptable training. Confirm the holder's scope before advertising that capability.

### X-03 · P2 · VERIFIED · Factual — full-size E-PROPS images expose owner-gated references and settings

`content/proof-assets.json:478` and `:493`, `tools/redact_proof.py:10`, `/e-props-dealer-support`. Opening the linked checklist reveals the aircraft type and exact propeller configuration. Opening the packet reveals the configuration reference and type-certificate reference that §6 CS-2 defaults to withholding. The checklist also retains aircraft-specific RPM targets despite the registry saying those settings are masked. The frozen files predate the redesign, but v103 explicitly links the originals at readable size. The images identify a TL-2000 application. They do not establish a connection to the Sling draft.

Evidence — `python audit.py` located the linked checklist on `e-props-dealer-support.html`. Decoding `dist/assets/images/proof/eprops-install-checklist-preview-1200.ed787e002be1.webp` showed “TL-2000 Sting Sport – DUR-3-175-C4-T (Configuration Control Record)”. The packet `eprops-engineering-packet-fanout-1200-clean.12a70dd3f874.webp` showed the same configuration and “EASA.P.512”. Mask the gated details or record an owner decision allowing these exact images and correct the registry description. The visually inspected G5 equipment box also retains a readable purchasing label and barcodes on the left, despite masking the serial field on the right. Include that label in its outstanding rights review.

### X-04 · P2 · VERIFIED · Factual — the gearbox notice leaves the decisive aircraft/model distinction implicit

`content/updates.json:10`, `/rotax-gearbox-notice`. An ASTM 912 UL/ULS/iS owner sees a broad engine-family summary and has to open the regulatory document to distinguish the FAA AD from the manufacturer's ASB. The current wording is qualified, but §7 says this boundary is already explicit. The generated page leaves the models and Table 1 unnamed.

Evidence — `python copycheck.py` returned “FAA AD 2026-16-11 has specific certified-engine, aircraft and installed-gearbox criteria.” The public copy contains no `UL/ULS` or `Table 1` text. Identify the listed certified 912 F/S/A/iSc and 914 F variants, Table 1 type-certificated aircraft, and applicable gearbox serials. The supplied register gives August 28, 2026 as the effective date. Say that ASTM 912 UL/ULS/iS use the manufacturer/LSA bulletin path. Preserve the official link.

### X-05 · P2 · VERIFIED · Methodological — a stale query can leave intake half initialized

`templates/site.js:14` and `:22`, `/support-request`. An unknown topic named like an inherited JavaScript object property resolves to a value that is absent from the select. Reading the missing option throws. By then the native phone form is hidden and native validation disabled, but the enhanced submit handler has not been installed. This also occurs with the inherited lookup in RC3. No submission was needed to verify it.

Evidence — `node independent-ui.cjs` against the local artifact returned `topic=toString, noValidate=true, phoneFallback=false` and “Cannot read properties of undefined (reading 'textContent')”. The controls `topic=random` and `request=rotax-asb-review` initialized normally. Use a closed mapping with an own-key check and retain native behavior until initialization succeeds.

### X-06 · P2 · VERIFIED · Acceptance-criteria — all 33 RC3 FAQ deep links lose their target

`tools/compositions.py:144`, `/faq#question-1` through `#question-33`. An old bookmark lands at the FAQ introduction instead of its question. The questions still exist under `section-N`. Checking only routes and links generated by v103 misses incoming RC3 URLs.

Evidence — comparing `//*[@id and starts-with(@id,"question-")]` in both built FAQ files returned `RC3 33, v103 0`. `node independent-ui.cjs` returned `/faq#question-1 { found: false }` and `/faq#section-1 { found: true }`, with and without JS. Preserve the former IDs at the corresponding questions. The broader comparison found 114 removed RC3 DOM IDs, including generic section IDs. This finding establishes the 33 identifiable question targets.

## Findings on publication and verification tooling

The following reproductions used disposable copies. A VERIFIED fixture means the stated behavior was observed under its specified input. The frozen public build's actual contents are recorded above.

### X-07 · P1 · VERIFIED · Methodological — a social card can publish a case-only image

`tools/build_assets.py:68`, `tools/build_assets.py:75`, `tools/render_site.py:57`. The ordinary image pipeline excludes the private correspondence, but the social-card generator reopens the original through the unrestricted registry. Selecting it as the Our Work social image publishes the letter under a different JPEG filename and supplies its private-context alt text. A social crawler can retrieve both through OG even when the case remains draft.

Evidence — in `social-fixture`, changed only `SOCIAL['work']` from the weld detail to `tl-ultralight-designer-correspondence`. `python tools/build.py && python tools/verify_static.py` returned `PASS, 4196 checks`. Public output contained zero files named for the correspondence, yet OG pointed to `social-work.9c14d5f6f9a4.jpg` with alt “Designer’s instruction to retain the inspection protocol”. I decoded the JPEG and read the letter. The frozen card `social-work.71920c32a001.jpg` is the ordinary weld photo. Enforce the same asset eligibility before producing social cards and alt text.

### X-08 · P1 · VERIFIED · Methodological — an unregistered proof original and its ICC text pass the public build

`tools/build_assets.py:8`, `tools/build_assets.py:24`, `tools/verify_static.py:25`. Leaving an original next to a registered, case-only derivative copies the original into the public asset tree. The original bytes retain metadata. The check examines selected EXIF/XMP fields and ignores ICC profile text. This conflicts with §8's requirement for build-time privacy treatment.

Evidence — in `fixture`, used a 20×20 WebP with a synthetic registration-like ICC description, registered one copy as case-only on a draft stage, and left a second copy unregistered under `assets-src/images/proof/`. `python tools/build.py && python tools/verify_static.py` returned `PASS, 4198 checks`. The registered copy had zero public outputs. Reading the other built file with Pillow ImageCms returned `original-canary.159f939dda98.webp → N123ZZ sample`. Restrict the public proof pool to declared, eligible assets. Sanitize or reject sensitive metadata on the full-size output as well as derivatives. The independent scan found zero ICC profiles in the frozen rasters.

### X-09 · P1 · VERIFIED · Methodological — an ordinary editor save drops an internal-publication flag

`tools/preview.py:47`, `tools/preview.py:51`, `tools/editorial.py:33`. An editorial record may have a public workflow state while an independent `internal` or `placeholder` flag suppresses publication. Editing its title or saving it unchanged reconstructs the object without these flags. The rebuild can put the entry on a standalone route, in updates, and in the sitemap. This is an inherited RC3 authoring defect. The frozen five editorial records have neither flag. A record whose state remains `draft` stays excluded.

Evidence — `python editcheck.py` performed a local editor save on a synthetic internal record with `state=published` and returned `before visibility False / local editor save 303 / after internal flag None / standalone True sitemap True updates True`. Preserve independent publication flags when updating editable fields. Add round-trip coverage for both flags separately from the draft-state test.

### X-10 · P2 · VERIFIED · Methodological — case publication accepts an explicit negative confirmation

`tools/cases.py:23` and `:30`. A data import can supply the string `"false"` as confirmation, a list containing a null source, and a filled Verification stage for a job labeled pending manufacturer review. Each passes validation and the record enters the public selection. The current five drafts have the correct stage order. Duplicate slugs, reordered stages, unknown evidence, and a plain unconfirmed promotion were all rejected.

Evidence — `python casecheck.py` returned `selected 1 owner_confirmation 'false' sources [None] status In progress · pending manufacturer review verification done`. Require an explicit typed or structured confirmation and nonempty source references. Encode the pending-verification rule in the case model so the stepper and status cannot disagree.

### X-11 · P2 · VERIFIED · Acceptance-criteria — the suite passes four draft leaks at once

`tools/verify_static.py:16`, `:48`, `:53`, `:60`, `:98`; `tools/verify_release_features.mjs:5`. Case articles and owner markers are checked, but prose without an owner marker can escape. Sitemap membership is checked one expected URL at a time, allowing extra URLs. There is no cross-output comparison against the actual draft content. The case-only subject coverage expression includes an observed case-only subject on the expected side whenever it is already observed. The parsed `sitemap`, `subject_ids`, and accumulated `used` set have no effect on these decisions.

Evidence — in `metadata-fixture`, inserted the first draft slug in an extra sitemap entry, its title in home OG description and a new `search-index.json`, and its first stage paragraph in `/updates`, all in the generator before manifest creation. `npm test` exited 0, including `PASS, 4197` static checks and the independent rebuild. `cat dist/search-index.json` returned `["TL-2000 Sting Sport: engine-mount crack, repair or replace"]`. Derive expected private/public sets independently, require exact sitemap membership, and exercise every publication surface with a unique draft canary. The frozen candidate has none of these four text leaks.

### X-12 · P2 · VERIFIED · Acceptance-criteria — the archive verifier reads RC3 evidence for a v103 ZIP

`tools/verify_package.mjs:3` and `:5`, `tools/package_source.py:18`. Following the documented packaging path produces a correct v103 public ZIP but gives the v103 source/evidence archive the RC3 filename. The extracted-package browser verifier compares against the tracked RC3 manifest and 39-route list. It fails on a correct extraction before opening a browser. In a shared archive directory the hard-coded source filename can also collide with an existing RC3 archive.

Evidence — `npm run package` emitted `LCA_SITE_v103_owner_preview_DEPLOYABLE.zip` (318 files, clean extraction matched) and `LCA_SITE_v102_0_0_RC3_SOURCE_AND_VERIFICATION.zip`. `node tools/verify_package.mjs` exited 1 on `404.html` with actual `eb7f05a1…` and expected `90cd71d7…`. Use the selected release's frozen manifest, routes, and release identifier throughout the packaging workflow.

### X-13 · P3 · VERIFIED · Acceptance-criteria — a misspelled performance route exits successfully with zero measurements

`tools/performance.mjs:20`, `:56`, `:66`. A typo in a targeted retest filters out all routes. The final failure predicate has no rows to inspect. A mixed list can silently omit just one requested route.

Evidence — in scratch, `LCA_PERF_ROUTES=/our-wrok node tools/performance.mjs dist --after-only` returned `exit=0` and wrote `"runs": []`. Reject unknown routes and assert the expected number of completed mobile and desktop runs. The independent performance table above contains eight actual runs.

### X-14 · P3 · PLAUSIBLE · Factual — the turbocharger review attribution needs owner confirmation

`content/updates.json:54`, `/rotax-turbocharger-notice`. A reader can take the reviewer label as an actual technical review by the shop. The repository attributes a source check to Codex in RC3, and the redesign copy deck prescribes the new label. A copy instruction alone does not document who performed that shop review. An owner review may exist outside the frozen materials.

Evidence — `git diff 1521869 HEAD -- content/updates.json` shows the reviewer changing from “Codex: source document/content review” with a sign-off qualification to “Lima Charlie Aero technical review”. `python copycheck.py` found the new label in the rendered notice. Confirm the reviewer and date, or attribute the document check to its actual source. This finding concerns attribution. The AD scope, effective date, and required timing on this notice agree with the supplied facts.

### X-15 · P2 · VERIFIED · Methodological — the local Wrangler harness makes an external request on a cold start

`tools/test-server.mjs:6`, used by the browser and performance harnesses. The wrapper disables Wrangler metrics but leaves Miniflare’s independent Request.cf lookup enabled. I missed this setting on the initial review run. The cold emulator fetched Cloudflare’s `cf.json` endpoint, contrary to the no-external-contact instruction. The dependency makes an uncredentialed GET for network metadata. Its request does not upload site files or contain a form submission.

Evidence — the cold scratch dependency tree created a 2,064-byte `node_modules/.mf/cf.json` at 11:53:15 UTC. `rg -n 'defaultCfFetchEndpoint|writeFile\)\(cfPath' node_modules/miniflare/dist/src/index.js` locates the endpoint and the write after a successful response. For isolated reviews set `CLOUDFLARE_CF_FETCH_ENABLED=false` alongside `WRANGLER_SEND_METRICS=false`. I removed the scratch cache, disabled the lookup, and reran the complete public npm suite and the eight spot-check measurements. Both exited 0 and no new cf.json cache was created.

**Review environment.** After the HTTPS probe runner exited, the temporary Wrangler listener continued to serve the public-mode artifact at `127.0.0.1:18839`, with its inspector on `127.0.0.1:19839`. The sandbox denied the scoped socket-close request. The scratch evidence directory is `/tmp/lca-phase9-AaMOxn`.

## Conditions and sign-off

1. Use this frozen preview for a private owner fact-check with X-01 through X-04 visible to the reviewer. Resolve the paired-result claim and maintenance scope before treating those pages as approved copy. Obtain a decision on the document pixels, outstanding subject rights, dealer/training evidence, and case facts.
2. Before promotion or distribution of a subsequent candidate, close the draft-asset and editorial leaks in X-07 through X-09, tighten case publication, and demonstrate that the intended public outputs pass while deliberately leaked copies fail. Retest native intake, old FAQ links, and the extracted package against that candidate's manifest.
3. Use the offline emulator settings in X-15 for future local reviews. Independent design/SEO acceptance remains open. This review makes no aesthetic objection. The factual disagreements concern the prescribed before/after caption, the regulatory limits copy, the scope of document redaction, and potentially the reviewer attribution. The methodological and acceptance-criteria findings identify how to reproduce the remaining engineering gaps.

**Verdict — approve with conditions.**
