"""Verify catalog completeness and exact visible search-phrase coverage."""
from collections import Counter
from html.parser import HTMLParser
import json
import re
import unicodedata
from urllib.parse import quote

class CatalogRows(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = {}
        self.active = None
        self.cells = []
        self.cell = None
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'tr':
            self.active = attrs.get('id')
            self.cells = []
        if tag in ('td', 'th') and self.active:
            self.cell = ''
    def handle_data(self, text):
        if self.cell is not None:
            self.cell += text
    def handle_endtag(self, tag):
        if tag in ('td', 'th') and self.cell is not None:
            self.cells.append(self.cell)
            self.cell = None
        if tag == 'tr' and self.active:
            assert self.active not in self.rows, ('Duplicate catalog row', self.active)
            self.rows[self.active] = self.cells
            self.active = None

def normalized(text):
    return unicodedata.normalize('NFKC', re.sub(r'\s+', ' ', text)).casefold()

def validate_catalog(root, pages):
    data = json.loads((root/'content/app-catalog.json').read_text())
    assert data == json.loads((root/'data/app-catalog.json').read_text())
    assert len(data['categories']) == data['measurementCategoryCount'] == 71
    assert data['categoryCount'] == 72
    assert sum(len(c['units']) for c in data['categories']) == data['measurementUnitCount'] == 685
    codes = [c['code'] for c in data['currencies']]
    assert len(codes) == len(set(codes)) == data['currencyCount'] == 289
    assert not (set(codes) & set(data['excludedRetiredCodes']))
    assert dict(Counter(c['kind'] for c in data['currencies'])) == data['currencyCountsByKind']
    assert {c['code'] for c in data['currencies'] if c['kind'] == 'metal'} == {'XAU','XAG','XPT','XPD'}
    unit_path = root/'guides/complete-unit-category-catalog/index.html'
    currency_path = root/'guides/currency-crypto-code-reference/index.html'
    unit_rows = CatalogRows(); unit_rows.feed(unit_path.read_text())
    currency_rows = CatalogRows(); currency_rows.feed(currency_path.read_text())
    assert len(unit_rows.rows) == 685
    assert len(currency_rows.rows) == 289
    markdown = (root/'reference/app-catalog.md').read_text()
    unit_page = pages[unit_path.resolve()]
    assert 'Currency' in ' '.join(unit_page.words)
    for category in data['categories']:
        assert 'category-'+category['rawValue'] in unit_page.ids
        assert '## '+category['name']+'\n' in markdown
        assert len({u['raw'] for u in category['units']}) == len(category['units'])
        for unit in category['units']:
            row_id = 'unit-'+quote(category['rawValue'], safe='')+'-'+quote(unit['raw'], safe='')
            assert unit_rows.rows[row_id] == [unit['en'], unit.get('symbol','')], row_id
            assert '- '+unit['en']+' — '+unit.get('symbol','')+'\n' in markdown
    for currency in data['currencies']:
        assert currency_rows.rows['code-'+currency['code']] == [currency['code'], currency['englishName'], currency['kind']]
        assert '- '+currency['code']+' — '+currency['englishName']+'\n' in markdown
    inventory = json.loads((root/'content/search-term-coverage.json').read_text())
    assert len(inventory['terms']) == len({r['term'] for r in inventory['terms']}) == 279
    visible = {str(path.relative_to(root)): normalized(' '.join(page.words)) for path, page in pages.items()}
    results = []
    for record in inventory['terms']:
        assert record['status'] in ('include', 'excluded') and record['reason']
        if record['status'] == 'excluded':
            results.append(record)
            continue
        pattern = r'(?<!\w)'+re.escape(normalized(record['term']))+r'(?!\w)'
        matches = [path for path, text in visible.items() if re.search(pattern, text)]
        assert matches, ('Relevant search phrase absent from visible HTML', record['term'])
        results.append({**record, 'visibleOn': matches})
    report = {
        'passed': True, 'checkedOn': inventory['reviewedOn'],
        'categories': 72, 'measurementUnits': len(unit_rows.rows),
        'selectableCurrencyCodes': len(currency_rows.rows),
        'currencyCountsByKind': data['currencyCountsByKind'],
        'catalogHtmlJsonAndMarkdownAgree': True,
        'retiredCodesExcludedFromSelections': data['excludedRetiredCodes'],
        'searchTermsReviewed': len(results),
        'relevantSearchTermsCovered': sum(r['status']=='include' for r in results),
        'excludedSearchTerms': sum(r['status']=='excluded' for r in results),
        'matchingPolicy': 'Exact normalized phrases in visible HTML, excluding head, scripts and styles.',
        'results': results,
    }
    (root/'docs/catalog-and-search-audit-2026-10-28.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    return {key: value for key, value in report.items() if key != 'results'}
