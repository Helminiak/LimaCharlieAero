# Baseline Import Instructions — live-v100.2.5F

This branch exists only to import and verify the current live Lima Charlie Aero website before any redesign work begins.

## Source artifact

Use the user-supplied archive:

`LCA_SOURCE_OF_TRUTH_BASELINE_v100_2_5F_DEPLOYABLE(1).zip`

Authoritative archive SHA-256:

`e160c234b86aac2076db101c1b2e1acd27c46ed010866fd1aa6b21ff8214710a`

Expected archive contents:

- 214 files
- 14,184,009 total uncompressed bytes

## Import requirements

1. Extract the archive without changing file names, paths, capitalization, or file contents.
2. Import the deployed website files at repository root so the Git tree represents the actual live deployed structure.
3. Do not redesign, refactor, compress, rename, delete, deduplicate, or optimize anything during this import step.
4. Preserve binary assets byte-for-byte.
5. Exclude this instruction file from the deployed web root after the verified import is merged; project-control documentation belongs under `docs/`.
6. Generate a machine-readable manifest containing, for every imported website file:
   - relative path
   - size in bytes
   - SHA-256
7. Verify:
   - file count = 214
   - total uncompressed bytes = 14,184,009
   - every imported file hash matches the source archive
   - no source-archive file is missing
   - no unintended website file is added
8. Run a local static-site reference check for missing HTML/CSS/JS/image/font/download targets.
9. Render representative pages to ensure the byte-identical import is operational.
10. Commit the verified import to this branch.
11. Open a pull request into `main` titled:
    `Import verified live website baseline v100.2.5F`
12. In the PR body, include:
    - source archive SHA-256
    - imported file count
    - total imported bytes
    - manifest verification result
    - broken-reference result
    - any unavoidable discrepancies
13. Do not begin RC3 redesign work in this branch.

## Acceptance gate

This baseline import is accepted only when the Git contents are proven to represent the supplied live archive exactly. After merge, the resulting `main` commit becomes the permanent pre-redesign rollback point.
