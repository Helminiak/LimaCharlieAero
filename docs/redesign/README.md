# LCA v103 redesign: owner preview workstream

Branch: `redesign/v103-owner-preview`, created from frozen RC3 `1521869e0bc1e7136459404d2f16232bb69d045a`.
`main` (`6d9f82c`), the rollback reference `3d48ea6` and the RC3 freeze are untouched. PR #2's history is not modified.
**No merge, deployment, DNS change, Formspree submission or public publication is authorized.** Terminal state for this branch: **PREVIEW READY — USER REVIEW REQUIRED**.

## Roles and models (as actually run)

| Role | Agent | Model / effort, as verified |
|---|---|---|
| Design lead, independent design reviewer | Claude Code | `claude-opus-5-5` (Opus 5.5). The reasoning effort is set by the Claude Code harness for this session; the agent cannot read back the exact level, so this is reported as **not self-verifiable**, not claimed as "high" or "xhigh". Fable 5.2 challenger: **not used**. |
| Engineering lead, implementer, independent engineering reviewer | Codex CLI 0.170.0 (exec) | `gpt-6.2-astra`, `model_reasoning_effort=high` (CLI header and session `turn_context`). Final review is run at `xhigh`. |
| Supporting models | none used so far | — |

Codex sandbox: `workspace-write` with `sandbox_workspace_write.network_access=true`. This is needed for loopback binding by Wrangler/Chromium (the Phase 1 audit was BLOCKED without it). There is no approval bypass and no `danger-full-access`.

## Documents

| # | File | Owner |
|---|---|---|
| 1 | `01-BASELINE-AUDIT-CLAUDE.md`: production vs RC3 scored audit, privacy table, reconciliation | Claude |
| 1b | `CODEX_PHASE1_AUDIT.md`: independent engineering audit (written without reading Claude's) | Codex |
| 2 | `02-DESIGN-DIRECTIONS.md`: Direction A vs B, scoring, recommendation (B plus A evidence components) | Claude |
| 3 | `03-DESIGN-SPEC.md`: tokens, components, IA, page compositions, case register, regulatory register, acceptance | Claude |
| 4 | `CODEX_FEASIBILITY.md`: Codex's assessment of the spec | Codex |
| 5 | `IMPLEMENTATION_LOG.md`, `DEFECT_REGISTER.md`, test evidence | Codex |
| 6 | `REVIEW_CLAUDE.md` / `REVIEW_CODEX.md` / `REVIEW_RESOLUTION.md` | both |

Prototypes: `prototype/a/index.html` and `prototype/b/index.html` are static concept pages. They reference images at `../img/<key>-<w>.webp`, derived from the rollback tree's `assets/images` (mapping in `prototype/IMAGES.md`). The image binaries are not committed, to avoid duplicating the asset pool.
Screenshots: `evidence/redesign/baseline/` (production 2026-11-20 and RC3 at 390/1440) and `evidence/redesign/directions/`.

## Evidence-status vocabulary
VERIFIED, PARTIAL, FAILED, UNTESTED, BLOCKED: as defined in the operator feedback policy referenced by `main:AGENTS.md`.
