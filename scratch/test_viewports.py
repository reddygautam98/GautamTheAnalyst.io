import json
from playwright.sync_api import sync_playwright

VIEWPORTS = [320, 360, 390, 430, 768, 1024, 1280, 1440, 1920]
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

def test_viewports():
    overflow_results = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        for p_name in PAGES:
            page.goto(BASE_URL + p_name, wait_until="networkidle")
            for w in VIEWPORTS:
                page.set_viewport_size({"width": w, "height": 850})
                page.wait_for_timeout(100)
                
                info = page.evaluate("""() => {
                    const de = document.documentElement;
                    const b = document.body;
                    const sw = Math.max(de.scrollWidth, b.scrollWidth);
                    const cw = de.clientWidth;
                    const diff = sw - cw;
                    let badEls = [];
                    if (diff > 1) {
                        const all = document.querySelectorAll('*');
                        for (let el of all) {
                            const rect = el.getBoundingClientRect();
                            if (rect.right > cw + 1) {
                                badEls.push({
                                    tag: el.tagName,
                                    cls: el.className,
                                    id: el.id,
                                    right: rect.right,
                                    width: rect.width
                                });
                            }
                        }
                    }
                    return {
                        hasOverflow: diff > 1,
                        diff: diff,
                        sw: sw,
                        cw: cw,
                        badEls: badEls.slice(0, 5)
                    };
                }""")
                if info["hasOverflow"]:
                    overflow_results.append({
                        "page": p_name,
                        "viewport": w,
                        "diff": info["diff"],
                        "badEls": info["badEls"]
                    })
        browser.close()
        
    print(f"Total overflow occurrences: {len(overflow_results)}")
    for r in overflow_results:
        print(f"[{r['page']} @ {r['viewport']}px] diff={r['diff']}px badEls={r['badEls']}")

if __name__ == "__main__":
    test_viewports()
