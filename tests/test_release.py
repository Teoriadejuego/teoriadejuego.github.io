"""Independent artifact and promotion checks using isolated synthetic files only."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from tools import release


class ReleaseFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='portfolio-release-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'source.json'
        self.source_bytes = b'{"private_fixture": "must remain unchanged"}\n'
        self.source.write_bytes(self.source_bytes)
        self.content = {
            'site': {'updated': '2026-11-18'},
            'projects': [{'id': 'case-one'}],
            'publications': [{'id': 'paper-one'}],
        }
        self.url = 'https://example.org'
        self.candidate = self.root / '.portfolio-build-fixture' / 'site'
        self.candidate.mkdir(parents=True)
        for name in release.expected_paths(self.content) - {'release.json'}:
            path = self.candidate / name
            path.parent.mkdir(parents=True, exist_ok=True)
            if name == '.nojekyll':
                data = b''
            elif path.suffix in release.TEXT_SUFFIXES:
                data = 'Public fixture — prueba\n'.encode('utf-8')
            else:
                data = b'fixture-binary\x00\x01'
            path.write_bytes(data)

    def tearDown(self):
        self.assertEqual(self.source.read_bytes(), self.source_bytes,
                         'A release operation changed source material')

    def manifest(self, revision=None):
        return release.create_manifest(self.candidate, self.content, self.url, revision)

    def write_manifest(self, manifest):
        (self.candidate / 'release.json').write_bytes(
            (json.dumps(manifest, ensure_ascii=False) + '\n').encode('utf-8'))

    def assert_rejected(self, manifest):
        self.write_manifest(manifest)
        with self.assertRaises(release.ReleaseError):
            release.verify_release(self.candidate, self.content, self.url)

    def symlink(self, path, target, directory=False):
        try:
            path.symlink_to(target, target_is_directory=directory)
        except (OSError, NotImplementedError) as error:
            self.skipTest('Host cannot create a test symlink: ' + type(error).__name__)

    def old_output(self):
        target = self.root / 'public'
        target.mkdir()
        (target / 'previous.txt').write_bytes(b'previous valid release\n')
        return target


class ArtifactTests(ReleaseFixture):
    def test_expected_paths_include_both_languages_and_downloads(self):
        expected = release.expected_paths(self.content)
        self.assertIn('projects/case-one/index.html', expected)
        self.assertIn('en/projects/case-one/index.html', expected)
        self.assertIn('downloads/paper-one.bib', expected)
        self.assertIn('downloads/publications.bib', expected)
        self.assertIn('.nojekyll', expected)
        self.assertIn('release.json', expected)
        self.assertNotIn('source.json', expected)
        self.assertNotIn('data/publications.json', expected)

    def test_manifest_hashes_match_independent_byte_inventory(self):
        manifest = self.manifest('a' * 40)
        expected = []
        for path in sorted(self.candidate.rglob('*')):
            if path.is_file() and path.name not in {'release.json', '.nojekyll'}:
                raw = path.read_bytes()
                expected.append({'path': path.relative_to(self.candidate).as_posix(),
                                 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
        expected.sort(key=lambda entry: entry['path'])
        self.assertEqual(manifest['files'], expected)
        serialized = json.dumps(expected, ensure_ascii=False, sort_keys=True,
                                separators=(',', ':')).encode('utf-8')
        self.assertEqual(manifest['content_digest'], hashlib.sha256(serialized).hexdigest())
        self.assertEqual(release.verify_release(self.candidate, self.content, self.url), manifest)
        self.assertNotIn('\r', (self.candidate / 'release.json').read_bytes().decode('utf-8'))

    def test_repeat_and_revision_do_not_change_content_digest(self):
        first = self.manifest('a' * 40)
        first_bytes = (self.candidate / 'release.json').read_bytes()
        (self.candidate / 'release.json').unlink()
        second = self.manifest('a' * 40)
        self.assertEqual((self.candidate / 'release.json').read_bytes(), first_bytes)
        (self.candidate / 'release.json').unlink()
        third = self.manifest('b' * 40)
        self.assertEqual(first['content_digest'], second['content_digest'])
        self.assertEqual(first['content_digest'], third['content_digest'])
        self.assertNotEqual(first['source_revision'], third['source_revision'])

    def test_public_content_change_changes_digest(self):
        first = self.manifest()
        (self.candidate / 'release.json').unlink()
        (self.candidate / 'robots.txt').write_bytes(b'Changed public fixture\n')
        second = self.manifest()
        self.assertNotEqual(first['content_digest'], second['content_digest'])

    def test_tampering_is_detected(self):
        self.manifest()
        (self.candidate / 'robots.txt').write_bytes(b'changed after verification\n')
        with self.assertRaisesRegex(release.ReleaseError, 'MISMATCH'):
            release.verify_release(self.candidate, self.content)

    def test_missing_file_is_detected(self):
        self.manifest()
        (self.candidate / 'assets/hero.webp').unlink()
        with self.assertRaisesRegex(release.ReleaseError, 'MISSING'):
            release.verify_release(self.candidate, self.content)

    def test_extra_file_is_detected(self):
        self.manifest()
        (self.candidate / 'private-notes.txt').write_bytes(b'synthetic extra file\n')
        with self.assertRaisesRegex(release.ReleaseError, 'EXTRA'):
            release.verify_release(self.candidate, self.content)

    def test_file_symlink_is_rejected(self):
        self.manifest()
        linked = self.candidate / 'robots.txt'
        linked.unlink()
        self.symlink(linked, self.source)
        with self.assertRaisesRegex(release.ReleaseError, 'PATH'):
            release.verify_release(self.candidate, self.content)

    def test_directory_symlink_escape_is_rejected(self):
        self.manifest()
        self.symlink(self.candidate / 'escape', self.root, directory=True)
        with self.assertRaisesRegex(release.ReleaseError, 'PATH'):
            release.verify_release(self.candidate, self.content)

    def test_artifact_root_symlink_is_rejected(self):
        self.manifest()
        alias = self.root / 'alias'
        self.symlink(alias, self.candidate, directory=True)
        with self.assertRaisesRegex(release.ReleaseError, 'ROOT'):
            release.verify_release(alias, self.content)

    def test_link_detection_guard_without_host_symlink_privileges(self):
        """Exercise rejection locally; real filesystem links are tested separately."""
        self.manifest()
        detector = release.linklike
        for flagged in (self.candidate, self.candidate / 'robots.txt'):
            with self.subTest(flagged=flagged.name):
                with patch.object(release, 'linklike',
                                  side_effect=lambda path: path == flagged or detector(path)):
                    with self.assertRaises(release.ReleaseError):
                        release.verify_release(self.candidate, self.content)

    def test_manifest_traversal_or_absolute_paths_are_rejected(self):
        good = self.manifest()
        for path in ('../source.json', '/source.json', 'C:/fixture.txt', 'assets\\app.js'):
            with self.subTest(path=path):
                bad = deepcopy(good)
                bad['files'][0]['path'] = path
                self.assert_rejected(bad)

    def test_nonempty_sentinel_is_rejected(self):
        (self.candidate / '.nojekyll').write_bytes(b'not empty')
        with self.assertRaisesRegex(release.ReleaseError, 'CONTROL'):
            self.manifest()

    def test_invalid_utf8_and_crlf_are_rejected(self):
        for data, category in ((b'bad\xff\n', 'ENCODING'), (b'line\r\n', 'NEWLINES')):
            with self.subTest(category=category):
                (self.candidate / 'robots.txt').write_bytes(data)
                with self.assertRaisesRegex(release.ReleaseError, category):
                    self.manifest()

    def test_synthetic_secret_and_local_path_are_redacted(self):
        values = ['ghp_' + 'A' * 24, 'github_pat_' + 'B' * 24,
                  'C:\\Users\\synthetic-owner\\fixture.txt',
                  '-----BEGIN PRIVATE KEY-----']
        for value in values:
            with self.subTest(kind=value.split('_')[0][:12]):
                (self.candidate / 'robots.txt').write_bytes((value + '\n').encode('utf-8'))
                with self.assertRaises(release.ReleaseError) as caught:
                    self.manifest()
                self.assertNotIn(value, str(caught.exception))
                self.assertIn('PUBLIC_CONTENT', str(caught.exception))

    def test_public_byte_budget_exact_boundary(self):
        self.manifest()
        size = sum(p.stat().st_size for p in self.candidate.rglob('*') if p.is_file())
        with patch.object(release, 'MAX_PUBLIC_BYTES', size):
            release.verify_release(self.candidate, self.content)
        with patch.object(release, 'MAX_PUBLIC_BYTES', size - 1):
            with self.assertRaisesRegex(release.ReleaseError, 'BUDGET_PUBLIC'):
                release.verify_release(self.candidate, self.content)

    def test_asset_byte_budget_exact_boundary(self):
        self.manifest()
        size = sum(p.stat().st_size for p in (self.candidate / 'assets').iterdir())
        with patch.object(release, 'MAX_ASSET_BYTES', size):
            release.verify_release(self.candidate, self.content)
        with patch.object(release, 'MAX_ASSET_BYTES', size - 1):
            with self.assertRaisesRegex(release.ReleaseError, 'BUDGET_ASSETS'):
                release.verify_release(self.candidate, self.content)

    def test_unknown_version_and_boolean_version_are_rejected(self):
        good = self.manifest()
        for value in (2, True, '1', 1.0, None):
            with self.subTest(value=value):
                bad = deepcopy(good)
                bad['schema_version'] = value
                self.assert_rejected(bad)

    def test_manifest_fields_have_strict_types_and_shape(self):
        good = self.manifest()
        invalid = [('files', {}), ('files', None), ('content_digest', 123),
                   ('updated', 20261118), ('site_url', ['https://example.org']),
                   ('source_revision', True), ('source_revision', 'a' * 39),
                   ('source_revision', 'G' * 40)]
        for key, value in invalid:
            with self.subTest(key=key, value=value):
                bad = deepcopy(good)
                bad[key] = value
                self.assert_rejected(bad)
        for bad in ([], None, {**good, 'unexpected': 'field'},
                    {key: value for key, value in good.items() if key != 'updated'}):
            with self.subTest(shape=type(bad).__name__):
                self.assert_rejected(bad)

    def test_inventory_byte_counts_require_integer_not_bool_or_float(self):
        (self.candidate / 'robots.txt').write_bytes(b'x')
        good = self.manifest()
        index = next(i for i, entry in enumerate(good['files']) if entry['path'] == 'robots.txt')
        for value in (True, 1.0, '1', -1):
            with self.subTest(value=repr(value)):
                bad = deepcopy(good)
                bad['files'][index]['bytes'] = value
                self.assert_rejected(bad)

    def test_inventory_order_duplicates_and_extra_fields_are_rejected(self):
        good = self.manifest()
        cases = []
        bad = deepcopy(good); bad['files'].reverse(); cases.append(bad)
        bad = deepcopy(good); bad['files'].append(deepcopy(bad['files'][0])); cases.append(bad)
        bad = deepcopy(good); bad['files'][0]['extra'] = 1; cases.append(bad)
        for index, bad in enumerate(cases):
            with self.subTest(index=index):
                self.assert_rejected(bad)

    def test_duplicate_json_keys_are_rejected_at_every_level(self):
        good = self.manifest()
        raw = json.dumps(good)
        top_duplicate = '{"schema_version": 2, ' + raw[1:]
        entry = good['files'][0]
        nested_duplicate = raw.replace(json.dumps(entry),
                                       '{"path": "../wrong", ' + json.dumps(entry)[1:], 1)
        for label, text in (('top', top_duplicate), ('entry', nested_duplicate)):
            with self.subTest(level=label):
                (self.candidate / 'release.json').write_bytes((text + '\n').encode('utf-8'))
                with self.assertRaises(release.ReleaseError):
                    release.verify_release(self.candidate, self.content)

    def test_malformed_json_is_rejected(self):
        self.manifest()
        (self.candidate / 'release.json').write_bytes(b'{not JSON\n')
        with self.assertRaisesRegex(release.ReleaseError, 'JSON'):
            release.verify_release(self.candidate, self.content)

    def test_manifest_identity_and_date_must_match_candidate(self):
        good = self.manifest()
        for key, value in (('site_url', 'https://other.example'), ('updated', '2025-01-01')):
            with self.subTest(key=key):
                bad = deepcopy(good); bad[key] = value
                self.assert_rejected(bad)


class PromotionTests(ReleaseFixture):
    def test_successful_promotion_replaces_only_generated_output(self):
        self.manifest()
        target = self.old_output()
        candidate_bytes = (self.candidate / 'release.json').read_bytes()
        release.promote(self.root, self.candidate)
        self.assertEqual((target / 'release.json').read_bytes(), candidate_bytes)
        self.assertFalse((target / 'previous.txt').exists())
        self.assertFalse(self.candidate.exists())
        self.assertEqual(list(self.root.glob('.portfolio-previous-*')), [])
        release.verify_release(target, self.content)

    def test_first_publication_without_previous_output(self):
        self.manifest()
        release.promote(self.root, self.candidate)
        release.verify_release(self.root / 'public', self.content)
        self.assertEqual(list(self.root.glob('.portfolio-previous-*')), [])

    def test_failed_second_rename_restores_previous_output(self):
        target = self.old_output()
        rename = Path.rename

        def fail_candidate(path, destination):
            if path == self.candidate:
                raise OSError('synthetic candidate rename failure')
            return rename(path, destination)

        with patch.object(Path, 'rename', fail_candidate):
            with self.assertRaisesRegex(release.ReleaseError, 'PROMOTION_FAILED'):
                release.promote(self.root, self.candidate)
        self.assertEqual((target / 'previous.txt').read_bytes(), b'previous valid release\n')
        self.assertTrue(self.candidate.is_dir())
        self.assertEqual(list(self.root.glob('.portfolio-previous-*')), [])

    def test_failed_restoration_retains_previous_bytes_and_reports_path(self):
        target = self.old_output()
        rename = Path.rename

        def fail_candidate_and_recovery(path, destination):
            if path == self.candidate or path.parent.name.startswith('.portfolio-previous-'):
                raise OSError('synthetic locked destination')
            return rename(path, destination)

        with patch.object(Path, 'rename', fail_candidate_and_recovery):
            with self.assertRaisesRegex(release.ReleaseError, 'PROMOTION_RECOVERY') as caught:
                release.promote(self.root, self.candidate)
        saved = list(self.root.glob('.portfolio-previous-*/public/previous.txt'))
        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0].read_bytes(), b'previous valid release\n')
        self.assertIn(saved[0].parent.relative_to(self.root).as_posix(), str(caught.exception))
        self.assertFalse(target.exists())
        self.assertTrue(self.candidate.is_dir())

    def test_failed_first_rename_does_not_change_previous_output(self):
        target = self.old_output()
        rename = Path.rename

        def fail_old(path, destination):
            if path == target:
                raise OSError('synthetic previous-directory lock')
            return rename(path, destination)

        with patch.object(Path, 'rename', fail_old):
            with self.assertRaisesRegex(release.ReleaseError, 'PROMOTION_FAILED'):
                release.promote(self.root, self.candidate)
        self.assertEqual((target / 'previous.txt').read_bytes(), b'previous valid release\n')
        self.assertTrue(self.candidate.exists())
        self.assertEqual(list(self.root.glob('.portfolio-previous-*')), [])

    def test_public_symlink_is_rejected_without_touching_target(self):
        elsewhere = self.root / 'elsewhere'
        elsewhere.mkdir()
        (elsewhere / 'keep.txt').write_bytes(b'keep')
        self.symlink(self.root / 'public', elsewhere, directory=True)
        with self.assertRaisesRegex(release.ReleaseError, 'PROMOTION_PATH'):
            release.promote(self.root, self.candidate)
        self.assertEqual((elsewhere / 'keep.txt').read_bytes(), b'keep')
        self.assertTrue(self.candidate.is_dir())

    def test_public_regular_file_is_rejected(self):
        (self.root / 'public').write_bytes(b'not a directory')
        with self.assertRaisesRegex(release.ReleaseError, 'PROMOTION_PATH'):
            release.promote(self.root, self.candidate)
        self.assertEqual((self.root / 'public').read_bytes(), b'not a directory')

    def test_candidate_outside_owned_staging_is_rejected(self):
        outside = self.root / 'unowned' / 'site'
        outside.mkdir(parents=True)
        (outside / 'keep.txt').write_bytes(b'keep')
        target = self.old_output()
        with self.assertRaisesRegex(release.ReleaseError, 'PROMOTION_PATH'):
            release.promote(self.root, outside)
        self.assertTrue((outside / 'keep.txt').exists())
        self.assertTrue((target / 'previous.txt').exists())
        with tempfile.TemporaryDirectory(prefix='portfolio-outside-test-') as other:
            foreign = Path(other) / '.portfolio-build-foreign' / 'site'
            foreign.mkdir(parents=True)
            with self.assertRaisesRegex(release.ReleaseError, 'PROMOTION_PATH'):
                release.promote(self.root, foreign)
            self.assertTrue(foreign.is_dir())

    def test_candidate_symlink_is_rejected(self):
        linked = self.root / '.portfolio-build-linked' / 'site'
        linked.parent.mkdir()
        self.symlink(linked, self.candidate, directory=True)
        with self.assertRaisesRegex(release.ReleaseError, 'PROMOTION_PATH'):
            release.promote(self.root, linked)
        self.assertTrue(self.candidate.is_dir())

    def test_link_detection_blocks_promotion_without_host_privileges(self):
        """Mock only the detector; neither rename nor path guards are mocked."""
        target = self.old_output()
        detector = release.linklike
        for flagged in (self.candidate, target):
            with self.subTest(flagged=flagged.name):
                with patch.object(release, 'linklike',
                                  side_effect=lambda path: path == flagged or detector(path)):
                    with self.assertRaisesRegex(release.ReleaseError, 'PROMOTION_PATH'):
                        release.promote(self.root, self.candidate)
                self.assertEqual((target / 'previous.txt').read_bytes(), b'previous valid release\n')
                self.assertTrue(self.candidate.is_dir())


class RevisionTests(unittest.TestCase):
    def test_clean_valid_git_revision_is_attributed(self):
        with patch.object(release.subprocess, 'check_output', side_effect=['', 'a' * 40 + '\n']):
            self.assertEqual(release.current_revision(Path('.')), 'a' * 40)

    def test_dirty_or_invalid_revision_is_not_attributed(self):
        for status, revision in [(' M source.json\n', 'a' * 40), ('?? new-source.json\n', 'a' * 40),
                                 ('', 'not-a-sha')]:
            with self.subTest(status=status, revision=revision):
                with patch.object(release.subprocess, 'check_output', side_effect=[status, revision]):
                    self.assertIsNone(release.current_revision(Path('.')))

    def test_unavailable_git_has_no_revision(self):
        for error in (OSError('unavailable'), subprocess.CalledProcessError(128, ['git'])):
            with self.subTest(error=type(error).__name__):
                with patch.object(release.subprocess, 'check_output', side_effect=error):
                    self.assertIsNone(release.current_revision(Path('.')))


if __name__ == '__main__':
    unittest.main()
