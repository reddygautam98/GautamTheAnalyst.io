from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page()
    page.goto('http://127.0.0.1:8080/contact.html')
    
    # Check elements in DOM
    f = page.query_selector("#enquiry")
    fbCard = page.query_selector("#fallbackCard")
    print("Form found:", f is not None)
    print("fbCard found:", fbCard is not None)
    if fbCard:
        print("fbCard hidden before:", fbCard.get_attribute("hidden"))
    
    # Check required fields
    reqs = page.evaluate("() => Array.from(document.querySelectorAll('#enquiry [required]')).map(el => ({name: el.name, id: el.id, type: el.type, val: el.value}))")
    print("Required fields:", reqs)
    
    # Fill fields
    page.fill("#enquiry-name", "Gautam Test")
    page.fill("#enquiry-email", "gautam@example.com")
    page.fill("#enquiry-msg", "Hello this is a test project enquiry with more details.")
    
    # Check submit button
    btn = page.query_selector("#enquiry button[type='submit']")
    print("Submit btn found:", btn is not None)
    
    # Intercept navigation or mailto
    page.click("#enquiry button[type='submit']")
    page.wait_for_timeout(500)
    
    if fbCard:
        print("fbCard hidden after:", fbCard.get_attribute("hidden"))
    
    errors = page.evaluate("() => Array.from(document.querySelectorAll('#enquiry [aria-invalid=\"true\"]')).map(el => ({id: el.id, name: el.name}))")
    print("Aria-invalid fields after submit:", errors)
    
    sent = page.query_selector("#sent")
    if sent:
        print("sent hidden after:", sent.get_attribute("hidden"), "text:", sent.inner_text()[:40])
    
    b.close()
