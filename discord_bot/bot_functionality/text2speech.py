import os
import gtts
from playsound import playsound

def t2t(text):
    file_path="./daibl/temp.mp3"
    tts = gtts.gTTS(text)

    tts.save(file_path)
    playsound(file_path)
    os.remove(file_path)