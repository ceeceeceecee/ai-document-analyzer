import asyncio
from playwright.async_api import async_playwright

APP_URL = "http://localhost:8501"
VIEWPORT = {"width": 1280, "height": 900}
OUTPUT_DIR = "/screenshots"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport=VIEWPORT, locale="de-DE")
        page = await context.new_page()
        await page.goto(APP_URL, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)
        await page.screenshot(path=f"{OUTPUT_DIR}/streamlit-ui.png", full_page=False)
        print("OK: streamlit-ui.png")
        await browser.close()

asyncio.run(main())
