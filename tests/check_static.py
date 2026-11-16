from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json
ROOT=Path(__file__).resolve().parents[1]/'public'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set();self.h1=0;self.canonical=[];self.jsons=[];self.injson=False;self.buf='';self.lang=None;self.images=[];self.title="";self.intitle=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='title':self.intitle=True
  if a.get('srcset'):self.links.extend(v.strip().split()[0] for v in a['srcset'].split(','))
  if tag=='html':self.lang=a.get('lang')
  if tag=='h1':self.h1+=1
  if a.get('id'):self.ids.add(a['id'])
  if tag=='a' and a.get('href'):self.links.append(a['href'])
  if tag in ['img','script'] and a.get('src'):self.links.append(a['src'])
  if tag=='link' and a.get('href'):
   self.links.append(a['href'])
   if a.get('rel')=='canonical':self.canonical.append(a['href'])
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
for f,p in pages.items():
 for href in p.links:
  u=urlsplit(href)
  if u.scheme or u.netloc:continue
  target=(f.parent/unquote(u.path)).resolve() if u.path else f
  if target.is_dir():
   assert u.path.endswith('/'),(f,'Directory link without trailing slash',href)
   target=target/'index.html'
  assert target.exists(),(f,href,target)
  if u.fragment and target in pages:assert unquote(u.fragment) in pages[target].ids,(f,href)
for locale in ['', 'en/']:
 s=(ROOT/locale/'publications/index.html').read_text(encoding='utf8')
 assert s.count('class="publication"')==12
 assert s.count('class="year"')==12
 assert '10.2139/ssrn.7687098' in s
for s in ROOT.rglob('*.html'):
 text=s.read_text(encoding='utf8')
 assert 'C:\\Users' not in text
 assert 'TODO' not in text
print(f'Static checks passed: {len(pages)} pages; links, anchors, structured data, images and publication completeness.')
