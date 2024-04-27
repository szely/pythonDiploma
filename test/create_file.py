# Открываем файл Excel
import openpyxl

workbook = openpyxl.load_workbook('/Users/a1234/PycharmProjects/pythonDiploma/test/files.xlsx')
sheet = workbook.active

# Получаем данные из первого столбца
file_names = [cell.value for cell in sheet['A']]

# Создаем файлы
for name in file_names:
    with open(name, 'w') as file:
        file.write('')  # Создаем пустой файл

print('Файлы созданы')