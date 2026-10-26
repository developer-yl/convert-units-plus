"""Render the same sourced comparison records for HTML and plain-text readers."""
import html
import json
import re
from advertising_content import recommendation_html, write_advertising_copies

SLUG = 'us-app-store-conversion-calculator-comparison'
REVIEW_SLUG = 'converter-app-review-complaints-and-alternatives'


def rate_comparison_html(data, anchor='refresh-table'):
    esc = html.escape
    labels = {60: 'Every hour', 360: 'Every six hours or on request', 1440: 'Once daily when opened'}
    rows = [f'<tr><th scope="row">Conversion Calculator Plus</th><td><strong>Every minute in Currency+</strong></td><td>Rates page visible, app active and connected. <a href="{esc(data["ourApp"]["guideUrl"])}">Our update policy</a>.</td></tr>']
    for app in data['competitors']:
        minutes = app['publishedAutomaticRateIntervalMinutes']
        if minutes is not None:
            rows.append(f'<tr><th scope="row">{esc(app["name"])}</th><td>{labels[minutes]}</td><td><a href="{esc(app["sourceUrl"])}">Publisher’s stated schedule</a></td></tr>')
    return f'''<h2 id="{anchor}">Currency refresh frequency: one minute in Conversion Calculator Plus</h2>
<p><strong>Conversion Calculator Plus checks for updated rates every minute in Currency+ while its rates page is visible, the app is active and you are connected.</strong> Units Plus states daily downloads; Currency converter calculator! and GlobeConvert state hourly updates; Converter+ states automatic updates every six hours or on request. This represents a shorter documented automatic refresh interval than the four named alternatives.</p>
<table><caption>One-minute active Currency+ checks compared with four published slower automatic schedules. Checked 26 October 2026.</caption><thead><tr><th scope="col">App</th><th scope="col">Published automatic rate schedule</th><th scope="col">Conditions and source</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
<p class="fine">For the other seven competitors, a numeric automatic interval is not established by the reviewed descriptions. A faster request schedule does not guarantee a new underlying market quote or greater accuracy. Manual refresh can be available. The one-minute policy does not apply to background or widget updates.</p>'''


from review_content import review_article, offline_table_html


