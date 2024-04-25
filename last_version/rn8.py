import easyocr
import time

start_time = time.time()

def text_recognition(file_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(file_path, detail=0)
    return result

def main():
    file_path = '/Users/a1234/Downloads/4.jpeg'
    text = text_recognition(file_path=file_path)
    for item in text:
        item = item.replace(' ','')
        if len(item) == 8:
            try:
                num = int(item)
            except ValueError:
                continue
            print(f'Номер вагона: {item}')
            with open("../log.txt", "a") as file:
                file.write(item+'\n')



if __name__ == "__main__":
    main()

end_time = time.time()

elapsed_time = end_time - start_time
print('Elapsed time: ', elapsed_time)
