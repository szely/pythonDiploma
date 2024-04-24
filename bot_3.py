from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo


NAME = "@Our_HandyBOT"
TOKEN = "6941628121:AAHT8TIRFVFZT3U6mgNwqQjYdMYyVgqkT5I"
bot = Bot(TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Открыть веб страницу', web_app=WebAppInfo(url='https://github.com/szely/Python_23/blob/82a4d0e0d1ae613a10601baaec8f1e7c593d8d75/index.html')))
    await message.answer('Привет мой друг!', reply_markup=markup)


executor.start_polling(dp)