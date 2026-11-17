"""Read-only, offline validation of the portfolio's editorial inputs.

Validation never normalizes or reorders editorial data. Diagnostics use trusted
catalogue/field names and numeric record positions, never rejected values.
"""
from datetime import date
import ipaddress
import json
from pathlib import Path
import re
import unicodedata
from urllib.parse import unquote, urlsplit, urlunsplit


CATALOGUES = ("site", "projects", "publications", "software", "working-papers", "resources")
_SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
_REPO = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")
_DOI = re.compile(r"10\.\d{4,9}/[A-Za-z0-9._;()/:\-]+\Z", re.ASCII)
_TOPICS = {"experiments", "networks", "data", "behavior"}


class ContentError(ValueError):
    """An editorial input violates the published content contract."""


def _fail(path, message):
    raise ContentError(f"{path}: {message}") from None


def _object(value, path, required, optional=()):
    if type(value) is not dict:
        _fail(path, "expected an object")
    if set(value) - set(required) - set(optional):
        _fail(path, "unexpected field")
    for key in sorted(set(required) - set(value)):
        _fail(f"{path}.{key}", "required field is missing")


def _array(value, path, nonempty=False):
    if type(value) is not list or (nonempty and not value):
        _fail(path, "expected a nonempty list" if nonempty else "expected a list")


def _has_controls(value):
    return any(unicodedata.category(char) in {"Cc", "Cs"} for char in value)


def _text(value, path, allow_empty=False):
    if type(value) is not str:
        _fail(path, "expected text")
    if _has_controls(value):
        _fail(path, "control characters are not allowed")
    if not value.strip() and not (allow_empty and value == ""):
        _fail(path, "text must not be empty")


def _localized(value, path, allow_plain=False, lists=False):
    if allow_plain and type(value) is str:
        _text(value, path)
        return
    _object(value, path, {"es", "en"})
    for lang in ("es", "en"):
        field = f"{path}.{lang}"
        if lists:
            _array(value[lang], field, nonempty=True)
            for i, item in enumerate(value[lang]):
                _text(item, f"{field}[{i}]")
        else:
            _text(value[lang], field)


def _slug(value, path):
    _text(value, path)
    if not _SLUG.fullmatch(value):
        _fail(path, "expected a safe lowercase hyphenated identifier")


def _repo(value, path):
    _text(value, path)
    if not _REPO.fullmatch(value) or value.endswith("."):
        _fail(path, "expected a repository name without path separators")


def _doi(value, path):
    _text(value, path)
    if not _DOI.fullmatch(value):
        _fail(path, "expected a DOI identifier")


def _year(value, path):
    if type(value) is not int or not 1000 <= value <= 9999:
        _fail(path, "expected a four-digit integer year")


