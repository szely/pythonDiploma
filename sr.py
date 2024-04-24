# # import speech_recognition as sr
# #
# # r = sr.Recognizer()
# # mic = sr.Microphone()
# #
# #
# #
# # with mic as sourse:
# #     r.adjust_for_ambient_noise(sourse)
# #     print('Запись пошла, можно говорить!')
# #     audio = r.listen(sourse)
# #
# # text = r.recognize_google_cloud(audio, language='ru-Ru')
# #
# # print(f'Было сказано {text}')

import speech_recognition as sr
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/path/to/file.json"

# Создаем объект распознавателя речи
recognizer = sr.Recognizer()
# mic = sr.Microphone()

with sr.Microphone(device_index=0) as sourse:
    recognizer.adjust_for_ambient_noise(sourse)
    print('Запись пошла, можно говорить!')
    audio_file = recognizer.listen(sourse)

# Распознаем речь из аудио файла
# with audio_file as source:
#     audio_data = recognizer.record(source)

text = recognizer.recognize_google(audio_file, language='ru')

# Выводим текст
print(text)
