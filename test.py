from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless = True)

    page = browser.new_page()
    page.goto("https://www.hindustantimes.com/india-news/pm-modi-us-visit-modi-ji-thali-new-jersey-restaurant-year-of-millet-101686530395089.html")

    # Save the screenshot
    page.screenshot(path="screenshot.jpeg")