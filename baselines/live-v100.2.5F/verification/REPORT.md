# Verified live baseline import v100.2.5F

Source: `LCA_SOURCE_OF_TRUTH_BASELINE_v100_2_5F_DEPLOYABLE(1).zip`

Archive SHA-256: `e160c234b86aac2076db101c1b2e1acd27c46ed010866fd1aa6b21ff8214710a`

Starting main commit: `938c9fde853f902b215dc4adfdf2e35041f37575`

Starting import branch commit: `3a1640658143096da6b04efaaf5982b00b83af33`

## Results

| Requirement | Result |
| --- | --- |
| Website files at original repository-root paths | PASS: 214 |
| Total uncompressed website bytes | PASS: 14,184,009 |
| Direct byte comparison and per-file SHA-256 against ZIP | PASS: 214/214 |
| Missing or additional website files | None |
| Renaming, redesign, optimization, content changes | None |
| Binary preservation | PASS: direct byte comparison and Git blob identity |
| Static local references | PASS: 1,301 checked, zero missing targets |
| Representative renders | PASS: six pages at 1440×1000 and 390×844 |
| Runtime observations | No page errors, local HTTP failures, broken eager-loaded images, or horizontal overflow in 12 renders |
| Visual inspection | Desktop/mobile contact sheet inspected; headers, text, imagery and page structure render |

Machine-readable evidence: `manifest.json`, `verification.json`, `render-results.json`. Full-page screenshots are stored as WebP evidence (very tall pages split into numbered parts); screenshot compression does not affect any website file.

The original README and project-control documents are retained. The import instruction remains under `docs/`, not as a root-level instruction file. All new verification material is under `baselines/live-v100.2.5F/verification/`; it is excluded from the 214-file website comparison. No build transformation is required for this static baseline.

## Reproduction

From the repository root:

```sh
python3 baselines/live-v100.2.5F/verification/verify.py /path/to/source.zip
node baselines/live-v100.2.5F/verification/render.mjs .
```

The render script requires Playwright and its Chromium runtime (or `CHROMIUM_EXECUTABLE`). The executed environment used Chromium 153.0.8010.0 with the Sparticuz launch arguments and locally extracted SwiftShader libraries. The portable script uses normal Chromium launch arguments. Generated PNG screenshots may be converted to WebP for review storage.

## Scope and discrepancies

No source/import discrepancies were found. Static verification covers HTML attributes and srcsets, CSS URLs, literal JS asset paths and manifest icons. External services, arbitrary dynamically computed URLs, fragment correctness and actual form delivery are outside that check. Rendering used a local static server with extensionless HTML resolution; production hosting behavior and `_redirects` enforcement were not exercised by that server. Redirect destinations were resolved by the static reference check. No deployment, production mutation, or merge to main was performed.

The archive contents take precedence over future redesign requirements. This PR establishes the unchanged rollback baseline for independent review.
