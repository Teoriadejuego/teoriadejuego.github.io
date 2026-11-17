"""Independent numerical and representation checks for the synthetic lab.

Run against a built, served site. No build, clipboard, external service or file
output is performed. PLAYWRIGHT_BROWSER supports chromium (default) or firefox.
"""
import json
import math
import os
import re
from urllib.parse import parse_qs, urlencode, urlsplit

from playwright.sync_api import sync_playwright

BASE = os.environ.get("TEST_BASE_URL", "http://127.0.0.1:8078").rstrip("/")
BROWSER = os.environ.get("PLAYWRIGHT_BROWSER", "chromium")
CELLS = ("lab-n", "lab-delta", "lab-sd", "lab-se", "lab-lower", "lab-upper")
# Expected axis limits are explicit fixtures, not extracted from the application.
CASES = (
    (200, 3, 15, 20), (200, -3, 15, 20), (200, 0, 15, 20),
    (20, 15, 40, 40), (20, -15, 40, 40), (2000, 15, 5, 20),
    (20, 5, 8, 20), (20, -5, 8, 20),
    (1400, 2, 27, 20),  # lower bound is slightly negative, about -0.000188
    (1300, 1, 13, 20),  # lower bound is slightly positive, about 0.000592
)


def numeric(text, lang):
    value = text.strip().replace("\u2212", "-").replace("\xa0", "")
    value = value.replace(".", "").replace(",", ".") if lang == "es" else value.replace(",", "")
    return float(value)


def rounded_value(text, expected, lang, digits=None):
    separator = "," if lang == "es" else "."
    decimals = len(text.rsplit(separator, 1)[1]) if separator in text else 0
    if digits is not None:
        assert decimals == digits, ("decimal places", text, digits)
    assert math.isclose(numeric(text, lang), expected, rel_tol=0, abs_tol=0.5 * 10 ** -decimals + 1e-10), (text, expected)
    # Rounding must never erase the direction of a near-zero nonzero bound.
    if expected != 0:
        assert numeric(text, lang) * expected > 0, ("lost sign", text, expected)


def inspect_case(page, lang, n, delta, sd, axis_limit):
    # Independent route: standard errors of separate means combined by hypot.
    group_se = sd / math.sqrt(n)
    se = math.hypot(group_se, group_se)
    lo, hi = delta - 1.96 * se, delta + 1.96 * se
    assert [float(page.locator(selector).input_value()) for selector in ("#sample", "#effect", "#noise")] == [n, delta, sd]
    values = {cell: page.locator("#" + cell).text_content().strip() for cell in CELLS}
    assert numeric(values["lab-n"], lang) == n  # n per group, not total sample size
    assert numeric(values["lab-delta"], lang) == delta
    assert numeric(values["lab-sd"], lang) == sd
    rounded_value(values["lab-se"], se, lang, 2)
    rounded_value(values["lab-lower"], lo, lang)
    rounded_value(values["lab-upper"], hi, lang)

    interval = page.locator("#interval").inner_text()
    match = re.fullmatch(r"\[([^;]+); ([^\]]+)\]", interval)
    assert match, interval
    assert match.groups() == (values["lab-lower"], values["lab-upper"])
    title = page.locator("#chart-title").text_content()
    assert values["lab-lower"] in title and values["lab-upper"] in title and values["lab-delta"] in title
    assert page.locator(".demo-chart").get_attribute("aria-labelledby") == "chart-title"
    assert values["lab-delta"] in page.locator("#estimate").inner_text()
    assert values["lab-n"] == page.locator("#sample-value").inner_text()
    assert values["lab-delta"] == page.locator("#effect-value").inner_text()
    assert values["lab-sd"] == page.locator("#noise-value").inner_text()

    expected_words = (
        ("below zero" if hi < 0 else "above zero" if lo > 0 else "includes zero")
        if lang == "en" else
        ("debajo de cero" if hi < 0 else "encima de cero" if lo > 0 else "incluye el cero")
    )
    assert expected_words in page.locator("#interpretation").inner_text(), (n, delta, sd, expected_words)
    assert numeric(page.locator("#ci-positive").text_content(), lang) == axis_limit
    assert numeric(page.locator("#ci-negative").text_content(), lang) == -axis_limit
    # Convert plot positions back to data using the actual labelled tick positions.
    left = float(page.locator("#ci-negative").get_attribute("x"))
    right = float(page.locator("#ci-positive").get_attribute("x"))
    x1 = float(page.locator("#ci-line").get_attribute("x1"))
    x2 = float(page.locator("#ci-line").get_attribute("x2"))
    point = float(page.locator("#point").get_attribute("cx"))
    def from_plot(x):
        return -axis_limit + (x - left) / (right - left) * 2 * axis_limit
    for actual, expected in ((from_plot(x1), lo), (from_plot(x2), hi), (from_plot(point), delta)):
        assert math.isclose(actual, expected, rel_tol=0, abs_tol=1e-10), (actual, expected)
    assert left <= x1 <= point <= x2 <= right, (x1, point, x2, axis_limit)
    assert math.isclose(point, (x1 + x2) / 2, abs_tol=1e-10)
    return {"n_per_group": n, "delta": delta, "sd": sd, "se": se, "lower": lo, "upper": hi, "axis_limit": axis_limit}