def _url(value, path):
    _text(value, path)
    if any(char.isspace() or char in "\\<>\"'`" for char in value):
        _fail(path, "expected a safe absolute HTTPS URL")
    try:
        parsed = urlsplit(value)
        host, port = parsed.hostname, parsed.port
        if parsed.scheme != "https" or not host or parsed.username is not None or parsed.password is not None:
            _fail(path, "expected HTTPS without embedded credentials")
        if port is not None and not 1 <= port <= 65535:
            _fail(path, "invalid URL port")
        if ":" in host:
            ipaddress.IPv6Address(host)
        else:
            ascii_host = host.encode("idna").decode("ascii")
            labels = ascii_host.split(".")
            if len(ascii_host) > 253 or any(not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?", label) for label in labels):
                _fail(path, "invalid URL host")
    except (ValueError, UnicodeError):
        _fail(path, "invalid HTTPS URL")
    decoded = unquote(value)
    if _has_controls(decoded) or "\\" in decoded:
        _fail(path, "encoded controls or backslashes are not allowed")
    if re.search(r"%(?![0-9A-Fa-f]{2})", value):
        _fail(path, "invalid URL encoding")
    return parsed


def validate_site_url(value: str) -> str:
    """Return an HTTPS base without a trailing slash, preserving a safe prefix."""
    parsed = _url(value, "SITE_URL")
    if "?" in value or "#" in value:
        _fail("SITE_URL", "query and fragment are not allowed")
    prefix = parsed.path.rstrip("/")
    if parsed.path.endswith("//") or (prefix and any(
        not re.fullmatch(r"[A-Za-z0-9_~.-]+", part) or part in {".", ".."}
        for part in prefix.split("/")[1:]
    )):
        _fail("SITE_URL", "unsafe path prefix")
    return urlunsplit(("https", parsed.netloc, prefix, "", ""))


def _normalized(value):
    return unicodedata.normalize("NFC", " ".join(value.split())).casefold()


def _unique(values, path, normalize=lambda value: value):
    seen = set()
    for i, value in enumerate(values):
        key = normalize(value)
        if key in seen:
            _fail(f"{path}[{i}]", "duplicate entry")
        seen.add(key)


def _links(value, path):
    _array(value, path)
    for i, item in enumerate(value):
        field = f"{path}[{i}]"
        _object(item, field, {"label", "url"})
        _localized(item["label"], field + ".label")
        _url(item["url"], field + ".url")


def validate_content(content: dict) -> None:
    """Validate all six catalogues, preserving their values and editorial order."""
    _object(content, "content", CATALOGUES)
    site = content["site"]
    _object(site, "data/site.json", {"schema_version", "updated", "home_projects", "home_publications"})
    if type(site["schema_version"]) is not int or site["schema_version"] != 1:
        _fail("data/site.json.schema_version", "expected integer schema version 1")
    _text(site["updated"], "data/site.json.updated")
    try:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", site["updated"], re.ASCII):
            raise ValueError
        date.fromisoformat(site["updated"])
    except ValueError:
        _fail("data/site.json.updated", "expected a valid ISO calendar date")
    for key in ("home_projects", "home_publications"):
        path = f"data/site.json.{key}"
        _array(site[key], path, nonempty=True)
        for i, value in enumerate(site[key]):
            _slug(value, f"{path}[{i}]")
        _unique(site[key], path)
    for name in CATALOGUES[1:]:
        _array(content[name], f"data/{name}.json")

    publications = content["publications"]
    for i, item in enumerate(publications):
        path = f"data/publications.json[{i}]"
        _object(item, path, {"id", "doi", "year", "topic", "title", "authors", "author_parts", "journal", "volume", "issue", "pages", "summary", "links"}, {"version"})
        _slug(item["id"], path + ".id")
        _doi(item["doi"], path + ".doi")
        _year(item["year"], path + ".year")
        _text(item["topic"], path + ".topic")
        if item["topic"] not in _TOPICS:
            _fail(path + ".topic", "unknown publication topic")
        for key in ("title", "journal"):
            _text(item[key], path + "." + key)
        for key in ("volume", "issue", "pages"):
            _text(item[key], path + "." + key, allow_empty=True)
        _localized(item["summary"], path + ".summary")
        if "version" in item:
            _localized(item["version"], path + ".version")
        _links(item["links"], path + ".links")
        _array(item["authors"], path + ".authors", nonempty=True)
        _array(item["author_parts"], path + ".author_parts", nonempty=True)
        for j, author in enumerate(item["authors"]):
            _text(author, f"{path}.authors[{j}]")
        _unique(item["authors"], path + ".authors", _normalized)
        if len(item["authors"]) != len(item["author_parts"]):
            _fail(path + ".author_parts", "must match the author list length and order")
        for j, author in enumerate(item["author_parts"]):
            field = f"{path}.author_parts[{j}]"
            _object(author, field, {"given", "family"})
            _text(author["given"], field + ".given")
            _text(author["family"], field + ".family")
            if author["given"] + " " + author["family"] != item["authors"][j]:
                _fail(field, "must exactly match the author at this position")
    _unique([p["id"] for p in publications], "data/publications.json.id")
    _unique([p["doi"] for p in publications], "data/publications.json.doi", str.casefold)

    projects = content["projects"]
    translated = {"heading", "summary", "status", "role", "problem", "work", "evidence", "value", "seo_title"}
    for i, item in enumerate(projects):
        path = f"data/projects.json[{i}]"
        _object(item, path, translated | {"id", "title", "kind", "tags", "inspect", "related"}, {"repo", "demo", "doi", "source", "additional_links"})
        _slug(item["id"], path + ".id")
        _slug(item["related"], path + ".related")
        _localized(item["title"], path + ".title", allow_plain=True)
        _text(item["kind"], path + ".kind")
        if item["kind"] not in {"software", "research"}:
            _fail(path + ".kind", "unknown project kind")
        required = "repo" if item["kind"] == "software" else "doi"
        if required not in item:
            _fail(path + "." + required, "required for this project kind")
        for key in sorted(translated):
            _localized(item[key], path + "." + key)
        _localized(item["inspect"], path + ".inspect", lists=True)
        _array(item["tags"], path + ".tags", nonempty=True)
        for j, tag in enumerate(item["tags"]):
            _localized(tag, f"{path}.tags[{j}]", allow_plain=True)
        if "repo" in item:
            _repo(item["repo"], path + ".repo")
        if "doi" in item:
            _doi(item["doi"], path + ".doi")
        for key in ("demo", "source"):
            if key in item:
                _url(item[key], path + "." + key)
        if "additional_links" in item:
            _links(item["additional_links"], path + ".additional_links")
    _unique([p["id"] for p in projects], "data/projects.json.id")
    project_ids = {p["id"] for p in projects}
    publication_ids = {p["id"] for p in publications}
    dois = {p["doi"].casefold() for p in publications}
    for i, item in enumerate(projects):
        if item["related"] not in project_ids or item["related"] == item["id"]:
            _fail(f"data/projects.json[{i}].related", "must reference another project")
        if "doi" in item and item["doi"].casefold() not in dois:
            _fail(f"data/projects.json[{i}].doi", "must reference a publication")
    for key, ids in (("home_projects", project_ids), ("home_publications", publication_ids)):
        for i, value in enumerate(site[key]):
            if value not in ids:
                _fail(f"data/site.json.{key}[{i}]", "unknown catalogue reference")

    for i, item in enumerate(content["software"]):
        path = f"data/software.json[{i}]"
        _object(item, path, {"title", "repo", "description", "stage"}, {"demo"})
        _localized(item["title"], path + ".title", allow_plain=True)
        _repo(item["repo"], path + ".repo")
        for key in ("description", "stage"):
            _localized(item[key], path + "." + key)
        if "demo" in item:
            _url(item["demo"], path + ".demo")
    _unique([p["repo"] for p in content["software"]], "data/software.json.repo", str.casefold)

    for i, item in enumerate(content["working-papers"]):
        path = f"data/working-papers.json[{i}]"
        _object(item, path, {"title", "year", "authors", "url", "status"}, {"pdf"})
        _text(item["title"], path + ".title")
        _year(item["year"], path + ".year")
        _text(item["authors"], path + ".authors")
        authors = item["authors"].split(";")
        for j, author in enumerate(authors):
            _text(author, f"{path}.authors[{j}]")
        _unique(authors, path + ".authors", _normalized)
        _localized(item["status"], path + ".status")
        _url(item["url"], path + ".url")
        if "pdf" in item:
            _url(item["pdf"], path + ".pdf")
    _unique([p["url"] for p in content["working-papers"]], "data/working-papers.json.url")
    for i, item in enumerate(content["resources"]):
        path = f"data/resources.json[{i}]"
        _object(item, path, {"title", "url"}, {"pdf"})
        _text(item["title"], path + ".title")
        _url(item["url"], path + ".url")
        if "pdf" in item:
            _url(item["pdf"], path + ".pdf")
    _unique([p["url"] for p in content["resources"]], "data/resources.json.url")


def load_content(root: Path) -> dict:
    """Load the six known JSON files below root/data, then validate them."""
    try:
        root = Path(root).resolve(strict=True)
        data_dir = root / "data"
        if data_dir.resolve(strict=True) != data_dir or not data_dir.is_dir():
            _fail("data", "editorial directory must not redirect outside its location")
    except (OSError, RuntimeError, ValueError):
        _fail("data", "editorial directory is unavailable or unsafe")
    result = {}
    for name in CATALOGUES:
        label = f"data/{name}.json"
        try:
            path = (data_dir / f"{name}.json").resolve(strict=True)
            if not path.is_relative_to(data_dir) or not path.is_file():
                _fail(label, "file must remain inside the editorial directory")
            text = path.read_text(encoding="utf-8")
        except (OSError, RuntimeError, UnicodeError, ValueError):
            _fail(label, "file is unavailable, unsafe or not UTF-8")

        def unique_object(pairs):
            obj = {}
            for key, value in pairs:
                if key in obj:
                    _fail(label, "duplicate JSON object key")
                obj[key] = value
            return obj

        def reject_constant(_value):
            _fail(label, "non-finite JSON constants are not allowed")

        try:
            result[name] = json.loads(text, object_pairs_hook=unique_object, parse_constant=reject_constant)
        except ContentError:
            raise
        except (ValueError, RecursionError):
            _fail(label, "invalid JSON document")
    validate_content(result)
    return result
