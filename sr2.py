import speech_recognition as sr

# Создаем объект Recognizer
r = sr.Recognizer()

# Определяем источник звука
mic = sr.Microphone()

# Записываем аудио с микрофона
with mic as source:
    print("Говорите...")
    audio = r.listen(source)

try:
    # Преобразуем записанный звук в текст
    text = r.recognize_google(audio, language="ru")
    print("Вы сказали: " + text)
except sr.UnknownValueError:
    print("Извините, не удалось распознать речь.")
except sr.RequestError as e:
    print("Ошибка сервиса распознавания речи; {0}".format(e))