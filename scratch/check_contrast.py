import json
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8080/"
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

def check_contrast():
    contrast_results = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        
        for p_name in PAGES:
            for theme in ["light", "dark"]:
                page.goto(BASE_URL + p_name, wait_until="networkidle")
                page.evaluate(f"() => document.documentElement.dataset.theme = '{theme}'")
                page.wait_for_timeout(200)
                
                # Evaluate visible text elements
                failures = page.evaluate("""() => {
                    function getLuminance(r, g, b) {
                        const a = [r, g, b].map(v => {
                            v /= 255;
                            return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
                        });
                        return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722;
                    }

                    function parseRgba(str) {
                        const m = str.match(/rgba?\\((\\d+)\\s*,\\s*(\\d+)\\s*,\\s*(\\d+)(?:\\s*,\\s*([\\d.]+))?\\)/);
                        if (!m) return null;
                        return {
                            r: parseInt(m[1]),
                            g: parseInt(m[2]),
                            b: parseInt(m[3]),
                            a: m[4] !== undefined ? parseFloat(m[4]) : 1.0
                        };
                    }

                    function getEffectiveBg(el) {
                        let cur = el;
                        let r = 255, g = 255, b = 255; // default light
                        if (document.documentElement.dataset.theme === 'dark') {
                            r = 11; g = 15; b = 25; // #0b0f19
                        }
                        while (cur && cur !== document.documentElement) {
                            const style = window.getComputedStyle(cur);
                            const bg = parseRgba(style.backgroundColor);
                            if (bg && bg.a > 0.95) {
                                return bg;
                            }
                            cur = cur.parentElement;
                        }
                        return { r, g, b, a: 1 };
                    }

                    const textEls = document.querySelectorAll('p, span, h1, h2, h3, h4, h5, h6, a, button, label, li, td, th');
                    const issues = [];
                    for (let el of textEls) {
                        if (!el.innerText || !el.innerText.trim()) continue;
                        if (el.offsetParent === null) continue; // hidden
                        if (el.closest('[hidden]')) continue;
                        
                        const style = window.getComputedStyle(el);
                        if (style.display === 'none' || style.visibility === 'hidden' || parseFloat(style.opacity) < 0.1) continue;
                        
                        const fg = parseRgba(style.color);
                        if (!fg || fg.a < 0.2) continue;
                        
                        const bg = getEffectiveBg(el);
                        const L1 = getLuminance(fg.r, fg.g, fg.b);
                        const L2 = getLuminance(bg.r, bg.g, bg.b);
                        const cr = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
                        
                        const fontSize = parseFloat(style.fontSize);
                        const isBold = parseInt(style.fontWeight) >= 600 || style.fontWeight === 'bold';
                        const isLarge = fontSize >= 24 || (fontSize >= 18.5 && isBold);
                        const req = isLarge ? 3.0 : 4.5;
                        
                        if (cr < req) {
                            issues.push({
                                tag: el.tagName,
                                cls: el.className,
                                text: el.innerText.trim().slice(0, 30),
                                cr: cr.toFixed(2),
                                req: req,
                                color: style.color,
                                bg: `rgb(${bg.r},${bg.g},${bg.b})`,
                                fontSize: fontSize
                            });
                        }
                    }
                    return issues;
                }""")
                if failures:
                    contrast_results.append({
                        "page": p_name,
                        "theme": theme,
                        "failure_count": len(failures),
                        "sample_failures": failures[:10]
                    })
        browser.close()
        
    print(f"Total contrast issues found across pages/themes: {len(contrast_results)}")
    with open("scratch/contrast_results.json", "w", encoding="utf-8") as f:
        json.dump(contrast_results, f, indent=2)
    for c in contrast_results:
        print(f"[{c['page']} - {c['theme']}] {c['failure_count']} text elements below threshold")
        for s in c['sample_failures'][:3]:
            print(f"   {s['tag']}.{s['cls']} '{s['text']}': CR {s['cr']} (req {s['req']}) fg={s['color']} bg={s['bg']}")

if __name__ == "__main__":
    check_contrast()
