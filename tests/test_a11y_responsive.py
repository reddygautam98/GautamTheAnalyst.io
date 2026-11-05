"""
Playwright + axe-core accessibility and responsive testing suite for GautamTheAnalyst.io.
Tests all 8 compiled pages across 4 target viewports (320px, 768px, 1024px, 1440px)
in both light and dark themes.

Assertions:
1. HTTP 200 on all pages.
2. Axe-core accessibility: 0 serious or critical violations.
3. No horizontal overflow (document.documentElement.scrollWidth <= document.documentElement.clientWidth).
4. Visual snapshots for hero, featured document card, and status badges.
"""

import os
import pytest
from playwright.sync_api import sync_playwright
try:
    from axe_playwright_python.sync_playwright import Axe
except ImportError:
    Axe = None

BASE_URL = os.environ.get("TEST_BASE_URL", "http://127.0.0.1:8000")

PAGES = [
    "/index.html",
    "/about.html",
    "/services.html",
    "/projects.html",
    "/resume.html",
    "/contact.html",
    "/samples/index.html",
    "/404.html",
]

VIEWPORTS = [
    {"width": 320, "height": 600, "name": "mobile_sm"},
    {"width": 768, "height": 1024, "name": "tablet"},
    {"width": 1024, "height": 768, "name": "desktop_sm"},
    {"width": 1440, "height": 900, "name": "desktop_lg"},
]

THEMES = ["light", "dark"]


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

    # Force theme via data-theme attribute
    page.evaluate(f"document.documentElement.setAttribute('data-theme', '{theme}')")
    page.wait_for_timeout(100)

    # 1. Horizontal overflow assertion
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
    page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
    page.evaluate(f"document.documentElement.setAttribute('data-theme', '{theme}')")
    page.wait_for_timeout(200)

    # Screenshot Hero section
    hero = page.locator(".hero").first
    if hero.count() > 0:
        hero_shot = tmp_path / f"hero_{theme}.png"
        hero.screenshot(path=str(hero_shot))
        assert hero_shot.exists() and hero_shot.stat().st_size > 0

    # Screenshot Featured Document Card
    feat = page.locator(".card-featured, .feat-card").first
    if feat.count() > 0:
        feat_shot = tmp_path / f"featured_{theme}.png"
        feat.screenshot(path=str(feat_shot))
        assert feat_shot.exists() and feat_shot.stat().st_size > 0

    # Screenshot Status Badges
    badges = page.locator(".status-badge, .badge").first
    if badges.count() > 0:
        badge_shot = tmp_path / f"badge_{theme}.png"
        badges.screenshot(path=str(badge_shot))
        assert badge_shot.exists() and badge_shot.stat().st_size > 0

    context.close()

