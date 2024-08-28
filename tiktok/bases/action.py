import asyncio
import random

from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError

from database.models import TikTokRequest
from telegram.bot_instance import TelegramBot
from urllib.parse import urljoin

from tiktok.bases.locators import SEARCH_INPUT, SEARCH_BUTTON, CAPTCHA_CONTAINER, VIDEO_LINK, FOLLOW_BUTTON, \
    PRIMARY_MESSAGE_BUTTON, SECONDARY_MESSAGE_BUTTON, MESSAGE_INPUT, MESSAGE_SEND_BUTTON, COMMENT_INPUT, \
    COMMENT_SEND_BUTTON


class Action:
    def __init__(self, page: Page, chat_id: int):
        self.page = page
        self.chat_id = chat_id

    async def go_back_to_previous_page(self):
        try:
            await self.detect_and_handle_captcha()
            # Navigate back to the previous page
            await self.page.go_back(timeout=10000)
            print("Successfully navigated back to the previous page")
            await self.detect_and_handle_captcha()

        except PlaywrightTimeoutError:
            print("Timeout occurred while trying to go back to the previous page")

        except Exception as e:
            print(f"An error occurred while trying to go back: {e}")

    async def detect_and_handle_captcha(self):
        print(f"Starting detect_and_handle_captcha for chat_id: {self.chat_id}")
        try:
            await asyncio.sleep(2)
            captcha_element = await self.page.query_selector(CAPTCHA_CONTAINER)

            if captcha_element:
                print("CAPTCHA detected")
                await TelegramBot.send_message(self.chat_id, "CAPTCHA detected. Please solve it manually.")

                # Wait until CAPTCHA is solved
                while True:
                    captcha_solved = await self.page.query_selector(CAPTCHA_CONTAINER)
                    if not captcha_solved:
                        print("CAPTCHA solved")
                        return True
            else:
                print("No CAPTCHA detected")
                await asyncio.sleep(5)
                return False

        except PlaywrightTimeoutError:
            print("Timeout occurred while waiting for CAPTCHA detection")
            return False
        except Exception as e:
            print(f"Captcha detection error: {e}")
            return False

    async def scroll_and_collect_links(self, container_selector: str, link_selector: str, target_count: int):
        await self.detect_and_handle_captcha()
        await self.page.wait_for_selector(container_selector, timeout=30000)

        profile_urls = set()
        last_height = await self.page.evaluate('document.body.scrollHeight')

        while len(profile_urls) < target_count:
            # Scroll down the page
            await self.page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            await self.page.wait_for_timeout(2000)

            # Collect profile links
            profile_links = await self.page.query_selector_all(f'{container_selector} {link_selector}')
            for link in profile_links:
                href = await link.get_attribute('href')
                if href:
                    full_url = urljoin(self.page.url, href)
                    profile_urls.add(full_url)

            # Check if we've reached the end of the page
            new_height = await self.page.evaluate('document.body.scrollHeight')
            if new_height == last_height:
                break  # Exit loop if no new content is loaded
            last_height = new_height

        if not profile_urls:
            print("No profile links found")
            return
        print(f"Found {len(profile_urls)} profile links")

        return list(profile_urls)

    async def click_tab_item(self, tab_item_selector):
        try:
            await self.detect_and_handle_captcha()
            await self.page.wait_for_selector(tab_item_selector, timeout=30000)
            await self.page.click(tab_item_selector)
            print("Tab item clicked")
        except PlaywrightTimeoutError:
            print("Timeout occurred while waiting for the tab item")
        except Exception as e:
            print(f"An error occurred while clicking the tab item: {e}")

    async def fill_and_submit_search_form(self, search_query):
        try:
            await self.detect_and_handle_captcha()
            await self.page.wait_for_load_state('load')
            await self.detect_and_handle_captcha()
            search_input = await self.page.wait_for_selector(SEARCH_INPUT, timeout=30000)
            await search_input.fill(search_query)
            search_button = await self.page.wait_for_selector(SEARCH_BUTTON, timeout=30000)
            await search_button.click()
            print("Search form submitted")
            await self.detect_and_handle_captcha()
        except PlaywrightTimeoutError as e:
            print(f"Timeout occurred while searching by hashcode: {search_query} \n {e}")
        except Exception as e:
            print(f"An error occurred while searching by hashcode: {search_query} \n {e}")

    async def find_and_click_first_video(self):
        try:
            await self.detect_and_handle_captcha()

            await self.page.wait_for_selector(VIDEO_LINK, timeout=30000, state='visible')

            # Query the first element matching the XPath
            video_element = await self.page.query_selector(VIDEO_LINK)

            if video_element:
                # Extract the href attribute (for logging purposes)
                video_url = await video_element.get_attribute('href')
                print(f"Found video link: {video_url}")

                # Click the video link
                await video_element.click()
                print("Video link clicked successfully")
            else:
                print("No video link found")
        except PlaywrightTimeoutError:
            print("Timeout occurred while waiting for the video link")
        except Exception as e:
            print(f"An error occurred while trying to click the video link: {e}")

    async def click_follow_and_message(self, request: TikTokRequest):
        try:
            await self.detect_and_handle_captcha()

            # Follow button logic
            follow_button = await self.page.query_selector(FOLLOW_BUTTON)
            if follow_button:
                follow_button_text = await follow_button.text_content()
                if follow_button_text.lower() == "follow":
                    await self.click_button(FOLLOW_BUTTON)
                    await self.page.wait_for_selector(f"{FOLLOW_BUTTON}[aria-label*='Following']", timeout=30000)
                else:
                    print("Already following the user, skipping follow step")
            else:
                print("Follow button not found")

            # Message button logic
            message_button = await self.page.query_selector(PRIMARY_MESSAGE_BUTTON)
            if not message_button:
                message_button = await self.page.query_selector(SECONDARY_MESSAGE_BUTTON)

            if message_button:
                await message_button.click()
                await self.enter_message(request.messages)
            else:
                await asyncio.sleep(1000)
                print("Message button not found")

        except PlaywrightTimeoutError as e:
            print(f"Timeout occurred while following and messaging: {e}")
        except Exception as e:
            print(f"An error occurred while following and messaging: {e}")

    async def click_button(self, button_selector: str, button_text: str = None):
        try:
            await self.page.wait_for_selector(button_selector, timeout=30000)
            if button_text:
                button = await self.page.query_selector(f"text={button_text}")
                if button:
                    await button.click()
                    print(f"Button with text '{button_text}' clicked")
                else:
                    print(f"No button with text '{button_text}' found")
            else:
                await self.page.click(button_selector)
                print(f"Button with selector '{button_selector}' clicked")
        except PlaywrightTimeoutError:
            print(f"Timeout occurred while waiting for the button with selector '{button_selector}'")
        except Exception as e:
            print(f"An error occurred while clicking the button with selector '{button_selector}': {e}")

    async def enter_text_and_click_button(self, input_selector: str, button_selector: str, text: str, button_text: str):
        try:
            # Wait for the input area to be visible
            await self.page.wait_for_selector(input_selector, timeout=30000)

            # Focus on the input area and clear any existing content
            input_element = await self.page.query_selector(input_selector)
            if input_element:
                await input_element.focus()
                await input_element.evaluate('element => element.value = ""')  # Clear the input field
                await self.page.keyboard.type(str(text))
                print(f"{button_text} '{text}' entered successfully")

                # Wait for the button to appear and click it
                await self.page.wait_for_selector(button_selector, timeout=30000)
                await self.page.click(button_selector)
                print(f"{button_text} button clicked")
            else:
                print(f"{button_text} input area not found")
        except PlaywrightTimeoutError:
            print(f"Timeout occurred while waiting for the {button_text} input area or button")
        except Exception as e:
            print(f"An error occurred while entering {button_text}: {e}")

    async def enter_message(self, messages: list):
        message = random.choice(messages)
        await self.enter_text_and_click_button(MESSAGE_INPUT, MESSAGE_SEND_BUTTON, message, "Message")

    async def enter_comment(self, comments: list):
        comment_text = random.choice(comments)
        await self.enter_text_and_click_button(COMMENT_INPUT, COMMENT_SEND_BUTTON, comment_text, "Comment")