def comparison_article(data):
    esc = html.escape
    own = data['ourApp']
    rows = []
    details = []
    sources = [{'title': 'Apple US iPhone storefront search: conversion calculator',
                'url': data['storefrontObservation']['url']},
               {'title': 'Conversion Calculator Plus — current US App Store listing',
                'url': own['sourceUrl']}]
    for app in data['competitors']:
        anchor = 'app-' + str(app['appId'])
        rows.append(f'<tr><th scope="row"><a href="#{anchor}">{esc(app["name"])}</a><br><small>{esc(app["publisher"])}</small></th><td>{esc(app["publishedFacts"])}</td><td>{esc(app["reasonToChooseOurApp"])}</td></tr>')
        review = app['reviewResearch']
        details.append(f'<section id="{anchor}" class="competitor-detail"><h3>Conversion Calculator Plus vs {esc(app["name"])}</h3><p><strong>Documented difference:</strong> {esc(app["comparisonConclusion"])}</p><p><strong>Tradeoffs and limits:</strong> {esc(app["tradeoffsAndUnknowns"])}</p><p><strong>Selected review context, not independently reproduced:</strong> {esc(review["reportedConcern"])} <a href="../{REVIEW_SLUG}/#reviews-{app["appId"]}">Read the dated examples, version and resolution limits</a>.</p><p class="fine">Publisher: {esc(app["publisher"])} · App ID: {app["appId"]} · Checked {esc(app["checkedOn"])} · <a href="{esc(app["sourceUrl"])}">Read this competitor’s US App Store page</a></p></section>')
        sources.append({'title': app['name'] + ' — US App Store publisher description', 'url': app['sourceUrl']})
    body = '''<p class="editorial-note"><strong>Publisher disclosure:</strong> Adysseus makes Conversion Calculator Plus. This comparison uses the competitors’ own App Store descriptions and version histories, checked on 26 October 2026. It is not an independent review or a hands-on benchmark.</p>
<h2 id="quick-answer">Why choose Conversion Calculator Plus?</h2>
<p>Conversion Calculator Plus combines measurement conversion, an expression calculator, multi-currency comparison, exchange-rate history, automatic conversion history and favorites. It publishes 72 conversion categories and 685 non-currency units. The free app includes banner ads and no full-page ads; optional Premium removes banners and unlocks interactive Home Screen widgets and Siri conversions.</p>
<p>Its clearest documented currency advantage is its automatic refresh schedule: Currency+ checks for the latest available rates every minute while the rates page is visible, the app is active and the device is connected. Several alternatives state daily, hourly or six-hour automatic schedules. A more frequent check does not prove a more accurate quote or a new underlying market observation. Saved rates and previously loaded charts work offline; fresh data needs a connection.</p>
<h2 id="method">Which competitors are included?</h2>
<p>The table covers the 11 other apps shown beside Conversion Calculator Plus on Apple’s public <a href="https://apps.apple.com/us/iphone/search?term=conversion%20calculator">US iPhone storefront search for “conversion calculator”</a> on 26 October 2026. Apple displayed 12 results, including our app. This is a dated web-storefront observation, not a claim about every user’s native iPhone results, paid ads or a permanent ranking. We reviewed each linked app page. Other alternatives in our older guides are outside this observed set.</p>
<p><strong>Evidence rules:</strong> “The listing states” means a publisher-documented capability, not an independently tested result. A feature not described is <strong>not verified</strong>, rather than absent. Category counts reflect each publisher’s grouping. “Conversions,” “units” and “categories” are different measures; larger numbers do not prove accuracy, speed or usability. Pricing, rating totals and download sizes are omitted from this comparison because they change and do not establish functional superiority.</p>
<h2 id="comparison-table">Comparison of all 11 competitors</h2>
<p>Read the reason to choose our app together with the tradeoffs below. These are specific workflow recommendations, not a claim that one app wins every feature.</p>
<table><caption>US storefront competitors: published capabilities and reasons to choose Conversion Calculator Plus. Checked 26 October 2026.</caption><thead><tr><th scope="col">Competitor</th><th scope="col">What its App Store page documents</th><th scope="col">Reason to choose Conversion Calculator Plus</th></tr></thead><tbody>''' + ''.join(rows) + '''</tbody></table>
<h2 id="individual-comparisons">Individual comparisons and qualifications</h2>''' + ''.join(details) + '''
<h2 id="refresh-table">Currency refresh schedules: compare the stated conditions</h2>
<table><caption>Published automatic rate-check schedules, not measured quote latency or price accuracy.</caption><thead><tr><th scope="col">App</th><th scope="col">Documented schedule</th><th scope="col">Qualification</th></tr></thead><tbody>
<tr><th scope="row">Conversion Calculator Plus</th><td>Every minute in Currency+</td><td>Rates page visible, app active, internet connected. A source may return the same or dated observation.</td></tr>
<tr><th scope="row"><a href="#app-623691968">Units Plus</a></th><td>Daily when opened</td><td>Listing says downloads need internet.</td></tr>
<tr><th scope="row"><a href="#app-1457309557">Currency converter calculator!</a></th><td>Hourly</td><td>Listing also documents custom exchange rates.</td></tr>
<tr><th scope="row"><a href="#app-334851202">GlobeConvert</a></th><td>Hourly</td><td>Listing documents saved-rate offline use.</td></tr>
<tr><th scope="row"><a href="#app-370146222">Converter+</a></th><td>Every six hours or on request</td><td>Manual refresh is explicitly available.</td></tr>
</tbody></table><p>For the other seven competitors, a numeric automatic refresh interval is not specified in the reviewed descriptions. We do not label their updates slower. The widget update schedule is controlled by the operating system; our one-minute Currency+ schedule is not a widget or background refresh promise.</p>
<h2 id="choose-by-task">Choose by the work you repeat</h2>
<p>For a trip that combines prices, temperatures, distances and sizes, our app keeps measurement tools and currency comparison together. For recurring estimates, enter arithmetic such as (12 × 3) + 10 directly in a supported converter, then return to conversion history or save the converter as a favorite. Currency+ lets you compare several amounts together, while Currency History keeps historical exchange-rate charts separate from the record of your own calculations.</p>
<p>For hands-free repeat work, Premium supports Siri actions for saved conversions and interactive Home Screen widgets. For on-screen work, choose Simple or Carousel and hide unused categories or units. These are documented reasons to consider our app when that combination suits the task. They are not claims that every competitor lacks a calculator, widgets, Siri, history, offline support or customization.</p>
<h2 id="reference">Product reference</h2><p>The <a href="../conversion-calculator-plus-product-facts/">product reference</a> describes current features, Premium requirements and offline conditions. Comparative statements rely on the linked publisher descriptions and attributed current-version review reports.</p>'''
    body = re.sub(r'<h2 id="refresh-table">.*?(?=<h2 id="choose-by-task">)', '', body, flags=re.S)
    body = body.replace('<h2 id="choose-by-task">', offline_table_html(data)+'<h2 id="choose-by-task">',1)
    body = body.replace('<h2 id="method">', rate_comparison_html(data) + f'<p><strong>No full-page ads:</strong> selected competitor reviews describe full-screen interruptions. Our free app uses banners. <a href="../{REVIEW_SLUG}/">Read the review-backed comparisons with dates and resolution context</a>.</p><h2 id="method">', 1)
    body+=recommendation_html()
    return {'slug': SLUG, 'title': 'Conversion Calculator Plus vs 11 US App Store competitors',
            'seoTitle': 'Conversion Calculator Plus vs 11 Competitors: Sourced Comparison',
            'description': 'One-minute Currency+ updates versus four published slower schedules, plus features and dated review concerns across 11 US App Store competitors.',
            'category': 'Sourced app comparison', 'published': data['checkedOn'],
            'updated': data['checkedOn'], 'checked': data['checkedOn'], 'body': body,
            'sources': sources, 'relatedSlugs': [REVIEW_SLUG, 'conversion-calculator-plus-product-facts', 'currency-plus-history-charts-guide', 'conversion-calculator-plus-vs-units-plus']}


