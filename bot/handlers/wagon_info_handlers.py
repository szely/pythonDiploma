from aiogram import Bot, types
from aiogram import Router, F
from aiogram.filters.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from bot.keyboards.user_keyboards import create_buttons, tools_buttoms, choose_send_buttoms, back_choose_send_find_buttoms, main_menu, back_menu, back_menu_info
import logging
from bot.db.db import find_wagon
from bot.other_methods.check_wagon_number import check_wagon_number, get_wagon_type


logger = logging.getLogger(__name__)


# Создание экземпляра класса состояний для создания последовательности получения и отправки сообщений
class Form(StatesGroup):
    FIND_NUM = State()


router = Router()


# Вывод информации о вагоне из БД
@router.message(F.text == 'Информация о вагоне ℹ️')
async def scan_wagon_number(message: types.Message, state: FSMContext):
    logger.info("Пользователь %s id %s зашел в раздел 'Информация о вагоне'", message.from_user.first_name, message.from_user.id)
    await state.set_state(Form.FIND_NUM)
    await message.answer("Введите номер вагона или вернитесь в меню:", reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))


# Вывод данных о вагоне из БД.
@router.message(Form.FIND_NUM)
async def wagon_number(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    number = message.text
    if len(number) == 8:
        try:
            int(number)
            if check_wagon_number(number):
                res = find_wagon(number)
                if res != 0:
                    await message.answer(f'Информация по вагону {message.text}:')
                    info_str = ''
                    for key, value in res.items():
                        info_str += f'{key}: {value}\n'
                    await message.answer(info_str)
                    await message.answer("Запустите поиск заново или вернитесь в меню:", reply_markup=back_menu_info().as_markup(one_time_keyboard=True, resize_keyboard=True))
                    await state.clear()
                else:
                    wagon_type = get_wagon_type(number)
                    await message.answer(f'Информация по вагону {message.text} в базе данных не найдена! Этот вагон отностится к типу {wagon_type}.')
                    await message.answer("Запустите поиск заново или вернитесь в меню:", reply_markup=back_menu_info().as_markup(one_time_keyboard=True, resize_keyboard=True))
                    await state.clear()
            else:
                await message.reply('Это не номер вагона!')
                await message.answer("Введите номер вагона или вернитесь в меню:",
                                     reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))
                if message.text == 'Назад в меню ↩️':
                    await state.clear()
        except Exception as e:
            logger.error(f"Пользователь {message.from_user.first_name} id {message.from_user.id} ввел неверный формат данных: {e}")
            await message.reply('Номер вагона должен быть введенн в числовом вормате! Длина введенного номера должна быть равна 8!')
            await message.answer("Введите номер вагона или вернитесь в меню:",
                                 reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))
            if message.text == 'Назад в меню ↩️':
                await state.clear()
    else:
        await message.reply('Номер вагона должен быть введен в числовом формате! Длина введенного номера должна быть равна 8!')
        await message.answer("Введите номер вагона или вернитесь в меню:",
                             reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))
        if message.text == 'Назад в меню ↩️':
            await state.clear()





