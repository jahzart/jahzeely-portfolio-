/* Jahzeely Sinai portfolio: interactions and motion */
(function () {
  var root = document.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasGsap = typeof window.gsap !== 'undefined';
  var splits = [];
  var smoother = null;

  function store(key, val) {
    try { if (val === undefined) return localStorage.getItem(key); localStorage.setItem(key, val); } catch (e) { return null; }
  }
  function session(key, val) {
    try { if (val === undefined) return sessionStorage.getItem(key); sessionStorage.setItem(key, val); } catch (e) { return null; }
  }

  /* ---------- Language ---------- */
  function applyLang(lang) {
    splits.forEach(function (s) { s.revert(); });
    splits = [];
    document.querySelectorAll('[data-en]').forEach(function (el) {
      var v = el.getAttribute('data-' + lang);
      if (v !== null) el.textContent = v;
    });
    document.querySelectorAll('[data-en-aria]').forEach(function (el) {
      el.setAttribute('aria-label', el.getAttribute('data-' + lang + '-aria'));
    });
    root.lang = lang;
    document.querySelectorAll('.lang button').forEach(function (b) {
      b.setAttribute('aria-pressed', b.dataset.lang === lang ? 'true' : 'false');
    });
    if (window.ScrollTrigger) window.ScrollTrigger.refresh();
  }
  var lang = store('lang') === 'es' ? 'es' : 'en';
  if (lang === 'es') applyLang('es');
  document.querySelectorAll('.lang button').forEach(function (b) {
    b.setAttribute('aria-pressed', b.dataset.lang === lang ? 'true' : 'false');
    b.addEventListener('click', function () {
      lang = b.dataset.lang; store('lang', lang); applyLang(lang);
    });
  });

  /* ---------- Menu ---------- */
  var menu = document.querySelector('.menu');
  var menuTl = null;
  function openMenu() {
    if (!menu) return;
    menu.setAttribute('aria-hidden', 'false');
    if (hasGsap && !reduce) {
      menuTl = window.gsap.timeline();
      menuTl.set(menu, { visibility: 'visible' })
        .to(menu, { clipPath: 'inset(0 0 0% 0)', duration: .7, ease: 'expo.inOut' })
        .from(menu.querySelectorAll('.menu-links a span'), { yPercent: 110, duration: .7, stagger: .06, ease: 'expo.out' }, '-=.25')
        .from(menu.querySelectorAll('.menu-foot > *'), { opacity: 0, y: 10, duration: .4 }, '-=.4');
    } else {
      menu.style.visibility = 'visible'; menu.style.clipPath = 'none';
    }
    var first = menu.querySelector('.menu-links a');
    if (first) first.focus({ preventScroll: true });
  }
  function closeMenu() {
    if (!menu) return;
    menu.setAttribute('aria-hidden', 'true');
    if (hasGsap && !reduce) {
      window.gsap.to(menu, { clipPath: 'inset(0 0 100% 0)', duration: .6, ease: 'expo.inOut', onComplete: function () { menu.style.visibility = 'hidden'; } });
    } else {
      menu.style.visibility = 'hidden'; menu.style.clipPath = '';
    }
  }
  document.querySelectorAll('[data-menu-open]').forEach(function (b) { b.addEventListener('click', openMenu); });
  document.querySelectorAll('[data-menu-close]').forEach(function (b) { b.addEventListener('click', closeMenu); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && menu && menu.getAttribute('aria-hidden') === 'false') closeMenu(); });

  /* ---------- In-page anchors (work with ScrollSmoother) ---------- */
  function scrollToTarget(el) {
    if (smoother) smoother.scrollTo(el, true, 'top top');
    else el.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });
  }
  document.querySelectorAll('a[href*="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var url = new URL(a.href, location.href);
      if (url.pathname !== location.pathname || !url.hash) return;
      var target = document.querySelector(url.hash);
      if (!target) return;
      e.preventDefault();
      if (menu && menu.getAttribute('aria-hidden') === 'false') closeMenu();
      scrollToTarget(target);
      history.replaceState(null, '', url.hash);
    });
  });

  /* ---------- Back to top ---------- */
  var toTop = document.querySelector('.to-top');
  if (toTop) {
    toTop.addEventListener('click', function () {
      if (smoother) smoother.scrollTo(0, true); else window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
    });
  }
  function onScroll(y) { if (toTop) toTop.classList.toggle('show', y > 600); }

  /* ---------- Projects filter ---------- */
  var filterBtns = document.querySelectorAll('.filters button');
  function setFilter(f) {
    filterBtns.forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.filter === f ? 'true' : 'false'); });
    document.querySelectorAll('.pitem').forEach(function (it) {
      it.hidden = !(f === 'all' || (' ' + it.dataset.cat + ' ').indexOf(' ' + f + ' ') > -1);
    });
    if (window.ScrollTrigger) window.ScrollTrigger.refresh();
  }
  if (filterBtns.length) {
    filterBtns.forEach(function (b) { b.addEventListener('click', function () { setFilter(b.dataset.filter); }); });
    var qf = new URLSearchParams(location.search).get('filter');
    if (qf && document.querySelector('.filters button[data-filter="' + qf + '"]')) setFilter(qf);
  }

  /* ---------- Lightbox ---------- */
  var lb = document.querySelector('.lightbox');
  if (lb) {
    var imgs = Array.prototype.slice.call(document.querySelectorAll('[data-lightbox] img'));
    var lbImg = lb.querySelector('img');
    var idx = 0;
    var show = function (i) { idx = (i + imgs.length) % imgs.length; lbImg.src = imgs[idx].currentSrc || imgs[idx].src; lbImg.alt = imgs[idx].alt; };
    imgs.forEach(function (img, i) {
      img.parentElement.addEventListener('click', function () { show(i); lb.classList.add('open'); if (smoother) smoother.paused(true); });
    });
    var close = function () { lb.classList.remove('open'); if (smoother) smoother.paused(false); };
    lb.querySelector('.lb-close').addEventListener('click', close);
    lb.querySelector('.lb-prev').addEventListener('click', function (e) { e.stopPropagation(); show(idx - 1); });
    lb.querySelector('.lb-next').addEventListener('click', function (e) { e.stopPropagation(); show(idx + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(idx - 1);
      if (e.key === 'ArrowRight') show(idx + 1);
    });
  }

  /* ---------- Without GSAP or with reduced motion: static page ---------- */
  var loader = document.querySelector('.loader');
  if (!hasGsap || reduce) {
    if (loader) loader.remove();
    window.addEventListener('scroll', function () { onScroll(window.scrollY); }, { passive: true });
    return;
  }

  var gsap = window.gsap;
  gsap.registerPlugin(window.ScrollTrigger, window.ScrollSmoother, window.SplitText);
  var ST = window.ScrollTrigger;
  var desktop = window.matchMedia('(min-width: 1025px)').matches;

  smoother = window.ScrollSmoother.create({
    wrapper: '#smooth-wrapper', content: '#smooth-content',
    smooth: 1.1, effects: true, smoothTouch: false,
    onUpdate: function (self) { onScroll(self.scrollTop()); }
  });

  /* Loader, shorter after the first page of the session */
  var intro = gsap.timeline({ paused: true });
  function startIntro() { intro.play(); }
  if (loader) {
    var quick = session('seen') === '1';
    session('seen', '1');
    var letters = loader.querySelectorAll('.loader-word span');
    var lt = gsap.timeline({ onComplete: function () { loader.remove(); } });
    if (quick) {
      lt.set(loader.querySelector('.loader-word'), { opacity: 0 })
        .to(loader, { yPercent: -100, duration: .7, ease: 'expo.inOut', delay: .05 })
        .add(startIntro, '-=.35');
    } else {
      lt.from(letters, { yPercent: 110, duration: .7, stagger: .05, ease: 'expo.out' })
        .to(loader.querySelector('.loader-bar'), { scaleX: 1, duration: 1, ease: 'power2.inOut' }, 0)
        .to(letters, { yPercent: -110, duration: .5, stagger: .03, ease: 'expo.in' }, '+=.1')
        .to(loader, { yPercent: -100, duration: .8, ease: 'expo.inOut' }, '-=.15')
        .add(startIntro, '-=.4');
    }
  } else {
    startIntro();
  }

  /* Hero (home) */
  var heroTitle = document.querySelector('.hero-title');
  if (heroTitle) {
    var heroSplit = window.SplitText.create(heroTitle.querySelectorAll('.line'), { type: 'chars', mask: 'chars' });
    intro.from(heroSplit.chars, { yPercent: 105, duration: 1, stagger: .035, ease: 'expo.out' })
      .from(heroTitle.querySelectorAll('.arrow'), { yPercent: 105, duration: 1, ease: 'expo.out' }, '<.15')
      .from('.hero-bar', { opacity: 0, duration: .8 }, .2)
      .from('.hero-intro', { opacity: 0, y: 30, duration: 1, ease: 'expo.out' }, .5);
  }
  /* Page title (projects / detail) */
  document.querySelectorAll('[data-intro]').forEach(function (el, i) {
    var s = window.SplitText.create(el, { type: 'lines', mask: 'lines' });
    splits.push(s);
    intro.from(s.lines, { yPercent: 105, duration: 1, stagger: .08, ease: 'expo.out' }, i * .1);
  });

  /* Line reveals on scroll */
  document.querySelectorAll('[data-split]').forEach(function (el) {
    var s = window.SplitText.create(el, { type: 'lines', mask: 'lines' });
    splits.push(s);
    gsap.from(s.lines, {
      yPercent: 105, duration: 1, stagger: .07, ease: 'expo.out',
      scrollTrigger: { trigger: el, start: 'top 88%' }
    });
  });
  document.querySelectorAll('[data-reveal]').forEach(function (el) {
    gsap.from(el, { opacity: 0, y: 40, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: el, start: 'top 90%' } });
  });

  /* Image reveal, plus inner parallax when the image is taller than its box */
  document.querySelectorAll('[data-clip]').forEach(function (box) {
    gsap.from(box, { clipPath: 'inset(0 0 100% 0)', duration: 1.2, ease: 'expo.inOut', scrollTrigger: { trigger: box, start: 'top 92%' } });
  });
  document.querySelectorAll('[data-parallax]').forEach(function (box) {
    var img = box.querySelector('img');
    gsap.from(box, { clipPath: 'inset(0 0 100% 0)', duration: 1.2, ease: 'expo.inOut', scrollTrigger: { trigger: box, start: 'top 90%' } });
    if (img) {
      gsap.fromTo(img, { yPercent: -8 }, { yPercent: 0, ease: 'none', scrollTrigger: { trigger: box, start: 'top bottom', end: 'bottom top', scrub: true } });
    }
  });

  /* Services stack (desktop) */
  if (desktop) {
    var rows = gsap.utils.toArray('.svc-row');
    rows.forEach(function (row, i) {
      if (i === rows.length - 1) return;
      ST.create({ trigger: row, start: 'top top', endTrigger: rows[rows.length - 1], end: 'top top', pin: true, pinSpacing: false });
      gsap.to(row.children, {
        opacity: .25, ease: 'none',
        scrollTrigger: { trigger: rows[i + 1], start: 'top bottom', end: 'top top', scrub: true }
      });
    });
  }

  /* Big type sliding with scroll */
  document.querySelectorAll('.big-type .track').forEach(function (track) {
    gsap.to(track, {
      x: function () { return -(track.scrollWidth - window.innerWidth * .55); }, ease: 'none',
      scrollTrigger: { trigger: track.parentElement, start: 'top 80%', end: 'bottom top', scrub: true, invalidateOnRefresh: true }
    });
  });

  /* Footer marquee */
  document.querySelectorAll('.marquee').forEach(function (m) {
    var inner = m.querySelector('.marquee-inner');
    m.appendChild(inner.cloneNode(true)).setAttribute('aria-hidden', 'true');
    var parts = m.querySelectorAll('.marquee-inner');
    var loop = gsap.to(parts, { xPercent: -100, duration: 22, ease: 'none', repeat: -1 });
    ST.create({
      trigger: m, start: 'top bottom', end: 'bottom top',
      onUpdate: function (self) { gsap.to(loop, { timeScale: self.direction === 1 ? 1 : -1, duration: .4, overwrite: true }); }
    });
  });

  /* Jump to hash after load */
  if (location.hash) {
    var t = document.querySelector(location.hash);
    if (t) window.addEventListener('load', function () { setTimeout(function () { smoother.scrollTo(t, false, 'top top'); }, 50); });
  }
  window.addEventListener('load', function () { ST.refresh(); });
})();
