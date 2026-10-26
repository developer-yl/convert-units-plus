# Conversion Calculator Plus — official website

Public marketing site for the iPhone/iPad app, served by GitHub Pages from the
root of `main`: https://developer-yl.github.io/convert-units-plus/ .
The App Store Marketing URL and Support URL use this site; `#support` and the
existing `privacy.html` remain valid. No framework, npm dependencies, runtime
server, tracking script or external font is required.

## Edit and rebuild

- `scripts/build_site.py`: shared page template, homepage, code reference and
  Simplified/Traditional Chinese pages. Standard Python 3 only.
- `content/articles.json`: ten original articles: one editorial best-app list,
  four competitor comparisons and five educational guides. Each has a headline,
  description, body HTML, primary-source citations and related slugs.
- `content/testimonials.json`: three short genuine App Store review excerpts,
  with public nickname, date, territory, rating, source link and record ID.
- `content/keyword-inventory.json`: exact ten-localization metadata snapshot and
  semantic topic inventory. Do not paste raw keyword fields into hidden page
  content. The 298 target terms appear in useful visible prose/code tables.
- `content/competitor-sources.json`: dated competitor facts and source links.
- `assets/`: CSS and four unchanged first-party app assets.
- `content/asset-provenance.json`: original app-relative source paths and hashes.

```sh
python3 scripts/build_site.py
python3 scripts/validate_site.py
```

The generator writes static HTML, canonical/social metadata, JSON-LD,
`sitemap.xml`, `llms.txt` and a generated-page manifest. It does not edit the
privacy policy, upload App Store media or change release state. Commit source
and generated files together. Keep the build date and checked facts current.

## Content rules

The site includes five requested homepage sections: what the app is, how it
works, main features, audience segments and genuine positive review excerpts.

Comparisons are clearly publisher-authored editorial recommendations. They
explain where our documented feature mix is a better fit and acknowledge rival
strengths. Never turn a public Search API position or a short Store web list
into a claim of native iPhone organic ranking. Do not invent hands-on tests,
awards, reviews, unavailable rival features or unsupported capabilities.

Current product facts: 72 categories, 685 non-currency units; world currency,
crypto and metal comparisons; Simple and Carousel modes; 2016 classic mode;
expression calculator; Currency+; saved rates/charts and automatic conversion
history/favorites. Live updates need connectivity; offline data must have been
loaded previously. Siri and interactive widgets need optional Premium. Free
includes banner ads and no full-page ads. The app does not execute transfers
or crypto trades. Currency code recognition does not guarantee a fresh quote.

The educational constants are sourced to NIST/BIPM. Recipes distinguish mass
from volume; gallons distinguish US liquid from Imperial. Preserve those
qualifications when changing examples. Reviews refer to earlier app versions,
not a claim that reviewers used this release. Do not publish complete customer
review dumps or credentials.

## Crawling and AI access

Pages are public, static HTML: article text and navigation are present without
JavaScript. They have `index,follow` metadata, canonical URLs, a linked XML
sitemap and appropriate WebPage/Article/SoftwareApplication JSON-LD. `llms.txt`
is a plain-text guide for tools, not a guarantee of crawler adoption or citation.

**Robots rules are host-wide.** Crawlers consult
`https://developer-yl.github.io/robots.txt`, not a project-path file at
`/convert-units-plus/robots.txt`. The host file returned HTTP 404 on 20 October
2026. No host-wide crawler policy or AI-training preference was changed by this
update. Do not add a project-path robots file and claim it controls the host.

The home page returned HTTP 200 to a request identifying as OAI-SearchBot,
without an X-Robots-Tag exclusion. This checks HTTP accessibility; it does not
prove that OpenAI has crawled, indexed or cited the site. Search inclusion and
model answers are not guaranteed by markup, content or bot user-agent tests.

