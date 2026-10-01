# Water Damage Restoration Largo — static site

Local-service SEO site for **Water Damage Restoration Largo** (Largo, FL).
Plain static HTML: no build step, no framework, no dependencies. One CSS file, one JS file.

- **Domain:** https://waterdamagerestorationlargo.com
- **Phone:** +1 833-289-9993 (inbound calls only — no forms, email, SMS or social channels)
- **Pages:** 38 HTML pages + sitemap.xml + robots.txt + vercel.json

## Structure

```
index.html                     Home
service/index.html             Services index
service/<slug>/index.html      15 service pages
fl/index.html                  Service areas index
fl/<area>/index.html           11 city / location pages
blog/index.html                Blog index
blog/<slug>/index.html         3 articles
about-us/ contact-us/ faq/ privacy-policy/ terms-of-service/
assets/site.css                All styles
assets/site.js                 Mega menus, drawer, accordions, scroll reveal
assets/*.jpg                   Photography (SEO-named)
_data/*.json                   Source content (services, areas, blog, pages)
sitemap.xml  robots.txt  vercel.json
```

All internal links are **absolute** on the brand domain
(`https://waterdamagerestorationlargo.com/...`), so every link, canonical, `og:url`
and sitemap entry names the same host. Every URL is a directory with `index.html`,
matching the `/service/<slug>/` and `/fl/<area>/` URL patterns, and every internal
link carries a trailing slash to match `trailingSlash: true`.

Asset references (`assets/*`, CSS, JS, images, favicon) are deliberately left
**relative** so pages still render on a preview deployment or when opened from disk.
Note the trade-off: because navigation links are absolute, clicking a link on a
preview deployment or a local copy jumps to the live production domain.

## Content source of truth

Page copy lives in `_data/`:

| File | Contents |
| --- | --- |
| `services-a.json`, `services-b.json` | 15 services: intro, scope, process, local sections, signs, FAQs, related services, 300+ char card description |
| `areas.json` | 11 locations: utility, permitting authority, geography, housing/pipe eras, neighborhoods, "Good to know", FAQs |
| `blog.json` | 3 articles with body blocks and contextual link phrases |
| `pages.json` | Home sections, About, Contact, FAQ, Privacy, Terms |

Pages were generated from a single shared template (head, header with two two-column
mega-menus, mobile drawer, breadcrumbs, CTA blocks, footer, schema). To change the
header, footer, or schema everywhere, edit the template block and regenerate — do not
hand-edit 40 files.

## Deploying to Vercel

```
vercel deploy --prod
```

`vercel.json` sets `trailingSlash: true`, one-year immutable caching on `/assets/*`,
basic security headers, and legacy redirects (`/services`, `/contact`, `/about`).
Any static host works: upload the repo root as-is.

## Consolidated pages

`/service/water-damage-restoration/` and `/fl/largo/` were removed and 301 redirect
to `/` in `vercel.json`. The core "water damage restoration Largo FL" term and its
secondary variants (company, experts, contractors, repair, cleanup, mitigation,
emergency water removal, flood damage restoration) are targeted on the home page,
which carries the absorbed scope content and a `Service` schema block. Largo is
still a served city everywhere in copy and in `areaServed` schema - it simply has
no separate location page.

## Card links and images

Each card links once, from its heading. The duplicate `.more` button that
repeated the same href with "<name> details" anchor text was removed site-wide
(179 of them); Google counts the first link's anchor anyway, so the second was
redundant. On `fl/index.html` the button carried a better anchor than the
heading ("Clearwater water damage restoration" vs "Clearwater, FL"), so those
headings were rewritten to carry that text before the buttons were removed.

Home page service cards carry the same photo as the service page they link to,
pulled from the `img`/`alt` fields in `_data`. Images are full-bleed to the card
edge via a negative margin on `.card img`, fixed at 16:10, with intrinsic
width/height so nothing shifts while they load.

## Home page intent

The home page is commercial-intent. It answers "who do I hire, what will it
cost, how does insurance work, do they cover me" rather than teaching water
damage theory. The long "Why Water Damage Behaves Differently in Largo" essay
was moved off it in favour of a hiring/cost/insurance section, and the blog
teaser block was reduced to a chips row that keeps the internal links without
the informational copy. Educational depth lives on the blog and the service
pages, which is where that intent belongs.

