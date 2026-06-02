#!/usr/bin/env python3
"""Generate Nassau Cruise Excursions static site files."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://nassaucruiseexcursions.com"
SITE = "Nassau Cruise Excursions"
DATE = "2026-06-02"


def page_shell(
    *,
    title: str,
    description: str,
    keywords: str,
    canonical_path: str,
    data_page: str,
    hero: str,
    content: str,
    preload: str = "images/hero-nassau.jpg",
    schema: dict | None = None,
    trust: bool = True,
) -> str:
    canon = f"{DOMAIN}/{canonical_path}".rstrip("/") if canonical_path else f"{DOMAIN}/"
    if canonical_path and not canonical_path.endswith(".html") and canonical_path != "":
        canon = f"{DOMAIN}/{canonical_path}"
    schema_block = ""
    if schema:
        schema_block = (
            f'  <script type="application/ld+json">\n'
            f"{json.dumps(schema, indent=2)}\n"
            f"  </script>\n"
        )
    trust_attr = '\n  data-trust-strip="partials/trust-strip.html"' if trust else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <title>{title}</title>
  <meta name="description" content="{description}" />
  <meta name="keywords" content="{keywords}" />
  <link rel="canonical" href="{canon}" />
  <link rel="preload" as="image" href="{preload}" fetchpriority="high" />

  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canon}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:image" content="{DOMAIN}/{preload}" />
  <meta property="og:site_name" content="{SITE}" />
  <meta name="twitter:card" content="summary_large_image" />

{schema_block}
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="js/tailwind-config.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="css/site.css" />
</head>
<body
  class="bg-white text-gray-800 antialiased"
  data-page="{data_page}"
  data-base=""
  data-hero="{hero}"
  data-content="{content}"{trust_attr}
>

  <div id="site-nav"></div>
  <div id="page-hero"></div>
  <div id="page-trust-strip"></div>
  <main id="page-content"></main>
  <div id="site-footer"></div>

  <script src="js/site.js"></script>
</body>
</html>
"""


def write(path: str, content: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"  wrote {path}")