def main():
    if BROWSER not in ("chromium", "firefox"):
        raise ValueError("PLAYWRIGHT_BROWSER must be chromium or firefox")
    results, errors = [], []
    with sync_playwright() as p:
        options = {"headless": True}
        executable = os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
        if BROWSER == "chromium" and executable:
            options["executable_path"] = executable
        browser = getattr(p, BROWSER).launch(**options)
        try:
            page = browser.new_page()
            page.on("pageerror", lambda error: errors.append(str(error)))
            for lang in ("es", "en"):
                route = BASE + ("/en" if lang == "en" else "") + "/lab/"
                for case in CASES:
                    n, delta, sd, axis = case
                    page.goto(route + "?" + urlencode({"n": n, "delta": delta, "sd": sd}), wait_until="networkidle")
                    results.append({"language": lang, **inspect_case(page, lang, *case)})
                    details = page.locator("#lab-n").locator("xpath=ancestor::details")
                    assert details.count() == 1
                    assert details.locator("table").count() == 1
                    assert details.locator('[aria-live], [role="status"], [role="alert"]').count() == 0
                # Native keyboard disclosure; no extra live region for table updates.
                summary = details.locator("summary")
                summary.focus()
                page.keyboard.press("Enter")
                assert details.get_attribute("open") is not None
                assert page.locator("#lab-n").is_visible()
                assert page.locator('.demo-results[role="status"]').count() == 1
                page.keyboard.press("Enter")
                assert details.get_attribute("open") is None

                for query, case in (
                    ("n=Infinity&delta=NaN&sd=-100", (200, 3, 5, 20)),
                    ("n=99999&delta=-999&sd=999", (2000, -15, 40, 20)),
                    ("n=21&delta=0.26&sd=5.5", (20, 0.5, 6, 20)),
                ):
                    page.goto(route + "?" + query + "#demo", wait_until="networkidle")
                    inspect_case(page, lang, *case)
                    actual = parse_qs(urlsplit(page.url).query)
                    for key, value, default in zip(("n", "delta", "sd"), case[:3], (200, 3, 15)):
                        assert actual.get(key) == ([str(value)] if value != default else None)

                # Changing controls updates every representation without adding history entries.
                page.goto(route + "?n=20&delta=-5&sd=8#demo", wait_until="networkidle")
                length = page.evaluate("history.length")
                page.locator("#effect").fill("5")
                inspect_case(page, lang, 20, 5, 8, 20)
                assert page.evaluate("history.length") == length
                page.locator("a.lang").click()
                page.wait_for_load_state("networkidle")
                other = "en" if lang == "es" else "es"
                inspect_case(page, other, 20, 5, 8, 20)
                assert urlsplit(page.url).fragment == "demo"
                page.locator("#lab-reset").click()
                inspect_case(page, other, 200, 3, 15, 20)
                assert not urlsplit(page.url).query
                assert page.locator("#sample").evaluate("e=>e===document.activeElement")
                # History traversal reloads the controls and table from the restored URL.
                page.goto(route + "?n=20&delta=-5&sd=8#demo", wait_until="networkidle")
                page.evaluate("history.pushState(null,'','?n=800&delta=0&sd=15#demo')")
                for selector, value in (("#sample", "800"), ("#effect", "0"), ("#noise", "15")):
                    page.locator(selector).fill(value)
                inspect_case(page, lang, 800, 0, 15, 20)
                page.go_back(wait_until="load")
                page.wait_for_function("document.querySelector('#sample').value==='20'")
                inspect_case(page, lang, 20, -5, 8, 20)
            assert not errors, errors
        finally:
            browser.close()
    print(json.dumps({"browser": BROWSER, "cases": results, "url_and_keyboard_checks": True, "javascript_errors": errors}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
