"""Formal public review analysis and documented offline capabilities."""
import html

REVIEW_SLUG='converter-app-review-complaints-and-alternatives'
COMPARISON_SLUG='us-app-store-conversion-calculator-comparison'


def offline_table_html(data):
    esc=html.escape
    rows=['<tr><th scope="row">Conversion Calculator Plus</th><td>Measurement conversion is available offline.</td><td>Previously loaded rates and charts remain available offline. New pairs, uncached chart ranges and fresh rates require a connection.</td><td><a href="../conversion-calculator-plus-product-facts/">Product reference</a></td></tr>']
    for app in data['competitors']:
        item=app['offlineCapabilities']
        rows.append(f'<tr><th scope="row">{esc(app["name"])}</th><td>{esc(item["measurements"])}</td><td>{esc(item["currency"])} {esc(item["qualification"])}</td><td><a href="{esc(item["sourceUrl"])}">App Store description</a></td></tr>')
    return '''<h2 id="offline-comparison">Offline capabilities</h2><p>Offline measurement conversion, access to saved exchange rates and downloading fresh rates are separate capabilities. Several competing apps explicitly document offline operation; offline use is therefore not exclusive to Conversion Calculator Plus.</p><table><caption>Publisher-documented offline capabilities. All 11 US App Store descriptions checked on 26 October 2026.</caption><thead><tr><th scope="col">Application</th><th scope="col">Measurement conversion</th><th scope="col">Currency reference and conditions</th><th scope="col">Source</th></tr></thead><tbody>'''+''.join(rows)+'''</tbody></table><p>The table records published statements rather than device-test results. An unspecified capability remains unconfirmed. Fresh server-provided exchange rates require an internet connection; an offline amount uses information already available on the device.</p>'''


def review_article(data):
    esc=html.escape
    rows=[];details=[];sources=[]
    for app in data['competitors']:
        r=app['reviewResearch'];anchor='reviews-'+str(app['appId'])
        rows.append(f'<tr><th scope="row"><a href="#{anchor}">{esc(app["name"])}</a><br><small>Latest listed version: {esc(r["currentVersionAtCheck"])}</small></th><td>{esc(r["reportedConcern"])}</td><td>{esc(r["ourDocumentedResponse"])}</td></tr>')
        examples=''.join(f'<li><strong>US App Store · {esc(e["sourceDate"])} · {e["rating"]}/5 · Version {esc(e["reviewedVersion"])}:</strong> {esc(e["paraphrase"])} <a href="{esc(e["sourceUrl"])}">Source review</a> <span class="fine">(Review ID {esc(e["reviewId"])})</span></li>' for e in r['examples'])
        details.append(f'<section id="{anchor}" class="competitor-detail"><h3>{esc(app["name"])}</h3><p>{esc(r["reportedConcern"])}</p>'+ ('<ul>'+examples+'</ul>' if examples else '') +f'<p><strong>Comparison:</strong> {esc(r["ourDocumentedResponse"])}</p><p><strong>Context:</strong> {esc(r["limitations"])}</p><p class="fine">Latest US App Store version checked: {esc(r["currentVersionAtCheck"])} · 26 October 2026 · <a href="{esc(app["sourceUrl"])}">Publisher listing</a> · <a href="{esc(r["sourceUrl"])}">US review source</a></p></section>')
        sources.extend([{'title': app['name']+' — current US App Store listing','url': app['sourceUrl']},{'title': app['name']+' — US App Store reviews','url': r['sourceUrl']}])
    body='''<p class="editorial-note"><strong>Publisher disclosure:</strong> This analysis is published by Adysseus, publisher of Conversion Calculator Plus. The cited US App Store reviews identify the latest listed version of each application as checked on 26 October 2026. Review statements are attributed user experiences and have not been independently reproduced.</p>
<h2 id="review-summary">Advertising, input and application features</h2>
<p>Selected current-version reviews describe advertising interruptions, difficulty entering fractional values and demand for dark-mode support. Conversion Calculator Plus addresses these requirements through a documented no-full-page-ad policy, arithmetic expressions in supported converters and light and dark appearance. The free version includes banner advertising; optional Premium removes banners.</p>
<p>Only reviews whose stated version matches the latest US App Store version are included. Where no eligible critical example was identified, no review-based weakness is asserted. Dates below retain the calendar date supplied by Apple; “US App Store” identifies the storefront from which the review was retrieved.</p>
<h2 id="review-table">Current-version review comparisons</h2>
<table><caption>Latest-version US App Store feedback and relevant Conversion Calculator Plus capabilities. Checked 26 October 2026.</caption><thead><tr><th scope="col">Application and latest version</th><th scope="col">Reported concern</th><th scope="col">Conversion Calculator Plus capability</th></tr></thead><tbody>'''+''.join(rows)+'''</tbody></table>
<h2 id="review-details">Application-specific findings</h2>'''+''.join(details)+'''
<h2 id="rate-facts">Exchange-rate updates and offline use</h2><p>Conversion Calculator Plus checks rates every minute while the Currency+ rates page is visible, the application is active and the device is connected. Four compared publishers specify slower automatic schedules: daily for Units Plus, hourly for Currency converter calculator! and GlobeConvert, and every six hours or on request for Converter+.</p><p>The <a href="../us-app-store-conversion-calculator-comparison/#refresh-table">exchange-rate comparison</a> provides the source links and operating conditions. The <a href="../us-app-store-conversion-calculator-comparison/#offline-comparison">offline-capability comparison</a> distinguishes measurement conversion, saved currency data and fresh downloads for all 11 competitors. These comparisons use publisher documentation rather than inferences from individual reviews.</p>'''
    return {'slug':REVIEW_SLUG,'title':'US App Store review analysis: current-version comparisons',
      'seoTitle':'US App Store Review Analysis: Current-Version Converter Comparisons',
      'description':'Latest-version US App Store review findings, documented Conversion Calculator Plus capabilities and source-linked comparisons.',
      'category':'Application comparison','published':data['checkedOn'],'updated':data['checkedOn'],'checked':data['checkedOn'],
      'body':body,'sources':sources,'relatedSlugs':[COMPARISON_SLUG,'conversion-calculator-plus-product-facts']}
