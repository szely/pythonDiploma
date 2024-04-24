

import telebot
from telebot import types
import os
from pathlib import Path

Token = "6519207648:AAG3nad5ENAnHfSXF-o5Hz39mceHn5B696E"
bot = telebot.TeleBot(Token)
my_directory = '/Users/a1234/Downloads/my_files'
my_directory.split()
msg = ''
msg_2 = ''
def create_dirs(path1):
    path = Path(path1)
    dirs = []
    for item in path.rglob("*"):
        if item.is_dir():
            dirs.append(str(item))
    return dirs

print(create_dirs(my_directory))
def create_dirs_file(path1):
    path = Path(path1)
    dirs = {}
    dirs2 ={}
    i = 0
    for item in path.rglob("*"):
        dirs[i] = str(item.parent)
        dirs2[str(item.parent)] = i
        i +=1
        res = [dirs, dirs2]
    return res

q1 = create_dirs_file(my_directory)[0]
q2 = create_dirs_file(my_directory)[1]

def create_file_buttons(path1):
    path = Path(path1)
    the_dict = []
    for item in path.iterdir():
        if item.name !='.DS_Store':
            the_dict.append(item)
    return the_dict

print(create_file_buttons(my_directory))

def creat_buttom(dir):
    markup = types.InlineKeyboardMarkup()
    # n = 0
    files = create_file_buttons(dir)
    # while n in files.values():
    #     markup.append(types.ReplyKeyboardMarkup(resize_keyboard=True))
    btns1 = ''
    for i in files:
        btns1 = (types.InlineKeyboardButton(f"{i.name}", callback_data=str(i)))
        markup.add(btns1)
    bt = types.InlineKeyboardButton('Назад', callback_data=str(Path(dir).parent))
    markup.add(bt)

    return markup

print(creat_buttom(my_directory))

@bot.message_handler(commands=['start'])
def start(message):
    markup = creat_buttom(my_directory)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Выбери файл".format(
                         message.from_user), reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def sort(callback):
    global msg
    global f
    global msg_2
    msg_2 = callback.data
    if Path(callback.data).is_dir():
        msg = callback.data
        path = callback.data
        markup = creat_buttom(path)
        bot.send_message(callback.message.chat.id,  text="Привет, {0.first_name}! Выбери файл".format(callback.message.from_user),
                         reply_markup=markup)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif Path(callback.data).is_file():
        file = open(f"{callback.data}", "rb")
        bot.send_document(callback.message.chat.id, file)
        file.close()
        # bot.reply_backend(callback.message.chat.id, callback.message.message_id)
        # bot.send_message(callback.message.chat.id, callback.message.message_id - 1)
    else:
        path = f[msg]
        markup = creat_buttom(path)
        bt = types.InlineKeyboardButton('Назад', callback_data=msg)
        markup.add(bt)
        bot.send_message(callback.message.chat.id,  text="Привет, {0.first_name}! Выбери файл".format(callback.message.from_user), reply_markup=markup)



bot.polling(none_stop=True)