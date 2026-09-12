/**
 * Nassau Cruise Excursions — Workers Assets entry (Phase 18B).
 * Canonical: extensionless WITHOUT trailing slash on apex HTTPS.
 * www → apex; .html → extensionless; trailing slash → drop; query preserved.
 * Legacy soft-home traps and thin routes redirect to real pages (no soft-404).
 */
const APEX_HOST = 'nassaucruiseexcursions.com';

/** Explicit legacy / soft-home maps (checked before generic .html stripping). */
const LEGACY_REDIRECTS = {
  '/beaches': '/nassau-beaches',
  '/family-tours': '/best-nassau-cruise-excursions',
  '/book': '/',
  '/book.html': '/',
  '/swimming-pigs-excursions': '/best-nassau-cruise-excursions',
  '/swimming-pigs-excursions.html': '/best-nassau-cruise-excursions',
  '/nassau-faq': '/nassau-cruise-port-guide',
  '/nassau-faq.html': '/nassau-cruise-port-guide',
  '/contact.html': '/contact',
  '/about.html': '/about',
  '/privacy.html': '/privacy',
  '/terms.html': '/terms',
  '/index.html': '/',
};

function toCanonicalPath(pathname) {
  let path = pathname || '/';
  if (path.toLowerCase().endsWith('.html')) {
    path = path.slice(0, -5);
    if (path.toLowerCase().endsWith('/index')) path = path.slice(0, -6);
    if (path === '' || path === '/index') path = '/';
  }
  if (path.length > 1 && path.endsWith('/')) {
    path = path.replace(/\/+$/, '') || '/';
  }
  return path || '/';
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const host = url.hostname.toLowerCase();
    const isWww = host === `www.${APEX_HOST}`;
    const isHttp = url.protocol === 'http:';
    const rawPath = url.pathname || '/';
    const rawLower = rawPath.toLowerCase();
    const is404Doc = rawLower === '/404.html';

    const legacyTarget = LEGACY_REDIRECTS[rawLower] || LEGACY_REDIRECTS[rawPath];
    if (legacyTarget && !is404Doc) {
      const dest = new URL(url.toString());
      dest.hostname = APEX_HOST;
      dest.protocol = 'https:';
      dest.pathname = legacyTarget;
      return Response.redirect(dest.toString(), 301);
    }

    const hasHtml = rawLower.endsWith('.html');
    const hasTrail =
      rawPath.length > 1 && rawPath.endsWith('/') && !rawPath.includes('.');

    if ((isWww || isHttp || hasHtml || hasTrail) && !is404Doc) {
      const dest = new URL(url.toString());
      dest.hostname = APEX_HOST;
      dest.protocol = 'https:';
      dest.pathname = toCanonicalPath(rawPath);
      if (dest.toString() !== url.toString()) {
        return Response.redirect(dest.toString(), 301);
      }
    }

    if (isWww || isHttp) {
      const dest = new URL(url.toString());
      dest.hostname = APEX_HOST;
      dest.protocol = 'https:';
      if (dest.toString() !== url.toString()) {
        return Response.redirect(dest.toString(), 301);
      }
    }

    const assetResponse = await env.ASSETS.fetch(request);

    if (assetResponse.status === 404) {
      const notFound = await env.ASSETS.fetch(new URL('/404.html', url.origin));
      return new Response(notFound.body, {
        status: 404,
        headers: {
          'content-type': 'text/html; charset=utf-8',
          'cache-control': 'no-store',
        },
      });
    }

    return assetResponse;
  },
};
