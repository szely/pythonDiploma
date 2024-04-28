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

number_path = {}
path_number = {}
path_buttons = {}
buttons = {}
message_choose = ''

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    # await state.set_state(Form.EMAIL_ADR)
    await message.answer(f'Привет {message.from_user.first_name}! Я твой персональный помощник HandyBOT!')
    if find_user_id(int(message.from_user.id)) != 0:
        await message.answer(f'{message.from_user.first_name}, ты уж есть в базе!')
        await message.answer("Выберите инструмент:", reply_markup=tools_buttoms().as_markup(resize_keyboard=True, one_time_keyboard=True))
    else:
        await state.set_state(Form.EMAIL_ADR)
        await message.answer(f'Для того, чтобы я мог отправлять тебе сообщения на эллектронную почту, укажи ее адрес.')

@router.message(Form.EMAIL_ADR)
async def reg_email(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    email = message.text
    db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username, email=email)
    await message.answer(f'Спасибо, {message.from_user.first_name}, адрес зарегистрирован!')
    await message.answer("Выберите инструмент",
                         reply_markup=tools_buttoms().as_markup(resize_keyboard=True, one_time_keyboard=True))
    await state.clear()

@router.message(Command("menu"))
async def main_menu(message: types.Message) -> None:
    await message.answer("Выберите инструмент",
                         reply_markup=tools_buttoms().as_markup(resize_keyboard=True, one_time_keyboard=True))
    logger.info("User %s started the conversation.", message.from_user)
