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
import logging
import sqlite3
from bot.db.db import find_wagon

logger = logging.getLogger(__name__)


class Form(StatesGroup):
    GET_NNS = State()
    GET_OSS = State()
    GET_SNAV = State()
    GET_SLV = State()
    GET_STOKP = State()
    GET_SONK = State()
    GET_SLKP = State()

router = Router()


nss = 0
oss = 0
snav = 0
slv = 0
stokp = 0
sonk = 0
slkp = 0

@router.message(F.text == 'Оценить вагон 🪙')
async def macro_info(message: types.Message,  state: FSMContext):
    await state.set_state(Form.GET_NNS)
    await message.answer('Введите нормативный срок службы вагона, лет:', reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))

@router.message(Form.GET_NNS)
async def get_nss(message: types.Message, state: FSMContext):
    global nss
    await state.update_data(name=message.text)
    nss = float(message.text.replace(',', '.'))
    await state.set_state(Form.GET_OSS)
    await message.answer('Введите остаточный срок службы, лет:', reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))

@router.message(Form.GET_OSS)
async def get_oss(message: types.Message, state: FSMContext):
    global oss
    await state.update_data(name=message.text)
    oss = float(message.text.replace(',', '.'))
    await state.set_state(Form.GET_SNAV)
    await message.answer('Введите стоимость нового аналога вагона, тыс. руб.:', reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))

@router.message(Form.GET_SNAV)
async def get_snav(message: types.Message, state: FSMContext):
    global snav
    await state.update_data(name=message.text)
    snav = float(message.text.replace(',', '.'))
    await state.set_state(Form.GET_SLV)
    await message.answer('Введите стоимость лома вагона, тыс. руб.:', reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))

@router.message(Form.GET_SLV)
async def get_slv(message: types.Message, state: FSMContext):
    global slv
    await state.update_data(name=message.text)
    slv = float(message.text.replace(',', '.'))
    await state.set_state(Form.GET_STOKP)
    await message.answer('Введите среднюю толшину обода КП, мм:', reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))

@router.message(Form.GET_STOKP)
async def get_stokp(message: types.Message, state: FSMContext):
    global stokp
    await state.update_data(name=message.text)
    stokp = float(message.text.replace(',', '.'))
    await state.set_state(Form.GET_SONK)
    await message.answer('Введите стоимость СОНК, тыс. руб.:', reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))

@router.message(Form.GET_SONK)
async def get_sonk(message: types.Message, state: FSMContext):
    global sonk
    await state.update_data(name=message.text)
    sonk = float(message.text.replace(',', '.'))
    await state.set_state(Form.GET_SLKP)
    await message.answer('Введите стоимость лома КП, тыс. руб.:', reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))

@router.message(Form.GET_SLKP)
async def get_slkp(message: types.Message, state: FSMContext):
    global nss
    global oss
    global snav
    global slv
    global stokp
    global sonk
    global slkp
    await state.update_data(name=message.text)
    slkp = float(message.text.replace(',', '.'))
    sv = round((snav - slv - sonk * 4) / nss * oss + slv + ((sonk - slkp) / 52 * (stokp - 24) + slkp) * 4, 3)
    await message.answer(f'Стоимость вагона по оценке затратным подходом: {sv} тыс. руб.')
    await state.clear()
    await message.answer("Вернуться в меню:",
                         reply_markup=back_menu().as_markup(one_time_keyboard=True,
                                                                                resize_keyboard=True))


