#!/usr/bin/env python3
"""Generate /book/{slug}/ and /book/{slug}/received/ for Nassau Explore Walking RTB.

Canonical URLs: HTTPS, apex, extensionless, no trailing slash.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_nassau_pages import footer_html, nav_html  # noqa: E402

PRODUCTS = [
    {
        "id": "explore-nassau-walking-tour",
        "name": "Explore Nassau Walking Tour",
        "product_path": "/one-day-in-nassau",
        "price_list": (
            "<li>Adults — $48</li>"
            "<li>Children (ages 4–12) — $30</li>"
            "<li>Ages 0–3 — not bookable online</li>"
            "<li>Maximum 10 participants online</li>"
        ),
        "duration": "1 hour 30 minutes",
        "meeting": (
            "Meeting: approximately a 5–15 minute walk from the cruise pier. "
            "Exact meeting details are supplied after confirmation."
        ),
        "truth": (
            "A guided historic Nassau walking experience covering central landmarks such as "
            "Queen's Staircase, the Fort Fincastle area / historic fort context, "
            "and Rawson / Parliament Square, with Lucayan / Arawak history framing. "
            "Do not assume Fort Fincastle interior entry is included or that the fort is open. "
            "Food and beverages are not included. Moderate walking is required; Queen's Staircase "
            "includes 66 steps. Not wheelchair accessible. Guests should be physically fit for walking."
        ),
    },
]


def guest_fieldset(name: str) -> str:
    return f"""
        <fieldset class="booking-fieldset">
          <legend>How many people are travelling?</legend>
          <label for="adults">Adults <span class="muted">— $48 each</span>
            <input type="number" name="adults" id="adults" min="1" max="10" value="2" required />
          </label>
          <label for="children">Children (ages 4–12) <span class="muted">— $30 each</span>
            <input type="number" name="children" id="children" min="0" max="10" value="0" />
          </label>
          <p class="help">At least one adult is required. Maximum 10 participants online. For larger groups email <a href="mailto:hello@nassaucruiseexcursions.com">hello@nassaucruiseexcursions.com</a>.</p>
          <p class="help">Travelling with a child aged 0–3? Please contact us before booking at <a href="mailto:hello@nassaucruiseexcursions.com">hello@nassaucruiseexcursions.com</a>.</p>
        </fieldset>
        <div class="booking-review" id="booking-review" aria-live="polite">
          <h3>Review</h3>
          <dl>
            <div><dt>Tour</dt><dd>{name}</dd></div>
            <div><dt>Date</dt><dd id="rev-date">—</dd></div>
            <div><dt>Cruise ship</dt><dd id="rev-ship">—</dd></div>
            <div><dt>Adults</dt><dd id="rev-adults">—</dd></div>
            <div id="rev-children-row"><dt>Children</dt><dd id="rev-children">—</dd></div>
            <div class="booking-total"><dt>Total</dt><dd id="rev-total">USD $0</dd></div>
          </dl>
          <p class="help">Displayed total is for review. The charge amount is always calculated server-side. This is a request — payment does not confirm the excursion.</p>
        </div>"""


def book_page(p: dict) -> str:
    pid = p["id"]
    name = p["name"]
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Book {name} | Nassau Cruise Excursions</title>
  <meta name="description" content="Request {name} online. Pay securely to request — confirmation is emailed separately." />
  <link rel="canonical" href="https://nassaucruiseexcursions.com/book/{pid}" />
  <meta name="robots" content="noindex,follow" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700&amp;family=Source+Sans+3:wght@400;500;600;700&amp;display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/css/site.css" />
</head>
<body data-page="book" data-product-id="{pid}">
{nav_html("home")}
<main id="main" class="page-main">

<section class="section booking-flow">
  <div class="wrap booking-shell px-4 sm:px-6">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="/">Home</a> · <a href="{p["product_path"]}">{name}</a> · Booking
    </nav>
    <p class="eyebrow">Booking request</p>
    <h1 class="text-3xl font-display font-bold text-gray-900 mb-3">Book your excursion</h1>
    <p class="text-gray-600 mb-4">Choose your cruise date and complete payment to send your booking request. Confirmation is emailed separately after we arrange your excursion.</p>
    <ol class="booking-steps" aria-label="Booking steps">
      <li class="is-current">Tour</li>
      <li>Date / cruise</li>
      <li>Guests</li>
      <li>Details</li>
      <li>Review</li>
      <li>Payment</li>
      <li>Received</li>
    </ol>
    <div class="booking-panel">
      <h2 class="text-xl font-display font-bold text-gray-900">{name}</h2>
      <ul class="price-list">{p["price_list"]}</ul>
      <p class="help">{p["duration"]}. {p["meeting"]}</p>
      <p class="help">{p["truth"]}</p>
      <div class="booking-status-banner" id="booking-status-banner" role="status">
        <strong id="booking-status-title">Book with confidence</strong>
        <p id="booking-status-body">Secure your booking request with payment today. We'll confirm your excursion separately, and if we're unable to confirm it, you'll receive a full refund.</p>
      </div>
      <form class="booking-form" id="nas-booking-form" method="post" action="#" data-product-id="{pid}" data-live="0" novalidate>
        <fieldset class="booking-fieldset">
          <legend>Date / cruise</legend>
          <label for="cruise_date">Excursion date
            <input type="date" name="cruise_date" id="cruise_date" required min="2026-09-01" max="2028-12-31" />
          </label>
          <label for="ship_name">Cruise ship
            <input type="text" name="ship_name" id="ship_name" required maxlength="80" autocomplete="organization" placeholder="e.g. Celebrity Beyond" />
          </label>
          <p class="help">Enter your ship and date. We do not show live supplier availability — confirmation follows after your request.</p>
        </fieldset>
{guest_fieldset(name)}
        <fieldset class="booking-fieldset">
          <legend>Lead passenger details</legend>
          <label for="lead_name">Full name
            <input type="text" name="name" id="lead_name" required minlength="2" autocomplete="name" />
          </label>
          <label for="lead_email">Email
            <input type="email" name="email" id="lead_email" required autocomplete="email" />
          </label>
          <label for="lead_phone">Mobile / WhatsApp
            <input type="tel" name="phone" id="lead_phone" required autocomplete="tel" />
          </label>
          <label for="mobility">Mobility information
            <textarea name="mobility" id="mobility" rows="2" maxlength="500" placeholder="Any walking limits or mobility needs we should know about"></textarea>
          </label>
          <label for="special_requirements">Special requirements <span class="muted">(optional)</span>
            <textarea name="special_requirements" id="special_requirements" rows="2" maxlength="800"></textarea>
          </label>
          <p class="help">The booking contact must be an adult.</p>
        </fieldset>
        <div class="booking-honesty" id="booking-honesty">
          <h3>Book with confidence</h3>
          <p>Secure your booking request with payment today. We'll confirm your excursion separately, and if we're unable to confirm it, you'll receive a full refund.</p>
          <p>Free cancellation outside 14 days before your excursion. From the 14th day before your excursion, bookings are non-refundable.</p>
        </div>
        <label class="consent">
          <input type="checkbox" name="ack" id="booking_ack" required />
          <span>I understand this is a booking request. Payment is taken when I submit my request and does not confirm the excursion. Confirmation will be emailed separately when my places are confirmed. If the excursion cannot be confirmed, the amount paid will be refunded in full to my original payment method.</span>
        </label>
        <p id="booking-error" class="booking-error" hidden role="alert"></p>
        <div class="booking-actions">
          <a class="btn btn--outline" href="{p["product_path"]}">Back</a>
          <button type="submit" class="btn btn--solid" id="booking-submit" hidden>Pay &amp; request</button>
          <button type="button" class="btn btn--solid" id="booking-submit-locked" disabled title="Live checkout is locked">Checkout locked — opening soon</button>
        </div>
        <p class="help" id="booking-footer-note">Prefer to ask first? <a href="mailto:hello@nassaucruiseexcursions.com">hello@nassaucruiseexcursions.com</a></p>
      </form>
    </div>
  </div>
</section>

</main>
{footer_html()}
  <script src="/js/commercial-config.js" defer></script>
  <script src="/js/booking.js" defer></script>
  <script src="/js/nav.js" defer></script>
</body>
</html>
"""


