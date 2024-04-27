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
import sqlite3
from bot.db.db import find_wagon

logger = logging.getLogger(__name__)


class Form(StatesGroup):
    # MAIN_MENU = State()
    SEARCH = State()
    # PARSING_WORD = State()
    # PARSING_NUMBER = State()
    # HELP_MENU = State()
    # FAQ_MENU = State()
    # TO_BOT = State()
    FIND_NUM = State()

router = Router()
@router.message(F.text == 'Сканер номера вагона 🖋')
async def scan_vagon_number(message: types.Message, state: FSMContext):
    await state.set_state(Form.FIND_NUM)
    await message.answer("Введите номер вагона")

@router.message(Form.FIND_NUM)
async def vagon_number(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(f'Информация по данному вагону:')
    res = find_wagon(message.text)
    for key, value in res.items():
        await message.answer(f'{key}: {value}')
    await message.answer("Вернуться в меню",
                         reply_markup=main_menu().as_markup(one_time_keyboard=True,
                                                                                resize_keyboard=True))



