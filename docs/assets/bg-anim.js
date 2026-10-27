/**
 * GautamTheAnalyst.io - Bespoke Page Background Animations
 * Unique, content-tailored canvas animations for each portfolio page:
 * - Home: Financial Telemetry & Constellation Stream
 * - About: Blueprint Architecture Grid & Circuit Matrix
 * - Services: Deliverable Pipeline Flow Channels
 * - Projects: Interactive Intelligence Dot Matrix
 * - Samples: Requirements Traceability Scanning Matrix
 * - Resume: Executive Career Horizon Wave
 * - Contact: Global Connectivity Radar Beacon
 * 
 * Performance & A11y:
 * - 60fps capped, DPR capped at 2, viewport-clipped
 * - IntersectionObserver: halts rendering when off-screen
 * - Honors prefers-reduced-motion and html.is-anim-paused (renders one static frame)
 * - Zero pointer blocking (pointer-events: none)
 */
(function() {
  'use strict';

  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var MAX_DPR = 2;

  function isReduced() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function isPaused() {
    return document.documentElement.classList.contains('is-anim-paused');
  }

  function getThemeColors() {
    var isDark = document.documentElement.dataset.theme === 'dark';
    return {
      isDark: isDark,
      primary: isDark ? 'rgba(56, 189, 248, ' : 'rgba(37, 99, 235, ',
      secondary: isDark ? 'rgba(129, 140, 248, ' : 'rgba(79, 70, 229, ',
      accent: isDark ? 'rgba(52, 211, 153, ' : 'rgba(16, 185, 129, ',
      grid: isDark ? 'rgba(148, 163, 184, 0.07)' : 'rgba(15, 23, 42, 0.05)',
      cardBg: isDark ? 'rgba(15, 23, 42, 0.6)' : 'rgba(255, 255, 255, 0.7)'
    };
  }

  // Generic Canvas Host Manager
  function setupCanvas(host, renderFn, mouseMoveFn) {
    var canvas = host.querySelector('canvas.bg-anim-canvas');
    if (!canvas) {
      canvas = document.createElement('canvas');
      canvas.className = 'bg-anim-canvas';
      canvas.setAttribute('aria-hidden', 'true');
      host.insertBefore(canvas, host.firstChild);
    }
    var ctx = canvas.getContext('2d');
    if (!ctx) return;

    var cssW = 0, cssH = 0, dpr = 1;
    var isVisible = false;
    var rafId = null;
    var mouse = { x: -9999, y: -9999, active: false };

    function resize() {
      var rect = host.getBoundingClientRect();
      cssW = rect.width || window.innerWidth;
      cssH = rect.height || 600;
      dpr = Math.min(window.devicePixelRatio || 1, MAX_DPR);

      var pw = Math.round(cssW * dpr);
      var ph = Math.round(cssH * dpr);
      if (canvas.width !== pw || canvas.height !== ph) {
        canvas.width = pw;
        canvas.height = ph;
        canvas.style.width = '100%';
        canvas.style.height = '100%';
      }
    }

    function loop(t) {
      if (!isVisible || document.hidden || isReduced() || isPaused()) {
        rafId = null;
        return;
      }
      ctx.save();
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      renderFn(ctx, cssW, cssH, t, mouse, getThemeColors());
      ctx.restore();
      rafId = requestAnimationFrame(loop);
    }

    function checkState() {
      if (isVisible && !document.hidden && !isReduced() && !isPaused()) {
        if (!rafId) rafId = requestAnimationFrame(loop);
      } else {
        if (rafId) {
          cancelAnimationFrame(rafId);
          rafId = null;
        }
        if (isVisible) {
          ctx.save();
          ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
          renderFn(ctx, cssW, cssH, 1000, { x: -9999, y: -9999, active: false }, getThemeColors());
          ctx.restore();
        }
      }
    }

    if (fine) {
      host.addEventListener('pointermove', function(e) {
        var r = host.getBoundingClientRect();
        mouse.x = e.clientX - r.left;
        mouse.y = e.clientY - r.top;
        mouse.active = true;
        if (mouseMoveFn) mouseMoveFn(mouse, cssW, cssH);
        if (!rafId && isVisible && !isReduced() && !isPaused()) {
          rafId = requestAnimationFrame(loop);
        }
      }, { passive: true });

      host.addEventListener('pointerleave', function() {
        mouse.active = false;
        mouse.x = -9999;
        mouse.y = -9999;
      }, { passive: true });
    }

    var ro = ('ResizeObserver' in window) ? new ResizeObserver(function() {
      resize();
      checkState();
    }) : null;
    if (ro) ro.observe(host);

    var io = ('IntersectionObserver' in window) ? new IntersectionObserver(function(es) {
      es.forEach(function(e) {
        isVisible = e.isIntersecting;
        checkState();
      });
    }, { threshold: 0.05 }) : null;
    if (io) io.observe(host);

    var mo = new MutationObserver(checkState);
    mo.observe(document.documentElement, { attributes: true, attributeFilter: ['class', 'data-theme'] });
    document.addEventListener('visibilitychange', checkState);

    window.addEventListener('pagehide', function() {
      if (rafId) cancelAnimationFrame(rafId);
      if (ro) ro.disconnect();
      if (io) io.disconnect();
      if (mo) mo.disconnect();
    });

    resize();
    checkState();
  }

  // 1. HOME: Financial Telemetry & Constellation Stream
  function initHomeTelemetry(host) {
    var nodes = [];
    var count = 38;
    var tags = ['TXN', 'ACK', 'RECON', 'REST', 'SLA', '200 OK', '99.8%', 'STTM', 'AUDIT'];

    for (var i = 0; i < count; i++) {
      nodes.push({
        x: Math.random() * 1400,
        y: Math.random() * 700,
        vx: (Math.random() - 0.5) * 0.45,
        vy: (Math.random() - 0.5) * 0.35,
        radius: Math.random() * 2.2 + 1.2,
        tag: tags[i % tags.length],
        showTag: i % 4 === 0,
        pulse: Math.random() * Math.PI * 2
      });
    }

    setupCanvas(host, function(ctx, w, h, t, mouse, pal) {
      ctx.clearRect(0, 0, w, h);

      // Update positions
      for (var i = 0; i < nodes.length; i++) {
        var n = nodes[i];
        n.x += n.vx;
        n.y += n.vy;
        n.pulse += 0.025;

        // Wrap around bounds
        if (n.x < -20) n.x = w + 20;
        if (n.x > w + 20) n.x = -20;
        if (n.y < -20) n.y = h + 20;
        if (n.y > h + 20) n.y = -20;

        // Mouse attraction
        if (mouse.active) {
          var dx = mouse.x - n.x;
          var dy = mouse.y - n.y;
          var dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 180 && dist > 1) {
            n.x += (dx / dist) * 0.35;
            n.y += (dy / dist) * 0.35;
          }
        }
      }

      // Draw connecting telemetry lines
      for (var i = 0; i < nodes.length; i++) {
        for (var j = i + 1; j < nodes.length; j++) {
          var dx = nodes[i].x - nodes[j].x;
          var dy = nodes[i].y - nodes[j].y;
          var d = Math.sqrt(dx * dx + dy * dy);
          if (d < 130) {
            var alpha = (1 - (d / 130)) * 0.16;
            ctx.strokeStyle = pal.primary + alpha.toFixed(3) + ')';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(nodes[i].x, nodes[i].y);
            ctx.lineTo(nodes[j].x, nodes[j].y);
            ctx.stroke();
          }
        }
      }

      // Draw nodes and tags
      ctx.font = '500 9px "IBM Plex Mono", monospace';
      for (var i = 0; i < nodes.length; i++) {
        var n = nodes[i];
        var glow = Math.sin(n.pulse) * 0.12 + 0.28;

        ctx.fillStyle = pal.primary + glow.toFixed(3) + ')';
        ctx.beginPath();
        ctx.arc(n.x, n.y, n.radius, 0, Math.PI * 2);
        ctx.fill();

        if (n.showTag) {
          ctx.fillStyle = pal.secondary + (glow * 0.7).toFixed(3) + ')';
          ctx.fillText(n.tag, n.x + 7, n.y + 3);
        }
      }

      // Mouse interactive beacon
      if (mouse.active) {
        var rad = (Math.sin(t * 0.003) * 15 + 45);
        ctx.strokeStyle = pal.primary + '0.12)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.arc(mouse.x, mouse.y, rad, 0, Math.PI * 2);
        ctx.stroke();
      }
    });
  }

  // 2. ABOUT: Architectural Blueprint Grid & Circuit Matrix
  function initAboutBlueprint(host) {
    var pulses = [];
    for (var i = 0; i < 7; i++) {
      pulses.push({
        x: Math.random() * 1200,
        y: Math.floor(Math.random() * 15) * 44,
        speed: Math.random() * 2 + 1.5,
        len: Math.random() * 60 + 40
      });
    }

    setupCanvas(host, function(ctx, w, h, t, mouse, pal) {
      ctx.clearRect(0, 0, w, h);

      // Draw subtle CAD coordinate marks
      ctx.strokeStyle = pal.grid;
      ctx.lineWidth = 1;

      var step = 88;
      ctx.beginPath();
      for (var x = 0; x < w; x += step) {
        ctx.moveTo(x, 0); ctx.lineTo(x, h);
      }
      for (var y = 0; y < h; y += step) {
        ctx.moveTo(0, y); ctx.lineTo(w, y);
      }
      ctx.stroke();

      // Draw crosshairs at grid intersections
      ctx.strokeStyle = pal.primary + '0.18)';
      ctx.lineWidth = 1;
      for (var x = step; x < w; x += step * 2) {
        for (var y = step; y < h; y += step * 2) {
          ctx.beginPath();
          ctx.moveTo(x - 5, y); ctx.lineTo(x + 5, y);
          ctx.moveTo(x, y - 5); ctx.lineTo(x, y + 5);
          ctx.stroke();
        }
      }

      // Traveling specification pulses along blueprint channels
      for (var p = 0; p < pulses.length; p++) {
        var item = pulses[p];
        item.x += item.speed;
        if (item.x > w + 100) {
          item.x = -item.len;
          item.y = Math.floor(Math.random() * (h / 44)) * 44;
        }

        var grad = ctx.createLinearGradient(item.x - item.len, item.y, item.x, item.y);
        grad.addColorStop(0, pal.primary + '0)');
        grad.addColorStop(1, pal.primary + '0.35)');
        ctx.strokeStyle = grad;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(item.x - item.len, item.y);
        ctx.lineTo(item.x, item.y);
        ctx.stroke();

        ctx.fillStyle = pal.primary + '0.6)';
        ctx.beginPath();
        ctx.arc(item.x, item.y, 2.5, 0, Math.PI * 2);
        ctx.fill();
      }

      // Mouse crosshair coordinates
      if (mouse.active) {
        ctx.strokeStyle = pal.secondary + '0.22)';
        ctx.setLineDash([4, 4]);
        ctx.beginPath();
        ctx.moveTo(mouse.x, 0); ctx.lineTo(mouse.x, h);
        ctx.moveTo(0, mouse.y); ctx.lineTo(w, mouse.y);
        ctx.stroke();
        ctx.setLineDash([]);

        ctx.font = '500 10px "IBM Plex Mono", monospace';
        ctx.fillStyle = pal.primary + '0.45)';
        ctx.fillText('LOC [' + Math.round(mouse.x) + ',' + Math.round(mouse.y) + ']', mouse.x + 10, mouse.y - 8);
      }
    });
  }

  // 3. SERVICES: Deliverable Pipeline Flow Channels
  function initServicesPipeline(host) {
    var packets = [];
    var lanes = 5;

    for (var i = 0; i < 22; i++) {
      packets.push({
        lane: i % lanes,
        progress: Math.random(),
        speed: (Math.random() * 0.0012) + 0.0008,
        label: ['BRD', 'API', 'STTM', 'UAT', 'SQL', 'BDD', 'RTM'][i % 7],
        size: Math.random() * 3 + 3
      });
    }

    setupCanvas(host, function(ctx, w, h, t, mouse, pal) {
      ctx.clearRect(0, 0, w, h);

      var laneH = h / (lanes + 1);

      // Draw multi-lane process channels
      for (var l = 1; l <= lanes; l++) {
        var y = l * laneH;
        var waveY = Math.sin(t * 0.001 + l) * 12;

        ctx.strokeStyle = pal.primary + '0.07)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(0, y + waveY);
        ctx.bezierCurveTo(w * 0.33, y - waveY * 2, w * 0.66, y + waveY * 2, w, y + waveY);
        ctx.stroke();
      }

      // Render traveling deliverable packets
      ctx.font = '600 9px "IBM Plex Mono", monospace';
      for (var i = 0; i < packets.length; i++) {
        var pk = packets[i];
        pk.progress += pk.speed;
        if (pk.progress > 1) pk.progress = 0;

        var yBase = (pk.lane + 1) * laneH;
        var waveOff = Math.sin(t * 0.001 + pk.lane) * 12;
        var x = pk.progress * w;
        var y = yBase + waveOff;

        // Packet glow
        var distM = mouse.active ? Math.hypot(mouse.x - x, mouse.y - y) : 999;
        var boost = distM < 120 ? (1 - distM / 120) * 0.4 : 0;
        var alpha = (0.2 + boost).toFixed(3);

        ctx.fillStyle = pal.primary + alpha + ')';
        ctx.beginPath();
        ctx.arc(x, y, pk.size + (boost * 3), 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = pal.secondary + (0.35 + boost).toFixed(3) + ')';
        ctx.fillText(pk.label, x + 8, y + 3);
      }
    });
  }

  // 4. PROJECTS: Interactive Intelligence Dot Matrix
  function initProjectsDotMatrix(host) {
    var spacing = 36;

    setupCanvas(host, function(ctx, w, h, t, mouse, pal) {
      ctx.clearRect(0, 0, w, h);

      var cols = Math.ceil(w / spacing);
      var rows = Math.ceil(h / spacing);
      var timeSec = t * 0.0015;

      for (var r = 0; r < rows; r++) {
        var y0 = r * spacing;
        for (var c = 0; c < cols; c++) {
          var x0 = c * spacing;

          var wave = Math.sin(c * 0.18 + timeSec) * Math.cos(r * 0.18 - timeSec * 0.8);
          var dotRadius = 1.2 + wave * 0.6;
          var alpha = 0.08 + wave * 0.04;

          // Mouse proximity spring & glow
          if (mouse.active) {
            var dx = mouse.x - x0;
            var dy = mouse.y - y0;
            var dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < 140) {
              var factor = 1 - (dist / 140);
              dotRadius += factor * 3.5;
              alpha += factor * 0.4;
            }
          }

          if (dotRadius > 0.4) {
            ctx.fillStyle = pal.primary + Math.max(0.04, alpha).toFixed(3) + ')';
            ctx.beginPath();
            ctx.arc(x0, y0, Math.max(0.6, dotRadius), 0, Math.PI * 2);
            ctx.fill();
          }
        }
      }
    });
  }

  // 5. BA SAMPLES: Requirements Traceability Scanning Matrix
  function initSamplesMatrix(host) {
    var codes = ['REQ-01', 'BR-02', 'FR-004', 'US-03', 'TC-002', 'RTM 100%', 'UAT PASS', '200 OK', 'REST-API', 'SLA 4H'];
    var columns = [];
    var colCount = 14;

    for (var i = 0; i < colCount; i++) {
      columns.push({
        x: (i + 0.5) * (1400 / colCount),
        y: Math.random() * 600,
        speed: Math.random() * 0.6 + 0.35,
        code: codes[i % codes.length],
        pulse: Math.random() * Math.PI
      });
    }

    setupCanvas(host, function(ctx, w, h, t, mouse, pal) {
      ctx.clearRect(0, 0, w, h);

      // Audit scanline moving vertically
      var scanY = ((t * 0.05) % (h + 100)) - 50;
      var scanGrad = ctx.createLinearGradient(0, scanY - 35, 0, scanY + 35);
      scanGrad.addColorStop(0, 'rgba(56, 189, 248, 0)');
      scanGrad.addColorStop(0.5, pal.primary + '0.12)');
      scanGrad.addColorStop(1, 'rgba(56, 189, 248, 0)');

      ctx.fillStyle = scanGrad;
      ctx.fillRect(0, scanY - 35, w, 70);

      ctx.strokeStyle = pal.primary + '0.25)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(0, scanY); ctx.lineTo(w, scanY);
      ctx.stroke();

      // Drifting traceability badges
      ctx.font = '600 10px "IBM Plex Mono", monospace';
      for (var i = 0; i < columns.length; i++) {
        var item = columns[i];
        item.y += item.speed;
        if (item.y > h + 30) item.y = -30;

        var dMouse = mouse.active ? Math.hypot(mouse.x - item.x, mouse.y - item.y) : 999;
        var boost = dMouse < 130 ? (1 - dMouse / 130) * 0.5 : 0;
        var alpha = (0.16 + boost).toFixed(3);

        ctx.strokeStyle = pal.primary + alpha + ')';
        ctx.fillStyle = pal.secondary + (0.2 + boost).toFixed(3) + ')';

        var txtW = ctx.measureText(item.code).width;
        ctx.strokeRect(item.x - 4, item.y - 10, txtW + 8, 15);
        ctx.fillText(item.code, item.x, item.y + 2);
      }
    });
  }

  // 6. RESUME: Executive Career Horizon Wave
  function initResumeHorizon(host) {
    setupCanvas(host, function(ctx, w, h, t, mouse, pal) {
      ctx.clearRect(0, 0, w, h);

      var time = t * 0.0008;
      var waves = [
        { amp: 35, freq: 0.002, speed: 1.0, alpha: 0.09, y: h * 0.4 },
        { amp: 45, freq: 0.0016, speed: -0.7, alpha: 0.07, y: h * 0.55 },
        { amp: 30, freq: 0.0025, speed: 1.3, alpha: 0.06, y: h * 0.7 }
      ];

      for (var i = 0; i < waves.length; i++) {
        var wv = waves[i];
        ctx.strokeStyle = pal.primary + wv.alpha + ')';
        ctx.lineWidth = 1.5;
        ctx.beginPath();

        for (var x = 0; x <= w; x += 15) {
          var y = wv.y + Math.sin(x * wv.freq + time * wv.speed) * wv.amp;
          if (mouse.active) {
            var dist = Math.abs(mouse.x - x);
            if (dist < 150) {
              y += (1 - dist / 150) * (mouse.y - y) * 0.25;
            }
          }
          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();
      }
    });
  }

  // 7. CONTACT: Global Connectivity Radar Beacon
  function initContactRadar(host) {
    var satellites = [
      { angle: 0.4, dist: 120, label: 'BLR (IST)', speed: 0.003 },
      { angle: 2.1, dist: 180, label: 'US-EST', speed: 0.002 },
      { angle: 3.8, dist: 240, label: 'EU-GMT', speed: 0.0015 },
      { angle: 5.2, dist: 300, label: 'APAC', speed: 0.0025 }
    ];

    setupCanvas(host, function(ctx, w, h, t, mouse, pal) {
      ctx.clearRect(0, 0, w, h);

      var cx = w * 0.75;
      var cy = h * 0.45;
      if (w < 800) { cx = w * 0.5; cy = h * 0.35; }

      // Target steer toward cursor if nearby
      if (mouse.active && Math.hypot(mouse.x - cx, mouse.y - cy) < 350) {
        cx += (mouse.x - cx) * 0.15;
        cy += (mouse.y - cy) * 0.15;
      }

      // Concentric radar rings
      var rings = [80, 150, 220, 290, 360];
      ctx.lineWidth = 1;
      for (var i = 0; i < rings.length; i++) {
        var r = rings[i];
        ctx.strokeStyle = pal.primary + (0.08 - i * 0.012).toFixed(3) + ')';
        ctx.beginPath();
        ctx.arc(cx, cy, r, 0, Math.PI * 2);
        ctx.stroke();
      }

      // Rotating radar sweep beam
      var sweepAngle = (t * 0.0012) % (Math.PI * 2);
      var grad = ctx.createRadialGradient(cx, cy, 20, cx, cy, 360);
      grad.addColorStop(0, pal.primary + '0.2)');
      grad.addColorStop(1, 'rgba(56, 189, 248, 0)');

      ctx.save();
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.arc(cx, cy, 360, sweepAngle - 0.4, sweepAngle);
      ctx.closePath();
      ctx.fillStyle = grad;
      ctx.fill();
      ctx.restore();

      // Satellite time-zone hubs
      ctx.font = '600 9px "IBM Plex Mono", monospace';
      for (var s = 0; s < satellites.length; s++) {
        var sat = satellites[s];
        sat.angle += sat.speed;
        var sx = cx + Math.cos(sat.angle) * sat.dist;
        var sy = cy + Math.sin(sat.angle) * sat.dist;

        ctx.fillStyle = pal.primary + '0.45)';
        ctx.beginPath();
        ctx.arc(sx, sy, 3, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = pal.secondary + '0.35)';
        ctx.fillText(sat.label, sx + 6, sy + 3);
      }
    });
  }

  // Automatic Dispatcher based on data-bg-anim attribute
  function initAll() {
    var targets = document.querySelectorAll('[data-bg-anim]');
    for (var i = 0; i < targets.length; i++) {
      var el = targets[i];
      var type = el.getAttribute('data-bg-anim');
      if (type === 'telemetry') initHomeTelemetry(el);
      else if (type === 'blueprint') initAboutBlueprint(el);
      else if (type === 'pipeline') initServicesPipeline(el);
      else if (type === 'dotmatrix') initProjectsDotMatrix(el);
      else if (type === 'rtm') initSamplesMatrix(el);
      else if (type === 'horizon') initResumeHorizon(el);
      else if (type === 'radar') initContactRadar(el);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }
})();
