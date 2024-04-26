from vosk import Model, KaldiRecognizer
import sys
import json
import os
import time
import wave

model = Model(r"/Users/a1234/PycharmProjects/pythonDiploma/bot/models/vosk/model")

wf = wave.open(r'/Users/a1234/PycharmProjects/pythonDiploma/1234.wav', "rb")
rec = KaldiRecognizer(model,  44100)

result = ''
last_n = False

while True:
    data = wf.readframes(44100)
    if len(data) == 0:
        break

    if rec.AcceptWaveform(data):
        res = json.loads(rec.Result())

        if res['text'] != '':
            result += f" {res['text']}"
            last_n = False
        elif not last_n:
            result += '\n'
            last_n = True

res = json.loads(rec.FinalResult())
result += f" {res['text']}"

print(result)


