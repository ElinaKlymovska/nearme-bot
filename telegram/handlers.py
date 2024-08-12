# telegram/handlers.py

from aiogram import Router, types, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import telegram.keyboards as kb
from database.init_db import get_session
from database.data_handler import DataHandler
from tiktok.caller_tiktok_bot import CallerTikTokBot

router = Router()


class LoginForm(StatesGroup):
    username = State()
    password = State()
    hashtags = State()
    comments = State()
    messages = State()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Привіт!", reply_markup=kb.main)


@router.message(F.text == "Create new request to tiktok processing")
async def enter_tiktok_credential(message: types.Message, state: FSMContext):
    await state.set_state(LoginForm.username)
    await message.answer("Please enter your TikTok username:")


@router.message(StateFilter(LoginForm.username))
async def process_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(LoginForm.password)
    await message.answer("Please enter your TikTok password:")


@router.message(StateFilter(LoginForm.password))
async def process_password(message: types.Message, state: FSMContext):
    data = await state.get_data()
    username = data.get("username")
    password = message.text
    async for session in get_session():
        await DataHandler.save_credential(username, password, session)
    await state.update_data(password=password)
    await state.set_state(LoginForm.hashtags)
    await message.answer("Please enter the hashtags (comma-separated):")


@router.message(StateFilter(LoginForm.hashtags))
async def process_hashtags(message: types.Message, state: FSMContext):
    hashtags = message.text.split(",")
    await state.update_data(hashtags=hashtags)
    await state.set_state(LoginForm.comments)
    await message.answer("Please enter the comments (underline-separated):")


@router.message(StateFilter(LoginForm.comments))
async def process_comments(message: types.Message, state: FSMContext):
    comments = message.text.split("_")
    await state.update_data(comments=comments)
    await state.set_state(LoginForm.messages)
    await message.answer("Please enter the messages (underline-separated):")


@router.message(StateFilter(LoginForm.messages))
async def process_messages(message: types.Message, state: FSMContext):
    messages = message.text.split("_")
    data = await state.get_data()
    username = data["username"]
    password = data["password"]
    hashtags = data["hashtags"]
    comments = data["comments"]

    chat_id = message.chat.id

    async for session in get_session():
        credential = await DataHandler.get_credential_by_username(username, session)
        if credential:
            await DataHandler.create_tiktok_request(
                chat_id, credential, hashtags, comments, messages, session
            )
            await message.answer("TikTok request created successfully.")
        else:
            await message.answer(f"Credential for username '{username}' not found.")

    await state.clear()


@router.message(F.text == "Choose from existed requests")
async def choose_request(message: types.Message):
    async for session in get_session():
        requests = await DataHandler.get_all_requests(session)

        # Ensure all lazy-loaded attributes are loaded
        for request in requests:
            await session.refresh(request, ['credential', 'hashtags', 'comments', 'messages'])

    if not requests:
        await message.answer("No requests available.")
        return

    keyboard = await kb.get_choose_request_keyboard(requests)

    await message.answer("Choose a request:", reply_markup=keyboard)


@router.callback_query(lambda query: query.data.startswith('choose_request:'))
async def process_choose_request(callback_query: types.CallbackQuery, state: FSMContext):
    # Extract request ID from callback data
    request_id = int(callback_query.data.split(':')[-1])

    # Fetch request details from database
    async for session in get_session():
        request = await DataHandler.get_request_by_id(request_id, session)
        if not request:
            await callback_query.answer("Request not found.", show_alert=True)
            return

        # Process request details as needed
        # For example, you can retrieve and display detailed information about the request
        hashtags_str = ", ".join([hashtag.hashtag for hashtag in request.hashtags])
        comments_str = ", ".join([comment.comment for comment in request.comments])
        messages_str = ", ".join([message.message for message in request.messages])

        response_text = (
            f"<b>Request Details:</b>\n"
            f"<b>Username:</b> {request.credential.username}\n"
            f"<b>Hashtags:</b> {hashtags_str}\n"
            f"<b>Comments:</b> {comments_str}\n"
            f"<b>Messages:</b> {messages_str}"
        )

        # Respond to the user with the request details
        await callback_query.message.edit_text(response_text, parse_mode='HTML')

        await CallerTikTokBot.start_tiktok_bot(request)


