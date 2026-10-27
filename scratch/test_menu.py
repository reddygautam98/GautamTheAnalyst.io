from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={'width': 390, 'height': 800})
    page.goto('http://127.0.0.1:8080/index.html')
    
    # Check if menu button has SVG
    mb = page.query_selector("#menu")
    print("MB text/html before click:", mb.inner_html()[:40])
    
    page.click('#menu')
    page.wait_for_timeout(100)
    is_open = page.evaluate("() => document.getElementById('nav').classList.contains('open')")
    print("Nav is open after click:", is_open)
    b.close()
