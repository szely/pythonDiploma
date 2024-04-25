import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import CallbackQuery, FSInputFile
from pathlib import Path
from to_email import send_email
import reg_data

# Включаем логирование, чтобы не пропустить важные сообщения
# logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
# logging.debug("A DEBUG Message")
# logging.info("An INFO")
# logging.warning("A WARNING")
# logging.error("An ERROR")
# logging.critical("A message of CRITICAL severity")


#  Токен
TOKEN = reg_data.TOKEN
# Объект бота
bot = Bot(TOKEN)
# Диспетчер
dp = Dispatcher()

# Указываем путь к корневой директории
my_directory = reg_data.my_directory

# Указываем первую папку
first_dir = reg_data.first_dir

ignore = '.DS_Store'
number_path = {}
path_number = {}
path_buttons = {}
buttons = {}
message_choose = ''


# Создаем словари сопоставлений, присваиваем номера кажому элементу - файл папка и связываем его с путем к этому элементу
def create_dirs_files_map(path):
    path = Path(path)
    number_path = {}
    path_number ={}
    i = 0
    for item in path.rglob("*"):
        number_path[i] = str(item)
        path_number[str(item)] = i
        i += 1
    result = [number_path, path_number]
    return result


# Создаем заготовку для формирования кнопок
def create_path_buttons(path):
    global ignore
    path = Path(path)
    dict = {}
    for item in path.rglob("*"):
        if item.name not in ignore:
            if item.is_dir():
                dict[str(item)] = []
                for item_in_dir in item.iterdir():
                    if item_in_dir.name not in ignore:
                        dict[str(item)].append(str(item_in_dir))
                        dict[str(item)].sort()
    return dict


def create_buttons(path_buttons, number_path, path_number):
    result = {}
    for key, value in path_buttons.items():
        result[key] = InlineKeyboardBuilder()
        for v in value:
            if Path(v).is_dir():
                name = ('📂 ' + str(v.split('/')[-1]))
            else:
                name = ('📃 ' + v.split('/')[-1])
            call = path_number.get(v)
            button = (types.InlineKeyboardButton(text=str(name), callback_data=str(call)))
            result[key].add(button)
            result[key].adjust(1)
        if str(Path(key).parent) != my_directory:
            m = int(path_number.get(str(Path(key).parent)))
            k ='↩️ Назад'
            n = (types.InlineKeyboardButton(text=str(k), callback_data=str(m)))
            result[key].add(n)
            result[key].adjust(1)
    return result

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    global number_path
    global path_number
    global path_buttons
    global buttons
    global first_dir
    builder = ReplyKeyboardBuilder()
    builder.button(text='Файловый менеджер')
    builder.button(text='Сканер номера вагона')
    builder.button(text='Сканер номера паспорта вагона')
    builder.adjust(1)
    await message.answer("Выберите инструмент", reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True))
    number_path = create_dirs_files_map(my_directory)[0]
    path_number = create_dirs_files_map(my_directory)[1]
    path_buttons = create_path_buttons(my_directory)
    buttons = create_buttons(path_buttons, number_path, path_number)


@dp.message()
async def instrument(message: types.Message):
    global buttons
    global first_dir
    global message_choose
    message_choose = message.text
    if message_choose == 'Файловый менеджер':
        builder_type_send = ReplyKeyboardBuilder()
        builder_type_send.button(text='В бот')
        builder_type_send.button(text='На почту')
        builder_type_send.adjust(2)
        await message.answer("Куда отправлять файлы?", reply_markup=builder_type_send.as_markup(one_time_keyboard=True, resize_keyboard=True))
    if message_choose == 'В бот':
        this_button = buttons.get(str(my_directory + first_dir))
        await message.answer("Выберите файл или папку", reply_markup=this_button.as_markup())
    if message_choose == 'На почту':
        this_button = buttons.get(str(my_directory + first_dir))
        await message.answer("Выберите файл или папку", reply_markup=this_button.as_markup())


@dp.callback_query()
async def call(callback):
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

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())