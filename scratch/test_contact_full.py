from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page()
    page.goto('http://127.0.0.1:8080/contact.html')
    
    fbCard = page.query_selector("#fallbackCard")
    
    # Fill all required fields including service
    page.fill("#enquiry-name", "Gautam Test")
    page.fill("#enquiry-email", "gautam@example.com")
    page.select_option("#enquiry-service", index=1)
    page.fill("#enquiry-msg", "Hello this is a test project enquiry with more details.")
    
    page.click("#enquiry button[type='submit']")
    page.wait_for_timeout(500)
    
    print("fbCard hidden after full submit:", fbCard.get_attribute("hidden"))
    errors = page.evaluate("() => Array.from(document.querySelectorAll('#enquiry [aria-invalid=\"true\"]')).map(el => ({id: el.id, name: el.name}))")
    print("Aria-invalid fields after submit:", errors)
    
    b.close()
