from pathlib import Path
import os, json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
BASE=os.environ.get('TEST_BASE_URL','http://127.0.0.1:8078')
EXE=os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE',r'C:/Users/aalfo/AppData/Local/ms-playwright/chromium_headless_shell-1234/chrome-headless-shell-win64/chrome-headless-shell.exe')
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=EXE)
 page=browser.new_page(viewport={'width':740,'height':390})
 page.goto(BASE+'/projects/arco/',wait_until='networkidle')
 assert page.locator('.site-header').evaluate('(e)=>getComputedStyle(e).position')=='relative'
 assert page.locator('.case-aside').evaluate('(e)=>getComputedStyle(e).position')=='static'
 assert page.locator('.case-top').get_attribute('data-project')=='arco'
 assert page.locator('.case-top .visual').evaluate('(e)=>getComputedStyle(e).backgroundColor')=='rgb(233, 243, 241)'
 nojs=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
 np=nojs.new_page();np.goto(BASE+'/',wait_until='networkidle')
 assert not np.locator('.menu-toggle').is_visible()
 assert np.locator('#navigation').is_visible()
 nojs.close()
 page.goto(BASE+'/lab/?n=Infinity&delta=NaN&sd=-100#demo',wait_until='networkidle')
 assert [page.locator('#'+x).input_value() for x in ['sample','effect','noise']]==['200','3','5']
 page.goto(BASE+'/lab/?n=99999&delta=-999&sd=999',wait_until='networkidle')
 assert [page.locator('#'+x).input_value() for x in ['sample','effect','noise']]==['2000','-15','40']
 page.goto(BASE+'/lab/?n=21&delta=0.26&sd=5.5#demo',wait_until='networkidle')
 assert [page.locator('#'+x).input_value() for x in ['sample','effect','noise']]==['20','0.5','6']
 before=page.evaluate('history.length')
 page.locator('#effect').fill('2.5')
 assert page.evaluate('history.length')==before
 href=page.locator('a.lang').get_attribute('href');assert 'delta=2.5' in href and '#demo' in href
 page.goto(href,wait_until='networkidle');assert page.locator('#effect').input_value()=='2.5'
 page.locator('#lab-reset').click();assert '?' not in page.url
 assert page.locator('#sample').evaluate('(e)=>e===document.activeElement')
 browser.close()
print('Round 3 browser checks passed.')
