import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from os.path import basename
import reg_data

from_addr = reg_data.from_addr
to_addr = reg_data.to_addr
password = reg_data.password

def email(f, t):
    global from_addr
    global to_addr
    global password
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
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
        mailserver.login(user=from_addr, password=password)
        mailserver.sendmail(f'{from_addr}',f'{to_addr}',msg.as_string())
        msg.attach(part)
        mailserver.quit()
        status = "На Вашу почту успешно отправлен файл "
        print(status)
    except smtplib.SMTPException:
        status = "Ошибка: Невозможно отправить файл "
        print(status)
    return status


def send_email(file_path, file_name):
    file = open(f"{file_path}", "rb")
    g = str(file_path)
    status = email(g, file_name)
    file.close()
    return status
