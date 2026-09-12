#!/usr/bin/env python3
"""Generate static World 2.0 HTML for Nassau Cruise Excursions (Phase 18B)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APEX = "https://nassaucruiseexcursions.com"
SITE = "Nassau Cruise Excursions"
EMAIL = "hello@nassaucruiseexcursions.com"

# CSS-only hero gradients (no active image assets in 18B)
HERO_BG = (
    "linear-gradient(140deg, rgba(15, 23, 42, 0.88) 0%, rgba(30, 64, 175, 0.72) 40%, "
    "rgba(14, 116, 144, 0.55) 68%, rgba(249, 115, 22, 0.35) 100%), "
    "radial-gradient(ellipse at 70% 20%, rgba(56, 189, 248, 0.25), transparent 55%), "
    "linear-gradient(160deg, #0f172a 0%, #1e3a8a 45%, #0e7490 100%)"
)


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def nav_html(active: str) -> str:
    links = [
        ("home", "/", "Home"),
        ("excursions", "/best-nassau-cruise-excursions", "Excursions"),
        ("beaches", "/nassau-beaches", "Beaches"),
        ("snorkelling", "/nassau-snorkelling-tours", "Snorkelling"),
        ("port", "/nassau-cruise-port-guide", "Port Guide"),
        ("contact", "/contact", "Contact"),
    ]
    desk = []
    for key, href, label in links:
        desk.append(
            f'<a href="{href}" data-nav="{key}" class="text-gray-600 hover:text-ocean-600 transition-colors">{label}</a>'
        )
    mobile_links = links + [
        ("private", "/nassau-private-tours", "Private tours"),
        ("atlantis", "/atlantis-resort-excursions", "Atlantis"),
        ("oneday", "/one-day-in-nassau", "One day"),
        ("about", "/about", "About"),
    ]
    mobile = "\n".join(
        f'<a href="{href}">{label}</a>' for _, href, label in mobile_links
    )
    return f"""<nav class="fixed top-0 left-0 right-0 z-50 bg-white/90 border-b border-ocean-100 shadow-sm" aria-label="Primary">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex items-center justify-between h-12">
      <a href="/" class="flex items-center gap-2">
        <div class="w-7 h-7 rounded-full btn-ocean flex items-center justify-center">
          <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14H9V8h2v8zm4 0h-2V8h2v8z"/>
          </svg>
        </div>
        <span class="font-display font-semibold text-ocean-800 text-base leading-tight">Nassau Cruise<br/><span class="text-[10px] font-body font-normal text-pr-500 tracking-widest uppercase">Excursions</span></span>
      </a>
      <div class="hidden lg:flex items-center gap-5 text-sm font-medium">
        {"".join(desk)}
      </div>
      <a href="/best-nassau-cruise-excursions" class="hidden md:inline-flex items-center gap-2 btn-ocean text-white text-sm font-semibold px-4 py-2 rounded-full shadow-md">
        Compare options
      </a>
      <button type="button" class="lg:hidden p-2 rounded-lg text-gray-600 hover:bg-sand-50" id="menu-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu">
        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
      </button>
    </div>
  </div>
  <div class="mobile-menu lg:hidden" id="mobile-menu" data-mobile-panel="true" hidden>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex flex-col gap-3 text-sm font-medium border-t border-ocean-50 bg-white">
      {mobile}
    </div>
  </div>
</nav>"""


def footer_html() -> str:
    return f"""<footer class="bg-gray-900 text-gray-400 py-14">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-10 mb-12">
      <div class="sm:col-span-2 lg:col-span-1">
        <a href="/" class="font-display font-semibold text-white text-lg">{SITE}</a>
        <p class="mt-3 text-sm leading-relaxed">Independent planning guide for cruise visitors to Nassau, Bahamas. Not affiliated with any cruise line or resort brand.</p>
        <p class="mt-4 text-sm"><a class="text-ocean-300 hover:text-white" href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div>
        <h2 class="text-white text-sm font-semibold uppercase tracking-wider mb-4">Decide</h2>
        <ul class="space-y-2 text-sm">
          <li><a href="/best-nassau-cruise-excursions" class="hover:text-white transition-colors">Best excursions</a></li>
          <li><a href="/nassau-beaches" class="hover:text-white transition-colors">Beaches</a></li>
          <li><a href="/nassau-snorkelling-tours" class="hover:text-white transition-colors">Snorkelling</a></li>
          <li><a href="/atlantis-resort-excursions" class="hover:text-white transition-colors">Atlantis</a></li>
          <li><a href="/nassau-private-tours" class="hover:text-white transition-colors">Private tours</a></li>
        </ul>
      </div>
      <div>
        <h2 class="text-white text-sm font-semibold uppercase tracking-wider mb-4">Plan</h2>
        <ul class="space-y-2 text-sm">
          <li><a href="/nassau-cruise-port-guide" class="hover:text-white transition-colors">Port guide</a></li>
          <li><a href="/one-day-in-nassau" class="hover:text-white transition-colors">One day in Nassau</a></li>
          <li><a href="/methodology" class="hover:text-white transition-colors">Methodology</a></li>
        </ul>
      </div>
      <div>
        <h2 class="text-white text-sm font-semibold uppercase tracking-wider mb-4">Trust</h2>
        <ul class="space-y-2 text-sm">
          <li><a href="/about" class="hover:text-white transition-colors">About</a></li>
          <li><a href="/contact" class="hover:text-white transition-colors">Contact</a></li>
          <li><a href="/privacy" class="hover:text-white transition-colors">Privacy</a></li>
          <li><a href="/terms" class="hover:text-white transition-colors">Terms</a></li>
        </ul>
      </div>
    </div>
    <div class="border-t border-gray-800 pt-8 text-xs text-center sm:text-left">
      <p>&copy; 2026 {SITE}. Editorial information only — confirm times with your ship and operators before you go ashore.</p>
    </div>
  </div>
</footer>"""


def trust_strip(items: list[str]) -> str:
    lis = "".join(
        f'<li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> {esc(t)}</li>'
        for t in items
    )
    return f"""<section class="trust-strip" aria-label="Planning highlights">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <ul class="trust-strip__list">{lis}</ul>
  </div>
