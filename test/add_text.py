import os

# Функция для добавления текста в файлы
def add_text_to_files(directory, text):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'a') as f:
                f.write('n' + text)

# Задаем директорию, в которой будем добавлять текст
directory = '/Users/a1234/Downloads/Финансовый департамент'
text_to_add = 'Это тестовый файл'

add_text_to_files(directory, text_to_add)