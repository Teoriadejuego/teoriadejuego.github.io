"""Independent editorial fixtures; no shared public/ build or network access."""
import copy
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import unittest
from unittest import mock

from tools.content_contract import ContentError, load_content, validate_content, validate_site_url


ROOT = Path(__file__).resolve().parents[1]


def bilingual(es="Texto público", en="Public text"):
    return {"es": es, "en": en}


def fixture():
    """Small synthetic corpus, intentionally not the production record counts."""
    publication = {
        "id": "historical-study", "doi": "10.1234/example.1", "year": 1901,
        "topic": "experiments", "title": "A documented experiment",
        "authors": ["Ana García López", "Ben Smith"],
        "author_parts": [{"given": "Ana", "family": "García López"}, {"given": "Ben", "family": "Smith"}],
        "journal": "Example Journal", "volume": "", "issue": "", "pages": "1–9",
        "summary": bilingual(), "links": [{"label": bilingual(), "url": "https://example.org/paper"}],
        "version": bilingual("Manuscrito anterior", "Earlier manuscript"),
    }
    project = {
        "id": "public-tool", "title": "PUBLIC-TOOL", "kind": "software",
        "repo": "example_repo", "demo": "https://example.org/demo/#guide",
        "tags": ["Python", bilingual("Datos", "Data")], "related": "research-case",
        "inspect": {"es": ["Consulta el código."], "en": ["Inspect the code."]},
        **{key: bilingual() for key in ("heading", "summary", "status", "role", "problem", "work", "evidence", "value", "seo_title")},
    }
    research = copy.deepcopy(project)
    research.update(id="research-case", title=bilingual(), kind="research", related="public-tool", doi=publication["doi"])
    research.pop("repo")
    research.pop("demo")
    research["additional_links"] = [{"label": bilingual(), "url": "https://example.org/data"}]
    return {
        "site": {"schema_version": 1, "updated": "2024-02-29", "home_projects": ["public-tool"], "home_publications": ["historical-study"]},
        "projects": [project, research], "publications": [publication],
        "software": [{"title": "Example", "repo": "example_repo", "description": bilingual(), "stage": bilingual()}],
        "working-papers": [{"title": "Work in progress", "year": 2099, "authors": "Ana García López; Ben Smith", "url": "https://doi.org/10.1234/working.1", "status": bilingual()}],
        "resources": [{"title": "Teaching instructions", "url": "https://example.org/record?id=42", "pdf": "https://example.org/paper%20%281%29.pdf"}],
    }


def write_fixture(root, content=None):
    content = fixture() if content is None else content
    (root / "data").mkdir(parents=True)
    for name, value in content.items():
        (root / "data" / (name + ".json")).write_text(json.dumps(value, ensure_ascii=False), encoding="utf8")
    return content


