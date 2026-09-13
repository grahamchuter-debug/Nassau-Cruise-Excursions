/**
 * Authenticated internal Stripe event handoff from the shared World 2.0 webhook gateway.
 * Stripe signature is verified once at the gateway — this route must never be public-unauthenticated.
 */
import type Stripe from "stripe";
import { findNassauBookingProduct } from "../../../../shared/destinations/nassau-products";
import { jsonResponse } from "../cors";
import { claimEvent, eventAlreadyProcessed, getBookingByPaymentIntentId } from "../db";
import { deliverOutboxForBooking } from "../email";
import {
  fulfillCheckoutSession,
  markPaymentFailedFromIntent,
  markPaymentFailedFromSession,
  markRefundedFromCharge,
} from "../fulfill";
import { enqueuePostPaymentNotifications } from "../notify";
import { createStripe } from "../stripe";
import { StripeModeError } from "../stripe-guard";

export type GatewayHandoffPayload = {
  event_id: string;
  event_type: string;
  stripe_created: number;
  world_version: string;
  destination: string;
  booking_reference: string | null;
  product_id: string | null;
  booking_worker: string | null;
  environment: "test" | "live";
  checkout_session_id: string | null;
  payment_intent_id: string | null;
  amount_total: number | null;
  currency: string | null;
  payment_status: string | null;
  charge_fully_refunded: boolean | null;
  refund_status: string | null;
};

function gatewayTokenOk(request: Request, env: Env): boolean {
  const expected = String(env.GATEWAY_HANDOFF_TOKEN || "").trim();
  if (!expected) return false;
  const auth = request.headers.get("authorization") || "";
  const match = /^Bearer\s+(.+)$/i.exec(auth);
  if (!match) return false;
  const provided = match[1]!.trim();
  if (provided.length !== expected.length) return false;
  let diff = 0;
  for (let i = 0; i < expected.length; i++) diff |= expected.charCodeAt(i) ^ provided.charCodeAt(i);
  return diff === 0;
}

async function scheduleOutbox(env: Env, reference: string, ctx?: ExecutionContext): Promise<void> {
  const run = deliverOutboxForBooking(env, reference);
  if (ctx?.waitUntil) ctx.waitUntil(run);
  else await run;
}

function paymentsMode(env: Env): string {
  return String(env.PAYMENTS_MODE ?? "preview");
}

export async function handleGatewayStripeEvent(request: Request, env: Env, ctx?: ExecutionContext): Promise<Response> {
  if (!gatewayTokenOk(request, env)) {
    return jsonResponse({ ok: false, code: "UNAUTHORIZED", message: "Unauthorized." }, 401);
  }

  const body = (await request.json().catch(() => null)) as GatewayHandoffPayload | null;
  if (!body || typeof body !== "object" || typeof body.event_id !== "string" || typeof body.event_type !== "string") {
    return jsonResponse({ ok: false, code: "INVALID_BODY", message: "Invalid handoff payload." }, 400);
  }

  if (body.destination !== "nassau") {
    return jsonResponse({ ok: false, code: "FOREIGN_DESTINATION", message: "Not a Nassau event." }, 400);
  }

  const mode = paymentsMode(env);
  const expectedEnv = mode === "live" ? "live" : "test";
  if (body.environment !== expectedEnv) {
    return jsonResponse({ ok: false, code: "ENVIRONMENT", message: "Environment mismatch." }, 400);
  }

  if (body.product_id) {
    const product = findNassauBookingProduct(body.product_id);
    if (!product) {
      return jsonResponse({ ok: false, code: "FOREIGN_PRODUCT", message: "Unknown product." }, 400);
    }
  }

  if (body.booking_reference && !/^W2NAS-[A-Z0-9]+$/i.test(body.booking_reference)) {
    return jsonResponse({ ok: false, code: "BAD_REFERENCE", message: "Invalid booking reference." }, 400);
  }

  if (await eventAlreadyProcessed(env, body.event_id)) {
    return jsonResponse({ ok: true, received: true, duplicate: true });
  }

  try {
    switch (body.event_type) {
      case "checkout.session.completed":
      case "checkout.session.async_payment_succeeded": {
        if (!body.checkout_session_id) {
          return jsonResponse({ ok: false, code: "MISSING_SESSION", message: "checkout_session_id required." }, 400);
        }
        const stripe = createStripe(env);
        const session = await stripe.checkout.sessions.retrieve(body.checkout_session_id);
        const booking = await fulfillCheckoutSession(env, session);
        if (booking) {
          await enqueuePostPaymentNotifications(env, booking);
          await scheduleOutbox(env, booking.booking_reference, ctx);
        }
        break;
      }
      case "checkout.session.async_payment_failed": {
        if (!body.checkout_session_id) break;
        const stripe = createStripe(env);
        const session = await stripe.checkout.sessions.retrieve(body.checkout_session_id);
        await markPaymentFailedFromSession(env, session);
        break;
      }
      case "payment_intent.payment_failed": {
        if (!body.payment_intent_id) break;
        const stripe = createStripe(env);
        const intent = await stripe.paymentIntents.retrieve(body.payment_intent_id);
        await markPaymentFailedFromIntent(env, intent);
        break;
      }
      case "charge.refunded": {
        if (body.payment_intent_id) {
          await markRefundedFromCharge(env, body.payment_intent_id, Boolean(body.charge_fully_refunded));
        }
        break;
      }
      case "refund.updated": {
        if (body.refund_status === "succeeded" && body.payment_intent_id) {
          const booking = await getBookingByPaymentIntentId(env, body.payment_intent_id);
          if (booking && booking.payment_status !== "refunded") {
            await markRefundedFromCharge(env, body.payment_intent_id, true);
          }
        }
        break;
      }
      default:
        break;
    }

    await claimEvent(env, body.event_id, body.event_type, body.booking_reference);
  } catch (err) {
    if (err instanceof StripeModeError) {
      return jsonResponse({ ok: false, code: err.code, message: err.message }, 503);
    }
    console.error("gateway_handoff_error", body.event_type, String(err));
    return jsonResponse({ ok: false, code: "HANDOFF", message: "Handoff processing failed." }, 500);
  }

  console.log(
    JSON.stringify({
      handoff: "gateway_stripe_event",
      event_id: body.event_id,
      event_type: body.event_type,
      booking_reference: body.booking_reference,
      result: "ok",
    }),
  );

  return jsonResponse({ ok: true, received: true });
}

/** Type-only keep Stripe import used when retrieving objects. */
export type _Stripe = Stripe;
