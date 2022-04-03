import multiprocessing
from time import sleep
from playsound import playsound

from .sound_enums import AudioType, Sounds

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
    pass