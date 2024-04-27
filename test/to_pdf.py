import os
from pathlib import Path
from fpdf import FPDF


# Функция для создания PDF файла с текстом
def create_pdf(file_name, text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=text, ln=True)
    pdf.output(file_name)


# Функция для обхода всех файлов в директории
def process_files(directory, extension):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(root, file)
                os.remove(file_path)  # Удаляем файл с указанным разрешением

                pdf_file = file.replace(extension, '.pdf')  # Создаем новое имя для PDF файла
                pdf_file_path = os.path.join(root, pdf_file)

                text = "This is test file"
                create_pdf(pdf_file_path, text)  # Создаем и заполняем PDF файл


# Указываем директорию для обхода
directory_path = '/Users/a1234/Downloads/Финансовый департамент'
# Указываем разрешение файлов, которые нужно удалить и заменить на PDF
file_extension = '.pdf'
process_files(directory_path, file_extension)

