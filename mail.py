import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from os.path import basename

def email(f, t):
    msg = MIMEMultipart()
    msg['From'] = 'szely@yandex.ru'
    msg['To'] = 'szely@yandex.ru'
    msg['Subject'] = t
    message = 'Это тестовое сообщение и отвечать на него не нужно'
    msg.attach(MIMEText(message))

    file = f
    with open(file, "rb") as fil:
        part = MIMEApplication(
            fil.read(),
            Name=basename(file)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file)
        msg.attach(part)


    try:
        mailserver = smtplib.SMTP('smtp.yandex.ru',587)
        mailserver.set_debuglevel(True)
    # Определяем, поддерживает ли сервер TLS
        mailserver.ehlo()
    # Защищаем соединение с помощью шифрования tls
        mailserver.starttls()
    # Повторно идентифицируем себя как зашифрованное соединение перед аутентификацией.
        mailserver.ehlo()
        mailserver.login('szely@yandex.ru', 'Irsha#1415')
        mailserver.sendmail('szely@yandex.ru','szely@yandex.ru',msg.as_string())
        msg.attach(part)
        mailserver.quit()
        print("Письмо успешно отправлено")
    except smtplib.SMTPException:
        print("Ошибка: Невозможно отправить сообщение")


import telebot
from telebot import types
import os

Token = "6519207648:AAG3nad5ENAnHfSXF-o5Hz39mceHn5B696E"
bot = telebot.TeleBot(Token)
my_directory = '/Users/a1234/Downloads/my_files'

def create_file_buttons(directory):
    files = os.listdir(directory)
    keyboard = []
    for file in files:
        keyboard.append(file)
    return keyboard

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





bot.polling(none_stop=True)