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
from bot.keyboards.user_keyboards import create_buttons, tools_buttoms, choose_send_buttoms, back_choose_send_find_buttoms
from bot.other_methods.other_methods import create_dirs_files_map, create_path_buttons
from bot.other_methods.to_email import send_email
from bot.other_methods.find_file import search_dict_by_key_part, swapped_dict
from bot.other_methods.speach_rec import convert_to_wav, speach_rec
import logging
import sqlite3

logger = logging.getLogger(__name__)


class Form(StatesGroup):
    # MAIN_MENU = State()
    SEARCH = State()
    # PARSING_WORD = State()
    # PARSING_NUMBER = State()
    # HELP_MENU = State()
    # FAQ_MENU = State()
    # TO_BOT = State()

router = Router()
@router.message(F.text == 'Сканер номера вагона 🖋')
async def scan_vagon_number(message: types.Message):
    await message.answer("Ок", reply_markup=choose_send_buttoms().as_markup(one_time_keyboard=True, resize_keyboard=True))


