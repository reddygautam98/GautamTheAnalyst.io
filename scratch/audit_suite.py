import os
import sys
import json
import urllib.parse
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

VIEWPORTS = [320, 360, 390, 430, 768, 1024, 1280, 1440, 1920]
BASE_URL = "http://127.0.0.1:8080/"

def run_audit():
    results = {
        "console_errors": [],
        "console_warnings": [],
        "failed_requests": [],
        "overflow_issues": [],
        "broken_links": [],
        "heading_issues": [],
        "a11y_issues": [],
        "functional_checks": []
    }

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Listen to console and request failures
        current_page_name = ""
        def on_console(msg):
            if msg.type in ["error"]:
                results["console_errors"].append({"page": current_page_name, "text": msg.text, "location": msg.location})
            elif msg.type in ["warning"]:
                results["console_warnings"].append({"page": current_page_name, "text": msg.text})

        def on_request_failed(req):
            results["failed_requests"].append({"page": current_page_name, "url": req.url, "failure": req.failure})

        page.on("console", on_console)
        page.on("requestfailed", on_request_failed)

        for p_name in PAGES:
            current_page_name = p_name
            url = BASE_URL + p_name
            print(f"Auditing page: {p_name}")
            resp = page.goto(url, wait_until="networkidle")
            if not resp or resp.status != 200:
                results["failed_requests"].append({"page": p_name, "url": url, "status": resp.status if resp else "no_response"})

            # Check headings hierarchy
            headings = page.eval_on_selector_all("h1, h2, h3, h4, h5, h6", """elements => elements.map(el => ({
                tag: el.tagName.toLowerCase(),
                text: el.innerText.trim(),
                level: parseInt(el.tagName[1]),
                visible: el.offsetParent !== null
            }))""")
            h1_count = sum(1 for h in headings if h["tag"] == "h1")
            if h1_count != 1:
                results["heading_issues"].append({"page": p_name, "issue": f"Expected exactly 1 h1, found {h1_count}"})

            prev_level = 1
            for h in headings:
                if h["level"] > prev_level + 1:
                    results["heading_issues"].append({"page": p_name, "issue": f"Heading hierarchy jump: {prev_level} to {h['level']} ('{h['text']}')"})
                prev_level = h["level"]

            # Check missing alt text on images (excluding decorative aria-hidden images)
            img_issues = page.eval_on_selector_all("img", """imgs => imgs.map(img => ({
                src: img.getAttribute('src'),
                alt: img.getAttribute('alt'),
                hasAlt: img.hasAttribute('alt'),
                ariaHidden: img.getAttribute('aria-hidden') === 'true'
            })).filter(i => !i.ariaHidden && (!i.hasAlt || i.alt === null || i.alt.trim() === ''))""")
            for img in img_issues:
                results["a11y_issues"].append({"page": p_name, "issue": f"Image missing descriptive alt: {img['src']}"})

            # Check buttons without accessible name
            btn_issues = page.eval_on_selector_all("button", """btns => btns.map(b => ({
                id: b.id,
                cls: b.className,
                text: b.innerText.trim(),
                ariaLabel: b.getAttribute('aria-label'),
                ariaLabelledby: b.getAttribute('aria-labelledby'),
                title: b.getAttribute('title')
            })).filter(b => !b.text && !b.ariaLabel && !b.ariaLabelledby && !b.title)""")
            for b in btn_issues:
                results["a11y_issues"].append({"page": p_name, "issue": f"Button without accessible name: #{b['id']} .{b['cls']}"})

            # Check internal links and anchors
            links = page.eval_on_selector_all("a", """anchors => anchors.map(a => ({
                href: a.getAttribute('href'),
                text: a.innerText.trim(),
                ariaLabel: a.getAttribute('aria-label')
            }))""")
            for l in links:
                href = l["href"]
                if not href:
                    results["broken_links"].append({"page": p_name, "issue": "Empty href on anchor", "text": l["text"]})
                elif href.startswith("#") and len(href) > 1:
                    target_id = href[1:]
                    has_target = page.evaluate(f"() => !!document.getElementById('{target_id}') || !!document.querySelector('[name=\"{target_id}\"]')")
                    if not has_target:
                        results["broken_links"].append({"page": p_name, "issue": f"Anchor target not found: {href}", "text": l["text"]})
                elif not href.startswith("http") and not href.startswith("mailto:") and not href.startswith("tel:") and not href.startswith("javascript:"):
                    # Relative link to another file
                    # Resolve path
                    curr_dir = os.path.dirname(os.path.join("docs", p_name))
                    clean_path = href.split("?")[0].split("#")[0]
                    target_file = os.path.normpath(os.path.join(curr_dir, clean_path))
                    if not os.path.exists(target_file):
                        results["broken_links"].append({"page": p_name, "issue": f"Target file does not exist: {target_file} (href: {href})", "text": l["text"]})

            # Test Viewport widths for horizontal overflow
            for vp_w in VIEWPORTS:
                page.set_viewport_size({"width": vp_w, "height": 800})
                page.wait_for_timeout(100)
                overflow_info = page.evaluate("""() => {
                    const docEl = document.documentElement;
                    const body = document.body;
                    const scrollW = Math.max(docEl.scrollWidth, body.scrollWidth);
                    const clientW = docEl.clientWidth;
                    const hasOverflow = scrollW > clientW + 1; // 1px threshold for subpixel
                    let overflowingElements = [];
                    if (hasOverflow) {
                        const all = document.querySelectorAll('*');
                        for (let el of all) {
                            const rect = el.getBoundingClientRect();
                            if (rect.right > clientW + 1) {
                                overflowingElements.push({
                                    tag: el.tagName,
                                    id: el.id,
                                    cls: el.className,
                                    right: rect.right,
                                    clientW: clientW
                                });
                            }
                        }
                    }
                    return {
                        hasOverflow: hasOverflow,
                        scrollW: scrollW,
                        clientW: clientW,
                        overflowingElements: overflowingElements.slice(0, 5)
                    };
                }""")
                if overflow_info["hasOverflow"]:
                    results["overflow_issues"].append({
                        "page": p_name,
                        "viewport": vp_w,
                        "scrollW": overflow_info["scrollW"],
                        "clientW": overflow_info["clientW"],
                        "elements": overflow_info["overflowingElements"]
                    })

        browser.close()

    print("\n=== AUDIT RESULTS ===")
    print(f"Console errors: {len(results['console_errors'])}")
    for e in results["console_errors"]:
        print(f"  [{e['page']}] {e['text']}")

    print(f"Console warnings: {len(results['console_warnings'])}")
    for w in results["console_warnings"]:
        print(f"  [{w['page']}] {w['text']}")

    print(f"Failed requests: {len(results['failed_requests'])}")
    for f in results["failed_requests"]:
        print(f"  [{f['page']}] {f['url']}")

    print(f"Overflow issues: {len(results['overflow_issues'])}")
    for o in results["overflow_issues"]:
        print(f"  [{o['page']} @ {o['viewport']}px] scrollW={o['scrollW']} clientW={o['clientW']} el={o['elements']}")

    print(f"Broken links: {len(results['broken_links'])}")
    for b in results["broken_links"]:
        print(f"  [{b['page']}] {b['issue']} ('{b['text']}')")

    print(f"Heading issues: {len(results['heading_issues'])}")
    for h in results["heading_issues"]:
        print(f"  [{h['page']}] {h['issue']}")

    print(f"A11y issues: {len(results['a11y_issues'])}")
    for a in results["a11y_issues"]:
        print(f"  [{a['page']}] {a['issue']}")

    with open("scratch/audit_summary.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_audit()
