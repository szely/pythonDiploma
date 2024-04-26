from pathlib import Path
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from dotenv import load_dotenv
import os

# Создаем кнопки по заранее подготовленной структуре
def create_buttons(path_buttons, number_path, path_number):
    result = {}
    for key, value in path_buttons.items():
        result[key] = InlineKeyboardBuilder()
        for v in value:
            if Path(v).is_dir():
                name = ('📂 ' + str(v.split('/')[-1]))
            else:
                name = ('📃 ' + v.split('/')[-1])
            call = path_number.get(v)
            button = (types.InlineKeyboardButton(text=str(name), callback_data=str(call)))
            result[key].add(button)
            result[key].adjust(1)
            load_dotenv('.env')
            my_directory = os.getenv("MY_DIRECTORY")
        if str(Path(key).parent) != my_directory:
            m = int(path_number.get(str(Path(key).parent)))
            k ='↩️ Назад'
            n = (types.InlineKeyboardButton(text=str(k), callback_data=str(m)))
            result[key].add(n)
            result[key].adjust(1)
    return result

def tools_buttoms():
    builder = ReplyKeyboardBuilder()
    builder.button(text='Файловый менеджер')
    builder.button(text='Сканер номера вагона')
    builder.button(text='Сканер номера паспорта вагона')
    builder.adjust(1)
    return builder

def choose_send_buttoms():
    builder_type_send = ReplyKeyboardBuilder()
    builder_type_send.button(text='В бот 🤖')
    builder_type_send.button(text='На почту 📩')
    builder_type_send.adjust(2)
    return builder_type_send

def back_choose_send_find_buttoms():
    builder_type_send = ReplyKeyboardBuilder()
    builder_type_send.button(text='Метод отправки 📨')
    builder_type_send.button(text='Назад в меню ↩️')
    builder_type_send.button(text='Поиск файлов 🔎')
    builder_type_send.adjust(2)
    return builder_type_send