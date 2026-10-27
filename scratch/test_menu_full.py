from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={'width': 390, 'height': 800})
    page.goto('http://127.0.0.1:8080/index.html')
    
    # 1. Click menu button to open
    page.click('#menu')
    page.wait_for_timeout(100)
    open1 = page.evaluate("() => document.getElementById('nav').classList.contains('open')")
    aria_exp1 = page.evaluate("() => document.getElementById('menu').getAttribute('aria-expanded')")
    print("Test 1 - Open on click:", open1, "aria-expanded:", aria_exp1)
    
    # 2. Click menu button again to close
    page.click('#menu')
    page.wait_for_timeout(100)
    closed1 = not page.evaluate("() => document.getElementById('nav').classList.contains('open')")
    aria_exp2 = page.evaluate("() => document.getElementById('menu').getAttribute('aria-expanded')")
    print("Test 2 - Close on second click:", closed1, "aria-expanded:", aria_exp2)
    
    # 3. Open and close with Escape
    page.click('#menu')
    page.wait_for_timeout(100)
    page.keyboard.press("Escape")
    page.wait_for_timeout(100)
    closed2 = not page.evaluate("() => document.getElementById('nav').classList.contains('open')")
    print("Test 3 - Close on Escape:", closed2)
    
    # 4. Open and close with backdrop click
    page.click('#menu')
    page.wait_for_timeout(100)
    page.click('#navBackdrop', force=True)
    page.wait_for_timeout(100)
    closed3 = not page.evaluate("() => document.getElementById('nav').classList.contains('open')")
    print("Test 4 - Close on backdrop click:", closed3)
    
    # 5. Open and click a nav link
    page.click('#menu')
    page.wait_for_timeout(100)
    page.click('#nav a[href="projects.html"]')
    page.wait_for_timeout(200)
    closed4 = not page.evaluate("() => document.getElementById('nav').classList.contains('open')")
    print("Test 5 - Close on navigation link click:", closed4)

    b.close()
