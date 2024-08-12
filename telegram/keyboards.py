from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List

from database.models import Credential, TikTokRequest

# Main keyboard markup
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Create new request to tiktok processing'), KeyboardButton(text='Choose from existed requests')],
    [KeyboardButton(text='Hashtags'), KeyboardButton(text='Comments'), KeyboardButton(text='Massages')]
], resize_keyboard=True)


async def get_choose_request_keyboard(requests: List[TikTokRequest]) -> InlineKeyboardMarkup:
    inline_keyboard = []

    for request in requests:
        hashtags_str = ", ".join([hashtag.hashtag for hashtag in request.hashtags])
        comments_str = ", ".join([comment.comment for comment in request.comments])
        messages_str = ", ".join([message.message for message in request.messages])

        button_text = (
            f"{request.credential.username}, {hashtags_str}, {comments_str}, {messages_str}"
        )

        button = InlineKeyboardButton(
            text=button_text,
            callback_data=f"choose_request:{request.id}"
        )

        inline_keyboard.append([button])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
