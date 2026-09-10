/* Water Damage Restoration Largo — site behaviour */
(function () {
  var d = document;

  /* sticky header shadow */
  var hdr = d.querySelector('.site-header');
  if (hdr) {
    var onScroll = function () { hdr.classList.toggle('scrolled', window.scrollY > 10); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* desktop mega menus */
  var triggers = [].slice.call(d.querySelectorAll('[data-mega]'));
  function closeAll(except) {
    triggers.forEach(function (t) {
      if (t === except) return;
      t.setAttribute('aria-expanded', 'false');
      var p = d.getElementById(t.getAttribute('data-mega'));
      if (p) p.classList.remove('open');
    });
  }
  triggers.forEach(function (t) {
    var panel = d.getElementById(t.getAttribute('data-mega'));
    if (!panel) return;
    var li = t.parentNode;
    var open = function (v) {
      t.setAttribute('aria-expanded', v ? 'true' : 'false');
      panel.classList.toggle('open', v);
      if (v) closeAll(t);
    };
    t.addEventListener('click', function (e) {
      e.preventDefault();
      open(t.getAttribute('aria-expanded') !== 'true');
    });
    li.addEventListener('mouseenter', function () { open(true); });
    li.addEventListener('mouseleave', function () { open(false); });
    panel.addEventListener('focusout', function (e) {
      if (!li.contains(e.relatedTarget)) open(false);
    });
  });
  d.addEventListener('click', function (e) {
    if (!e.target.closest('.nav')) closeAll(null);
  });
  d.addEventListener('keydown', function (e) { if (e.key === 'Escape') { closeAll(null); drawer(false); } });

  /* mobile drawer */
  var dr = d.querySelector('.drawer'), scrim = d.querySelector('.scrim'), burger = d.querySelector('.burger');
  function drawer(v) {
    if (!dr) return;
    dr.classList.toggle('open', v);
    if (scrim) scrim.classList.toggle('open', v);
    if (burger) burger.setAttribute('aria-expanded', v ? 'true' : 'false');
    d.documentElement.style.overflow = v ? 'hidden' : '';
  }
  if (burger) burger.addEventListener('click', function () { drawer(!dr.classList.contains('open')); });
  if (scrim) scrim.addEventListener('click', function () { drawer(false); });
  var dc = d.querySelector('.drawer-close');
  if (dc) dc.addEventListener('click', function () { drawer(false); });

  /* drawer collapsible submenus */
  [].slice.call(d.querySelectorAll('.acc-btn')).forEach(function (b) {
    b.addEventListener('click', function () {
      var sub = b.nextElementSibling, on = sub.classList.toggle('open');
      b.setAttribute('aria-expanded', on ? 'true' : 'false');
    });
  });

  /* scroll reveal */
  var items = [].slice.call(d.querySelectorAll('.rv'));
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
    items.forEach(function (el) { io.observe(el); });
  }

  /* FAQ accordion: one open at a time within a group */
  [].slice.call(d.querySelectorAll('.faq')).forEach(function (group) {
    var all = [].slice.call(group.querySelectorAll('details'));
    all.forEach(function (det) {
      det.addEventListener('toggle', function () {
        if (det.open) all.forEach(function (o) { if (o !== det) o.open = false; });
      });
    });
  });

  /* current year */
  [].slice.call(d.querySelectorAll('[data-year]')).forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
