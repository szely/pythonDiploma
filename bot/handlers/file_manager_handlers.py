from aiogram import Bot, types
from aiogram.types import CallbackQuery, FSInputFile
from aiogram import Router, F
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
from bot.db.db import db_table_val, find_user_id, get_user_email


logger = logging.getLogger(__name__)

router = Router()


# Создание экземпляра класса состояний для создания последовательности получения и отправки сообщений
class Form(StatesGroup):
    SEARCH = State()
    EMAIL_ADR = State()


# # Вызов в меня раздела "Отчетность" - проводник по структуре папок с отчетными документами
@router.message(F.text == 'Отчетность 🗄')
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
    logger.info("Пользователь %s id %s зашел в раздел 'Отчетность'", message.from_user.first_name, message.from_user.id)
    await message.answer("Куда отправлять файлы?", reply_markup=choose_send_buttoms().as_markup(one_time_keyboard=True, resize_keyboard=True))


# Выбор метода отправки файлов. В бот - файлы отправляются в чат.
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
    logger.info("Пользователь %s id %s выбрал метод отправки 'В бот'", message.from_user.first_name, message.from_user.id)
    await message.answer("Выберите файл или папку", reply_markup=this_button.as_markup())
    await message.answer("Можете изменить метод отправки, найти файл, или вернуться в меню", reply_markup=back_choose_send_find_buttoms().as_markup(one_time_keyboard=True, resize_keyboard=True))


# Выбор метода отправки файлов. На почту - файлы отправляются на указанную пользователем при регистрации электронную почту.
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
    logger.info("Пользователь %s id %s выбрал метод отправки 'На почту'", message.from_user.first_name, message.from_user.id)
    await message.answer("Выберите файл или папку", reply_markup=this_button.as_markup())
    await message.answer("Можете изменить метод отправки, найти файл, или вернуться в меню", reply_markup=back_choose_send_find_buttoms().as_markup(one_time_keyboard=True, resize_keyboard=True))


# Данный блок позволяет изменить способ отправки (в бот/на почту)
@router.message(F.text == "Метод отправки 📨")
async def methods_send(message: types.Message):
    await message.answer("Куда отправлять файлы?", reply_markup=choose_send_buttoms().as_markup(one_time_keyboard=True, resize_keyboard=True))


# Возврат в основное меню
@router.message(F.text == 'Назад в меню ↩️')
async def methods_send(message: types.Message):
    await message.answer("Выберите инструмент",
                         reply_markup=tools_buttoms().as_markup(resize_keyboard=True, one_time_keyboard=True))


# Заново показывает структуру папок
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


# Вызов поиска файлов по структуре. Реализован и текстовый и голосовой поиск.
@router.message(F.text == "Поиск файлов 🔎")
async def find_file(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.SEARCH)
    logger.info("Пользователь %s id %s запустил поиск файлов", message.from_user.first_name, message.from_user.id)
    await message.answer('Напишите название файла или пришлите аудиосообщение!')


# ОБработчик поиска
@router.message(Form.SEARCH)
async def search(message: Message, state: FSMContext, bot: Bot) -> None:
    global number_path
    global path_number
    global path_buttons
    global buttons
    global message_choose
    await state.update_data(name=message.text)
    if message.text:
        text = message.text
        logger.info("Пользователь %s id %s ищет файл(ы) '%s' через текстовое сообщение", message.from_user.first_name, message.from_user.id, message.text)
        await message.answer('Ищу файлы')
    else:
        file_id = message.voice.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        file_name = Path("", f"{file_id}.ogg")
        await bot.download_file(file_path, destination=file_name, timeout=0)
        file_name_wav = convert_to_wav(file_name)
        logger.info("Пользователь %s id %s ищет файл(ы) '%s' через аудио сообщение", message.from_user.first_name, message.from_user.id, message.text)
        await message.answer('Ищу файлы')
        text = speach_rec(file_name_wav)
        os.remove(file_name)
        os.remove(file_name_wav)
    found_files_p_n = search_dict_by_key_part(path_number, text)
    if found_files_p_n:
        # file_name_wav = convert_to_wav(file_name)
        await message.answer('Получите файл(ы)!')
        if message_choose == 'В бот 🤖':
            for key in found_files_p_n:
                file = FSInputFile(key)
                logger.info("Для пользователя %s id %s найден(ы) файл(ы) '%s'", message.from_user.first_name,
                            message.from_user.id, key)
                await bot.send_document(message.chat.id, file)
        if message_choose == 'На почту 📩':
            for key in found_files_p_n:
                file_name = key.split('/')[-1]
                user_email = get_user_email(message.from_user.id)
                status = send_email(key, file_name,user_email)
                logger.info("Для пользователя %s id %s найден(ы) файл(ы) '%s'", message.from_user.first_name,
                            message.from_user.id, key)
                await message.answer(f'{status} "{file_name}"')
    else:
        logger.info("Для пользователя %s id %s не найдены файл(ы)", message.from_user.first_name,
                    message.from_user.id)
        await message.answer('Файл(ы) не найден(ы)!')
    await message.answer("Можете изменить метод отправки, найти файл, или вернуться в меню",
                         reply_markup=back_choose_send_find_buttoms().as_markup(one_time_keyboard=True,
                                                                                resize_keyboard=True))
    await state.clear()


# Навигация по структуре отчетности (проводник)
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
    if Path(number_path.get(int(callback.data))).is_file()and message_choose == 'В бот 🤖':
        file = FSInputFile(number_path.get(int(callback.data)))
        await bot.send_document(callback.message.chat.id, file)
    if Path(number_path.get(int(callback.data))).is_file() and message_choose == 'На почту 📩':
        user_email = get_user_email(callback.from_user.id)
        file_name = str(Path(number_path.get(int(callback.data)))).split('/')[-1]
        status = send_email(str(Path(number_path.get(int(callback.data)))), file_name, user_email)
        await callback.message.answer(f'{status} "{file_name}"')