from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page()
    page.goto('http://127.0.0.1:8080/resume.html')
    page.emulate_media(media="print")
    
    css_info = page.evaluate("""() => {
        const btn = document.querySelector('#printResumeBtn');
        const actions = btn.closest('.actions');
        const sf = document.querySelector('.skill-filter-wrap') || document.querySelector('.skill-filter-chip');
        return {
            actionsDisplay: actions ? window.getComputedStyle(actions).display : null,
            btnDisplay: window.getComputedStyle(btn).display,
            sfDisplay: sf ? window.getComputedStyle(sf).display : null,
            btnMatchedRules: 'btn matched'
        };
    }""")
    print("CSS Info in print:", css_info)
    b.close()
