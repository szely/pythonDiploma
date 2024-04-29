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
from bot.keyboards.user_keyboards import create_buttons, tools_buttoms, choose_send_buttoms, back_choose_send_find_buttoms, main_menu, back_menu
from bot.other_methods.other_methods import create_dirs_files_map, create_path_buttons
from bot.other_methods.to_email import send_email
from bot.other_methods.find_file import search_dict_by_key_part, swapped_dict
from bot.other_methods.speach_rec import convert_to_wav, speach_rec
from bot.other_methods.get_currency import get_currency_rate
import logging
import sqlite3
from bot.db.db import find_wagon

logger = logging.getLogger(__name__)


class Form(StatesGroup):
    # MAIN_MENU = State()
    # SEARCH = State()
    # PARSING_WORD = State()
    # PARSING_NUMBER = State()
    # HELP_MENU = State()
    # FAQ_MENU = State()
    # TO_BOT = State()
    FIND_NUM = State()

router = Router()

import requests
from aiogram import types

@router.message(F.text == 'Макроинформация 🌎')
async def macro_info(message: types.Message):
    usd_rub = get_currency_rate(['USD', 'RUB'])
    eur_usd = get_currency_rate(['EUR', 'RUB'])
    await message.answer(f'Текущий курс ЦБ РФ:\nUSD/RUB = {usd_rub}руб.\nEUR/RUB = {eur_usd}руб.')
    await message.answer("Вернуться в меню:",
                         reply_markup=back_menu().as_markup(one_time_keyboard=True,
                                                                                resize_keyboard=True))


