from pathlib import Path
from playwright.sync_api import sync_playwright
import json,os
ROOT=Path(__file__).resolve().parents[1]
QA=ROOT/'qa';QA.mkdir(exist_ok=True)
EXE=os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE')
BASE=os.environ.get('TEST_BASE_URL','http://127.0.0.1:8078').rstrip('/')+'/'
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,**({'executable_path':EXE} if EXE else {}))
 page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 for file in (ROOT/'public').rglob('index.html'):
  route=file.relative_to(ROOT/'public').as_posix().removesuffix('index.html')
  response=page.goto(BASE+route,wait_until='networkidle')
  assert response.status==200,route
  assert page.locator('h1').count()==1,route
  assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),route
  assert page.locator('img').evaluate_all('(els)=>els.every(i=>i.complete&&i.naturalWidth>0)'),route
 for route,name in [('', 'home'),('projects/','projects'),('publications/','publications'),('projects/sonar/','sonar'),('profile/','profile'),('lab/','lab'),('en/','home-en')]:
  page.goto(BASE+route,wait_until='networkidle');page.screenshot(path=str(QA/(name+'-desktop.png')),full_page=True)
 page.goto(BASE+'publications/',wait_until='networkidle')
 page.locator('#pub-search').fill('PNAS');assert page.locator('.publication:visible').count()==2
 page.locator('#pub-search').fill('National Academy');assert page.locator('.publication:visible').count()==2
 page.locator('#pub-search').fill('');page.locator('#pub-topic').select_option('networks');assert page.locator('.publication:visible').count()==1
 page.locator('#pub-year').select_option('2021');assert page.locator('#pub-empty').is_visible()
 page.locator('#pub-topic').select_option('');page.locator('#pub-year').select_option('');assert page.locator('.publication:visible').count()==12
 page.locator('#pub-search').fill('ZZZ-no-match');assert page.locator('#pub-empty').is_visible()
 page.goto(BASE+'lab/',wait_until='networkidle')
 assert '[0,1; 5,9]' in page.locator('#interval').inner_text(),page.locator('#interval').inner_text()
 page.locator('#sample').fill('20');page.locator('#sample').dispatch_event('input');assert 'incluye el cero' in page.locator('#interpretation').inner_text()
 page.locator('#noise').fill('40');page.locator('#effect').fill('15');page.locator('#effect').dispatch_event('input')
 assert page.locator('#ci-positive').text_content()=='+40'
 assert 30<float(page.locator('#ci-line').get_attribute('x2'))<470
 for width in [390,768]:
  page.set_viewport_size({'width':width,'height':844})
  for file in (ROOT/'public').rglob('index.html'):
   route=file.relative_to(ROOT/'public').as_posix().removesuffix('index.html');page.goto(BASE+route,wait_until='networkidle')
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),(width,route)
  for route,name in [('', 'home'),('publications/','publications'),('lab/','lab'),('projects/arco/','arco')]:
   page.goto(BASE+route,wait_until='networkidle');page.screenshot(path=str(QA/(name+f'-{width}.png')),full_page=True)
 page.set_viewport_size({'width':390,'height':844});page.goto(BASE,wait_until='networkidle')
 page.get_by_role('button',name='Menú',exact=True).click();assert page.locator('#navigation').is_visible()
 page.get_by_role('link',name='English',exact=True).click();assert '/en/' in page.url
 page.goto(BASE+'profile/');page.emulate_media(media='print');assert not page.locator('.site-header').is_visible();assert page.locator('h1').is_visible();page.emulate_media(media='screen')
 keyboard=browser.new_page();keyboard.goto(BASE);keyboard.keyboard.press('Tab');assert keyboard.locator('.skip').evaluate('(e)=>e===document.activeElement')
 assert not errors,errors
 # Core evidence remains available without JavaScript.
 context=browser.new_context(java_script_enabled=False);nojs=context.new_page()
 nojs.goto(BASE+'publications/');assert nojs.locator('.publication:visible').count()==12
 browser.close()
 (QA/'browser-results.json').write_text(json.dumps({'pages':24,'viewports':[1440,768,390],'publication_filter':True,'lab_calculation':True,'no_javascript':True,'page_errors':errors},indent=2),encoding='utf8')
 print('Browser checks passed: all routes, three viewport widths, filters, bilingual navigation, synthetic calculation and no-JavaScript content.')
