# Conversion Calculator Plus — official website

Public marketing site for the iPhone/iPad app, served by GitHub Pages from the
root of `main`: https://developer-yl.github.io/convert-units-plus/ .
The App Store Marketing URL and Support URL use this site; `#support` and the
existing `privacy.html` remain valid. No framework, npm dependencies, runtime
server, tracking script or external font is required.

## Edit and rebuild

- `scripts/build_site.py`: shared page template, homepage, code reference and
  Simplified/Traditional Chinese pages. Standard Python 3 only.
- `content/articles.json`: nine original articles: one editorial best-app list,
  four competitor comparisons and four educational guides. Each has a headline,
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
