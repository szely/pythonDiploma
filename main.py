import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import CallbackQuery, FSInputFile
from pathlib import Path
from to_email import send_email
import reg_data
import os
from dotenv import load_dotenv
import logging
from bot.handlers.user_handlers import register_user_handlers


def register_handler(dp: Dispatcher) -> None:
    register_user_handlers(dp)

async def main() -> None:
    """Entry point
    """
    load_dotenv('.env')

    token = os.getenv("TOKEN_API")
    bot = Bot(token)
    dp = Dispatcher(bot)

    register_handler(dp)

    try:
        await dp.start_polling()
    except Exception as _ex:
        print(f'There is an exception - {_ex}')


if __name__ == "__main__":
    asyncio.run(main())