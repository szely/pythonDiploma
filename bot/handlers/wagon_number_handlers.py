from aiogram import Bot, types
from aiogram import Router, F
from aiogram.filters.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from bot.keyboards.user_keyboards import back_menu, back_menu_wagon_number
import logging
from bot.db.db import find_wagon
from bot.other_methods.wagon_rec import get_wagon_number
from bot.other_methods.check_wagon_number import check_wagon_number, get_wagon_type
import os


logger = logging.getLogger(__name__)


# Создание экземпляра класса состояний для создания последовательности получения и отправки сообщений
class Form(StatesGroup):
    REC_NUM = State()

router = Router()


# Запрос фото с номером вагона
@router.message(F.text == 'Сканер номера вагона 📷')
async def get_wagon_photo(message: types.Message, state: FSMContext):
	logger.info("Пользователь %s id %s зашел в раздел 'Сканер номера вагона'", message.from_user.first_name, message.from_user.id)
	await state.set_state(Form.REC_NUM)
	await message.answer(f'Сфотографируйте номер вагона на кузове или вернитесь в меню:', reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))


# Получение фото с номером вагона и его обработка
@router.message(F.photo, Form.REC_NUM)
async def wagon_number(message: types.Message, state: FSMContext):
	await state.update_data(name=message.text)
	file = message.photo[-1].file_id
	file_name = f'{file}.png'
	await message.bot.download(file=file, destination=file_name)
	number = get_wagon_number(file_name)
	os.remove(file_name)
	try:
		number != None
		if len(number) == 8:
			try:
				int(number)
				if check_wagon_number(number):
					res = find_wagon(number)
					if res != 0:
						await message.answer(f'Информация по вагону {number}:')
						info_str = ''
						for key, value in res.items():
							info_str += f'{key}: {value}\n'
						await message.answer(info_str)
						await message.answer("Запустите сканер заново или вернитесь в меню:", reply_markup=back_menu_wagon_number().as_markup(one_time_keyboard=True, resize_keyboard=True))
						await state.clear()
					else:
						wagon_type = get_wagon_type(number)
						await message.answer(f'Информация по вагону {number} в базе данных не найдена! Этот вагон отностится к типу {wagon_type}.')
						await message.answer("Запустите сканер заново или вернитесь в меню:", reply_markup=back_menu_wagon_number().as_markup(one_time_keyboard=True, resize_keyboard=True))
						await state.clear()
				else:
					await message.reply('Это не номер вагона!')
					await message.answer("Сфотографируйте номер заново или вернитесь в меню:", reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))
					if message.text == 'Назад в меню ↩️':
						await state.clear()
			except Exception as e:
				logger.error(f"Пользователь {message.from_user.first_name} id {message.from_user.id} прислал фото с несуществующем номером вагона, или номер вагона распознан не корректно: {e}")
				await message.reply("Номер вагона должен быть в числовом вормате! Длина номера вагона должна быть равна 8!")
				await message.answer("Сфотографируйте номер заново или вернитесь в меню:", reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))
				if message.text == 'Назад в меню ↩️':
					await state.clear()
		else:
			await message.reply("Номер вагона должен быть в числовом вормате! Длина номера вагона должна быть равна 8!")
			await message.answer("Сфотографируйте номер заново или вернитесь в меню:",  reply_markup=back_menu().as_markup(one_time_keyboard=True, resize_keyboard=True))
			if message.text == 'Назад в меню ↩️':
				await state.clear()
	except Exception as e:
		logger.error(f"Пользователь {message.from_user.first_name} id {message.from_user.id} прислал фото номера вагона, который не удалось распознать: {e}")
		await message.answer(" Номер вагона не распознан, запустите сканер заново или вернитесь в меню:", reply_markup=back_menu_wagon_number().as_markup(one_time_keyboard=True, resize_keyboard=True))
		if message.text == 'Назад в меню ↩️':
			await state.clear()
