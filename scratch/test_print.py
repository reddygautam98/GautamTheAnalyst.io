from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page()
    page.goto('http://127.0.0.1:8080/resume.html', wait_until='networkidle')
    
    # 1. Test clicking a skill filter on screen
    page.click('.skill-filter-chip[data-skill="sql"]')
    dimmed_count_before_print = page.evaluate("() => document.querySelectorAll('.role li.is-dimmed').length")
    print("Screen: SQL filter clicked, dimmed bullets count:", dimmed_count_before_print)
    
    # 2. Emulate print
    page.emulate_media(media="print")
    
    print_visibility = page.evaluate("""() => {
        const header = document.querySelector('.site-header');
        const footer = document.querySelector('.site-footer');
        const printBtn = document.querySelector('#printResumeBtn');
        const actions = printBtn ? printBtn.closest('.actions') : null;
        const sfWrap = document.querySelector('.skills-filter-wrap');
        const dimmedLi = document.querySelector('.role li.is-dimmed');
        const roles = document.querySelectorAll('.role');
        
        return {
            headerDisplay: header ? window.getComputedStyle(header).display : null,
            footerDisplay: footer ? window.getComputedStyle(footer).display : null,
            actionsDisplay: actions ? window.getComputedStyle(actions).display : null,
            sfWrapDisplay: sfWrap ? window.getComputedStyle(sfWrap).display : null,
            dimmedLiOpacity: dimmedLi ? window.getComputedStyle(dimmedLi).opacity : 'none-dimmed',
            firstRoleDisplay: roles[0] ? window.getComputedStyle(roles[0]).display : null,
            firstRoleBreakInside: roles[0] ? window.getComputedStyle(roles[0]).breakInside : null
        };
    }""")
    print("Print Media Styles:", print_visibility)
    b.close()
