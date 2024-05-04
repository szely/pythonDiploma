import os
from dotenv import load_dotenv
import asyncio
from aiogram import Bot, Dispatcher
from bot.handlers import user_handlers, wagon_info_handlers, file_manager_handlers, analitics_handlers, macro_info_handlers, wagon_valuation_handlers
import logging

# Запуск логирования
logging.basicConfig(filename='bot.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Запуск бота
async def main():
    load_dotenv('.env')
    token = os.getenv("TOKEN_API")
    bot = Bot(token)
    dp = Dispatcher()

    dp.include_routers( user_handlers.router, file_manager_handlers.router, wagon_info_handlers.router, analitics_handlers.router, macro_info_handlers.router,  wagon_valuation_handlers.router)

    # await bot.delete_webhook(drop_pending_updates=True)
    # try:
    await dp.start_polling(bot)
    # except Exception as _ex:
    #     print(f'There is an exception - {_ex}')


if __name__ == "__main__":
    asyncio.run(main())