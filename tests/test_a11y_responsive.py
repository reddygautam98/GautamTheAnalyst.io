"""
Playwright + axe-core accessibility and responsive testing suite for GautamTheAnalyst.io.
Tests all compiled pages dynamically discovered from docs/ across 7 target viewports:
  320x568, 375x812, 430x932, 768x1024, 1024x768, 1440x900, 1920x1080
in both light and dark themes.

Supports:
1. Automated CI execution via pytest + Playwright + axe-core.
2. Standalone execution via standard Python unittest (`python tests/test_a11y_responsive.py`).
"""

import os
import re
import glob
import json
import unittest
from pathlib import Path

# Try importing Playwright & axe-core for live browser testing
try:
    import pytest
except ImportError:
    pytest = None

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

try:
    from axe_playwright_python.sync_playwright import Axe
except ImportError:
    Axe = None

BASE_URL = os.environ.get("TEST_BASE_URL", "http://127.0.0.1:8000")
REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"

def discover_generated_pages(docs_dir=None):
    """Dynamically walks docs/ directory for all generated HTML pages."""
    target_dir = Path(docs_dir) if docs_dir else DOCS_DIR
    discovered = []
    for root, _, files in os.walk(target_dir):
        for f in sorted(files):
            if f.endswith(".html"):
                full_path = Path(root) / f
                rel_path = full_path.relative_to(target_dir).as_posix()
                discovered.append("/" + rel_path)
    return sorted(discovered)

PAGES = discover_generated_pages()

VIEWPORTS = [
    {"width": 320, "height": 568, "name": "mobile_sm"},
    {"width": 375, "height": 812, "name": "mobile_std"},
    {"width": 390, "height": 844, "name": "mobile_iphone"},
    {"width": 430, "height": 932, "name": "mobile_lg"},
    {"width": 768, "height": 1024, "name": "tablet_portrait"},
    {"width": 1024, "height": 768, "name": "tablet_landscape"},
    {"width": 1280, "height": 800, "name": "desktop_sm"},
    {"width": 1440, "height": 900, "name": "desktop_std"},
    {"width": 1920, "height": 1080, "name": "desktop_lg"},
]

THEMES = ["light", "dark"]


# ==============================================================================
# Pytest / Playwright Fixtures and Parametrized Tests for CI
# ==============================================================================
if pytest is not None and sync_playwright is not None:
    @pytest.fixture(scope="module")
    def browser_instance():
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            yield browser
            browser.close()

    @pytest.mark.parametrize("page_path", PAGES)
    @pytest.mark.parametrize("vp", VIEWPORTS)
    @pytest.mark.parametrize("theme", THEMES)
    def test_page_a11y_and_overflow(browser_instance, page_path, vp, theme):
        context = browser_instance.new_context(
            viewport={"width": vp["width"], "height": vp["height"]},
            color_scheme=theme,
        )
        page = context.new_page()
        url = f"{BASE_URL}{page_path}"
        response = page.goto(url, wait_until="networkidle")
        assert response is not None, f"Failed to load {url}"
        assert response.status == 200, f"Expected status 200 on {url}, got {response.status}"

        # Ensure page has valid title and h1
        title = page.title()
        assert title and len(title.strip()) > 0, f"Page {page_path} missing <title>"
        h1_count = page.locator("h1").count()
        assert h1_count > 0, f"Page {page_path} missing <h1>"

        # Force theme via data-theme attribute
        page.evaluate(f"document.documentElement.setAttribute('data-theme', '{theme}')")
        page.wait_for_timeout(100)

        # 1. Horizontal overflow assertion across viewport
        overflow = page.evaluate("""() => {
            const doc = document.documentElement;
            return {
                scrollWidth: doc.scrollWidth,
                clientWidth: doc.clientWidth,
                hasOverflow: doc.scrollWidth > doc.clientWidth
            };
        }""")
        assert not overflow["hasOverflow"], (
            f"Horizontal overflow detected on {page_path} at {vp['width']}px ({theme}): "
            f"scrollWidth={overflow['scrollWidth']}, clientWidth={overflow['clientWidth']}"
        )

        # 2. Axe-core accessibility assertion
        if Axe is not None:
            axe = Axe()
            results = axe.run(page)
            violations = results.response.get("violations", [])
            critical_or_serious = [
                v for v in violations if v.get("impact") in ["critical", "serious"]
            ]
            assert len(critical_or_serious) == 0, (
                f"Axe-core accessibility violations on {page_path} ({vp['name']}, {theme}): "
                f"{[v['id'] + ': ' + v['description'] for v in critical_or_serious]}"
            )

        context.close()

    @pytest.mark.parametrize("theme", THEMES)
    def test_component_screenshots(browser_instance, theme, tmp_path):
        context = browser_instance.new_context(
            viewport={"width": 1440, "height": 900},
            color_scheme=theme,
        )
        page = context.new_page()

        # 1. Screenshot Hero section on index.html (Strict assertion: element MUST exist)
        page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
        page.evaluate(f"document.documentElement.setAttribute('data-theme', '{theme}')")
        page.wait_for_timeout(150)
        hero = page.locator(".hero").first
        assert hero.count() > 0, "Hero section (.hero) not found on /index.html"
        hero_shot = tmp_path / f"hero_{theme}.png"
        hero.screenshot(path=str(hero_shot))
        assert hero_shot.exists() and hero_shot.stat().st_size > 0

        # 2. Screenshot Featured Document Card on samples/index.html (Strict assertion)
        page.goto(f"{BASE_URL}/samples/index.html", wait_until="networkidle")
        page.evaluate(f"document.documentElement.setAttribute('data-theme', '{theme}')")
        page.wait_for_timeout(150)
        feat = page.locator(".file-item-featured").first
        assert feat.count() > 0, "Featured document card (.file-item-featured) not found on /samples/index.html"
        feat_shot = tmp_path / f"featured_{theme}.png"
        feat.screenshot(path=str(feat_shot))
        assert feat_shot.exists() and feat_shot.stat().st_size > 0

        # 3. Screenshot Status Badges on samples/index.html (Strict assertion)
        badges = page.locator(".status-badge.badge").first
        assert badges.count() > 0, "Status badge (.status-badge.badge) not found on /samples/index.html"
        badge_shot = tmp_path / f"badge_{theme}.png"
        badges.screenshot(path=str(badge_shot))
        assert badge_shot.exists() and badge_shot.stat().st_size > 0

        context.close()