</section>"""


def hero(
    eyebrow: str,
    title_html: str,
    lead: str,
    actions_html: str,
    chips: list[tuple[str, str]] | None = None,
    aria: str = "Nassau Bahamas cruise port atmosphere",
) -> str:
    chip_html = ""
    if chips:
        chip_html = (
            '<div class="mt-5 flex flex-wrap gap-2">'
            + "".join(
                f'<a href="{href}" class="inline-flex items-center rounded-full bg-white/10 border border-white/25 px-3 py-1 text-xs text-white/90 hover:bg-white/20">{esc(label)}</a>'
                for label, href in chips
            )
            + "</div>"
        )
    return f"""<section class="site-hero">
  <div class="absolute inset-0 hero-bg-custom" style="background-image: {HERO_BG};" role="img" aria-label="{esc(aria)}"></div>
  <div class="site-hero__inner max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl">
      <div class="site-hero__eyebrow inline-flex items-center gap-2 bg-white/15 backdrop-blur-sm border border-white/30 rounded-full px-4 py-1.5 mb-3">
        <span class="w-2 h-2 rounded-full bg-pr-400"></span>
        <span class="text-white/90 text-xs font-semibold tracking-widest uppercase">{esc(eyebrow)}</span>
      </div>
      <h1 class="site-hero__title text-4xl sm:text-5xl lg:text-[3.25rem] font-display font-bold text-white leading-tight mb-3">{title_html}</h1>
      <p class="site-hero__lead text-base sm:text-lg text-white/85 font-light leading-relaxed mb-5 max-w-2xl">{esc(lead)}</p>
      <div class="site-hero__actions flex flex-col sm:flex-row gap-3">{actions_html}</div>
      {chip_html}
    </div>
  </div>
  <svg class="site-hero__wave relative z-10 text-white" viewBox="0 0 1440 48" preserveAspectRatio="none" aria-hidden="true"><path fill="currentColor" d="M0,32 C240,64 480,0 720,24 C960,48 1200,48 1440,16 L1440,48 L0,48 Z"/></svg>
</section>"""


def breadcrumb(items: list[tuple[str, str]]) -> dict:
    elements = []
    for i, (name, url) in enumerate(items, 1):
        elements.append(
            {
                "@type": "ListItem",
                "position": i,
                "name": name,
                "item": url if url.startswith("http") else f"{APEX}{url}",
            }
        )
    return {"@type": "BreadcrumbList", "itemListElement": elements}


def base_graph(extra: list | None = None) -> list:
    graph = [
        {
            "@type": "WebSite",
            "name": SITE,
            "url": f"{APEX}/",
            "description": "Independent cruise-passenger planning guide for Nassau shore excursions in the Bahamas.",
            "inLanguage": "en-GB",
            "publisher": {
                "@type": "Organization",
                "name": SITE,
                "url": f"{APEX}/",
                "email": EMAIL,
            },
        },
        {
            "@type": "Organization",
            "name": SITE,
            "url": f"{APEX}/",
            "email": EMAIL,
            "description": (
                f"{SITE} provides cruise-focused excursion information and independent destination "
                "advice for passengers visiting Nassau, Bahamas. Not affiliated with any cruise line."
            ),
        },
    ]
    if extra:
        graph.extend(extra)
    return graph


def page(
    *,
    path: str,
    title: str,
    description: str,
    data_page: str,
    hero_html: str,
    trust_html: str,
    main_html: str,
    schema_extra: list | None = None,
    og_type: str = "website",
) -> None:
    canonical = f"{APEX}/" if path == "/" else f"{APEX}{path}"
    schema = {"@context": "https://schema.org", "@graph": base_graph(schema_extra)}
    schema_json = json.dumps(schema, ensure_ascii=True, indent=2)

    html = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:type" content="{og_type}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(description)}" />
  <meta property="og:site_name" content="{SITE}" />
  <meta property="og:locale" content="en_GB" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{esc(title)}" />
  <meta name="twitter:description" content="{esc(description)}" />
  <meta name="geo.region" content="BS" />
  <meta name="geo.placename" content="Nassau, Bahamas" />
  <script type="application/ld+json">
{schema_json}
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/css/site.css" />
</head>
<body class="bg-white text-gray-800 antialiased" data-page="{data_page}">
  <a class="skip-link" href="#main-content">Skip to content</a>
  <div id="site-nav" data-inlined="true">
{nav_html(data_page)}
  </div>
  <div id="page-hero" data-inlined="true">
{hero_html}
  </div>
  <div id="page-trust-strip" data-inlined="true">
{trust_html}
  </div>
  <main id="main-content" tabindex="-1" data-inlined="true">
{main_html}
  </main>
  <div id="site-footer" data-inlined="true">
{footer_html()}
  </div>
  <script src="/js/nav.js" defer></script>
</body>
</html>
"""
    if path == "/":
        out = ROOT / "index.html"
    elif path == "/404":
        out = ROOT / "404.html"
    else:
        out = ROOT / path.lstrip("/") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}")


def prose_page(path: str, data_page: str, title: str, description: str, h1: str, body: str, crumbs: list[tuple[str, str]]) -> None:
    page(
        path=path,
        title=title,
        description=description,
        data_page=data_page,
        hero_html=hero(
            "Nassau · cruise planning",
            h1,
            description,
            f'<a href="/best-nassau-cruise-excursions" class="btn-primary inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm shadow-xl">Compare options</a>',
        ),
        trust_html=trust_strip(
            ["Editorial guide", "Cruise-day focused", "No fake ratings"]
        ),
        main_html=f"""<section class="py-14 bg-white">
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 prose-nassau">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> · {esc(crumbs[-1][0])}</nav>
    {body}
  </div>
</section>""",
        schema_extra=[breadcrumb(crumbs)],
    )


