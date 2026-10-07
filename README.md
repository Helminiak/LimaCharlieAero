# Lima Charlie Aero Website

Version-controlled source repository for the Lima Charlie Aero website.

## Repository purpose

This repository is the authoritative source of truth for the public Lima Charlie Aero website: site source, content, assets, build tooling, validation tooling, SEO controls, accessibility checks, release manifests, and deployable release artifacts where appropriate.

The repository is intended to make every website release reproducible from a specific Git commit or tag.

## Repository scope

Appropriate contents include:

- Website source code and templates
- Public images and static assets
- Public marketing copy
- SEO metadata and structured-data definitions
- Accessibility and static-site validation tooling
- Build scripts and deployment packaging
- Release manifests and checksums
- Test fixtures that contain no customer or credential data
- Design and implementation documentation
- GitHub Actions used to validate or package the site

## Do not commit

Do not store:

- Customer records, work orders, invoices, logbooks, or BUDS reports
- Personal identifying information that is not intentionally public
- Passwords, API tokens, private keys, Cloudflare secrets, or .env files containing secrets
- Proprietary third-party material without redistribution rights
- Litigation, medical, banking, or unrelated private records

Use environment variables or GitHub encrypted secrets for deployment credentials.

## Branch policy

- `main` = production-approved website source only.
- Substantial work is performed on named development branches.
- Codex or another implementation agent makes code changes on development branches.
- Implementation must complete its closed-loop verification cycle before review.
- ChatGPT or another independent reviewer may perform design, SEO, accessibility, and human-factors review.
- Changes merge to `main` only after review and acceptance.

Expected flow:

```text
main
  -> development branch
  -> implementation
  -> closed-loop QA
  -> pull request
  -> independent design/SEO/accessibility review
  -> corrections if required
  -> merge to main
  -> tag/release
  -> deployment
```

## Current live baseline

The live website baseline originally supplied for controlled import was:

- Baseline ID: `live-v100.2.5F`
- Artifact: `LCA_SOURCE_OF_TRUTH_BASELINE_v100_2_5F_DEPLOYABLE(1).zip`
- SHA-256: `e160c234b86aac2076db101c1b2e1acd27c46ed010866fd1aa6b21ff8214710a`
- Files in archive: `214`
- Uncompressed bytes: `14,184,009`

Historical ZIP artifacts are release evidence, not working copies. Git commits, branches, tags, and releases should identify the controlled working state going forward.

## Change-control rule

Do not perform a major redesign directly on `main`.

A release should be traceable to:

```text
issue / requirement
       ↓
development branch
       ↓
commits
       ↓
automated validation
       ↓
pull request
       ↓
review
       ↓
merge
       ↓
version tag
       ↓
release artifact
```

## Long-term objective

Eliminate ambiguous local folders and ZIP-based working copies. A commit SHA should uniquely identify the source being reviewed, tested, packaged, or deployed.

## Agent entrypoints and license

Before making changes, read [AGENTS.md](AGENTS.md), [the multi-LLM workflow](docs/MULTI_LLM_WORKFLOW.md) and the assigned issue. Use an owned task branch, record the full source commit and validate the actual repository state before handoff.

License: not yet selected by this governance bootstrap. Preserve existing copyright and any existing license or UNLICENSED declarations; public visibility is not an open-source license.
