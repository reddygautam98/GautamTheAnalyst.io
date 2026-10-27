from playwright.sync_api import sync_playwright

CHANNELS = ["chrome", "msedge"]
PAGES = ["index.html", "about.html", "services.html", "projects.html", "resume.html", "contact.html", "samples/index.html", "404.html"]
BASE_URL = "http://127.0.0.1:8080/"

def run_cross_browser():
    with sync_playwright() as p:
        for ch in CHANNELS:
            print(f"\n--- Testing Browser Channel: {ch} ---")
            try:
                b = p.chromium.launch(channel=ch)
                page = b.new_page(viewport={"width": 1280, "height": 800})
                
                errors = []
                page.on("pageerror", lambda err: errors.append(str(err)))
                page.on("console", lambda msg: errors.append(msg.text) if msg.type in ["error"] else None)
                
                for p_name in PAGES:
                    resp = page.goto(BASE_URL + p_name, wait_until="networkidle")
                    assert resp.status == 200, f"Status {resp.status} on {p_name}"
                
                # Test mobile menu toggle on channel
                page.set_viewport_size({"width": 390, "height": 844})
                page.goto(BASE_URL + "index.html", wait_until="networkidle")
                page.click("#menu")
                page.wait_for_timeout(100)
                is_open = page.evaluate("() => document.getElementById('nav').classList.contains('open')")
                print(f"[{ch}] Mobile menu opened successfully:", is_open)
                assert is_open, f"Mobile menu failed to open on {ch}"
                
                print(f"[{ch}] All 8 pages loaded with {len(errors)} runtime errors.")
                b.close()
            except Exception as e:
                print(f"[{ch}] Test error:", e)

if __name__ == "__main__":
    run_cross_browser()
