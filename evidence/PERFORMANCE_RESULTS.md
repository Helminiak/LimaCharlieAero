# Final performance evidence

Mobile Lighthouse 13.5.0, Chromium 153, local route/header model, simulated throttling. These are laboratory measurements, not field p75 Core Web Vitals or INP. Each eight-route final run used an isolated browser after competing browser work stopped. Earlier failed runs are retained.

| Route | Performance | Accessibility | SEO | LCP ms | CLS | TBT ms | Transfer bytes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| / | 100 | 100 | 100 | 1657 | 0 | 0 | 202676 |
| /services | 100 | 100 | 100 | 1217 | 0 | 0 | 381294 |
| /e-props-dealer-support | 100 | 100 | 100 | 1205 | 0 | 0 | 303488 |
| /rotax-engine-systems-support | 100 | 100 | 100 | 1278 | 0 | 0 | 207923 |
| /rotax-gearbox-propeller-vibration | 100 | 100 | 100 | 1216 | 0 | 0 | 410430 |
| /rotax-installation-review | 100 | 100 | 100 | 1358 | 0 | 0 | 341910 |
| /light-sport-prebuy-evaluation | 100 | 100 | 100 | 1128 | 0 | 0 | 154746 |
| /support-request | 100 | 100 | 100 | 1205 | 0 | 0 | 62628 |

The homepage originally failed at 1.883 s in both concurrent and isolated tests. Header-only derivatives and a corrected declared aspect ratio reduced the final run to 1.657 s and zero CLS. An isolated correction run was 1.732 s. No unfavorable run was discarded. After the final signature-mask adjustment, the only affected page, E-PROPS, was rerun: P/A/SEO 100/100/100, LCP 1214 ms, CLS 0, TBT 0. Full results are in artifact-performance.json and affected-performance.json. Exact raw reports are losslessly compressed under lighthouse/*.json.gz.
