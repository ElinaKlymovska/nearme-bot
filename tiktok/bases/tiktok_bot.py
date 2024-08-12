from playwright.async_api import Page

from database.models import TikTokRequest
from tiktok.bases.action import Action
from tiktok.bases.locators import USERS_TAB_ITEM_SELECTOR, PROFILE_CONTAINER, PROFILE_LINK, NEXT_VIDEO


class TikTokBot:
    def __init__(self, page: Page, action: Action):
        self.page = page
        self.action = action

    async def scenario_1(self, search_query, request: TikTokRequest):
        await self.action.fill_and_submit_search_form(search_query)
        await self.action.click_tab_item(USERS_TAB_ITEM_SELECTOR)

        profile_urls = await self.action.scroll_and_collect_links(PROFILE_CONTAINER, PROFILE_LINK, 20)

        await self.navigate_to_user_profiles(profile_urls, request)

    async def navigate_to_user_profiles(self, profile_urls: list, request: TikTokRequest):
        try:
            for index, full_url in enumerate(profile_urls):
                print(f"Navigating to: {full_url}")
                try:
                    await self.page.goto(full_url)
                    await self.page.wait_for_load_state('networkidle')
                    await self.page.wait_for_timeout(4000)
                    await self.action.detect_and_handle_captcha()

                    await self.comment_scenario_1(request)

                    await self.action.click_follow_and_message(request)

                except Exception as e:
                    print(f"Error during link navigation to {full_url}: {e}")

        except Exception as e:
            print(f"An error occurred: {e}")

    async def comment_scenario_1(self, request: TikTokRequest):
        await self.action.find_and_click_first_video()
        await self.action.enter_comment(request.comments)

        for i in range(5):
            await self.action.click_button(NEXT_VIDEO)
            await self.action.enter_comment(request.comments)

        await self.action.go_back_to_previous_page()
