/**
 * Public commercial status for Nassau Cruise Excursions (Phase 18D).
 * Internal supply references must never appear on customer pages.
 *
 * Gate values:
 * - BOOKING_ENABLED — journey visible; live Pay & request disabled
 * - BOOKING_ENABLED — live checkout allowed (requires Worker LIVE unlock too)
 */
window.NAS_COMMERCIAL = {
  bookingsApiUrl: "https://nassau-bookings-prod.dark-violet-8d91.workers.dev",
  email: "hello@nassaucruiseexcursions.com",
  siteName: "Nassau Cruise Excursions",
  defaultPublicBookingStatus: "BOOKING_ENABLED",
  cancellation:
    "Free cancellation outside 14 days before your excursion. From the 14th day before your excursion, bookings are non-refundable.",
  paymentNotConfirmation:
    "Secure your booking request with payment today. We'll confirm your excursion separately, and if we're unable to confirm it, you'll receive a full refund.",
  unableToConfirm:
    "If we are unable to confirm your excursion after payment, you will receive a full refund to your original payment method.",
  meetingInstructions:
    "Meeting: approximately a 5–15 minute walk from the cruise pier. Exact meeting details are supplied after confirmation.",
  overTenGuidance:
    "For groups larger than 10, email hello@nassaucruiseexcursions.com before requesting.",
  products: {
    "explore-nassau-walking-tour": {
      productId: "explore-nassau-walking-tour",
      slug: "explore-nassau-walking-tour",
      name: "Explore Nassau Walking Tour",
      shortTitle: "Explore Walking Tour",
      productPath: "/one-day-in-nassau",
      bookingPath: "/book/explore-nassau-walking-tour",
      receivedPath: "/book/explore-nassau-walking-tour/received",
      adultUsd: 48,
      childUsd: 30,
      infantUsd: null,
      guestModel: "adult_child",
      durationLabel: "1 hour 30 minutes",
      maxGuests: 10,
      publicBookingStatus: "BOOKING_ENABLED",
      displayPrice: "Adults $48 · Children (ages 4–12) $30 · Ages 0–3 contact us",
    },
  },
};
