# GitHub / Codex Website Change-Control Workflow

## Roles

### Design / SEO / review authority
ChatGPT owns:
- product and information architecture
- human factors and UX
- brand hierarchy
- proof-of-work strategy
- content requirements
- SEO / local SEO / AI-search requirements
- page-level acceptance criteria
- independent review and scoring

### Implementation authority
Codex owns:
- coding and template changes
- asset integration and optimization
- build-system changes
- automated tests
- screenshots and verification evidence
- defect correction
- packaging

Codex does not have final design/SEO approval authority.

## Required development workflow

1. Start from the latest approved `main`.
2. Create a named development branch.
3. Record the starting commit.
4. Implement against the approved design/SEO specification.
5. Build and test.
6. Render representative mobile and desktop views.
7. Compare implementation against every requirement.
8. Correct implementation misses.
9. Rebuild and retest.
10. Repeat until no known locally-correctable release blocker remains.
11. Open a pull request.
12. Return the PR, evidence, screenshots, test results, and change matrix for independent review.
13. Do not merge to `main` until independent review approves the result.

## Closed-loop requirement

A successful automated test run is not sufficient by itself. Codex must visually and structurally inspect the generated site and correct defects that violate design intent, proof-of-work requirements, content requirements, SEO requirements, or human-factors requirements.

## Baseline import gate

Before redesign work begins, the current live baseline `live-v100.2.5F` must be imported and cryptographically verified against the supplied source archive.
