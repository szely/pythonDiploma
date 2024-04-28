import os
from dotenv import load_dotenv
import asyncio
from aiogram import Bot, Dispatcher
from bot.handlers import user_handlers, scaner_handlers, file_manager_handlers, analitics_handlers
import logging
from logging.handlers import RotatingFileHandler
import sqlite3


logging.basicConfig(filename='bot.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)  # Устанавливаем уровень логирования

# настроим rfl
handler = RotatingFileHandler('bot.log', maxBytes=1, backupCount=1)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(handler)

# Запуск бота
async def main():
    load_dotenv('.env')
    token = os.getenv("TOKEN_API")
    bot = Bot(token)
    dp = Dispatcher()

    dp.include_routers( user_handlers.router, file_manager_handlers.router, scaner_handlers.router, analitics_handlers.router)

    # await bot.delete_webhook(drop_pending_updates=True)
    # try:
    await dp.start_polling(bot)
    # except Exception as _ex:
    #     print(f'There is an exception - {_ex}')


if __name__ == "__main__":
    asyncio.run(main())