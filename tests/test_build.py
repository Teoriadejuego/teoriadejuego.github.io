"""Build acceptance in disposable repositories; never builds the shared public/.

These tests exercise handled validation/render failures, not process termination
or atomic directory exchange. Rename recovery belongs to the release tests.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest


SOURCE = Path(__file__).resolve().parents[1]
BASE = "https://portfolio.example.org/site"
SOURCE_FILES = ("build.py", "tools/content_contract.py", "tools/release.py", "tests/check_static.py")


def tree_bytes(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}


class IsolatedBuildTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="portfolio-build-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "fixture"
        self.root.mkdir()
        for name in SOURCE_FILES:
            destination = self.root / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SOURCE / name, destination)
        for name in ("data", "assets"):
            shutil.copytree(SOURCE / name, self.root / name)
        self.env = os.environ.copy()
        for key in ("PYTHONPATH", "PYTHONPYCACHEPREFIX", "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "PORTFOLIO_OUTPUT_DIR"):
            self.env.pop(key, None)
        self.env.update(SITE_URL=BASE, PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1", PYTHONIOENCODING="utf-8")

    def run_python(self, code=None, env=None):
        command = [sys.executable, "-B", "-X", "utf8"]
        command += ["-c", textwrap.dedent(code)] if code is not None else ["build.py"]
        return subprocess.run(command, cwd=self.root, env=self.env if env is None else env,
                              capture_output=True, text=True, encoding="utf8", timeout=45)

    def successful_build(self, code=None, env=None):
        result = self.run_python(code=code, env=env)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("BUILD_VALID:", result.stdout)
        self.assertEqual(result.stderr, "")
        self.assert_no_staging()
        return json.loads((self.root / "public/release.json").read_text(encoding="utf8"))

    def assert_no_staging(self):
        self.assertEqual(list(self.root.glob(".portfolio-build-*")), [])
        self.assertEqual(list(self.root.glob(".portfolio-previous-*")), [])

    def source_snapshot(self):
        return {name: data for name, data in tree_bytes(self.root).items() if not name.startswith("public/")}

    def assert_previous_preserved(self, before, result, diagnostic=None):
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("BUILD_VALID:", result.stdout)
        if diagnostic:
            self.assertIn(diagnostic, result.stderr)
        self.assertEqual(tree_bytes(self.root / "public"), before)
        self.assert_no_staging()

    def test_import_has_no_filesystem_side_effects(self):
        before = tree_bytes(self.root)
        result = self.run_python("import build\nassert build.OUT is None")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(tree_bytes(self.root), before)
        self.assertFalse((self.root / "public").exists())
        self.assert_no_staging()
        (self.root / "public").mkdir()
        (self.root / "public/index.html").write_bytes(b"PREVIOUS_PUBLIC_BYTES")
        before = tree_bytes(self.root)
        result = self.run_python("import build")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(tree_bytes(self.root), before)

    def test_valid_build_preserves_sources_and_produces_verifiable_bytes(self):
        before = self.source_snapshot()
        manifest = self.successful_build()
        self.assertEqual(self.source_snapshot(), before)
        self.assertEqual(manifest["schema_version"], 1)
        self.assertEqual(manifest["site_url"], BASE)
        self.assertIsNone(manifest["source_revision"])  # Fixture is deliberately not a Git checkout.
        site = json.loads((self.root / "data/site.json").read_text(encoding="utf8"))
        self.assertEqual(manifest["updated"], site["updated"])
        output = tree_bytes(self.root / "public")
        self.assertEqual(output[".nojekyll"], b"")
        payload = {name: data for name, data in output.items() if name not in {"release.json", ".nojekyll"}}
        self.assertEqual([entry["path"] for entry in manifest["files"]], sorted(payload))
        for entry in manifest["files"]:
            data = payload[entry["path"]]
            self.assertEqual(entry["bytes"], len(data))
            self.assertEqual(entry["sha256"], hashlib.sha256(data).hexdigest())
        canonical = json.dumps(manifest["files"], ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf8")
        self.assertEqual(manifest["content_digest"], hashlib.sha256(canonical).hexdigest())
        for name, data in output.items():
            if Path(name).suffix in {".html", ".css", ".js", ".svg", ".json", ".xml", ".txt", ".bib"}:
                self.assertNotIn("\r", data.decode("utf8"), name)
        self.assertIn((BASE + "/en/").encode(), output["en/index.html"])

    def test_rebuild_is_byte_identical_with_different_hash_seed_and_timezone(self):
        first_env = {**self.env, "PYTHONHASHSEED": "1", "TZ": "UTC"}
        first = self.successful_build(env=first_env)
        before = tree_bytes(self.root / "public")
        second = self.successful_build(env={**self.env, "PYTHONHASHSEED": "739", "TZ": "Europe/Madrid"})
        self.assertEqual(first["content_digest"], second["content_digest"])
        self.assertEqual(tree_bytes(self.root / "public"), before)

    def test_source_text_newlines_do_not_change_artifact_digest(self):
        first = self.successful_build()
        before = tree_bytes(self.root / "public")
        for parent in [self.root / "data", self.root / "assets"]:
            for path in parent.iterdir():
                if path.suffix in {".json", ".js", ".css", ".svg"}:
                    text = path.read_text(encoding="utf8")
                    path.write_bytes(text.replace("\n", "\r\n").encode("utf8"))
        changed_sources = self.source_snapshot()
        second = self.successful_build()
        self.assertEqual(first["content_digest"], second["content_digest"])
        self.assertEqual(tree_bytes(self.root / "public"), before)
        self.assertEqual(self.source_snapshot(), changed_sources)

    def test_successful_promotion_removes_stale_and_private_fixture_files(self):
        first = self.successful_build()
        before = tree_bytes(self.root / "public")
        (self.root / "public/stale-private-note.txt").write_text("SYNTHETIC_PRIVATE_FIXTURE", encoding="utf8")
        nested = self.root / "public/old-route"
        nested.mkdir()
        (nested / "index.html").write_bytes(b"STALE_PUBLIC_PAGE")
        # A source-side operator note must also remain outside the output.
        (self.root / "operator-private-fixture.txt").write_text("SYNTHETIC_OPERATOR_NOTE", encoding="utf8")
        sources = self.source_snapshot()
        second = self.successful_build()
        self.assertEqual(second["content_digest"], first["content_digest"])
        self.assertEqual(tree_bytes(self.root / "public"), before)
        self.assertEqual(self.source_snapshot(), sources)

    def test_invalid_editorial_inputs_preserve_previous_output(self):
        self.successful_build()
        before = tree_bytes(self.root / "public")
        target = self.root / "data/site.json"
        original = target.read_bytes()
        variants = [b'{"SECRET_FIXTURE_VALUE":broken}', json.dumps({"schema_version": 1, "updated": "2024-02-30", "home_projects": ["sonar"], "home_publications": ["honesty"]}).encode()]
        for raw in variants:
            with self.subTest(case="invalid JSON" if b"broken" in raw else "invalid date"):
                target.write_bytes(raw)
                current_sources = self.source_snapshot()
                result = self.run_python()
                self.assert_previous_preserved(before, result, "data/site.json")
                self.assertNotIn("SECRET_FIXTURE_VALUE", result.stderr)
                self.assertEqual(self.source_snapshot(), current_sources)
        target.write_bytes(original)

    def test_invalid_site_url_preserves_previous_output_and_sanitizes_error(self):
        self.successful_build()
        before = tree_bytes(self.root / "public")
        for value in ["javascript:SECRET_FIXTURE_VALUE", "https://user:SECRET_FIXTURE_VALUE@example.org", "https://example.org/?token=SECRET_FIXTURE_VALUE", "https://example.org/../private"]:
            with self.subTest(case=value.split(":", 1)[0]):
                result = self.run_python(env={**self.env, "SITE_URL": value})
                self.assert_previous_preserved(before, result, "SITE_URL")
                self.assertNotIn("SECRET_FIXTURE_VALUE", result.stderr)

    def test_partial_render_io_failure_preserves_previous_and_cleans_staging(self):
        self.successful_build()
        before = tree_bytes(self.root / "public")
        sources = self.source_snapshot()
        result = self.run_python('''
            import build
            def partial(output, content, site_url):
                (output / 'partial.html').write_text('PARTIAL_CANDIDATE', encoding='utf8')
                raise OSError('SECRET_RENDER_FIXTURE')
            build.render = partial
            raise SystemExit(build.main())
        ''')
        self.assert_previous_preserved(before, result, "RENDER_FAILED")
        self.assertNotIn("SECRET_RENDER_FIXTURE", result.stderr)
        self.assertEqual(self.source_snapshot(), sources)

    def test_unexpected_render_exception_does_not_publish_or_echo_payload(self):
        self.successful_build()
        before = tree_bytes(self.root / "public")
        result = self.run_python('''
            import build
            def partial(output, content, site_url):
                (output / 'partial.html').write_bytes(b'PARTIAL_CANDIDATE')
                raise RuntimeError('SECRET_RENDER_FIXTURE')
            build.render = partial
            raise SystemExit(build.main())
        ''')
        self.assert_previous_preserved(before, result)
        self.assertNotIn("SECRET_RENDER_FIXTURE", result.stderr)

    def test_static_check_failure_blocks_promotion(self):
        self.successful_build()
        before = tree_bytes(self.root / "public")
        result = self.run_python('''
            import build
            original = build.render
            def broken_link(output, content, site_url):
                original(output, content, site_url)
                target = output / 'index.html'
                target.write_text(target.read_text(encoding='utf8') + '<a href="missing-page/">Broken fixture</a>', encoding='utf8', newline='\\n')
            build.render = broken_link
            raise SystemExit(build.main())
        ''')
        self.assert_previous_preserved(before, result, "STATIC_CHECK_FAILED")

    def test_artifact_extra_file_blocks_promotion_after_render(self):
        self.successful_build()
        before = tree_bytes(self.root / "public")
        result = self.run_python('''
            import build
            original = build.render
            def extra_file(output, content, site_url):
                original(output, content, site_url)
                (output / 'private-fixture.txt').write_text('SYNTHETIC_PRIVATE_FIXTURE', encoding='utf8')
            build.render = extra_file
            raise SystemExit(build.main())
        ''')
        self.assert_previous_preserved(before, result, "ARTIFACT_EXTRA")

    def test_unapproved_asset_blocks_promotion_and_remains_a_source(self):
        self.successful_build()
        before = tree_bytes(self.root / "public")
        (self.root / "assets/private-fixture.txt").write_text("SYNTHETIC_PRIVATE_FIXTURE", encoding="utf8")
        sources = self.source_snapshot()
        result = self.run_python()
        self.assert_previous_preserved(before, result, "ASSET_INVENTORY")
        self.assertEqual(self.source_snapshot(), sources)

    def test_build_and_static_child_make_no_network_or_acquisition_calls(self):
        guard = Path(self.temporary.name) / "guard"
        guard.mkdir()
        marker = guard / "blocked-attempt"
        (guard / "sitecustomize.py").write_text(textwrap.dedent('''
            import os, subprocess, sys
            def audit(event, args):
                blocked = event.startswith('socket.') or event == 'urllib.Request'
                if event == 'subprocess.Popen':
                    executable, command = args[0], args[1]
                    # Windows audits a serialized command and may leave executable=None.
                    serialized = command if isinstance(command, str) else subprocess.list2cmdline(command)
                    name = os.path.basename(executable).lower() if executable else None
                    git_commands = [subprocess.list2cmdline(parts) for parts in (
                        ['git', 'status', '--porcelain'], ['git', 'rev-parse', 'HEAD'])]
                    git_read = name in (None, 'git', 'git.exe') and serialized in git_commands
                    expected_static = subprocess.list2cmdline([sys.executable, os.environ['BUILD_STATIC_SCRIPT']])
                    static_child = executable in (None, sys.executable) and serialized == expected_static
                    blocked = not (git_read or static_child)
                if blocked:
                    with open(os.environ['BUILD_GUARD_MARKER'], 'w', encoding='utf8') as handle:
                        handle.write('Blocked network or acquisition attempt')
                    raise RuntimeError('NETWORK_OR_ACQUISITION_FORBIDDEN')
            sys.addaudithook(audit)
        '''), encoding="utf8")
        env = {**self.env, "PYTHONPATH": str(guard), "BUILD_GUARD_MARKER": str(marker), "BUILD_STATIC_SCRIPT": str(self.root / "tests/check_static.py")}
        for code in ["import socket; socket.socket()", "import subprocess; subprocess.run(['git', 'fetch'])"]:
            # Prove the guard rejects both network use and acquisition commands
            # before relying on its silence during the real build.
            result = self.run_python(code, env=env)
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(marker.exists())
            self.assertIn("NETWORK_OR_ACQUISITION_FORBIDDEN", result.stderr)
            marker.unlink()
        self.successful_build(env=env)
        self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()
