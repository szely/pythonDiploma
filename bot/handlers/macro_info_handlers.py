from aiogram import Router, F
from bot.keyboards.user_keyboards import create_buttons, tools_buttoms, choose_send_buttoms, back_choose_send_find_buttoms, main_menu, back_menu
from bot.other_methods.get_currency import get_currency_rate
import logging
from aiogram import types


logger = logging.getLogger(__name__)

router = Router()


# Вывод информации о текущем курсе валют.
@router.message(F.text == 'Макроинформация 🌎')
async def macro_info(message: types.Message):
    usd_rub = get_currency_rate(['USD', 'RUB'])
    eur_usd = get_currency_rate(['EUR', 'RUB'])
    logger.info("Пользователь %s id %s зашел в раздел 'Макроинформация'", message.from_user.first_name, message.from_user.id)
    await message.answer(f'Текущий курс ЦБ РФ:\nUSD/RUB = {usd_rub} руб.\nEUR/RUB = {eur_usd} руб.')
    await message.answer("Вернуться в меню:",
                         reply_markup=back_menu().as_markup(one_time_keyboard=True,
                                                                                resize_keyboard=True))


