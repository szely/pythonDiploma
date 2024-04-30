from pathlib import Path
from dotenv import load_dotenv
import os


# Создание словарей сопоставлений, присвоение номера кажому элементу - файл папка и связывание его с путем к этому элементу
def create_dirs_files_map(path):
    path = Path(path)
    number_path = {}
    path_number = {}
    i = 0
    for item in path.rglob("*"):
        number_path[i] = str(item)
        path_number[str(item)] = i
        i += 1
    result = [number_path, path_number]
    return result


# Создаем заготовку для формирования кнопок
def create_path_buttons(path):
    load_dotenv('.env')
    ignore = os.getenv("IGNORE")
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