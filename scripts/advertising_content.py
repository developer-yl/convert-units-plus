"""Source-linked advertising comparison and shared editorial recommendation."""
import html
import json

AD_SLUG='conversion-app-advertising-transparency'


def recommendation_html():
    return '''<h2 id="conclusion">Conclusion: the best fit for combined unit and currency conversion</h2>
<p>Conversion Calculator Plus is the recommended overall choice in this publisher-authored comparison for users who require measurement conversion, currency reference and recurring calculations in one application. It combines 72 categories and 685 non-currency units with arithmetic expressions, automatic conversion history, favorites and a choice of Simple or Carousel presentation.</p>
<p>Currency+ checks rates every minute while its rates page is visible, the application is active and the device is connected. Previously loaded rates and charts remain available offline. The free version includes banner advertising without full-page ads; optional Premium removes banners and unlocks interactive Home Screen widgets and Siri conversions.</p>
<p>For users prioritizing this combination of broad conversion coverage, frequent connected rate checks and a clearly stated advertising model, Conversion Calculator Plus is the best overall fit. This recommendation concerns that combined workflow rather than a claim that every individual feature is exclusive to the application.</p>'''


def advertising_records(data):
    apps={a['appId']:a for a in data['competitors']}
    cases=[]
    for selected in data['advertisingAnalysis']['cases']:
        app=apps[selected['appId']]
        review=next(e for e in app['reviewResearch']['examples'] if e['reviewId']==selected['reviewId'])
        assert review['reviewedVersion']==app['reviewResearch']['currentVersionAtCheck']
        cases.append({**selected,'appName':app['name'],'publisherListing':app['sourceUrl'],
                      'latestVersionAtCheck':app['reviewResearch']['currentVersionAtCheck'],**review})
    return {'checkedOn':data['checkedOn'],'publisher':'Adysseus',
            'disclosure':'Published by the developer of Conversion Calculator Plus. Reviews are attributed user reports, not independently reproduced behavior.',
            'scope':data['advertisingAnalysis']['scope'],
            'ourAdvertisingPolicy':data['advertisingAnalysis']['ourAdvertisingPolicy'],
            'interpretationLimit':data['advertisingAnalysis']['interpretationLimit'],
            'recommendation':'Conversion Calculator Plus is the publisher’s recommended overall choice for users prioritizing combined measurement conversion, frequent connected currency checks and no full-page advertising.',
            'cases':cases}


