/**
 * GautamTheAnalyst.io - Interactive 3D Card Dynamics, Border Beam & Cinematic Focus Blur
 * Inspired by Lightswind Glowing Cards, 3D Perspective Card & Border Beam.
 * Adds tactile 3D perspective tilt, cursor spotlight, and depth-of-field focus blur.
 */
(function() {
  'use strict';

  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) return;

  function isPaused() {
    return document.documentElement.classList.contains('is-anim-paused');
  }

  var selector = [
    '.card',
    '.scard',
    '.pcard',
    '.step-card',
    '.peek-card',
    '.kit',
    '.rbody',
    '.role',
    '.tk-tile',
    '.form-card',
    '.contact-rail',
    '.contact-fallback-card',
    '.resume-side-card',
    '.what-card',
    '.principle-card',
    '.about-console',
    '.impact-card',
    '.sh-item',
    '.proof-card',
    '.proof > div',
    '.file-list li',
    '.file-item',
    '.notfound-links-card',
    '.feature',
    '.featured-paytrack',
    '.hero-slider',
    '.term-card',
    '.schema-preview',
    '.wf-kpi-card',
    '.us-story-card',
    '.faq details',
    '.faq-item',
    '.mini-stat',
    '.hfs-item',
    '.cta-panel',
    '.magic-card'
  ].join(', ');

  function clearAllActiveCards() {
    document.querySelectorAll('.is-focused-card').forEach(function(el) {
      el.classList.remove('is-focused-card');
    });
    document.querySelectorAll('.has-card-focused').forEach(function(sec) {
      sec.classList.remove('has-card-focused');
    });
    document.body.classList.remove('has-card-focused-mode');
  }

  function initCards() {
    var cards = document.querySelectorAll(selector);

    cards.forEach(function(card) {
      var raf = null;
      var rect = null;

      // Desktop 3D Tilt & Specular Spotlight
      if (fine) {
        function onPointerEnter() {
          if (isPaused()) return;
          rect = card.getBoundingClientRect();
        }

        function onPointerMove(e) {
          if (isPaused()) return;
          if (raf) return;

          raf = requestAnimationFrame(function() {
            raf = null;
            if (!rect) rect = card.getBoundingClientRect();
            var x = e.clientX - rect.left;
            var y = e.clientY - rect.top;

            // Spotlight coordinates
            card.style.setProperty('--mx', x + 'px');
            card.style.setProperty('--my', y + 'px');

            // Subtle 3D tilt angles (max ~5 degrees for professional stability)
            var px = (x / rect.width) - 0.5;
            var py = (y / rect.height) - 0.5;
            var tiltX = (-py * 7).toFixed(2);
            var tiltY = (px * 7).toFixed(2);

            card.style.transform = 'perspective(900px) rotateX(' + tiltX + 'deg) rotateY(' + tiltY + 'deg) translateY(-4px)';
          });
        }

        function onPointerLeave() {
          if (raf) {
            cancelAnimationFrame(raf);
            raf = null;
          }
          rect = null;
          card.style.transform = '';
        }

        card.addEventListener('pointerenter', onPointerEnter, { passive: true });
        card.addEventListener('pointermove', onPointerMove, { passive: true });
        card.addEventListener('pointerleave', onPointerLeave, { passive: true });
      }

      // Touch & Click Focus Interaction ("when I touch a card it blurs other sections")
      card.addEventListener('click', function(e) {
        if (isPaused()) return;
        // If clicking a direct interactive button, link, input, select, textarea, summary, allow navigation/toggle without blocking
        if (e.target.closest('a[href], button, input, textarea, select, summary')) return;

        var isAlreadyFocused = card.classList.contains('is-focused-card');
        clearAllActiveCards();

        if (!isAlreadyFocused) {
          card.classList.add('is-focused-card');
          var sec = card.closest('.sec, section, .wrap, main');
          if (sec) sec.classList.add('has-card-focused');
          document.body.classList.add('has-card-focused-mode');
        }
      });
    });

    // Dismiss focus blur when tapping outside or pressing Escape
    document.addEventListener('pointerdown', function(e) {
      if (!e.target.closest(selector)) {
        clearAllActiveCards();
      }
    }, { passive: true });

    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        clearAllActiveCards();
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCards);
  } else {
    initCards();
  }
})();
