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
from bot.db.db import db_table_val, find_user_id, get_user_email
from bot.other_methods.dash_board import paint_waterfall_chart
from bot.db.db import profitability_info
import datetime
logger = logging.getLogger(__name__)

current_date = datetime.datetime.now().strftime('%d.%m.%Y')

router = Router()

class Form(StatesGroup):
    SEARCH = State()
    EMAIL_ADR = State()


@router.message(F.text == 'Аналитика 📊')
async def file_manager(message: types.Message, bot: Bot):
    data_for_image = profitability_info(current_date)
    if data_for_image == 0:
        await message.answer(f'На {current_date} данных нет!')
    else:
        image_path = paint_waterfall_chart(data_for_image, message.message_id)
        await message.answer(f'Данные на {current_date}:')
        await message.answer_photo(FSInputFile(image_path))
        os.remove(image_path)