def main() -> None:
    print("Building Nassau site…")

    write(
        "partials/nav.html",
        """<nav class="fixed top-0 left-0 right-0 z-50 bg-white/90 border-b border-ocean-100 shadow-sm">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex items-center justify-between h-12">
      <a href="index.html" class="flex items-center gap-2">
        <div class="w-7 h-7 rounded-full btn-ocean flex items-center justify-center">
          <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14H9V8h2v8zm4 0h-2V8h2v8z"/>
          </svg>
        </div>
        <span class="font-display font-semibold text-ocean-800 text-base leading-tight">Nassau<br/><span class="text-[10px] font-body font-normal text-teal-600 tracking-widest uppercase">Cruise Excursions</span></span>
      </a>
      <div class="hidden lg:flex items-center gap-6 text-sm font-medium">
        <a href="index.html" data-nav="home" class="text-gray-600 hover:text-ocean-600 transition-colors">Home</a>
        <a href="best-nassau-cruise-excursions.html" data-nav="excursions" class="text-gray-600 hover:text-ocean-600 transition-colors">Excursions</a>
        <a href="nassau-beaches.html" data-nav="beaches" class="text-gray-600 hover:text-ocean-600 transition-colors">Beaches</a>
        <a href="nassau-snorkelling-tours.html" data-nav="snorkelling" class="text-gray-600 hover:text-ocean-600 transition-colors">Snorkelling</a>
        <a href="nassau-private-tours.html" data-nav="private" class="text-gray-600 hover:text-ocean-600 transition-colors">Private Tours</a>
        <a href="nassau-cruise-port-guide.html" data-nav="port" class="text-gray-600 hover:text-ocean-600 transition-colors">Port Guide</a>
      </div>
      <a href="best-nassau-cruise-excursions.html" class="hidden md:inline-flex items-center gap-2 btn-ocean text-white text-sm font-semibold px-4 py-2 rounded-full shadow-md">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
        Book a Tour
      </a>
      <button type="button" class="lg:hidden p-2 rounded-lg text-gray-600 hover:bg-ocean-50" aria-label="Open menu">
        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
      </button>
    </div>
  </div>
</nav>
""",
    )

    write(
        "partials/footer.html",
        f"""  <footer class="bg-gray-900 text-gray-400 py-14">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-10 mb-12">
        <div class="sm:col-span-2 lg:col-span-1">
          <a href="index.html" class="font-display font-semibold text-white text-lg">{SITE}</a>
          <p class="mt-3 text-sm leading-relaxed">Planning guide for cruise visitors to Nassau, Bahamas. Not affiliated with any cruise line.</p>
        </div>
        <div>
          <h3 class="text-white text-sm font-semibold uppercase tracking-wider mb-4">Excursions</h3>
          <ul class="space-y-2 text-sm">
            <li><a href="best-nassau-cruise-excursions.html" class="hover:text-white transition-colors">All Excursions</a></li>
            <li><a href="atlantis-resort-excursions.html" class="hover:text-white transition-colors">Atlantis Resort</a></li>
            <li><a href="swimming-pigs-excursions.html" class="hover:text-white transition-colors">Swimming Pigs</a></li>
            <li><a href="nassau-beaches.html" class="hover:text-white transition-colors">Beaches</a></li>
            <li><a href="nassau-snorkelling-tours.html" class="hover:text-white transition-colors">Snorkelling</a></li>
            <li><a href="nassau-private-tours.html" class="hover:text-white transition-colors">Private Tours</a></li>
          </ul>
        </div>
        <div>
          <h3 class="text-white text-sm font-semibold uppercase tracking-wider mb-4">Resources</h3>
          <ul class="space-y-2 text-sm">
            <li><a href="nassau-cruise-port-guide.html" class="hover:text-white transition-colors">Port Guide</a></li>
            <li><a href="one-day-in-nassau.html" class="hover:text-white transition-colors">One Day in Nassau</a></li>
            <li><a href="nassau-faq.html" class="hover:text-white transition-colors">FAQ</a></li>
          </ul>
        </div>
      </div>
      <div class="border-t border-gray-800 pt-8 text-xs text-center sm:text-left">
        <p>&copy; 2026 {SITE}. Verify times and prices with operators before booking.</p>
      </div>
    </div>
  </footer>
""",
    )

    write(
        "partials/trust-strip.html",
        f"""<section class="trust-strip" aria-label="Nassau cruise excursion highlights">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <ul class="trust-strip__list">
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> Cruise Friendly Planning</li>
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> Atlantis &amp; Paradise Island</li>
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> Beach &amp; Snorkelling Tours</li>
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> Swimming Pigs Day Trips</li>
    </ul>
  </div>
</section>
""",
    )

    # Heroes
    heroes = {
        "hero-home.html": _hero_home(),
        "hero-excursions.html": _hero_excursions(),
        "hero-port-guide.html": _hero_port(),
        "hero-one-day.html": _hero_one_day(),
        "hero-beaches.html": _hero_beaches(),
        "hero-snorkelling.html": _hero_snorkelling(),
        "hero-private.html": _hero_private(),
        "hero-faq.html": _hero_faq(),
        "hero-atlantis.html": _hero_atlantis(),
        "hero-swimming-pigs.html": _hero_pigs(),
    }
    for name, html in heroes.items():
        write(f"partials/{name}", html)

    # Content
    contents = {
        "home.html": _content_home(),
        "best-nassau-cruise-excursions.html": _content_best(),
        "nassau-cruise-port-guide.html": _content_port(),
        "one-day-in-nassau.html": _content_one_day(),
        "nassau-beaches.html": _content_beaches(),
        "atlantis-resort-excursions.html": _content_atlantis(),
        "swimming-pigs-excursions.html": _content_pigs(),
        "nassau-snorkelling-tours.html": _content_snorkelling(),
        "nassau-private-tours.html": _content_private(),
        "nassau-faq.html": _content_faq(),
    }
    for name, html in contents.items():
        write(f"content/{name}", html)

    pages = [
        dict(
            file="index.html",
            title=f"{SITE} | Best Cruise Port Tours &amp; Bahamas Adventures",
            description="Discover the best Nassau cruise excursions for cruise passengers — Atlantis, swimming pigs, beaches, snorkelling, private tours and Paradise Island adventures.",
            keywords="Nassau cruise excursions, Nassau shore excursions, Nassau tours from cruise port, Bahamas cruise port tours, Paradise Island excursions",
            path="",
            data_page="home",
            hero="partials/hero-home.html",
            content="content/home.html",
            schema={
                "@context": "https://schema.org",
                "@type": "WebSite",
                "name": SITE,
                "url": f"{DOMAIN}/",
                "description": "Planning guide for Nassau cruise shore excursions in the Bahamas",
            },
        ),
        dict(
            file="best-nassau-cruise-excursions.html",
            title="Best Nassau Cruise Excursions | Cruise Port Tours &amp; Island Adventures",
            description="Browse the best Nassau cruise excursions — Atlantis day passes, swimming pigs, Cable Beach, snorkelling sails and private Bahamas tours with cruise-friendly timing.",
            keywords="best Nassau cruise excursions, Nassau shore excursions, Bahamas cruise port tours, Paradise Island excursions, Nassau day trips",
            path="best-nassau-cruise-excursions.html",
            data_page="excursions",
            hero="partials/hero-excursions.html",
            content="content/best-nassau-cruise-excursions.html",
            schema={
                "@context": "https://schema.org",
                "@type": "WebPage",
                "name": "Best Nassau Cruise Excursions",
                "url": f"{DOMAIN}/best-nassau-cruise-excursions.html",
                "description": "Hub comparing Nassau cruise shore excursions for cruise passengers",
            },
        ),
        dict(
            file="nassau-cruise-port-guide.html",
            title="Nassau Cruise Port Guide for Cruise Passengers",
            description="Complete Nassau cruise port guide — Prince George Wharf, Paradise Island ferries, taxis, beaches, shore excursions and how to plan your Bahamas port day.",
            keywords="Nassau cruise port guide, Prince George Wharf, Paradise Island ferry, Nassau port day, Nassau taxis, cruise passenger guide Nassau",
            path="nassau-cruise-port-guide.html",
            data_page="port",
            hero="partials/hero-port-guide.html",
            content="content/nassau-cruise-port-guide.html",
            preload="images/cruise-port.jpg",
            schema={
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": "Nassau Cruise Port Guide",
                "url": f"{DOMAIN}/nassau-cruise-port-guide.html",
            },
        ),
        dict(
            file="one-day-in-nassau.html",
            title="One Day in Nassau from a Cruise Ship | Port Day Itineraries",
            description="How to spend one day in Nassau on a cruise stop — sample itineraries for beaches, Atlantis, swimming pigs, downtown Bay Street and snorkelling with return-to-ship timing.",
            keywords="one day in Nassau cruise ship, Nassau port day itinerary, Nassau cruise stop planning, Bahamas one day cruise",
            path="one-day-in-nassau.html",
            data_page="port",
            hero="partials/hero-one-day.html",
            content="content/one-day-in-nassau.html",
        ),
        dict(
            file="nassau-beaches.html",
            title="Nassau Beaches for Cruise Passengers | Cable Beach &amp; Paradise Island",
            description="Best Nassau beaches for cruise passengers — Cable Beach, Cabbage Beach, Junkanoo Beach and resort beach days with travel times from Prince George Wharf.",
            keywords="Nassau beaches cruise passengers, Cable Beach Nassau, Cabbage Beach Paradise Island, Junkanoo Beach, Nassau beach guide",
            path="nassau-beaches.html",
            data_page="beaches",
            hero="partials/hero-beaches.html",
            content="content/nassau-beaches.html",
            preload="images/nassau-beach.jpg",
        ),
        dict(
            file="atlantis-resort-excursions.html",
            title="Atlantis Resort Excursions from Nassau Cruise Port",
            description="Plan Atlantis Paradise Island excursions from Nassau — day passes, Aquaventure, marine habitats and beach club access with cruise-friendly transfers from the port.",
            keywords="Atlantis resort excursions Nassau, Atlantis day pass cruise, Aquaventure Nassau, Paradise Island Atlantis cruise, Bahamas Atlantis shore excursion",
            path="atlantis-resort-excursions.html",
            data_page="excursions",
            hero="partials/hero-atlantis.html",
            content="content/atlantis-resort-excursions.html",
            preload="images/private-vip-island-tour.jpg",
        ),
        dict(
            file="swimming-pigs-excursions.html",
            title="Swimming Pigs Excursions from Nassau | Rose Island &amp; Exuma Day Trips",
            description="Swimming pigs excursions from Nassau cruise port — Rose Island pig beach, boat tours and longer Exuma Cays day trips built around your ship schedule.",
            keywords="swimming pigs excursions Nassau, Rose Island swimming pigs, Exuma pigs from Nassau, Bahamas pig beach cruise excursion",
            path="swimming-pigs-excursions.html",
            data_page="excursions",
            hero="partials/hero-swimming-pigs.html",
            content="content/swimming-pigs-excursions.html",
            preload="images/catamaran-snorkel-sail.jpg",
        ),
        dict(
            file="nassau-snorkelling-tours.html",
            title="Nassau Snorkelling Tours | Reef &amp; Catamaran Cruise Excursions",
            description="Nassau snorkelling tours for cruise guests — Rose Island reefs, catamaran snorkel sails, reef parks and clear Bahamian water with operators who plan around all aboard.",
            keywords="Nassau snorkelling tours, Nassau snorkel cruise excursion, Rose Island snorkelling, Bahamas catamaran snorkel Nassau",
            path="nassau-snorkelling-tours.html",
            data_page="snorkelling",
            hero="partials/hero-snorkelling.html",
            content="content/nassau-snorkelling-tours.html",
            preload="images/snorkeling-tour.jpg",
        ),
        dict(
            file="nassau-private-tours.html",
            title="Nassau Private Tours | Custom Cruise Port Shore Excursions",
            description="Private Nassau tours for cruise passengers — custom island drives, beach hops, Atlantis visits and swimming pigs with flexible timing for your group.",
            keywords="Nassau private tours, private Nassau shore excursion, custom Bahamas cruise tour, Nassau VIP tour cruise port",
            path="nassau-private-tours.html",
            data_page="private",
            hero="partials/hero-private.html",
            content="content/nassau-private-tours.html",
            preload="images/private-tour.jpg",
        ),
        dict(
            file="nassau-faq.html",
            title="Nassau Cruise Excursions FAQ | Port Day Planning Answers",
            description="FAQ for Nassau cruise excursions — port timing, currency, Atlantis tickets, swimming pigs tours, taxis, beaches and independent vs ship excursions.",
            keywords="Nassau cruise excursions FAQ, Nassau port questions, Bahamas cruise port FAQ, Nassau shore excursion advice",
            path="nassau-faq.html",
            data_page="port",
            hero="partials/hero-faq.html",
            content="content/nassau-faq.html",
            schema={
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": "How much time do cruise ships spend in Nassau?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Most ships are in port 7 to 10 hours. Half-day tours work well; full-day Exuma pig trips need an early departure and a longer port call.",
                        },
                    },
                    {
                        "@type": "Question",
                        "name": "Can I visit Atlantis on a cruise day?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Yes. Book an Atlantis day pass or organised excursion with ferry or transfer time from Prince George Wharf factored in.",
                        },
                    },
                    {
                        "@type": "Question",
                        "name": "What currency is used in Nassau?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "The Bahamian dollar is official; US dollars are widely accepted at par for most tourist purchases.",
                        },
                    },
                ],
            },
        ),
    ]

    for p in pages:
        write(
            p["file"],
            page_shell(
                title=p["title"],
                description=p["description"],
                keywords=p["keywords"],
                canonical_path=p["path"],
                data_page=p["data_page"],
                hero=p["hero"],
                content=f"content/{p['content'].split('/')[-1]}",
                preload=p.get("preload", "images/hero-nassau.jpg"),
                schema=p.get("schema"),
            ),
        )

    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")

    urls = [
        ("", "1.0", "weekly"),
        ("best-nassau-cruise-excursions.html", "0.9", "monthly"),
        ("nassau-cruise-port-guide.html", "0.8", "monthly"),
        ("one-day-in-nassau.html", "0.8", "monthly"),
        ("nassau-beaches.html", "0.8", "monthly"),
        ("atlantis-resort-excursions.html", "0.8", "monthly"),
        ("swimming-pigs-excursions.html", "0.8", "monthly"),
        ("nassau-snorkelling-tours.html", "0.8", "monthly"),
        ("nassau-private-tours.html", "0.8", "monthly"),
        ("nassau-faq.html", "0.7", "monthly"),
    ]
    sitemap_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, priority, freq in urls:
        path = loc if loc else ""
        url = f"{DOMAIN}/{path}"
        sitemap_lines.append("  <url>")
        sitemap_lines.append(f"    <loc>{url}</loc>")
        sitemap_lines.append(f"    <lastmod>{DATE}</lastmod>")
        sitemap_lines.append(f"    <changefreq>{freq}</changefreq>")
        sitemap_lines.append(f"    <priority>{priority}</priority>")
        sitemap_lines.append("  </url>")
    sitemap_lines.append("</urlset>")
    write("sitemap.xml", "\n".join(sitemap_lines) + "\n")

    write(
        "template.html",
        f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Page Title | {SITE}</title>
  <meta name="description" content="Write a unique meta description for this page (150–160 characters)." />
  <link rel="canonical" href="{DOMAIN}/page-slug.html" />
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="js/tailwind-config.js"></script>
  <link rel="stylesheet" href="css/site.css" />
</head>
<body class="bg-white text-gray-800 antialiased" data-page="excursions" data-hero="partials/hero-inner.html" data-content="content/page-starter.html">
  <div id="site-nav"></div>
  <div id="page-hero"></div>
  <main id="page-content"></main>
  <div id="site-footer"></div>
  <script src="js/site.js"></script>
</body>
</html>
""",
    )

    # package.json + wrangler for deploy
    write(
        "package.json",
        """{
  "name": "nassau-cruise-excursions",
  "private": true,
  "scripts": {
    "build": "python3 scripts/build-nassau-site.py",
    "deploy": "wrangler deploy",
    "preview": "python3 -m http.server 8898"
  },
  "devDependencies": {
    "wrangler": "^4.94.0"
  }
}
""",
    )
    write(
        "wrangler.jsonc",
        """{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "nassau-cruise-excursions",
  "compatibility_date": "2026-06-02",
  "observability": { "enabled": true },
  "assets": { "directory": "." },
  "routes": [
    {
      "pattern": "nassaucruiseexcursions.com",
      "custom_domain": true
    }
  ]
}
""",
    )
    write(
        "deploy.sh",
        f"""#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -f node_modules/.bin/wrangler ]]; then
  npm install
fi

echo "Deploying {SITE} to Cloudflare..."
npx wrangler deploy

echo "Done. Check {DOMAIN}/ shortly."
""",
    )

    # Patch CSS image paths
    css_path = ROOT / "css" / "site.css"
    css = css_path.read_text(encoding="utf-8")
    css = css.replace("magens-bay-beach.jpg", "nassau-beach.jpg")
    css = css.replace("hero-st-thomas-magens-bay.jpg", "hero-nassau.jpg")
    css = css.replace("kayak-hike-snorkel-st-thomas.jpg", "kayak-snorkel-nassau.jpg")
    css_path.write_text(css, encoding="utf-8")
    print("  patched css/site.css")

    print("Done.")


# --- Hero partials (abbreviated in separate functions) ---

def _hero_wave() -> str:
    return '<div class="absolute bottom-0 left-0 right-0"><svg viewBox="0 0 1440 48" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" class="site-hero__wave" aria-hidden="true"><path d="M0 24 C360 48 1080 0 1440 24 L1440 48 L0 48 Z" fill="white"/></svg></div>'


def _hero_home() -> str:
    return f"""  <section class="site-hero">
    <div class="absolute inset-0 hero-bg" role="img" aria-label="Turquoise water and white sand beach near Nassau, Bahamas cruise port"></div>
    <div class="site-hero__inner max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="max-w-3xl">
        <div class="site-hero__eyebrow inline-flex items-center gap-2 bg-white/15 backdrop-blur-sm border border-white/30 rounded-full px-4 py-1.5 mb-3">
          <span class="w-2 h-2 rounded-full bg-teal-400 animate-pulse"></span>
          <span class="text-white/90 text-xs font-semibold tracking-widest uppercase">Bahamas · New Providence</span>
        </div>
        <h1 class="site-hero__title text-4xl sm:text-5xl lg:text-[3.25rem] font-display font-bold text-white leading-tight mb-3">
          Discover the Best<br/><span class="text-teal-300">Nassau Cruise</span><br/>Excursions
        </h1>
        <p class="site-hero__lead text-base sm:text-lg text-white/85 font-light leading-relaxed mb-5 max-w-2xl">
          Atlantis, swimming pigs, Cable Beach, reef snorkelling and private island tours — planned around your cruise schedule in the Bahamas capital.
        </p>
        <div class="site-hero__actions flex flex-col sm:flex-row gap-3">
          <a href="best-nassau-cruise-excursions.html" class="btn-primary inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm shadow-xl">Explore Excursions</a>
          <a href="nassau-private-tours.html" class="btn-outline inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm">Private Tours</a>
        </div>
        <div class="site-hero__tags flex flex-wrap gap-2 mt-5 pt-4 border-t border-white/20">
          <span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">Atlantis</span>
          <span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">Swimming Pigs</span>
          <span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">Beach Days</span>
          <span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">Snorkelling</span>
        </div>
      </div>
    </div>
    {_hero_wave()}
  </section>"""


def _hero_excursions() -> str:
    return _hero_inner(
        "Cruise Port · Nassau Bahamas",
        "Best Nassau<br/><span class=\"text-teal-300\">Cruise Excursions</span>",
        "Compare Atlantis passes, swimming pigs, beaches, snorkelling sails and private tours built for your ship's timetable.",
        "images/hero-nassau.jpg",
        "Aerial view of turquoise Bahamian waters near Nassau for cruise shore excursions",
    )


def _hero_port() -> str:
    return _hero_inner(
        "Complete Cruise Passenger Guide",
        "Nassau<br/><span class=\"text-teal-300\">Cruise Port Guide</span>",
        "Prince George Wharf, Paradise Island ferries, taxis, beaches and how to make the most of your Bahamas port day.",
        "images/cruise-port.jpg",
        "Cruise ships docked at Nassau harbour with downtown waterfront and Paradise Island",
        breadcrumb="Cruise Port Guide",
        cta=("best-nassau-cruise-excursions.html", "View Shore Excursions →"),
        tags=["🚢 Prince George Wharf", "⛴️ Paradise Island", "🏖️ Beaches", "🚕 Taxis"],
    )


def _hero_one_day() -> str:
    return _hero_inner(
        "Cruise Port Planning Guide",
        "One Perfect Day<br/><span class=\"text-teal-300\">in Nassau</span>",
        "Sample itineraries for beaches, Atlantis, swimming pigs, downtown Bay Street and snorkelling with return-to-ship timing.",
        "images/hero-nassau.jpg",
        "Nassau Bahamas harbour and turquoise Caribbean water for cruise day planning",
        breadcrumb="One Day in Nassau",
    )


def _hero_beaches() -> str:
    return _hero_inner(
        "Nassau · Bahamas · Caribbean",
        "Best <span class=\"text-teal-300\">Nassau Beaches</span><br/>for Cruise Guests",
        "Cable Beach, Cabbage Beach on Paradise Island and calm bays — all reachable on a typical port day.",
        "images/nassau-beach.jpg",
        "White sand beach with turquoise water at Cable Beach near Nassau Bahamas",
        breadcrumb="Nassau Beaches",
    )


def _hero_snorkelling() -> str:
    return _hero_inner(
        "Nassau · Bahamas · Caribbean",
        "Nassau <span class=\"text-teal-300\">Snorkelling</span><br/>Tours",
        "Rose Island reefs, catamaran snorkel sails and clear Bahamian water with cruise-friendly return times.",
        "images/snorkeling-tour.jpg",
        "Snorkelling in clear turquoise water on a Nassau Bahamas reef tour",
        breadcrumb="Snorkelling Tours",
    )


def _hero_private() -> str:
    return _hero_inner(
        "Exclusive Private Shore Excursions",
        "Private Nassau Tours<br/><span class=\"text-violet-300\">Your Way</span>",
        "Custom island drives, beach hops, Atlantis visits and swimming pigs at your group's pace.",
        "images/private-tour.jpg",
        "Private tour vehicle with scenic Nassau Bahamas coastline for cruise passengers",
        breadcrumb="Private Nassau Tours",
    )


def _hero_faq() -> str:
    return _hero_inner(
        "Cruise Passenger Planning Guide",
        "Nassau Cruise<br/><span class=\"text-teal-300\">Excursions FAQ</span>",
        "Clear answers on port timing, currency, Atlantis, swimming pigs, taxis and independent excursions.",
        "images/hero-nassau.jpg",
        "Nassau Bahamas cruise port with harbour and island views",
        breadcrumb="FAQ",
    )


def _hero_atlantis() -> str:
    return _hero_inner(
        "Paradise Island · Bahamas",
        "Atlantis Resort<br/><span class=\"text-teal-300\">Excursions</span>",
        "Day passes, Aquaventure, marine habitats and beach club access with transfers from the cruise pier.",
        "images/private-vip-island-tour.jpg",
        "Atlantis Paradise Island resort towers and marina near Nassau Bahamas",
        breadcrumb="Atlantis Excursions",
    )


def _hero_pigs() -> str:
    return _hero_inner(
        "Bahamas Iconic Experience",
        "Swimming Pigs<br/><span class=\"text-teal-300\">Excursions</span>",
        "Rose Island pig beach and longer Exuma Cays boat trips — timed for cruise schedules.",
        "images/catamaran-snorkel-sail.jpg",
        "Boat excursion on turquoise Bahamian water for swimming pigs tour from Nassau",
        breadcrumb="Swimming Pigs",
    )


def _hero_inner(
    eyebrow: str,
    title: str,
    lead: str,
    image: str,
    aria: str,
    breadcrumb: str = "",
    cta: tuple[str, str] | None = None,
    tags: list[str] | None = None,
) -> str:
    bc = ""
    if breadcrumb:
        bc = f"""<nav class="site-hero__breadcrumb flex items-center gap-2 mb-4 text-xs text-white/60" aria-label="Breadcrumb">
        <a href="index.html" class="hover:text-white transition-colors">Home</a>
        <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
        <span class="text-white/80">{breadcrumb}</span>
      </nav>"""
    cta_html = ""
    if cta:
        cta_html = f'<a href="{cta[0]}" class="btn-ocean inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm shadow-xl">{cta[1]}</a>'
    tags_html = ""
    if tags:
        tags_html = '<div class="site-hero__tags flex flex-wrap gap-2 mt-5 pt-4 border-t border-white/20">' + "".join(
            f'<span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">{t}</span>'
            for t in tags
        ) + "</div>"
    return f"""<section class="site-hero">
  <div class="absolute inset-0 hero-bg-custom" style="background-image: linear-gradient(135deg, rgba(7, 89, 133, 0.72) 0%, rgba(13, 148, 136, 0.52) 60%, rgba(0, 0, 0, 0.35) 100%), url('{image}');" role="img" aria-label="{aria}"></div>
  <div class="site-hero__inner max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl">
      {bc}
      <div class="site-hero__eyebrow inline-flex items-center gap-2 bg-white/15 backdrop-blur-sm border border-white/30 rounded-full px-4 py-1.5 mb-3">
        <span class="w-2 h-2 rounded-full bg-teal-400 animate-pulse"></span>
        <span class="text-white/90 text-xs font-semibold tracking-widest uppercase">{eyebrow}</span>
      </div>
      <h1 class="site-hero__title text-4xl sm:text-5xl lg:text-[3.25rem] font-display font-bold text-white leading-tight mb-3">{title}</h1>
      <p class="site-hero__lead text-base sm:text-lg text-white/85 font-light leading-relaxed mb-5 max-w-2xl">{lead}</p>
      <div class="site-hero__actions flex flex-col sm:flex-row gap-3">{cta_html}</div>
      {tags_html}
    </div>
  </div>
  {_hero_wave()}
</section>"""


def _card_grid(cards: list[tuple]) -> str:
    items = []
    for img, alt, title, desc, link, label in cards:
        items.append(f"""<div class="card-hover bg-white rounded-3xl overflow-hidden shadow-md border border-blue-50 flex flex-col">
      <div class="card-media h-44 relative overflow-hidden">
        <img src="{img}" alt="{alt}" width="600" height="352" loading="lazy" decoding="async" />
      </div>
      <div class="p-6 flex flex-col flex-1">
        <h3 class="text-lg font-display font-semibold text-gray-900 mb-2">{title}</h3>
        <p class="text-sm text-gray-500 leading-relaxed flex-1">{desc}</p>
        <a href="{link}" class="mt-5 btn-ocean inline-flex items-center justify-center text-white text-xs font-semibold px-5 py-2.5 rounded-full">{label}</a>
      </div>
    </div>""")
    return '<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">' + "".join(items) + "</div>"


def _content_home() -> str:
    cards = _card_grid([
        ("images/beach-excursion.jpg", "Cable Beach Nassau with white sand and turquoise Bahamian water", "Nassau Beaches", "Cable Beach, Cabbage Beach and resort beach days a short taxi from Prince George Wharf.", "nassau-beaches.html", "Explore Beaches"),
        ("images/snorkeling-tour.jpg", "Snorkelling on a coral reef near Nassau Bahamas", "Snorkelling Tours", "Catamaran sails and Rose Island reef stops with gear included and cruise-friendly returns.", "nassau-snorkelling-tours.html", "View Snorkelling"),
        ("images/private-vip-island-tour.jpg", "Atlantis Paradise Island resort near Nassau cruise port", "Atlantis Resort", "Day passes, Aquaventure and marine habitats on Paradise Island with organised transfers.", "atlantis-resort-excursions.html", "Atlantis Guide"),
        ("images/catamaran-snorkel-sail.jpg", "Boat tour to swimming pigs beach in the Bahamas from Nassau", "Swimming Pigs", "Rose Island pig beach or full-day Exuma Cays adventures — confirm duration vs your port time.", "swimming-pigs-excursions.html", "Swimming Pigs"),
    ])
    return f"""<section class="pt-8 pb-16 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-center">
      <div>
        <div class="inline-flex items-center gap-2 text-ocean-600 text-xs font-semibold tracking-widest uppercase mb-3"><div class="w-8 h-px bg-ocean-400"></div>Bahamas Cruise Capital</div>
        <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 mb-5">Why Cruise Passengers<br/><span class="text-ocean-600">Love Nassau</span></h2>
        <p class="text-gray-600 leading-relaxed mb-5">Nassau is one of the Caribbean's busiest cruise ports, pairing a walkable downtown with Paradise Island's Atlantis resort, famous swimming pigs tours and easy beach escapes. Whether you want a relaxed Cable Beach afternoon or a high-energy Aquaventure day, Nassau fits almost every cruise style.</p>
        <p class="text-gray-600 leading-relaxed mb-8">Most excursions pick up near <strong>Prince George Wharf</strong> and plan returns with buffer time before your ship's all-aboard call.</p>
        <a href="best-nassau-cruise-excursions.html" class="btn-ocean inline-flex items-center gap-2 text-white font-semibold px-7 py-3.5 rounded-full text-sm shadow-lg">Browse All Excursions</a>
      </div>
      <div class="info-image rounded-3xl aspect-[4/3] shadow-2xl overflow-hidden">
        <img src="images/nassau-beach.jpg" alt="Turquoise water and white sand beach near Nassau Bahamas for cruise passengers" width="800" height="600" loading="lazy" decoding="async" />
      </div>
    </div></div></section>
    <section class="py-20 bg-amber-50"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-14"><h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900">Popular Nassau Excursion Types</h2>
      <p class="mt-4 text-gray-500 max-w-xl mx-auto">From Atlantis to swimming pigs — find the right Nassau experience for your port day.</p></div>
      {cards}
    </div></section>
    <section class="py-20 bg-ocean-800"><div class="max-w-3xl mx-auto px-4 text-center">
      <h2 class="text-3xl font-display font-bold text-white mb-4">Ready for Your Nassau Port Day?</h2>
      <p class="text-ocean-100 mb-8">Browse excursions, port tips and FAQs planned around your cruise schedule.</p>
      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <a href="best-nassau-cruise-excursions.html" class="btn-primary inline-flex items-center justify-center text-white font-semibold px-8 py-4 rounded-full">Browse Excursions</a>
        <a href="nassau-faq.html" class="btn-outline inline-flex items-center justify-center text-white font-semibold px-8 py-4 rounded-full">Read FAQs</a>
      </div>
    </div></section>"""


def _content_best() -> str:
    cards = _card_grid([
        ("images/beach-excursion.jpg", "Cable Beach Nassau with white sand and turquoise Bahamian water", "Nassau Beaches", "Cable Beach, Cabbage Beach and resort beach days a short taxi from Prince George Wharf.", "nassau-beaches.html", "Explore Beaches"),
        ("images/snorkeling-tour.jpg", "Snorkelling on a coral reef near Nassau Bahamas", "Snorkelling Tours", "Catamaran sails and Rose Island reef stops with gear included and cruise-friendly returns.", "nassau-snorkelling-tours.html", "View Snorkelling"),
        ("images/private-vip-island-tour.jpg", "Atlantis Paradise Island resort near Nassau cruise port", "Atlantis Resort", "Day passes, Aquaventure and marine habitats on Paradise Island with organised transfers.", "atlantis-resort-excursions.html", "Atlantis Guide"),
        ("images/catamaran-snorkel-sail.jpg", "Boat tour to swimming pigs beach in the Bahamas from Nassau", "Swimming Pigs", "Rose Island pig beach or full-day Exuma Cays adventures — confirm duration vs your port time.", "swimming-pigs-excursions.html", "Swimming Pigs"),
    ])
    return f"""<section class="pt-8 pb-12 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-center">
      <div>
        <div class="inline-flex items-center gap-2 text-ocean-600 text-xs font-semibold tracking-widest uppercase mb-3"><div class="w-8 h-px bg-ocean-400"></div>Compare &amp; Choose</div>
        <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 mb-5">Best Nassau Cruise<br/><span class="text-ocean-600">Excursions</span></h2>
        <p class="text-gray-600 leading-relaxed mb-5">Use this hub to match your port day with the right Bahamas experience — Atlantis day passes, half-day swimming pigs, reef snorkelling, Cable Beach time or a private driver who knows cruise all-aboard deadlines.</p>
        <p class="text-gray-600 leading-relaxed mb-8">Operators typically pick up at <strong>Prince George Wharf</strong> and build in 60 to 90 minutes of buffer before your ship sails.</p>
        <a href="nassau-cruise-port-guide.html" class="text-ocean-600 font-semibold text-sm hover:text-teal-600">Read the port guide →</a>
      </div>
      <div class="info-image rounded-3xl aspect-[4/3] shadow-2xl overflow-hidden">
        <img src="images/nassau-beach.jpg" alt="Turquoise water and white sand beach near Nassau Bahamas for cruise passengers" width="800" height="600" loading="lazy" decoding="async" />
      </div>
    </div></div></section>
    <section class="py-20 bg-amber-50"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-14"><h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900">Excursion Types</h2>
      <p class="mt-4 text-gray-500 max-w-xl mx-auto">From Atlantis to swimming pigs — find the right Nassau experience for your port day.</p></div>
      {cards}
    </div></section>"""


def _content_port() -> str:
    return """<section class="pt-8 pb-16 bg-white"><div class="max-w-3xl mx-auto px-4 text-center">
      <h2 class="text-3xl font-display font-bold text-gray-900 mb-6">Your First Look at Nassau Port</h2>
      <p class="text-gray-600 leading-relaxed">Most large ships dock at <strong>Prince George Wharf</strong> on New Providence, steps from Bay Street shopping and a short taxi or ferry ride to Paradise Island. Cruise calls typically run <strong>7 to 10 hours</strong> — enough for Atlantis, a beach afternoon or a swimming pigs boat tour if you leave early.</p>
    </div></section>
    <section id="where-ships-dock" class="py-16 bg-gray-50 scroll-mt-12"><div class="max-w-7xl mx-auto px-4">
      <h2 class="text-2xl font-display font-bold text-gray-900 text-center mb-10">Where Ships Dock</h2>
      <div class="grid lg:grid-cols-2 gap-8">
        <div class="bg-white rounded-3xl p-8 border border-gray-100 shadow-sm">
          <h3 class="font-display text-xl font-bold mb-3">Prince George Wharf</h3>
          <p class="text-sm text-gray-600 leading-relaxed">The main Nassau cruise pier. Walk to Straw Market, Bay Street boutiques and waterfront cafés. Taxis and tour pickups cluster at the terminal exit.</p>
        </div>
        <div class="bg-white rounded-3xl p-8 border border-gray-100 shadow-sm">
          <h3 class="font-display text-xl font-bold mb-3">Paradise Island Access</h3>
          <p class="text-sm text-gray-600 leading-relaxed">Atlantis and Cabbage Beach sit across the harbour. Reach them by organised excursion transfer, taxi over the bridge, or the passenger ferry from downtown — factor 20 to 40 minutes each way.</p>
        </div>
      </div>
    </div></section>
    <section class="py-16 bg-white"><div class="max-w-7xl mx-auto px-4">
      <h2 class="text-2xl font-display font-bold text-center mb-8">Quick Answers</h2>
      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 text-sm">
        <div class="bg-ocean-50 rounded-2xl p-6"><strong class="text-gray-900">Currency</strong><p class="mt-2 text-gray-600">Bahamian dollar (BSD); US dollars accepted at par in most tourist areas.</p></div>
        <div class="bg-teal-50 rounded-2xl p-6"><strong class="text-gray-900">Language</strong><p class="mt-2 text-gray-600">English is official — easy for North American and UK cruise guests.</p></div>
        <div class="bg-emerald-50 rounded-2xl p-6"><strong class="text-gray-900">Taxis</strong><p class="mt-2 text-gray-600">Fixed-rate zones from the pier; agree the fare before departing. Many drivers also offer island tours by the hour.</p></div>
      </div>
      <p class="text-center mt-10"><a href="one-day-in-nassau.html" class="text-ocean-600 font-semibold">See sample one-day itineraries →</a></p>
    </div></section>"""


def _content_one_day() -> str:
    return """<section id="itineraries" class="py-16 bg-white"><div class="max-w-7xl mx-auto px-4">
      <h2 class="text-3xl font-display font-bold text-center mb-12">Sample One-Day Itineraries</h2>
      <div class="grid lg:grid-cols-3 gap-8">
        <div class="bg-sky-50 rounded-3xl p-7 border border-sky-100">
          <h3 class="font-display font-bold text-lg mb-4">Atlantis &amp; Paradise Island</h3>
          <ul class="text-sm text-gray-600 space-y-2"><li><strong>8:30</strong> — Ferry or transfer to Paradise Island</li><li><strong>9:00</strong> — Atlantis day pass or beach club</li><li><strong>2:00</strong> — Return to downtown for shopping</li><li><strong>4:00</strong> — Back at pier with buffer</li></ul>
          <a href="atlantis-resort-excursions.html" class="mt-4 inline-block text-sky-700 font-semibold text-sm">Atlantis guide →</a>
        </div>
        <div class="bg-teal-50 rounded-3xl p-7 border border-teal-100">
          <h3 class="font-display font-bold text-lg mb-4">Beach &amp; Snorkel</h3>
          <ul class="text-sm text-gray-600 space-y-2"><li><strong>8:15</strong> — Meet catamaran snorkel tour</li><li><strong>9:00</strong> — Sail with reef stop at Rose Island</li><li><strong>1:00</strong> — Lunch near port</li><li><strong>4:30</strong> — All aboard buffer</li></ul>
          <a href="nassau-snorkelling-tours.html" class="mt-4 inline-block text-teal-700 font-semibold text-sm">Snorkelling tours →</a>
        </div>
        <div class="bg-amber-50 rounded-3xl p-7 border border-amber-100">
          <h3 class="font-display font-bold text-lg mb-4">Swimming Pigs Half Day</h3>
          <ul class="text-sm text-gray-600 space-y-2"><li><strong>8:00</strong> — Boat departs for Rose Island pigs</li><li><strong>10:30</strong> — Swim, photos, light snorkel</li><li><strong>12:30</strong> — Return to Nassau</li><li><strong>2:00</strong> — Optional downtown stroll</li></ul>
          <a href="swimming-pigs-excursions.html" class="mt-4 inline-block text-amber-700 font-semibold text-sm">Pig tours →</a>
        </div>
      </div>
    </div></section>"""


def _content_beaches() -> str:
    return """<section class="py-16 bg-white"><div class="max-w-7xl mx-auto px-4">
      <p class="text-center text-gray-600 max-w-2xl mx-auto mb-12">Nassau beaches are close to port — most cruise guests reach sand within 15 to 25 minutes by taxi.</p>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div class="card-hover bg-white rounded-3xl border p-5"><h3 class="font-display font-bold mb-2">Cable Beach</h3><p class="text-xs text-gray-500">Wide resort strip west of downtown; calm water, chair rentals and beach bars. ~15 min from pier.</p></div>
        <div class="card-hover bg-white rounded-3xl border p-5"><h3 class="font-display font-bold mb-2">Cabbage Beach</h3><p class="text-xs text-gray-500">Paradise Island's main public beach near Atlantis; lively on ship days. ~20 min with bridge traffic.</p></div>
        <div class="card-hover bg-white rounded-3xl border p-5"><h3 class="font-display font-bold mb-2">Junkanoo Beach</h3><p class="text-xs text-gray-500">Closest to downtown — walkable from the wharf for a quick dip between shopping stops.</p></div>
        <div class="card-hover bg-white rounded-3xl border p-5"><h3 class="font-display font-bold mb-2">Love Beach</h3><p class="text-xs text-gray-500">Quieter local favourite west of Cable Beach; snorkelling off the reef on calm days.</p></div>
      </div>
    </div></section>"""


def _content_atlantis() -> str:
    return """<section class="py-16 bg-white"><div class="max-w-3xl mx-auto px-4">
      <h2 class="text-2xl font-display font-bold text-gray-900 mb-6">Atlantis from the Cruise Port</h2>
      <p class="text-gray-600 leading-relaxed mb-4">Atlantis Paradise Island is Nassau's signature experience — water slides at Aquaventure, marine habitats, beaches and casinos (adults only). Cruise guests typically buy a <strong>day pass</strong> through the resort or a shore excursion that includes round-trip transfer.</p>
      <ul class="space-y-3 text-sm text-gray-600 mb-8">
        <li>✓ Book ahead on busy ship days — passes can sell out.</li>
        <li>✓ Allow 45 to 60 minutes total transfer time pier ↔ Paradise Island.</li>
        <li>✓ Wear water shoes for Aquaventure; bring a credit card for incidentals.</li>
      </ul>
      <a href="best-nassau-cruise-excursions.html" class="btn-ocean inline-flex text-white font-semibold px-6 py-3 rounded-full text-sm">Compare all excursions</a>
    </div></section>"""


def _content_pigs() -> str:
    return """<section class="py-16 bg-white"><div class="max-w-3xl mx-auto px-4">
      <h2 class="text-2xl font-display font-bold text-gray-900 mb-6">Swimming Pigs Near Nassau</h2>
      <p class="text-gray-600 leading-relaxed mb-4"><strong>Rose Island</strong> half-day tours are the most common pig encounter from Nassau — short boat ride, swim with pigs, often a snorkel stop. Full-day <strong>Exuma Cays</strong> flights or speedboat trips reach the famous Big Major Cay but need a longer port call (8+ hours ashore) and premium pricing.</p>
      <p class="text-gray-600 leading-relaxed mb-6">Confirm departure time, return guarantee and whether lunch is included before booking independently.</p>
      <a href="nassau-cruise-port-guide.html" class="text-ocean-600 font-semibold text-sm">Port timing guide →</a>
    </div></section>"""


def _content_snorkelling() -> str:
    return """<section class="py-16 bg-white"><div class="max-w-7xl mx-auto px-4">
      <div class="grid lg:grid-cols-2 gap-12 items-center">
        <div>
          <h2 class="text-2xl font-display font-bold mb-4">Top Nassau Snorkelling Options</h2>
          <p class="text-gray-600 text-sm leading-relaxed mb-4"><strong>Catamaran snorkel sails</strong> combine sailing, open bar (on many tours) and a reef stop — ideal for groups who want a social half day.</p>
          <p class="text-gray-600 text-sm leading-relaxed"><strong>Rose Island</strong> trips reach shallow reefs with parrotfish and sergeant majors; good for beginners. Reef-safe sunscreen is encouraged to protect Bahamian coral.</p>
        </div>
        <div class="card-media rounded-3xl overflow-hidden h-64">
          <img src="images/reef-snorkel-nassau.jpg" alt="Reef snorkelling with tropical fish on a Nassau Bahamas tour" width="600" height="400" loading="lazy" decoding="async" />
        </div>
      </div>
    </div></section>"""


def _content_private() -> str:
    return """<section id="private-tours" class="py-16 bg-white"><div class="max-w-3xl mx-auto px-4">
      <h2 class="text-2xl font-display font-bold mb-6">Why Book a Private Nassau Tour?</h2>
      <p class="text-gray-600 leading-relaxed mb-4">Private vans or SUVs let you combine Atlantis, Cable Beach, Queen's Staircase, Fort Fincastle and a pig beach stop in one customised loop — without waiting for a large coach group.</p>
      <p class="text-gray-600 leading-relaxed mb-6">Popular for families, multi-generational groups and anyone who wants a dedicated driver-guide who understands cruise all-aboard times.</p>
      <a href="best-nassau-cruise-excursions.html" class="btn-ocean inline-flex text-white font-semibold px-6 py-3 rounded-full text-sm">See excursion types</a>
    </div></section>"""


def _content_faq() -> str:
    return """<section class="py-16 bg-white"><div class="max-w-3xl mx-auto px-4 space-y-4">
      <details class="faq-item rounded-2xl border border-ocean-100 p-5"><summary class="font-semibold text-gray-900 cursor-pointer">How much time do I need in Nassau port?</summary>
        <p class="mt-4 text-sm text-gray-500">Most ships allow 7 to 10 hours. Half-day tours (3–4 hours) suit swimming pigs or snorkel sails; Atlantis often needs 5 to 6 hours with transfers.</p></details>
      <details class="faq-item rounded-2xl border border-ocean-100 p-5"><summary class="font-semibold text-gray-900 cursor-pointer">Is Nassau safe for independent exploration?</summary>
        <p class="mt-4 text-sm text-gray-500">Tourist areas around the pier, Bay Street and organised excursions are heavily visited. Use official taxis, avoid isolated areas at night, and keep valuables secure — as in any busy port city.</p></details>
      <details class="faq-item rounded-2xl border border-ocean-100 p-5"><summary class="font-semibold text-gray-900 cursor-pointer">Can I walk to beaches from the cruise pier?</summary>
        <p class="mt-4 text-sm text-gray-500">Junkanoo Beach is walkable. Cable Beach and Paradise Island beaches require a taxi, ferry or excursion transfer.</p></details>
      <details class="faq-item rounded-2xl border border-ocean-100 p-5"><summary class="font-semibold text-gray-900 cursor-pointer">Do I need Bahamian cash?</summary>
        <p class="mt-4 text-sm text-gray-500">US dollars work almost everywhere. Small vendors may prefer cash; ATMs are at the terminal and downtown.</p></details>
      <details class="faq-item rounded-2xl border border-ocean-100 p-5"><summary class="font-semibold text-gray-900 cursor-pointer">Ship excursion or book independently?</summary>
        <p class="mt-4 text-sm text-gray-500">Ship tours guarantee the ship waits if the operator is late. Reputable Nassau operators plan returns with buffer time — read reviews and confirm policies before paying.</p></details>
    </div></section>"""


if __name__ == "__main__":
    main()
