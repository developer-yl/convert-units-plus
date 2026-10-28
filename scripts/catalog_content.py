"""Complete visible catalogs and matching machine-readable references."""
import html
import json
from pathlib import Path
from urllib.parse import quote

UNIT_SLUG = 'complete-unit-category-catalog'
CURRENCY_SLUG = 'currency-crypto-code-reference'
def esc(value): return html.escape(str(value), quote=True)
def unit_id(category, unit): return 'unit-'+quote(category, safe='')+'-'+quote(unit, safe='')

def unit_catalog(data):
    intro = '''<article class="article catalog"><header class="article-header"><a class="back" href="../">← All guides</a><p class="eyebrow">Complete catalog · Updated 28 October 2026</p><h1>Every category.<br>Every measurement unit.</h1><p class="article-deck">Browse all 72 conversion categories: 71 measurement categories containing 685 units, plus Currency for world currencies, crypto and precious metals.</p></header><div class="article-body"><p>Use this directory to find an everyday or engineering conversion before opening the iPhone or iPad app. Names and symbols follow the app’s English package catalog. The same unit can appear in more than one category when it serves a different quantity. The total counts category entries rather than unique spellings.</p><p><a href="../currency-crypto-code-reference/">Open the complete currency, crypto and metals catalog →</a></p><nav class="catalog-index" aria-label="Conversion categories"><a href="../currency-crypto-code-reference/">Currency</a>'''
    categories = sorted(data['categories'], key=lambda c: c['name'].casefold())
    intro += ''.join(f'<a href="#category-{esc(c["rawValue"])}">{esc(c["name"])} <span>({len(c["units"])})</span></a>' for c in categories)
    intro += '</nav><p class="fine">Use your browser’s Find command to search this complete static directory. All rows are present without JavaScript.</p>'
    for c in categories:
        intro += f'<section id="category-{esc(c["rawValue"])}"><h2>{esc(c["name"])} <small>· {len(c["units"])} units</small></h2><div class="table-wrap"><table><thead><tr><th>Unit</th><th>Symbol / scale</th></tr></thead><tbody>'
        intro += ''.join(f'<tr id="{unit_id(c["rawValue"], u["raw"])}"><th scope="row">{esc(u["en"])}</th><td>{esc(u.get("symbol", ""))}</td></tr>' for u in c['units'])
        intro += '</tbody></table></div></section>'
    intro += '''<h2>Choose the quantity first</h2><p>Temperature readings and temperature intervals use different rules. A cooking mass is not a volume without a density. Fuel economy depends on the gallon system. Shoe and ring sizes use regional scales. Select the exact category and named unit in the app.</p><p><a href="../measurement-conversion-guide/">Read the measurement conversion guide</a> · <a href="../kitchen-cooking-unit-conversions/">Cooking and baking units</a> · <a href="../calculator-history-and-widgets/">Calculator and widgets</a></p><h2>Catalog sources</h2><p>Exported from ConversionKit’s English unit catalog and checked against its category registry on 28 October 2026. Currency entries come from CurrencyKit and exclude the app’s withdrawn SSP selection.</p><p><a href="../../data/app-catalog.json">Download the full catalog as JSON</a> · <a href="../../reference/app-catalog.md">Read the plain-text catalog</a></p></div></article>'''
    return intro

