import os
from dotenv import load_dotenv
import asyncio
from aiogram import Bot, Dispatcher
from bot.handlers import user_handlers


# Запуск бота
async def main():
    load_dotenv('.env')
    token = os.getenv("TOKEN_API")
    bot = Bot(token)
    dp = Dispatcher()

    dp.include_routers(user_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    # try:
    await dp.start_polling(bot)
    # except Exception as _ex:
    #     print(f'There is an exception - {_ex}')



if __name__ == "__main__":
    asyncio.run(main())