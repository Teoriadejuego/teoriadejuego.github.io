"""Deterministic public artifacts. No private documents or visitor data are inputs."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

ASSETS = (
    'app.js', 'favicon.svg', 'hero.webp', 'pbis-product.webp',
    'portrait-400.webp', 'portrait-800.webp', 'portrait.webp',
    'thumb-airplanes.webp',
    'thumb-arco.webp',
    'thumb-climate.webp',
    'thumb-cooperation.webp',
    'thumb-delay.webp',
    'thumb-networks.webp',
    'thumb-pbis.webp',
    'thumb-sonar.webp',
    'thumb-teenslab.webp',
    'thumb-voting.webp',
    'social-en.jpg', 'social-es.jpg', 'style.css',
)
TEXT_SUFFIXES = {'.html', '.css', '.js', '.svg', '.json', '.xml', '.txt', '.bib'}
MAIN_ROUTES = ('', 'for-teams/', 'projects/', 'publications/', 'profile/', 'lab/', 'privacy/')
MAX_PUBLIC_BYTES = 1_100_000
MAX_ASSET_BYTES = 550_000
SECRET = re.compile(r'github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|[A-Za-z]:[\\/]+Users[\\/]+', re.I)


class ReleaseError(ValueError):
    """A diagnostic safe to show in local or CI logs."""


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf8')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def decode_manifest(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ReleaseError('MANIFEST_JSON: duplicate object key')
            result[key] = value
        return result
    def nonfinite(_):
        raise ReleaseError('MANIFEST_JSON: non-finite number')
    try:
        return json.loads(raw, object_pairs_hook=unique, parse_constant=nonfinite)
    except (ValueError, UnicodeError) as error:
        raise ReleaseError('MANIFEST_JSON: invalid release metadata') from error


def linklike(path):
    return path.is_symlink() or getattr(path, 'is_junction', lambda: False)()


def expected_paths(content):
    routes = MAIN_ROUTES + tuple('projects/' + p['id'] + '/' for p in content['projects'])
    paths = {prefix + route + 'index.html' for prefix in ('', 'en/') for route in routes}
    paths.update('assets/' + name for name in ASSETS)
    paths.update('downloads/' + p['id'] + '.bib' for p in content['publications'])
    paths.update({'downloads/publications.bib', '404.html', 'sitemap.xml', 'robots.txt', '.nojekyll', 'release.json'})
    return paths


def copy_assets(root, output):
    source = root / 'assets'
    if linklike(source) or source.resolve().parent != root.resolve():
        raise ReleaseError('ASSET_PATH: source assets must be an ordinary repository directory')
    if {p.name for p in source.iterdir()} != set(ASSETS):
        raise ReleaseError('ASSET_INVENTORY: update the reviewed asset allowlist before adding or removing assets')
    target = output / 'assets'
    target.mkdir()
    for name in ASSETS:
        path = source / name
        if linklike(path) or not path.is_file():
            raise ReleaseError('ASSET_PATH: only ordinary approved files can be copied')
        if path.suffix in TEXT_SUFFIXES:
            (target / name).write_text(path.read_text(encoding='utf8'), encoding='utf8', newline='\n')
        else:
            shutil.copyfile(path, target / name)


def inspect_tree(output, content, include_manifest=True):
    if linklike(output) or not output.is_dir():
        raise ReleaseError('ARTIFACT_ROOT: expected an ordinary output directory')
    expected = expected_paths(content)
    if not include_manifest:
        expected.remove('release.json')
    files = {}
    base = output.resolve()
    for path in output.rglob('*'):
        if linklike(path) or not path.resolve().is_relative_to(base):
            raise ReleaseError('ARTIFACT_PATH: links and escapes are not allowed')
        if path.is_file():
            name = path.relative_to(output).as_posix()
            if name not in expected:
                raise ReleaseError('ARTIFACT_EXTRA: unexpected file in public output')
            files[name] = path.read_bytes()
    if set(files) != expected:
        raise ReleaseError('ARTIFACT_MISSING: expected public files are missing')
    if files['.nojekyll'] != b'':
        raise ReleaseError('ARTIFACT_CONTROL: deployment sentinel must be empty')
    if sum(map(len, files.values())) > MAX_PUBLIC_BYTES:
        raise ReleaseError('BUDGET_PUBLIC: public artifact exceeds its reviewed byte budget')
    if sum(len(data) for name, data in files.items() if name.startswith('assets/')) > MAX_ASSET_BYTES:
        raise ReleaseError('BUDGET_ASSETS: assets exceed their reviewed byte budget')
    for name, data in files.items():
        if Path(name).suffix in TEXT_SUFFIXES:
            try:
                text = data.decode('utf8')
            except UnicodeDecodeError as error:
                raise ReleaseError('TEXT_ENCODING: public text must be UTF-8') from error
            if '\r' in text:
                raise ReleaseError('TEXT_NEWLINES: public text must use LF')
            if SECRET.search(text):
                raise ReleaseError('PUBLIC_CONTENT: a credential-like value or local owner path was detected')
    return files


def inventory(files):
    return [{'path': name, 'bytes': len(data), 'sha256': digest(data)}
            for name, data in sorted(files.items()) if name not in {'release.json', '.nojekyll'}]


def create_manifest(output, content, site_url, source_revision=None):
    from tools.content_contract import validate_site_url
    files = inspect_tree(output, content, include_manifest=False)
    entries = inventory(files)
    manifest = {'schema_version': 1, 'site_url': validate_site_url(site_url),
                'updated': content['site']['updated'], 'content_digest': digest(canonical(entries)),
                'source_revision': source_revision, 'files': entries}
    (output / 'release.json').write_text(json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + '\n', encoding='utf8', newline='\n')
    verify_release(output, content, site_url)
    return manifest


def verify_release(output, content, site_url=None):
    from tools.content_contract import validate_site_url
    files = inspect_tree(output, content)
    manifest = decode_manifest(files['release.json'])
    fields = {'schema_version', 'site_url', 'updated', 'content_digest', 'source_revision', 'files'}
    if not isinstance(manifest, dict) or set(manifest) != fields:
        raise ReleaseError('MANIFEST_SCHEMA: unexpected release fields')
    if type(manifest['schema_version']) is not int or manifest['schema_version'] != 1:
        raise ReleaseError('MANIFEST_VERSION: unsupported release schema')
    try:
        base = validate_site_url(manifest['site_url'])
    except ValueError as error:
        raise ReleaseError('MANIFEST_URL: invalid site identity') from error
    if site_url is not None and base != site_url:
        raise ReleaseError('MANIFEST_URL: site identity differs from the candidate')
    if manifest['updated'] != content['site']['updated']:
        raise ReleaseError('MANIFEST_DATE: editorial date differs from the source')
    revision = manifest['source_revision']
    if revision is not None and (not isinstance(revision, str) or not re.fullmatch('[0-9a-f]{40}', revision)):
        raise ReleaseError('MANIFEST_REVISION: invalid source revision')
    if not isinstance(manifest['content_digest'], str) or not re.fullmatch('[0-9a-f]{64}', manifest['content_digest']):
        raise ReleaseError('MANIFEST_DIGEST: invalid digest')
    if not isinstance(manifest['files'], list):
        raise ReleaseError('MANIFEST_INVENTORY: expected an ordered list')
    for entry in manifest['files']:
        if (not isinstance(entry, dict) or set(entry) != {'path', 'bytes', 'sha256'} or
                not isinstance(entry['path'], str) or type(entry['bytes']) is not int or entry['bytes'] < 0 or
                not isinstance(entry['sha256'], str) or not re.fullmatch('[0-9a-f]{64}', entry['sha256'])):
            raise ReleaseError('MANIFEST_INVENTORY: invalid file record')
    entries = inventory(files)
    if manifest['files'] != entries or manifest['content_digest'] != digest(canonical(entries)):
        raise ReleaseError('MANIFEST_MISMATCH: inventory, bytes or digest differ')
    return manifest


def current_revision(root):
    """Do not attribute uncommitted source content to a clean commit."""
    try:
        dirty = subprocess.check_output(['git', 'status', '--porcelain'], cwd=root, text=True, stderr=subprocess.DEVNULL)
        revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    return revision if not dirty.strip() and re.fullmatch('[0-9a-f]{40}', revision) else None


def _remove_owned_holder(root, holder):
    # Check the resolved absolute deletion target before any recursive cleanup.
    root = root.resolve()
    if linklike(holder) or holder.resolve().parent != root or not holder.name.startswith('.portfolio-previous-'):
        raise ReleaseError('CLEANUP_PATH: refused an unowned recovery directory')
    shutil.rmtree(holder)


def promote(root, candidate):
    """Replace generated output only; restore it if the second rename fails."""
    root = root.resolve()
    candidate = Path(candidate)
    target = root / 'public'
    if (linklike(candidate) or candidate.name != 'site' or
            candidate.resolve().parents[1] != root or
            not candidate.parent.name.startswith('.portfolio-build-')):
        raise ReleaseError('PROMOTION_PATH: candidate is not an owned staging directory')
    if linklike(target) or (target.exists() and not target.is_dir()):
        raise ReleaseError('PROMOTION_PATH: public must be an ordinary generated directory')
    holder = Path(tempfile.mkdtemp(prefix='.portfolio-previous-', dir=root))
    previous = holder / 'public'
    moved = False
    try:
        if target.exists():
            target.rename(previous)
            moved = True
        try:
            candidate.rename(target)
        except OSError as error:
            if moved:
                try:
                    previous.rename(target)
                except OSError:
                    raise ReleaseError('PROMOTION_RECOVERY: previous output retained at ' + previous.relative_to(root).as_posix()) from error
            raise ReleaseError('PROMOTION_FAILED: previous output restored; no candidate promoted') from error
    except OSError as error:
        raise ReleaseError('PROMOTION_FAILED: previous output was not changed') from error
    finally:
        # If restoration failed, retain the previous output for manual recovery.
        if not previous.exists():
            _remove_owned_holder(root, holder)
    if holder.exists():
        _remove_owned_holder(root, holder)


def _fetch(url):
    request = Request(url, headers={'User-Agent': 'PortfolioReleaseVerifier/1.0', 'Accept-Encoding': 'identity'})
    with urlopen(request, timeout=30) as response:
        return response.read(), response.status, response.headers.get_content_type()


def verify_remote(url, expected, expected_revision=None):
    from tools.content_contract import validate_site_url
    base = validate_site_url(url)
    try:
        raw, status, _ = _fetch(base + '/release.json')
        if status != 200:
            raise ReleaseError('REMOTE_MANIFEST: manifest request was not successful')
        served = decode_manifest(raw)
    except (OSError, ValueError) as error:
        raise ReleaseError('REMOTE_MANIFEST: no verified manifest received; publication is not confirmed') from error
    fields = {'schema_version', 'site_url', 'updated', 'content_digest', 'source_revision', 'files'}
    if (not isinstance(served, dict) or set(served) != fields or
            type(served['schema_version']) is not int or served['schema_version'] != 1 or
            served['site_url'] != base):
        raise ReleaseError('REMOTE_SCHEMA: unsupported or mismatched site release')
    source_revision = served['source_revision']
    if source_revision is not None and (not isinstance(source_revision, str) or
                                        not re.fullmatch('[0-9a-f]{40}', source_revision)):
        raise ReleaseError('REMOTE_SCHEMA: invalid source revision')
    if not isinstance(served['files'], list):
        raise ReleaseError('REMOTE_SCHEMA: expected an ordered file inventory')
    for entry in served['files']:
        if (not isinstance(entry, dict) or set(entry) != {'path', 'bytes', 'sha256'} or
                not isinstance(entry['path'], str) or type(entry['bytes']) is not int or entry['bytes'] < 0 or
                not isinstance(entry['sha256'], str) or not re.fullmatch('[0-9a-f]{64}', entry['sha256'])):
            raise ReleaseError('REMOTE_SCHEMA: invalid file record')
    for field in ('content_digest', 'updated', 'files'):
        if served.get(field) != expected[field]:
            raise ReleaseError('REMOTE_MISMATCH: served release differs from the validated candidate')
    revision = expected_revision or expected.get('source_revision')
    if revision and served.get('source_revision') != revision:
        raise ReleaseError('REMOTE_REVISION: expected source revision is not served')

    def check(entry):
        try:
            data, status, mime = _fetch(base + '/' + quote(entry['path'], safe='/'))
        except OSError as error:
            raise ReleaseError('REMOTE_FILE: could not confirm ' + entry['path']) from error
        if status != 200 or len(data) != entry['bytes'] or digest(data) != entry['sha256']:
            raise ReleaseError('REMOTE_BYTES: content differs for ' + entry['path'])
        suffix = Path(entry['path']).suffix
        types = {'.html': {'text/html'}, '.css': {'text/css'}, '.js': {'text/javascript', 'application/javascript'},
                 '.webp': {'image/webp'}, '.jpg': {'image/jpeg'}, '.svg': {'image/svg+xml'}}
        if suffix in types and mime not in types[suffix]:
            raise ReleaseError('REMOTE_MIME: unexpected media type for ' + entry['path'])
        return {'path': entry['path'], 'status': status, 'mime': mime, 'bytes': len(data)}

    with ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(check, expected['files']))
    return {'content_digest': served['content_digest'], 'source_revision': served['source_revision'], 'files': records}


def main():
    from tools.content_contract import load_content
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['verify', 'verify-remote'])
    parser.add_argument('--directory', type=Path, default=ROOT / 'public')
    parser.add_argument('--url', default='https://teoriadejuego.github.io')
    parser.add_argument('--expected-revision')
    args = parser.parse_args()
    try:
        content = load_content(ROOT)
        release = verify_release(args.directory, content)
        if args.command == 'verify-remote':
            result = verify_remote(args.url, release, args.expected_revision)
            (ROOT / 'qa').mkdir(exist_ok=True)
            (ROOT / 'qa/remote-release.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8')
            print('REMOTE_CONFIRMED:', result['content_digest'], result['source_revision'], len(result['files']), 'files')
        else:
            print('ARTIFACT_VALID:', release['content_digest'], len(release['files']), 'servable files')
    except (ValueError, OSError) as error:
        print(str(error) if isinstance(error, ValueError) else 'RELEASE_IO: operation could not be completed', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