def currency_catalog(data):
    counts = data['currencyCountsByKind']
    body = f'''<article class="article catalog"><header class="article-header"><a class="back" href="../">← All guides</a><p class="eyebrow">Complete catalog · Updated 28 October 2026</p><h1>All currencies, crypto<br>and precious metals.</h1><p class="article-deck">{data['currencyCount']} selectable codes: {counts['fiat']} world currency and currency-like entries, {counts['crypto']} cryptocurrencies and tokens, and {counts['metal']} precious metals.</p></header><div class="article-body"><p>Look up every recognized code and its English catalog name. This directory describes the app’s selections; inclusion does not guarantee a fresh quote, a circulating currency, an active token market or an executable trade. Check availability and the displayed timestamp in the app. Withdrawn SSP is excluded.</p><nav class="catalog-index" aria-label="Currency catalog groups"><a href="#fiat">World currencies</a><a href="#crypto">Cryptocurrencies and tokens</a><a href="#metal">Precious metals</a><a href="../{UNIT_SLUG}/">All measurement units</a></nav><p><a href="../travel-currency-converter-guide/">Currency names, FX comparisons and travel pairs</a> · <a href="../crypto-and-precious-metals-guide/">Crypto and metal quote guide</a></p><h2>Read a money conversion clearly</h2><p>Forex or FX means foreign exchange. A money conversion compares amounts using a quote; the app does not transfer money or place trades. A pound, peso, dinar, dirham or franc needs its code and region. GBP is pound sterling, also called quid; AUD is sometimes called the Aussie dollar and NZD the kiwi. CNY is the Chinese yuan or renminbi, often written RMB. BRL is the Brazilian Real.</p><p>Bitcoin Cash uses BCH, distinct from Bitcoin BTC. Ether is the native asset of Ethereum ETH. A stablecoin label, including Tether USDT, USD Coin USDC or DAI, does not guarantee a fixed price. PAX Gold PAXG and Tether Gold XAUT are tokens in the crypto group, distinct from physical-metal quotes.</p>'''
    for kind, name in [('fiat', 'World currencies and currency-like units'), ('crypto', 'Cryptocurrencies and tokens'), ('metal', 'Precious metals')]:
        body += f'<section id="{kind}"><h2>{name} <small>· {counts[kind]} codes</small></h2>'
        if kind == 'fiat': body += '<p>This follows the package’s fiat grouping, which also includes regional, offshore, supranational, historical and currency-like entries. Recognition is separate from current rate availability.</p>'
        if kind == 'metal': body += '<p>XAU is gold, XAG silver, XPT platinum and XPD palladium. A troy ounce differs from an ordinary mass ounce; check the quote basis before comparing a metal price. These are indicative metal comparisons, without jewelry-purity or scrap-value adjustments.</p>'
        body += '<div class="table-wrap"><table><thead><tr><th>Code</th><th>English catalog name</th><th>Type</th></tr></thead><tbody>'
        body += ''.join(f'<tr id="code-{esc(c["code"])}"><th scope="row">{esc(c["code"])}</th><td>{esc(c["englishName"])}</td><td>{kind}</td></tr>' for c in data['currencies'] if c['kind'] == kind)
        body += '</tbody></table></div></section>'
    body += '''<h2>Rates, offline use and widgets</h2><p>Currency+ checks for rates every minute while its rates page is visible, the app is active and internet is connected. A check can return the same observation. Previously loaded rates and charts remain usable offline; uncached data needs a connection. Interactive converter widgets require optional Premium and show their own update age; the active app’s one-minute schedule is not a widget background-update promise.</p><p><a href="../currency-plus-history-charts-guide/">Currency+ and chart controls</a> · <a href="../../data/app-catalog.json">Full catalog JSON</a> · <a href="../../reference/app-catalog.md">Plain-text catalog</a></p><p class="fine">Catalog names and classifications were exported from CurrencyKit on 28 October 2026 and checked against ConversionKit’s currency case list and retired-code policy. This is a code reference, not investment advice or a trading service.</p></div></article>'''
    return body

def write_catalog_copies(root, data):
    (root/'data/app-catalog.json').write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
    md = '# Complete Conversion Calculator Plus catalog\n\nChecked: '+data['checkedOn']+'.\n\n'+data['coverageNote']+'\n\n'
    md += f"{data['categoryCount']} categories; {data['measurementUnitCount']} measurement entries; {data['currencyCount']} selectable currency/crypto/metal codes.\n\n"
    for c in sorted(data['categories'], key=lambda c: c['name']):
        md += '## '+c['name']+'\n\n'
        md += ''.join('- '+u['en']+' — '+u.get('symbol','')+'\n' for u in c['units'])+'\n'
    for kind in ('fiat', 'crypto', 'metal'):
        md += '## Currency: '+kind+'\n\n'
        md += ''.join('- '+c['code']+' — '+c['englishName']+'\n' for c in data['currencies'] if c['kind']==kind)+'\n'
    (root/'reference/app-catalog.md').write_text(md)