class EditorialValidationTests(unittest.TestCase):
    def setUp(self):
        self.content = fixture()

    def reject(self, content, field):
        with self.assertRaises(ContentError) as caught:
            validate_content(content)
        self.assertIn(field, str(caught.exception))
        return str(caught.exception)

    def test_valid_fixture_is_not_mutated(self):
        before = copy.deepcopy(self.content)
        self.assertIsNone(validate_content(self.content))
        self.assertEqual(self.content, before)

    def test_real_catalogues_pass_without_changes_or_fixed_counts(self):
        expected = {name: json.loads((ROOT / "data" / (name + ".json")).read_text(encoding="utf8")) for name in self.content}
        self.assertEqual(load_content(ROOT), expected)

    def test_missing_and_unknown_catalogues(self):
        for name in self.content:
            with self.subTest(name=name):
                broken = copy.deepcopy(self.content)
                del broken[name]
                self.reject(broken, "content." + name)
        broken = copy.deepcopy(self.content)
        broken["private-catalogue"] = "DO_NOT_ECHO"
        message = self.reject(broken, "content")
        self.assertNotIn("private-catalogue", message)
        self.assertNotIn("DO_NOT_ECHO", message)

    def test_every_catalogue_rejects_unexpected_fields(self):
        for name in self.content:
            with self.subTest(name=name):
                broken = copy.deepcopy(self.content)
                record = broken[name] if name == "site" else broken[name][0]
                record["CONFIDENTIAL_FIELD_NAME"] = "DO_NOT_ECHO"
                message = self.reject(broken, "data/" + name + ".json")
                self.assertNotIn("CONFIDENTIAL_FIELD_NAME", message)
                self.assertNotIn("DO_NOT_ECHO", message)

    def test_wrong_record_and_list_types(self):
        for name in self.content:
            with self.subTest(name=name):
                broken = copy.deepcopy(self.content)
                broken[name] = [] if name == "site" else {}
                self.reject(broken, "data/" + name + ".json")
                if name != "site":
                    broken[name] = ["not a record"]
                    self.reject(broken, "data/" + name + ".json[0]")

    def test_missing_required_fields_in_each_catalogue(self):
        fields = {"site": "updated", "projects": "role", "publications": "authors", "software": "stage", "working-papers": "status", "resources": "title"}
        for name, field in fields.items():
            with self.subTest(name=name):
                broken = copy.deepcopy(self.content)
                record = broken[name] if name == "site" else broken[name][0]
                del record[field]
                self.reject(broken, "." + field)

    def test_schema_version_is_strict_integer_one(self):
        for value in [True, False, 1.0, "1", None, 2]:
            with self.subTest(value=value):
                self.content["site"]["schema_version"] = value
                self.reject(self.content, "site.json.schema_version")

    def test_date_is_calendar_iso_not_clock_dependent(self):
        for value in ["2023-02-29", "2024-02-30", "2024-13-01", "2024-2-01", "20240201", "2024-01-01T00:00:00", "2024-01-01Z", None, True]:
            with self.subTest(value=value):
                self.content["site"]["updated"] = value
                self.reject(self.content, "site.json.updated")

    def test_year_types_and_historical_future_years(self):
        for name in ["publications", "working-papers"]:
            for value in [True, False, 2024.0, "2024", -1, 10000, None, float("nan"), float("inf")]:
                with self.subTest(name=name, value=value):
                    broken = copy.deepcopy(self.content)
                    broken[name][0]["year"] = value
                    self.reject(broken, ".year")
        validate_content(self.content)  # 1901 and 2099 are explicit editorial years.

    def test_ids_and_repository_names_reject_path_escape(self):
        for value in ["../private", "/absolute", "a/b", "a\\b", "a%2fb", "UPPER", "a\"x", "a b", "a\n"]:
            with self.subTest(value=value):
                broken = copy.deepcopy(self.content)
                broken["projects"][0]["id"] = value
                self.reject(broken, "projects.json[0].id")
        for value in ["../private", "a/b", "a\\b", "a?x", ".", "repo."]:
            with self.subTest(repo=value):
                broken = copy.deepcopy(self.content)
                broken["software"][0]["repo"] = value
                self.reject(broken, ".repo")

    def test_identifiers_doi_and_featured_lists_are_unique(self):
        for name in ["projects", "publications"]:
            broken = copy.deepcopy(self.content)
            broken[name].append(copy.deepcopy(broken[name][0]))
            self.reject(broken, name + ".json.id")
        broken = copy.deepcopy(self.content)
        extra = copy.deepcopy(broken["publications"][0])
        extra.update(id="second-study", doi=extra["doi"].upper())
        broken["publications"].append(extra)
        self.reject(broken, "publications.json.doi")
        for key in ["home_projects", "home_publications"]:
            broken = copy.deepcopy(self.content)
            broken["site"][key] *= 2
            self.reject(broken, key)

    def test_duplicate_auxiliary_records_are_rejected(self):
        for name, field in [("software", "repo"), ("working-papers", "url"), ("resources", "url")]:
            with self.subTest(name=name):
                broken = copy.deepcopy(self.content)
                broken[name].append(copy.deepcopy(broken[name][0]))
                self.reject(broken, name + ".json." + field)

    def test_featured_lists_cannot_be_empty_or_plain_text(self):
        for key in ["home_projects", "home_publications"]:
            for value in [[], "public-tool", [None]]:
                with self.subTest(key=key, value=value):
                    broken = copy.deepcopy(self.content)
                    broken["site"][key] = value
                    self.reject(broken, key)

    def test_reference_targets_and_catalogue_boundaries(self):
        for path, value in [("home_projects", "historical-study"), ("home_publications", "public-tool")]:
            broken = copy.deepcopy(self.content)
            broken["site"][path] = [value]
            self.reject(broken, path)
        for value in ["missing-project", "public-tool"]:
            broken = copy.deepcopy(self.content)
            broken["projects"][0]["related"] = value
            self.reject(broken, ".related")
        self.content["projects"][1]["doi"] = "10.1234/not-in-catalogue"
        self.reject(self.content, "projects.json[1].doi")

    def test_project_kinds_and_publication_topics_are_known(self):
        broken = copy.deepcopy(self.content)
        broken["projects"][0]["kind"] = "private-service"
        self.reject(broken, ".kind")
        self.content["publications"][0]["topic"] = "invented-topic"
        self.reject(self.content, ".topic")

    def test_project_evidence_required_by_kind(self):
        for index, field in [(0, "repo"), (1, "doi")]:
            broken = copy.deepcopy(self.content)
            del broken["projects"][index][field]
            self.reject(broken, "." + field)

    def test_translations_are_required_and_typed(self):
        for name, field in [("projects", "role"), ("publications", "summary"), ("software", "stage"), ("working-papers", "status")]:
            for value in [{"es": "Texto"}, {"es": "Texto", "en": ""}, {"es": "Texto", "en": []}, "Spanish-only fallback"]:
                with self.subTest(name=name, value=value):
                    broken = copy.deepcopy(self.content)
                    broken[name][0][field] = value
                    self.reject(broken, "." + field)
        self.content["projects"][0]["inspect"]["en"] = "A list is required"
        self.reject(self.content, ".inspect.en")

    def test_original_titles_and_technical_labels_are_preserved(self):
        before = copy.deepcopy(self.content)
        validate_content(self.content)
        self.assertEqual(self.content["projects"][0]["title"], "PUBLIC-TOOL")
        self.assertEqual(self.content, before)

    def test_author_parts_length_order_and_compound_surnames(self):
        broken = copy.deepcopy(self.content)
        broken["publications"][0]["author_parts"].reverse()
        self.reject(broken, ".author_parts[0]")
        broken["publications"][0]["author_parts"].pop()
        self.reject(broken, ".author_parts")
        validate_content(self.content)
        self.assertEqual(self.content["publications"][0]["author_parts"][0]["family"], "García López")

    def test_duplicate_authors_rejected_without_deduplication(self):
        self.content["publications"][0]["authors"].append("ana garci\u0301a lo\u0301pez")
        self.reject(self.content, ".authors[2]")
        broken = fixture()
        broken["working-papers"][0]["authors"] = "Ana García López; ana garcía lópez"
        self.reject(broken, ".authors[1]")

    def test_nested_unknown_fields_and_empty_authorship(self):
        broken = copy.deepcopy(self.content)
        broken["publications"][0]["author_parts"][0]["private"] = "DO_NOT_ECHO"
        self.reject(broken, ".author_parts[0]")
        broken = copy.deepcopy(self.content)
        broken["projects"][1]["additional_links"][0]["token"] = "DO_NOT_ECHO"
        self.reject(broken, ".additional_links[0]")
        broken = copy.deepcopy(self.content)
        broken["publications"][0]["authors"] = []
        self.reject(broken, ".authors")

    def test_urls_in_every_link_location_reject_credentials(self):
        paths = [("projects", "demo"), ("projects", "source"), ("software", "demo"), ("working-papers", "url"), ("working-papers", "pdf"), ("resources", "url"), ("resources", "pdf")]
        for name, field in paths:
            broken = copy.deepcopy(self.content)
            broken[name][0][field] = "https://private:DO_NOT_ECHO@example.org/"
            message = self.reject(broken, "." + field)
            self.assertNotIn("DO_NOT_ECHO", message)
            self.assertNotIn("private", message)
        self.content["publications"][0]["links"][0]["url"] = "javascript:DO_NOT_ECHO"
        message = self.reject(self.content, ".links[0].url")
        self.assertNotIn("DO_NOT_ECHO", message)

    def test_executable_relative_and_malformed_urls(self):
        values = ["javascript:alert(1)", "data:text/html,private", "file:///private", "http://example.org", "//example.org", "../file", "https://", "https://example.org\n/", "https://example.org/%0a", "https://example.org/%5cprivate", "https://example.org/%ZZ", "https://bad_host/", "https://example.org:99999/", "https://example.org/<tag>"]
        for value in values:
            with self.subTest(value=value):
                broken = copy.deepcopy(self.content)
                broken["resources"][0]["url"] = value
                self.reject(broken, ".url")

    def test_equal_years_and_reordered_lists_remain_editorial(self):
        extra = copy.deepcopy(self.content["publications"][0])
        extra.update(id="another-study", doi="10.1234/example.2")
        self.content["publications"].insert(0, extra)
        self.content["projects"].reverse()
        before = copy.deepcopy(self.content)
        validate_content(self.content)
        self.assertEqual(self.content, before)
        self.assertEqual([p["year"] for p in self.content["publications"]], [1901, 1901])

    def test_map_key_order_does_not_change_validity_or_values(self):
        def reverse_maps(value):
            if isinstance(value, dict):
                return {key: reverse_maps(value[key]) for key in reversed(value)}
            if isinstance(value, list):
                return [reverse_maps(item) for item in value]
            return value
        reordered = reverse_maps(self.content)
        validate_content(reordered)
        self.assertEqual(reordered, self.content)
        self.assertEqual(list(reordered), list(reversed(self.content)))

    def test_optional_catalogues_can_be_empty(self):
        for name in ["software", "working-papers", "resources"]:
            self.content[name] = []
        validate_content(self.content)

    def test_control_characters_do_not_enter_bibliography(self):
        for value in ["Title\n\nInjected entry", "Hidden\x00value", "Bad\ud800text"]:
            broken = copy.deepcopy(self.content)
            broken["publications"][0]["title"] = value
            self.reject(broken, ".title")


