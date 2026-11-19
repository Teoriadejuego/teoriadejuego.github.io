from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote,urlunsplit
import json,os,sys
PROJECT_ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT_ROOT))
from tools.content_contract import load_content,validate_site_url
from tools.release import expected_paths
CONTENT=load_content(PROJECT_ROOT)
BASE=validate_site_url(os.environ.get('SITE_URL','https://teoriadejuego.github.io'))
BASE_URL=urlsplit(BASE);BASE_PATH=BASE_URL.path.rstrip('/')+'/'
ROOT=Path(os.environ.get('PORTFOLIO_OUTPUT_DIR',str(PROJECT_ROOT/'public'))).resolve()
EXPECTED=expected_paths(CONTENT)
PUB_COUNT=len(CONTENT['publications']); PAGE_COUNT=2*(7+len(CONTENT['projects']))
def all_urls(value):
 if isinstance(value,str):return {value} if value.startswith('https://') else set()
 if isinstance(value,dict):return set().union(*(all_urls(v) for v in value.values()))
 if isinstance(value,list):return set().union(*(all_urls(v) for v in value))
 return set()
APPROVED_EXTERNAL={urlunsplit((*urlsplit(u)[:4],'')) for u in all_urls(CONTENT)}
class Page(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set();self.h1=0;self.canonical=[];self.jsons=[];self.injson=False;self.buf='';self.lang=None;self.images=[];self.title="";self.intitle=False;self.alternates={}
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='title':self.intitle=True
  if a.get('srcset'):self.links.extend(v.strip().split()[0] for v in a['srcset'].split(','))
  if tag=='html':self.lang=a.get('lang')
  if tag=='h1':self.h1+=1
  if a.get('id'):
   assert a['id'] not in self.ids,('Duplicate element ID',a['id'])
   self.ids.add(a['id'])
  if tag=='a' and a.get('href'):self.links.append(a['href'])
  if tag in ['img','script'] and a.get('src'):self.links.append(a['src'])
  if tag=='link' and a.get('href'):
   self.links.append(a['href'])
   if a.get('rel')=='canonical':self.canonical.append(a['href'])
   if a.get('rel')=='alternate':self.alternates[a.get('hreflang')]=a['href']
  if tag=='img':self.images.append(a)
  if tag=='script' and a.get('type')=='application/ld+json':self.injson=True;self.buf=''
 def handle_data(self,d):
  if self.intitle:self.title+=d
  if self.injson:self.buf+=d
 def handle_endtag(self,t):
  if t=='title':self.intitle=False
  if t=='script' and self.injson:self.jsons.append(json.loads(self.buf));self.injson=False
pages={}
for f in ROOT.rglob('*.html'):
 p=Page();p.feed(f.read_text(encoding='utf8'));pages[f.resolve()]=p
 assert p.h1==1,(f,'h1',p.h1)
 assert p.lang in ['es','en'],f
 if f.name!='404.html':assert len(p.canonical)==1 and p.jsons,f
 for a in p.images:assert 'alt' in a and a.get('width') and a.get('height'),(f,a)
assert len({p.title for p in pages.values()})==len(pages),'Duplicate page titles'
assert len(pages)==PAGE_COUNT+1, 'Unexpected HTML page inventory'
for f,p in pages.items():
 route=f.relative_to(ROOT).as_posix().removesuffix('index.html')
 if f.name!='404.html':
  assert p.canonical==[BASE+'/'+route],('Canonical mismatch',route)
  key=route[3:] if route.startswith('en/') else route
  assert p.lang==('en' if route.startswith('en/') else 'es'),('Language mismatch',route)
  assert p.alternates=={'es':BASE+'/'+key,'en':BASE+'/en/'+key,'x-default':BASE+'/'+key},('Language alternatives',route)
 for href in p.links:
  u=urlsplit(href)
  if u.scheme or u.netloc:
   assert u.scheme in ('https','mailto'),('Unsafe link scheme',route)
   if (u.scheme,u.netloc)!=(BASE_URL.scheme,BASE_URL.netloc):continue
   if not unquote(u.path).startswith(BASE_PATH):continue
   relative=unquote(u.path)[len(BASE_PATH):]
   approved=urlunsplit((u.scheme,u.netloc,u.path,u.query,'')) in APPROVED_EXTERNAL
   expected_path=relative+'index.html' if relative.endswith('/') or not relative else relative
   if approved and expected_path not in EXPECTED:continue # separately hosted project demo
   target=(ROOT/relative).resolve()
  else:
   target=(f.parent/unquote(u.path)).resolve() if u.path else f
  assert target.is_relative_to(ROOT),('Link escapes artifact',route)
  if target.is_dir():
   assert u.path.endswith('/'),('Directory link without trailing slash',route)
   target=target/'index.html'
  assert target.exists(),('Missing link target',route,href)
  if u.fragment and target in pages:assert unquote(u.fragment) in pages[target].ids,('Missing anchor',route,href)
# A thumbnail must appear on both language editions of the published site.
thumbnail_files = set((ROOT/'assets').glob('thumb-*.webp'))
for language in ('es', 'en'):
 used = {
  (path.parent / image['src']).resolve()
  for path, page in pages.items() if page.lang == language
  for image in page.images if image.get('class') == 'editorial-thumb'
 }
 assert used == thumbnail_files, ('Editorial thumbnail inventory', language, used ^ thumbnail_files)
for locale in ['', 'en/']:
 s=(ROOT/locale/'publications/index.html').read_text(encoding='utf8')
 assert s.count('class="publication"')==PUB_COUNT
 assert s.count('class="year"')==PUB_COUNT
 assert '10.2139/ssrn.7687098' in s
for s in ROOT.rglob('*.html'):
 text=s.read_text(encoding='utf8')
 assert 'C:\\Users' not in text
 assert 'TODO' not in text
print(f'Static checks passed: {len(pages)} pages; links, anchors, structured data, images and publication completeness.')

# Every sitemap URL declares the same reciprocal language pair.
import xml.etree.ElementTree as ET
site=ET.parse(ROOT/'sitemap.xml');ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'}
entries=site.findall('s:url',ns);listed={e.find('s:loc',ns).text for e in entries}
assert len(entries)==PAGE_COUNT and len(listed)==PAGE_COUNT
pairs={e.find('s:loc',ns).text:{a.attrib['hreflang']:a.attrib['href'] for a in e.findall('x:link',ns)} for e in entries}
for url,pair in pairs.items():
 assert set(pair)=={'es','en'} and url in pair.values()
 for target in pair.values():assert target in listed and pairs[target]==pair
print(f'Sitemap: {PAGE_COUNT} URLs, reciprocal ES/EN alternates verified.')

for f,p in pages.items():
 if f.parent.name=='publications':
  collection=next(s for s in p.jsons if s.get('@type')=='CollectionPage')
  articles=[s for s in p.jsons if s.get('@type')=='ScholarlyArticle']
  items=collection['mainEntity']['itemListElement']
  assert collection['mainEntity']['numberOfItems']==len(articles)==len(items)==PUB_COUNT
  assert [x['item']['@id'] for x in items]==[a['@id'] for a in articles]
  assert all(a['description'] for a in articles)
print(f'Publication collection: {PUB_COUNT} linked article entities in each language.')

# Preserve publisher author order and compound family names in machine-readable output.
source_pubs=CONTENT['publications']
for pub in source_pubs:
 assert [a['given']+' '+a['family'] for a in pub['author_parts']]==pub['authors']
 citation=(ROOT/'downloads'/(pub['id']+'.bib')).read_text(encoding='utf8')
 assert 'author={'+' and '.join(a['family']+', '+a['given'] for a in pub['author_parts'])+'}' in citation
assert 'Hernando de Larramendi, Miguel' in (ROOT/'downloads/publications.bib').read_text(encoding='utf8')
print(f'Bibliography: author order and compound family names verified for all {PUB_COUNT} papers.')
