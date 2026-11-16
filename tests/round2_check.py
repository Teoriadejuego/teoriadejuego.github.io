"""Regression checks for second-round improvements; never writes the OS clipboard."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json, os

ROOT=Path(__file__).resolve().parents[1]
BASE=os.environ.get('TEST_BASE_URL','http://127.0.0.1:8078').rstrip('/')+'/'
EXE=os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE')
AXE=os.environ.get('AXE_SCRIPT')
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,**({'executable_path':EXE} if EXE else {}))
 page=browser.new_page(viewport={'width':1440,'height':1000})
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(BASE+'publications/?q=PNAS&year=2023&topic=networks#triadic',wait_until='networkidle')
 assert page.locator('.publication:visible').count()==1
 page.locator('a.lang').click();page.wait_for_load_state('networkidle')
 assert '/en/publications/' in page.url and 'q=PNAS' in page.url and '#triadic' in page.url
 assert page.locator('#pub-year').input_value()=='2023'
 assert page.locator('#pub-topic').input_value()=='networks'
 assert page.locator('.publication:visible').count()==1
 page.locator('#pub-reset').click()
 assert '?' not in page.locator('a.lang').get_attribute('href')
 page.locator('#private-solutions summary').click()
 assert page.locator('#private-solutions .authors-list li').count()==72
 for item in json.loads((ROOT/'data/publications.json').read_text(encoding='utf8')):
  bib=(ROOT/'public/downloads'/(item['id']+'.bib')).read_text(encoding='utf8')
  assert item['doi'] in bib and item['title'] in bib
  assert all(author['family']+', '+author['given'] in bib for author in item['author_parts'])
 page.goto(BASE+'for-teams/',wait_until='networkidle')
 assert page.locator('.nav [aria-current="page"]').inner_text()=='Para equipos'
 assert page.locator('.fit-grid h3').count()==3 and page.locator('.fit-grid h2').count()==0
 # Stubbing prevents access to the user's real Windows clipboard.
 page.evaluate("Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async value=>{window.copiedEmail=value}}})")
 page.locator('[data-copy-email]').click()
 assert page.evaluate('window.copiedEmail')=='aalfonsoc@gmail.com'
 assert page.locator('.copy-status').inner_text()=='Correo copiado.'
 page.evaluate("Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async()=>{throw new Error('simulated denial')}}})")
 page.locator('[data-copy-email]').click()
 assert 'Selecciona la dirección' in page.locator('.copy-status').inner_text()
 assert page.locator('.contact-link').get_attribute('href')=='mailto:aalfonsoc@gmail.com'
 page.goto(BASE+'lab/',wait_until='networkidle')
 for selector,value in [('#sample','20'),('#noise','8'),('#effect','5')]:
  page.locator(selector).fill(value);page.locator(selector).dispatch_event('input')
 assert '0,04' in page.locator('#interval').inner_text()
 assert 'encima de cero' in page.locator('#interpretation').inner_text()
 page.locator('#effect').fill('-5');page.locator('#effect').dispatch_event('input')
 assert '-0,04' in page.locator('#interval').inner_text()
 assert 'debajo de cero' in page.locator('#interpretation').inner_text()
 assert page.locator('.resource-group').count()==2 and page.locator('.resource-list li').count()==14
 for width in [320,810]:
  page.set_viewport_size({'width':width,'height':900})
  for file in (ROOT/'public').rglob('index.html'):
   route=file.relative_to(ROOT/'public').as_posix().removesuffix('index.html')
   page.goto(BASE+route,wait_until='networkidle')
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,route)
 page.set_viewport_size({'width':1440,'height':1000})
 page.goto(BASE,wait_until='networkidle')
 assert len(set(page.locator('.work .visual').evaluate_all('(els)=>els.map(e=>Math.round(e.getBoundingClientRect().height))')))==1
 for route,name in [('', 'home'),('for-teams/','for-teams'),('projects/pbis/','pbis'),('publications/','publications')]:
  page.goto(BASE+route,wait_until='networkidle')
  page.screenshot(path=str(ROOT/'qa'/f'{name}-desktop-r2.png'),full_page=True)
 page.goto(BASE+'profile/',wait_until='networkidle')
 assert not page.locator('.print-source').is_visible()
 page.emulate_media(media='print');assert page.locator('.print-source').is_visible()
 assert not page.locator('#contact').is_visible()
 assert page.locator('.section.tint').evaluate("e=>getComputedStyle(e).backgroundColor")=='rgb(255, 255, 255)'
 assert BASE not in page.locator('.print-source').inner_text()
 page.screenshot(path=str(ROOT/'qa/profile-print-r2.png'),full_page=True)
 page.emulate_media(media='screen')
 context=browser.new_context(java_script_enabled=False);nojs=context.new_page()
 nojs.goto(BASE+'publications/',wait_until='networkidle')
 assert not nojs.locator('.filters').is_visible()
 assert nojs.locator('.publication:visible').count()==12
 nojs.goto(BASE+'lab/',wait_until='networkidle')
 nojs.locator('.resource-group summary').first.click()
 assert nojs.locator('.resource-list li:visible').count()==9
 axe_results=[]
 if AXE:
  for route in ['', 'for-teams/','publications/','projects/pbis/','lab/','profile/','en/for-teams/']:
   page.goto(BASE+route,wait_until='networkidle');page.add_script_tag(path=AXE)
   results=page.evaluate("async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})")
   axe_results.append({'route':route,'violations':results['violations']})
   assert not results['violations'],(route,results['violations'])
 assert not errors,errors
 assert sum(f.stat().st_size for f in (ROOT/'assets').iterdir() if f.is_file())<550000
 browser.close()
 (ROOT/'qa/round2-results.json').write_text(json.dumps({'extra_viewports':[320,810],'clipboard':'success and rejection tested with stub','near_zero_intervals':True,'language_state':True,'individual_bibtex':12,'axe':axe_results,'errors':errors},ensure_ascii=False,indent=2),encoding='utf8')
 print('Round 2 checks passed: locale state, 12 citations, clipboard stub, near-zero bounds, print, no-JS, 320/810px, asset budget and optional axe.')
