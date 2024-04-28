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


class Form(StatesGroup):
    SEARCH = State()
    EMAIL_ADR = State()

number_path = {}
path_number = {}
path_buttons = {}
buttons = {}
message_choose = ''

router = Router()

@router.message(F.text == "Поиск файлов 🔎")
async def find_file(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.SEARCH)
    await message.answer('Напишите название файла или пришлите аудиосообщение!')

@router.message(Form.SEARCH)
async def search(message: Message, state: FSMContext, bot: Bot) -> None:
    global number_path
    global path_number
    global path_buttons
    global buttons
    global message_choose
    await state.update_data(name=message.text)
    if message.text:
        # await state.update_data(name=message.text)
        text = message.text
        await message.answer('Ищу файлы')
        logger.info("User %s search file.", [message.from_user, message.text])
    else:
        file_id = message.voice.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        file_name = Path("", f"{file_id}.ogg")
        await bot.download_file(file_path, destination=file_name, timeout=0)
        file_name_wav = convert_to_wav(file_name)
        await message.answer('Ищу файлы')
        text = speach_rec(file_name_wav)
        os.remove(file_name)
        os.remove(file_name_wav)
    found_files_p_n = search_dict_by_key_part(path_number, text)
    if found_files_p_n:
        await message.answer('Получите файл(ы)!')
        if message_choose == 'В бот 🤖':
            for key in found_files_p_n:
                file = FSInputFile(key)
                await bot.send_document(message.chat.id, file)
        if message_choose == 'На почту 📩':
            for key in found_files_p_n:
                file_name = key.split('/')[-1]
                status = send_email(key, file_name)
                await message.answer(f'{status} "{file_name}"')
    else:
        await message.answer('Файл(ы) не найден(ы)!')
    await message.answer("Можете изменить метод отправки, найти файл, или вернуться в меню",
                         reply_markup=back_choose_send_find_buttoms().as_markup(one_time_keyboard=True,
                                                                                resize_keyboard=True))
