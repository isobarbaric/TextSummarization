
from gtts import gTTS
from playsound import playsound

import os
  
class Reader:

    def __init__(self, text):
        self.text = text
    
    def read(self):
        speech_audio = gTTS(text = self.text, lang = 'en', slow = False)
        speech_audio.save('text-spoken.mp3')
        playsound('text-spoken.mp3')
        os.remove('text-spoken.mp3')

a = Reader("lorem ipsum lorem ipsum")
a.read()