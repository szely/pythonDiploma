from aiogram import Bot, types
from aiogram.types import CallbackQuery, FSInputFile
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import os
from dotenv import load_dotenv
from pathlib import Path
from bot.keyboards.user_keyboards import create_buttons, tools_buttoms, choose_send_buttoms, back_choose_send_find_buttoms, main_menu
from bot.other_methods.other_methods import create_dirs_files_map, create_path_buttons
from bot.other_methods.to_email import send_email
from bot.other_methods.find_file import search_dict_by_key_part, swapped_dict
from bot.other_methods.speach_rec import convert_to_wav, speach_rec
import logging
from bot.db.db import db_table_val, find_user_id
logger = logging.getLogger(__name__)


router = Router()

class Form(StatesGroup):
    SEARCH = State()
    EMAIL_ADR = State()



@router.message(F.text == 'Файловый менеджер 🗄')
async def file_manager(message: types.Message):
    global number_path
    global path_number
    global path_buttons
    global buttons
    load_dotenv('.env')
    my_directory = os.getenv("MY_DIRECTORY")
    load_dotenv('.env')
    number_path = create_dirs_files_map(my_directory)[0]
    path_number = create_dirs_files_map(my_directory)[1]
    path_buttons = create_path_buttons(my_directory)
    buttons = create_buttons(path_buttons, number_path, path_number)
    await message.answer("Куда отправлять файлы?", reply_markup=choose_send_buttoms().as_markup(one_time_keyboard=True, resize_keyboard=True))

@router.message(F.text == 'В бот 🤖')
async def file_manager(message: types.Message):
    global number_path
    global path_number
    global path_buttons
    global buttons
    global message_choose
    message_choose = message.text
    load_dotenv('.env')
    my_directory = os.getenv("MY_DIRECTORY")
    load_dotenv('.env')
    first_dir = os.getenv("FIRST_DIR")
    this_button = buttons.get(str(my_directory + first_dir))
    await message.answer("Выберите файл или папку", reply_markup=this_button.as_markup())
    await message.answer("Можете изменить метод отправки, найти файл, или вернуться в меню", reply_markup=back_choose_send_find_buttoms().as_markup(one_time_keyboard=True, resize_keyboard=True))
@router.message(F.text == "На почту 📩")
async def file_manager(message: types.Message):
    global number_path
    global path_number
    global path_buttons
    global buttons
    global message_choose
    message_choose = message.text
    load_dotenv('.env')
    my_directory = os.getenv("MY_DIRECTORY")
    load_dotenv('.env')
    first_dir = os.getenv("FIRST_DIR")
    this_button = buttons.get(str(my_directory + first_dir))
    await message.answer("Выберите файл или папку", reply_markup=this_button.as_markup())
    await message.answer("Можете изменить метод отправки, найти файл, или вернуться в меню", reply_markup=back_choose_send_find_buttoms().as_markup(one_time_keyboard=True, resize_keyboard=True))

@router.message(F.text == "Метод отправки 📨")
async def methods_send(message: types.Message):
    await message.answer("Куда отправлять файлы?", reply_markup=choose_send_buttoms().as_markup(one_time_keyboard=True, resize_keyboard=True))

@router.message(F.text == 'Назад в меню ↩️')
async def methods_send(message: types.Message):
    await message.answer("Выберите инструмент",
                         reply_markup=tools_buttoms().as_markup(resize_keyboard=True, one_time_keyboard=True))
@router.message(F.text == "Структура 🗄")
async def structure(message: Message) -> None:
    global number_path
    global path_number
    global path_buttons
    global buttons
    load_dotenv('.env')
    my_directory = os.getenv("MY_DIRECTORY")
    load_dotenv('.env')
    first_dir = os.getenv("FIRST_DIR")
    this_button = buttons.get(str(my_directory + first_dir))
    await message.answer("Выберите файл или папку", reply_markup=this_button.as_markup())
    await message.answer("Можете изменить метод отправки, найти файл, или вернуться в меню",
                         reply_markup=back_choose_send_find_buttoms().as_markup(one_time_keyboard=True,
                                                                                resize_keyboard=True))

@router.callback_query()
async def call(callback: CallbackQuery, bot: Bot):
    global number_path
    global path_number
    global path_buttons
    global buttons
    global message_choose
    if Path(number_path.get(int(callback.data))).is_dir():
        path = number_path.get(int(callback.data))
        markup = buttons.get(path)
        await callback.message.answer('Выберите папку или файл', reply_markup=markup.as_markup())
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        # await callback.message.answer("Можете изменить метод отправки или вернуться в меню",
        #                      reply_markup=back_choose_send_find_buttoms().as_markup(one_time_keyboard=True,
        #                                                                             resize_keyboard=True))
    if Path(number_path.get(int(callback.data))).is_file()and message_choose == 'В бот 🤖':
        file = FSInputFile(number_path.get(int(callback.data)))
        await bot.send_document(callback.message.chat.id, file)
        # await callback.message.answer("Можете изменить метод отправки или вернуться в меню",
                             # reply_markup=back_choose_send_find_buttoms().as_markup(one_time_keyboard=True,
                             #                                                        resize_keyboard=True))
    if Path(number_path.get(int(callback.data))).is_file() and message_choose == 'На почту 📩':
        file_name = str(Path(number_path.get(int(callback.data)))).split('/')[-1]
        status = send_email(str(Path(number_path.get(int(callback.data)))), file_name)
        await callback.message.answer(f'{status} "{file_name}"')
        # await callback.message.answer("Можете изменить метод отправки или вернуться в меню",
        #                      reply_markup=back_choose_send_find_buttoms().as_markup(one_time_keyboard=True,
        #                                                                             resize_keyboard=True))

