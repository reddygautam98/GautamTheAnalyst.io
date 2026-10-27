/**
 * ASCII Wave (Vanilla JS Reimplementation)
 * Inspired by Lightswind ASCII Wave design reference.
 * Text-based animation using ASCII characters on HTML Canvas.
 * Dependency-free, respects reduced-motion, pauses offscreen / when motion is paused.
 */
(function() {
  'use strict';

  var RAMP = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@'];
  var CELL_W = 12;
  var CELL_H = 18;
  var MAX_DPR = 2;
  var MAX_WIDTH = 1600;
  var MAX_HEIGHT = 700;
  var TARGET_FPS = 30;
  var FRAME_INTERVAL = 1000 / TARGET_FPS;

  function parseColor(str) {
    if (!str) return null;
    str = str.trim();
    if (str.indexOf('#') === 0) {
      var hex = str.slice(1);
      if (hex.length === 3) hex = hex.split('').map(function(c) { return c + c; }).join('');
      if (hex.length === 6) {
        var num = parseInt(hex, 16);
        return { r: (num >> 16) & 255, g: (num >> 8) & 255, b: num & 255 };
      }
    }
    var rgbMatch = str.match(/rgba?\((\d+)\s*,\s*(\d+)\s*,\s*(\d+)/i);
    if (rgbMatch) {
      return { r: parseInt(rgbMatch[1], 10), g: parseInt(rgbMatch[2], 10), b: parseInt(rgbMatch[3], 10) };
    }
    return null;
  }

  function initWave(host) {
    var canvas = host.querySelector('canvas');
    if (!canvas) {
      canvas = document.createElement('canvas');
      host.appendChild(canvas);
    }
    var ctx = canvas.getContext('2d');
    if (!ctx) return;

    var speed = parseFloat(host.getAttribute('data-speed') || '1') || 1;
    var customColor = host.getAttribute('data-color');
    var isVisible = false;
    var rafId = null;
    var lastTimestamp = 0;
    var time = 0;
    var cssW = 0;
    var cssH = 0;
    var dpr = 1;
    var baseColor = { r: 56, g: 189, b: 248 };

    function resolveColor() {
      if (customColor) {
        var parsed = parseColor(customColor);
        if (parsed) { baseColor = parsed; return; }
      }
      try {
        var style = window.getComputedStyle(host);
        var parsedFromStyle = parseColor(style.color);
        if (parsedFromStyle) baseColor = parsedFromStyle;
      } catch (_) {}
    }

    function isReducedMotion() {
      return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    }

    function isAnimPaused() {
      return document.documentElement.classList.contains('is-anim-paused');
    }

    function shouldAnimate() {
      return isVisible && !document.hidden && !isReducedMotion() && !isAnimPaused();
    }

    function resize() {
      var rect = host.getBoundingClientRect();
      var rawW = rect.width || 300;
      var rawH = rect.height || 200;

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
      resolveColor();
    }

    function drawFrame(t) {
      if (!ctx || cssW <= 0 || cssH <= 0) return;

      ctx.save();
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, cssW, cssH);

      ctx.font = '12px "IBM Plex Mono", monospace';
      ctx.textBaseline = 'top';

      var cols = Math.ceil(cssW / CELL_W);
      var rows = Math.ceil(cssH / CELL_H);

      // Batch glyphs by ramp index to minimise fillStyle state changes
      var buckets = [];
      for (var b = 0; b < RAMP.length; b++) buckets.push([]);

      for (var r = 0; r < rows; r++) {
        var y = r * CELL_H;
        for (var c = 0; c < cols; c++) {
          var x = c * CELL_W;
          // Sum-of-sines field simulation
          var v1 = Math.sin(c * 0.12 + t * 1.3);
          var v2 = Math.cos(r * 0.16 - t * 0.95);
          var v3 = Math.sin((c + r) * 0.08 + t * 0.5);
          var norm = (v1 + v2 + v3 + 3) / 6; // 0 .. 1

          if (norm < 0.22) continue; // Sparse background spaces

          var rampIdx = Math.floor(((norm - 0.22) / 0.78) * (RAMP.length - 1));
          if (rampIdx < 1) continue;
          if (rampIdx >= RAMP.length) rampIdx = RAMP.length - 1;

          buckets[rampIdx].push(x, y);
        }
      }

      // Draw batched glyphs
      var rampLen = RAMP.length;
      for (var i = 1; i < rampLen; i++) {
        var coords = buckets[i];
        if (!coords.length) continue;

        // Max alpha capped around ~0.28 to keep foreground text readable
        var alpha = (0.07 + (i / rampLen) * 0.21).toFixed(3);
        ctx.fillStyle = 'rgba(' + baseColor.r + ',' + baseColor.g + ',' + baseColor.b + ',' + alpha + ')';
        var char = RAMP[i];

        for (var k = 0; k < coords.length; k += 2) {
          ctx.fillText(char, coords[k], coords[k + 1]);
        }
      }

      ctx.restore();
    }

    function tick(timestamp) {
      if (!shouldAnimate()) {
        rafId = null;
        return;
      }

      var delta = timestamp - lastTimestamp;
      if (delta >= FRAME_INTERVAL) {
        lastTimestamp = timestamp - (delta % FRAME_INTERVAL);
        time += 0.045 * speed;
        drawFrame(time);
      }
      rafId = requestAnimationFrame(tick);
    }

    function checkState() {
      if (shouldAnimate()) {
        if (!rafId) {
          lastTimestamp = performance.now();
          rafId = requestAnimationFrame(tick);
        }
      } else {
        if (rafId) {
          cancelAnimationFrame(rafId);
          rafId = null;
        }
        // When motion is paused or reduced, draw one static frame
        if (isVisible) {
          drawFrame(time || 1.0);
        }
      }
    }

    var ro = null;
    if ('ResizeObserver' in window) {
      ro = new ResizeObserver(function() {
        resize();
        if (isVisible) drawFrame(time);
      });
      ro.observe(host);
    } else {
      window.addEventListener('resize', function() {
        resize();
        if (isVisible) drawFrame(time);
      });
    }

    var io = null;
    if ('IntersectionObserver' in window) {
      io = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          isVisible = entry.isIntersecting;
          checkState();
        });
      }, { threshold: 0.05 });
      io.observe(host);
    } else {
      isVisible = true;
      checkState();
    }

    function onVisibilityChange() {
      checkState();
    }
    document.addEventListener('visibilitychange', onVisibilityChange);

    var mo = null;
    if ('MutationObserver' in window) {
      mo = new MutationObserver(function() {
        checkState();
      });
      mo.observe(document.documentElement, { attributes: true, attributeFilter: ['class', 'data-theme'] });
    }

    function cleanup() {
      if (rafId) cancelAnimationFrame(rafId);
      if (io) io.disconnect();
      if (ro) ro.disconnect();
      if (mo) mo.disconnect();
      document.removeEventListener('visibilitychange', onVisibilityChange);
      window.removeEventListener('pagehide', cleanup);
    }
    window.addEventListener('pagehide', cleanup);

    resize();
    drawFrame(1.0);
    checkState();
  }

  function init() {
    var hosts = document.querySelectorAll('[data-ascii-wave]');
    for (var i = 0; i < hosts.length; i++) {
      initWave(hosts[i]);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
