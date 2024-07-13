from aiogram import Router, F
from bot.keyboards.user_keyboards import back_menu, currency_cnverter, currency
from bot.other_methods.get_currency import get_currency_rate
from bot.other_methods.other_methods import currency_map
import logging
from aiogram import types
from aiogram.filters.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


logger = logging.getLogger(__name__)

router = Router()

class Form(StatesGroup):
    FIRST_CUR = State()
    SECOND_CUR = State()
    SUM_CUR = State()
    FIND_NUM = State()


first_cur = ''
second_cur = ''
sum_cur = 0


# Для переключения в роутер 'Информация о вагоне'
@router.message(F.text == 'Информация о вагоне ℹ️')
async def back(message: types.Message, state: FSMContext):
    await state.clear()
    logger.info("Пользователь %s id %s зашел в раздел 'Информация о вагоне'", message.from_user.first_name, message.from_user.id)
    await state.set_state(Form.FIND_NUM)
    await message.answer("Введите номер вагона или вернитесь в меню:", reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))


# Вывод информации о текущем курсе валют.
@router.message(F.text == 'Макроинформация 🌎')
async def macro_info(message: types.Message):
    try:
        usd_rub = get_currency_rate(['USD', 'RUB'])
        eur_rub = get_currency_rate(['EUR', 'RUB'])
        kzt_rub = get_currency_rate(['KZT', 'RUB'])
        logger.info("Пользователь %s id %s зашел в раздел 'Макроинформация'", message.from_user.first_name, message.from_user.id)
        await message.answer(f'Текущий курс ЦБ РФ:\nUSD/RUB = {usd_rub} руб.\nEUR/RUB = {eur_rub} руб.\nKZT/RUB = {kzt_rub} руб.')
        await message.answer("Вернитесь в меню или воспользуйтесь конвертером валют:", reply_markup=currency_cnverter().as_markup(one_time_keyboard=True, resize_keyboard=True))
    except Exception as e:
        logger.error(f"Ошибка! {e}")
        await message.reply('Произошла ошибка!')
        await message.answer("Вернуться в меню:",
                             reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))


# Запуск конвертера валют
@router.message(F.text == 'Конвертер валют 💱')
async def currency_cinverter(message: types.Message, state: FSMContext):
    await state.set_state(Form.FIRST_CUR)
    await message.answer('Выберите валюту из которой хотите конвертировать: ', reply_markup=currency().as_markup(one_time_keyboard=True, resize_keyboard=True))


# Получение валюты из которой конвертируем
@router.message(Form.FIRST_CUR)
async def first_cur(message: types.Message, state: FSMContext):
    global first_cur
    first_cur = currency_map(message.text)
    if first_cur != False:
        await state.set_state(Form.SECOND_CUR)
        await message.answer('Выберите валюту в которую хотите конвертировать: ', reply_markup=currency().as_markup(one_time_keyboard=True, resize_keyboard=True))
    else:
        logger.error(f"Пользователь {message.from_user.first_name} id {message.from_user.id} ввел неверную валюту {message.text}")
        await message.reply('Некорректный ввод, выберите валюту из списка!')
        await message.answer('Выберите валюту из которой хотите конвертировать: ', reply_markup=currency().as_markup(one_time_keyboard=True, resize_keyboard=True))


# Получение валюты в которую конвертируем
@router.message(Form.SECOND_CUR)
async def second_cur(message: types.Message, state: FSMContext):
    global second_cur
    await state.update_data(name=message.text)
    second_cur = currency_map(message.text)
    if second_cur != False:
        await state.set_state(Form.SUM_CUR)
        await message.answer('Введите сумму, которую хотите конвертировать: ')
    else:
        logger.error(f"Пользователь {message.from_user.first_name} id {message.from_user.id} ввел неверную валюту {message.text}")
        await message.reply('Некорректный ввод, выберите валюту из списка!')
        await message.answer('Выберите валюту в которую хотите конвертировать: ', reply_markup=currency().as_markup(one_time_keyboard=True, resize_keyboard=True))


# Получение суммы, которую конвертируем и вывод результата
@router.message(Form.SUM_CUR)
async def sum_cur(message: types.Message, state: FSMContext):
    global first_cur
    global second_cur
    global sum_cur
    await state.update_data(name=message.text)
    try:
        if first_cur == 'RUB' and second_cur == 'RUB':
            sum_cur = float(message.text)
            result = sum_cur
            await message.answer(f'{sum_cur} {first_cur} = {result} {second_cur}\n Вернитесь в меню или снова воспользуйтесь конвертером валют: ', reply_markup=currency_cnverter().as_markup(one_time_keyboard=True, resize_keyboard=True))
            await state.clear()
        else:
            sum_cur = float(message.text)
            result = round(get_currency_rate([first_cur, second_cur]) * sum_cur, 4)
            await message.answer('Результат конвертации (округление до 4-х знаков после запятой):')
            await message.answer(f'{sum_cur} {first_cur} = {result} {second_cur}')
            await message.answer('Вернитесь в меню или снова воспользуйтесь конвертером валют: ',reply_markup=currency_cnverter().as_markup(one_time_keyboard=True, resize_keyboard=True))
            await state.clear()
    except Exception as e:
        logger.error(f"Пользователь {message.from_user.first_name} id {message.from_user.id} ввел неверный формат данных: {e}")
        await message.reply('Некорректный формат данных!')
        await message.answer('Введите сумму, которую хотите конвертировать: ', reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))





