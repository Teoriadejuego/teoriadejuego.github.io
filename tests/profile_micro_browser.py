"""Focused ES/EN profile, hiring and synthetic-lab checks; no external navigation."""
import json
import os
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from playwright.sync_api import sync_playwright

BASE = os.environ.get('TEST_BASE_URL', 'http://127.0.0.1:8078').rstrip('/')
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'qa/micro-100'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    errors = []
    with sync_playwright() as p:
        options = {'headless': True}
        if os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE'):
            options['executable_path'] = os.environ['PLAYWRIGHT_CHROMIUM_EXECUTABLE']
        browser = p.chromium.launch(**options)
        try:
            context = browser.new_context(viewport={'width': 1440, 'height': 1000})
            page = context.new_page()
            page.on('pageerror', lambda error: errors.append(str(error)))
            for lang, prefix in [('es', ''), ('en', '/en')]:
                page.goto(BASE + prefix + '/profile/')
                assert page.locator('h1').inner_text() == 'Antonio Alfonso Costillo'
                assert page.locator('.thesis-record a').get_attribute('href') == 'https://hdl.handle.net/10433/14568'
                assert page.locator('.principles').locator('a[href*="projects/teenslab/"]').count() == 1
                page.emulate_media(media='print')
                assert page.locator('.timeline li>div>p').first.evaluate('(el)=>getComputedStyle(el).breakAfter') == 'avoid'
                page.emulate_media(media='screen')
                page.goto(BASE + prefix + '/for-teams/')
                assert page.locator('.fit-grid').bounding_box()['y'] < page.locator('.hiring-facts').bounding_box()['y']
                emails = page.locator('a[href^="mailto:"]')
                for i in range(emails.count()):
                    href = urlsplit(emails.nth(i).get_attribute('href'))
                    assert href.path == 'aalfonsoc@gmail.com' and parse_qs(href.query).get('subject')

                page.goto(BASE + prefix + '/lab/')
                assert page.locator('.resource-group').count() == 3
                assert page.locator('.resource-list li').count() == 14
                assert page.locator('#interval').inner_text().endswith('points' if lang == 'en' else 'puntos')
                assert page.locator('#lab-reset').get_attribute('aria-describedby') == 'lab-reset-values'
                assert page.locator('.lab-inputs td').count() == page.locator('.lab-calculated td').count() == 3
                page.locator('.control-help summary').focus()
                page.keyboard.press('Enter')
                assert page.locator('.control-help').get_attribute('open') is not None
                page.locator('.lab-values summary').click()
                before = page.locator('#lab-se').inner_text().replace(',', '.')
                page.locator('#sample').fill('800')
                after = page.locator('#lab-se').inner_text().replace(',', '.')
                assert abs(float(before) / 2 - float(after)) < 0.011
                assert page.locator('#effect').input_value() == '3'
                for selector, value in [('#sample', '20'), ('#effect', '15'), ('#noise', '40')]:
                    page.locator(selector).fill(value)
                notice = page.locator('#lab-scale-note').inner_text()
                assert '30' in notice and '40' in notice and ('changed' if lang == 'en' else 'cambiado') in notice, notice
                page.locator('#lab-reset').click()
                assert page.locator('#sample').input_value() == '200'
                assert page.locator('#sample').evaluate('(el)=>el===document.activeElement')
                assert page.locator('#lab-scale-note').inner_text().count('40') == 1
                assert page.locator('[aria-live]').count() == 1

                for route in ('profile', 'for-teams', 'lab'):
                    for width in (320, 1440):
                        page.set_viewport_size({'width': width, 'height': 1000})
                        page.goto(BASE + prefix + '/' + route + '/')
                        if route == 'lab':
                            page.locator('.lab-values summary').click()
                            page.locator('.control-help summary').click()
                        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'), (lang, route, width)
                        page.evaluate('window.scrollTo(0, 0)')
                        page.screenshot(path=str(OUT / f'{route}-{lang}-{width}.png'), full_page=True)
                page.set_viewport_size({'width': 320, 'height': 1000})
                page.goto(BASE + prefix + '/lab/')
                page.locator('.lab-values summary').click()
                page.evaluate("""() => {
                    const sizes=[...document.querySelectorAll('body *')].map(el=>[el,parseFloat(getComputedStyle(el).fontSize)]);
                    for (const [el,size] of sizes) el.style.fontSize=(size*2)+'px';
                }""")
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'), (lang, 'text200')
                # Capture from the page origin: a tall element screenshot would
                # paint the sticky header over the element at its scrolled offset.
                page.evaluate('window.scrollTo(0, 0)')
                page.screenshot(path=str(OUT / f'lab-{lang}-320-text200.png'), full_page=True)
            context.close()
            assert not errors, errors
        finally:
            browser.close()
    print(json.dumps({'languages': ['es', 'en'], 'routes': ['profile', 'for-teams', 'lab'],
                      'viewports': [320, 1440], 'lab_text_percent': 200, 'javascript_errors': errors}))


if __name__ == '__main__':
    main()
