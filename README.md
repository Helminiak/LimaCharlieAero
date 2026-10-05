# Lima Charlie Aero Website

Private source repository for the Lima Charlie Aero website.

## Repository role

This repository is intended to become the authoritative, version-controlled source of truth for the website.

### Branch policy

- `main` = production-approved website source only.
- Substantial work is performed on named development branches.
- Codex implements code changes on development branches.
- Codex must complete its closed-loop implementation / verification cycle before review.
- ChatGPT serves as the independent design / SEO / human-factors reviewer.
- Changes merge to `main` only after review and acceptance.

## Current live baseline

The current live website baseline supplied for import is:

- Baseline ID: `live-v100.2.5F`
- Artifact: `LCA_SOURCE_OF_TRUTH_BASELINE_v100_2_5F_DEPLOYABLE(1).zip`
- SHA-256: `e160c234b86aac2076db101c1b2e1acd27c46ed010866fd1aa6b21ff8214710a`
- Files in archive: `214`
- Uncompressed bytes: `14,184,009`

The archive itself is the authoritative binary reference until its complete contents are imported and verified in Git.

## Change-control rule

Do not perform a major redesign directly on `main`.

The expected flow is:

```text
main
  -> development branch
  -> Codex implementation
  -> Codex closed-loop QA
  -> pull request
  -> independent design/SEO review
  -> corrections if required
  -> merge to main
  -> release/deployment
```

## Immediate next step

Import the exact `live-v100.2.5F` deployed contents into a controlled import branch, verify every file against the baseline archive, then merge that verified baseline into `main` before the next redesign branch is created.
