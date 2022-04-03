
from time import sleep
from turtle import delay
from scenes.scene_base import SceneBase, SceneTypes
from engine.game_manager import GameManager
from engine.sound_manager import SoundManager, Sounds
from contestants.contestant import Player, PromptTypes

from utils import print_with_delay, clear_screen
from images.utils import print_ascii_art_from_file

class MainMenuScene(SceneBase):
    def __init__(self):
        super(MainMenuScene, self).__init__(scene_type=SceneTypes.MAIN_MENU)

    def on_scene_enter(self):
        clear_screen()
        SoundManager.play_sound(Sounds.MAIN_THEME, loop=True)
        print_with_delay("Loading Anne Robinson...", delay=0.2)
        clear_screen
        self.play()

    def play(self):
        print_ascii_art_from_file(r"assets\ascii_art\logo.txt", delay=0.25)
        Player.get_response(PromptTypes.CONTINUE)

        print("=== MAIN MENU ===")
        print('=               =')
        print('=    1. Play    =')
        print('=    2. Quit    =')
        print('=               =')
        print("=================")

        response = Player.get_response(PromptTypes.NUMBER)
        if not response.isnumeric():
            response = int(Player.get_response(PromptTypes.NUMBER))


        GameManager.scene_queue.put(SceneTypes.SETUP)
            
        self.on_scene_exit()

    def on_scene_exit(self):
        SoundManager.stop_playing()
        clear_screen()
        return None


