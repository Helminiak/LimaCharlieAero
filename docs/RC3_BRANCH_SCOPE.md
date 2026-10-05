# RC3 Branch Scope — Proof of Work, Warmth, SEO

Branch: `rc3-proof-of-work-seo`

Base: approved `main` baseline containing the verified live v100.2.5F website.

## Purpose

This branch is the controlled implementation branch for the next Lima Charlie Aero redesign cycle.

The design/SEO team owns product direction. Codex owns implementation.

## Non-negotiable rules

1. Do not redesign directly on `main`.
2. Do not remove, shorten, consolidate, or replace substantive technical content without explicit design/SEO direction.
3. Do not regress to founder-centric workflow language such as systemic "Tell Joe", "Call Joe", "Text Joe", or "Joe does everything".
4. Lima Charlie Aero remains the primary business identity. Founder credentials support authority but do not replace the company brand.
5. Proof of actual work is a primary design requirement.
6. Use only factual, supportable work evidence. Do not fabricate case studies, outcomes, testimonials, staff, certifications, turnaround times, or customer counts.
7. Preserve the current live baseline as the comparison point for content depth, proof imagery, technical authority, trust, and owner comprehension.
8. Preserve engineering advantages from the newer RC2 work where they improve performance, accessibility, maintainability, responsiveness, or owner usability.
9. Codex must perform a closed-loop implementation / review / correction / rebuild / retest cycle before requesting design/SEO review.
10. Codex does not have final design/SEO approval authority.

## Required Codex return evidence

At minimum:
- full changed-file inventory
- route-by-route change matrix
- before/after screenshots for key routes at mobile and desktop
- proof-of-work image placement matrix
- content retention/restoration matrix
- SEO metadata/internal-link/schema matrix
- accessibility results
- performance/Lighthouse results
- broken-link/reference results
- known external validation blockers
- exact commit SHA(s)
- final PR into `main`

## Merge gate

This branch must not be merged until:
1. Codex closed-loop QA is complete;
2. all locally correctable release blockers are resolved;
3. the design/SEO team independently reviews the implementation;
4. any required corrections are made and re-tested;
5. the final candidate is explicitly approved for merge.
