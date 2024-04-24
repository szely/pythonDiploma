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
from pathlib import Path

Token = "6519207648:AAG3nad5ENAnHfSXF-o5Hz39mceHn5B696E"
bot = telebot.TeleBot(Token)
my_directory = '/Users/a1234/Downloads/my_files'
my_directory.split()
def create_file_buttons(path1):
    path = Path(path1)
    the_dict = {}
    for item in path.rglob("*"):
        if item.is_dir():
            the_dict[str(item)] = []
            for item_2 in item.iterdir():
                if item_2.name != '.DS_Store':
                    the_dict[str(item)].append(str(item_2))
    return the_dict


print(create_file_buttons(my_directory))
markup = {}
files = create_file_buttons(my_directory)
for k , v in files.items():
    markup[k] = (types.ReplyKeyboardMarkup(resize_keyboard=True))
btns1 = {}
for k, v in files.items():
    btns1[k] = []
    for i in v:
        btns1[k].append(types.KeyboardButton(f"{i}"))

for k in markup.keys():
    markup.get(k).add(*btns1.get(k))

@bot.message_handler(commands=['start'])
def start(message):
    # markup.get('folder_1').add(*btns1.get('folder_1'))
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Выбери файл".format(
                         message.from_user), reply_markup=markup.get('/Users/a1234/Downloads/my_files/folder_1'))


@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text in files.keys()):
        # markup.get(message.text).add(*btns1.get(message.text))
        bot.send_message(message.chat.id,
                         text="Привет, {0.first_name}! Выбери файл".format(
                             message.from_user), reply_markup=markup.get(message.text))





    # files = create_file_buttons(my_directory)
    # if (message.text in files):
    #         file = open(f"{str(my_directory + '/' + message.text)}", "rb")
    #         bot.send_document(message.chat.id, file)
    #         # g = str(my_directory + '/' + message.text)
    #         # email(g, message.text)
    #         # bot.send_message(message.chat.id, f' Файл "{message.text}" отправлен на Вашу почту')
    #         # file.close()
    # else:
    #     bot.send_message(message.chat.id, text="На такую комманду я не запрограммирован..")





bot.polling(none_stop=True)