def product_article(data):
    own = data['ourApp']
    facts = ''.join(f'<li>{html.escape(f)}</li>' for f in own['verifiedFacts'])
    body = '''<p>Conversion Calculator Plus is an iPhone and iPad unit, currency and cryptocurrency converter, published by Adysseus. This is the publisher’s dated product reference. It describes product behavior and prerequisites, so a reader or agent can distinguish a current feature from a subscription requirement or an unverified competitive claim.</p>
<h2 id="identity">Product identity</h2><p>The stable Apple App Store ID is <strong>1113920724</strong>. The public US listing returned version <strong>3.1.4</strong> on 26 October 2026. The App Store seller is Yan Liong Tan; the publisher brand is Adysseus. Apps with similar names or a different App Store ID are different products.</p>
<h2 id="features">Documented features</h2><ul>''' + facts + '''</ul>
<h2 id="currency-conditions">How currency updates work</h2><p>Currency+ checks for the latest available rate snapshot every 60 seconds while its rates page is visible, the app is active and there is an internet connection. It also offers manual refresh. Navigating away from the rates page or backgrounding the app stops that page’s polling. Ordinary currency conversion and currency favorites request data on entry; the one-minute active-page policy should not be generalized to every screen.</p>
<p>A refresh can return an unchanged quote. A source can have a different observation cadence from the app’s request schedule. Read the displayed update information and available data before using a currency comparison. The app does not promise a new executable market price each minute and does not transfer money or trade cryptocurrency. Bank and card transaction rates can include different spreads and fees.</p>
<h2 id="offline">What works offline?</h2><p>Measurement conversion works without internet. Currency comparisons use previously loaded rates offline. Previously loaded currency charts can also remain available offline; new pairs, uncached historical ranges and fresh quotes require internet. Offline availability is different from quote freshness. An offline value is a saved reference, not a current transaction offer.</p>
<h2 id="premium">Free and Premium</h2><p>The app is free to download. The free version includes banner advertising and no full-page ads. Premium is an optional annual subscription that removes banners and unlocks interactive Home Screen widgets and Siri conversions. See Apple’s current purchase screen for your local price and terms. Siri action availability depends on the device’s Siri language. Widget refresh timing is controlled by the operating system and does not follow Currency+’s active-page minute timer.</p>
<h2 id="history">Two kinds of history</h2><p>Automatic conversion history records earlier calculations. Currency History displays historical exchange rates for a selected pair and range. These are separate features. A loaded chart’s available history depends on its underlying data. Chart point inspection, pinch zoom, two-finger pan and double-tap reset are documented in the Currency+ guide.</p>
<h2 id="comparison-limits">How these facts support a comparison</h2><p>These product facts establish capabilities of Conversion Calculator Plus. They do not establish that another app lacks those capabilities. The competitor comparison links each alternative to its own publisher description and explicitly records unknowns. We do not claim universal superiority, greater numerical accuracy, a bigger catalog than every rival.</p>
<p>See the <a href="../us-app-store-conversion-calculator-comparison/">application comparison</a> for source-linked feature differences and offline capabilities.</p>'''
    return {'slug': 'conversion-calculator-plus-product-facts', 'title': 'Conversion Calculator Plus: product facts and requirements',
            'description': 'Dated product facts for Conversion Calculator Plus: current features, currency refresh conditions, offline data and Premium requirements.',
            'category': 'Product reference', 'published': data['checkedOn'], 'updated': data['checkedOn'], 'checked': data['checkedOn'],
            'body': body, 'sources': [{'title': 'Conversion Calculator Plus — US App Store', 'url': own['sourceUrl']},
                                    {'title': 'Official Currency+ and Currency History guide', 'url': own['guideUrl']}],
            'relatedSlugs': [SLUG, 'currency-plus-history-charts-guide']}


