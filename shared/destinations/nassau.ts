/**
 * Nassau destination booking core.
 * Product catalogue: shared/destinations/nassau-products.ts
 * Public editorial: scripts/build_nassau_pages.py
 * Internal supply mapping: product.supplierReferenceNotes (never public HTML)
 */
import type { DestinationBookingCore } from "../world-booking/types";

export const nassauBookingCore = {
  id: "nassau",
  siteName: "Nassau Cruise Excursions",
  siteHostname: "nassaucruiseexcursions.com",
  siteUrl: "https://nassaucruiseexcursions.com",
  bookingEmail: "hello@nassaucruiseexcursions.com",
  originatingSite: "nassaucruiseexcursions.com",
  originatingPort: "Nassau, Bahamas",
  bookingRefPrefix: "W2NAS",
  sessionKeyPrefix: "w2-nas-booking",
  sessionKeyVersion: 1,
  currencyCode: "USD",
  bookableWindow: {
    start: "2026-09-01",
    end: "2028-12-31",
  },
  /** No specialist schedule import — cruise date/ship are customer-entered. */
  schedulePortSlug: "nassau",
  customShipSlug: "not-listed",
  contactPath: "/contact",
  termsPath: "/terms",
  privacyPath: "/privacy",
} as const satisfies DestinationBookingCore;