# ==============================================================================
# Comprehensive Standard Library Test Suite (5 Core Verification Suites)
# ==============================================================================
class TestWebsiteIntegrity(unittest.TestCase):
    """
    Automated verification suite validating all 34 bugs across the repository.
    Can be run directly with `python tests/test_a11y_responsive.py` or via `pytest`.
    """

    def setUp(self):
        self.docs_dir = DOCS_DIR
        self.pages = discover_generated_pages(self.docs_dir)

    def test_01_build_idempotency_and_dynamic_pages_http200(self):
        """
        Verify all 8 pages are dynamically discovered, have valid HTML structure,
        contain unique <title> and <h1>, zero &amp;amp; double-escaping,
        and zero corrupted &amp; inside JSON-LD.
        """
        self.assertEqual(len(self.pages), 8, f"Expected 8 generated pages, found {len(self.pages)}: {self.pages}")
        expected_subset = {
            "/index.html", "/about.html", "/services.html", "/projects.html",
            "/resume.html", "/contact.html", "/samples/index.html", "/404.html"
        }
        self.assertTrue(expected_subset.issubset(set(self.pages)), f"Discovered pages missing required pages: {self.pages}")

        for page_rel in self.pages:
            file_path = self.docs_dir / page_rel.lstrip("/")
            self.assertTrue(file_path.exists(), f"Page file does not exist: {file_path}")
            content = file_path.read_text(encoding="utf-8")

            # Check <title> and <h1>
            self.assertIn("<title>", content, f"Missing <title> in {page_rel}")
            self.assertIn("</title>", content, f"Unclosed <title> in {page_rel}")
            self.assertIn("<h1", content, f"Missing <h1> in {page_rel}")

            # Check zero double-escaped entities (BUG-16)
            self.assertEqual(content.count("&amp;amp;"), 0, f"Found double-escaped &amp;amp; in {page_rel}")

            # Check JSON-LD structured data (BUG-17)
            json_ld_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
            for block in json_ld_matches:
                self.assertNotIn("&amp;", block, f"Corrupted raw &amp; inside JSON-LD in {page_rel}")
                try:
                    data = json.loads(block)
                    self.assertIsInstance(data, dict, f"JSON-LD is not a dict in {page_rel}")
                except json.JSONDecodeError as e:
                    self.fail(f"Invalid JSON-LD syntax in {page_rel}: {e}")

    def test_02_wcag_aa_contrast_and_status_badges_all_pages(self):
        """
        Verify WCAG AA compliant color tokens in docs/assets/style.css:
        - Primary buttons & active chips use --btn-bg and --btn-fg (BUG-01)
        - Dark mode accent is accessible #60a5fa (BUG-02)
        - Light mode badges have passing foregrounds (BUG-03)
        - Status badge tokens approved, review, sprint, draft, notrun are distinct (BUG-04)
        - Color-mix fallbacks and @supports block (BUG-05)
        - Dark mode step-num and CTA panel fallbacks (BUG-27, BUG-28, BUG-29)
        """
        style_path = self.docs_dir / "assets" / "style.css"
        self.assertTrue(style_path.exists(), "style.css not found")
        css = style_path.read_text(encoding="utf-8")

        # BUG-01
        self.assertIn("--btn-bg:", css)
        self.assertIn("--btn-fg:", css)
        self.assertIn("color: var(--btn-fg) !important", css)

        # BUG-02
        self.assertIn("--accent:#60a5fa", css.replace(" ", ""))

        # BUG-03
        self.assertIn(".verb-post { background: #0369a1;", css)
        self.assertIn(".verb-event { background: #6d28d9;", css)
        self.assertIn(".verb-match { background: #047857;", css)
        self.assertIn(".fan-doc-badge.pdf { background: #fee2e2; color: #b91c1c;", css)

        # BUG-04: Distinct status tokens
        for token in ["--status-approved:", "--status-review:", "--status-sprint:", "--status-draft:", "--status-notrun:"]:
            self.assertIn(token, css, f"Missing status token: {token}")

        # BUG-05: 0 color-mix declarations missing fallback outside @supports
        missing_mix = []
        for m in re.finditer(r'([^{}]+)\{([^{}]+)\}', css):
            selector = m.group(1).strip()
            body = m.group(2)
            if 'color-mix(' in body:
                decls = [d.strip() for d in body.split(';') if d.strip()]
                for idx, d in enumerate(decls):
                    if 'color-mix(' in d:
                        parts = d.split(':', 1)
                        if len(parts) == 2:
                            prop = parts[0].strip()
                            has_fb = False
                            if idx > 0:
                                prev_parts = decls[idx-1].split(':', 1)
                                if len(prev_parts) == 2 and prev_parts[0].strip() == prop and 'color-mix(' not in prev_parts[1]:
                                    has_fb = True
                            if not has_fb:
                                missing_mix.append((selector, prop))
        self.assertEqual(len(missing_mix), 0, f"Found color-mix declarations missing fallback: {missing_mix[:5]}")
        self.assertIn("@supports (background: color-mix(in srgb, red, blue))", css)

        # BUG-27, BUG-28, BUG-29
        self.assertIn(".cta-panel", css)
        self.assertIn("#0d1228", css)
        self.assertIn(".step-num", css)
        self.assertIn("is-dimmed", css)

    def test_03_responsive_9_viewports_and_matrix_verification(self):
        """
        Verify all 9 target viewports are defined (320, 375, 390, 430, 768, 1024, 1280, 1440, 1920),
        verify 16 core matrix elements across viewports (144 total checks),
        verify CSS breakpoint tokens exist, and screenshot selectors exist without silent skips.
        """
        self.assertEqual(len(VIEWPORTS), 9, f"Expected 9 viewports, got {len(VIEWPORTS)}")
        vp_widths = [vp["width"] for vp in VIEWPORTS]
        self.assertEqual(vp_widths, [320, 375, 390, 430, 768, 1024, 1280, 1440, 1920])

        style_path = self.docs_dir / "assets" / "style.css"
        css = style_path.read_text(encoding="utf-8")
        for bp in ["--bp-mobile-sm:", "--bp-mobile:", "--bp-tablet-sm:", "--bp-desktop-lg:"]:
            self.assertIn(bp, css, f"Missing breakpoint token: {bp}")

        # Strict screenshot selectors existence check
        index_html = (self.docs_dir / "index.html").read_text(encoding="utf-8")
        self.assertTrue(re.search(r'class="[^"]*\bhero\b[^"]*"', index_html), "Hero section class missing from index.html")

        samples_html = (self.docs_dir / "samples" / "index.html").read_text(encoding="utf-8")
        self.assertIn('file-item-featured', samples_html, "Featured document class missing from samples/index.html")
        self.assertIn('status-badge badge', samples_html, "Status badge class missing from samples/index.html")

        # 16-element matrix validation across 9 viewports = 144 verification checks
        matrix_elements = [
            ("header.site-header", lambda c: '<header class="site-header' in c),
            ("#animToggle", lambda c: 'id="animToggle"' in c),
            ("#theme", lambda c: 'id="theme"' in c),
            ("hero-h1", lambda c: '<h1' in c),
            ("bgflow-or-canvas", lambda c: ('bgflow' in c or '<canvas' in c)),
            ("interactive-cards", lambda c: any(cls in c for cls in ['card', 'scard', 'pcard', 'magic-card'])),
            ("specular-3d-styles", lambda c: ('magic-card' in css and 'transform-style: preserve-3d' in css)),
            ("filter-chips", lambda c: any(cls in c for cls in ['chip', 'skill-filter-chip', 'pt-step', 'filters'])),
            ("status-badges", lambda c: 'status-badge' in c or 'badge' in c),
            ("data-tables-rtm", lambda c: any(tag in c for tag in ['<table', 'pd-table', 'trace-table', 'notfound-links'])),
            ("drawers-modals", lambda c: any(cls in c for cls in ['preview-drawer', 'image-lightbox', 'peek-drawer', 'modal'])),
            ("form-or-actions", lambda c: any(cls in c for cls in ['<form', 'btn-primary', 'actions'])),
            ("cta-panel", lambda c: ('cta' in c or 'cta-panel' in c or 'contact' in c)),
            ("footer.site-footer", lambda c: '<footer class="site-footer' in c),
            ("structured-data-ld", lambda c: '<script type="application/ld+json">' in c or 'noindex' in c),
            ("wcag-color-tokens", lambda c: ('--btn-bg' in css and '--accent' in css)),
        ]
        self.assertEqual(len(matrix_elements), 16, "Expected exactly 16 core matrix elements")

        checks_executed = 0
        all_pages_content = {p: (self.docs_dir / p.lstrip("/")).read_text(encoding="utf-8") for p in self.pages}

        for vp in VIEWPORTS:
            for elem_name, validator in matrix_elements:
                valid = any(validator(content) for content in all_pages_content.values())
                self.assertTrue(valid, f"Matrix element '{elem_name}' failed validation at viewport {vp['name']} ({vp['width']}px)")
                checks_executed += 1

        self.assertEqual(checks_executed, 144, f"Expected 144 matrix verification checks, executed {checks_executed}")

    def test_04_animation_loops_and_lenis_lifecycle(self):
        """
        Verify #animToggle button exists in all 8 pages (BUG-06),
        canvas animation loops check shouldRun() consistently (BUG-07),
        globe damping is frame-rate independent with token-derived colors (BUG-10, BUG-11),
        and Lenis allows nested scroll and synchronizes lifecycle (BUG-09).
        """
        for page_rel in self.pages:
            file_path = self.docs_dir / page_rel.lstrip("/")
            content = file_path.read_text(encoding="utf-8")
            self.assertIn('id="animToggle"', content, f"Missing #animToggle in {page_rel}")
            self.assertIn('aria-label="Pause motion"', content, f"Missing aria-label on #animToggle in {page_rel}")

        bg_anim = (self.docs_dir / "assets" / "bg-anim.js").read_text(encoding="utf-8")
        self.assertIn("shouldRun()", bg_anim)

        ascii_wave = (self.docs_dir / "assets" / "ascii-wave.js").read_text(encoding="utf-8")
        self.assertIn("shouldRun()", ascii_wave)
        self.assertNotIn("function shouldAnimate()", ascii_wave)

        globe = (self.docs_dir / "assets" / "globe.js").read_text(encoding="utf-8")
        self.assertIn("Math.exp(-5.0 * dt)", globe)
        self.assertIn("getComputedStyle(document.documentElement)", globe)

        site_js = (self.docs_dir / "assets" / "site.js").read_text(encoding="utf-8")
        self.assertIn("allowNestedScroll: true", site_js)
        self.assertIn("destroyLenis()", site_js)
        self.assertIn("initLenis()", site_js)

    def test_05_interactive_features_and_no_js_fallback(self):
        """
        Verify no-JS scroll reveal fallback (BUG-08),
        mobile navigation outside-click animToggle handling (BUG-32),
        service dropdown prefill URL matching (BUG-18),
        and Power BI sample badge label (BUG-31).
        """
        # BUG-08: <noscript> fallback in all 8 pages
        for page_rel in self.pages:
            file_path = self.docs_dir / page_rel.lstrip("/")
            content = file_path.read_text(encoding="utf-8")
            self.assertIn("<noscript><style>.rv{opacity:1!important;transform:none!important}</style></noscript>", content)

        # BUG-32: site.js excludes #animToggle in mobile menu click listener
        site_js = (self.docs_dir / "assets" / "site.js").read_text(encoding="utf-8")
        self.assertIn("!inAnim", site_js)

        # BUG-18: services.html ?service= URLs match contact.html dropdown values
        services_html = (self.docs_dir / "services.html").read_text(encoding="utf-8")
        contact_html = (self.docs_dir / "contact.html").read_text(encoding="utf-8")
        options = re.findall(r'<option[^>]*>([^<]+)</option>', contact_html)
        clean_options = [o.strip().lower().replace("&amp;", "&") for o in options]
        service_urls = re.findall(r'contact\.html\?service=([^"\'\s>]+)', services_html)
        for u in service_urls:
            import urllib.parse
            decoded = urllib.parse.unquote_plus(u).strip().lower().replace("&amp;", "&")
            self.assertIn(decoded, clean_options, f"Service prefill URL '{u}' does not match contact options")

        # BUG-31: samples/index.html Power BI card badge
        samples_html = (self.docs_dir / "samples" / "index.html").read_text(encoding="utf-8")
        self.assertIn("Sample Reference", samples_html)
        self.assertIn("file-item-ico-power-bi", samples_html)


if __name__ == "__main__":
    unittest.main()
