# AGENTS.md

## Purpose

Public static website source, genuine public assets, SEO/accessibility validation and reproducible release packages.

## Repository Boundary

Belongs here: Site source, templates, assets with publication rights, validation tools and release manifests.

Does not belong here: Customer records, invoices, private BUDS/logbooks, personal documents, credentials and unauthorized third-party assets.

## Source of Truth

The Git state and assigned issue/PR are authoritative engineering state. Read README.md, this file, docs/MULTI_LLM_WORKFLOW.md and the assigned issue. ZIP/folder names such as FINAL, FIXED or NEW are not versions. Current user instructions and security constraints take precedence over repository prose.

## Repository-specific controls

main is production-approved source. Preserve PR #2 and rc3-proof-of-work-seo; no redesign, deployment, DNS change or production merge is included. Preserve factual proof-of-work, substantial technical content, page-specific SEO and accessibility. Do not fabricate business claims or use stock/AI imagery as maintenance evidence. RC3 requirements remain in docs/RC3_CODEX_MASTER_IMPLEMENTATION_PROMPT.md on that branch; resolve guidance/template conflicts deliberately before integrating both PRs.

## Required Workflow

1. Fetch/pull safely before beginning; inspect branch, HEAD, remotes and working-tree status. Do not overwrite uncommitted work.
2. Read the entrypoints and issue acceptance criteria; state your implementer/reviewer/QA/research/integration role.
3. Inspect open issues/PRs and overlapping file changes; coordinate conflicts on the issue.
4. Create a dedicated branch from an agreed current base. One branch has one editing owner.
5. Make narrowly scoped changes, run relevant tests and document failures/skips.
6. Commit with an informative message, open/update a PR and record test evidence and risks.
7. Hand off using repository, branch, full SHA, issue, PR and next action; verify the actual state on receipt.

## Branching and Multi-Agent Rule

Authoritative/default branch: `main`. Do not commit substantive work directly to it. Use `agent/<agent-name>/<issue-number>-<short-description>`; bootstrap governance uses `repo-bootstrap/multi-llm-governance`. Never let multiple agents concurrently edit one branch or silently overwrite another's unmerged work. GitHub Issues/PRs coordinate ownership. Merge, release and deployment are separate authorized actions.

## Testing

On main, baselines/live-v100.2.5F/verification/verify.py requires the exact recorded legacy archive and writes verification evidence. On rc3-proof-of-work-seo, use npm ci, npm run build, npm test and npm run package with the branch's Python/Playwright dependencies. Do not report those RC3 checks as run on main.

For documentation/governance, check diff whitespace, parse YAML, validate metadata against actual visibility/default branch, and verify ignore rules for secrets, weights and explicitly allowed fixtures. A syntax or governance check is not application/hardware acceptance.

## Security

Never commit credentials, tokens, keys, customer records or private personal evidence. Sanitize fixtures/logs. Review history as well as the current tree before public exposure; .gitignore does not sanitize tracked history. See SECURITY.md. Investigate >25 MiB objects; keep bulk data/weights external and record manifests/checksums. Preserve the public exporter/private entry-engine boundary.

## Generated Files

Do not hand-edit generated releases, build outputs, caches or benchmark reports to manufacture a pass. Change the generator/source and regenerate under controlled versions. Label captured evidence with its source commit and environment; do not overwrite historical acceptance evidence during governance.

## Handoff

A PR description records objective, scope/files, exact tests and results, known limitations, agent/role, independent-review findings and next action. Follow docs/MULTI_LLM_WORKFLOW.md. License: not yet selected by this bootstrap; preserve any existing license/UNLICENSED declaration.
