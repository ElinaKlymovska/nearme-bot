import sys
import logging

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Dispatcher

from telegram.bot_instance import TelegramBot
from telegram.handlers import router
from database.init_db import init_db


async def telegram():
    await init_db()
    bot = TelegramBot
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await dp.start_polling(bot)


async def telegram_bot_starter():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        await telegram()
    except KeyboardInterrupt:
        print('Exit')