def build_home() -> None:
    faq = [
        (
            "Where do cruise ships dock in Nassau?",
            "Most large ships use Prince George Wharf on New Providence, next to downtown Nassau. Confirm your sailing's terminal notes — berth assignments can vary on busy days.",
        ),
        (
            "How long do ships usually stay?",
            "Many Nassau calls leave several hours ashore, often in a roughly half-day to full-day window. Always use your ship's published gangway and all-aboard times — they vary by itinerary.",
        ),
        (
            "Can I walk from the pier?",
            "Downtown streets, Bay Street shopping, and Junkanoo Beach are among the closest options on foot. Cable Beach and Paradise Island usually need a taxi, ferry, or organised transfer — build return buffer before all-aboard.",
        ),
        (
            "Can I book tours on this site yet?",
            "Yes — you can request the Explore Nassau Walking Tour online. Payment creates a booking request; confirmation is emailed separately. If we cannot confirm, you receive a full refund. Other day styles remain editorial planning guides.",
        ),
    ]
    faq_schema = {
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faq
        ],
    }
    cards = [
        ("Beach day", "Near-port sand vs a longer taxi beach — match distance to your return window.", "/nassau-beaches", "Beach"),
        ("Atlantis", "Paradise Island as a place/experience option — plan transfers and access carefully.", "/atlantis-resort-excursions", "Atlantis"),
        ("Snorkelling / water", "Boat reefs and island stops that fit half-day or longer calls.", "/nassau-snorkelling-tours", "Water"),
        ("See Nassau", "Explore Nassau Walking Tour — guided historic downtown walking you can request online.", "/book/explore-nassau-walking-tour", "Town"),
        ("Private tour", "When a custom pace helps families or mixed interests.", "/nassau-private-tours", "Private"),
        ("Short port day", "What fits — and what to skip — when time ashore is tight.", "/one-day-in-nassau", "Short call"),
    ]
    card_html = "".join(
        f"""<a href="{href}" class="card-hover block bg-white rounded-3xl border border-blue-50 shadow-md p-6">
  <div class="text-xs font-semibold tracking-widest uppercase text-ocean-600 mb-2">{esc(tag)}</div>
  <h3 class="text-xl font-display font-semibold text-gray-900 mb-2">{esc(title)}</h3>
  <p class="text-sm text-gray-600 leading-relaxed">{esc(blurb)}</p>
</a>"""
        for title, blurb, href, tag in cards
    )
    faq_html = "".join(
        f"""<details class="faq-item rounded-2xl border border-ocean-100 p-5 bg-white">
  <summary class="font-semibold text-gray-900 cursor-pointer">{esc(q)}</summary>
  <p class="mt-4 text-sm text-gray-600 leading-relaxed">{esc(a)}</p>
</details>"""
        for q, a in faq
    )
    page(
        path="/",
        title="Nassau Cruise Excursions | Bahamas Cruise Port Planning",
        description="Plan Nassau cruise excursions from Prince George Wharf — beaches, snorkelling, Paradise Island, downtown walking and realistic return-window choices.",
        data_page="home",
        hero_html=hero(
            "Bahamas · New Providence cruise port",
            'Nassau Cruise <br/><span class="text-pr-400">Excursions</span> for Ship Passengers',
            "A practical guide to what fits a Nassau call: beach time, Paradise Island, reef snorkelling, downtown walking, or a private plan matched to your group's pace.",
            '<a href="/best-nassau-cruise-excursions" class="btn-primary inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm shadow-xl">Compare options</a>'
            '<a href="/nassau-cruise-port-guide" class="btn-outline inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm">Port guide</a>',
            chips=[
                ("Beach day", "/nassau-beaches"),
                ("Atlantis", "/atlantis-resort-excursions"),
                ("Snorkelling", "/nassau-snorkelling-tours"),
                ("See Nassau", "/book/explore-nassau-walking-tour"),
            ],
            aria="Stylised Nassau cruise-port atmosphere",
        ),
        trust_html=trust_strip(
            [
                "Cruise-day planning focus",
                "Downtown + Paradise Island choices",
                "Honest timing caveats",
                "No fake reviews",
            ]
        ),
        main_html=f"""
<section class="pt-10 pb-14 bg-white">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid lg:grid-cols-2 gap-12 items-start">
    <div>
      <div class="section-label">Bahamas cruise capital</div>
      <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 mb-5">What Nassau is actually <span class="text-ocean-600">good for</span></h2>
      <p class="text-gray-600 leading-relaxed mb-4">Nassau packs a walkable downtown harbour, Paradise Island across the water, and easy beach or boat options into one busy cruise call. The hard part is not finding ideas — it is matching them to <strong>gangway time</strong>, transfer buffers, and how much walking or swimming your group wants.</p>
      <p class="text-gray-600 leading-relaxed mb-8">Most organised pickups cluster near <strong>Prince George Wharf</strong>. Build your own return margin before all-aboard; this guide does not promise ship-wait guarantees.</p>
      <a href="/best-nassau-cruise-excursions" class="btn-ocean inline-flex items-center gap-2 text-white font-semibold px-7 py-3.5 rounded-full text-sm shadow-lg">Browse day styles</a>
    </div>
    <aside class="cruise-snapshot" aria-label="Cruise passenger snapshot">
      <h3 class="font-display font-semibold text-ocean-800 text-lg mb-4">Cruise passenger snapshot</h3>
      <dl class="cruise-snapshot__grid">
        <div class="cruise-snapshot__item"><dt>Pier area</dt><dd>Prince George Wharf / downtown Nassau</dd></div>
        <div class="cruise-snapshot__item"><dt>Walkable</dt><dd>Bay Street, Straw Market, Junkanoo Beach</dd></div>
        <div class="cruise-snapshot__item"><dt>Needs transfer</dt><dd>Cable Beach, Paradise Island, most boat days</dd></div>
        <div class="cruise-snapshot__item"><dt>Currency</dt><dd>Bahamian dollar; USD widely accepted in tourist areas</dd></div>
        <div class="cruise-snapshot__item"><dt>Language</dt><dd>English</dd></div>
        <div class="cruise-snapshot__item"><dt>Planning rule</dt><dd>Confirm all-aboard; leave buffer for traffic and queues</dd></div>
      </dl>
    </aside>
  </div>
</section>

<section class="py-16 bg-pr-50">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="text-center mb-10">
      <div class="section-label justify-center">Decision spine</div>
      <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900">Six useful starting points</h2>
      <p class="mt-4 text-gray-600 max-w-2xl mx-auto">Not a ranked catalogue — choose the day style that fits your call, then read the deeper guide.</p>
    </div>
    <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">{card_html}</div>
  </div>
</section>

<section class="py-12 bg-white">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
    <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Planning routes</h2>
    <p class="text-gray-600 mb-6 max-w-2xl mx-auto">Move from the homepage into the pages that answer cruise decisions — not synonym clones.</p>
    <div class="flex flex-wrap justify-center gap-3 text-sm">
      <a class="text-ocean-700 font-semibold hover:underline" href="/best-nassau-cruise-excursions">Best excursions</a>
      <a class="text-ocean-700 font-semibold hover:underline" href="/nassau-cruise-port-guide">Port guide</a>
      <a class="text-ocean-700 font-semibold hover:underline" href="/nassau-beaches">Beaches</a>
      <a class="text-ocean-700 font-semibold hover:underline" href="/nassau-snorkelling-tours">Snorkelling</a>
      <a class="text-ocean-700 font-semibold hover:underline" href="/atlantis-resort-excursions">Atlantis</a>
      <a class="text-ocean-700 font-semibold hover:underline" href="/one-day-in-nassau">One day</a>
      <a class="text-ocean-700 font-semibold hover:underline" href="/nassau-private-tours">Private</a>
      <a class="text-ocean-700 font-semibold hover:underline" href="/methodology">Methodology</a>
    </div>
  </div>
</section>

<section id="faq" class="py-16 bg-sand-50">
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
    <h2 class="text-3xl font-display font-bold text-gray-900 text-center mb-8">Nassau cruise FAQ</h2>
    <div class="space-y-4">{faq_html}</div>
  </div>
</section>
""",
        schema_extra=[faq_schema],
    )


