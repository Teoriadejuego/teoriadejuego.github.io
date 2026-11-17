# Portfolio contracts

These contracts adapt the supplied teaching-platform plan to the existing public portfolio. They do not introduce a private application, participant data, authentication, polling, Qualtrics acquisition or a new scientific classification.

## Ownership and invariants

- The coordinator owns `build.py`, build/release support, shared HTML, CI and integration.
- The content-contract owner writes `tools/content_contract.py` and its unit tests.
- The interaction/methods owner writes `assets/app.js` and independent browser tests.
- The design/documentation owner writes the table styles and operator documentation after the plan is recorded.
- Only the coordinator builds or promotes the shared `public/` directory during parallel implementation. Tests that generate fixtures use temporary directories.
- Spanish and English remain first-class routes. Existing URLs, verified professional claims, scientific sources and individual contributions remain intact.
- The laboratory remains synthetic: independent groups, equal group sizes, equal SD, normal approximation; SE = sqrt(2 SD² / n), interval = delta ± 1.96 SE. It is not a power calculation or a causal estimate.

## Editorial inputs

`tools.content_contract` exposes `ContentError(ValueError)`, `load_content(root: Path) -> dict`, `validate_content(content: dict) -> None` and `validate_site_url(value: str) -> str`. Loading and validation perform no writes or network requests.

The content dictionary has keys `site`, `projects`, `publications`, `software`, `working-papers` and `resources`. The five existing datasets retain their formats. Validation rejects duplicate identifiers, unsafe slugs, unexpected fields, invalid types, missing translations, broken local references, invalid author order and unsafe URL schemes/credentials. Errors identify a file/record/field without echoing sensitive values.

`data/site.json` is an object with exactly:

- `schema_version`: integer `1`;
- `updated`: valid ISO calendar date;
- `home_projects`: nonempty list of distinct project IDs;
- `home_publications`: nonempty list of distinct publication IDs.

Counts are derived from the datasets. Historical article/capture dates remain separate from the site update date. Production `SITE_URL` must be a safe absolute HTTPS base without credentials, query or fragment. Local preview uses `TEST_BASE_URL` and does not change canonical identity.

## Browser interaction

Publication query parameters `q`, `topic` and `year` describe the actual selected controls. Unknown topic/year values are removed on initial load and history navigation. Unrelated query parameters and the fragment are preserved. Valid state survives the language switch. Without JavaScript all publications remain readable.

The lab exposes a native, keyboard-accessible details/table in both languages. Table cells use IDs `lab-n`, `lab-delta`, `lab-sd`, `lab-se`, `lab-lower`, `lab-upper`. They are updated alongside the existing graph and textual interval, without adding a second live announcement region. Bounds use the same display precision as the existing interval; SE is displayed to two decimal places. No scientific rule changes.

The site stores filter and synthetic lab settings in the URL. It does not persist them in cookies, localStorage or a remote service. Links to other sites may have their own policies; loading the portfolio itself must not call them.

## Build and publication

The build validates inputs before writing. It renders into a new temporary directory beneath the repository, using an explicit asset allowlist and UTF-8/LF text. It verifies the candidate before replacing generated `public/`. A validation/render failure preserves the previous output; a promotion failure attempts restoration and reports a retained recovery path if restoration cannot complete. This is not a claim of a cross-platform atomic directory exchange.

The generated inventory consists only of bilingual pages, `404.html`, approved assets, BibTeX downloads, `sitemap.xml`, `robots.txt`, `.nojekyll` and `release.json`. Source data, review logs, private documents, caches and development files are not public outputs. Unknown files, symlinks and path escapes are rejected by verification. Pattern scanning supplements the allowlist; it does not prove that arbitrary text contains no confidential information.

`release.json` uses schema version `1` and contains `site_url`, `updated`, `content_digest`, `source_revision` and `files`. `files` is sorted by relative POSIX path; each record has `path`, `bytes`, `sha256`. The manifest excludes itself and the deployment-only `.nojekyll` sentinel from its inventory; the empty sentinel is still checked in the local artifact. GitHub Pages does not serve that sentinel as a public resource. `content_digest` is SHA-256 of the canonical UTF-8 JSON inventory (sorted keys, compact separators). `source_revision` is an optional 40-character Git SHA, otherwise null (including an uncommitted source tree). No runtime clock or user information is included. The same rendered content has the same digest even when the source revision changes.

The manifest is a consistency record, not a cryptographic signature or a protection against a compromised host. Visitors do not poll it or depend on it for rendering. Deployment checks compare the served manifest and bytes with the validated candidate.

## Acceptance and limits

Unit tests cover rejected editorial inputs, deterministic builds, stale-file exclusion, tampering and recovery. Browser tests independently check statistical values against Python calculations, accessible/textual equivalence, public-only network requests, controls, keyboard, language and responsive layouts. CI runs validation before any Pages deployment; PR checks cannot deploy.

No interviews, representative user study, accessibility certification, search ranking guarantee, load-capacity guarantee or perpetual availability of external repositories is claimed. Performance measurements identify their local test conditions. Documentation describes how to edit, validate, deploy and recover using the existing hosting account.
