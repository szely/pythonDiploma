from pydub import AudioSegment
import os
import speech_recognition as sr


# Модель конвертации в wav формат, необходимый для работы распознования по аудио
def convert_to_wav(filename):
    audio = AudioSegment.from_file(filename, format="ogg")
    file_name, file_extension = os.path.splitext(filename)
    output_filename = file_name + ".wav"
    audio.export(output_filename, format="wav")
    return output_filename


# Модель распознования аудио в текст
def speach_rec(file):
    r = sr.Recognizer()
    with sr.AudioFile(file) as sourse:
        audio = r.record(sourse)
    text = r.recognize_google(audio, language='ru')
    return text