def build_best() -> None:
    rows = [
        ("Beach day", "Half day+", "Near Junkanoo (walk/short ride) or taxi to Cable / Paradise Island beaches", "Families, first-timers, low-effort sand", "Traffic and chair/facility unknowns — leave return buffer", "/nassau-beaches"),
        ("Walking / city", "1.5–3 hours", "Starts near downtown / pier area", "History, photos, lighter mobility than boat days", "Heat, uneven streets, stairs at some sites", "/book/explore-nassau-walking-tour"),
        ("Snorkel / boat", "Half day typical", "Boat meeting near harbour; exact point on operator ticket", "Groups who want water without a full island day", "Weather, swim ability, ladder boarding", "/nassau-snorkelling-tours"),
        ("Paradise Island / Atlantis-type day", "Often 5–6 hours with transfers", "Taxi, ferry, or excursion transfer across the harbour", "Families chasing a resort-scale day", "Access rules, queues, transfer time — verify independently", "/atlantis-resort-excursions"),
        ("Private plan", "Flexible", "Driver meet near pier (confirm on booking)", "Mixed ages, custom stops, tighter timing control", "Cost; still needs buffer for traffic", "/nassau-private-tours"),
        ("Short-call option", "Under ~4 hours ashore usable", "Stay close: downtown, Junkanoo, short walk tour", "Late tenders / early all-aboard", "Skip Exuma flights and long island circuits", "/one-day-in-nassau"),
    ]
    cards = "".join(
        f"""<article class="bg-white rounded-3xl border border-blue-50 shadow-sm p-6">
  <h3 class="text-xl font-display font-semibold text-gray-900 mb-2">{esc(name)}</h3>
  <dl class="text-sm text-gray-600 space-y-2 mb-4">
    <div><dt class="font-semibold text-ocean-800 inline">Port-day time: </dt><dd class="inline">{esc(time)}</dd></div>
    <div><dt class="font-semibold text-ocean-800 inline">From the pier: </dt><dd class="inline">{esc(from_pier)}</dd></div>
    <div><dt class="font-semibold text-ocean-800 inline">Best for: </dt><dd class="inline">{esc(best)}</dd></div>
    <div><dt class="font-semibold text-ocean-800 inline">Caveats: </dt><dd class="inline">{esc(caveats)}</dd></div>
  </dl>
  <a href="{href}" class="text-ocean-700 font-semibold text-sm hover:underline">Read the guide →</a>
</article>"""
        for name, time, from_pier, best, caveats, href in rows
    )
    page(
        path="/best-nassau-cruise-excursions",
        title="Best Nassau Cruise Excursions | Compare Day Styles",
        description="Compare Nassau cruise excursion styles — beach, walking, snorkelling, Paradise Island, private and short-call options — without fake rankings.",
        data_page="excursions",
        hero_html=hero(
            "Compare & choose",
            'Best Nassau <br/><span class="text-pr-400">Cruise Excursions</span>',
            "Match your port day to a realistic style — not a popularity contest. Use time ashore, transfer needs, and swimming comfort as your filters.",
            '<a href="/nassau-cruise-port-guide" class="btn-primary inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm shadow-xl">Port logistics</a>'
            '<a href="/one-day-in-nassau" class="btn-outline inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm">One-day plans</a>',
        ),
        trust_html=trust_strip(
            ["Category comparison", "No fake best-sellers", "Cruise timing first"]
        ),
        main_html=f"""
<section class="py-14 bg-white">
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 mb-10">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> · Best excursions</nav>
    <p class="text-gray-600 leading-relaxed mb-4">This page compares <strong>day styles</strong> cruise guests actually choose from Nassau. It does not invent star ratings, “most popular” claims, or live inventory.</p>
    <p class="text-gray-600 leading-relaxed">Online request-to-book is available for one product: the <a class="text-ocean-700 font-semibold" href="/book/explore-nassau-walking-tour">Explore Nassau Walking Tour</a>. Payment creates a request — confirmation follows separately.</p>
  </div>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid md:grid-cols-2 gap-6">{cards}</div>
</section>
<section class="py-12 bg-sand-50">
  <div class="max-w-3xl mx-auto px-4 text-center">
    <h2 class="text-2xl font-display font-bold text-gray-900 mb-3">Swimming pigs?</h2>
    <p class="text-gray-600 leading-relaxed mb-4">Pig encounters near Nassau are usually boat trips (often Rose Island area) or longer Exuma-style days. They are not a separate thin page here — treat them as a water/boat decision and confirm duration against all-aboard before you commit.</p>
    <a href="/nassau-snorkelling-tours" class="text-ocean-700 font-semibold hover:underline">See snorkelling &amp; water timing →</a>
  </div>
</section>
""",
        schema_extra=[
            breadcrumb(
                [("Home", "/"), ("Best Nassau cruise excursions", "/best-nassau-cruise-excursions")]
            ),
            {
                "@type": "WebPage",
                "name": "Best Nassau Cruise Excursions",
                "url": f"{APEX}/best-nassau-cruise-excursions",
                "description": "Compare Nassau cruise excursion day styles for ship passengers.",
            },
        ],
    )


