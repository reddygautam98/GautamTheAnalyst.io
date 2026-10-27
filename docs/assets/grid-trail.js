/**
 * Interactive Grid Trail (Vanilla JS Reimplementation)
 * Inspired by Lightswind Interactive Grid Background.
 * Subtly highlights 44px blueprint grid cells under the cursor.
 * Only active for fine pointer devices; zero idle animation overhead.
 */
(function() {
  'use strict';

  var GRID_SIZE = 44;
  var TRAIL_MAX = 6;
  var FADE_DURATION = 900; // ms
  var MAX_DPR = 2;
  var MAX_WIDTH = 1920;
  var MAX_HEIGHT = 800;

  function parseRgb(colorStr) {
    if (!colorStr) return { r: 37, g: 99, b: 235 };
    var match = colorStr.match(/rgba?\((\d+)\s*,\s*(\d+)\s*,\s*(\d+)/i);
    if (match) {
      return { r: parseInt(match[1], 10), g: parseInt(match[2], 10), b: parseInt(match[3], 10) };
    }
    if (colorStr.indexOf('#') === 0) {
      var hex = colorStr.slice(1);
      if (hex.length === 3) hex = hex.split('').map(function(c) { return c + c; }).join('');
      if (hex.length === 6) {
        var num = parseInt(hex, 16);
        return { r: (num >> 16) & 255, g: (num >> 8) & 255, b: num & 255 };
      }
    }
    return { r: 37, g: 99, b: 235 };
  }

  function initGridTrail(host) {
    var canvas = host.querySelector('canvas.grid-trail-canvas') || host.querySelector('canvas');
    if (!canvas) {
      canvas = document.createElement('canvas');
      canvas.className = 'grid-trail-canvas';
      canvas.setAttribute('aria-hidden', 'true');
      host.insertBefore(canvas, host.firstChild);
    }

    // Only enable for fine mouse pointers (not touch) and when motion is allowed
    var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
    var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!finePointer || reducedMotion) {
      return; // Leave empty canvas element untouched
    }

    var ctx = canvas.getContext('2d');
    if (!ctx) return;

    var cssW = 0;
    var cssH = 0;
    var dpr = 1;
    var trail = [];
    var animating = false;
    var rafId = null;
    var themeColor = { r: 37, g: 99, b: 235 };

    function resolveThemeColor() {
      try {
        var isDark = document.documentElement.dataset.theme === 'dark';
        if (isDark) {
          themeColor = { r: 56, g: 189, b: 248 }; // --accent-2 sky blue in dark
        } else {
          themeColor = { r: 37, g: 99, b: 235 }; // --accent cobalt in light
        }
      } catch (_) {}
    }

    function isAnimPaused() {
      return document.documentElement.classList.contains('is-anim-paused');
    }

    function resize() {
      var rect = host.getBoundingClientRect();
      var rawW = rect.width || window.innerWidth;
      var rawH = rect.height || 400;

      cssW = Math.min(Math.max(rawW, 60), MAX_WIDTH);
      cssH = Math.min(Math.max(rawH, 40), MAX_HEIGHT);
      dpr = Math.min(window.devicePixelRatio || 1, MAX_DPR);

      var pixelW = Math.round(cssW * dpr);
      var pixelH = Math.round(cssH * dpr);

      if (canvas.width !== pixelW || canvas.height !== pixelH) {
        canvas.width = pixelW;
        canvas.height = pixelH;
        canvas.style.width = '100%';
        canvas.style.height = '100%';
      }
      resolveThemeColor();
    }

    function render(now) {
      if (isAnimPaused()) {
        ctx.clearRect(0, 0, cssW, cssH);
        trail = [];
        animating = false;
        rafId = null;
        return;
      }

      // Filter expired cells
      var active = [];
      for (var i = 0; i < trail.length; i++) {
        if (now - trail[i].t < FADE_DURATION) {
          active.push(trail[i]);
        }
      }
      trail = active;

      ctx.save();
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, cssW, cssH);

      if (trail.length === 0) {
        ctx.restore();
        animating = false;
        rafId = null;
        return; // Zero idle draw overhead
      }

      // Draw active cells
      for (var j = 0; j < trail.length; j++) {
        var item = trail[j];
        var age = now - item.t;
        var progress = Math.max(0, 1 - (age / FADE_DURATION)); // 1 down to 0
        var fillAlpha = (progress * 0.22).toFixed(3);
        var borderAlpha = (progress * 0.45).toFixed(3);

        ctx.fillStyle = 'rgba(' + themeColor.r + ',' + themeColor.g + ',' + themeColor.b + ',' + fillAlpha + ')';
        ctx.fillRect(item.x, item.y, GRID_SIZE, GRID_SIZE);

        ctx.strokeStyle = 'rgba(' + themeColor.r + ',' + themeColor.g + ',' + themeColor.b + ',' + borderAlpha + ')';
        ctx.lineWidth = 1;
        ctx.strokeRect(item.x + 0.5, item.y + 0.5, GRID_SIZE - 1, GRID_SIZE - 1);
      }

      ctx.restore();
      rafId = requestAnimationFrame(render);
    }

    function startAnimation() {
      if (!animating) {
        animating = true;
        rafId = requestAnimationFrame(render);
      }
    }

    function onMouseMove(e) {
      if (isAnimPaused()) return;
      var rect = host.getBoundingClientRect();
      if (e.clientX < rect.left || e.clientX > rect.right || e.clientY < rect.top || e.clientY > rect.bottom) {
        return;
      }

      // Snap coordinates to 44px viewport grid used by body::before
      var col = Math.floor(e.clientX / GRID_SIZE);
      var row = Math.floor(e.clientY / GRID_SIZE);

      var cellX = (col * GRID_SIZE) - rect.left;
      var cellY = (row * GRID_SIZE) - rect.top;

      // Avoid repeating the same cell consecutively
      if (trail.length > 0) {
        var last = trail[trail.length - 1];
        if (last.col === col && last.row === row) return;
      }

      trail.push({
        col: col,
        row: row,
        x: cellX,
        y: cellY,
        t: performance.now()
      });

      if (trail.length > TRAIL_MAX) {
        trail.shift();
      }

      startAnimation();
    }

    function onMouseLeave() {
      // Allow current trail to naturally fade out to 0
    }

    host.addEventListener('mousemove', onMouseMove, { passive: true });
    host.addEventListener('mouseleave', onMouseLeave, { passive: true });

    var ro = null;
    if ('ResizeObserver' in window) {
      ro = new ResizeObserver(resize);
      ro.observe(host);
    } else {
      window.addEventListener('resize', resize);
    }

    var mo = null;
    if ('MutationObserver' in window) {
      mo = new MutationObserver(function() {
        resolveThemeColor();
        if (isAnimPaused() && animating) {
          ctx.clearRect(0, 0, cssW, cssH);
          trail = [];
          animating = false;
          if (rafId) cancelAnimationFrame(rafId);
        }
      });
      mo.observe(document.documentElement, { attributes: true, attributeFilter: ['class', 'data-theme'] });
    }

    function cleanup() {
      if (rafId) cancelAnimationFrame(rafId);
      if (ro) ro.disconnect();
      if (mo) mo.disconnect();
      host.removeEventListener('mousemove', onMouseMove);
      host.removeEventListener('mouseleave', onMouseLeave);
      window.removeEventListener('pagehide', cleanup);
    }
    window.addEventListener('pagehide', cleanup);

    resize();
  }

  function init() {
    var hosts = document.querySelectorAll('[data-grid-trail]');
    for (var i = 0; i < hosts.length; i++) {
      initGridTrail(hosts[i]);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
