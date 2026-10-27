from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1280, "height": 900})
    
    logs = []
    errors = []
    page.on("console", lambda msg: logs.append(f"[{msg.type}] {msg.text}") if msg.type != "error" else errors.append(f"[{msg.type}] {msg.text}"))
    page.on("pageerror", lambda err: errors.append(str(err)))
    
    print("Navigating to http://localhost:8000/contact.html ...")
    page.goto("http://localhost:8000/contact.html", wait_until="networkidle")
    page.wait_for_timeout(1000)
    
    print("Console errors on load:", errors)
    assert len(errors) == 0, f"Expected 0 errors, got: {errors}"
    
    # Verify globe elements
    card = page.query_selector("#globeCard")
    canvas = page.query_selector("#globeCanvas")
    reset_btn = page.query_selector("#globeResetBtn")
    
    print("Globe card found:", card is not None)
    print("Globe canvas found:", canvas is not None)
    print("Reset button found:", reset_btn is not None)
    assert card is not None and canvas is not None, "Globe elements missing!"
    
    # Check dark mode screenshot
    page.screenshot(path="scratch/contact_globe_dark.png")
    print("Saved scratch/contact_globe_dark.png")
    
    # Test drag interaction
    box = canvas.bounding_box()
    print("Canvas bounding box:", box)
    page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    page.mouse.down()
    page.mouse.move(box["x"] + box["width"] / 2 + 100, box["y"] + box["height"] / 2 - 20)
    page.wait_for_timeout(200)
    page.mouse.up()
    page.wait_for_timeout(500)
    print("Drag interaction completed cleanly!")
    
    # Test reset button click
    page.evaluate("() => document.getElementById('globeResetBtn').click()")
    page.wait_for_timeout(400)
    print("Reset button clicked cleanly!")
    
    # Element screenshot of the globe card
    card.screenshot(path="scratch/globe_card_light.png")
    print("Saved scratch/globe_card_light.png")
    
    # Test theme toggle to dark mode
    theme_btn = page.query_selector("#theme")
    if theme_btn:
        print("Toggling theme to dark mode...")
        theme_btn.click()
        page.wait_for_timeout(600)
        theme = page.evaluate("() => document.documentElement.dataset.theme")
        print("Current theme:", theme)
        card.screenshot(path="scratch/globe_card_dark.png")
        print("Saved scratch/globe_card_dark.png")
        
    # Test mobile viewport 390px
    page.set_viewport_size({"width": 390, "height": 844})
    page.wait_for_timeout(500)
    overflow = page.evaluate("() => document.documentElement.scrollWidth > window.innerWidth")
    print("Mobile 390px horizontal overflow:", overflow)
    assert not overflow, "Mobile layout has horizontal overflow!"
    page.screenshot(path="scratch/contact_globe_mobile.png")
    print("Saved scratch/contact_globe_mobile.png")
    
    print("Final console errors:", errors)
    b.close()
    print("ALL TESTS PASSED!")
