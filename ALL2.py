

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


def create_dirs2(path1):
    i = 0
    path = Path(path1)
    dirs = {}
    for item in path.rglob("*"):
        if item.is_dir():
            dirs[i] = {'type': 'folder', 'path': str(item), 'name': str(item.name), 'parants': str(item.parent), 'elem':[]}
            # path2 = Path(dirs[i]['path'])
            # for item2 in path2.iterdir():
            #     dirs[i]['elem'].append(item2.name)

        # if item.name != '.DS_Store':
        #     dirs[i] = {'path': str(item), 'name': str(item.name), 'parants' : str(item.parent)}
        # dirs[i] = {'name': str(item.name)}
            i += 1
    return dirs

ff = create_dirs2(my_directory)
print(ff)

def create_file_buttons(path1):
    path = Path(path1)
    the_dict = []
    for item in path.iterdir():
        if item.name !='.DS_Store':
            the_dict.append(item.name)
    return the_dict

print(create_file_buttons(ff[0]['path']))
f = create_file_buttons(my_directory)

def creat_buttom(dir):
    markup = types.InlineKeyboardMarkup()
    # n = 0
    files = create_file_buttons(dir)
    # while n in files.values():
    #     markup.append(types.ReplyKeyboardMarkup(resize_keyboard=True))
    btns1 = ''
    for i in files:
        btns1 = (types.InlineKeyboardButton(f"{i}", callback_data=str(i)))
        markup.add(btns1)
    bt = types.InlineKeyboardButton('Назад', callback_data='Назад')
    markup.add(bt)

    return markup

print(creat_buttom(my_directory))

@bot.message_handler(commands=['start'])
def start(message):
    global f
    markup = creat_buttom(ff[0]['path'])
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Выбери файл".format(
                         message.from_user), reply_markup=markup)




# @bot.message_handler(content_types=['text'])
def func(message):
    # if message.text in create_dirs(my_directory):
    dirs = create_dirs2(my_directory)
    path = dirs.get(message)
    markup = creat_buttom(path)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Выбери файл".format(message.from_user), reply_markup=markup)

def func_1(message):
    global msg
    print(msg)
    dirs = create_dirs(my_directory)
    path = dirs.get(msg)
    print(path)
    file = open(f"{str(path + '/' + message.text)}", "rb")
    bot.send_document(message.chat.id, file)

def func_2(message):
    global msg
    # if message.text in create_dirs(my_directory):
    dirs = create_dirs(my_directory)
    path = (dirs.get(msg)).replace(str('/' + msg), '')
    print(path)
    markup = creat_buttom(path)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Выбери файл".format(message.from_user), reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def sort(callback):
    global msg
    global msg_2
    ch = '.'
    if callback.data == 'Назад':
        func_2(msg_2)
        msg_2 = callback.data
        msg = callback.data

    elif ch in callback.data:
        func_1(callback.data)
    else:
        dirs = create_dirs(my_directory)
        path = dirs.get(callback.data)
        markup = creat_buttom(path)
        bot.send_message(callback.message.chat.id,  text="Привет, {0.first_name}! Выбери файл".format(callback.message.from_user),
                         reply_markup=markup)


bot.polling(none_stop=True)