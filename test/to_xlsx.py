import os
import openpyxl

def create_xlsx_file(file_name):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet['A1'] = "This is test file"
    workbook.save(file_name)

def replace_files(dir_path, extension):
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith(extension):
                os.remove(os.path.join(root, file))
                new_file_name = file.replace(extension, '.xlsx')
                create_xlsx_file(os.path.join(root, new_file_name))

dir_path = '/Users/a1234/Downloads/Финансовый департамент'
extension = ".xlsb"

replace_files(dir_path, extension)