from aiogram import Bot, types
from aiogram import Router, F
from aiogram.filters.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from bot.keyboards.user_keyboards import create_buttons, tools_buttoms, choose_send_buttoms, back_choose_send_find_buttoms, main_menu, back_menu
import logging


logger = logging.getLogger(__name__)


# Создание экземпляра класса состояний для создания последовательности получения и отправки сообщений
class Form(StatesGroup):
    GET_NNS = State()
    GET_OSS = State()
    GET_SNAV = State()
    GET_SLV = State()
    GET_STOKP = State()
    GET_SONK = State()
    GET_SLKP = State()


router = Router()


# Создание глобальных переменных, необходимых для осуществления оценки вагона
nss = 0 # Нормативный срок службы вагона в годах
oss = 0 # Остаточный срок службы вагона в годах
snav = 0 # Стоимость нового аналога оцениваемого вагона, тыс. руб.
slv = 0 # Стоимость лома вагона, тыс. руб.
stokp = 0 # Средняя текущая толщина обода колесной пары, мм
sonk = 0 # Стоимсоть новой колесной пары (старая ось, новое колесо - СОНК), тыс. руб.
slkp = 0 # Стоимость лома колесной пары, тыс. руб.


# Запуск процесса оценки вагона
@router.message(F.text == 'Оценить вагон 🪙')
async def macro_info(message: types.Message,  state: FSMContext):
    logger.info("Пользователь %s id %s зашел в раздел 'Оценить вагон'", message.from_user.first_name, message.from_user.id)
    await state.set_state(Form.GET_NNS)
    await message.answer('Введите нормативный срок службы вагона, лет:', reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))


# Получение нормативного срока вагона
@router.message(Form.GET_NNS)
async def get_nss(message: types.Message, state: FSMContext):
    global nss
    await state.update_data(name=message.text)
    try:
        nss = float(message.text.replace(',', '.'))
        await state.set_state(Form.GET_OSS)
        await message.answer('Введите остаточный срок службы, лет:',
                             reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))
    except Exception as e:
        logger.error(f"Пользователь {message.from_user.first_name} id {message.from_user.id} ввел неверный формат данных: {e}")
        await message.reply('Некорректный формат данных!')
        await message.answer('Введите нормативный срок службы вагона, лет:',
                             reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))


# Получение остаточного срока вагона
@router.message(Form.GET_OSS)
async def get_oss(message: types.Message, state: FSMContext):
    global oss
    await state.update_data(name=message.text)
    try:
        oss = float(message.text.replace(',', '.'))
        await state.set_state(Form.GET_SNAV)
        await message.answer('Введите стоимость нового аналога вагона, тыс. руб.:',
                             reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))
    except Exception as e:
        logger.error(f"Пользователь {message.from_user.first_name} id {message.from_user.id} ввел неверный формат данных: {e}")
        await message.reply('Некорректный формат данных!')
        await message.answer('Введите остаточный срок службы, лет:',
                             reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))


# Получение стоимости нового аналога оцениваемого вагона
@router.message(Form.GET_SNAV)
async def get_snav(message: types.Message, state: FSMContext):
    global snav
    await state.update_data(name=message.text)
    try:
        snav = float(message.text.replace(',', '.'))
        await state.set_state(Form.GET_SLV)
        await message.answer('Введите стоимость лома вагона, тыс. руб.:', reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))
    except Exception as e:
        logger.error(f"Пользователь {message.from_user.first_name} id {message.from_user.id} ввел неверный формат данных: {e}")
        await message.reply('Некорректный формат данных!')
        await message.answer('Введите стоимость нового аналога вагона, тыс. руб.:',
                             reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))


# Получение стоимость лома вагона
@router.message(Form.GET_SLV)
async def get_slv(message: types.Message, state: FSMContext):
    global slv
    await state.update_data(name=message.text)
    try:
        slv = float(message.text.replace(',', '.'))
        await state.set_state(Form.GET_STOKP)
        await message.answer('Введите среднюю толшину обода КП (мин.: 25 мм, макс.: 76 мм), мм:', reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))
    except Exception as e:
        logger.error(f"Пользователь {message.from_user.first_name} id {message.from_user.id} ввел неверный формат данных: {e}")
        await message.reply('Некорректный формат данных!')
        await message.answer('Введите стоимость лома вагона, тыс. руб.:', reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))


# Получение средней толщины обода колеса вагона
@router.message(Form.GET_STOKP)
async def get_stokp(message: types.Message, state: FSMContext):
    global stokp
    await state.update_data(name=message.text)
    try:
        stokp = float(message.text.replace(',', '.'))
        await state.set_state(Form.GET_SONK)
        await message.answer('Введите стоимость СОНК, тыс. руб.:', reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))
    except Exception as e:
        logger.error(f"Пользователь {message.from_user.first_name} id {message.from_user.id} ввел неверный формат данных: {e}")
        await message.reply('Некорректный формат данных!')
        await message.answer('Введите среднюю толшину обода КП (мин.: 25 мм, макс.: 76 мм), мм:', reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))


# Получение стоимости СОНК
@router.message(Form.GET_SONK)
async def get_sonk(message: types.Message, state: FSMContext):
    global sonk
    await state.update_data(name=message.text)
    try:
        sonk = float(message.text.replace(',', '.'))
        await state.set_state(Form.GET_SLKP)
        await message.answer('Введите стоимость лома КП, тыс. руб.:', reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))
    except Exception as e:
        logger.error(f"Пользователь {message.from_user.first_name} id {message.from_user.id} ввел неверный формат данных: {e}")
        await message.reply('Некорректный формат данных!')
        await message.answer('Введите стоимость СОНК, тыс. руб.:', reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))


# Получение стоимости лома колесной пары и вывод стоимостной оценки вагона
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
    try:
        slkp = float(message.text.replace(',', '.'))
        try:
            sv = round((snav - slv - sonk * 4) / nss * oss + slv + ((sonk - slkp) / 52 * (stokp - 24) + slkp) * 4, 3)
            await message.answer(f'Стоимость вагона по оценке затратным подходом: {sv} тыс. руб.')
            await state.clear()
            await message.answer("Вернуться в меню:", reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))
        except Exception as e:
            logger.error(f"Ошибка! {e}")
            await message.reply('Произошла ошибка!')
            await message.answer("Вернуться в меню:", reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))
    except Exception as e:
        logger.error(f"Пользователь {message.from_user.first_name} id {message.from_user.id} ввел неверный формат данных: {e}")
        await message.reply('Некорректный формат данных!')
        await message.answer('Введите стоимость лома КП, тыс. руб.:', reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))



