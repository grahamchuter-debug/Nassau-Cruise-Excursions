/**
 * Progressive enhancement only — primary content is inlined HTML.
 * Mobile nav + active nav highlighting.
 */
(function () {
  function setActiveNav() {
    var page = document.body && document.body.dataset.page;
    if (!page) return;
    document.querySelectorAll('[data-nav]').forEach(function (link) {
      var isActive = link.dataset.nav === page;
      link.classList.toggle('text-ocean-600', isActive);
      link.classList.toggle('font-semibold', isActive);
      link.classList.toggle('text-gray-600', !isActive);
      if (isActive) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });
  }

  function wireMobileNav() {
    var nav = document.querySelector('#site-nav nav') || document.querySelector('nav');
    if (!nav) return;
    var btn = nav.querySelector('#menu-toggle') || nav.querySelector('button[aria-label="Open menu"], button[aria-label="Close menu"]');
    if (!btn) return;

    var panel = nav.querySelector('[data-mobile-panel]') || nav.querySelector('#mobile-menu');
    if (!panel) return;

    function setOpen(open) {
      if (open) {
        panel.removeAttribute('hidden');
        panel.classList.remove('hidden');
      } else {
        panel.setAttribute('hidden', '');
        panel.classList.add('hidden');
      }
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    }

    if (btn.dataset.wired === 'true') return;
    btn.dataset.wired = 'true';
    setOpen(false);
    btn.addEventListener('click', function () {
      var isHidden = panel.hasAttribute('hidden') || panel.classList.contains('hidden');
      setOpen(isHidden);
    });
    panel.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        setOpen(false);
      });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    setActiveNav();
    wireMobileNav();
  });
})();