[OpenAI's crawler documentation](https://developers.openai.com/api/docs/bots)
distinguishes OAI-SearchBot (search discovery), GPTBot (potential training use)
and ChatGPT-User (user-directed page visits). Their controls are independent.
For a future intentional robots policy, use the owner’s domain-root repository
and preserve rules for other sites sharing this host.

## Publish and verify

The existing GitHub Pages configuration publishes `main` `/` automatically.
Fetch the remote before committing; preserve unrelated work. Run the build and
validator, inspect desktop/mobile layouts and at least one comparison, then
commit and push normally. Do not force-push. Check the Pages build for the exact
commit and verify public home, guide, sitemap, asset and Chinese-page responses.

The generated files and sources are small; do not delete the native app's raw
capture inputs or confuse this website's four assets with disposable App Store
screenshot exports.

## Search-engine ownership and sitemap submissions

Google Search Console uses the URL-prefix property
`https://developer-yl.github.io/convert-units-plus/`. Its public verification
meta tag and Bing Webmaster Tools’ `msvalidate.01` tag are generated on the English home page by `scripts/build_site.py`;
keep them after verification so ownership remains valid. These are public
ownership tokens, not API credentials. Submit `sitemap.xml` in Search Console
and Bing Webmaster Tools after ownership verification. Submission requests
discovery; it does not guarantee indexing or search placement. Do not use the
retired anonymous Google/Bing sitemap ping endpoints.

The home-page callout and comparison articles emphasize connected rate
refreshes every minute. The Units Plus listing documents a daily download
when opened. The expanded US storefront comparison also documents hourly updates for Currency
converter calculator! and GlobeConvert, and six-hour automatic updates (or manual
refresh) for Converter+. The remaining seven do not specify a numeric interval
in the reviewed descriptions; do not infer that their updates are slower. Recheck linked publisher
sources before changing those comparisons.

## Currency+ and chart guide update — 22 October 2026

The homepage now explains multi-currency inputs, expressions, minute refreshes,
chart ranges, point readouts and offline prerequisites. A dedicated Currency+
and Currency History guide and Chinese summaries describe the controls.
The public US App Store lookup still returned 3.1.1 during this update, so
pinch zoom on both axes, two-finger pan and double-tap reset are explicitly
marked as coming in 3.1.2. Remove that availability note after verifying release.
A refresh checks for the latest available rate; it does not promise a changed
quote from every provider each minute. Source behavior and gestures were checked
against the app’s build 3 implementation and simulator verification.
Existing screenshots are unchanged first-party captures from the earlier layout.
Per-article publication/update/check dates preserve older comparison provenance.

## US storefront comparison — 26 October 2026

The current comparison uses the 12 visible results (our app plus 11 competitors)
from Apple's **public US iPhone web storefront**, searched in a browser for
`conversion calculator`. It does not claim native-device order or permanent rank.
All 11 linked App Store pages were reviewed, including their descriptions and
relevant version history. Their numeric claims are publisher assertions.

- Source records: `content/us-storefront-comparison.json`.
- HTML and text rendering: `scripts/comparison_content.py`, called by the builder.
- Generated JSON: `data/competitor-comparison.json`.
- Generated plain text: `reference/competitor-comparison.md` and `reference/product-facts.md`.
- Public comparison: `guides/us-app-store-conversion-calculator-comparison/`.
- Current facts: `guides/conversion-calculator-plus-product-facts/`.

Maintain all generated formats by editing the source records and rebuilding.
Every app has a stable ID, source URL, check date, documented facts, reasons to
choose our app and explicit tradeoffs/unknowns. Never turn an unmentioned feature
into an absence. No universal winner, accuracy advantage, unit-count ratio or
pricing advantage is asserted. GlobeConvert's description gives conflicting
physical-unit totals, so those numbers do not support a catalog superiority claim.
oWorld's 18+ is a lower bound, not a complete category count.

Our catalog was cross-checked against the ConversionKit registry (72 categories)
and its English non-currency catalog (685 units). The one-minute policy was
checked against the app's Currency+ architecture: visible rates page, foreground
app, internet. The public Apple Search API returned our release 3.1.4; chart
gestures are no longer labeled as an upcoming 3.1.2 feature.

Host-root robots.txt still returns 404 and an OAI-SearchBot user-agent request to
our home page returns 200 without X-Robots-Tag exclusions (26 October 2026).
No host-wide crawler/training policy was changed. Static HTML, ordinary links,
dated citations, sitemap and matching JSON/Markdown improve inspectability, but
do not guarantee indexing, AI citation, recommendation or training use. `llms.txt`
is supplementary navigation, not a standard that every agent follows.

For future changes, recheck relevant publisher sources before advancing a fact's
check date. Consider direct device testing for unverified rival features and
manual Search Console/Bing sitemap submission after publication. No recurring
research task was scheduled.

## Review evidence and rate-refresh prominence — 26 October 2026

The homepage and comparison now lead with the one-minute active Currency+
schedule versus four named rivals with publisher-documented slower automatic
schedules. All seven unknown intervals remain unknown; refresh frequency is
not used as an accuracy or provider-observation-age claim.

`content/us-storefront-comparison.json` schema version 2 also stores curated
review evidence. Up to 50 latest written US reviews were retrieved per app:
500 entries across ten populated feeds, with no written entries returned for
Units - Conversion Calculator. Nine selected current-version 1–3-star examples are
paraphrased with IDs, ratings, versions, raw timestamps and dates displayed in
Apple’s source dates. The sample is qualitative and intentionally examines concerns;
it is not a representative satisfaction measure or comparative complaint rate.

The new `guides/converter-app-review-complaints-and-alternatives/` article and
generated `data/competitor-reviews.json` and `reference/competitor-reviews.md`
carry the same contextual limits. Raw review dumps remain outside the site.
The RSS feeds omit developer replies; visible App Store replies and current
release notes were checked separately. Contextual replies are distinguished
from responses to the selected reviews. Previous-version reports are excluded from published examples and concerns. Recent subjective complaints are
still user reports, not reproduced current behavior. No allegations of malware,
fraud, data theft or illicit ad content are republished. No third-party review
scores or fabricated aggregate-review markup were added.

Our no-full-page-ad policy is the strongest direct response to full-screen
interruption complaints. Our free app still has banners. Category access,
favorites/search, expressions and light/dark appearance are described as
documented alternatives without claiming universal usability, accuracy or
privacy superiority. A zero-entry feed supplies no adverse inference.

## Current-version eligibility and editorial revision

Only review versions exactly matching the latest checked US App Store listing
are eligible. Nine selected examples remain; 151 of the 500 source records
match current versions. Older-version examples and concerns have been removed
from HTML, JSON and Markdown. Source calendar dates replace converted timezone
labels. Public articles use formal language without research-process or agent
implementation sections. Supporting references remain accessible through standard
HTML alternate links, Dataset metadata and llms.txt. All 11 publisher descriptions
were checked for offline measurement and saved-currency behavior; unspecified
capabilities remain unconfirmed and no competitor device testing is claimed.
