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
 browser.close()
print('Round 3 browser checks passed.')