def build_port() -> None:
    page(
        path="/nassau-cruise-port-guide",
        title="Nassau Cruise Port Guide | Prince George Wharf Tips",
        description="Nassau cruise port guide for Prince George Wharf — downtown walking, Junkanoo Beach, Paradise Island access, taxis, and return-to-ship planning.",
        data_page="port",
        hero_html=hero(
            "Port logistics",
            'Nassau <br/><span class="text-pr-400">Cruise Port Guide</span>',
            "Orient yourself at Prince George Wharf, then decide what is walkable versus what needs a taxi, ferry, or organised transfer.",
            '<a href="/one-day-in-nassau" class="btn-primary inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm shadow-xl">One-day ideas</a>'
            '<a href="/best-nassau-cruise-excursions" class="btn-outline inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm">Compare options</a>',
        ),
        trust_html=trust_strip(
            ["Prince George Wharf focus", "Walk vs transfer", "Buffer before all-aboard"]
        ),
        main_html="""
<section class="py-14 bg-white">
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> · Port guide</nav>
    <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Where ships dock</h2>
    <p class="text-gray-600 leading-relaxed mb-4">Most large cruise ships call at <strong>Prince George Wharf</strong> on New Providence, beside downtown Nassau. From the terminal exit you are close to Bay Street shopping, the Straw Market area, and waterfront cafés. Always check your sailing’s terminal notes — busy days can change berth and gangway flow.</p>
    <p class="text-gray-600 leading-relaxed mb-8">Organised tour pickups commonly cluster near the pier. If you arrange anything independently, agree the meeting point in writing and leave margin for crowds.</p>

    <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">What is walkable</h2>
    <ul class="list-disc pl-5 text-gray-600 space-y-2 mb-8">
      <li><strong>Bay Street &amp; downtown</strong> — shopping, photo stops, and short cultural loops.</li>
      <li><strong>Straw Market area</strong> — expect bargaining and variable quality; keep valuables secure.</li>
      <li><strong>Junkanoo Beach</strong> — among the closest beach options for a quick dip between pier and ship.</li>
    </ul>

    <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Paradise Island access</h2>
    <p class="text-gray-600 leading-relaxed mb-4">Paradise Island (including the Atlantis resort complex) sits across the harbour. Cruise guests typically cross by <strong>taxi over the bridge</strong>, a <strong>passenger ferry</strong> when operating, or an excursion transfer. Treat crossing time as a planning variable — traffic, queues, and weather all matter — and re-check same-day ferry or taxi advice locally rather than relying on a fixed published fare or timetable from this page.</p>

    <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Taxis &amp; practicalities</h2>
    <p class="text-gray-600 leading-relaxed mb-4">Licensed taxis are the usual independent option for Cable Beach and Paradise Island. <strong>Agree the fare or rate basis before you depart</strong>; do not publish assumed tariffs here because they change. US dollars are widely accepted in tourist areas; Bahamian dollars are also used. English is the everyday language for visitors.</p>

    <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Return-to-ship planning</h2>
    <p class="text-gray-600 leading-relaxed mb-4">Work backwards from all-aboard, not from “tour end.” Add buffer for pier security lines, traffic, and weather delays on boat days. Ship-sponsored tours sometimes carry wait-for-ship policies; independent plans do not automatically inherit that protection — read any operator policy carefully.</p>

    <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Short calls, families, mobility</h2>
    <p class="text-gray-600 leading-relaxed mb-4">If usable time ashore is short, stay close: downtown walking, Junkanoo Beach, or a brief guided loop. Families chasing Paradise Island should budget transfer plus entry/queue time. Mobility varies by tour — boat ladders, ferry steps, and historic stairways can be limiting; ask operators about access before paying.</p>

    <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Weather &amp; water caveats</h2>
    <p class="text-gray-600 leading-relaxed mb-8">Wind, rain, and sea state can alter snorkel and island boat days. Beaches remain public spaces with variable conditions. There are no wildlife or “perfect water” guarantees on this site.</p>

    <p class="text-sm text-gray-500">Related: <a class="text-ocean-700 font-semibold" href="/book/explore-nassau-walking-tour">Explore Nassau Walking Tour</a> · <a class="text-ocean-700 font-semibold" href="/one-day-in-nassau">One day in Nassau</a> · <a class="text-ocean-700 font-semibold" href="/nassau-beaches">Beaches</a> · <a class="text-ocean-700 font-semibold" href="/methodology">Methodology</a></p>
  </div>
</section>
""",
        schema_extra=[
            breadcrumb([("Home", "/"), ("Nassau cruise port guide", "/nassau-cruise-port-guide")]),
            {
                "@type": "WebPage",
                "name": "Nassau Cruise Port Guide",
                "url": f"{APEX}/nassau-cruise-port-guide",
            },
        ],
    )


def build_beaches() -> None:
    beaches = [
        ("Junkanoo Beach", "Closest practical sand for many cruise guests — often reachable on foot or a very short ride from the wharf area.", "Strong for short calls and “just need the water” days.", "Can be busy on ship days; facilities and chair setups vary — verify on the day.", "DIY"),
        ("Cable Beach", "Resort strip west of downtown; typically a taxi ride rather than a stroll.", "Half-day beach focus when you want a longer shoreline and resort-area amenities nearby.", "Traffic both ways; confirm taxi plan before you leave the pier.", "DIY taxi or excursion"),
        ("Cabbage Beach", "Paradise Island public beach near the Atlantis area — transfer required.", "Combine with a Paradise Island day if transfers already fit your schedule.", "Bridge/ferry time plus crowds; not a last-minute dash before all-aboard.", "Transfer + DIY"),
        ("Love Beach", "Quieter local favourite further west; sometimes paired with calm-day snorkelling off the reef.", "Guests wanting a less resort-front vibe — only if timing is comfortable.", "Farther transfer; reef/snorkel conditions are weather-dependent.", "DIY with timing caution"),
    ]
    blocks = "".join(
        f"""<article class="bg-white rounded-3xl border border-blue-50 p-6 shadow-sm">
  <h3 class="text-xl font-display font-semibold text-gray-900 mb-2">{esc(name)}</h3>
  <p class="text-sm text-gray-600 leading-relaxed mb-3">{esc(where)}</p>
  <p class="text-sm text-gray-600 leading-relaxed mb-2"><strong class="text-ocean-800">Best for:</strong> {esc(best)}</p>
  <p class="text-sm text-gray-600 leading-relaxed mb-2"><strong class="text-ocean-800">Caveats:</strong> {esc(caveats)}</p>
  <p class="text-xs font-semibold tracking-widest uppercase text-pr-600">{esc(mode)}</p>
</article>"""
        for name, where, best, caveats, mode in beaches
    )
    page(
        path="/nassau-beaches",
        title="Nassau Beaches for Cruise Passengers | Junkanoo to Cable",
        description="Choose a Nassau beach from the cruise port — Junkanoo, Cable, Cabbage and Love Beach with DIY vs excursion practicality.",
        data_page="beaches",
        hero_html=hero(
            "Beach decisions",
            'Nassau Beaches <br/><span class="text-pr-400">from the Cruise Port</span>',
            "Pick sand that fits your clock: walkable Junkanoo, taxi-out Cable Beach, or Paradise Island’s Cabbage Beach when transfers already make sense.",
            '<a href="/one-day-in-nassau" class="btn-primary inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm shadow-xl">Short vs full day</a>'
            '<a href="/nassau-cruise-port-guide" class="btn-outline inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm">Port guide</a>',
        ),
        trust_html=trust_strip(
            ["Distance-first advice", "DIY vs transfer", "No mislabelled islands"]
        ),
        main_html=f"""
<section class="py-14 bg-white">
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 mb-10">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> · Beaches</nav>
    <p class="text-gray-600 leading-relaxed">Bahamian beaches are public in principle, but <strong>getting there and back before all-aboard</strong> is the real decision. This page covers New Providence / Paradise Island options cruise guests commonly weigh — not Exuma or other islands.</p>
  </div>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid md:grid-cols-2 gap-6 mb-12">{blocks}</div>
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
    <h2 class="text-2xl font-display font-bold text-gray-900 mb-3">DIY vs organised beach time</h2>
    <p class="text-gray-600 leading-relaxed mb-4">DIY works best for Junkanoo or a pre-agreed taxi to Cable Beach when your group is confident navigating the pier. Organised beach or island days trade flexibility for a set meeting point and shared return plan — still not a substitute for watching all-aboard yourself.</p>
    <p class="text-gray-600 leading-relaxed">Facilities (chairs, restrooms, food) change by beach and season; treat them as day-of facts. For boat-based beach clubs or private islands, read the snorkelling guide’s timing notes.</p>
  </div>
</section>
""",
        schema_extra=[
            breadcrumb([("Home", "/"), ("Nassau beaches", "/nassau-beaches")]),
            {"@type": "WebPage", "name": "Nassau Beaches", "url": f"{APEX}/nassau-beaches"},
        ],
    )


