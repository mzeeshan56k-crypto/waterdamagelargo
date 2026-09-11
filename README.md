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

## SEO implementation

- Unique title + meta description + canonical (real domain) on all 38 pages
- `LocalBusiness` / `HomeAndConstructionBusiness` schema on every page
- `FAQPage` schema on every page with an accordion (home, services, locations, FAQ)
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
