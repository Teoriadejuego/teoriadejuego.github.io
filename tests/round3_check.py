from pathlib import Path
import os, json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
BASE=os.environ.get('TEST_BASE_URL','http://127.0.0.1:8078')
EXE=os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE')
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,**({'executable_path':EXE} if EXE else {}))
 errors=[]
 page=browser.new_page(viewport={'width':740,'height':390})
 page.on('pageerror',lambda e:errors.append(str(e)))
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
 page.set_viewport_size({'width':1440,'height':900});page.goto(BASE+'/',wait_until='networkidle')
 page.locator('#navigation a').first.focus()
 page.set_viewport_size({'width':390,'height':844});page.wait_for_timeout(100)
 assert page.locator('.menu-toggle').evaluate('(e)=>e===document.activeElement')
 page.set_viewport_size({'width':1440,'height':900});page.wait_for_timeout(100)
 assert page.locator('#navigation a').first.evaluate('(e)=>e===document.activeElement')
 # The plotted width must narrow with n, widen with SD and reflect negative effects.
 page.goto(BASE+'/lab/',wait_until='networkidle')
 def width():return page.locator('#ci-line').evaluate('(e)=>Number(e.getAttribute("x2"))-Number(e.getAttribute("x1"))')
 initial=width();page.locator('#sample').fill('800');assert width()<initial
 narrow=width();page.locator('#noise').fill('30');assert width()>narrow
 page.locator('#effect').fill('-3');assert float(page.locator('#point').get_attribute('cx'))<250
 page.locator('#effect').fill('0');assert float(page.locator('#point').get_attribute('cx'))==250
 assert page.locator('#interval').inner_text().startswith('[')
 # Serve the absolute production asset URLs locally when inspecting the static 404.
 page.route('https://teoriadejuego.github.io/assets/**',lambda route:route.fulfill(path=str(ROOT/'public/assets'/route.request.url.rsplit('/',1)[-1])))
 page.goto(BASE+'/404.html',wait_until='networkidle')
 assert page.locator('h1').inner_text()=='Esta página no está aquí.'
 assert page.locator('main a').count()==5
 assert page.locator('meta[name="robots"]').get_attribute('content')=='noindex'
 page.screenshot(path=str(ROOT/'qa/404-r3.png'),full_page=True)
 # Enlarged text must not cause horizontal loss of content at the narrow supported width.
 page.set_viewport_size({'width':320,'height':844})
 for route in ['','for-teams/','projects/','publications/','profile/','lab/']:
  page.goto(BASE+'/'+route,wait_until='networkidle')
  page.add_style_tag(content='html{font-size:200%}')
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),('200% text overflow',route)
 # Verify both graphic alternatives, reduced motion and reproducible final screenshots.
 page.emulate_media(forced_colors='active',reduced_motion='reduce')
 page.goto(BASE+'/projects/pbis/',wait_until='networkidle')
 assert page.locator('html').evaluate('(e)=>getComputedStyle(e).scrollBehavior')=='auto'
 assert page.locator('.schematic path').evaluate('(e)=>getComputedStyle(e).vectorEffect')=='non-scaling-stroke'
 page.screenshot(path=str(ROOT/'qa/pbis-forced-colors-r3.png'),full_page=True)
 page.emulate_media(forced_colors='none',reduced_motion='no-preference')
 page.set_viewport_size({'width':1440,'height':1000})
 for route,name in [('', 'home'),('for-teams/','teams'),('publications/','publications'),('lab/','lab'),('projects/pbis/','pbis')]:
  page.goto(BASE+'/'+route,wait_until='networkidle')
  page.screenshot(path=str(ROOT/f'qa/{name}-desktop-r3.png'),full_page=True)
 # Decode the shipped assets instead of trusting the HTML size attributes.
 for thumbnail in sorted((ROOT/'public/assets').glob('thumb-*.webp')):
  dimensions = page.evaluate("""async url => {
    const image = new Image();
    image.src = url;
    await image.decode();
    return [image.naturalWidth, image.naturalHeight];
  }""", BASE+'/assets/'+thumbnail.name)
  assert dimensions == [224, 224], (thumbnail.name, dimensions)
 asset_bytes=sum(f.stat().st_size for f in (ROOT/'assets').iterdir() if f.is_file())
 assert asset_bytes<550000,asset_bytes
 assert not errors,errors
 (ROOT/'qa/round3-results.json').write_text(json.dumps({'asset_bytes':asset_bytes,'lab_url_sanitization':True,'breakpoint_focus':True,'text_200_percent_320px':True,'no_js_navigation':True,'404_local_asset_render':True,'forced_colors_and_reduced_motion':True,'errors':errors},indent=2),encoding='utf8')
 browser.close()
print('Round 3 browser checks passed.')
