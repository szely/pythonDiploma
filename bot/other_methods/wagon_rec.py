import easyocr


# модель распознавания текста
def text_recognition(file_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(file_path, detail=0)
    return result

# получение номера вагона из фото
def get_wagon_number(file_path):
    text = text_recognition(file_path=file_path)
    for item in text:
      item = item.replace(' ','')
      if len(item) == 8:
          try:
            num = int(item)
          except ValueError:
            continue
          return item