def build_snorkel() -> None:
    page(
        path="/nassau-snorkelling-tours",
        title="Nassau Snorkelling Tours | Cruise Port Water Days",
        description="Plan Nassau snorkelling from the cruise port — boat reefs vs beach snorkel, time commitment, weather dependence and swimming requirements.",
        data_page="snorkelling",
        hero_html=hero(
            "Water days",
            'Nassau <br/><span class="text-pr-400">Snorkelling</span> for Cruise Guests',
            "Choose between a social catamaran reef stop and a longer island/beach water day — then check swim comfort and sea conditions.",
            '<a href="/best-nassau-cruise-excursions" class="btn-primary inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm shadow-xl">Compare day styles</a>'
            '<a href="/nassau-beaches" class="btn-outline inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm">Beach alternatives</a>',
        ),
        trust_html=trust_strip(
            ["No wildlife guarantees", "Weather is a variable", "Ladder & swim checks"]
        ),
        main_html="""
<section class="py-14 bg-white">
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> · Snorkelling</nav>
    <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Boat snorkel vs beach / island snorkel</h2>
    <p class="text-gray-600 leading-relaxed mb-4"><strong>Catamaran or powerboat reef stops</strong> are the classic cruise-passenger pattern: meet near the harbour, sail to a snorkel site, then return on a published window. <strong>Beach or private-island snorkel</strong> days add ferry or beach time and often run longer.</p>
    <p class="text-gray-600 leading-relaxed mb-8">Rose Island–area trips are commonly marketed for shallow reefs and beginner-friendly water. Exact sites move with sea conditions — captains choose workable water, not a fixed postcard spot.</p>

    <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Time commitment</h2>
    <p class="text-gray-600 leading-relaxed mb-8">Many boat snorkel products sit in a roughly half-day window; island beach-and-snorkel packages can approach five hours including transfers. Map the advertised return against all-aboard with spare margin — do not treat brochure duration as door-to-gangway time.</p>

    <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Who it suits</h2>
    <ul class="list-disc pl-5 text-gray-600 space-y-2 mb-8">
      <li>Comfortable swimming in open water and climbing a boat ladder.</li>
      <li>Groups who want a shared water day without walking tours.</li>
      <li>Short calls: prefer simpler near-port beach time instead of long island circuits.</li>
    </ul>

    <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Caveats</h2>
    <p class="text-gray-600 leading-relaxed mb-4">Wind and swell cancel or reshape snorkel stops. Medical conditions, back/knee limits, and intoxication rules often apply. Reef-safe sunscreen helps protect coral. This site does not guarantee turtles, pigs, or “perfect visibility.”</p>
    <p class="text-sm text-gray-500">Related: <a class="text-ocean-700 font-semibold" href="/one-day-in-nassau">One day timing</a> · <a class="text-ocean-700 font-semibold" href="/nassau-cruise-port-guide">Port guide</a></p>
  </div>
</section>
""",
        schema_extra=[
            breadcrumb([("Home", "/"), ("Nassau snorkelling", "/nassau-snorkelling-tours")]),
            {"@type": "WebPage", "name": "Nassau Snorkelling Tours", "url": f"{APEX}/nassau-snorkelling-tours"},
        ],
    )


def build_atlantis() -> None:
    page(
        path="/atlantis-resort-excursions",
        title="Atlantis from Nassau Cruise Port | Paradise Island Planning",
        description="Plan a Paradise Island / Atlantis-area day from Nassau cruise port — transfers, time use and access caveats without affiliation claims.",
        data_page="atlantis",
        hero_html=hero(
            "Paradise Island",
            'Atlantis as a <br/><span class="text-pr-400">Cruise-Day Option</span>',
            "Paradise Island is a short harbour crossing from downtown Nassau. Treat Atlantis as a place and experience cluster — not an affiliation, and not a guaranteed day-pass product on this site.",
            '<a href="/nassau-cruise-port-guide" class="btn-primary inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm shadow-xl">Transfer context</a>'
            '<a href="/nassau-beaches" class="btn-outline inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm">Beach alternatives</a>',
        ),
        trust_html=trust_strip(
            ["No resort affiliation", "No day-pass promises", "Transfer time matters"]
        ),
        main_html="""
<section class="py-14 bg-white">
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> · Atlantis</nav>
    <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">What this page is — and is not</h2>
    <p class="text-gray-600 leading-relaxed mb-4">Cruise guests often ask about the <strong>Atlantis</strong> resort complex on Paradise Island. This page helps you decide whether a Paradise Island day fits your call. It does <strong>not</strong> claim official affiliation with Atlantis or Brookfield/related brands, does not sell day passes, and does not guarantee Aquaventure access, pricing, or availability.</p>

    <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">How guests typically get there</h2>
    <p class="text-gray-600 leading-relaxed mb-8">From Prince George Wharf, guests commonly use a taxi across the bridge, a passenger ferry when running, or an organised excursion transfer. Build round-trip transfer and queue time into your plan. We do not publish fixed ferry schedules or taxi fares here because they change — confirm locally on the day.</p>

    <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Time use</h2>
    <p class="text-gray-600 leading-relaxed mb-8">A resort-scale day with transfers often needs a generous slice of the call — many guests budget something on the order of five to six hours including travel, but your ship’s window is the only number that matters. If time is tight, downtown walking or Junkanoo Beach is usually the safer fit.</p>

    <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Access &amp; planning honesty</h2>
    <ul class="list-disc pl-5 text-gray-600 space-y-2 mb-8">
      <li>Non-guest access rules, day products, and marine/park areas change — verify on official resort channels or a trusted operator before you go.</li>
      <li>Scenic “drive-by / photo stop” tours are not the same as full resort access.</li>
      <li>Families should plan meals, lockers, and exit buffers deliberately.</li>
    </ul>
    <p class="text-sm text-gray-500">Alternatives: <a class="text-ocean-700 font-semibold" href="/nassau-beaches">Beaches</a> · <a class="text-ocean-700 font-semibold" href="/one-day-in-nassau">One day in Nassau</a></p>
  </div>
</section>
""",
        schema_extra=[
            breadcrumb([("Home", "/"), ("Atlantis from Nassau cruise port", "/atlantis-resort-excursions")]),
            {"@type": "WebPage", "name": "Atlantis from Nassau Cruise Port", "url": f"{APEX}/atlantis-resort-excursions"},
        ],
    )


