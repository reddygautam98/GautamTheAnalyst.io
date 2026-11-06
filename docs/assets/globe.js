/**
 * Interactive 3D Dotted Globe (Cobe WebGL Implementation)
 * Features:
 * - Dotted 3D orthographic projection of continents & location beacons
 * - Pointer / mouse / touch drag-to-rotate with frame-rate independent inertia damping
 * - Scroll-wheel zoom in / out with clamping
 * - Bengaluru, India location marker (12.97° N, 77.59° E) centered on load (cobe convention: phi = 3.358 rad, theta = 0.23 rad)
 * - Reset view button centering back to Bengaluru focus
 * - Dynamic Light / Dark mode theme token synchronization (via getComputedStyle)
 * - Seamless dark base matching --bg (#0b0f19) to eliminate canvas boundary artifacts
 * - Single shouldRun() gating loop for offscreen, document.hidden, prefers-reduced-motion, and site-motion-toggle
 * - Guaranteed single rafId tracking, cancellation on pause, and resume without duplicate scheduling
 * - WebGL context lost & restored handlers and static fallback resilience
 */
import createGlobe from './cobe.js';

(function() {
  'use strict';

  var globeCard = document.getElementById('globeCard');
  var canvas = document.getElementById('globeCanvas');
  var resetBtn = document.getElementById('globeResetBtn');
  if (!globeCard || !canvas) return;

  var dpr = Math.min(window.devicePixelRatio || 1, 2);
  var width = canvas.clientWidth || 320;
  var height = canvas.clientHeight || 320;

  // Set internal canvas resolution
  canvas.width = width * dpr;
  canvas.height = height * dpr;

  // Bengaluru coordinates: 12.9716° N, 77.5946° E
  // In cobe convention:
  // phi = atan2(-cos(lon), -sin(lon)) = -lon_rad - pi/2 ≈ -2.925 rad or +3.358 rad
  // theta = lat_rad ≈ 0.23 rad
  var BENGALURU_PHI = 3.358;
  var BENGALURU_THETA = 0.23;

  var phi = BENGALURU_PHI;
  var theta = BENGALURU_THETA;
  var targetPhi = BENGALURU_PHI;
  var targetTheta = BENGALURU_THETA;
  var scale = 1.0;
  var targetScale = 1.0;

  var pointerInteracting = false;
  var pointerStartX = 0;
  var pointerStartY = 0;
  var phiStart = 0;
  var thetaStart = 0;
  var isVisible = true;
  var globeInstance = null;
  var rafId = null;
  var lastTime = 0;

  // Markers: Bengaluru primary beacon + key global remote collaboration hubs
  var MARKERS = [
    { location: [12.9716, 77.5946], size: 0.12 }, // Bengaluru, India (Primary)
    { location: [51.5074, -0.1278], size: 0.05 }, // London / EMEA
    { location: [40.7128, -74.0060], size: 0.05 }, // New York / US East
    { location: [37.7749, -122.4194], size: 0.04 }, // San Francisco / US West
    { location: [1.3521, 103.8198], size: 0.05 }   // Singapore / APAC
  ];

  function parseRgb01(str) {
    if (!str) return null;
    str = str.trim();
    if (str.indexOf('#') === 0) {
      var hex = str.slice(1);
      if (hex.length === 3) hex = hex.split('').map(function(c) { return c + c; }).join('');
      if (hex.length === 6) {
        var num = parseInt(hex, 16);
        return [((num >> 16) & 255) / 255, ((num >> 8) & 255) / 255, (num & 255) / 255];
      }
    }
    var m = str.match(/rgba?\((\d+)\s*,\s*(\d+)\s*,\s*(\d+)/i);
    if (m) {
      return [parseInt(m[1], 10) / 255, parseInt(m[2], 10) / 255, parseInt(m[3], 10) / 255];
    }
    return null;
  }

  function getThemeColors() {
    var isDark = document.documentElement.dataset.theme === 'dark';
    var cs = window.getComputedStyle(document.documentElement);
    var bgCol = parseRgb01(cs.getPropertyValue('--bg')) || (isDark ? [11/255, 15/255, 25/255] : [248/255, 250/255, 252/255]);
    var accentCol = parseRgb01(cs.getPropertyValue('--accent')) || (isDark ? [59/255, 130/255, 246/255] : [37/255, 99/255, 235/255]);
    var accent2Col = parseRgb01(cs.getPropertyValue('--accent-2')) || (isDark ? [56/255, 189/255, 248/255] : [3/255, 105/255, 161/255]);

    var softCol = parseRgb01(cs.getPropertyValue('--soft')) || (isDark ? [22/255, 32/255, 54/255] : [241/255, 245/255, 249/255]);
    var lineCol = parseRgb01(cs.getPropertyValue('--line')) || (isDark ? [30/255, 41/255, 59/255] : [226/255, 232/255, 240/255]);

    if (isDark) {
      return {
        dark: 1,
        baseColor: bgCol, // Seamless dark base matching --bg (#0b0f19)
        markerColor: accent2Col, // Sky 400 (#38bdf8)
        glowColor: accentCol, // Blue 500 (#3b82f6)
        mapBaseBrightness: 0.05,
        mapBrightness: 6
      };
    } else {
      return {
        dark: 0,
        baseColor: [
          bgCol[0] * 0.85 + softCol[0] * 0.15,
          bgCol[1] * 0.88 + softCol[1] * 0.12,
          bgCol[2] * 0.95 + softCol[2] * 0.05
        ],
        markerColor: accentCol, // Blue 600 (#2563eb)
        glowColor: [
          bgCol[0] * 0.95 + softCol[0] * 0.05,
          bgCol[1] * 0.95 + softCol[1] * 0.05,
          bgCol[2] * 0.98 + softCol[2] * 0.02
        ],
        mapBaseBrightness: 0.08,
        mapBrightness: 8
      };
    }
  }

  function isReducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function isAnimPaused() {
    return document.documentElement.classList.contains('is-anim-paused');
  }

  function shouldRun() {
    return isVisible && !document.hidden && !isReducedMotion() && !isAnimPaused();
  }

  function showFallback() {
    var wrap = globeCard.querySelector('.globe-canvas-wrap');
    if (wrap && !wrap.querySelector('.globe-fallback')) {
      canvas.style.display = 'none';
      var fb = document.createElement('div');
      fb.className = 'globe-fallback';
      fb.setAttribute('role', 'img');
      fb.setAttribute('aria-label', 'Static globe map highlighting Bengaluru, India (UTC+5:30)');
      fb.innerHTML = '<div class="globe-fallback-art"></div>';
      wrap.appendChild(fb);
    }
  }

  function initGlobe() {
    try {
      var colors = getThemeColors();

      globeInstance = createGlobe(canvas, {
        devicePixelRatio: dpr,
        width: canvas.width,
        height: canvas.height,
        phi: phi,
        theta: theta,
        dark: colors.dark,
        diffuse: 1.2,
        mapSamples: 16000,
        mapBrightness: colors.mapBrightness,
        mapBaseBrightness: colors.mapBaseBrightness,
        baseColor: colors.baseColor,
        markerColor: colors.markerColor,
        glowColor: colors.glowColor,
        markers: MARKERS,
        scale: scale,
        onRender: function(state) {
          var c = getThemeColors();
          state.dark = c.dark;
          state.baseColor = c.baseColor;
          state.markerColor = c.markerColor;
          state.glowColor = c.glowColor;
          state.mapBrightness = c.mapBrightness;
          state.mapBaseBrightness = c.mapBaseBrightness;
          state.phi = phi;
          state.theta = theta;
          state.scale = scale;
          state.width = canvas.width;
          state.height = canvas.height;
        }
      });

      // Stop cobe internal infinite loop so globe.js controls every frame
      if (globeInstance && typeof globeInstance.toggle === 'function') {
        globeInstance.toggle(false);
      }
    } catch (err) {
      console.warn('Globe WebGL initialization failed; showing fallback.', err);
      showFallback();
    }
  }

  function renderFrame(dt) {
    if (!globeInstance) return;

    if (!pointerInteracting && !isReducedMotion() && !isAnimPaused()) {
      targetPhi += 0.003;
    }

    // Frame-rate-independent damping: k ≈ 5.0 matches 0.08 damping at 60 Hz
    var factor = 1 - Math.exp(-5.0 * dt);
    phi += (targetPhi - phi) * factor;
    theta += (targetTheta - theta) * factor;
    scale += (targetScale - scale) * factor;

    try {
      globeInstance.render();
    } catch (_) {}
  }

  function loop(timestamp) {
    if (!shouldRun()) {
      if (rafId) {
        cancelAnimationFrame(rafId);
        rafId = null;
      }
      return;
    }
    rafId = null;

    var now = timestamp || performance.now();
    var dt = lastTime ? Math.min((now - lastTime) / 1000, 0.05) : 1 / 60;
    lastTime = now;

    renderFrame(dt);

    if (shouldRun() && !rafId) {
      rafId = requestAnimationFrame(loop);
    }
  }

  function checkState() {
    if (shouldRun()) {
      if (!rafId) {
        lastTime = performance.now();
        rafId = requestAnimationFrame(loop);
      }
    } else {
      if (rafId) {
        cancelAnimationFrame(rafId);
        rafId = null;
      }
      // When paused or reduced motion, render one static frame
      if (isVisible && globeInstance) {
        renderFrame(1 / 60);
      }
    }
  }

  // Pointer interactions (mouse and touch drag)
  canvas.addEventListener('pointerdown', function(e) {
    pointerInteracting = true;
    pointerStartX = e.clientX;
    pointerStartY = e.clientY;
    phiStart = targetPhi;
    thetaStart = targetTheta;
    try { canvas.setPointerCapture(e.pointerId); } catch (_) {}
    globeCard.classList.add('is-dragging');
  });

  canvas.addEventListener('pointermove', function(e) {
    if (!pointerInteracting) return;
    var deltaX = e.clientX - pointerStartX;
    var deltaY = e.clientY - pointerStartY;

    // Horizontal drag controls rotation (phi)
    targetPhi = phiStart + deltaX * 0.005;

    // Vertical drag controls tilt (theta) clamped to reasonable bounds
    targetTheta = Math.max(-0.4, Math.min(0.6, thetaStart - deltaY * 0.004));

    if (!rafId && isVisible) {
      renderFrame(1 / 60);
    }
  });

  function stopPointer(e) {
    if (pointerInteracting) {
      pointerInteracting = false;
      try { canvas.releasePointerCapture(e.pointerId); } catch (_) {}
      globeCard.classList.remove('is-dragging');
    }
  }

  canvas.addEventListener('pointerup', stopPointer);
  canvas.addEventListener('pointercancel', stopPointer);

  // Wheel zoom with clamping
  globeCard.addEventListener('wheel', function(e) {
    if (e.target === canvas) {
      e.preventDefault();
      var zoomDelta = e.deltaY * -0.0015;
      targetScale = Math.max(0.85, Math.min(1.35, targetScale + zoomDelta));
      if (!rafId && isVisible) {
        renderFrame(1 / 60);
      }
    }
  }, { passive: false });

  // Reset button: smooth pan back to Bengaluru
  if (resetBtn) {
    resetBtn.addEventListener('click', function() {
      targetPhi = BENGALURU_PHI;
      targetTheta = BENGALURU_THETA;
      targetScale = 1.0;
      resetBtn.classList.add('is-active');
      setTimeout(function() {
        resetBtn.classList.remove('is-active');
      }, 400);
      checkState();
    });
  }

  // Reduced motion preference & dynamic OS updates
  var mql = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (mql && mql.addEventListener) {
    mql.addEventListener('change', checkState);
  }

  // Listen for global site-motion-toggle event
  window.addEventListener('site-motion-toggle', checkState);
  document.addEventListener('visibilitychange', checkState);

  // Sync theme changes with MutationObserver on data-theme
  var themeObserver = new MutationObserver(function() {
    if (globeInstance) {
      renderFrame(1 / 60);
    }
  });
  themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme', 'class'] });

  // WebGL context lost & restored resilience
  canvas.addEventListener('webglcontextlost', function(e) {
    e.preventDefault();
    if (rafId) {
      cancelAnimationFrame(rafId);
      rafId = null;
    }
  });
  canvas.addEventListener('webglcontextrestored', function() {
    initGlobe();
    checkState();
  });

  // IntersectionObserver: pause rendering offscreen
  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        isVisible = entry.isIntersecting;
        checkState();
      });
    }, { threshold: 0.05 });
    observer.observe(globeCard);
  } else {
    isVisible = true;
    checkState();
  }

  // Window resize handler
  var resizeTimer;
  window.addEventListener('resize', function() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function() {
      var newW = canvas.clientWidth;
      var newH = canvas.clientHeight;
      if (newW && newH && globeInstance) {
        canvas.width = newW * dpr;
        canvas.height = newH * dpr;
        if (typeof globeInstance.resize === 'function') {
          try { globeInstance.resize(); } catch (_) {}
        }
        renderFrame(1 / 60);
      }
    }, 150);
  });

  window.addEventListener('pagehide', function() {
    if (rafId) {
      cancelAnimationFrame(rafId);
      rafId = null;
    }
    if (themeObserver) themeObserver.disconnect();
    if (observer) observer.disconnect();
  });

  // Expose rafId state checker for verification/tests
  window._getGlobeRafId = function() { return rafId; };

  // Initialize
  initGlobe();
  checkState();
})();
