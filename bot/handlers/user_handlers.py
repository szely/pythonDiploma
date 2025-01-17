from aiogram import Bot, types
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from bot.keyboards.user_keyboards import tools_buttoms
import logging
from bot.db.db import db_table_val, find_user_id
from bot.other_methods.to_email import check_address


logger = logging.getLogger(__name__)

router = Router()


# Создание экземпляра класса состояний для создания последовательности получения и отправки сообщений
class Form(StatesGroup):
    SEARCH = State()
    EMAIL_ADR = State()


# Создание глобальных переменных необходимых для работы файлового менеджера (проводника)
number_path = {}
path_number = {}
path_buttons = {}
buttons = {}
message_choose = ''


# Стартовая команда. Осуществляется проверка регистрации пользователя в БД.
@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    logger.info("Пользователь %s id %s начал разговор.", message.from_user.first_name, message.from_user.id)
    await message.answer(f'Привет {message.from_user.first_name}! Я твой персональный помощник HandyBOT!')
    if find_user_id(int(message.from_user.id)) != 0:
        await message.answer(f'{message.from_user.first_name}, ты уж есть в базе!')
        await message.answer("Выберите инструмент:", reply_markup=tools_buttoms().as_markup(resize_keyboard=True, one_time_keyboard=True))
    else:
        await state.set_state(Form.EMAIL_ADR)
        await message.answer(f'Для того, чтобы я мог отправлять тебе сообщения на электронную почту, укажи ее адрес:')


# Регистрация адреса электронной почты, необходимого для отправки методом "НА почту".
@router.message(Form.EMAIL_ADR)
async def reg_email(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    email = message.text
    if check_address(email) == True:
        db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username, email=email)
        logger.info("Пользователь %s id %s зарегистрировал адрес электронной почты.", message.from_user.first_name, message.from_user.id)
        await message.answer(f'Спасибо, {message.from_user.first_name}, адрес зарегистрирован!')
        await message.answer("Выберите инструмент",
                         reply_markup=tools_buttoms().as_markup(resize_keyboard=True, one_time_keyboard=True))
        await state.clear()
    else:
        logger.error(f"Пользователь {message.from_user.first_name} id {message.from_user.id} ввел некорректный адресс электронной почты")
        await message.answer(f'Введен некорректный адрес электронной почты, попробуй снова:')


# Вызов основного меню.
@router.message(Command("menu"))
async def main_menu(message: types.Message) -> None:
    await message.answer("Выберите инструмент",
                         reply_markup=tools_buttoms().as_markup(resize_keyboard=True, one_time_keyboard=True))
    logger.info("Пользователь %s id %s начал разговор.", message.from_user.first_name, message.from_user.id)