def build_oneday() -> None:
    page(
        path="/one-day-in-nassau",
        title="One Day in Nassau from a Cruise Ship | Port Day Plans",
        description="One day in Nassau from a cruise ship — short-call, half-day and fuller-day plans for downtown, beach and organised options.",
        data_page="oneday",
        hero_html=hero(
            "Port-day scenarios",
            'One Day in <br/><span class="text-pr-400">Nassau</span>',
            "Use your usable hours ashore — not brochure fantasy — to choose downtown DIY, a beach block, or one organised half day.",
            '<a href="/best-nassau-cruise-excursions" class="btn-primary inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm shadow-xl">Compare styles</a>'
            '<a href="/nassau-cruise-port-guide" class="btn-outline inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm">Port guide</a>',
        ),
        trust_html=trust_strip(
            ["Short / half / fuller day", "What to skip", "No invented schedules"]
        ),
        main_html="""
<section class="py-14 bg-white">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <nav class="breadcrumb mb-8" aria-label="Breadcrumb"><a href="/">Home</a> · One day in Nassau</nav>
    <div class="grid lg:grid-cols-3 gap-6 mb-12">
      <article class="bg-sky-50 rounded-3xl p-7 border border-sky-100">
        <h2 class="font-display font-bold text-lg mb-3">Short call</h2>
        <p class="text-sm text-gray-600 leading-relaxed mb-3">When usable time is tight, stay near the pier: Bay Street, Straw Market, Junkanoo Beach, or a brief walking loop.</p>
        <p class="text-sm text-gray-600"><strong>Skip:</strong> Paradise Island resort days, long island boats, anything with uncertain return traffic.</p>
      </article>
      <article class="bg-teal-50 rounded-3xl p-7 border border-teal-100">
        <h2 class="font-display font-bold text-lg mb-3">Half day</h2>
        <p class="text-sm text-gray-600 leading-relaxed mb-3">One organised boat snorkel, a Cable Beach taxi block, or a downtown walking focus — then return with margin.</p>
        <p class="text-sm text-gray-600"><strong>Rule:</strong> one primary plan beats stacking three “quick” stops.</p>
      </article>
      <article class="bg-amber-50 rounded-3xl p-7 border border-amber-100">
        <h2 class="font-display font-bold text-lg mb-3">Fuller day</h2>
        <p class="text-sm text-gray-600 leading-relaxed mb-3">Paradise Island / resort-scale days or longer island beach packages only when your ship window and transfers clearly fit.</p>
        <p class="text-sm text-gray-600"><strong>Still skip:</strong> same-day Exuma flight products unless your call and operator timing are explicitly compatible.</p>
      </article>
    </div>
    <div class="max-w-3xl">
      <h2 class="text-2xl font-display font-bold text-gray-900 mb-3">DIY downtown</h2>
      <p class="text-gray-600 leading-relaxed mb-6">A self-guided loop can cover harbour streets, market browsing, and a beach dip without pre-booking. Carry water, watch heat, and keep an eye on the clock — DIY has no operator “return plan.”</p>
      <h2 class="text-2xl font-display font-bold text-gray-900 mb-3">See Nassau on foot</h2>
      <p class="text-gray-600 leading-relaxed mb-4">Guided walking suits guests who want context without a boat. You can request the <a class="text-ocean-700 font-semibold" href="/book/explore-nassau-walking-tour">Explore Nassau Walking Tour</a> online — payment creates a booking request; confirmation is emailed separately.</p>
      <p class="text-sm text-gray-500">Deep links: <a class="text-ocean-700 font-semibold" href="/book/explore-nassau-walking-tour">Book walking tour</a> · <a class="text-ocean-700 font-semibold" href="/nassau-beaches">Beaches</a> · <a class="text-ocean-700 font-semibold" href="/atlantis-resort-excursions">Atlantis</a> · <a class="text-ocean-700 font-semibold" href="/nassau-private-tours">Private tours</a></p>
    </div>
  </div>
</section>
""",
        schema_extra=[
            breadcrumb([("Home", "/"), ("One day in Nassau", "/one-day-in-nassau")]),
            {"@type": "WebPage", "name": "One Day in Nassau", "url": f"{APEX}/one-day-in-nassau"},
        ],
    )


def build_private() -> None:
    page(
        path="/nassau-private-tours",
        title="Nassau Private Tours | Cruise Port Planning Notes",
        description="When a private Nassau tour makes sense for cruise passengers — flexibility, families and timing — editorial guidance only.",
        data_page="private",
        hero_html=hero(
            "Custom pace",
            'Private Nassau Tours <br/><span class="text-pr-400">— Editorial Guide</span>',
            "Private vehicles help when your group needs a custom stop list and a driver who understands all-aboard pressure — this page does not offer live booking yet.",
            '<a href="/best-nassau-cruise-excursions" class="btn-primary inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm shadow-xl">See other day styles</a>'
            '<a href="/contact" class="btn-outline inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm">Contact</a>',
        ),
        trust_html=trust_strip(
            ["Editorial only", "No live prices", "No implied availability"]
        ),
        main_html="""
<section class="py-14 bg-white">
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> · Private tours</nav>
    <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Who private suits</h2>
    <ul class="list-disc pl-5 text-gray-600 space-y-2 mb-8">
      <li>Multi-generational groups with different energy levels.</li>
      <li>Guests combining a short city loop with a specific beach or viewpoint.</li>
      <li>Travellers who want control over stop length more than a fixed coach itinerary.</li>
    </ul>
    <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">When it makes sense</h2>
    <p class="text-gray-600 leading-relaxed mb-4">Private shines when the alternative is compromising on pace. It is less necessary if you only want a single shared boat snorkel or a walkable downtown morning.</p>
    <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Caveats</h2>
    <p class="text-gray-600 leading-relaxed mb-4">Traffic still exists. Private does not create extra hours ashore. This site does not list suppliers, prices, or current bookability for private Nassau tours.</p>
  </div>
</section>
""",
        schema_extra=[
            breadcrumb([("Home", "/"), ("Private Nassau tours", "/nassau-private-tours")]),
            {"@type": "WebPage", "name": "Nassau Private Tours", "url": f"{APEX}/nassau-private-tours"},
        ],
    )


