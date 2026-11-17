"""Public-route, URL-state and privacy regression checks in a fresh browser.

Requests outside TEST_BASE_URL's origin and non-read methods are blocked and
reported as failures. Storage writes and cookies are checked across navigation.
The clipboard is stubbed before application code; it is never read or written.
"""
import json
import os
from urllib.parse import parse_qs, urlencode, urlsplit

from playwright.sync_api import sync_playwright

BASE = os.environ.get("TEST_BASE_URL", "http://127.0.0.1:8078").rstrip("/")
BROWSER = os.environ.get("PLAYWRIGHT_BROWSER", "chromium")


def origin(url):
    parts = urlsplit(url)
    return parts.scheme.lower(), (parts.hostname or "").lower(), parts.port or (443 if parts.scheme == "https" else 80)


INIT = """(() => {
  window.__portfolioStorageWrites = [];
  window.__portfolioClipboardCalls = 0;
  for (const name of ['setItem', 'removeItem', 'clear']) {
    const original = Storage.prototype[name];
    Storage.prototype[name] = function (...args) {
      window.__portfolioStorageWrites.push(name);
      return original.apply(this, args);
    };
  }
  const cookie = Object.getOwnPropertyDescriptor(Document.prototype, 'cookie');
  if (cookie && cookie.set && cookie.get) {
    Object.defineProperty(Document.prototype, 'cookie', {
      configurable: cookie.configurable, enumerable: cookie.enumerable,
      get: cookie.get,
      set(value) {
        window.__portfolioStorageWrites.push('cookie');
        return cookie.set.call(this, value);
      }
    });
  }
  Object.defineProperty(navigator, 'clipboard', {
    configurable: true,
    value: { writeText: async () => {
      window.__portfolioClipboardCalls += 1;
      throw new Error('Clipboard blocked in privacy test');
    }}
  });
})();"""


def check_storage(page, context):
    state = page.evaluate("""() => ({
      local: localStorage.length, session: sessionStorage.length,
      cookie: document.cookie, writes: window.__portfolioStorageWrites,
      clipboard: window.__portfolioClipboardCalls
    })""")
    assert state == {"local": 0, "session": 0, "cookie": "", "writes": [], "clipboard": 0}, state
    assert context.cookies() == [], "The portfolio set a browser cookie"
    assert page.evaluate("window.__portfolioXss === undefined"), "Search text was executed"


def query(page):
    return parse_qs(urlsplit(page.url).query, keep_blank_values=True)


