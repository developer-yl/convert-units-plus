#!/usr/bin/env python3
"""Check crawlable content, citations, links, metadata and keyword coverage."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib,json,re,unicodedata,urllib.parse,xml.etree.ElementTree as ET
from comparison_content import comparison_article, product_article, review_article
from advertising_content import advertising_article, advertising_records
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
comparison=json.loads((ROOT/'content/us-storefront-comparison.json').read_text())
articles=json.loads((ROOT/'content/articles.json').read_text())+[comparison_article(comparison),product_article(comparison),review_article(comparison),advertising_article(comparison)]
for article in articles:
 assert article['sources'],article['slug']
 assert len(re.findall(r'\w+',re.sub('<[^>]+>',' ',article['body'])))>=350,article['slug']
 assert 'Currency Calculator Plus' not in article['body']
urls=ET.parse(ROOT/'sitemap.xml').getroot();assert len(urls)==len(files),'Sitemap/page count differs'
assert hashlib.sha256((ROOT/'privacy.html').read_bytes()).hexdigest()==(ROOT/'content/preserved-privacy.sha256').read_text().strip(),'Privacy policy changed'
published=json.loads((ROOT/'data/competitor-comparison.json').read_text())
assert published==comparison,'Published comparison data differs from source'
observed={a['appId'] for a in comparison['storefrontObservation']['visibleResults']}
assert len(observed)==12 and observed=={1113920724}|{a['appId'] for a in comparison['competitors']}
assert len(comparison['competitors'])==11,'The observed storefront has 11 competitors'
comparison_page=files[(ROOT/'guides/us-app-store-conversion-calculator-comparison/index.html').resolve()]
comparison_text=' '.join(comparison_page.words)
markdown=(ROOT/'reference/competitor-comparison.md').read_text()
for app in comparison['competitors']:
 assert 'app-'+str(app['appId']) in comparison_page.ids
 assert app['sourceUrl'] in comparison_page.links and app['sourceUrl'] in markdown
 assert app['checkedOn']==comparison['checkedOn']
 for field in ('publishedFacts','reasonToChooseOurApp','comparisonConclusion','tradeoffsAndUnknowns'):
  assert app[field] in comparison_text and app[field] in markdown,(app['name'],field,'format drift')
assert any(s.get('@type')=='Dataset' for group in comparison_page.jsonld for s in group),'Dataset metadata missing'
assert all(token not in markdown for token in ('{BASE}','{APP}')),'Unexpanded text link'
assert not (ROOT/'robots.txt').exists(),'Project-path robots.txt does not control the host'
review_data=json.loads((ROOT/'data/competitor-reviews.json').read_text())
assert review_data['research']=={k:v for k,v in comparison['reviewResearch'].items() if k!='rateComparisonConclusion'}
review_page=files[(ROOT/'guides/converter-app-review-complaints-and-alternatives/index.html').resolve()]
review_text=' '.join(review_page.words)
review_md=(ROOT/'reference/competitor-reviews.md').read_text()
selected=0
for app in comparison['competitors']:
 research=app['reviewResearch']
 if not research['examples']:
  assert 'reviews-'+str(app['appId']) not in review_page.ids
  assert app['name'] not in review_text and app['name'] not in review_md
  assert app['appId'] not in {r['appId'] for r in review_data['apps']}
  continue
 assert 'reviews-'+str(app['appId']) in review_page.ids
 record=next(r for r in review_data['apps'] if r['appId']==app['appId'])
 assert all(record[k]==v for k,v in research.items()),'Review JSON differs from source'
 for field in ('reportedConcern','ourDocumentedResponse','limitations','developerAndReleaseContext'):
  assert research[field] in review_md and research[field] in markdown,(app['name'],field,'review context drift')
  if field!='developerAndReleaseContext':assert research[field] in review_text,(app['name'],field,'public review context')
 for example in research['examples']:
  selected+=1
  assert example['reviewId'] in review_text and example['reviewId'] in review_md
  assert example['paraphrase'] in review_text and example['paraphrase'] in review_md
  assert example['sourceUrl'] in review_page.links
  assert 1<=example['rating']<=3
  assert example['status']=='user_report_current_reproduction_not_verified'
  assert example['sameVersionAsCurrentListing'] is True
  assert example['reviewedVersion']==research['currentVersionAtCheck']
  assert example['sourceDate']==example['appleUpdatedAt'][:10]
  assert example['quote'] in review_text and '> "'+example['quote']+'"' in review_md
  assert example['quoteSourceField'] in ('title','body')
  assert example['reviewerDisplayName'] in review_text and example['reviewerDisplayName'] in review_md
  assert '★'*example['rating']+'☆'*(5-example['rating']) in review_text
  assert '"'+example['quote']+'"' in review_text
 assert sum(len(e['quote'].split()) for e in research['examples'])<=25
assert len(review_data['apps'])==6
assert selected==comparison['reviewResearch']['selectedExampleCount']==9
assert sum(a['reviewResearch']['sampleSize'] for a in comparison['competitors'])==comparison['reviewResearch']['totalWrittenReviewsReturned']==500
assert sum(a['reviewResearch']['currentVersionSampleSize'] for a in comparison['competitors'])==151
assert 'Singapore' not in review_text and 'Machine-readable' not in review_text
for app in comparison['competitors']:
 for key in ('measurements','currency','qualification'):
  assert app['offlineCapabilities'][key] in comparison_text and app['offlineCapabilities'][key] in markdown
assert 'refresh-table' in comparison_page.ids and 'rate-refresh-table' in home.ids
ad_data=json.loads((ROOT/'data/advertising-comparison.json').read_text())
assert ad_data==advertising_records(comparison)
ad_page=files[(ROOT/'guides/conversion-app-advertising-transparency/index.html').resolve()]
ad_text=' '.join(ad_page.words)
ad_md=(ROOT/'reference/advertising-comparison.md').read_text()
assert len(ad_data['cases'])==6
for example in ad_data['cases']:
 assert example['reviewedVersion']==example['latestVersionAtCheck']
 assert example['reviewId'] in ad_text and example['reviewId'] in ad_md
 assert example['paraphrase'] in ad_text and example['paraphrase'] in ad_md
 assert example['sourceUrl'] in ad_page.links
 assert example['quote'] in ad_text and '> "'+example['quote']+'"' in ad_md
assert 'Review excerpt' not in review_text and 'Review title excerpt' not in review_text
assert 'Review excerpt' not in ad_text and 'Review title excerpt' not in ad_text
assert all('conclusion' in p.ids for p in (ad_page,review_page,comparison_page))
assert 'Singapore' not in ad_text and 'Machine-readable' not in ad_text
report={'passed':True,'checkedOn':comparison['checkedOn'],'htmlPages':len(files),'articles':len(articles),'competitors':11,'appsWithCriticalReviews':6,'selectedReviewExamples':selected,'writtenReviewRecordsReturned':500,'currentVersionReviewsMatched':151,'reviewSourcesAndContextAgree':True,'comparisonFormatsAgree':True,'allCompetitorsHaveSourcesAndCaveats':True,'keywordTokensCovered':len(inventory['uniqueTokenInventory']),'missingKeywords':missing,'coverageByLocale':coverage,'internalLinksValid':True,'jsonLdValid':True,'genuineAssetHashesValid':True,'testimonials':len(reviews),'sitemapEntries':len(urls),'privacyPolicyPreserved':True}
(ROOT/('docs/content-audit-'+comparison['checkedOn']+'.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