def build_trust_pages() -> None:
    prose_page(
        "/contact",
        "contact",
        "Contact | Nassau Cruise Excursions",
        "Contact Nassau Cruise Excursions for editorial questions about this Nassau cruise planning guide.",
        'Contact <span class="text-pr-400">Nassau Cruise Excursions</span>',
        f"""
    <h2 class="text-xl font-display font-bold text-gray-900 mb-3">Email</h2>
    <p class="text-gray-600 leading-relaxed mb-4">For editorial questions about this planning guide, email <a class="text-ocean-700 font-semibold" href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    <p class="text-gray-600 leading-relaxed mb-4">Include your ship date and the page you are asking about. Do not send payment card details by email.</p>
    <p class="text-gray-600 leading-relaxed">You can request the <a class="text-ocean-700 font-semibold" href="/book/explore-nassau-walking-tour">Explore Nassau Walking Tour</a> online. For other questions about this planning guide, email <a class="text-ocean-700 font-semibold" href="mailto:{EMAIL}">{EMAIL}</a>.</p>
""",
        [("Home", "/"), ("Contact", "/contact")],
    )
    prose_page(
        "/about",
        "about",
        "About | Nassau Cruise Excursions",
        "About Nassau Cruise Excursions — independent cruise-passenger planning for Nassau, Bahamas.",
        'About this <span class="text-pr-400">guide</span>',
        f"""
    <p class="text-gray-600 leading-relaxed mb-4">{SITE} is an independent editorial site helping cruise passengers choose realistic shore days in Nassau. We are not a cruise line, not a harbour authority, and not affiliated with Atlantis or other resort brands.</p>
    <p class="text-gray-600 leading-relaxed mb-4">Recommendations prioritise port-day fit: walking distance, transfer burden, swimming requirements, and return buffers. See <a class="text-ocean-700 font-semibold" href="/methodology">methodology</a> for how pages are written.</p>
""",
        [("Home", "/"), ("About", "/about")],
    )
    prose_page(
        "/privacy",
        "privacy",
        "Privacy | Nassau Cruise Excursions",
        "Privacy information for Nassau Cruise Excursions.",
        'Privacy <span class="text-pr-400">notice</span>',
        f"""
    <p class="text-gray-600 leading-relaxed mb-4">This is an editorial website. If you email {EMAIL}, we use your message only to reply.</p>
    <p class="text-gray-600 leading-relaxed mb-4">Standard hosting and security logs may be processed by our infrastructure providers. We do not sell personal information.</p>
    <p class="text-gray-600 leading-relaxed">Card payments for online booking requests are handled on a hosted Stripe checkout — not collected through unstructured email.</p>
""",
        [("Home", "/"), ("Privacy", "/privacy")],
    )
    prose_page(
        "/terms",
        "terms",
        "Terms | Nassau Cruise Excursions",
        "Terms for using the Nassau Cruise Excursions editorial website.",
        'Terms of <span class="text-pr-400">use</span>',
        """
    <p class="text-gray-600 leading-relaxed mb-4">Content on this site is general information for cruise passengers planning time ashore in Nassau. It is not a booking contract, not professional advice, and not a guarantee of access, timing, weather, or safety outcomes.</p>
    <p class="text-gray-600 leading-relaxed mb-4">Confirm gangway and all-aboard times with your ship. Confirm meeting points, inclusions, and cancellation terms with any operator you use.</p>
    <p class="text-gray-600 leading-relaxed">Place names such as Atlantis are used for geographic orientation only and do not imply endorsement or partnership.</p>
""",
        [("Home", "/"), ("Terms", "/terms")],
    )
    prose_page(
        "/methodology",
        "methodology",
        "Methodology | Nassau Cruise Excursions",
        "How Nassau Cruise Excursions writes cruise-passenger guides.",
        'Editorial <span class="text-pr-400">methodology</span>',
        """
    <ul class="list-disc pl-5 text-gray-600 space-y-3 mb-6">
      <li>Prioritise cruise-port decisions over generic tourism brochure copy.</li>
      <li>Preserve useful URLs with redirects; do not protect thin pages for their own sake.</li>
      <li>No fake ratings, review stars, or unsupported “most popular” claims.</li>
      <li>No ship-return guarantees copied from third-party marketing.</li>
      <li>No invented taxi fares, ferry timetables, or wildlife promises.</li>
      <li>Images with unclear rights stay quarantined; CSS-only presentation is acceptable.</li>
      <li>Commerce stays off until a product is verified — editorial CTAs only in this phase.</li>
    </ul>
""",
        [("Home", "/"), ("Methodology", "/methodology")],
    )


def build_404() -> None:
    page(
        path="/404",
        title="Page not found | Nassau Cruise Excursions",
        description="The page you requested is not available on Nassau Cruise Excursions.",
        data_page="home",
        hero_html=hero(
            "404",
            'Page <span class="text-pr-400">not found</span>',
            "That URL is not part of this planning guide. Try the homepage or excursion comparison.",
            '<a href="/" class="btn-primary inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm shadow-xl">Home</a>'
            '<a href="/best-nassau-cruise-excursions" class="btn-outline inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm">Excursions</a>',
        ),
        trust_html=trust_strip(["Real 404", "No soft-home fallback", "Use the guides"]),
        main_html="""
<section class="py-14 bg-white">
  <div class="max-w-3xl mx-auto px-4 text-center">
    <p class="text-gray-600 mb-6">Useful starting points:</p>
    <div class="flex flex-wrap justify-center gap-3 text-sm">
      <a class="text-ocean-700 font-semibold" href="/nassau-cruise-port-guide">Port guide</a>
      <a class="text-ocean-700 font-semibold" href="/nassau-beaches">Beaches</a>
      <a class="text-ocean-700 font-semibold" href="/contact">Contact</a>
    </div>
  </div>
</section>
""",
    )


def write_robots_sitemap() -> None:
    (ROOT / "robots.txt").write_text(
        f"""User-agent: *
Allow: /

Sitemap: {APEX}/sitemap.xml
""",
        encoding="utf-8",
    )
    urls = [
        ("/", "1.0", "weekly"),
        ("/best-nassau-cruise-excursions", "0.9", "monthly"),
        ("/nassau-cruise-port-guide", "0.9", "monthly"),
        ("/nassau-beaches", "0.9", "monthly"),
        ("/nassau-snorkelling-tours", "0.8", "monthly"),
        ("/atlantis-resort-excursions", "0.8", "monthly"),
        ("/one-day-in-nassau", "0.8", "monthly"),
        ("/nassau-private-tours", "0.7", "monthly"),
        ("/about", "0.5", "yearly"),
        ("/contact", "0.5", "yearly"),
        ("/privacy", "0.5", "yearly"),
        ("/terms", "0.5", "yearly"),
        ("/methodology", "0.5", "yearly"),
    ]
    body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, pri, freq in urls:
        loc = APEX if path == "/" else f"{APEX}{path}"
        body.append("  <url>")
        body.append(f"    <loc>{loc}</loc>")
        body.append(f"    <changefreq>{freq}</changefreq>")
        body.append(f"    <priority>{pri}</priority>")
        body.append("  </url>")
    body.append("</urlset>")
    body.append("")
    (ROOT / "sitemap.xml").write_text("\n".join(body), encoding="utf-8")
    print("wrote robots.txt + sitemap.xml")


def main() -> None:
    build_home()
    build_best()
    build_port()
    build_beaches()
    build_snorkel()
    build_atlantis()
    build_oneday()
    build_private()
    build_trust_pages()
    build_404()
    write_robots_sitemap()


if __name__ == "__main__":
    main()