class SiteURLTests(unittest.TestCase):
    def test_safe_https_base_and_path_prefix(self):
        for value, expected in [("https://example.org/", "https://example.org"), ("https://example.org/team/site-v1/", "https://example.org/team/site-v1"), ("https://example.org:8443/site", "https://example.org:8443/site"), ("https://[2001:db8::1]/site/", "https://[2001:db8::1]/site")]:
            with self.subTest(value=value):
                self.assertEqual(validate_site_url(value), expected)

    def test_unsafe_bases_are_rejected_without_echo(self):
        values = [None, True, "https://name:DO_NOT_ECHO@example.org", "http://example.org", "https://example.org?token=DO_NOT_ECHO", "https://example.org#DO_NOT_ECHO", "https://example.org?", "https://example.org#", "https://example.org/a/../b", "https://example.org/./b", "https://example.org/%2e%2e/b", "https://example.org/%252e%252e/b", "https://example.org/a//b", "https://example.org//", "https://example.org/a\\b", "https://example.org/DO_NOT_ECHO\n", "https://[broken/"]
        for value in values:
            with self.subTest(value=value):
                with self.assertRaises(ContentError) as caught:
                    validate_site_url(value)
                self.assertIn("SITE_URL", str(caught.exception))
                self.assertNotIn("DO_NOT_ECHO", str(caught.exception))


class LoadingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "portfolio"
        self.expected = write_fixture(self.root)

    def rejected_load(self, field):
        with self.assertRaises(ContentError) as caught:
            load_content(self.root)
        self.assertIn(field, str(caught.exception))
        self.assertNotIn(str(self.root), str(caught.exception))
        self.assertNotIn("DO_NOT_ECHO", str(caught.exception))
        return str(caught.exception)

    def test_load_is_offline_read_only_and_order_preserving(self):
        before = {p.name: p.read_bytes() for p in (self.root / "data").iterdir()}
        with mock.patch.object(Path, "write_text", side_effect=AssertionError("write")), mock.patch.object(Path, "write_bytes", side_effect=AssertionError("write")), mock.patch.object(socket, "create_connection", side_effect=AssertionError("network")), mock.patch.object(socket, "getaddrinfo", side_effect=AssertionError("network")):
            actual = load_content(self.root)
        self.assertEqual(actual, self.expected)
        self.assertEqual(before, {p.name: p.read_bytes() for p in (self.root / "data").iterdir()})
        self.assertEqual(set(p.name for p in self.root.iterdir()), {"data"})

    def test_json_duplicate_keys_at_root_or_nested_are_rejected(self):
        target = self.root / "data/site.json"
        for text in ['{"DO_NOT_ECHO":1,"DO_NOT_ECHO":2}', '{"outer":{"DO_NOT_ECHO":1,"DO_NOT_ECHO":2}}']:
            with self.subTest(nested="outer" in text):
                target.write_text(text, encoding="utf8")
                message = self.rejected_load("data/site.json")
                self.assertIn("duplicate JSON", message)

    def test_nonfinite_json_constants_are_rejected(self):
        target = self.root / "data/site.json"
        for value in ["NaN", "Infinity", "-Infinity"]:
            with self.subTest(value=value):
                target.write_text('{"private":' + value + '}', encoding="utf8")
                self.assertIn("non-finite", self.rejected_load("data/site.json"))

    def test_malformed_json_and_invalid_utf8_are_sanitized(self):
        target = self.root / "data/site.json"
        target.write_text('{"DO_NOT_ECHO":broken}', encoding="utf8")
        self.rejected_load("data/site.json")
        target.write_bytes(b"\xffDO_NOT_ECHO")
        self.rejected_load("data/site.json")

    def test_missing_file_is_reported_without_absolute_path(self):
        (self.root / "data/resources.json").unlink()
        self.rejected_load("data/resources.json")

    def test_resolved_escape_fails_before_read_even_without_symlink_privilege(self):
        target = self.root / "data/site.json"
        outside = Path(self.temp.name) / "outside.json"
        outside.write_text("DO_NOT_ECHO", encoding="utf8")
        original_resolve, original_read = Path.resolve, Path.read_text

        def redirected(path, *args, **kwargs):
            return outside if path == target else original_resolve(path, *args, **kwargs)

        def guarded_read(path, *args, **kwargs):
            if path == outside:
                self.fail("An escaped file must never be read")
            return original_read(path, *args, **kwargs)

        with mock.patch.object(Path, "resolve", redirected), mock.patch.object(Path, "read_text", guarded_read):
            self.rejected_load("data/site.json")

    def test_file_symlink_escape_rejected(self):
        target = self.root / "data/site.json"
        outside = Path(self.temp.name) / "outside.json"
        outside.write_text(json.dumps(self.expected["site"]), encoding="utf8")
        target.unlink()
        try:
            target.symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest("Creating symlinks is not permitted on this host")
        self.rejected_load("data/site.json")
        self.assertTrue(outside.exists())

    def test_symlink_remaining_inside_data_can_be_read(self):
        target = self.root / "data/site.json"
        actual = target.with_name("site-source.json")
        target.rename(actual)
        try:
            target.symlink_to(actual)
        except (OSError, NotImplementedError):
            self.skipTest("Creating symlinks is not permitted on this host")
        self.assertEqual(load_content(self.root), self.expected)

    @unittest.skipUnless(os.name == "nt", "Windows junction regression")
    def test_data_directory_junction_escape_rejected(self):
        directory = self.root / "data"
        outside = Path(self.temp.name) / "outside-data"
        directory.rename(outside)
        result = subprocess.run(["cmd", "/c", "mklink", "/J", str(directory), str(outside)], capture_output=True)
        if result.returncode:
            outside.rename(directory)
            self.skipTest("Creating junctions is not permitted on this host")
        try:
            self.rejected_load("data")
            self.assertTrue((outside / "site.json").exists())
        finally:
            os.rmdir(directory)  # Remove the fixture junction itself, never its target.


if __name__ == "__main__":
    unittest.main()
