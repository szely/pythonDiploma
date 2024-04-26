from pydub import AudioSegment
import os
import speech_recognition as sr

def convert_to_wav(filename):
    # Load the audio file
    audio = AudioSegment.from_file(filename, format="ogg")

    # Set the output file path and format
    file_name, file_extension = os.path.splitext(filename)
    output_filename = file_name + ".wav"

    # Export the audio file in wav format
    audio.export(output_filename, format="wav")

    return output_filename

def speach_rec(file):
    r = sr.Recognizer()
    with sr.AudioFile(file) as sourse:
        audio = r.record(sourse)
    text = r.recognize_google(audio, language='ru')
    return text