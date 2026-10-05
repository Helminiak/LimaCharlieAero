# RC3 defect and correction register

No open locally correctable P0/P1 remains after the listed corrections and relevant retests. External release gates below are not PASS results.

| ID | Severity | Defect / evidence | Cause | Correction | Retest |
| --- | --- | --- | --- | --- | --- |
| RC3-01 | P1 | `first-static-checks.json`: repeated “What happens next” exceeded limit | Shared generic copy | Page-specific headings and contextual sections | Current static repetition checks PASS |
| RC3-02 | P1 | Desktop intake screenshot: active Request Service text invisible | White button text combined with pale active-link background | Explicit dark active button background and border | Visual reinspection and final axe/browser sweep PASS |
| RC3-03 | P1 | Homepage LCP 1.803/1.806 s exceeded 1.8 s gate despite score 100 | Render-blocking stylesheet request; LCP trace identified lead text | Central CSS emitted inline; hero bytes reduced without removing proof | Initial correction passed; later 1.883 s regression addressed in RC3-10 |
| RC3-04 | P1 | Source-resolution E-PROPS document previews exposed registration, serial and named signature data | Historical filename/credit implied redaction but pixels still disclosed identifiers | Deterministic masks in `redact_proof.py`; captions distinguish process preview from instructions/approval | Source-resolution visual check; final static and browser tests PASS |
| RC3-05 | P1 | Technical routes had no contextual cross-links | Shared navigation existed but related service paths were omitted | Intent-specific links across 21 routes | 1,282 local references verified; route SEO matrix and final browser sweep PASS |
| RC3-06 | P2 | ROTAX hub was text-only in early content | No proof placement in hub source | Two relevant existing proof subjects after early sections | Final responsive/browser checks PASS; screenshot review |
| RC3-07 | P2 | Service-area wording could imply unconfirmed off-airport service | Overbroad inherited planning copy | Explicit coordination language without mobile-service promise | Source/content and visual review; current static checks PASS |
| RC3-08 | P1 engineering | Offline clean-room npm install failed on uncached zod | Incomplete package cache | Fresh online install from unchanged lockfile; preserve failure log | 156 pinned packages installed; final clean-room build comparison recorded separately |
| RC3-09 | P2 tooling | Targeted axe test harness failed before page scan | Used browser.newPage instead of explicit context required by axe | Explicit browser context | Full final axe suite independently PASS; targeted harness rerun recorded |

| RC3-10 | P1 | Final and isolated homepage LCP 1.883 s; CLS 0.01322 | Oversized header assets and incorrect declared wordmark ratio | Deterministic header derivatives; original brand masters preserved; correct 400:133 ratio | Isolated LCP 1.732 s, final eight-route LCP home 1.657 s / E-PROPS 1.205 s; CLS 0 on all eight; shared browser/visual rerun required before freeze |

## External gates, not locally correctable defects

- All 38 proof subjects retain REVIEW REQUIRED rights status. Public release remains on hold until the owner confirms rights and any identifiable-person/aircraft permissions.
- A verified maintenance chronology or causal before/after claim requires owner records. Current modules explicitly avoid such claims; Design/SEO must review whether additional documented chronology is needed.
- Real Formspree inbox delivery: NOT RUN — EXTERNAL VALIDATION REQUIRED. Test submissions were intercepted locally.
- Production Cloudflare behavior, DNS and deployment: NOT RUN — EXTERNAL VALIDATION REQUIRED / outside authorized scope. Local Wrangler behavior is separately tested.
- WebKit native runtime lacks required host libraries. Chromium and Firefox pass; WebKit and physical Safari/mobile-device testing remain external validation requirements.
- Actual screen-reader and physical-device usability checks and independent Design/SEO acceptance remain unperformed. No weighted release approval is claimed.
