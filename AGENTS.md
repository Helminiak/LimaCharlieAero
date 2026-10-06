# AGENTS.md — Lima Charlie Aero website

## Repository-wide Codex rules

- main is production-approved history. Never modify or merge main from an implementation task unless the user explicitly authorizes the merge after independent review.
- The active implementation branch is rc3-proof-of-work-seo.
- docs/RC3_CODEX_MASTER_IMPLEMENTATION_PROMPT.md is authoritative for the RC3 product, design, SEO, human-factors, content, proof, testing, and release requirements.
- Codex is the implementation engineer. Do not independently rebrand, simplify, shorten, or redesign away substantive requirements.
- Lima Charlie Aero is the primary business identity. Founder-specific language belongs only where the person is actually the subject.
- Never fabricate staff, reviews, customers, case histories, results, turnaround times, certifications, prices, authorizations, geographic coverage, or technical claims.
- Never use stock or AI-generated aviation maintenance imagery as proof of work.
- Real work evidence must be factual, permission-reviewed, and contextually placed.
- Do not reintroduce Tell Joe, Contact Joe, Call Joe, Text Joe, Meet Joe, Joe reviews, or owner-operated into deployed public copy.
- Keep the site static, lightweight, accessible, deterministic, and Cloudflare-compatible. Do not introduce a heavy framework or CMS.
- No Cloudflare deployment, DNS change, external paid-service change, customer contact, or production merge is authorized in RC3.
- Passing automated tests is not sufficient. Perform visual self-review, log defects, correct them, rebuild, and retest.
- Terminal status for RC3 is ENGINEERING CANDIDATE COMPLETE — DESIGN/SEO SIGN-OFF REQUIRED.

## Code review rules

### Product regressions
- Flag any change that removes substantive technical content, proof-of-work evidence, owner-facing context, or page-specific SEO semantics without an explicit requirement and documented reason.

### Brand truth
- Flag founder-centric default CTAs, invented staffing/capacity, fake testimonials/reviews, unsupported technical authority, or copy that implies services/coverage not supported by repository truth.

### Release integrity
- Flag any path that can deploy or merge to production without independent review, any build that exposes docs/baselines/source files in public output, or any verification result that is reported PASS without actually running the check.
