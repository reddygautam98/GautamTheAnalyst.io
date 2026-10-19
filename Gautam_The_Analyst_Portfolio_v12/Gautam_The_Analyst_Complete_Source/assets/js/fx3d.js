/* Gautam The Analyst — 3D / background effects layer (no libraries; runs after site.js) */
(() => {
  'use strict';
  const root = document.documentElement;
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const DPR = Math.min(devicePixelRatio || 1, 1.75);
  const pointer = { x: 0, y: 0 };            // -1..1 across the viewport
  addEventListener('pointermove', e => { pointer.x = e.clientX / innerWidth * 2 - 1; pointer.y = e.clientY / innerHeight * 2 - 1; }, { passive: true });
  const accent = () => (root.dataset.theme === 'light' ? ['8,126,160', '91,70,229', '226,84,14'] : ['56,225,255', '143,125,255', '255,122,53']);

  /* shared run-loop: pauses off-screen canvases and hidden tabs */
  function loop(el, draw) {
    let raf = 0, visible = true;
    const tick = t => { raf = 0; if (visible && !document.hidden && !window.__v5s) { draw(t); } if (!reduce && visible && !document.hidden) raf = requestAnimationFrame(tick); };
    const kick = () => { if (!raf) raf = requestAnimationFrame(tick); };
    new IntersectionObserver(([en]) => { visible = en.isIntersecting; if (visible) kick(); }).observe(el);
    document.addEventListener('visibilitychange', kick);
    kick();
  }
  function fit(canvas) {
    const ctx = canvas.getContext('2d');
    const size = () => { const w = canvas.clientWidth, h = canvas.clientHeight; canvas.width = Math.max(1, w * DPR); canvas.height = Math.max(1, h * DPR); ctx.setTransform(DPR, 0, 0, DPR, 0, 0); };
    size(); new ResizeObserver(size).observe(canvas);
    return ctx;
  }

  /* ---------- tiny 3D engine: wireframe solids with depth-shaded glow ---------- */
  const shapes = {
    sphere() {
      const n = 150, pts = [], edges = [], g = Math.PI * (3 - Math.sqrt(5));
      for (let i = 0; i < n; i++) { const y = 1 - (i / (n - 1)) * 2, r = Math.sqrt(1 - y * y), th = g * i; pts.push([Math.cos(th) * r, y, Math.sin(th) * r]); }
      for (let i = 0; i < n; i++) {
        const d = pts.map((p, j) => [j, (p[0] - pts[i][0]) ** 2 + (p[1] - pts[i][1]) ** 2 + (p[2] - pts[i][2]) ** 2]).filter(a => a[0] !== i).sort((a, b) => a[1] - b[1]).slice(0, 3);
        d.forEach(([j]) => { if (!edges.some(e => (e[0] === i && e[1] === j) || (e[0] === j && e[1] === i))) edges.push([i, j]); });
      }
      return { pts, edges, scale: .78 };
    },
    icosa() {
      const p = (1 + Math.sqrt(5)) / 2, v = [];
      [[-1, p, 0], [1, p, 0], [-1, -p, 0], [1, -p, 0], [0, -1, p], [0, 1, p], [0, -1, -p], [0, 1, -p], [p, 0, -1], [p, 0, 1], [-p, 0, -1], [-p, 0, 1]].forEach(a => { const l = Math.hypot(...a); v.push(a.map(x => x / l)); });
      const edges = []; v.forEach((a, i) => v.forEach((b, j) => { if (j > i && Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]) < 1.06) edges.push([i, j]); }));
      return { pts: v, edges, scale: .8, inner: true };
    },
    torus() {
      const U = 28, V = 12, R = .66, r = .27, pts = [], edges = [];
      for (let u = 0; u < U; u++) for (let v = 0; v < V; v++) { const a = u / U * 6.283, b = v / V * 6.283; pts.push([(R + r * Math.cos(b)) * Math.cos(a), r * Math.sin(b), (R + r * Math.cos(b)) * Math.sin(a)]); }
      const id = (u, v) => (u % U) * V + (v % V);
      for (let u = 0; u < U; u++) for (let v = 0; v < V; v++) { edges.push([id(u, v), id(u + 1, v)]); edges.push([id(u, v), id(u, v + 1)]); }
      return { pts, edges, scale: .95 };
    },
    lattice() {
      const pts = [], edges = [], k = 3, id = (x, y, z) => (x * k + y) * k + z;
      for (let x = 0; x < k; x++) for (let y = 0; y < k; y++) for (let z = 0; z < k; z++) pts.push([(x - 1) * .5, (y - 1) * .5, (z - 1) * .5]);
      for (let x = 0; x < k; x++) for (let y = 0; y < k; y++) for (let z = 0; z < k; z++) { if (x < k - 1) edges.push([id(x, y, z), id(x + 1, y, z)]); if (y < k - 1) edges.push([id(x, y, z), id(x, y + 1, z)]); if (z < k - 1) edges.push([id(x, y, z), id(x, y, z + 1)]); }
      return { pts, edges, scale: 1.25 };
    }
  };
  function solid(canvas, kind, opts = {}) {
    const ctx = fit(canvas), sh = shapes[kind](), spin = opts.spin ?? .00022;
    let ax = .4, ay = 0, tx = 0, ty = 0, last = 0;
    const rot = ([x, y, z], a, b) => { const c1 = Math.cos(b), s1 = Math.sin(b), x1 = x * c1 + z * s1, z1 = -x * s1 + z * c1, c2 = Math.cos(a), s2 = Math.sin(a); return [x1, y * c2 - z1 * s2, y * s2 + z1 * c2]; };
    loop(canvas, t => {
      const w = canvas.clientWidth, h = canvas.clientHeight, s = Math.min(w, h) / 2 * sh.scale, dt = Math.min(50, t - last || 16); last = t;
      const rect = canvas.getBoundingClientRect(), cx = rect.left + rect.width / 2, cy = rect.top + rect.height / 2;
      tx = reduce ? 0 : ((pointer.x * innerWidth / 2 + innerWidth / 2) - cx) / innerWidth; ty = reduce ? 0 : ((pointer.y * innerHeight / 2 + innerHeight / 2) - cy) / innerHeight;
      ay += dt * spin * 6; ax += (.35 + ty * .9 - ax) * .04; const by = ay + tx * .9 + scrollY * .0016;
      const [c0, c1, c2] = accent();
      ctx.clearRect(0, 0, w, h);
      const P = sh.pts.map(p => { const r = rot(p, ax, by), f = 3 / (3 - r[2]); return { x: w / 2 + r[0] * s * f, y: h / 2 + r[1] * s * f, z: r[2], f }; });
      ctx.lineWidth = 1;
      sh.edges.forEach(([a, b]) => { const A = P[a], B = P[b], d = ((A.z + B.z) / 2 + 1) / 2; ctx.strokeStyle = `rgba(${d > .5 ? c0 : c1},${.12 + d * .55})`; ctx.beginPath(); ctx.moveTo(A.x, A.y); ctx.lineTo(B.x, B.y); ctx.stroke(); });
      P.slice().sort((a, b) => a.z - b.z).forEach(p => { const d = (p.z + 1) / 2, r = (1.2 + d * 2.4) * p.f; const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, r * 3.2); g.addColorStop(0, `rgba(${c0},${.25 + d * .7})`); g.addColorStop(1, `rgba(${c0},0)`); ctx.fillStyle = g; ctx.beginPath(); ctx.arc(p.x, p.y, r * 3.2, 0, 6.283); ctx.fill(); ctx.fillStyle = `rgba(255,255,255,${.35 + d * .6})`; ctx.beginPath(); ctx.arc(p.x, p.y, r * .75, 0, 6.283); ctx.fill(); });
      if (sh.inner) { // orbiting satellite on icosahedron
        const q = rot([Math.cos(t / 900) * 1.18, Math.sin(t / 1300) * .5, Math.sin(t / 900) * 1.18], ax, by), f = 3 / (3 - q[2]);
        ctx.fillStyle = `rgb(${c2})`; ctx.shadowColor = `rgb(${c2})`; ctx.shadowBlur = 14; ctx.beginPath(); ctx.arc(w / 2 + q[0] * s * f, h / 2 + q[1] * s * f, 4 * f, 0, 6.283); ctx.fill(); ctx.shadowBlur = 0;
      }
    });
  }

  /* hero globe (home) + a different 3D solid on each sub-page hero */
  const frame = $('.art-frame');
  if (frame) { const c = document.createElement('canvas'); c.className = 'globe3d'; c.setAttribute('aria-hidden', 'true'); frame.prepend(c); solid(c, 'sphere', { spin: .00018 }); }
  const sub = $('.subpage-hero');
  if (sub && innerWidth > 920) {
    const kind = { about: 'torus', services: 'lattice', projects: 'icosa', resume: 'torus', contact: 'sphere' }[(location.pathname.split('/').pop() || '').replace('.html', '')] || 'icosa';
    const box = document.createElement('div'); box.className = 'hero3d'; box.setAttribute('aria-hidden', 'true');
    const c = document.createElement('canvas'); box.append(c); sub.append(box); solid(c, kind);
  }

  /* ---------- perspective grid floor under every hero ---------- */
  $$('.hero, .subpage-hero').forEach(h => { const f = document.createElement('div'); f.className = 'floor'; f.setAttribute('aria-hidden', 'true'); h.prepend(f); });

  /* ---------- background depth: stars, orbs, floating glass cubes, scroll hue ---------- */
  const fx = $('.bg-fx');
  if (fx) {
    const parallax = [];
    const add = (el, speed, px = 0) => { fx.append(el); parallax.push({ el, speed, px, base: el.dataset.t || '' }); };
    [['o1', 420, '8%', '6%', .08], ['o2 orb', 300, '78%', '38%', .14], ['o1', 220, '60%', '78%', .22]].forEach(([c, s, l, t, sp], i) => {
      const o = document.createElement('div'); o.className = 'orb' + (i === 1 ? ' o2' : ''); Object.assign(o.style, { width: s + 'px', height: s + 'px', left: l, top: t }); add(o, sp, 18);
    });
    [[70, '86%', '16%', .16], [48, '5%', '52%', .24], [96, '90%', '66%', .1], [38, '46%', '88%', .3]].forEach(([s, l, t, sp], i) => {
      const w = document.createElement('div'); w.className = 'cube-wrap'; Object.assign(w.style, { left: l, top: t, width: s + 'px', height: s + 'px' });
      const c = document.createElement('div'); c.className = 'cube'; c.style.cssText = `inset:0;--s:${s}px`;
      const inn = document.createElement('div'); inn.className = 'cube-in'; inn.style.animationDuration = 18 + i * 7 + 's'; inn.style.animationDirection = i % 2 ? 'reverse' : 'normal'; inn.innerHTML = '<i></i><i></i><i></i><i></i><i></i><i></i>';
      c.append(inn); w.append(c); add(w, sp, 26);
    });
    const cv = document.createElement('canvas'); cv.className = 'stars'; fx.insertBefore(cv, $('.noise', fx));
    const ctx = fit(cv);
    const stars = Array.from({ length: 120 }, () => ({ x: Math.random(), y: Math.random(), z: Math.random() * .85 + .15, tw: Math.random() * 6.28 }));
    let shoot = null, nextShoot = 4000, sx = 0, sy = 0;
    const frameStars = t => {
      const w = cv.clientWidth, h = cv.clientHeight, [c0] = accent(), sc = scrollY;
      sx += (pointer.x - sx) * .05; sy += (pointer.y - sy) * .05;
      ctx.clearRect(0, 0, w, h);
      for (const s of stars) {
        const x = ((s.x * w - sx * 26 * s.z) % w + w) % w, y = ((s.y * h - sc * .22 * s.z - sy * 16 * s.z) % h + h) % h;
        const a = (.25 + .6 * Math.abs(Math.sin(t / 1100 + s.tw))) * s.z; ctx.fillStyle = `rgba(${root.dataset.theme === 'light' ? c0 : '220,236,255'},${a})`;
        ctx.fillRect(x, y, s.z * 1.8, s.z * 1.8);
      }
      if (!reduce) {
        if (!shoot && t > nextShoot) { shoot = { x: Math.random() * w * .7, y: Math.random() * h * .35, l: 0 }; nextShoot = t + 6000 + Math.random() * 7000; }
        if (shoot) { shoot.x += 14; shoot.y += 6; shoot.l += 1; const g = ctx.createLinearGradient(shoot.x, shoot.y, shoot.x - 90, shoot.y - 38); g.addColorStop(0, `rgba(${c0},.9)`); g.addColorStop(1, `rgba(${c0},0)`); ctx.strokeStyle = g; ctx.lineWidth = 1.6; ctx.beginPath(); ctx.moveTo(shoot.x, shoot.y); ctx.lineTo(shoot.x - 90, shoot.y - 38); ctx.stroke(); if (shoot.l > 60) shoot = null; }
      }
    };
    loop(cv, frameStars);
    let tick = false;
    const onScroll = () => {
      if (tick) return; tick = true;
      requestAnimationFrame(() => {
        const y = scrollY, max = Math.max(1, document.documentElement.scrollHeight - innerHeight);
        parallax.forEach(p => { p.el.style.transform = `translate3d(${pointer.x * p.px}px, ${-y * p.speed}px, 0)`; });
        fx.style.setProperty('--hue', (y / max) * 70 - 20 + 'deg');
        tick = false;
      });
    };
    addEventListener('scroll', onScroll, { passive: true }); if (!reduce) addEventListener('pointermove', onScroll, { passive: true }); onScroll();
  }

  /* ---------- tilt + holographic glare + HUD brackets on cards ---------- */
  const tiltSel = '.service-card, .project-card, .detail-card, .skill-group, .sample-feature-card, .principle, .card, .benefit, .metric, .scope-item, .contact-method, .process-step';
  const hudSel = '.service-card, .sample-feature-card, .principle, .detail-card, .skill-group, .card, .project-card';
  $$('.metric, .benefit').forEach(m => { const l = document.createElement('span'); l.className = 'pulse-line'; l.setAttribute('aria-hidden', 'true'); m.append(l); });
  $$(tiltSel).forEach(card => {
    const g = document.createElement('span'); g.className = 'glare'; g.setAttribute('aria-hidden', 'true'); card.append(g);
    if (card.matches(hudSel)) ['tl', 'tr', 'bl', 'br'].forEach(c => { const h = document.createElement('i'); h.className = 'hud ' + c; h.setAttribute('aria-hidden', 'true'); card.append(h); });
    if (!fine || reduce) return;
    card.classList.add('tilt');
    const w0 = () => card.offsetWidth;
    let raf = 0;
    card.addEventListener('pointerenter', () => { if (card.hasAttribute('data-reveal')) { card.removeAttribute('data-reveal'); card.style.removeProperty('--d'); } card.classList.remove('resting'); });
    card.addEventListener('pointermove', e => {
      if (raf) return;
      raf = requestAnimationFrame(() => {
        raf = 0; const r = card.getBoundingClientRect(), px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height, max = w0() > 700 ? 2.2 : w0() > 420 ? 5.5 : 9;
        card.style.setProperty('--ry', ((px - .5) * 2 * max).toFixed(2) + 'deg'); card.style.setProperty('--rx', ((.5 - py) * 2 * max).toFixed(2) + 'deg');
        card.style.setProperty('--gx', (px * 100).toFixed(1) + '%'); card.style.setProperty('--gy', (py * 100).toFixed(1) + '%');
        card.style.setProperty('--bx', (px * 100).toFixed(1) + '%'); card.style.setProperty('--by', (py * 100).toFixed(1) + '%');
      });
    });
    card.addEventListener('pointerleave', () => { card.classList.add('resting'); card.style.setProperty('--rx', '0deg'); card.style.setProperty('--ry', '0deg'); });
  });

  /* ---------- 3D toolkit ring (drag / inertia / auto-spin) ---------- */
  const scene = $('#ring-scene'), ring = $('#ring');
  if (scene && ring) {
    const n = +ring.style.getPropertyValue('--n') || 10;
    const setRadius = () => { const w = scene.clientWidth, item = w < 560 ? 150 : 184; ring.style.setProperty('--r', Math.round(item / 2 / Math.tan(Math.PI / n) + 26) + 'px'); ring.style.setProperty('--rm', Math.round(150 / 2 / Math.tan(Math.PI / n) + 18) + 'px'); };
    setRadius(); new ResizeObserver(setRadius).observe(scene);
    let rot = 0, vel = reduce ? 0 : .16, drag = false, lx = 0, hover = false;
    scene.addEventListener('pointerdown', e => { drag = true; lx = e.clientX; scene.classList.add('drag'); scene.setPointerCapture(e.pointerId); });
    scene.addEventListener('pointermove', e => { if (!drag) return; const dx = e.clientX - lx; lx = e.clientX; rot += dx * .35; vel = dx * .35; });
    const up = () => { drag = false; scene.classList.remove('drag'); if (Math.abs(vel) < .05) vel = reduce ? 0 : .16; };
    scene.addEventListener('pointerup', up); scene.addEventListener('pointercancel', up);
    scene.addEventListener('pointerenter', () => { hover = true; }); scene.addEventListener('pointerleave', () => { hover = false; });
    scene.tabIndex = 0;
    scene.addEventListener('keydown', e => { if (e.key === 'ArrowLeft') { rot += 36; vel = 0; } if (e.key === 'ArrowRight') { rot -= 36; vel = 0; } });
    loop(scene, () => {
      if (!drag) { const target = reduce ? 0 : (hover ? .05 : .16); vel += (target - vel) * .02; rot += vel; }
      ring.style.setProperty('--rot', rot.toFixed(2) + 'deg');
    });
  }
})();
