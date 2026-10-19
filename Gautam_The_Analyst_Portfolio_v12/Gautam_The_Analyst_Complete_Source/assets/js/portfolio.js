/* Gautam The Analyst — 2026 portfolio patterns (kinetic type, magnetic buttons, scroll-spy, marquee, case stack, view toggle) */
(() => {
  'use strict';
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));

  /* kinetic headlines: words rise out of a mask */
  let wi = 0;
  const split = (node, inAccent) => {
    Array.from(node.childNodes).forEach(n => {
      if (n.nodeType === 3) {
        const frag = document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(part => {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.append(' '); return; }
          const w = document.createElement('span'); w.className = 'kw' + (inAccent ? ' acc' : ''); w.style.setProperty('--w', Math.min(wi++, 14));
          const i = document.createElement('i'); i.textContent = part; w.append(i); frag.append(w);
        });
        n.replaceWith(frag);
      } else if (n.nodeType === 1 && !n.classList.contains('kw')) split(n, inAccent || n.classList.contains('accent'));
    });
  };
  if (!reduce) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('go'); io.unobserve(e.target); } }), { threshold: .3 });
    $$('main h1, main h2').forEach(h => {
      if (h.closest('.bt-stat')) return;
      wi = 0; const label = h.textContent.trim().replace(/\s+/g, ' ');
      split(h, false); h.setAttribute('aria-label', label); $$('.kw', h).forEach(k => k.setAttribute('aria-hidden', 'true'));
      h.classList.add('kinetic'); io.observe(h);
    });
  }

  /* magnetic primary buttons */
  if (fine && !reduce) $$('.btn-primary').forEach(b => {
    b.addEventListener('pointermove', e => { const r = b.getBoundingClientRect(); b.style.setProperty('--tx', ((e.clientX - r.left - r.width / 2) * .22).toFixed(1) + 'px'); b.style.setProperty('--ty', ((e.clientY - r.top - r.height / 2) * .3).toFixed(1) + 'px'); });
    b.addEventListener('pointerleave', () => { b.style.setProperty('--tx', '0px'); b.style.setProperty('--ty', '0px'); });
  });

  /* scroll-spy dots (home) */
  if ($('main#home')) {
    const map = [['home', 'Intro'], ['proof', 'Proof'], ['services', 'Services'], ['lifecycle', 'Process'], ['toolkit', 'Toolkit'], ['projects', 'Work'], ['ba-samples', 'Samples'], ['about', 'About'], ['contact', 'Contact']].filter(([id]) => $('#' + id));
    const nav = document.createElement('nav'); nav.className = 'dots'; nav.setAttribute('aria-label', 'Page sections');
    nav.innerHTML = map.map(([id, l]) => `<a href="#${id}" aria-label="${l}"><span>${l}</span></a>`).join(''); document.body.append(nav);
    const links = $$('a', nav);
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) links.forEach(a => a.classList.toggle('on', a.getAttribute('href') === '#' + e.target.id)); }), { rootMargin: '-45% 0px -50% 0px' });
    map.forEach(([id]) => io.observe($('#' + id)));
  }

  /* giant scroll-linked marquee above the footer */
  const page = (location.pathname.split('/').pop() || 'index').replace('.html', '') || 'index';
  const words = { index: ['REQUIREMENTS', 'DATA', 'API FLOWS', 'UAT', 'HANDOVER'], about: ['CLEAR SCOPE', 'EVIDENCE', 'TRACEABLE', 'PLAIN LANGUAGE'], services: ['DISCOVER', 'DEFINE', 'VALIDATE', 'HAND OVER'], projects: ['SQL', 'POWER BI', 'ETL', 'RAG', 'FORECASTING'], resume: ['BRD/FRD', 'BDD', 'RTM', 'AGILE', 'UAT'], contact: ["LET'S TALK", 'SCOPE IT', 'SHIP IT'] }[page];
  const footer = $('.site-footer');
  if (words && footer) {
    const mq = document.createElement('div'); mq.className = 'mq'; mq.setAttribute('aria-hidden', 'true');
    const row = (cls) => `<div class="mq-row ${cls}">${[...words, ...words, ...words].map((w, i) => (i % 2 ? `<b>${w}</b>` : `<span>${w}</span>`) + '<i>✦</i>').join('')}</div>`;
    mq.innerHTML = row('a') + row('b'); footer.before(mq);
    const [a, b] = $$('.mq-row', mq);
    if (!reduce) {
      let t = false; const upd = () => { t = false; const r = mq.getBoundingClientRect(), p = (innerHeight - r.top); a.style.transform = `translateX(${-p * .35 - 200}px)`; b.style.transform = `translateX(${p * .35 - 1800}px)`; };
      addEventListener('scroll', () => { if (!t) { t = true; requestAnimationFrame(upd); } }, { passive: true }); upd();
    }
  }

  /* process line fill + sticky case-stack depth */
  const dark = $$('.section-dark .process-grid');
  const cases = $$('.case');
  const onScroll = () => {
    dark.forEach(g => { const r = g.getBoundingClientRect(); g.style.setProperty('--p', clamp((innerHeight * .6 - r.top) / r.height, 0, 1).toFixed(3)); });
    if (!reduce && innerWidth > 760) cases.forEach((c, i) => {
      const n = cases[i + 1]; if (!n) return;
      const top = parseFloat(getComputedStyle(c).top) || 100, gap = n.getBoundingClientRect().top - top, p = clamp(1 - gap / c.offsetHeight, 0, 1);
      c.style.transform = `scale(${(1 - p * .06).toFixed(4)})`; c.style.filter = `brightness(${(1 - p * .4).toFixed(3)})`;
    });
  };
  let tk = false; addEventListener('scroll', () => { if (!tk) { tk = true; requestAnimationFrame(() => { tk = false; onScroll(); }); } }, { passive: true }); onScroll();

  /* projects: grid / list */
  const grid = $('.project-grid');
  $$('.vt').forEach(b => b.addEventListener('click', () => { $$('.vt').forEach(x => x.setAttribute('aria-pressed', String(x === b))); grid?.classList.toggle('list', b.dataset.view === 'list'); }));
})();
