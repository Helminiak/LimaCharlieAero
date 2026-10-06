# Browser and accessibility results

Final full sweep: Chromium 153.0.8010.0 and Firefox 155.0 PASS. 124 route/redirect/header cases, 276 responsive layout cases, 39 axe route scans, 20 mocked form cases; no page-script errors, horizontal overflow, broken images or axe violations. Tested widths: 320, 375, 390, 768, 1024, 1440. All 39 routes receive Chromium/axe checks; Firefox receives seven representative routes across all widths. Keyboard menu, skip/focus, reduced-motion mode, no-JS paths and accessible form errors are exercised in verify_browser.mjs.

After the final document-mask adjustment, the affected E-PROPS page passed six additional layout/axe checks. Shared templates were unchanged after the final full sweep. See final-checks.json and affected-browser-checks.json. Automated keyboard interaction and screenshot inspection are not a physical assistive-technology user study.

WebKit: NOT RUN — EXTERNAL VALIDATION REQUIRED. Installed browser could not launch because native host libraries including libGLESv2.so.2 are unavailable. This was not silently converted to PASS. Physical Safari/iOS/Android, actual screen-reader testing, real Formspree inbox delivery, production Cloudflare and field performance remain unvalidated. Form requests were locally intercepted, never sent to a real inbox.
