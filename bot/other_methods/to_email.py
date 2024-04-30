import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from os.path import basename
from dotenv import load_dotenv
import os


# Алгоритм подключения и отправки по email
def email(f, t, user_email):
    load_dotenv('.env')
    from_adr = os.getenv("FROM_ADDR")
    to_adr = os.getenv("TO_ADDR")
    password = os.getenv("PASSWORD")
    msg = MIMEMultipart()
    msg['From'] = from_adr
    msg['To'] = user_email
    msg['Subject'] = t
    message = 'Спасибо, что выбрали HandyBOT!'
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
        mailserver.login(user=from_adr, password=password)
        mailserver.sendmail(f'{from_adr}', f'{user_email}', msg.as_string())
        msg.attach(part)
        mailserver.quit()
        status = f"На Вашу почту {user_email} успешно отправлен файл "
        print(status)
    except smtplib.SMTPException:
        status = "Ошибка: Невозможно отправить файл "
        print(status)
    return status


# Запуск процесса отправки файла по email
def send_email(file_path, file_name, user_email):
    file = open(f"{file_path}", "rb")
    g = str(file_path)
    status = email(g, file_name, user_email)
    file.close()
    return status
