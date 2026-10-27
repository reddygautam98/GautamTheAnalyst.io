from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page()
    
    errors = []
    warnings = []
    failed_reqs = []
    
    page.on("pageerror", lambda err: errors.append(str(err)))
    page.on("console", lambda msg: errors.append(f"Console {msg.type}: {msg.text}") if msg.type == "error" else warnings.append(msg.text))
    page.on("requestfailed", lambda req: failed_reqs.append(req.url))
    
    page.goto('http://127.0.0.1:8080/samples/index.html', wait_until='networkidle')
    
    print("Page errors on load:", errors)
    print("Failed requests:", failed_reqs)
    
    # Test preview drawer: click preview button
    preview_btn = page.query_selector("[data-preview]")
    print("Preview button found:", preview_btn is not None)
    if preview_btn:
        print("Clicking preview button...")
        preview_btn.click()
        page.wait_for_timeout(300)
        
        drawer = page.query_selector("#previewDrawer")
        print("Drawer found:", drawer is not None)
        if drawer:
            print("Drawer hidden:", drawer.get_attribute("hidden"))
            print("Drawer style display / opacity:", page.evaluate("""() => {
                const el = document.getElementById('previewDrawer');
                const panel = el.querySelector('.pd-panel');
                return {
                    drawerDisplay: window.getComputedStyle(el).display,
                    drawerVisibility: window.getComputedStyle(el).visibility,
                    panelDisplay: panel ? window.getComputedStyle(panel).display : null,
                    panelOpacity: panel ? window.getComputedStyle(panel).opacity : null,
                    panelTransform: panel ? window.getComputedStyle(panel).transform : null
                };
            }"""))
            
        # Test tab switching inside drawer
        for tab_id in ["pdtab-brd", "pdtab-frd", "pdtab-stories", "pdtab-rtm", "pdtab-mom"]:
            tab = page.query_selector(f"#{tab_id}")
            if tab:
                tab.click()
                page.wait_for_timeout(100)
                pane_id = tab.get_attribute("aria-controls")
                pane = page.query_selector(f"#{pane_id}")
                hidden = pane.get_attribute("hidden") if pane else "not found"
                print(f"Tab {tab_id} -> Pane {pane_id} hidden: {hidden}")
                
        # Test closing drawer
        close_btn = page.query_selector("#pdClose")
        if close_btn:
            close_btn.click()
            page.wait_for_timeout(200)
            print("After close click, drawer hidden:", drawer.get_attribute("hidden") if drawer else None)
            
    print("Errors after drawer interaction:", errors)
    b.close()
