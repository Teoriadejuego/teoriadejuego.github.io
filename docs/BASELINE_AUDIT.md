# Baseline audit — 18 November 2026

Baseline source: `32d65dbc3fac3c071c514db06d6ec7b8a0b2dde5`. This is an inspection of the implemented portfolio, not a user study or a report of a current data leak.

## Existing strengths to preserve

- 26 bilingual pages and a useful 404; 12 articles, two working papers, six cases, six software records and 14 institutional materials.
- Public content is available as static HTML without JavaScript. Responsive navigation, keyboard focus, reduced motion and forced colours already have regression coverage.
- Hiring routes lead to project-specific evidence. Individual contributions are distinguished from team outcomes, and synthetic demonstrations are labelled.
- Bibliographies preserve publisher author order and compound family names. DOI and institutional links are retained, including the stated access limitations.
- Seven independently calculated laboratory scenarios matched the existing values and geometry. No numerical defect was observed. Controls made no network requests in the observed public run.
- Prior local checks covered the 26 routes, three main viewport widths, additional narrow widths, 200% text, filters, language state, clipboard success/failure with a stub, no-JS and seven axe routes.

## Reproduced gaps

| Area | Evidence at baseline | Required response |
| --- | --- | --- |
| Build isolation | The generator reuses `public/` and copies all of `assets/` with `dirs_exist_ok=True`. | Generate a clean candidate and reject unexpected files before promotion. |
| Failure recovery | Files are overwritten as rendering progresses. | Preserve the last valid generated output when input validation, rendering or candidate checks fail; restore on promotion failure. |
| Editorial contracts | JSON is loaded directly; duplicate IDs can be overwritten in dictionaries. | Validate types, fields, identifiers, references and translations before writing anything. |
| Link safety | HTML escaping exists but input URL schemes and `SITE_URL` are not constrained. | Reject unsafe schemes, credentials and malformed bases with sanitised errors. |
| Reproducible bytes | Windows checkout uses CRLF and text writers do not explicitly choose LF. | Normalise textual output and hash the actual published bytes. |
| Release identity | No machine-readable file inventory or content digest exists. | Publish a deterministic consistency manifest, with an optional clean-source Git revision. |
| Internal links | The static checker skips absolute links even when they address this site. | Resolve same-origin paths and verify root confinement, pages and anchors. |
| Invalid filters | `?topic=invalid&year=1900` shows empty controls and all articles while preserving invalid URL values. | Normalise supported query values on initial load and history navigation. |
| Method regression | Existing checks sample behaviour but do not jointly compare numerical values, chart geometry and accessible text against an independent oracle. | Add an independent Python-based browser check with documented synthetic cases. |
| Deployment checks | The workflow builds and runs static checks only. | Require unit, browser, method and artifact checks before deployment; PRs cannot deploy. |
| Operator guidance | Existing README explains basic editing and deployment, but not version verification and recovery. | Document the actual contracts, editing workflow, diagnostics and recovery in English. |

## Boundaries

The source plan's Qualtrics acquisition, participant records, historical class groups, scientific classifications, suppression threshold, private sessions, cooldown and student polling do not exist in this portfolio. Adding them would create a different product. Their relevant intent is transferred to editorial integrity, public-only outputs, deterministic builds, coherent publication and accessible evidence.

Performance checks will report local conditions and byte budgets. They cannot establish GitHub Pages capacity, field Core Web Vitals or the experience of representative recruiters. Automated accessibility checks supplement keyboard and visual review; they do not certify accessibility. External repositories may reject automated access or change independently of this site.
