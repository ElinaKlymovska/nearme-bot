import asyncio
import os
import pickle
import random
from playwright.async_api import TimeoutError as PlaywrightTimeoutError


class Login:
    def __init__(self, page, action):
        self.page = page
        self.action = action

    async def login(self, username: str, password: str):
        try:
            await self.page.goto("https://www.tiktok.com/login/phone-or-email/email")
            await asyncio.sleep(random.uniform(3, 7))
            await self.page.fill('input[name="username"]', username)
            await self.page.fill("//input[@type='password']", password)
            await self.page.click('button[type="submit"]')

            if await self.action.detect_and_handle_captcha():
                await self.page.click('button[type="submit"]')

            await self.page.wait_for_selector("button[data-e2e='top-login-button']", timeout=10000)
            print("Logged in")
        except Exception as e:
            print(f"An error occurred during login: {e}")

    async def get_cookies(self, username: str, password: str):
        cookie_file = f"files/cookies/{username}_cookies"
        if os.path.exists(cookie_file):
            print("Cookies exist! Loading cookies...")
            await self.load_cookies(cookie_file)
            await self.page.reload()
            await asyncio.sleep(5)
            if await self.check_login_status():
                print("User is not logged in, re-attempting login")
                await self.relogin_and_save_cookies(username, password, cookie_file)
        else:
            print("No cookies found! Trying to log in...")
            await self.relogin_and_save_cookies(username, password, cookie_file)

    async def check_login_status(self):
        try:
            await self.page.wait_for_selector("button[data-e2e='top-login-button']", timeout=10000)
            print("Login button is present, user is not logged in")
            return True
        except PlaywrightTimeoutError:
            print("Login button is not present, user is logged in")
            return False

    async def load_cookies(self, cookie_file):
        with open(cookie_file, "rb") as cookies_file:
            cookies = pickle.load(cookies_file)
            for cookie in cookies:
                cookie['domain'] = ".tiktok.com"
            await self.page.context.add_cookies(cookies)
            print("Cookies loaded")

    async def relogin_and_save_cookies(self, username: str, password: str, cookie_file: str):
        await self.login(username, password)
        cookies = await self.page.context.cookies()
        with open(cookie_file, "wb") as cookies_file:
            pickle.dump(cookies, cookies_file)
        print("Cookies saved")