def received_page(p: dict) -> str:
    pid = p["id"]
    name = p["name"]
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Booking request received | Nassau Cruise Excursions</title>
  <meta name="description" content="Your Nassau excursion payment was received. This is a booking request, not a confirmation." />
  <link rel="canonical" href="https://nassaucruiseexcursions.com/book/{pid}/received" />
  <meta name="robots" content="noindex,follow" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700&amp;family=Source+Sans+3:wght@400;500;600;700&amp;display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/css/site.css" />
</head>
<body data-page="book-received" data-product-id="{pid}">
{nav_html("home")}
<main id="main" class="page-main">

<section class="section booking-flow">
  <div class="wrap booking-shell px-4 sm:px-6">
    <p class="eyebrow">Request received</p>
    <h1 class="text-3xl font-display font-bold text-gray-900 mb-3">We've received your request</h1>
    <p class="text-gray-600 mb-4">We've received your payment and your excursion request. This is not a booking confirmation. We're arranging your {name} and will email you again once it is confirmed.</p>
    <div id="booking-ref-wrap" class="booking-ref" hidden>
      <p class="muted">Your reference</p>
      <p id="booking-ref" class="booking-ref__code"></p>
    </div>
    <p class="help">If we are unable to confirm your excursion, you will receive a full refund to your original payment method.</p>
    <div class="booking-actions">
      <a class="btn btn--solid" href="/">Back to home</a>
      <a class="btn btn--outline" href="mailto:hello@nassaucruiseexcursions.com">Contact us</a>
    </div>
  </div>
</section>

</main>
{footer_html()}
  <script src="/js/booking-received.js" defer></script>
  <script src="/js/nav.js" defer></script>
</body>
</html>
"""


def main() -> None:
    for p in PRODUCTS:
        book_dir = ROOT / "book" / p["id"]
        received_dir = book_dir / "received"
        book_dir.mkdir(parents=True, exist_ok=True)
        received_dir.mkdir(parents=True, exist_ok=True)
        (book_dir / "index.html").write_text(book_page(p), encoding="utf-8")
        (received_dir / "index.html").write_text(received_page(p), encoding="utf-8")
        print(f"wrote /book/{p['id']} and /book/{p['id']}/received")


if __name__ == "__main__":
    main()
