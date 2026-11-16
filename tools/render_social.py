"""Render code-native sharing cards with the existing supplied portrait; no image synthesis."""
from pathlib import Path
from base64 import b64encode
import os
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
photo='data:image/webp;base64,'+b64encode((ROOT/'assets/portrait-800.webp').read_bytes()).decode()
exe=os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE')
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,**({'executable_path':exe} if exe else {}))
 page=browser.new_page(viewport={'width':1200,'height':630},device_scale_factor=1)
 for lang,title,sub in [('es','Experimentos, datos y software.','Economista experimental · PhD'),('en','Experiments, data and software.','Experimental economist · PhD')]:
  html=f"""<!doctype html><html lang="{lang}"><meta charset="utf-8"><style>*{{box-sizing:border-box}}body{{margin:0;background:#10263e;color:white;font-family:Arial,sans-serif}}main{{height:630px;display:grid;grid-template-columns:1fr 310px;gap:60px;padding:65px 70px;align-items:center}}.name{{font-size:29px;margin:0 0 38px}}h1{{font-family:Georgia,serif;font-size:65px;line-height:1.12;font-weight:400;margin:0 0 30px}}.sub{{font-size:22px;color:#b8dfe0;margin:0}}.url{{font-size:19px;color:#d7e4eb;margin:36px 0 0}}img{{width:310px;height:390px;object-fit:cover;object-position:50% 35%;border-radius:4px 4px 20px 4px}}</style><main><div><p class="name">Antonio Alfonso</p><h1>{title}</h1><p class="sub">{sub}</p><p class="url">teoriadejuego.github.io</p></div><img src="{photo}" alt="Antonio Alfonso"></main></html>"""
  page.set_content(html,wait_until='load')
  page.screenshot(path=str(ROOT/f'assets/social-{lang}.jpg'),type='jpeg',quality=82)
 browser.close()
