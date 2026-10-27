from playwright.sync_api import sync_playwright

PAGES = [
    "index.html",
    "about.html",
    "services.html",
    "projects.html",
    "resume.html",
    "contact.html",
    "samples/index.html",
    "404.html"
]
BASE_URL = "http://127.0.0.1:8080/"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    
    for p_name in PAGES:
        page.goto(BASE_URL + p_name, wait_until="networkidle")
        # Apply 200% zoom equivalent or scale
        page.evaluate("() => document.body.style.zoom = '2.0'")
        page.wait_for_timeout(150)
        
        sw = page.evaluate("() => document.documentElement.scrollWidth")
        cw = page.evaluate("() => document.documentElement.clientWidth")
        diff = sw - cw
        print(f"[{p_name} @ 200% zoom] scrollWidth={sw}, clientWidth={cw}, diff={diff}")
    browser.close()
