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
from aiogram.filters import CommandStart

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
    # path_buttons = create_path_buttons(my_directory)
    # buttons = create_buttons(path_buttons, found_files_n_p, found_files_p_n)
    # path = number_path.get(73)
    # print(path)
    # markup = buttons.get(path)
    # print(markup)

    # await message.answer('Выберите файл', reply_markup=markup.as_markup())
    for key in found_files_p_n:
        print(key)
        file = FSInputFile(key)
        await bot.send_document(message.chat.id, file)

    # await message.answer(str(found_files_n_p))
    # await message.answer(str(found_files_p_n))

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
#
#
# from bot.other_methods.audio_to_text import STT
#
# stt = STT()
#
# # Хэндлер на получение голосового и аудио сообщения
# @router.message(types.Audio, types.Voice, types.Document
#     # types.ContentType.VOICE,
#     # types.ContentType.AUDIO,types.ContentType.DOCUMENT
# )
# async def voice_message_handler(message: types.Message, bot: Bot):
#     """
#     Обработчик на получение голосового и аудио сообщения.
#     """
#     if message.content_type == types.Voice:
#         file_id = message.voice.file_id
#     elif message.content_type == types.Audio:
#         file_id = message.audio.file_id
#     elif message.content_type == types.Document:
#         file_id = message.document.file_id
#     else:
#         await message.reply("Формат документа не поддерживается")
#         return
#
#     file = await bot.get_file(file_id)
#     file_path = file.file_path
#     file_on_disk = Path("", f"{file_id}.tmp")
#     await bot.download_file(file_path, destination=file_on_disk)
#     await message.reply("Аудио получено")
#
#     text = stt.audio_to_text(file_on_disk)
#     if not text:
#         text = "Формат документа не поддерживается"
#     await message.answer(text)
#
#     os.remove(file_on_disk)  # Удаление временного файла

@router.message(types.audio.Audio)



