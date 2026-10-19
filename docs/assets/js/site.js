/* Gautam Reddy portfolio — small, dependency-free.
   Features: theme toggle, mobile menu, reveal-on-scroll (IntersectionObserver),
   project filter/search, enquiry form -> mailto draft. No scroll listeners, no rAF loops. */
(function () {
  "use strict";
  var doc = document.documentElement;
  var EMAIL = "reddygautam98@gmail.com";

  function safeGet(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function safeSet(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

  /* ---- theme ---- */
  var themeBtn = document.getElementById("theme-toggle");
  function currentTheme() { return doc.getAttribute("data-theme") === "dark" ? "dark" : "light"; }
  function syncThemeBtn() {
    if (!themeBtn) return;
    var dark = currentTheme() === "dark";
    themeBtn.setAttribute("aria-label", dark ? "Switch to light theme" : "Switch to dark theme");
    themeBtn.setAttribute("aria-pressed", dark ? "true" : "false");
  }
  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      var next = currentTheme() === "dark" ? "light" : "dark";
      doc.setAttribute("data-theme", next);
      safeSet("gr-theme", next);
      syncThemeBtn();
    });
    syncThemeBtn();
  }

  /* ---- mobile menu ---- */
  var menuBtn = document.getElementById("menu-toggle");
  var nav = document.getElementById("site-nav");
  if (menuBtn && nav) {
    function setMenu(open) {
      nav.classList.toggle("open", open);
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    }
    menuBtn.addEventListener("click", function () { setMenu(!nav.classList.contains("open")); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") setMenu(false); });
    nav.addEventListener("click", function (e) { if (e.target.tagName === "A") setMenu(false); });
  }

  /* ---- reveal on scroll ---- */
  var items = document.querySelectorAll(".reveal");
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (items.length) {
    if (!("IntersectionObserver" in window) || reduce) {
      items.forEach(function (el) { el.classList.add("in"); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
        });
      }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });
      items.forEach(function (el) { io.observe(el); });
    }
  }

  /* ---- projects filter + search ---- */
  var list = document.getElementById("project-list");
  if (list) {
    var cards = Array.prototype.slice.call(list.querySelectorAll("[data-cat]"));
    var chips = document.querySelectorAll(".chip[data-filter]");
    var q = document.getElementById("project-search");
    var count = document.getElementById("project-count");
    var empty = document.getElementById("project-empty");
    var cat = "all";
    function apply() {
      var term = q ? q.value.trim().toLowerCase() : "";
      var shown = 0;
      cards.forEach(function (c) {
        var okCat = cat === "all" || c.getAttribute("data-cat") === cat;
        var okTerm = !term || c.textContent.toLowerCase().indexOf(term) > -1;
        var show = okCat && okTerm;
        c.hidden = !show;
        if (show) shown++;
      });
      if (count) count.textContent = shown + (shown === 1 ? " project" : " projects");
      if (empty) empty.hidden = shown !== 0;
    }
    chips.forEach(function (ch) {
      ch.addEventListener("click", function () {
        cat = ch.getAttribute("data-filter");
        chips.forEach(function (o) { o.setAttribute("aria-pressed", o === ch ? "true" : "false"); });
        apply();
      });
    });
    if (q) q.addEventListener("input", apply);
    apply();
  }

  /* ---- enquiry form -> mailto draft ---- */
  var form = document.getElementById("enquiry-form");
  if (form) {
    var status = document.getElementById("form-status");
    function field(n) { return form.elements[n]; }
    function setErr(el, msg) {
      var out = document.getElementById(el.name + "-err");
      el.setAttribute("aria-invalid", msg ? "true" : "false");
      if (out) out.textContent = msg || "";
    }
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = true, first = null;
      ["name", "email", "service", "message"].forEach(function (n) {
        var el = field(n), v = (el.value || "").trim(), msg = "";
        if (!v) msg = "This field is required.";
        else if (n === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) msg = "Enter a valid email address.";
        else if (n === "message" && v.length < 20) msg = "Please add a little more detail (20+ characters).";
        setErr(el, msg);
        if (msg) { ok = false; if (!first) first = el; }
      });
      if (!ok) { if (first) first.focus(); if (status) status.textContent = "Please fix the highlighted fields."; return; }
      var svc = field("service").value;
      var body = [
        "Name: " + field("name").value.trim(),
        "Email: " + field("email").value.trim(),
        "Company: " + (field("company").value.trim() || "-"),
        "Service: " + svc,
        "Engagement: " + field("engagement").value,
        "Timeline: " + field("timeline").value,
        "Reference: " + (field("link").value.trim() || "-"),
        "",
        field("message").value.trim()
      ].join("\n");
      var href = "mailto:" + EMAIL + "?subject=" + encodeURIComponent("Enquiry: " + svc) + "&body=" + encodeURIComponent(body);
      if (status) status.textContent = "Opening your email app with a draft. Nothing is sent until you press Send.";
      window.location.href = href;
    });
  }

  /* ---- copy email ---- */
  document.querySelectorAll("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () {
      var t = b.getAttribute("data-copy"), label = b.textContent;
      function done() { b.textContent = "Copied"; setTimeout(function () { b.textContent = label; }, 1500); }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(t).then(done, function () {});
    });
  });

  /* ---- footer year ---- */
  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();
})();
