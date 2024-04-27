import os

def create_pptx_file(file_name):
    with open(file_name, 'w') as file:
        file.write("This is test file")

def replace_files(dir_path, extension):
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith(extension):
                os.remove(os.path.join(root, file))
                new_file_name = file.replace(extension, '.pptx')
                create_pptx_file(os.path.join(root, new_file_name))

dir_path = '/Users/a1234/Downloads/Финансовый департамент'
extension = ".pptx"

replace_files(dir_path, extension)