from playwright.sync_api import sync_playwright


SBR_WS_CDP = 'wss://brd-customer-hl_4907aa65-zone-scraping_browser1:f4fww9uxfict@brd.superproxy.io:9222'

with sync_playwright() as playwright:
    browser = playwright.chromium.connect_over_cdp(SBR_WS_CDP)
    page = browser.new_page()
    page.goto('https://www.google.com')
    page.pause()