def main():
    if BROWSER not in ("chromium", "firefox"):
        raise ValueError("PLAYWRIGHT_BROWSER must be chromium or firefox")
    if origin(BASE)[0] not in ("http", "https"):
        raise ValueError("TEST_BASE_URL must use HTTP or HTTPS")
    allowed = origin(BASE)
    requests, violations, errors, visited = [], [], [], set()
    with sync_playwright() as p:
        options = {"headless": True}
        executable = os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
        if BROWSER == "chromium" and executable:
            options["executable_path"] = executable
        browser = getattr(p, BROWSER).launch(**options)
        try:
            context = browser.new_context(service_workers="block")
            def guard(route):
                request = route.request
                item = {"method": request.method, "url": request.url, "type": request.resource_type}
                requests.append(item)
                if origin(request.url) != allowed or request.method not in ("GET", "HEAD"):
                    violations.append(item)
                    route.abort()
                else:
                    route.continue_()
            context.route("**/*", guard)
            def block_socket(socket):
                violations.append({"type": "websocket", "url": socket.url})
                # No connection to a remote server is opened by this route.
                socket.close(code=1008, reason="WebSocket traffic is not used by this portfolio")
            context.route_web_socket("**/*", block_socket)
            context.add_init_script(INIT)
            page = context.new_page()
            page.on("pageerror", lambda error: errors.append(str(error)))

            def visit(url):
                assert origin(url) == allowed, "Test would leave the public origin"
                response = page.goto(url, wait_until="networkidle")
                assert response and response.status == 200, (url, response.status if response else None)
                visited.add(urlsplit(page.url).path)
                check_storage(page, context)

            for lang in ("es", "en"):
                root = BASE + ("/en/" if lang == "en" else "/")
                visit(root)
                # Follow every current public project without opening external evidence.
                visit(root + "projects/")
                cases = page.locator(".work h3 a").evaluate_all("xs=>xs.map(a=>a.href)")
                assert cases, "No project evidence routes"
                for url in cases:
                    visit(url)
                    assert page.locator(".case-aside p").inner_text().strip()
                    assert page.locator(".case-actions a").count() > 0

                visit(root + "publications/?topic=invalid&year=1900&campaign=one&campaign=two#triadic")
                total = page.locator(".publication").count()
                assert total > 0 and page.locator(".publication:visible").count() == total
                assert page.locator("#pub-topic").input_value() == page.locator("#pub-year").input_value() == ""
                assert not page.locator("#pub-reset").is_visible()
                assert query(page) == {"campaign": ["one", "two"]}
                assert urlsplit(page.url).fragment == "triadic"

                # User text stays an inert input value even after reload; a bad
                # implementation would attempt a blocked external image request.
                payload = '<img data-portfolio-xss src="https://privacy-probe.invalid/pixel" onerror="window.__portfolioXss=1">'
                visit(root + "publications/?" + urlencode({"q": payload, "campaign": "privacy-check"}) + "#triadic")
                assert page.locator("#pub-search").input_value() == payload
                assert page.locator("img[data-portfolio-xss]").count() == 0
                assert page.locator("#pub-empty").is_visible()
                assert page.locator(".publication:visible").count() == 0
                count = len(requests)
                page.locator("#pub-search").fill("__portfolio_no_match__")
                page.locator("#pub-reset").click()
                assert page.locator(".publication:visible").count() == total
                assert not page.locator("#pub-empty").is_visible()
                assert page.locator("#pub-search").evaluate("e=>e===document.activeElement")
                assert query(page) == {"campaign": ["privacy-check"]}
                page.wait_for_timeout(100)
                assert len(requests) == count, "Filtering sent a network request"
                check_storage(page, context)

                visit(root + "publications/?q=triadic&topic=networks&year=2023&campaign=one&campaign=two#triadic")
                assert page.locator(".publication:visible").count() == 1
                page.locator("a.lang").click()
                page.wait_for_load_state("networkidle")
                assert page.locator(".publication:visible").get_attribute("id") == "triadic"
                assert query(page) == {"q": ["triadic"], "topic": ["networks"], "year": ["2023"], "campaign": ["one", "two"]}
                assert urlsplit(page.url).fragment == "triadic"
                check_storage(page, context)
                # Real history traversal through an invalid state exercises popstate.
                invalid = "?topic=invalid&year=1900&campaign=one&campaign=two#triadic"
                page.evaluate("q=>{history.pushState(null,'',q);history.pushState(null,'','?q=triadic#triadic')}", invalid)
                page.go_back(wait_until="load")
                page.wait_for_function("document.querySelector('#pub-topic').value==='' && !location.search.includes('topic=')")
                assert query(page) == {"campaign": ["one", "two"]}
                assert page.locator(".publication:visible").count() == total
                assert not page.locator("#pub-reset").is_visible()
                assert urlsplit(page.url).fragment == "triadic"
                check_storage(page, context)

                visit(root + "lab/?n=20&delta=-5&sd=8#demo")
                count = len(requests)
                for selector, value in (("#sample", "800"), ("#effect", "0"), ("#noise", "40")):
                    page.locator(selector).fill(value)
                page.locator("#lab-reset").click()
                page.wait_for_timeout(100)
                assert len(requests) == count, "The synthetic laboratory sent a network request"
                check_storage(page, context)

                visit(root + "for-teams/")
                evidence = page.locator(".fit-grid article>a").evaluate_all("xs=>xs.map(a=>a.href)")
                assert len(evidence) == 3
                for url in evidence:
                    visit(url)
                    assert page.locator(".case-actions a").count() > 0
                    # Inspect public link schemes without contacting outside services.
                    for href in page.locator(".case-actions a").evaluate_all("xs=>xs.map(a=>a.href)"):
                        assert origin(href) == allowed or urlsplit(href).scheme == "https", href
                for suffix in ("profile/", "privacy/"):
                    visit(root + suffix)
            # Two live, independent contexts must not share URL/filter state.
            isolated_contexts, isolated_pages = [], []
            try:
                for _ in range(2):
                    isolated = browser.new_context(service_workers="block")
                    isolated_contexts.append(isolated)
                    isolated.route("**/*", guard)
                    isolated.route_web_socket("**/*", block_socket)
                    isolated.add_init_script(INIT)
                    isolated_page = isolated.new_page()
                    isolated_page.on("pageerror", lambda error: errors.append(str(error)))
                    isolated_pages.append(isolated_page)
                for isolated_page, isolated, suffix in zip(isolated_pages, isolated_contexts, ("?q=PNAS", "?topic=networks")):
                    response = isolated_page.goto(BASE + "/publications/" + suffix, wait_until="networkidle")
                    assert response and response.status == 200
                    check_storage(isolated_page, isolated)
                first, second = isolated_pages
                assert first.locator("#pub-search").input_value() == "PNAS"
                assert second.locator("#pub-topic").input_value() == "networks"
                def filter_state(target):
                    return {"url": target.url, **target.evaluate("""() => ({
                      search:document.querySelector('#pub-search').value,
                      topic:document.querySelector('#pub-topic').value,
                      year:document.querySelector('#pub-year').value,
                      visible:[...document.querySelectorAll('.publication')].filter(e=>!e.hidden).map(e=>e.id)
                    })""")}
                count = len(requests)
                second_before = filter_state(second)
                first.locator("#pub-search").fill("__isolated_context_no_match__")
                assert first.locator(".publication:visible").count() == 0
                first.wait_for_timeout(100)
                assert filter_state(second) == second_before, "First context changed the second context"
                first_before = filter_state(first)
                second.locator("#pub-reset").click()
                assert second.locator(".publication:visible").count() == second.locator(".publication").count()
                second.wait_for_timeout(100)
                assert filter_state(first) == first_before, "Second context changed the first context"
                assert len(requests) == count, "Isolated filter interactions sent network requests"
                for isolated_page, isolated in zip(isolated_pages, isolated_contexts):
                    check_storage(isolated_page, isolated)
            finally:
                for isolated in isolated_contexts:
                    isolated.close()
            assert not violations, violations
            assert not errors, errors
            assert requests and all(r["method"] in ("GET", "HEAD") for r in requests)
        finally:
            browser.close()
    print(json.dumps({"browser": BROWSER, "public_routes": sorted(visited), "requests": len(requests), "outside_origin_or_mutable_attempts": violations, "storage_writes": 0, "clipboard_calls": 0, "filter_recovery_and_language": True, "simultaneous_context_isolation": {"contexts": 2, "directions_checked": 2, "state": ["url", "search", "topic", "year", "visible_articles"]}, "javascript_errors": errors}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
