from asyncore import loop
from email.mime import audio
import multiprocessing
from time import sleep
from playsound import playsound

import os
import enum

import pyttsx3

class Sounds(enum.Enum):
    STING = r"assets\sound\sfx\sting.mp3"
    MAIN_THEME = r"assets\sound\music\main_theme.mp3"
    SUDDEN_DEATH = r"assets\sound\music\sudden_death.mp3"
    WALK_OF_SHAME = r"assets\sound\music\walk_of_shame.mp3"
    QUESTION_BED = r"assets\sound\music\question_bed.mp3"
    CREDITS = r"assets\sound\music\credits.mp3"
    PENALITY_SHOOTOUT = r"assets\sound\music\penality_shootout.mp3"

class AudioType(enum.IntEnum):
    MUSIC_TRACK = 1
    SFX = 2

sound_paths = {}
sound_paths[Sounds.MAIN_THEME] = r"assets\sound\music\main_theme.mp3"
sound_paths[Sounds.STING] = r"assets\sound\sfx\sting.mp3"

class SoundManager():
    """

    Manages two threads. A music track thread and a sound effect thread.

    Music can loop. While a sound effect cannot.

    """
    _threads = {}
    _current_sounds = {}
    for audio_type in AudioType:
        _threads[audio_type] = None
        _current_sounds[audio_type] = None   

    def _play_sound(path, loop=False):
        while loop:
            playsound(path, block=True)
        if not loop:
            playsound(path, block=True) 

    def _terminate_thread(thread:multiprocessing.Process):
        if thread != None:
            try:
                thread.terminate()
            except Exception:
                print(Exception)

    _tts_engine = pyttsx3.init()
    def play_text_to_speech(text):
        SoundManager._tts_engine.say(text)
        SoundManager._tts_engine.runAndWait()

    @classmethod
    def play_sound(self, sound:Sounds, loop=False, audio_type:AudioType=AudioType.SFX, delay_thread_termination=0.5):
        old_thread = SoundManager._threads[audio_type]
        new_thread = multiprocessing.Process(target=SoundManager._play_sound, args=(sound.value, loop), daemon=True)

        SoundManager._threads[audio_type] = new_thread
        SoundManager._current_sounds[audio_type] = sound
        new_thread.start()
        sleep(delay_thread_termination)

        SoundManager._terminate_thread(old_thread)
        
    @classmethod
    def stop_playing(self, audio_type:AudioType=None):
        if audio_type == None:
            for audio_type, thread in SoundManager._threads.items():
                print(audio_type, thread)
                SoundManager._terminate_thread(thread)
                SoundManager._current_sounds[audio_type] = None
        else:
            SoundManager._terminate_thread(thread=SoundManager._current_track_thread)
            SoundManager._current_sounds[audio_type] = None

if __name__ == "__main__":
    print(os.getcwd())
    print(os.listdir())
    SoundManager.play_sound(Sounds.MAIN_THEME, audio_type=AudioType.MUSIC_TRACK, delay_thread_termination=0)
    input()
    SoundManager.play_sound(Sounds.SUDDEN_DEATH, audio_type=AudioType.MUSIC_TRACK, delay_thread_termination=0.5)
    input()
    SoundManager.play_sound(Sounds.STING, audio_type=AudioType.SFX, loop=False)
    input()
    SoundManager.stop_playing()
