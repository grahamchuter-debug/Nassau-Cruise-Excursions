import { nassauBookingCore } from "./nassau";
import type { AgeBand, BookableProductConfig, ProductCapacity, ProductPricing } from "../world-booking/types";

/**
 * Operational routing: Wow A Tour ops mailbox for Graham’s manual fulfilment.
 * Public customers never see SEG. Graham places corresponding bookings via his
 * established SEG affiliate / white-label account using INTERNAL supply refs only.
 */
const OPERATIONS = {
  id: "wow-a-tour-operations",
  displayName: "Wow A Tour",
  notificationEmail: "info@wowatour.com",
  routingStatus: "production_ready" as const,
};

const REQUEST_SETTLEMENT = "charge_refund" as const;

/** Graham online max — never describe as supplier capacity. */
const NAS_CAPACITY: ProductCapacity = {
  minGuests: 1,
  maxGuestsPerBooking: 10,
  maxGuestsPerBookingSource: "approved",
  supplierGroupSize: null,
  maxGuestsPerGuide: null,
};

/**
 * Phase 18D Graham-approved:
 * Adult $48 · Child $30 (ages 4–12).
 * Ages 0–3 NOT BOOKABLE ONLINE (infant band not_sold — reject).
 * At least one adult required (shared adult_child engine rule).
 */
const WALK_AGE_BANDS: readonly AgeBand[] = [
  { id: "adult", label: "Adults", minAge: 13, maxAge: null, pricingStatus: "priced" },
  { id: "child", label: "Children (ages 4–12)", minAge: 4, maxAge: 12, pricingStatus: "priced" },
  { id: "infant", label: "Ages 0–3", minAge: 0, maxAge: 3, pricingStatus: "not_sold" },
];

function adultChildUsd(adultAmount: number, childAmount: number): ProductPricing {
  return {
    model: "adult_child",
    currency: "USD",
    adultAmount,
    childAmount,
    childPricingStatus: "priced",
    infantAmount: null,
    infantPricingStatus: "not_sold",
    pricingNeedsConfirmation: false,
  };
}

const SHARED_PENDING = [
  "Customer cancellation APPROVED: free outside 14 days before excursion; from the 14th day non-refundable.",
  "Unable to confirm after payment: full refund to original payment method.",
  "Meeting: approximately a 5–15 minute walk from the cruise pier; exact instructions after confirmation.",
  "Fulfilment: Graham places corresponding booking via established SEG affiliate / white-label route (INTERNAL).",
  "Payment received ≠ excursion confirmed.",
  "Online max 10 guests per booking (Graham online limit — not supplier capacity).",
  "At least one adult required (engine adult_child rule).",
  "Ages 0–3 NOT BOOKABLE ONLINE — contact hello@nassaucruiseexcursions.com.",
  "Do NOT promise Fort Fincastle interior entry / open admission (source status UNCLEAR / closed note).",
  "Queen's Staircase remains source-supported in itinerary wording.",
  "commercial_status=SEG_FULFILMENT_READY · fulfilment_mode=SEG_MANUAL · supplier=UNKNOWN · direct_supplier_status=NOT_CONTACTED · net_cost=UNKNOWN · margin=UNKNOWN",
] as const;

export const NASSAU_CANCELLATION_COPY = {
  customerCancellation:
    "Free cancellation outside 14 days before your excursion. From the 14th day before your excursion, bookings are non-refundable. If we are unable to confirm your excursion after payment, you will receive a full refund to your original payment method.",
  freeWindow: "Free cancellation outside 14 days before your excursion.",
  insideWindow: "From the 14th day before your excursion, bookings are non-refundable.",
  unableToConfirm:
    "If we are unable to confirm your excursion after payment, you will receive a full refund to your original payment method.",
  paymentNotConfirmation:
    "Secure your booking request with payment today. We'll confirm your excursion separately, and if we're unable to confirm it, you'll receive a full refund.",
  meetingInstructions:
    "Meeting: approximately a 5–15 minute walk from the cruise pier. Exact meeting details are supplied after confirmation.",
  overTenGuidance: "For groups larger than 10, email hello@nassaucruiseexcursions.com before requesting.",
} as const;

const EXPLORE_WALK: BookableProductConfig = {
  id: "explore-nassau-walking-tour",
  destinationId: nassauBookingCore.id,
  slug: "explore-nassau-walking-tour",
  name: "Explore Nassau Walking Tour",
  durationLabel: "1 hour 30 minutes",
  bookingMode: "request",
  availability: "live",
  bookingPath: "/book/explore-nassau-walking-tour",
  receivedPath: "/book/explore-nassau-walking-tour/received",
  confirmedPath: "/book/explore-nassau-walking-tour/received",
  productPath: "/one-day-in-nassau",
  pricing: adultChildUsd(48, 30),
  ageBands: WALK_AGE_BANDS,
  capacity: NAS_CAPACITY,
  requiredCustomerFields: ["name", "email", "phone"],
  supplier: OPERATIONS,
  paymentSettlement: REQUEST_SETTLEMENT,
  schedulePortSlug: "nassau",
  pendingCommercialRules: [
    ...SHARED_PENDING,
    "Adult USD 48 · Child USD 30 (ages 4–12) · Ages 0–3 not bookable online",
    "Guided historic Nassau walking · Queen's Staircase · Parliament Square / Rawson context · Lucayan/Arawak history framing",
    "Food and beverages NOT included",
    "Moderate activity · walking required · Queen's Staircase includes 66 steps · not wheelchair accessible · physically fit for walking",
    "Do NOT claim Fort Fincastle interior entry, open fort admission, ship-return guarantees, or invented meeting landmarks",
  ],
  supplierReferenceNotes: [
    "INTERNAL SUPPLY: SEG_MANUAL · canahike",
    "INTERNAL CODE: canahike",
    "Supplier contact: UNKNOWN · NOT_CONTACTED · net/margin UNKNOWN",
    "Fulfilment: place via established SEG affiliate / white-label route (manual — do not automate).",
    "Selling: Adult USD 48 · Child USD 30 (ages 4–12) · Ages 0–3 NOT BOOKABLE ONLINE.",
    "Customer cancellation: Free cancellation outside 14 days before your excursion. From the 14th day before your excursion, bookings are non-refundable.",
    "Unable to confirm after payment: full refund to original payment method.",
  ],
};

export const NASSAU_BOOKABLE_PRODUCTS: readonly BookableProductConfig[] = [EXPLORE_WALK];

export function findNassauBookingProduct(productId: string): BookableProductConfig | null {
  return NASSAU_BOOKABLE_PRODUCTS.find((p) => p.id === productId) ?? null;
}

export function listNassauBookingProducts(): readonly BookableProductConfig[] {
  return NASSAU_BOOKABLE_PRODUCTS;
}
