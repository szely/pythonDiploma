import telebot
from telebot import types
import webbrowser
import sqlite3
import requests
import json
from currency_converter import CurrencyConverter

NAME = "@Our_HandyBOT"
TOKEN = "6941628121:AAHT8TIRFVFZT3U6mgNwqQjYdMYyVgqkT5I"
bot = telebot.TeleBot(TOKEN)

# Конвектор валют
currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, введите сумму')
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат, впишите сумму')
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
        btn4 = types.InlineKeyboardButton('Другое значение', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Число должно быть больше 0')
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = round(currency.convert(amount, values[0], values[1]), 2)
        bot.send_message(call.message.chat.id, f'Получается: {res}. Можете заново ввести сумму:')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару значений через слеш')
        bot.register_next_step_handler(call.message, my_currency)

def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = round(currency.convert(amount, values[0], values[1]), 2)
        bot.send_message(message.chat.id, f'Получается: {res}. Можете заново ввести сумму:')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, 'Что то не так. Впишите значения заново:')
        bot.register_next_step_handler(message, my_currency)


# # Погода
# API = 'b1e8c709dad0d3e2cc3992f3f91c376d'
#
# @bot.message_handler(commands=['start'])
# def start(message):
#     bot.send_message(message.chat.id, 'Привет, рад тебя видеть! Напиши название своего города')
#
# @bot.message_handler(content_types=['text'])
# def get_weather(message):
#     city = message.text.strip().lower()
#     res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
#     if res.status_code == 200:
#         data = json.loads(res.text)
#         temp = data["main"]["temp"]
#         bot.reply_to(message, f'Сейчас погода: {temp}')
#         image = 'sunny.png' if temp > 5.0 else 'cloudy.png'
#         file = open('./' + image, 'rb')
#         bot.send_photo(message.chat.id, file)
#     else:
#         bot.reply_to(message, 'Город указан не верно')


# Бот для работы с базой данных
# name = ''
#
# @bot.message_handler(commands=['start'])
# def start(message):
#     conn = sqlite3.connect('db.sql')
#     cur = conn.cursor()
#     cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
#     conn.commit()
#     cur.close()
#     conn.close()
#
#     bot.send_message(message.chat.id, 'Привет сейчас тебя зарегистрируем! Ввведите Ваше имя')
#     bot.register_next_step_handler(message, user_name)
# #
# def user_name(message):
#     global name
#     name = message.text.strip()
#     bot.send_message(message.chat.id, 'Ввведите пароль')
#     bot.register_next_step_handler(message, user_pass)
#
# def user_pass(message):
#     password = message.text.strip()
#     conn = sqlite3.connect('db.sql')
#     cur = conn.cursor()
#     cur.execute("INSERT INTO users(name, pass) VALUES ('%s', '%s')" % (name, password))
#     conn.commit()
#     cur.close()
#     conn.close()
#     markup = types.InlineKeyboardMarkup()
#     markup.add(types.InlineKeyboardButton('Список пользователей', callback_data ='users'))
#     bot.send_message(message.chat.id, 'Пользователь зарегистрирован', reply_markup=markup)
#
# @bot.callback_query_handler(func=lambda call: True)
# def callback(call):
#     conn = sqlite3.connect('db.sql')
#     cur = conn.cursor()
#     cur.execute('SELECT * FROM users')
#     users = cur.fetchall()
#     info = ''
#     for el in users:
#         info += f'Имя: {el[1]}, Пароль: {el[2]}\n'
#     cur.close()
#     conn.close()
#     bot.send_message(call.message.chat.id, info)


# Бот с комндами и кнопками
#
# @bot.message_handler(commands=['start'])
# def start(message):
#     markup = types.ReplyKeyboardMarkup()
#     btn1 = types.KeyboardButton('Перейти на сайт')
#     markup.row(btn1)
#     btn2 = types.KeyboardButton('Удалить фото')
#     btn3 = types.KeyboardButton('Изменить текст')
#     markup.row(btn2, btn3)
#     file = open('./image1.jpeg', 'rb')
#     bot.send_photo(message.chat.id, file, reply_markup=markup)
#     # bot.send_message(message.chat.id, 'Привет', reply_markup=markup)
#     bot.register_next_step_handler(message, on_click)
#
# def on_click(message):
#     if message.text == 'Перейти на сайт':
#         bot.send_message(message.chat.id, 'Website is open')
#     elif message.text == 'Удалить фото':
#         bot.send_message(message.chat.id, 'Deleted')
#
#
# @bot.message_handler(content_types=['photo', 'audio'])
# def get_photo(message):
#     markup = types.InlineKeyboardMarkup()
#     btn1 = types.InlineKeyboardButton('Перейти на сайт', url='https://google.com')
#     markup.row(btn1)
#     btn2 = types.InlineKeyboardButton('Удалить фото', callback_data='delete')
#     btn3 = types.InlineKeyboardButton('Изменить текст', callback_data='edit')
#     markup.row(btn2, btn3)
#     bot.reply_to(message, 'Какое красивое фото', reply_markup=markup)
#
# @bot.callback_query_handler(func=lambda callback: True)
# def callback_message(callback):
#     if callback.data =='delete':
#         bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
#     elif callback.data =='edit':
#         bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)
#
#
# @bot.message_handler(commands=['site', 'website'])
# def site(message):
#     webbrowser.open('https://itproger.com')
#
# # @bot.message_handler(commands=['start', 'main', 'hello'])
# # def main(message):
# #     bot.send_message(message.chat.id, f'Привет {message.from_user.first_name} {message.from_user.last_name}')
#
# @bot.message_handler(commands=['help'])
# def main(message):
#     bot.send_message(message.chat.id, '<b>Help</b> <em><u>information</u></em>', parse_mode='html')
#
# @bot.message_handler()
# def info(message):
#     if message.text.lower() == 'привет':
#         bot.send_message(message.chat.id, f'Привет {message.from_user.first_name} {message.from_user.last_name}')
#     elif message.text.lower() == 'id':
#         bot.reply_to(message, f'ID: {message.from_user.id}')
#




bot.polling(none_stop=True)