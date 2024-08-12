from playwright.async_api import async_playwright


class PlaywrightSetup:
    def __init__(self):
        self.browser = None
        self.playwright = None

    async def create_browser(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)
        return self.browser

    async def close_browser(self):
        await self.browser.close()
        await self.playwright.stop()

    async def create_page_with_url(self, url):
        browser = await self.create_browser()
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(url)
        title = await page.title()
        print(f"Title for {url}: {title}")
        return page
