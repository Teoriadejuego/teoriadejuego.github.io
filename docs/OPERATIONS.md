# Portfolio maintenance and release guide

This guide covers the Spanish/English portfolio at https://teoriadejuego.github.io. It uses a standard-library Python build and static GitHub Pages hosting. There is no private web application, participant database, login, background polling or visitor analytics service.

The implementation contract is [CONTRACTS.md](CONTRACTS.md). The [adapted plan](ADAPTED_PLAN.md) records acceptance criteria and their evidence-backed assessment; it is not a claim of 400 independent tests. Record actual command and deployment results when applying this guide to a new release.

## Edit public content

Work from the repository root. Keep personal certificates, administrative documents, credentials and source microdata outside this repository. A fact verified against a private document may be rewritten as an appropriate public professional statement; the document itself must not be published.

| Source | Purpose |
| --- | --- |
| `data/publications.json` | Published articles, complete author metadata, DOI and open-access destinations |
| `data/working-papers.json` | Working papers/preprints, kept distinct from reviewed articles |
| `data/projects.json` | Case studies, individual contribution, evidence and project status |
| `data/software.json` | Additional software and explanatory repositories |
| `data/resources.json` | Institutional teaching/research materials |
| `data/site.json` | Editorial date and selected homepage IDs |
| `SOURCES.md` | Provenance, version decisions and limits of external verification |
| `build.py`, `assets/` | Shared presentation and progressive enhancement |

Keep the established Spanish and English versions, existing routes and genuine contact details. Translate interface copy and professional descriptions; keep scientific titles in their original language. Do not infer commercial clients, business outcomes or individual technical contributions from a team's results.

The current delivery contains 12 articles, 2 working papers and 6 case studies across 26 content routes, plus a 404 page. Counts come from the datasets. Future additions should update the corpus and its explicit regression expectations together, rather than adding fake entries to satisfy a counter.

`data/site.json` has exactly four fields:

- `schema_version`: integer `1`.
- `updated`: a valid ISO calendar date such as `2026-11-18`.
- `home_projects`: a nonempty list of distinct IDs from the project catalogue.
- `home_publications`: a nonempty list of distinct IDs from the article catalogue.

Set `updated` when making an editorial update. Rebuilding alone must not advance this date. Article years, online publication dates and screenshot dates retain their separate meanings. A new homepage selection must refer to existing records; it must not alter scientific metadata to make a work appear newer.

## Validate and build

