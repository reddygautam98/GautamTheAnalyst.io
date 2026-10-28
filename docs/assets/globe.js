/**
 * Interactive 3D Dotted Globe (Cobe WebGL Implementation)
 * Features:
 * - Dotted 3D orthographic projection of continents & location beacons
 * - Pointer / mouse / touch drag-to-rotate with inertia damping
 * - Scroll-wheel zoom in / out with clamping
 * - Bengaluru, India location marker (12.97° N, 77.59° E) & global remote hubs
 * - Reset view button (⟲) centering back to Bengaluru focus
 * - Dynamic Light / Dark mode theme synchronization
 * - Pauses rendering when scrolled off-screen (IntersectionObserver)
 * - Respects prefers-reduced-motion and site-wide animation toggle
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
  // In radians: 77.5946° ≈ 1.354 rad
  var BENGALURU_PHI = 1.35;
  var BENGALURU_THETA = 0.25;

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
  var motionPaused = false;
  var globeInstance = null;

  // Markers: Bengaluru primary beacon + key global remote collaboration hubs
  var MARKERS = [
    { location: [12.9716, 77.5946], size: 0.12 }, // Bengaluru, India (Primary)
    { location: [51.5074, -0.1278], size: 0.05 }, // London / EMEA
    { location: [40.7128, -74.0060], size: 0.05 }, // New York / US East
    { location: [37.7749, -122.4194], size: 0.04 }, // San Francisco / US West
    { location: [1.3521, 103.8198], size: 0.05 }   // Singapore / APAC
  ];

  function getThemeColors() {
    var isDark = document.documentElement.dataset.theme === 'dark';
    if (isDark) {
      return {
        dark: 1,
        baseColor: [0.35, 0.45, 0.6],
        markerColor: [0.1, 0.8, 1],
        glowColor: [0.25, 0.45, 0.85],
        mapBaseBrightness: 0.05,
        mapBrightness: 6
      };
    } else {
      return {
        dark: 0,
        baseColor: [0.85, 0.9, 0.96],
        markerColor: [0.08, 0.45, 0.95],
        glowColor: [0.92, 0.94, 0.98],
        mapBaseBrightness: 0.08,
        mapBrightness: 8
      };
    }
  }

  function initGlobe() {
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
        if (!isVisible) return;

        var colors = getThemeColors();
        state.dark = colors.dark;
        state.baseColor = colors.baseColor;
        state.markerColor = colors.markerColor;
        state.glowColor = colors.glowColor;
        state.mapBrightness = colors.mapBrightness;
        state.mapBaseBrightness = colors.mapBaseBrightness;

        // Auto-rotation when not interacting and motion is not paused
        if (!pointerInteracting && !isMotionPaused()) {
          targetPhi += 0.003;
        }

        // Smooth damping towards target coordinates & zoom scale
        phi += (targetPhi - phi) * 0.08;
        theta += (targetTheta - theta) * 0.08;
        scale += (targetScale - scale) * 0.1;

        state.phi = phi;
        state.theta = theta;
        state.scale = scale;
        state.width = canvas.width;
        state.height = canvas.height;
      }
    });
  }

  // Pointer interactions (mouse and touch drag)
  canvas.addEventListener('pointerdown', function(e) {
    pointerInteracting = true;
    pointerStartX = e.clientX;
    pointerStartY = e.clientY;
    phiStart = targetPhi;
    thetaStart = targetTheta;
    canvas.setPointerCapture(e.pointerId);
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
  });

  function stopPointer(e) {
    if (pointerInteracting) {
      pointerInteracting = false;
      try {
        canvas.releasePointerCapture(e.pointerId);
      } catch (err) {}
      globeCard.classList.remove('is-dragging');
    }
  }

  canvas.addEventListener('pointerup', stopPointer);
  canvas.addEventListener('pointercancel', stopPointer);

  // Wheel zoom with clamping
  globeCard.addEventListener('wheel', function(e) {
    // Only capture zoom if hovering canvas directly
    if (e.target === canvas) {
      e.preventDefault();
      var zoomDelta = e.deltaY * -0.0015;
      targetScale = Math.max(0.85, Math.min(1.35, targetScale + zoomDelta));
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
    });
  }

  // Reduced motion preference & manual pause toggle
  var mql = window.matchMedia('(prefers-reduced-motion: reduce)');
  motionPaused = mql.matches;
  mql.addEventListener('change', function(e) {
    motionPaused = e.matches;
  });

  function isMotionPaused() {
    return motionPaused || document.documentElement.classList.contains('is-anim-paused');
  }

  var animBtn = document.getElementById('animToggle');
  if (animBtn) {
    animBtn.addEventListener('click', function() {
      motionPaused = document.documentElement.classList.contains('is-anim-paused');
    });
  }

  // IntersectionObserver: pause rendering offscreen
  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        isVisible = entry.isIntersecting;
      });
    }, { threshold: 0.05 });
    observer.observe(globeCard);
  }

  // Handle window resizing
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
          try {
            globeInstance.resize();
          } catch (e) {}
        }
      }
    }, 150);
  });

  // Initialize
  initGlobe();
})();
