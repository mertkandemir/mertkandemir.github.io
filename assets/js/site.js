/* mkandemir.com.tr — interactions */
(() => {
  const root = document.documentElement;
  const body = document.body;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(pointer: fine)').matches;

  // intro
  requestAnimationFrame(() => requestAnimationFrame(() => body.classList.add('loaded')));

  // year
  document.querySelectorAll('[data-year]').forEach(el => el.textContent = new Date().getFullYear());

  // remember language choice
  document.querySelectorAll('[data-lang]').forEach(a => a.addEventListener('click', () => {
    try { localStorage.setItem('mk-language', a.dataset.lang); } catch (e) {}
  }));

  // mobile menu
  const menuBtn = document.querySelector('.menu-btn');
  const menu = document.getElementById('mobile-menu');
  const behind = document.querySelectorAll('main, footer, .header .brand, .header .lang');
  const setMenu = open => {
    if (!menuBtn || open === body.classList.contains('menu-open')) return;
    body.classList.toggle('menu-open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.setAttribute('aria-label', open ? menuBtn.dataset.close || 'Close menu' : menuBtn.dataset.open || 'Open menu');
    behind.forEach(el => open ? el.setAttribute('inert', '') : el.removeAttribute('inert'));
    if (menu) {
      open ? menu.removeAttribute('inert') : menu.setAttribute('inert', '');
      if (open) { const first = menu.querySelector('a'); first && setTimeout(() => first.focus({ preventScroll: true }), 80); }
      else menuBtn.focus({ preventScroll: true });
    }
  };
  menu && menu.setAttribute('inert', '');
  menuBtn && menuBtn.addEventListener('click', () => setMenu(!body.classList.contains('menu-open')));
  menu && menu.addEventListener('keydown', e => { // keep focus inside the open menu
    if (e.key !== 'Tab') return;
    const items = [...menu.querySelectorAll('a'), menuBtn];
    const i = items.indexOf(document.activeElement);
    if (e.shiftKey && i <= 0) { e.preventDefault(); menuBtn.focus(); }
    else if (!e.shiftKey && i === items.length - 2) { e.preventDefault(); menuBtn.focus(); }
  });
  document.querySelectorAll('.mobile-menu a').forEach(a => a.addEventListener('click', () => setMenu(false)));
  addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); });
  addEventListener('resize', () => { if (innerWidth > 900) setMenu(false); }, { passive: true });

  // reveal on scroll
  const revealEls = document.querySelectorAll('[data-reveal], .case-hero, .product');
  if ('IntersectionObserver' in window && !reduce) {
    const io = new IntersectionObserver(entries => entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    }), { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    revealEls.forEach(el => io.observe(el));
  } else revealEls.forEach(el => el.classList.add('in'));

  // count-up
  const counters = document.querySelectorAll('[data-count]');
  const runCount = el => {
    const to = +el.dataset.count, dur = 1600, t0 = performance.now();
    const tick = t => {
      const k = Math.min(1, (t - t0) / dur), v = Math.round(to * (1 - Math.pow(1 - k, 4)));
      el.textContent = v;
      if (k < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  if ('IntersectionObserver' in window && !reduce) {
    const co = new IntersectionObserver(entries => entries.forEach(e => {
      if (e.isIntersecting) { runCount(e.target); co.unobserve(e.target); }
    }), { threshold: 0.6 });
    counters.forEach(el => { el.textContent = '0'; co.observe(el); });
  }

  // scroll-driven: header, progress, parallax, timeline, active nav
  const header = document.querySelector('.header');
  const progress = document.querySelector('.progress');
  const parallax = document.querySelector('.case-hero img');
  const timeline = document.querySelector('.timeline');
  const jobs = timeline ? [...timeline.querySelectorAll('.job')] : [];
  const navLinks = [...document.querySelectorAll('.nav a[href^="#"]')];
  const sections = navLinks.map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
  let ticking = false;
  const onScroll = () => {
    const y = scrollY, vh = innerHeight;
    header && header.classList.toggle('scrolled', y > 24);
    const max = root.scrollHeight - vh;
    progress && progress.style.setProperty('--p', max > 0 ? (y / max).toFixed(4) : 0);
    if (parallax && !reduce) {
      const r = parallax.parentElement.getBoundingClientRect();
      if (r.bottom > 0 && r.top < vh) {
        const k = (r.top + r.height / 2 - vh / 2) / vh;
        parallax.style.setProperty('--py', (k * -60).toFixed(1) + 'px');
      }
    }
    if (timeline) {
      const r = timeline.getBoundingClientRect();
      const p = Math.max(0, Math.min(1, (vh * 0.62 - r.top) / r.height));
      timeline.style.setProperty('--tp', reduce ? 1 : p.toFixed(4));
      jobs.forEach(j => j.classList.toggle('lit', reduce || j.getBoundingClientRect().top < vh * 0.62));
    }
    let current = null;
    sections.forEach((s, i) => { if (s.getBoundingClientRect().top < vh * 0.4) current = navLinks[i]; });
    navLinks.forEach(a => a.classList.toggle('active', a === current));
    ticking = false;
  };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  addEventListener('resize', onScroll, { passive: true });
  onScroll();

  // pointer effects (desktop only)
  if (fine && !reduce) {
    const spot = document.querySelector('.spot');
    addEventListener('pointermove', e => {
      spot && (spot.style.setProperty('--sx', e.clientX + 'px'), spot.style.setProperty('--sy', e.clientY + 'px'));
    }, { passive: true });
    document.querySelectorAll('.card').forEach(c => c.addEventListener('pointermove', e => {
      const r = c.getBoundingClientRect();
      c.style.setProperty('--mx', e.clientX - r.left + 'px');
      c.style.setProperty('--my', e.clientY - r.top + 'px');
    }));
    document.querySelectorAll('[data-magnetic]').forEach(b => {
      b.addEventListener('pointermove', e => {
        const r = b.getBoundingClientRect();
        b.style.transform = `translate(${(e.clientX - r.left - r.width / 2) * 0.18}px, ${(e.clientY - r.top - r.height / 2) * 0.28}px)`;
      });
      b.addEventListener('pointerleave', () => { b.style.transform = ''; });
    });
  }

  // copy e-mail
  document.querySelectorAll('[data-copy]').forEach(btn => btn.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(btn.dataset.copy);
      const label = btn.dataset.label || (btn.dataset.label = btn.textContent);
      btn.textContent = btn.dataset.done || label; btn.classList.add('done');
      setTimeout(() => { btn.textContent = label; btn.classList.remove('done'); }, 1800);
    } catch (e) { location.href = 'mailto:' + btn.dataset.copy; }
  }));

  // work-order simulation (illustrative)
  const wo = document.querySelector('[data-wo]');
  if (wo) {
    const ops = [...wo.querySelectorAll('.op')];
    const chip = wo.querySelector('[data-wo-status]');
    const qty = wo.querySelector('[data-wo-qty]');
    const scrap = wo.querySelector('[data-wo-scrap]');
    const tr = root.lang === 'tr';
    const labels = JSON.parse(wo.dataset.labels);
    const target = +qty.dataset.target;
    const setStatus = (i, cls) => { chip.className = 'chip ' + cls; chip.lastChild.textContent = labels[i]; };
    const paint = p => { // p: 0..ops.length
      ops.forEach((op, i) => {
        const v = Math.max(0, Math.min(1, p - i));
        op.querySelector('.bar').style.setProperty('--v', v.toFixed(3));
        op.querySelector('.pct').textContent = Math.round(v * 100) + '%';
        op.classList.toggle('done', v >= 1);
      });
      qty.textContent = Math.round(target * p / ops.length);
      const sv = (1.2 - 0.6 * (p / ops.length)).toFixed(1);
      scrap.textContent = tr ? '%' + sv.replace('.', ',') : sv + '%';
    };
    if (reduce) { paint(ops.length); setStatus(3, 'ok'); }
    else {
      let p = 0, phase = 0, hold = 0, last = performance.now();
      setStatus(0, '');
      const loop = t => {
        const dt = Math.min(64, t - last); last = t;
        if (phase === 0) { hold += dt; if (hold > 900) { phase = 1; hold = 0; setStatus(1, ''); } }
        else if (phase === 1) { hold += dt; if (hold > 700) { phase = 2; hold = 0; setStatus(2, 'run'); } }
        else if (phase === 2) { p += dt / 1500; if (p >= ops.length) { p = ops.length; phase = 3; setStatus(3, 'ok'); } }
        else { hold += dt; if (hold > 2600) { p = 0; phase = 0; hold = 0; setStatus(0, ''); } }
        paint(p);
        requestAnimationFrame(loop);
      };
      requestAnimationFrame(loop);
    }
  }
})();
