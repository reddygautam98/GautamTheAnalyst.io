/* Gautam The Analyst — site behaviour (theme, nav, motion, filters, command palette, form) */
(() => {
  'use strict';
  const SCRIPT_SRC = document.currentScript && document.currentScript.src;
  const root = document.documentElement;
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  root.classList.add('js');

  /* ---------- theme (single source of truth; dark by default) ---------- */
  const themeButton = $('#theme-toggle');
  const themeMeta = $('meta[name="theme-color"]');
  const readTheme = () => { try { return localStorage.getItem('gta-theme'); } catch (_) { return null; } };
  const paintTheme = theme => {
    const dark = theme !== 'light';
    root.dataset.theme = dark ? 'dark' : 'light';
    if (themeMeta) themeMeta.setAttribute('content', dark ? '#05070d' : '#f3f6fc');
    if (themeButton) {
      const label = `Switch to ${dark ? 'light' : 'dark'} theme`;
      themeButton.setAttribute('aria-pressed', String(dark));
      themeButton.setAttribute('aria-label', label);
      themeButton.setAttribute('title', label);
      const icon = $('.theme-toggle-icon', themeButton);
      const text = $('.theme-toggle-label', themeButton);
      if (icon) icon.textContent = dark ? '☀' : '☾';
      if (text) text.textContent = dark ? 'Light' : 'Dark';
    }
    window.dispatchEvent(new Event('gta-theme'));
  };
  const setTheme = (theme, persist) => { paintTheme(theme); if (persist) { try { localStorage.setItem('gta-theme', theme); } catch (_) {} } };
  const toggleTheme = () => setTheme(root.dataset.theme === 'light' ? 'dark' : 'light', true);
  paintTheme(readTheme() || root.dataset.theme || 'dark');
  themeButton?.addEventListener('click', toggleTheme);

  /* ---------- ambient background ---------- */
  const fx = document.createElement('div');
  fx.className = 'bg-fx'; fx.setAttribute('aria-hidden', 'true');
  fx.innerHTML = '<div class="aurora"></div><div class="grid"></div><canvas></canvas><div class="noise"></div>';
  document.body.prepend(fx);
  const progress = document.createElement('div');
  progress.className = 'scroll-progress'; progress.setAttribute('aria-hidden', 'true');
  document.body.prepend(progress);

  // Network-of-nodes canvas: a nod to data lineage / system integration.
  (function network() {
    const canvas = $('canvas', fx);
    if (!canvas || reduceMotion || root.classList.contains('gl-pending')) return;
    const ctx = canvas.getContext('2d');
    let w = 0, h = 0, dpr = 1, nodes = [], raf = 0, mouse = { x: -999, y: -999 }, rgb = '56,225,255';
    const resize = () => {
      dpr = Math.min(window.devicePixelRatio || 1, 1.5);
      w = canvas.clientWidth; h = canvas.clientHeight;
      canvas.width = w * dpr; canvas.height = h * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const count = Math.max(24, Math.min(70, Math.round(w / 24)));
      nodes = Array.from({ length: count }, () => ({ x: Math.random() * w, y: Math.random() * h, vx: (Math.random() - .5) * .28, vy: (Math.random() - .5) * .28, r: Math.random() * 1.4 + .7 }));
    };
    const color = () => { rgb = root.dataset.theme === 'light' ? '8,110,150' : '56,225,255'; };
    const frame = () => {
      window.__f = !window.__f; if (window.__v5s || window.__f) { raf = requestAnimationFrame(frame); return; }
      ctx.clearRect(0, 0, w, h);
      for (const n of nodes) {
        n.x += n.vx; n.y += n.vy;
        if (n.x < 0 || n.x > w) n.vx *= -1;
        if (n.y < 0 || n.y > h) n.vy *= -1;
        const dx = n.x - mouse.x, dy = n.y - mouse.y, d = Math.hypot(dx, dy);
        if (d < 120) { n.x += dx / d * .6; n.y += dy / d * .6; }
      }
      for (let i = 0; i < nodes.length; i++) {
        const a = nodes[i];
        ctx.fillStyle = `rgba(${rgb},.75)`; ctx.beginPath(); ctx.arc(a.x, a.y, a.r, 0, 6.283); ctx.fill();
        for (let j = i + 1; j < nodes.length; j++) {
          const b = nodes[j], d = Math.hypot(a.x - b.x, a.y - b.y);
          if (d < 140) { ctx.strokeStyle = `rgba(${rgb},${(1 - d / 140) * .35})`; ctx.lineWidth = .7; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke(); }
        }
      }
      raf = requestAnimationFrame(frame);
    };
    const start = () => { if (!raf) raf = requestAnimationFrame(frame); };
    const stop = () => { cancelAnimationFrame(raf); raf = 0; };
    resize(); color(); start();
    window.addEventListener('resize', resize, { passive: true });
    window.addEventListener('gta-theme', color);
    window.addEventListener('pointermove', e => { mouse = { x: e.clientX, y: e.clientY }; }, { passive: true });
    document.addEventListener('visibilitychange', () => (document.hidden ? stop() : start()));
  })();

  /* cursor glow (desktop only) */
  if (finePointer && !reduceMotion) {
    const glow = document.createElement('div');
    glow.className = 'cursor-glow'; glow.setAttribute('aria-hidden', 'true');
    document.body.append(glow);
    window.addEventListener('pointermove', e => {
      glow.style.setProperty('--cx', e.clientX + 'px'); glow.style.setProperty('--cy', e.clientY + 'px'); glow.classList.add('on');
    }, { passive: true });
    document.addEventListener('pointerleave', () => glow.classList.remove('on'));
  }

  /* ---------- header, progress, mobile menu ---------- */
  const header = $('.site-header');
  let ticking = false;
  const onScroll = () => {
    if (ticking) return; ticking = true;
    requestAnimationFrame(() => {
      const max = document.documentElement.scrollHeight - innerHeight;
      progress.style.transform = `scaleX(${max > 0 ? Math.min(1, scrollY / max) : 0})`;
      header?.classList.toggle('scrolled', scrollY > 12);
      ticking = false;
    });
  };
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // group the nav tools (palette + theme) next to the CTA
  const nav = $('.nav-links');
  const menuButton = $('.menu-toggle');
  if (nav && themeButton) {
    const cmd = document.createElement('button');
    cmd.type = 'button'; cmd.className = 'cmd-btn'; cmd.setAttribute('aria-haspopup', 'dialog');
    cmd.innerHTML = '<span aria-hidden="true">⌘</span><kbd>Ctrl K</kbd>';
    cmd.setAttribute('aria-label', 'Open quick navigation (Ctrl or Command + K)');
    const tools = document.createElement('div');
    tools.className = 'nav-tools';
    tools.append(cmd, themeButton);
    nav.after(tools);
    cmd.addEventListener('click', () => openPalette());
  }
  const closeMenu = () => { nav?.classList.remove('open'); menuButton?.setAttribute('aria-expanded', 'false'); if (menuButton) menuButton.textContent = 'Menu ☰'; };
  menuButton?.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.textContent = open ? 'Close ✕' : 'Menu ☰';
  });
  nav?.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMenu));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });

  /* ---------- reveal on scroll ---------- */
  const revealSel = '.wrap > *, .card, .section-heading, .hero-grid > *, .subpage-hero .container > *, .benefit, .metric, .service-card, .project-card, .process-step, .scope-item, .sample-feature-card, .detail-card, .skill-group, .career-entry, .principle, .contact-method, .contact-form, .faq-list details, .callout, .page-banner, .lifecycle, .about-visual, .about-copy, .center-cta, .proof-item, .terminal, .scope-copy';
  const revealEls = $$(revealSel);
  revealEls.forEach(el => {
    el.setAttribute('data-reveal', '');
    const siblings = el.parentElement ? Array.from(el.parentElement.children).filter(c => c.hasAttribute('data-reveal')) : [];
    el.style.setProperty('--d', Math.min(siblings.indexOf(el), 6) * 70 + 'ms');
  });
  if ('IntersectionObserver' in window && !reduceMotion) {
    const io = new IntersectionObserver(entries => entries.forEach(en => { if (en.isIntersecting) { const el = en.target; el.classList.add('in'); io.unobserve(el); setTimeout(() => { el.removeAttribute('data-reveal'); el.style.removeProperty('--d'); el.classList.remove('in'); }, 1100); } }), { threshold: .12, rootMargin: '0px 0px -6% 0px' });
    revealEls.forEach(el => io.observe(el));
  } else revealEls.forEach(el => el.classList.add('in'));

  /* ---------- spotlight cards ---------- */
  const spotSel = '.card, .service-card, .project-card, .detail-card, .skill-group, .sample-feature-card, .contact-method, .process-step, .career-entry, .scope-item, .principle, .benefit, .metric, .callout, .page-banner, .contact-form';
  $$(spotSel).forEach(card => {
    card.classList.add('spot');
    const g = document.createElement('span'); g.className = 'spot-glow'; g.setAttribute('aria-hidden', 'true'); card.prepend(g);
  });
  document.addEventListener('pointermove', e => {
    const card = e.target.closest?.('.spot'); if (!card) return;
    const r = card.getBoundingClientRect();
    card.style.setProperty('--mx', e.clientX - r.left + 'px'); card.style.setProperty('--my', e.clientY - r.top + 'px');
  }, { passive: true });

  /* hero 3D tilt */
  const frame = $('.art-frame');
  if (frame && finePointer && !reduceMotion && !root.classList.contains('gl-pending')) {
    const art = frame.closest('.hero-art');
    art.addEventListener('pointermove', e => {
      const r = art.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      frame.style.transform = `rotateY(${x * 14}deg) rotateX(${-y * 14}deg)`;
    });
    art.addEventListener('pointerleave', () => { frame.style.transform = ''; });
  }

  /* ---------- count-up metrics ---------- */
  $$('.metric strong').forEach(el => {
    const m = el.textContent.trim().match(/^(\d+)(.*)$/);
    if (!m || reduceMotion) return;
    const target = +m[1], suffix = m[2];
    el.setAttribute('aria-label', el.textContent.trim());
    const io = new IntersectionObserver(([en]) => {
      if (!en.isIntersecting) return; io.disconnect();
      el.textContent = '0' + suffix; const t0 = performance.now(), dur = 1400;
      const tick = t => { const p = Math.min(1, (t - t0) / dur); el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))) + suffix; if (p < 1) requestAnimationFrame(tick); };
      requestAnimationFrame(tick);
    }, { threshold: .6 });
    io.observe(el);
  });

  /* ---------- typed role line ---------- */
  const typed = $('.typed');
  if (typed) {
    const words = (typed.dataset.words || '').split('|').filter(Boolean);
    if (reduceMotion || !words.length) typed.textContent = words[0] || '';
    else {
      let wi = 0, ci = 0, del = false;
      const step = () => {
        const word = words[wi];
        ci += del ? -1 : 1; typed.textContent = word.slice(0, ci);
        let wait = del ? 28 : 62;
        if (!del && ci === word.length) { del = true; wait = 1500; }
        else if (del && ci === 0) { del = false; wi = (wi + 1) % words.length; wait = 350; }
        setTimeout(step, wait);
      };
      step();
    }
  }

  /* ---------- ticker: duplicate for a seamless loop ---------- */
  $$('.ticker-track').forEach(track => {
    if (reduceMotion) return;
    Array.from(track.children).forEach(c => { const k = c.cloneNode(true); k.setAttribute('aria-hidden', 'true'); track.append(k); });
  });

  /* ---------- lifecycle explorer ---------- */
  const lc = $('.lifecycle');
  if (lc) {
    const tabs = $$('.lc-tab', lc), panels = $$('.lc-panel', lc);
    const select = i => { tabs.forEach((t, k) => { t.setAttribute('aria-selected', String(k === i)); t.tabIndex = k === i ? 0 : -1; }); panels.forEach((p, k) => { p.hidden = k !== i; }); };
    tabs.forEach((t, i) => {
      t.addEventListener('click', () => select(i));
      t.addEventListener('keydown', e => {
        const dir = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key]; if (!dir) return;
        e.preventDefault(); const n = (i + dir + tabs.length) % tabs.length; select(n); tabs[n].focus();
      });
    });
    select(0);
  }
  // Traceability demo — values mirror samples/specs/requirements_traceability.csv (fictional PayTrack sample).
  const trace = $('#trace-demo');
  if (trace) {
    const data = {
      'BR-01': { fr: 'FR-002; FR-004', us: 'US-01; US-03', tc: 'TC-001; TC-002', s: 'Single operational view' },
      'BR-02': { fr: 'FR-005; FR-006; FR-007', us: 'US-03; US-04', tc: 'TC-003; TC-004; TC-005', s: 'Identify unmatched/inconsistent records and reasons' },
      'BR-03': { fr: 'FR-008; FR-009; FR-010; FR-011', us: 'US-05; US-06; US-07', tc: 'TC-006; TC-007; TC-008', s: 'Assign, comment on and resolve cases' }
    };
    const out = $('#trace-out'), chips = $$('.trace-chip', trace);
    const show = id => {
      chips.forEach(c => c.setAttribute('aria-pressed', String(c.dataset.id === id)));
      const d = data[id];
      out.innerHTML = `<span class="d">$</span> <span class="p">trace</span> <span class="c">${id}</span> <span class="d">--downstream</span>\n<span class="d">#</span> ${d.s}\n<span class="v">business</span>   → <span class="c">${id}</span>\n<span class="v">functional</span> → ${d.fr}\n<span class="v">stories</span>    → ${d.us}\n<span class="v">tests</span>      → <span class="o">${d.tc}</span> <span class="d">(status: Not Run)</span>`;
    };
    chips.forEach(c => c.addEventListener('click', () => show(c.dataset.id)));
    show('BR-01');
  }

  /* broken remote preview images degrade to a styled placeholder */
  $$('.project-thumb img').forEach(img => {
    const bad = () => { img.closest('.project-thumb')?.classList.add('broken'); img.remove(); };
    if (img.complete && img.naturalWidth === 0) bad(); else img.addEventListener('error', bad, { once: true });
  });

  /* ---------- project filters + search ---------- */
  const cardsAll = $$('.project-card[data-category]');
  if (cardsAll.length) {
    let filter = 'all', query = '';
    const count = $('.project-count');
    const apply = () => {
      let shown = 0;
      cardsAll.forEach(card => {
        const okCat = filter === 'all' || card.dataset.category === filter;
        const okQ = !query || card.textContent.toLowerCase().includes(query);
        card.classList.toggle('hidden', !(okCat && okQ)); if (okCat && okQ) shown++;
      });
      if (count) count.textContent = `// showing ${shown} of ${cardsAll.length} projects`;
    };
    $$('[data-filter]').forEach(btn => btn.addEventListener('click', () => {
      filter = btn.dataset.filter;
      $$('[data-filter]').forEach(b => b.setAttribute('aria-pressed', String(b === btn)));
      apply();
    }));
    $('#project-search')?.addEventListener('input', e => { query = e.target.value.trim().toLowerCase(); apply(); });
    apply();
  }

  /* ---------- contact: service preselect, form, copy buttons ---------- */
  const serviceSelect = $('#service');
  if (serviceSelect) {
    const queryService = new URLSearchParams(location.search).get('service');
    const options = Array.from(serviceSelect.options);
    if (queryService) {
      const norm = queryService.toLowerCase().replace(/\+/g, ' ').trim();
      const match = options.find(o => o.textContent.toLowerCase() === norm) || options.find(o => o.textContent.toLowerCase().includes(norm) || norm.includes(o.textContent.toLowerCase()));
      if (match) serviceSelect.value = match.value || match.textContent;
    }
    $$('.service-select').forEach(link => link.addEventListener('click', () => {
      const match = options.find(o => o.textContent.toLowerCase() === String(link.dataset.service || '').toLowerCase());
      if (match) serviceSelect.value = match.value || match.textContent;
    }));
  }
  const details = $('#project-details');
  if (details) {
    const counter = document.createElement('div'); counter.className = 'char-count'; details.after(counter);
    const upd = () => { counter.textContent = `${details.value.length} / ${details.maxLength} chars · min 30`; };
    details.addEventListener('input', upd); upd();
  }
  const form = $('#project-enquiry'), status = $('#form-status');
  form?.addEventListener('submit', event => {
    event.preventDefault();
    if (status) status.textContent = '';
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const g = k => String(data.get(k) || '').trim();
    if (g('details').length < 30) { if (status) status.textContent = 'Please describe the problem and desired outcome in at least 30 characters.'; $('#project-details')?.focus(); return; }
    const reference = g('reference');
    if (reference) {
      try { const u = new URL(reference); if (!['http:', 'https:'].includes(u.protocol)) throw new Error('bad'); }
      catch (_) { if (status) status.textContent = 'Please enter a complete http:// or https:// reference URL, or leave that field blank.'; $('#reference')?.focus(); return; }
    }
    const lines = ['Hello Gautam,', '', 'I would like to discuss a project enquiry.', '', 'CONTACT DETAILS', `Name: ${g('name')}`, `Email: ${g('email')}`, `Company: ${g('company') || 'Not provided'}`, '', 'PROJECT DETAILS', `Service: ${g('service')}`, `Engagement type: ${g('engagement') || 'Not sure yet'}`, `Target timeline: ${g('timeline') || 'Flexible / to discuss'}`, '', 'Problem and desired outcome:', g('details'), `Reference link: ${reference || 'Not provided'}`, '', 'Please let me know the best next step.', '', 'Thank you.'];
    if (status) status.textContent = 'Opening your email application with a prepared draft. Review it and press Send to contact Gautam.';
    location.href = `mailto:reddygautam98@gmail.com?subject=${encodeURIComponent('Project enquiry — ' + g('service'))}&body=${encodeURIComponent(lines.join('\n'))}`;
  });
  $$('.contact-method[href^="mailto:"], .contact-method[href^="tel:"]').forEach(a => {
    const btn = document.createElement('button');
    btn.type = 'button'; btn.className = 'copy-btn'; btn.textContent = 'copy';
    btn.setAttribute('aria-label', 'Copy ' + a.href.split(':')[0] + ' value');
    btn.addEventListener('click', async e => {
      e.preventDefault(); e.stopPropagation();
      const value = decodeURIComponent(a.getAttribute('href').replace(/^(mailto|tel):/, '').split('?')[0]);
      try { await navigator.clipboard.writeText(value); btn.textContent = 'copied ✓'; } catch (_) { btn.textContent = 'press Ctrl+C'; }
      setTimeout(() => { btn.textContent = 'copy'; }, 1600);
    });
    a.append(btn);
  });

  document.querySelectorAll('#year').forEach(n => { n.textContent = String(new Date().getFullYear()); });

  /* ---------- command palette (Ctrl/⌘ + K, or "/") ---------- */
  let palette;
  const base = location.pathname.includes('/samples/') ? '../' : '';
  const rawItems = [
    ['⌂', 'Home', 'index.html', 'g h'], ['◈', 'Services', 'services.html', 'g s'], ['▦', 'Projects', 'projects.html', 'g p'],
    ['❖', 'BA Samples gallery', 'samples/index.html', ''], ['◎', 'About', 'about.html', 'g a'], ['▤', 'Resume', 'resume.html', 'g r'], ['✉', 'Contact / project enquiry', 'contact.html#project-enquiry', 'g c'],
    ['↗', 'GitHub — reddygautam98', 'https://github.com/reddygautam98', ''], ['in', 'LinkedIn', 'https://www.linkedin.com/in/gautam-reddy-analyst', ''],
    ['@', 'Email Gautam', 'mailto:reddygautam98@gmail.com', ''], ['◐', 'Toggle light / dark theme', '#theme', 't']
  ];
  const items = rawItems.map(it => /^(https?:|mailto:|#)/.test(it[2]) ? it : [it[0], it[1], base + it[2], it[3]]);
  function openPalette() {
    if (!palette) {
      palette = document.createElement('dialog');
      palette.className = 'palette'; palette.setAttribute('aria-label', 'Quick navigation');
      palette.innerHTML = '<input type="text" role="combobox" aria-expanded="true" aria-controls="pal-list" placeholder="Jump to a page, project or action…" autocomplete="off" aria-label="Search pages and actions"><ul id="pal-list" role="listbox"></ul><div class="palette-foot"><span>↑↓ navigate</span><span>↵ open</span><span>esc close</span></div>';
      document.body.append(palette);
      const input = $('input', palette), list = $('ul', palette);
      let sel = 0, shown = items;
      const render = () => {
        list.innerHTML = shown.map((it, i) => `<li role="option" class="${i === sel ? 'sel' : ''}" aria-selected="${i === sel}">${it[2] === '#theme' ? `<button type="button" data-i="${i}">` : `<a href="${it[2]}" ${it[2].startsWith('http') ? 'target="_blank" rel="noopener noreferrer"' : ''}>`}<span class="ic" aria-hidden="true">${it[0]}</span>${it[1]}<span class="k">${it[3] || ''}</span>${it[2] === '#theme' ? '</button>' : '</a>'}</li>`).join('') || '<li style="padding:16px;color:var(--subtle)">No matches</li>';
        $('.sel', list)?.scrollIntoView({ block: 'nearest' });
      };
      const run = () => { const it = shown[sel]; if (!it) return; if (it[2] === '#theme') { toggleTheme(); palette.close(); } else { palette.close(); if (it[2].startsWith('http')) window.open(it[2], '_blank', 'noopener'); else location.href = it[2]; } };
      input.addEventListener('input', () => { const q = input.value.toLowerCase(); shown = items.filter(it => it[1].toLowerCase().includes(q)); sel = 0; render(); });
      palette.addEventListener('keydown', e => {
        if (e.key === 'ArrowDown') { e.preventDefault(); sel = Math.min(shown.length - 1, sel + 1); render(); }
        else if (e.key === 'ArrowUp') { e.preventDefault(); sel = Math.max(0, sel - 1); render(); }
        else if (e.key === 'Enter') { e.preventDefault(); run(); }
      });
      list.addEventListener('click', e => { if (e.target.closest('button[data-i]')) { toggleTheme(); palette.close(); } });
      palette.addEventListener('click', e => { if (e.target === palette) palette.close(); });
      palette._reset = () => { input.value = ''; shown = items; sel = 0; render(); input.focus(); };
    }
    if (!palette.open) palette.showModal();
    palette._reset();
  }
  document.addEventListener('keydown', e => {
    const typing = /^(input|textarea|select)$/i.test(document.activeElement?.tagName || '');
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); openPalette(); }
    else if (e.key === '/' && !typing) { e.preventDefault(); openPalette(); }
  });

  /* ---------- 3D tilt cards with glare / foil ---------- */
  const tiltSel = '.service-card, .project-card, .sample-feature-card, .principle, .detail-card, .skill-group, .metric, .benefit, .card, .process-step, .scope-item';
  if (finePointer && !reduceMotion) {
    $$(tiltSel).forEach(card => {
      card.classList.add('tilt');
      const max = card.matches('.metric, .benefit, .scope-item') ? 5 : 8;
      const glare = document.createElement('span'); glare.className = 'glare'; glare.setAttribute('aria-hidden', 'true'); card.append(glare);
      if (card.matches('.service-card, .sample-feature-card, .principle, .card')) { const f = document.createElement('span'); f.className = 'foil'; f.setAttribute('aria-hidden', 'true'); card.append(f); }
      let tx = 0, ty = 0, cx = 0, cy = 0, raf = 0, active = false, gx = 50, gy = 50;
      const loop = () => {
        cx += (tx - cx) * .14; cy += (ty - cy) * .14;
        card.style.setProperty('--rx', (-cy * max).toFixed(2) + 'deg'); card.style.setProperty('--ry', (cx * max).toFixed(2) + 'deg');
        card.style.setProperty('--px', cx.toFixed(3)); card.style.setProperty('--py', cy.toFixed(3));
        card.style.setProperty('--gx', gx.toFixed(1) + '%'); card.style.setProperty('--gy', gy.toFixed(1) + '%');
        if (active || Math.abs(cx) > .002 || Math.abs(cy) > .002) raf = requestAnimationFrame(loop); else raf = 0;
      };
      card.addEventListener('pointermove', e => {
        const r = card.getBoundingClientRect();
        const nx = (e.clientX - r.left) / r.width, ny = (e.clientY - r.top) / r.height;
        tx = nx * 2 - 1; ty = ny * 2 - 1; gx = nx * 100; gy = ny * 100; active = true; if (!raf) raf = requestAnimationFrame(loop);
      });
      card.addEventListener('pointerleave', () => { tx = 0; ty = 0; active = false; if (!raf) raf = requestAnimationFrame(loop); });
    });
  }

  /* ---------- WebGL layers (progressive enhancement: full → reduced → static CSS) ---------- */
  (function webglTier() {
    const nav = navigator, conn = nav.connection || {};
    const lowPower = conn.saveData || (nav.deviceMemory && nav.deviceMemory <= 2) || (nav.hardwareConcurrency && nav.hardwareConcurrency <= 2);
    let ok = false;
    try { const c = document.createElement('canvas'); ok = !!(c.getContext('webgl2') || c.getContext('webgl')); } catch (_) {}
    if (!ok || lowPower || !SCRIPT_SRC || location.search.includes('nogl')) return;
    const mobile = window.matchMedia('(max-width: 760px)').matches;
    root.classList.add('gl-pending');
    // decorative hosts are created here so the HTML stays clean
    const hosts = [];
    const hero = $('.hero-art'); if (hero) hosts.push([hero, 'core']);
    const about = $('.about-visual'); if (about) hosts.push([about, 'core']);
    const sub = $('.subpage-hero'); if (sub && !mobile) hosts.push([sub, 'knot']);
    hosts.forEach(([el, kind]) => { const d = document.createElement('div'); d.className = 'core3d core3d-' + kind; d.setAttribute('aria-hidden', 'true'); el.prepend(d); d._kind = kind; el._core = d; });
    const mount = () => {
      try {
        const G = window.GTA3D;
        hosts.forEach(([el]) => G.core(el._core, el._core._kind, { mobile, still: reduceMotion }));
        if (!reduceMotion) { const bg = document.createElement('canvas'); bg.className = 'bg-gl'; fx.prepend(bg); G.background(bg, { mobile }); }
        root.classList.add('gl'); root.classList.remove('gl-pending');
      } catch (err) { root.classList.remove('gl-pending'); hosts.forEach(([el]) => el._core.remove()); console.warn('3D layer disabled:', err); }
    };
    const load = () => { const s = document.createElement('script'); s.src = new URL('scenes.js', SCRIPT_SRC).href; s.onload = mount; s.onerror = () => { root.classList.remove('gl-pending'); hosts.forEach(([el]) => el._core.remove()); }; document.head.append(s); };
    (window.requestIdleCallback || (f => setTimeout(f, 200)))(load);
  })();
})();
