from database.models import TikTokRequest, Hashtag
from tiktok.bases.action import Action
from tiktok.bases.login_system import Login
from tiktok.bases.webdriver_setup import PlaywrightSetup
from tiktok.bases.tiktok_bot import TikTokBot

from tiktok.bases.locators import USERS_TAB_ITEM_SELECTOR, PROFILE_CONTAINER, PROFILE_LINK


def validate_hashtag(hashtag) -> str:
    if isinstance(hashtag, Hashtag):
        hashtag = str(hashtag)
    elif not isinstance(hashtag, str):
        raise ValueError("Invalid input: hashtag must be a string or Hashtag object.")
    return hashtag if hashtag.startswith("#") else "#" + hashtag


class CallerTikTokBot:
    @staticmethod
    async def start_tiktok_bot(request: TikTokRequest):
        try:
            playwright_set_up = PlaywrightSetup()
            page = await playwright_set_up.create_page_with_url("https://www.tiktok.com/")
            action = Action(page, request.chat_id)

            login = Login(page, action)
            await login.get_cookies(request.credential.username, request.credential.password)

            tiktok_bot = TikTokBot(page, action)

            for hashtag in request.hashtags:
                await tiktok_bot.scenario_1(validate_hashtag(hashtag), request)

            await page.close()
        except Exception as e:
            print(f"An error occurred in CallerTikTokBot: {e}")
