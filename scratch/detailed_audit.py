import os
import json
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8080/"

def run_detailed_tests():
    findings = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # 1. Test Home Page interactions
        page = browser.new_page()
        page_errors = []
        page.on("pageerror", lambda err: page_errors.append(str(err)))
        page.on("console", lambda msg: page_errors.append(f"Console {msg.type}: {msg.text}") if msg.type in ["error"] else None)
        
        page.goto(BASE_URL + "index.html", wait_until="networkidle")
        
        # Test Theme Toggle
        theme_btn = page.query_selector("#theme")
        if not theme_btn:
            findings.append({"area": "Theme", "issue": "#theme button missing on index.html"})
        else:
            initial_theme = page.evaluate("() => document.documentElement.dataset.theme")
            theme_btn.click()
            new_theme = page.evaluate("() => document.documentElement.dataset.theme")
            if initial_theme == new_theme:
                findings.append({"area": "Theme", "issue": "Theme button click did not toggle dataset.theme"})
            theme_btn.click() # restore
            
        # Test Motion Toggle
        anim_btn = page.query_selector("#animToggle")
        if anim_btn:
            anim_btn.click()
            is_paused = page.evaluate("() => document.documentElement.classList.contains('is-anim-paused')")
            if not is_paused:
                findings.append({"area": "Motion", "issue": "animToggle did not add is-anim-paused class"})
            anim_btn.click() # restore
            
        # Test Hero Slider
        slider_tabs = page.query_selector_all(".slider-tab")
        if slider_tabs:
            # Click tab 1
            slider_tabs[1].click()
            page.wait_for_timeout(200)
            active_slide = page.evaluate("""() => {
                const s = document.querySelectorAll('.slider-slide');
                return Array.from(s).findIndex(el => !el.hidden && el.classList.contains('is-active'));
            }""")
            if active_slide != 1:
                findings.append({"area": "Hero Slider", "issue": f"Clicking tab 1 did not activate slide 1 (active: {active_slide})"})
                
            # Click next button
            next_btn = page.query_selector("#slideNext")
            if next_btn:
                next_btn.click()
                page.wait_for_timeout(200)
                active_slide_after_next = page.evaluate("""() => {
                    const s = document.querySelectorAll('.slider-slide');
                    return Array.from(s).findIndex(el => !el.hidden && el.classList.contains('is-active'));
                }""")
                if active_slide_after_next != 2:
                    findings.append({"area": "Hero Slider", "issue": f"Clicking next did not advance to slide 2 (active: {active_slide_after_next})"})

        # Test Wireframe Pause button
        wf_pause = page.query_selector("#wfPauseBtn")
        if wf_pause:
            wf_pause.click()
            pressed = wf_pause.get_attribute("aria-pressed")
            if pressed != "true":
                findings.append({"area": "Wireframe Cycle", "issue": "wfPauseBtn aria-pressed not updated on click"})

        # Test Mobile Menu at 390px
        page.set_viewport_size({"width": 390, "height": 844})
        menu_btn = page.query_selector("#menu")
        nav_menu = page.query_selector("#nav")
        if menu_btn and nav_menu:
            menu_btn.click()
            page.wait_for_timeout(200)
            is_open = page.evaluate("() => document.getElementById('nav').classList.contains('open')")
            if not is_open:
                findings.append({"area": "Mobile Menu", "issue": "Clicking menu button at 390px did not open nav"})
            # Test Escape key
            page.keyboard.press("Escape")
            page.wait_for_timeout(200)
            is_open_after_esc = page.evaluate("() => document.getElementById('nav').classList.contains('open')")
            if is_open_after_esc:
                findings.append({"area": "Mobile Menu", "issue": "Pressing Escape did not close mobile menu"})

        # Reset viewport
        page.set_viewport_size({"width": 1280, "height": 800})
        
        # 2. Test Projects Page (Filters & Magnifier & Lightbox)
        page.goto(BASE_URL + "projects.html", wait_until="networkidle")
        chips = page.query_selector_all(".chip[data-f]")
        for chip in chips:
            cat = chip.get_attribute("data-f")
            chip.click()
            page.wait_for_timeout(200)
            # Check cards visibility
            mismatch = page.evaluate(f"""() => {{
                const cat = '{cat}';
                const cards = document.querySelectorAll('[data-cat]');
                for (let c of cards) {{
                    const shouldShow = (cat === 'all' || c.dataset.cat === cat);
                    if (shouldShow && c.hidden) return 'visible card is hidden';
                    if (!shouldShow && !c.hidden) return 'hidden card is visible';
                }}
                return null;
            }}""")
            if mismatch:
                findings.append({"area": "Project Filter", "issue": f"Filter '{cat}' failed: {mismatch}"})

        # Test Image Lightbox on projects
        zoom_btn = page.query_selector(".img-zoom-btn, .zoomable-img")
        if zoom_btn:
            zoom_btn.click()
            page.wait_for_timeout(200)
            ilb_hidden = page.evaluate("() => document.getElementById('imageLightbox').hidden")
            if ilb_hidden:
                findings.append({"area": "Lightbox", "issue": "Image zoom button did not open imageLightbox"})
            else:
                page.keyboard.press("Escape")
                page.wait_for_timeout(200)
                ilb_hidden_after_esc = page.evaluate("() => document.getElementById('imageLightbox').hidden")
                if not ilb_hidden_after_esc:
                    findings.append({"area": "Lightbox", "issue": "Escape did not close imageLightbox"})

        # 3. Test Samples Page (Preview Drawer & Phase Filter & View Toggle)
        page.goto(BASE_URL + "samples/index.html", wait_until="networkidle")
        preview_btn = page.query_selector("[data-preview]")
        if preview_btn:
            preview_btn.click()
            page.wait_for_timeout(200)
            drawer_hidden = page.evaluate("() => document.getElementById('previewDrawer').hidden")
            if drawer_hidden:
                findings.append({"area": "Preview Drawer", "issue": "Preview button did not open previewDrawer"})
            else:
                # Test drawer tab switching
                frd_tab = page.query_selector("#pdtab-frd")
                if frd_tab:
                    frd_tab.click()
                    page.wait_for_timeout(100)
                    frd_pane_hidden = page.evaluate("() => document.getElementById('pd-frd').hidden")
                    if frd_pane_hidden:
                        findings.append({"area": "Preview Drawer", "issue": "FRD tab click did not unhide pd-frd"})
                # Test close
                close_btn = page.query_selector("#pdClose")
                if close_btn:
                    close_btn.click()
                    page.wait_for_timeout(200)
                    drawer_hidden_after_close = page.evaluate("() => document.getElementById('previewDrawer').hidden")
                    if not drawer_hidden_after_close:
                        findings.append({"area": "Preview Drawer", "issue": "Close button did not close previewDrawer"})

        # Test phase filter
        pt_steps = page.query_selector_all(".pt-step")
        for step in pt_steps:
            phase = step.get_attribute("data-phase")
            step.click()
            page.wait_for_timeout(100)
            phase_mismatch = page.evaluate(f"""() => {{
                const phase = '{phase}';
                const items = document.querySelectorAll('.file-item');
                for (let it of items) {{
                    const itPhase = it.dataset.phase || 'all';
                    const shouldShow = (phase === 'all' || itPhase === phase || itPhase === 'all');
                    if (shouldShow && it.hidden) return 'visible item is hidden';
                    if (!shouldShow && !it.hidden) return 'hidden item is visible';
                }}
                return null;
            }}""")
            if phase_mismatch:
                findings.append({"area": "Samples Phase Filter", "issue": f"Phase '{phase}' failed: {phase_mismatch}"})

        # Test View Grid / List Toggle
        view_grid = page.query_selector("#viewGrid")
        view_list = page.query_selector("#viewList")
        if view_grid and view_list:
            view_grid.click()
            page.wait_for_timeout(100)
            has_grid_class = page.evaluate("() => document.querySelector('.file-list').classList.contains('file-list-grid')")
            if not has_grid_class:
                findings.append({"area": "Samples View Toggle", "issue": "viewGrid did not add file-list-grid class"})
            view_list.click()
            page.wait_for_timeout(100)
            has_grid_class_after_list = page.evaluate("() => document.querySelector('.file-list').classList.contains('file-list-grid')")
            if has_grid_class_after_list:
                findings.append({"area": "Samples View Toggle", "issue": "viewList did not remove file-list-grid class"})

        # 4. Test Resume Page (Skill chips & Print button)
        page.goto(BASE_URL + "resume.html", wait_until="networkidle")
        skill_chips = page.query_selector_all(".skill-filter-chip")
        if skill_chips:
            # Click second chip
            chip = skill_chips[1]
            chip.click()
            page.wait_for_timeout(100)
            has_highlighted = page.evaluate("() => document.querySelectorAll('.role li.is-highlighted').length > 0")
            if not has_highlighted:
                findings.append({"area": "Resume Skills Filter", "issue": f"Clicking skill chip '{chip.inner_text().strip()}' highlighted 0 bullets"})

        # 5. Test Contact Page (Form validation & Fallback card)
        page.goto(BASE_URL + "contact.html", wait_until="networkidle")
        submit_btn = page.query_selector("button[type='submit']")
        
        # Test Empty submit
        submit_btn.click()
        page.wait_for_timeout(100)
        invalid_fields = page.evaluate("() => document.querySelectorAll('#enquiry [aria-invalid=\"true\"]').length")
        if invalid_fields == 0:
            findings.append({"area": "Contact Form", "issue": "Submitting empty form did not set aria-invalid='true' on required fields"})
            
        # Test Invalid email
        name_input = page.query_selector("#enquiry-name")
        email_input = page.query_selector("#enquiry-email")
        msg_input = page.query_selector("#enquiry-msg")
        if name_input and email_input and msg_input:
            name_input.fill("Test User")
            email_input.fill("invalid-email")
            msg_input.fill("This is a test message with enough details.")
            submit_btn.click()
            page.wait_for_timeout(100)
            email_invalid = page.evaluate("() => document.getElementById('enquiry-email').getAttribute('aria-invalid') === 'true'")
            if not email_invalid:
                findings.append({"area": "Contact Form", "issue": "Invalid email did not trigger aria-invalid='true'"})
                
            # Fill valid email and invalid URL in ref
            email_input.fill("test@example.com")
            ref_input = page.query_selector("#enquiry-ref")
            if ref_input:
                ref_input.fill("not-a-url")
                submit_btn.click()
                page.wait_for_timeout(100)
                ref_invalid = page.evaluate("() => document.getElementById('enquiry-ref').getAttribute('aria-invalid') === 'true'")
                if not ref_invalid:
                    findings.append({"area": "Contact Form", "issue": "Invalid reference URL did not trigger aria-invalid='true'"})
                ref_input.fill("https://example.com")
                
            # Now fill service dropdown and submit valid form
            page.select_option("#enquiry-service", index=1)
            submit_btn.click()
            page.wait_for_timeout(200)
            fb_card_hidden = page.evaluate("() => document.getElementById('fallbackCard').hidden")
            if fb_card_hidden:
                findings.append({"area": "Contact Form", "issue": "Valid form submission did not show fallbackCard"})

        # 6. Test About Page (Console Tabs)
        page.goto(BASE_URL + "about.html", wait_until="networkidle")
        console_tabs = page.query_selector_all(".console-tab")
        if console_tabs:
            console_tabs[1].click()
            page.wait_for_timeout(100)
            tab1_active = page.evaluate("() => document.querySelectorAll('.console-panel')[1].classList.contains('is-active')")
            if not tab1_active:
                findings.append({"area": "About Console", "issue": "Clicking console tab 1 did not activate panel 1"})

        # Check collected errors
        if page_errors:
            findings.append({"area": "Runtime Page Errors", "issue": page_errors})

        browser.close()

    print("\n=== DETAILED INTERACTION TEST RESULTS ===")
    print(f"Total findings: {len(findings)}")
    for f in findings:
        print(f"[{f['area']}] {f['issue']}")

    with open("scratch/detailed_findings.json", "w", encoding="utf-8") as out:
        json.dump(findings, out, indent=2)

if __name__ == "__main__":
    run_detailed_tests()
