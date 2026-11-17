"""Remote manifest regressions with validated temporary artifacts and no network."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import unquote

from tools.content_contract import load_content
from tools import release


class RemoteReleaseTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='portfolio-remote-test-')
        self.addCleanup(temporary.cleanup)
        self.output = Path(temporary.name)
        content = load_content(Path(__file__).resolve().parents[1])
        for name in release.expected_paths(content) - {'release.json'}:
            path = self.output / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b'' if name == '.nojekyll' else b'Public synthetic fixture\n')
        self.base = 'https://portfolio.example.org/site'
        self.expected = release.create_manifest(self.output, content, self.base)
        self.assertEqual(release.verify_release(self.output, content, self.base), self.expected)

    def verify(self, served, status=200, expected_revision=None):
        raw = served if isinstance(served, bytes) else json.dumps(served).encode('utf8')
        types = {'.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript',
                 '.webp': 'image/webp', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml'}
        self.requests = []

        def fetch(url):
            self.requests.append(url)
            self.assertTrue(url.startswith(self.base + '/'))
            name = unquote(url[len(self.base) + 1:])
            if name == 'release.json':
                return raw, status, 'application/json'
            self.assertIn(name, {entry['path'] for entry in self.expected['files']})
            return (self.output / name).read_bytes(), 200, types.get(Path(name).suffix, 'text/plain')

        with patch.object(release, '_fetch', side_effect=fetch):
            return release.verify_remote(self.base, self.expected, expected_revision)

    def reject_before_files(self, served, diagnostic='REMOTE_SCHEMA', status=200):
        with self.assertRaisesRegex(release.ReleaseError, diagnostic) as caught:
            self.verify(served, status=status)
        self.assertNotIn('PRIVATE_FIXTURE_VALUE', str(caught.exception))
        self.assertEqual(self.requests, [self.base + '/release.json'])

    def test_valid_unattributed_release_checks_every_file(self):
        result = self.verify(self.expected)
        self.assertIsNone(result['source_revision'])
        self.assertEqual(result['content_digest'], self.expected['content_digest'])
        self.assertEqual(len(result['files']), len(self.expected['files']))
        self.assertEqual(len(self.requests), len(self.expected['files']) + 1)

    def test_valid_attributed_release_and_explicit_revision(self):
        self.expected['source_revision'] = 'a' * 40
        result = self.verify(self.expected, expected_revision='a' * 40)
        self.assertEqual(result['source_revision'], 'a' * 40)

    def test_every_required_field_must_exist(self):
        for field in self.expected:
            with self.subTest(field=field):
                served = deepcopy(self.expected)
                served.pop(field)
                self.reject_before_files(served)

    def test_extra_fields_rejected_without_echoing_values(self):
        served = {**self.expected, 'unexpected': 'PRIVATE_FIXTURE_VALUE'}
        self.reject_before_files(served)

    def test_schema_is_integer_one_not_boolean_float_or_string(self):
        for value in (True, False, 1.0, '1', 2, None, []):
            with self.subTest(value=value):
                self.reject_before_files({**self.expected, 'schema_version': value})

    def test_revision_must_be_null_or_lowercase_sha40(self):
        for value in (True, 1, {}, [], '', 'A' * 40, 'PRIVATE_FIXTURE_VALUE'):
            with self.subTest(value_type=type(value).__name__):
                self.reject_before_files({**self.expected, 'source_revision': value})

    def test_wrong_valid_revision_is_not_attributed_to_expected_commit(self):
        self.expected['source_revision'] = 'a' * 40
        self.reject_before_files({**self.expected, 'source_revision': 'b' * 40}, 'REMOTE_REVISION')

    def test_manifest_requires_http_200(self):
        for status in (201, 204, 304, 404, 503):
            with self.subTest(status=status):
                self.reject_before_files(self.expected, 'REMOTE_MANIFEST', status=status)

    def test_nonobject_or_malformed_json_is_controlled(self):
        for raw in (b'null', b'[]', b'"PRIVATE_FIXTURE_VALUE"', b'{broken PRIVATE_FIXTURE_VALUE',
                    b'{"schema_version":1,"schema_version":1}', b'{"schema_version":NaN}'):
            with self.subTest(raw=raw[:8]):
                diagnostic = 'REMOTE_SCHEMA' if raw in (b'null', b'[]', b'"PRIVATE_FIXTURE_VALUE"') else 'REMOTE_MANIFEST'
                self.reject_before_files(raw, diagnostic)

    def test_inventory_shape_rejected_before_file_downloads(self):
        for value in (None, {}, [None], [{'path': 'index.html', 'bytes': True, 'sha256': 'a' * 64}],
                      [{'path': 'index.html', 'bytes': 1, 'sha256': 'PRIVATE_FIXTURE_VALUE'}]):
            with self.subTest(value_type=type(value).__name__):
                self.reject_before_files({**self.expected, 'files': value})

    def test_changed_digest_or_inventory_is_not_confirmed(self):
        self.reject_before_files({**self.expected, 'content_digest': 'a' * 64}, 'REMOTE_MISMATCH')
        served = deepcopy(self.expected)
        served['files'][0]['bytes'] += 1
        self.reject_before_files(served, 'REMOTE_MISMATCH')

    def test_manifest_io_error_is_sanitized(self):
        with patch.object(release, '_fetch', side_effect=OSError('PRIVATE_FIXTURE_VALUE')):
            with self.assertRaisesRegex(release.ReleaseError, 'REMOTE_MANIFEST') as caught:
                release.verify_remote(self.base, self.expected)
        self.assertNotIn('PRIVATE_FIXTURE_VALUE', str(caught.exception))


if __name__ == '__main__':
    unittest.main()
