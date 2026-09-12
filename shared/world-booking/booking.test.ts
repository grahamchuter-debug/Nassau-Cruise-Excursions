/**
 * Shared booking engine tests — Nassau Phase 18D (Explore Nassau Walking Tour only).
 */
import assert from "node:assert/strict";
import { test } from "node:test";
import {
  NASSAU_BOOKABLE_PRODUCTS,
  NASSAU_CANCELLATION_COPY,
  findNassauBookingProduct,
} from "../destinations/nassau-products";
import { nassauBookingCore } from "../destinations/nassau";
import {
  assertClientTotalMatches,
  calculateBookingQuote,
  createBookingReference,
  destinationBrandFromCore,
  requestedCustomerEmail,
  statusAfterPaymentSuccess,
  supplierRequestEmail,
  validateCruise,
  validateCustomer,
} from "./index";

const brand = destinationBrandFromCore(nassauBookingCore);
const walking = findNassauBookingProduct("explore-nassau-walking-tour");
assert.ok(walking);

test("single Nassau product ID present", () => {
  assert.equal(NASSAU_BOOKABLE_PRODUCTS.length, 1);
  assert.equal(NASSAU_BOOKABLE_PRODUCTS[0]!.id, "explore-nassau-walking-tour");
});

test("adult_child USD 48 / 30; ages 0–3 not sold", () => {
  assert.equal(walking!.pricing.model, "adult_child");
  assert.equal(walking!.pricing.adultAmount, 48);
  assert.equal(walking!.pricing.childAmount, 30);
  assert.equal(walking!.pricing.childPricingStatus, "priced");
  assert.equal(walking!.pricing.infantAmount, null);
  assert.equal(walking!.pricing.infantPricingStatus, "not_sold");
  assert.equal(calculateBookingQuote(walking!, { adults: 1, children: 0, infants: 0 }).amountCents, 4800);
  assert.equal(calculateBookingQuote(walking!, { adults: 2, children: 0, infants: 0 }).amountCents, 9600);
  assert.equal(calculateBookingQuote(walking!, { adults: 1, children: 1, infants: 0 }).amountCents, 7800);
  assert.equal(calculateBookingQuote(walking!, { adults: 2, children: 2, infants: 0 }).amountCents, 15600);
  assert.equal(calculateBookingQuote(walking!, { adults: 5, children: 5, infants: 0 }).amountCents, 39000);
  assert.throws(() => calculateBookingQuote(walking!, { adults: 0, children: 0, infants: 0 }));
  assert.throws(() => calculateBookingQuote(walking!, { adults: 0, children: 1, infants: 0 }));
  assert.throws(() => calculateBookingQuote(walking!, { adults: 11, children: 0, infants: 0 }));
  assert.throws(() => calculateBookingQuote(walking!, { adults: 6, children: 5, infants: 0 }));
  assert.throws(() => calculateBookingQuote(walking!, { adults: -1, children: 0, infants: 0 }));
  assert.throws(() => calculateBookingQuote(walking!, { adults: 1, children: 0, infants: 1 }));
});

test("foreign and unknown product IDs rejected by catalogue", () => {
  assert.equal(findNassauBookingProduct("historic-walking-tour"), null);
  assert.equal(findNassauBookingProduct("willemstad-historic-walking-tour"), null);
  assert.equal(findNassauBookingProduct("spice-of-grenada"), null);
  assert.equal(findNassauBookingProduct("antigua-island-highlights"), null);
  assert.equal(findNassauBookingProduct("highlights-and-beach-break"), null);
  assert.equal(findNassauBookingProduct("unknown-product"), null);
  assert.equal(findNassauBookingProduct("canahike"), null);
});

test("client total must match server quote", () => {
  const quote = calculateBookingQuote(walking!, { adults: 1, children: 0, infants: 0 });
  assert.doesNotThrow(() => assertClientTotalMatches(quote, 4800));
  assert.throws(() => assertClientTotalMatches(quote, 5700));
});

test("payment success status is requested not confirmed", () => {
  assert.equal(statusAfterPaymentSuccess("request"), "requested");
});

test("booking references use Nassau W2NAS prefix", () => {
  assert.match(createBookingReference(nassauBookingCore), /^W2NAS-/);
  assert.equal(nassauBookingCore.bookingRefPrefix, "W2NAS");
});

test("customer and cruise validation", () => {
  assert.equal(
    validateCustomer({ name: "Alex Traveller", email: "alex@example.com", phone: "+447700900123" }),
    null,
  );
  assert.ok(validateCustomer({ name: "A", email: "x", phone: "1" }));
  assert.ok(
    validateCruise({
      date: "2020-01-01",
      shipName: "Celebrity Beyond",
      shipSlug: "not-listed",
      cruiseLine: "",
      isCustomShip: true,
      scheduleMatched: false,
    }),
  );
  assert.equal(
    validateCruise({
      date: "2027-03-15",
      shipName: "Celebrity Beyond",
      shipSlug: "not-listed",
      cruiseLine: "",
      isCustomShip: true,
      scheduleMatched: false,
    }),
    null,
  );
});

test("customer email brand and wording — no SEG / canahike leakage", () => {
  const mail = requestedCustomerEmail({
    reference: "W2NAS-TEST1",
    product: walking!,
    cruise: {
      date: "2027-03-15",
      shipName: "Celebrity Beyond",
      shipSlug: "not-listed",
      cruiseLine: "",
      isCustomShip: true,
      scheduleMatched: false,
    },
    guests: { adults: 1, children: 0, infants: 0 },
    amountLabel: "USD $48.00",
    customerName: "Alex Traveller",
    brand,
  });
  assert.match(mail.subject, /request|received/i);
  assert.match(mail.shell.summaryRows.map((r) => r.value).join(" "), /Explore Nassau Walking Tour/);
  const blob = `${mail.subject}\n${mail.body}\n${JSON.stringify(mail.shell)}`;
  assert.doesNotMatch(blob, /\bSEG\b|canahike|SEG_MANUAL|info@wowatour\.com|shoreexcursionsgroup/i);
  assert.match(blob, /not.*confirm|confirm.*separately|request/i);
});

test("ops email includes ACTION REQUIRED, phone, and internal supply", () => {
  const ops = supplierRequestEmail({
    reference: "W2NAS-TEST1",
    product: walking!,
    cruise: {
      date: "2027-03-15",
      shipName: "Celebrity Beyond",
      shipSlug: "not-listed",
      cruiseLine: "",
      isCustomShip: true,
      scheduleMatched: false,
    },
    guests: { adults: 2, children: 1, infants: 0 },
    customer: {
      name: "Alex Traveller",
      email: "alex@example.com",
      phone: "+447700900123",
    },
    amountLabel: "USD $126.00",
    destinationLabel: "Nassau Cruise Excursions — new booking request",
  });
  assert.match(ops.subject, /ACTION REQUIRED/);
  assert.match(ops.body, /\+447700900123/);
  assert.match(ops.body, /canahike|SEG_MANUAL/i);
  assert.match(ops.body, /Alex Traveller/);
  assert.match(NASSAU_CANCELLATION_COPY.customerCancellation, /outside 14 days/i);
  assert.match(NASSAU_CANCELLATION_COPY.unableToConfirm, /full refund/i);
});