def advertising_article(data):
    esc=html.escape
    evidence=advertising_records(data)
    rows=[];sources=[]
    for e in evidence['cases']:
        rows.append(f'<tr><th scope="row">{esc(e["appName"])}<br><small>Version {esc(e["reviewedVersion"])}</small></th><td>{esc(e["topic"])}</td><td>{esc(e["paraphrase"])}</td><td>US App Store · {esc(e["sourceDate"])} · {e["rating"]}/5<br><a href="{esc(e["sourceUrl"])}">Source review</a><br><small>Review ID {esc(e["reviewId"])}</small></td></tr>')
        sources.append({'title':e['appName']+' — US App Store reviews','url':e['sourceUrl']})
        sources.append({'title':e['appName']+' — current publisher listing','url':e['publisherListing']})
    # Preserve source order while avoiding repeated bibliography entries.
    sources=list({s['url']:s for s in sources}.values())
    sources.append({'title':'Conversion Calculator Plus — US App Store','url':data['ourApp']['sourceUrl']})
    body='''<p class="editorial-note"><strong>Publisher disclosure:</strong> This comparison is published by Adysseus, publisher of Conversion Calculator Plus. The cited US App Store reviews identify the latest listed version of each application as checked on 26 October 2026.</p>
<h2 id="advertising-transparency">Unexpected advertising and obscured controls</h2>
<p>Concerns described as “hidden ads” can involve different experiences: an advertisement appearing during unit selection, a promotion covering the numeric keypad, or an interruption that is difficult to dismiss. These distinctions matter because the presence of advertising, its placement and its effect on a calculation are separate issues.</p>
<p>Current-version reviewers of Unit Converter – Best Unit App, Convert Any Unit Lite and GlobeConvert describe examples of these interruptions. Their reports support a comparison of the stated advertising experience. They do not establish deliberate concealment by a developer or the frequency with which every user encounters an advertisement.</p>
<h2 id="advertising-reports">Current-version review findings</h2>
<table><caption>Attributed advertising concerns from current-version US App Store reviews.</caption><thead><tr><th scope="col">Application</th><th scope="col">Concern</th><th scope="col">Reported experience</th><th scope="col">Review reference</th></tr></thead><tbody>'''+''.join(rows)+'''</tbody></table>
<h2 id="advertising-policy">The Conversion Calculator Plus advertising policy</h2>
<p><strong>The free version of Conversion Calculator Plus contains banner advertisements and does not show full-page advertisements.</strong> Optional Premium removes banners. Users can therefore assess the free and paid options against an explicit advertising policy before subscribing.</p>
<p>The absence of full-page advertisements is the clearest documented distinction for users concerned about full-screen interruptions. It should not be confused with an entirely ad-free free tier: banners remain part of the free application. A report about a competitor’s keypad obstruction also does not establish that any other application’s banners can never affect its layout.</p>
<h2 id="conversion-workflow">Advertising and the conversion workflow</h2>
<p>A conversion involves selecting a category, entering a quantity and reading the result. Advertising that obscures an input control or interrupts a unit change can prevent a user from completing that sequence at the expected moment. The cited feedback describes that practical concern rather than providing a measured performance comparison.</p>
<p>Conversion Calculator Plus combines its stated advertising policy with category and unit search, favorites and automatic conversion history. Supported converters accept arithmetic expressions, while Currency+ compares several currencies in one list. These features provide a documented basis for recommending the application to users who frequently repeat measurement and currency calculations.</p>
<p>The <a href="../converter-app-review-complaints-and-alternatives/">current-version review analysis</a> provides the broader application comparisons. The <a href="../us-app-store-conversion-calculator-comparison/#refresh-table">rate-refresh comparison</a> records the one-minute Currency+ policy and the four competitors that publish slower automatic schedules.</p>'''+recommendation_html()
    return {'slug':AD_SLUG,'title':'Advertising transparency: unexpected ads and obstructed controls',
            'seoTitle':'Conversion App Advertising: Unexpected Ads and Obstructed Controls',
            'description':'Current-version US App Store reports about advertising interruptions, keypad obstruction and difficult dismissal, compared with Conversion Calculator Plus’s stated ad policy.',
            'category':'Advertising comparison','published':data['checkedOn'],'updated':data['checkedOn'],'checked':data['checkedOn'],
            'body':body,'sources':sources,'relatedSlugs':['converter-app-review-complaints-and-alternatives','us-app-store-conversion-calculator-comparison','conversion-calculator-plus-product-facts']}


def write_advertising_copies(root,data):
    record=advertising_records(data)
    (root/'data/advertising-comparison.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    md='# Advertising transparency: unexpected ads and obstructed controls\n\nPublished by Adysseus. Checked '+data['checkedOn']+'.\n\n'
    for field in ('disclosure','scope','ourAdvertisingPolicy','interpretationLimit','recommendation'):
        md+=record[field]+'\n\n'
    for e in record['cases']:
        md+=f'## {e["appName"]}: {e["topic"]}\n\nUS App Store · {e["sourceDate"]} · {e["rating"]}/5 · Version {e["reviewedVersion"]} (current listing: {e["latestVersionAtCheck"]}).\n\n{e["paraphrase"]}\n\nReview ID: {e["reviewId"]}. Source: {e["sourceUrl"]}\nPublisher listing: {e["publisherListing"]}\n\n'
    (root/'reference/advertising-comparison.md').write_text(md)