Claims on the home page must stay consistent with the footer disclaimer: this
site connects owners with independent contractors, does not warrant work, and
tells owners to verify license and insurance themselves. Do not add copy that
asserts the site itself is licensed and insured, or that it is the contractor.

## Keyword targeting and cannibalization

One page owns each commercial term. Only the home page title may lead with
"Water Damage Restoration Largo" - service pages lead with their own service,
location pages with their own city, and about/contact lead with their own
intent. Four pages previously led with the home page's phrase and the terms of
service page began picking up impressions for `water mitigation largo` and
`water damage restoration largo`; that is what the current titles prevent.

`privacy-policy/` and `terms-of-service/` are `noindex,follow`, carry no
`LocalBusiness` schema, and are excluded from `sitemap.xml`. They stay linked
and crawlable, so they still serve their trust purpose, but they cannot compete
for commercial queries. Revert by restoring `index,follow` if you ever want
them indexed.

The home page targets `water damage restoration largo fl`, `water mitigation
largo` and the secondary variants, with a dedicated water mitigation section
explaining mitigation versus restoration.

## Search Console verification

Every page carries the Google Search Console HTML-tag verification meta in the
first `<head>` block, immediately after the viewport meta:

```html
<meta name="google-site-verification" content="3Q3ksU9_4hkk9nWfRx_BhyDGSo-MuKHMrkOWiuqok04" />
```

Google only reads it on the verified URL (the home page for a URL-prefix
property), but it is on all 38 pages so verification still passes if the
property is ever set to a subpath. Leave the tag in place after verification -
Google rechecks periodically and removing it un-verifies the property. A domain
property uses a DNS TXT record instead and ignores this tag.

## SEO implementation

- Unique title + meta description + canonical (real domain) on all 38 pages
- `LocalBusiness` / `HomeAndConstructionBusiness` schema on every page
- **10 FAQs on every content page** (36 of 38 pages; the privacy policy and terms
  carry none by design), each answer 2-3 lines, written for answer-engine and LLM
  citation as well as rich results
- `FAQPage` schema on every page with an accordion, one block per page, kept in
  sync with the visible accordion and with the `faqs` arrays in `_data/`
- `BlogPosting` schema on articles, `Service` schema on service pages, `BreadcrumbList` on all inner pages
- Breadcrumbs rendered on every inner page
- Descriptive keyword-relevant `alt` text on every image; `width`/`height` set to reserve space
- Below-fold images `loading="lazy" decoding="async"`; hero images `fetchpriority="high"`
- Interlinking: services ↔ locations ↔ blog, related-services block on each service page,
  service cards with the service name as anchor text on every page

## Compliance rules baked in

- No 24/7, same-day, around-the-clock or response-time claims. Copy uses
  "confirmed arrival window" and "availability confirmed when you call".
- No free quote/estimate language anywhere.
- No reviews or testimonials section, and no review schema.
- Inbound calls only: no contact form, email intake, SMS or social links.
- Footer carries the required contractor/actor disclaimer verbatim on every page.

## QA results (last run)

- 38 pages checked; **0** broken internal links, **0** missing images
- 371 FAQs total; 370 unique questions; visible accordion and FAQPage schema counts match on every page
- Word counts: min above 1,000 — average ≈ 1,930 words per page
- Exactly one `<h1>` per page; no duplicate titles
- No banned availability or estimate claims
- Every image has descriptive alt text (no `image1.jpg` style filenames)

Re-run these checks after any content edit.

## Editing notes

- Palette and type are defined as CSS custom properties at the top of `assets/site.css`
  (navy `#0b2c4d`, blue `#1668b3`, cyan `#35a7e0`, orange `#f5821f`) — pulled from the logo.
- Fonts: Archivo (display) + Source Sans 3 (body), loaded from Google Fonts.
- Section rhythm: white → light tint → one dark section per page. Two background colors max.
- Motion: IntersectionObserver fade-up on `.rv` elements, hover lift on cards,
  `<details>` accordions. All motion is disabled under `prefers-reduced-motion`.
