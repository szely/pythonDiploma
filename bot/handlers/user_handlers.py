from aiogram import Bot, types
from aiogram.types import CallbackQuery, FSInputFile
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.state import StatesGroup, State
from bot.keyboards.user_keyboards import create_buttons, tools_buttoms, choose_send_buttoms
from bot.other_methods.other_methods import create_dirs_files_map, create_path_buttons
import os
from dotenv import load_dotenv
from pathlib import Path
from bot.other_methods.to_email import send_email
from bot.other_methods.find_file import search_dict_by_key_part, swapped_dict
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bot.other_methods.speach_rec import convert_to_wav, speach_rec

class Form(StatesGroup):
    MAIN_MENU = State()
    SEARCH = State()
    PARSING_WORD = State()
    PARSING_NUMBER = State()
    HELP_MENU = State()
    FAQ_MENU = State()

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

@router.message(F.text.lower() == "поиск файла")
async def find_file(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.SEARCH)
    await message.answer('Напишите название файла или пришлите аудиосообщение!')
@router.message(Form.SEARCH)
async def search(message: Message, state: FSMContext, bot: Bot) -> None:
    global number_path
    global path_number
    global path_buttons
    global buttons
    global message_choose
    load_dotenv('.env')
    my_directory = os.getenv("MY_DIRECTORY")
    await state.update_data(name=message.text)
    found_files_p_n = search_dict_by_key_part(path_number, message.text)
    found_files_n_p = swapped_dict(found_files_p_n)
    await message.answer('Получите файл(ы)!')
    for key in found_files_p_n:
        print(key)
        file = FSInputFile(key)
        await bot.send_document(message.chat.id, file)

@router.message(F.text)
async def instrument(message: types.Message):
    global buttons
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

@router.message(F.content_type.in_({'voice', 'audio'}))
async def voice_message_handler(message: types.Message, bot: Bot):
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_name = Path("", f"{file_id}.ogg")
    await bot.download_file(file_path, destination=file_name, timeout=0)
    file_name_wav = convert_to_wav(file_name)
    await message.answer('Ищу файлы')
    text = speach_rec(file_name_wav)
    global number_path
    global path_number
    global path_buttons
    global buttons
    global message_choose
    load_dotenv('.env')
    my_directory = os.getenv("MY_DIRECTORY")
    found_files_p_n = search_dict_by_key_part(path_number, text)
    found_files_n_p = swapped_dict(found_files_p_n)
    await message.answer('Получите файл(ы)!')
    for key in found_files_p_n:
        file = FSInputFile(key)
        await bot.send_document(message.chat.id, file)
    os.remove(file_name)
    os.remove(file_name_wav)
