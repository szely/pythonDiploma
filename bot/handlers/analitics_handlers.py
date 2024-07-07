from aiogram import Bot, types
from aiogram.types import CallbackQuery, FSInputFile
from aiogram import Router, F
from aiogram.filters.state import StatesGroup, State
import os
from bot.keyboards.user_keyboards import create_buttons, tools_buttoms, choose_send_buttoms, back_choose_send_find_buttoms, main_menu, back_menu
import logging
from bot.other_methods.dash_board import paint_waterfall_chart, paint_tree_chart
from bot.db.db import profitability_info, get_wagon_info
import datetime


logger = logging.getLogger(__name__)

current_date = datetime.datetime.now().strftime('%d.%m.%Y')

router = Router()


# Создание эксземпляра класса состояний для создания последовательности получения и отправки сообщений
class Form(StatesGroup):
    SEARCH = State()
    EMAIL_ADR = State()


# Вызов в меня раздела "Аналитика" - выводит прднастроенные диаграмы на текущую даты на основе данных БД.
@router.message(F.text == 'Аналитика 📊')
async def file_manager(message: types.Message, bot: Bot):
    data_for_image = profitability_info(current_date)
    data_for_image_wg = get_wagon_info()
    logger.info("Пользователь %s id %s зашел в раздел 'Аналитика'", message.from_user.first_name, message.from_user.id)
    if data_for_image == 0:
        await message.answer(f'На {current_date} данных нет!')
        await message.answer("Вернуться в основное меню:",
                             reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))
    else:
        image_path = paint_waterfall_chart(data_for_image, message.message_id)
        image_path_wg = paint_tree_chart(data_for_image_wg, f'{message.message_id}_wg')
        await message.answer(f'Данные на {current_date}:')
        await message.answer_photo(FSInputFile(image_path))
        await message.answer_photo(FSInputFile(image_path_wg))
        os.remove(image_path)
        os.remove(image_path_wg)
        await message.answer("Вернуться в основное меню:",
                             reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))