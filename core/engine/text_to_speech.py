
from pyttsx3 import engine as tts_engine
import pyttsx3
tts_engine = pyttsx3.init()


def say(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

