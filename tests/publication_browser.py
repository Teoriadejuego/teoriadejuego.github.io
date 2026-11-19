"""Publication search, language permalinks and mobile layout; no external navigation."""
import json
import os
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get('TEST_BASE_URL', 'http://127.0.0.1:8078').rstrip('/')


def main():
    with sync_playwright() as p:
        executable = os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE')
        browser = p.chromium.launch(headless=True, **({'executable_path': executable} if executable else {}))
        try:
            context = browser.new_context(viewport={'width': 320, 'height': 800}, service_workers='block')
            violations, errors = [], []
            def guard(route):
                request = route.request
                if urlsplit(request.url).netloc != urlsplit(BASE).netloc or request.method not in ('GET', 'HEAD'):
                    violations.append(request.url)
                    route.abort()
                else:
                    route.continue_()
            context.route('**/*', guard)
            page = context.new_page()
            page.on('pageerror', lambda error: errors.append(str(error)))
            records = []
            for language, prefix, group, topic_word in [('es', '', 'Filtrar artículos', 'redes'), ('en', '/en', 'Filter articles', 'networks')]:
                page.goto(BASE + prefix + '/publications/', wait_until='networkidle')
                assert page.get_by_role('group', name=group).count() == 1
                total = page.locator('.publication').count()
                page.locator('#pub-search').fill(topic_word)
                assert page.locator('.publication:visible').count() == 1
                assert page.locator('.publication:visible').get_attribute('id') == 'triadic'
                for label in ['BibTeX', 'Citar', 'Ficha institucional']:
                    page.locator('#pub-search').fill(label)
                    assert page.locator('.publication:visible').count() == 0
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
                page.locator('#pub-reset').click()
                years = page.locator('.publication').evaluate_all('xs=>[...new Set(xs.map(x=>x.dataset.year))].sort().reverse()')
                assert page.locator('#pub-year option').evaluate_all('xs=>xs.map(x=>x.value).filter(Boolean)') == years
                # This also exercises a future-year fixture without changing this test.
                for year in years:
                    page.locator('#pub-year').select_option(year)
                    assert page.locator('.publication:visible').count() > 0
                    assert page.locator('.publication:visible').evaluate_all('(xs)=>xs.every(x=>x.dataset.year===document.querySelector("#pub-year").value)')
                page.locator('#pub-reset').click()
                assert page.locator('.publication:visible').count() == total
                page.goto(BASE + prefix + '/publications/#private-solutions', wait_until='networkidle')
                article = page.locator('#private-solutions')
                assert article.evaluate('e=>getComputedStyle(e).outlineStyle') != 'none'
                assert article.locator('h2').get_attribute('lang') == 'en'
                assert article.locator('.publication-content').evaluate("e=>[...e.children].map(x=>x.className||x.tagName).slice(0,3)") == ['H2', 'venue', 'authors']
                assert article.locator('.authors strong').inner_text() == 'Antonio Alfonso'
                assert article.locator('.author-position').count() == 0
                # At narrow widths, the year starts where the title starts;
                # the decorative thumbnail sits on the other side of the row.
                assert abs(article.locator('.year').bounding_box()['x'] - article.locator('h2').bounding_box()['x']) < 1
                article.locator('summary').click()
                assert article.locator('.authors-list li').count() == 72
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
                assert article.get_by_role('link').count() == 2
                assert article.get_by_role('link', name='DOI', exact=True).count() == 1
                assert article.locator('.pub-links a').last.get_attribute('href').endswith('/pnas.202504632.pdf')
                term = 'cooperación' if language == 'es' else 'cooperation'
                page.locator('#pub-search').fill(term)
                assert article.is_visible()
                records.append({'language': language, 'years': years, 'topic_search': True, 'action_labels_excluded': True})
            nojs = browser.new_context(java_script_enabled=False, viewport={'width': 320, 'height': 800})
            nojs.route('**/*', guard)
            plain = nojs.new_page()
            plain.goto(BASE + '/publications/#triadic', wait_until='networkidle')
            assert plain.locator('#triadic').get_by_role('link').count() == 2
            assert plain.locator('#triadic .paper-keywords').is_visible()
            assert not errors, errors
            assert not violations, violations
            print(json.dumps({'publications': records, 'mobile_width': 320, 'no_js_links': True, 'page_errors': errors}))
        finally:
            browser.close()


if __name__ == '__main__':
    main()
