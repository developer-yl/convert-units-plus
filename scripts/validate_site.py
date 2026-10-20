#!/usr/bin/env python3
"""Check crawlable content, citations, links, metadata and keyword coverage."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib,json,re,unicodedata,urllib.parse,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.words=[];self.links=[];self.ids=set();self.images=[];self.h1=0;self.script=False;self.jsonld=[];self.buffer=[];self.canonical=None;self.description=None;self.title=False;self.title_text=[]
 def handle_starttag(self,t,pairs):
  a=dict(pairs)
  if t in ['head','script','style']:self.skip+=1
  if t=='h1':self.h1+=1
  if t=='title':self.title=True
  if 'id' in a:self.ids.add(a['id'])
  if t=='a' and a.get('href'):self.links.append(a['href'])
  if t=='link' and a.get('rel')=='canonical':self.canonical=a.get('href')
  if t=='meta' and a.get('name')=='description':self.description=a.get('content')
  if t=='img':self.images.append(a)
  if t=='script' and a.get('type')=='application/ld+json':self.script=True;self.buffer=[]
 def handle_endtag(self,t):
  if t in ['head','script','style']:self.skip-=1
  if t=='title':self.title=False
  if t=='script' and self.script:self.jsonld.append(json.loads(''.join(self.buffer)));self.script=False
 def handle_data(self,text):
  if not self.skip:self.words.append(text)
  if self.title:self.title_text.append(text)
  if self.script:self.buffer.append(text)
files={};allwords=[]
for f in sorted(ROOT.rglob('*.html')):
 if any(part.startswith('.') for part in f.relative_to(ROOT).parts):continue
 assert not f.name.startswith('_preview'), 'Remove temporary preview files before publishing'
 p=Page();p.feed(f.read_text());files[f.resolve()]=p;allwords+=p.words
 if f.name!='privacy.html':
  assert p.h1==1,(f,'one h1 required')
  assert p.canonical and p.canonical.startswith('https://developer-yl.github.io/convert-units-plus/'),(f,'canonical')
  assert p.description,(f,'description')
  assert p.jsonld,(f,'structured data')
  assert len(''.join(p.title_text))<=90,(f,'title too long')
for f,p in files.items():
 for link in p.links:
  url=urllib.parse.urlsplit(link)
  if url.scheme or url.netloc:continue
  target=(f.parent/urllib.parse.unquote(url.path or f.name)).resolve()
  if target.is_dir():target/='index.html'
  assert target.is_relative_to(ROOT),(f,link,'link escapes project')
  assert target.exists(),(f,link,'missing link target')
  if url.fragment and target.suffix=='.html':assert url.fragment in files[target].ids,(f,link,'missing anchor')
 for a in p.images:
  assert 'alt' in a,(f,'missing image alt')
  src=(f.parent/a['src']).resolve();assert src.exists(),(f,'missing image')
for row in json.loads((ROOT/'content/asset-provenance.json').read_text()):assert hashlib.sha256((ROOT/row['file']).read_bytes()).hexdigest()==row['sha256'],'Genuine app asset changed'
wordtext=unicodedata.normalize('NFKC',' '.join(allwords)).casefold();inventory=json.loads((ROOT/'content/keyword-inventory.json').read_text());missing=[];coverage={}
for locale in inventory['localeRecords']:
 covered=[]
 for word in locale['uniqueTokens']:
  token=unicodedata.normalize('NFKC',word).casefold();pattern=r'(?<!\w)'+re.escape(token)+r'(?!\w)' if token.isascii() else re.escape(token)
  if re.search(pattern,wordtext):covered.append(word)
  else:missing.append({'locale':locale['locale'],'token':word})
 coverage[locale['locale']]={'covered':len(covered),'total':len(locale['uniqueTokens'])}
assert not missing,missing
home=files[(ROOT/'index.html').resolve()]
assert {'what-is-the-app','how-it-works','main-features','audience-segments','testimonials','support'}.issubset(home.ids)
reviews=json.loads((ROOT/'content/testimonials.json').read_text());assert all(r['rating']==5 and r['author'] and r['reviewId'] and r['sourceURL'] for r in reviews)
assert sum(len(r['quote'].split()) for r in reviews)<=25
for article in json.loads((ROOT/'content/articles.json').read_text()):
 assert article['sources'],article['slug']
 assert len(re.findall(r'\w+',re.sub('<[^>]+>',' ',article['body'])))>=350,article['slug']
 assert 'Currency Calculator Plus' not in article['body']
urls=ET.parse(ROOT/'sitemap.xml').getroot();assert len(urls)==len(files),'Sitemap/page count differs'
assert hashlib.sha256((ROOT/'privacy.html').read_bytes()).hexdigest()==(ROOT/'content/preserved-privacy.sha256').read_text().strip(),'Privacy policy changed'
report={'passed':True,'htmlPages':len(files),'articles':len(json.loads((ROOT/'content/articles.json').read_text())),'keywordTokensCovered':len(inventory['uniqueTokenInventory']),'missingKeywords':missing,'coverageByLocale':coverage,'internalLinksValid':True,'jsonLdValid':True,'genuineAssetHashesValid':True,'testimonials':len(reviews),'sitemapEntries':len(urls),'privacyPolicyPreserved':True}
(ROOT/'docs/content-audit-2026-10-20.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