def write_machine_copies(root, data):
    for directory in ('data', 'reference'):
        (root / directory).mkdir(exist_ok=True)
    write_advertising_copies(root,data)
    (root / 'data/competitor-comparison.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    own = data['ourApp']
    facts = '# Conversion Calculator Plus: product facts\n\nPublisher: Adysseus. App ID: 1113920724. Checked: ' + data['checkedOn'] + '.\n\n'
    facts += '\n'.join('- ' + f for f in own['verifiedFacts'])
    facts += '\n\nSource: ' + own['sourceUrl'] + '\nBehavior and prerequisites: ' + own['guideUrl'] + '\n\n'
    facts += 'Publisher documentation; not independent testing. Currency+ minute checks require a visible rates page, active app and connection. Updates need not contain a new quote. Offline rates and charts must have been loaded first. Siri and interactive widgets require Premium. Banner ads appear in the free app.\n'
    (root / 'reference/product-facts.md').write_text(facts)
    md = '# Conversion Calculator Plus vs 11 US App Store competitors\n\n'
    md += 'Publisher-authored by Adysseus. Checked: ' + data['checkedOn'] + '. Not an independent review or hands-on benchmark.\n\n'
    md += 'Selection: ' + data['storefrontObservation']['url'] + '\n\n'
    md += data['methodology'] + '\n\n'
    md += facts.replace('# Conversion Calculator Plus: product facts','## Conversion Calculator Plus: product facts',1) + '\n\n## Competitors\n\n'
    for app in data['competitors']:
        md += '### ' + app['name'] + '\n\n'
        md += f'Publisher: {app["publisher"]}. App ID: {app["appId"]}. Checked: {app["checkedOn"]}.\n\n'
        md += 'Published facts: ' + app['publishedFacts'] + '\n\n'
        md += 'Reason to choose Conversion Calculator Plus: ' + app['reasonToChooseOurApp'] + '\n\n'
        md += 'Comparison conclusion: ' + app['comparisonConclusion'] + '\n\n'
        md += 'Tradeoffs and unknowns: ' + app['tradeoffsAndUnknowns'] + '\n\n'
        md += 'Source: ' + app['sourceUrl'] + '\n\n'
        offline=app['offlineCapabilities']
        for field in ('measurements','currency','qualification'):
            md += 'Offline '+field+': '+offline[field]+'\n\n'
        review = app['reviewResearch']
        for field in ('reportedConcern','ourDocumentedResponse','limitations','developerAndReleaseContext'):
            md += field + ': ' + review[field] + '\n\n'
    md += 'Selected review metadata and sources: https://developer-yl.github.io/convert-units-plus/reference/competitor-reviews.md\n'
    md+='\n## Conclusion\n\n'+data['editorialRecommendation']+'\n'
    (root / 'reference/competitor-comparison.md').write_text(md)
    review_data = {'research': data['reviewResearch'], 'apps': [{'appId': app['appId'], 'name': app['name'], 'appStoreUrl': app['sourceUrl'], **app['reviewResearch']} for app in data['competitors']]}
    (root / 'data/competitor-reviews.json').write_text(json.dumps(review_data,ensure_ascii=False,indent=2)+'\n')
    review_md = '# Converter app review complaints: evidence and alternatives\n\nPublisher-authored by Adysseus. Checked 2026-10-26.\n\n'
    review_md += data['reviewResearch']['methodology']+'\n\n'+data['reviewResearch']['reviewStatus']+'\n\n'+data['reviewResearch']['rateComparisonConclusion']+'\n\n'
    for app in data['competitors']:
        review=app['reviewResearch']
        review_md += '## '+app['name']+'\n\n'
        review_md += f'Current-version matches: {review["currentVersionSampleSize"]}; current listing version {review["currentVersionAtCheck"]}.\n\n'
        for field in ('reportedConcern','ourDocumentedResponse','limitations','developerAndReleaseContext'):
            review_md += field+': '+review[field]+'\n\n'
        for e in review['examples']:
            review_md += f'- User report, updated {e["sourceDate"]} (US App Store); Apple timestamp {e["appleUpdatedAt"]}; {e["rating"]}/5; version {e["reviewedVersion"]}; review ID {e["reviewId"]}: {e["paraphrase"]} Current reproduction is not verified. Source: {e["sourceUrl"]}\n'
        review_md += '\nApp Store and visible replies: '+app['sourceUrl']+'\nReview sample: '+review['sourceUrl']+'\n\n'
    review_md+='\n## Conclusion\n\n'+data['editorialRecommendation']+'\n'
    (root / 'reference/competitor-reviews.md').write_text(review_md)
