from aiogram import Bot, types
from aiogram import Router, F
from aiogram.filters.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from bot.keyboards.user_keyboards import create_buttons, tools_buttoms, choose_send_buttoms, back_choose_send_find_buttoms, main_menu, back_menu
import logging
from bot.db.db import find_wagon


logger = logging.getLogger(__name__)


# Создание экземпляра класса состояний для создания последовательности получения и отправки сообщений
class Form(StatesGroup):
    FIND_NUM = State()


router = Router()


# Вывод информации о вагоне из БД
@router.message(F.text == 'Информация о вагоне ℹ️')
async def scan_wagon_number(message: types.Message, state: FSMContext):
    await state.set_state(Form.FIND_NUM)
    await message.answer("Введите номер вагона:")


# Вывод данных о вагоне из БД.
@router.message(Form.FIND_NUM)
async def wagon_number(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    res = find_wagon(message.text)
    if res != 0:
        await message.answer(f'Информация по вагону {message.text}:')
        info_str = ''
        for key, value in res.items():
            info_str += f'{key}: {value}\n'
        await message.answer(info_str)
    else:
        await message.answer(f'Информация по вагону {message.text} не найдена!')
    await message.answer("Вернуться в меню:",
                         reply_markup=back_menu().as_markup(one_time_keyboard=True,
                                                                                resize_keyboard=True))
    await state.clear()



