from aiogram import Bot, types
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import Router
from aiogram.filters import Command
from bot.keyboards.user_keyboards import create_buttons, tools_buttoms, choose_send_buttoms
from bot.other_methods.other_methods import create_dirs_files_map, create_path_buttons
import os
from dotenv import load_dotenv
from pathlib import Path
from bot.other_methods.to_email import send_email


number_path = {}
path_number = {}
path_buttons = {}
buttons = {}
message_choose = ''

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    global number_path
    global path_number
    global path_buttons
    global buttons
    load_dotenv('.env')
    my_directory = os.getenv("MY_DIRECTORY")

    await message.answer("Выберите инструмент",
                         reply_markup=tools_buttoms().as_markup(resize_keyboard=True, one_time_keyboard=True))

    number_path = create_dirs_files_map(my_directory)[0]
    path_number = create_dirs_files_map(my_directory)[1]
    path_buttons = create_path_buttons(my_directory)
    buttons = create_buttons(path_buttons, number_path, path_number)

@router.message()
async def instrument(message: types.Message):
    global buttons
    # global first_dir
    global message_choose
    load_dotenv('.env')
    my_directory = os.getenv("MY_DIRECTORY")
    first_dir = os.getenv("FIRST_DIR")
    message_choose = message.text
    if message_choose == 'Файловый менеджер':
        await message.answer("Куда отправлять файлы?", reply_markup=choose_send_buttoms().as_markup(one_time_keyboard=True, resize_keyboard=True))
    if message_choose == 'В бот':
        this_button = buttons.get(str(my_directory + first_dir))
        await message.answer("Выберите файл или папку", reply_markup=this_button.as_markup())
    if message_choose == 'На почту':
        this_button = buttons.get(str(my_directory + first_dir))
        await message.answer("Выберите файл или папку", reply_markup=this_button.as_markup())

@router.callback_query()
async def call(callback: CallbackQuery, bot: Bot):
    global number_path
    global path_number
    global path_buttons
    global buttons
    global message_choose

    if Path(number_path.get(int(callback.data))).is_dir():
        path = number_path.get(int(callback.data))
        markup = buttons.get(path)
        await callback.message.answer('Выберите папку или файл', reply_markup=markup.as_markup())
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    if Path(number_path.get(int(callback.data))).is_file() and message_choose == 'В бот':
        file = FSInputFile(number_path.get(int(callback.data)))
        await bot.send_document(callback.message.chat.id, file)
    if Path(number_path.get(int(callback.data))).is_file() and message_choose == 'На почту':
        file_name = str(Path(number_path.get(int(callback.data)))).split('/')[-1]
        status = send_email(str(Path(number_path.get(int(callback.data)))), file_name)
        await callback.message.answer(f'{status} "{file_name}"')