Use Python 3.12, matching CI. CI selects Ubuntu 24.04 explicitly to avoid changes in the operating-system family behind `ubuntu-latest`; hosted images still receive updates. Browser dependency installation has a five-minute limit, with a twenty-minute validation-job limit. These bounds expose infrastructure failures without bypassing tests. See the [runner image migration guidance](https://github.com/actions/runner-images#latest-migration-process) and [Playwright CI instructions](https://playwright.dev/python/docs/ci). The production build has no third-party runtime dependencies. Browser QA has development dependencies:

```sh
python -m pip install -r requirements-dev.txt
python -m playwright install chromium firefox
```

The development requirements pin Playwright and greenlet. For a host that already has a compatible Chromium executable, the existing browser scripts accept `PLAYWRIGHT_CHROMIUM_EXECUTABLE`; avoid assuming that a developer's absolute Windows path exists elsewhere. CI installs its own browsers.

The editorial validator is `tools.content_contract`. Its public interfaces are `ContentError`, `load_content(root)`, `validate_content(content)` and `validate_site_url(value)`. Loading/validation performs no writes or network calls. It rejects unknown fields, unsafe IDs or URL schemes, credentials in URLs, missing translations, invalid types, duplicate IDs, broken references and inconsistent author order. Treat a failure as a request to correct the source, not permission to bypass validation.

Run the local gates from the repository root:

```sh
python -m unittest discover -s tests -p "test_*.py"
python build.py
python tests/check_static.py
python tools/release.py verify
```

`SITE_URL` defines production canonical identity and defaults to `https://teoriadejuego.github.io`. It must be an absolute HTTPS base without credentials, query or fragment. Do not change it to localhost for preview: use the preview URL or `TEST_BASE_URL` for browser tests instead.

The build validates inputs before writing. It renders into a fresh temporary directory under the repository, writes UTF-8/LF text and copies only approved assets. Candidate verification precedes promotion to `public/`. This removes stale generated files from a successful replacement rather than carrying them into a new release.

A validation or render failure preserves the previous output. If promotion fails, recovery attempts to restore it; a failure to restore must report a retained recovery path. Do not delete that path until its contents have been inspected and recovery is complete. This process is not a guarantee of a universally atomic directory exchange.

Only one coordinated process should build or promote the shared `public/` directory at a time. Tests that exercise failed builds use isolated temporary fixtures. Do not edit generated files to repair a source error: the next build replaces them.

## Inspect the public experience

To browse a local build:

```sh
python tools/preview.py --port 8078
```

Open `http://localhost:8078/` or `/en/`. This is a preview server, not production hosting. Its MIME or cache behaviour may differ from GitHub Pages; confirm important resource headers against the deployed site.

The coordinated checks manage their own ephemeral servers:

```sh
python tools/fetch_axe.py
python tools/check_browser.py --firefox
python tools/measure.py
```

`fetch_axe.py` obtains the pinned, integrity-checked axe asset in `qa/axe.min.js`; it is development tooling, not a script loaded by visitors. `check_browser.py` runs the Chromium suites and, with `--firefox`, the additional methods/privacy checks in Firefox. `measure.py` records local measurements as JSON under `qa/`. Record the browser, environment and network conditions when comparing results; localhost timings do not establish hosting capacity or a universal performance score.

The established focused scripts remain available when a preview server is running:

```sh
python tests/browser_check.py
python tests/round2_check.py
python tests/round3_check.py
```

They accept `TEST_BASE_URL` for the preview address; optional `AXE_SCRIPT` points to a local axe file. Do not run every historical suite after every small CSS edit. Run the checks relevant to the change, then the integrated release gates. A passing automated accessibility scan is useful evidence, not WCAG certification. Inspect keyboard behaviour, focus, zoom and representative screenshots as well.

## Understand the laboratory

The example uses synthetic inputs only. `n` is observations **per group**, with two independent groups of the same size and equal standard deviation. The calculation uses a normal approximation:

```text
SE = sqrt(2 × SD² / n)
lower = delta − 1.96 × SE
upper = delta + 1.96 × SE
```

The initial state is `n = 200`, `delta = 3`, `SD = 15`. The supported ranges are n 20–2000 in steps of 20, delta −15–15 in steps of 0.5 and SD 5–40 in steps of 1. The independent method tests must accompany any future scientific change.

The graph, textual interval and expandable table show the same computation. The table lists n, delta, SD, SE and both limits; SE has two decimal places, while limits follow the existing adaptive precision near zero. The table is not another live announcement region.

The approximate 95% interval describes the repeated-sampling coverage of this procedure under its assumptions. It is not a probability assigned to this particular fixed parameter. The demonstration does not generate real observations, estimate power, establish causality, account for selection bias or calculate business value. A wholly positive or negative interval is not by itself a decision rule for a consultancy project.

Publication filters and laboratory settings are stored in the URL. They are not stored by the application in cookies, localStorage or a remote database. Shared URLs and browser history can retain these settings, so do not enter confidential text into a public search URL. Valid settings survive language changes. Unknown topic/year values are removed, while unrelated parameters and fragments are preserved. Without JavaScript, the publication catalogue and source links remain readable; the interactive laboratory explains its JavaScript requirement.

## Inspect a release

`public/release.json` uses schema version `1`:

- `site_url` and `updated` identify the canonical site and editorial date.
- `source_revision` is the 40-character Git revision for an attributable clean source tree, otherwise `null`, including a tree with uncommitted source changes.
- `files` contains relative POSIX paths sorted by path, each with byte length and SHA-256.
- `content_digest` is SHA-256 of the canonical UTF-8 JSON inventory with sorted keys and compact separators.

The inventory excludes `release.json` itself and the deployment-only `.nojekyll` sentinel. The sentinel must exist and be empty in the local artifact, but GitHub Pages does not serve it as a public resource; do not require an HTTP download of it.

The same rendered files have the same digest even if the source revision differs. No build clock, visitor identifier or telemetry is included. The manifest is a consistency record, **not a cryptographic signature** and not protection against a compromised host. Visitors do not fetch it to render pages or poll it for updates.

Verification rejects missing/extra files, tampering, symlinks and path escapes. The distribution is restricted to approved bilingual HTML, 404, assets, BibTeX downloads, sitemap, robots, sentinel and manifest. Source data, tests, docs, reviews, caches and private documents are not public output. Pattern scanning supplements the allowlist; it does not prove that arbitrary prose contains no confidential information.

## Deploy and confirm

Inspect the diff and working tree, run the release gates, and commit the reviewed source changes. Building from a clean committed tree allows `source_revision` to identify the release. Push the intended commit to `main` using the existing GitHub account; the Pages workflow builds and checks before deployment. A pull-request check must not deploy. The workflow also supports its configured manual dispatch.

The `validate` job checks the candidate before uploading only `public/`. The `deploy` job requires successful validation and is restricted to `main` outside pull requests. Workflow concurrency serialises runs for the same ref. The final `confirm` job rebuilds the expected output from the same clean commit, then compares its manifest, revision and all served bytes with production. It allows six bounded attempts separated by ten seconds for propagation. A failed confirmation means a deployment was attempted but the served result was not verified; it does not automatically roll back the host. Review the diagnostic and follow the recovery procedure below.

```sh
git status --short
git diff --check
git log -1 --oneline
git push origin main
```

Run the push only when the intended source commit has been reviewed and selected; an uncommitted preview is not a deployed release. Check the actual Actions/Pages result rather than waiting an arbitrary number of minutes. No domain or DNS change is part of this workflow.

After deployment, compare the served manifest and bytes with the validated candidate:

```sh
python tools/release.py verify-remote --url https://teoriadejuego.github.io
```

When confirming a specific clean commit, add `--expected-revision` followed by its full 40-character SHA. A local build, uploaded artifact, successful deployment and verified served bytes are different states. Report the state actually observed; an HTTP failure or revision mismatch is not proof of successful publication. A browser may retain an older cached page until navigation/reload; the portfolio does not replace an active page automatically.

## Restore a known version

For a source regression, identify the introducing commit with `git log` and inspect it with `git show`. Start with a clean working tree; preserve unrelated edits before proceeding. Create a new commit that reverts the identified change:

```sh
git log --oneline
git show FULL_BAD_COMMIT_SHA
git revert FULL_BAD_COMMIT_SHA
```

Replace the placeholder with the actual inspected commit. Resolve any conflicts deliberately. For a merge commit or several dependent changes, review the correct parent/dependency order before reverting; do not blindly copy an unsuitable command. Do not use `reset --hard` or force-push as the normal recovery path.

Rerun validation, build, release verification and the relevant regression tests. Push the corrective commit to `main`, inspect CI and verify the served result against the corrective revision. This preserves history and creates a new traceable release. Local promotion recovery is separate: if the build reports a retained backup because restoration failed, stop competing writers and follow the reported path before retrying.

## Diagnose failures safely

| Symptom | Next step |
| --- | --- |
| Invalid field/type/translation or duplicate ID | Correct the named source record; rerun validation. Do not add filler to silence the check. |
| Broken local reference | Check selected IDs and catalogue references against existing records. |
| Unsafe URL or canonical base | Correct scheme, host/path and remove embedded credentials; never paste a secret-bearing rejected value into an issue. |
| Candidate render failed | Fix the reported source/template error; confirm previous output remains usable before rebuilding. |
| Unexpected file, symlink, path escape or hash mismatch | Inspect provenance; rebuild from approved sources and verify again. Do not hand-edit manifest hashes to accept unknown files. |
| Promotion/restoration failed | Stop other writers and file locks, inspect the retained recovery path and recover before retrying. |
| `source_revision` is null | Check for uncommitted/unattributable sources; commit reviewed changes and build clean when commit attribution is required. |
| Browser tool unavailable | Install the declared development dependency/browser, or configure a compatible local executable; do not mark the browser check passed. |
| Served revision/digest differs | Check Actions status and the intended commit; recheck served files before claiming success. |
| External article/PDF unavailable | Preserve DOI/institutional record and record the dated limitation; confirm the destination without mass retries. |

Share file/record/field, error category, command, revision and relevant sanitized output. Do not attach private documents, tokens, sensitive rejected values or personal experimental records. Keep QA artifacts outside the public distribution.

## Maintain open sources and evidence

Link article downloads to the institutional repository or publisher that hosts the identified version. Keep record pages and DOI fallbacks when a direct PDF is unavailable; do not present a record-only link as a guaranteed download. Distinguish published version, accepted manuscript and preprint. Do not mirror publisher PDFs or participant datasets into this portfolio.

External availability changes, and automated clients can receive anti-bot pages. Record what was checked, when and with what limitation. A past successful check is not perpetual availability. Search metadata, canonicals, hreflang and sitemap support discovery but cannot guarantee Google indexing or ranking.

For each release, retain a concise account of changed files, tests actually run, observed results, served revision/digest and unresolved limits. Shared evidence may support multiple plan criteria. Do not turn 400 criteria into 400 claimed changes or mark unexecuted checks as passed.
