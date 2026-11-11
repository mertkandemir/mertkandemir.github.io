/* mkandemir.com.tr */
(() => {
  const body = document.body;
  requestAnimationFrame(() => requestAnimationFrame(() => body.classList.add('ready')));

  // e-mail is assembled at runtime so scrapers don't find it in the HTML
  document.querySelectorAll('[data-mail]').forEach(el => {
    const addr = el.dataset.mail.replace('|', '@');
    el.href = 'mailto:' + addr;
    const t = el.querySelector('[data-mail-text]');
    if (t) t.textContent = addr;
  });

  // local time in İzmir
  const clock = document.querySelector('[data-clock]');
  if (clock) {
    const fmt = new Intl.DateTimeFormat(document.documentElement.lang === 'tr' ? 'tr-TR' : 'en-GB',
      { timeZone: 'Europe/Istanbul', hour: '2-digit', minute: '2-digit' });
    const tick = () => { clock.textContent = fmt.format(new Date()); };
    tick(); setInterval(tick, 15000);
  }

  // glossary search
  const input = document.querySelector('[data-search]');
  if (input) {
    const terms = [...document.querySelectorAll('.term')];
    const letters = [...document.querySelectorAll('.letter')];
    const empty = document.querySelector('.empty');
    const count = document.querySelector('[data-count]');
    const norm = s => s.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i');
    const index = terms.map(t => norm(t.textContent));
    const run = () => {
      const q = norm(input.value.trim());
      let shown = 0;
      terms.forEach((t, i) => { const ok = !q || index[i].includes(q); t.hidden = !ok; if (ok) shown++; });
      letters.forEach(l => {
        let n = l.nextElementSibling, any = false;
        while (n && !n.classList.contains('letter')) { if (n.classList.contains('term') && !n.hidden) any = true; n = n.nextElementSibling; }
        l.hidden = !any;
      });
      if (empty) empty.style.display = shown ? 'none' : 'block';
      if (count) count.textContent = shown;
    };
    input.addEventListener('input', run);
    const q = new URLSearchParams(location.search).get('q');
    if (q) { input.value = q; run(); }
    addEventListener('keydown', e => {
      if (e.key === '/' && document.activeElement !== input) { e.preventDefault(); input.focus(); }
      if (e.key === 'Escape' && document.activeElement === input) { input.value = ''; run(); }
    });
  }
})();
