# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.application import MIMEApplication
# from os.path import basename
#
# def email(f, t):
#     msg = MIMEMultipart()
#     msg['From'] = 'szely@yandex.ru'
#     msg['To'] = 'szely@yandex.ru'
#     msg['Subject'] = t
#     message = 'Это тестовое сообщение и отвечать на него не нужно'
#     msg.attach(MIMEText(message))
#
#     file = f
#     with open(file, "rb") as fil:
#         part = MIMEApplication(
#             fil.read(),
#             Name=basename(file)
#             )
#         # After the file is closed
#         part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file)
#         msg.attach(part)
#
#
#     try:
#         mailserver = smtplib.SMTP('smtp.yandex.ru',587)
#         mailserver.set_debuglevel(True)
#     # Определяем, поддерживает ли сервер TLS
#         mailserver.ehlo()
#     # Защищаем соединение с помощью шифрования tls
#         mailserver.starttls()
#     # Повторно идентифицируем себя как зашифрованное соединение перед аутентификацией.
#         mailserver.ehlo()
#         mailserver.login('szely@yandex.ru', 'Irsha#1415')
#         mailserver.sendmail('szely@yandex.ru','szely@yandex.ru',msg.as_string())
#         msg.attach(part)
#         mailserver.quit()
#         print("Письмо успешно отправлено")
#     except smtplib.SMTPException:
#         print("Ошибка: Невозможно отправить сообщение")


import telebot
from telebot import types
import os

Token = "6519207648:AAG3nad5ENAnHfSXF-o5Hz39mceHn5B696E"
bot = telebot.TeleBot(Token)
my_directory = '/Users/a1234/Downloads/my_files'

# def create_file_buttons(directory):
#     files = os.listdir(directory)
#     keyboard = []
#     for file in files:
#         keyboard.append(file)
#     return keyboard

# print(create_file_buttons(my_directory))
# print(len(create_file_buttons(my_directory)))

d = []
f = []
for root, dirs, files in os.walk(my_directory):
        for file in files:
        # if file.endswith('1.txt'):
        #     print(os.path.join(root, file))
                d.append(root)
                f.append(file)
# print(d)
# print(f)


def get_subdirectories(directory):
    return [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
#
#
# from os.path import isdir
# def parse_folder(path):
#     files = []
#     for file in os.listdir(path):
#         if isdir(path + '/' + file):
#             parse_folder(path + '/' + file)
#         files.append(file)
#     print(files)
#
#
# parse_folder(my_directory)
from pathlib import Path


# def parse_folder(path):
#     path = Path(path)
#
#     files = []
#     dirs =[]
#     all =[]
#
#     for item in path.rglob("*"):
#         all.append(item.name)
#
#         if item.is_dir():
#             dirs.append(item.name)
#         else:
#             files.append(item.name)
#
#     return files, dirs, all
#
#
# print(parse_folder(my_directory))
#
# from pathlib import Path


def parse_folder(path):
    path = Path(path)

    files = []
    dirs =[]
    all =[]
    the_dict = {}


    for item in path.rglob("*"):
        all.append(item.name)
        # the_dict[item] = [item.name, item.name]

        if item.is_dir():
            dirs.append(item.name)
            the_dict[item.name] = []
            for item_2 in item.rglob("*"):
                if item_2.name != '.DS_Store':
                # if item_2.is_file():
                    the_dict[item.name].append(item_2.name)



        else:
            files.append(item.name)

    # return files, dirs, all
    return the_dict


print(parse_folder(my_directory))


# for root, dirs, files in os.walk(my_directory):
#     for filename in files:
#         # print(dirs, filename)
#
#
# import json
# def path_to_dict(path):
#     d = {'object': os.path.basename(path)}
#     if os.path.isdir(path):
#         d['type'] = "directory"
#         d['children'] = [path_to_dict(os.path.join(path, x)) for x in os.listdir(path) if x !='.DS_Store']
#
#     with open('data.json', 'w') as fp:
#         json.dump(d, fp, indent=2)
#     return d
#
# print((path_to_dict(my_directory)['children']))

@bot.message_handler(commands=['start'])
def start(message):
    files = create_file_buttons(my_directory)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    i = 0
    btns = []
    while i < len(files):
        btns.append(types.KeyboardButton(f"{files[i]}"))
        i+=1
    markup.add(*btns)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Выбери файл".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    files = create_file_buttons(my_directory)
    if (message.text in files):
            file = open(f"{str(my_directory + '/' + message.text)}", "rb")
            # bot.send_document(message.chat.id, file)
            g = str(my_directory + '/' + message.text)
            email(g, message.text)
            bot.send_message(message.chat.id, f' Файл "{message.text}" отправлен на Вашу почту')
            file.close()
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммирован..")





# bot.polling(none_stop=True)