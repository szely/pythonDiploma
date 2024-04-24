import telebot
from telebot import types
from pathlib import Path

Token = "6941628121:AAHT8TIRFVFZT3U6mgNwqQjYdMYyVgqkT5I"
bot = telebot.TeleBot(Token)
# my_directory = '/Users/a1234'
my_directory = '/Users/a1234/Downloads/my_files'
first_dir = '/folder_1'

msg = ''
msg_2 = ''
ignore = '.DS_Store'
number_path = {}
path_number = {}
path_buttons = {}
buttons = {}

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

# Создаем заготовку для формиования кнопок
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


def create_buttoms(path_buttons, number_path, path_number):
    result = {}
    number_path
    path_number
    for key, value in path_buttons.items():
        result[key] = types.InlineKeyboardMarkup()
        for v in value:
            if Path(v).is_dir():
                name = ('📂 ' + str(v.split('/')[-1]))
            else:
                name = ('📃 ' + v.split('/')[-1])
            call = path_number.get(v)
            buttom = (types.InlineKeyboardButton(f"{name}", callback_data=call))
            result[key].add(buttom)
        if str(Path(key).parent) != my_directory:
            m = int(path_number.get(str(Path(key).parent)))
            k ='↩️ Назад'
            n = (types.InlineKeyboardButton(f'{k}', callback_data=m))
            result[key].add(n)
    return result


@bot.message_handler(commands=['start'])
def start(message):
    global number_path
    global path_number
    global path_buttons
    global buttons
    global first_dir
    number_path = create_dirs_files_map(my_directory)[0]
    path_number = create_dirs_files_map(my_directory)[1]
    path_buttons = create_path_buttons(my_directory)
    buttons = create_buttoms(path_buttons, number_path, path_number)
    this_buttom = buttons.get(str(my_directory + first_dir))
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Выбери файл".format(
                         message.from_user), reply_markup=this_buttom)


@bot.callback_query_handler(func=lambda callback: True)
def sort(callback):
    global number_path
    global path_number
    global path_buttons
    global buttons

    if Path(number_path.get(int(callback.data))).is_dir():
        path = number_path.get(int(callback.data))
        markup = buttons.get(path)
        bot.send_message(callback.message.chat.id,  text="Привет, {0.first_name}! Выбери файл".format(callback.message.from_user),
                         reply_markup=markup)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        
    elif Path(number_path.get(int(callback.data))).is_file():
        file = open(f"{number_path.get(int(callback.data))}", "rb")
        bot.send_document(callback.message.chat.id, file)
        file.close()

bot.polling(none_stop=True)