from asyncore import loop
from .scene_base import SceneBase
from .scene_types import SceneTypes
from engine.game_manager import GameManager
from engine.sound.sound_manager import SoundManager
from engine.sound.sound_enums import Sounds, AudioType
from contestants.player import Player
from contestants.contestant_enums import PromptType
from utils import clear_screen, print_with_delay
from contestants.utils import generate_random_npc_contestants

class SessionSetupScene(SceneBase):
    def __init__(self):
        super(SessionSetupScene, self).__init__(scene_type=SceneTypes.SETUP)

    def on_scene_enter(self):
        clear_screen()
        SoundManager.play_sound(Sounds.MAIN_THEME, audio_type=AudioType.MUSIC_TRACK, loop=True)
        self.play()

    def play(self):
        print('=== SETUP ===')
        print_with_delay("1. How many competitors do you want?")
        print_with_delay("[Pick a number from 1 to 7]")
        response = int(Player.get_response(PromptType.NUMBER, default_response=4))
        num_npc_contestants = response
        if response > GameManager.max_contestants:
            num_npc_contestants = GameManager.max_contestants
        elif response < GameManager.min_contestants:
            num_npc_contestants = GameManager.min_contestants
        print_with_delay("2. What is your name?")
        player_name = Player.get_response(PromptType.STRING, default_response="John Smith")
        print_with_delay("3. Where are you from?")
        player_location = Player.get_response(PromptType.STRING, default_response="Gallifrey")
        print_with_delay("4. What do you do?")
        player_occupation = Player.get_response(PromptType.STRING, default_response="Traveler")

        player = Player(player_name, player_location, player_occupation)

        GameManager.contestants = generate_random_npc_contestants(num_npc_contestants)
        GameManager.contestants.add(player)

        print("=== COMPLETE ===")
        Player.get_response(PromptType.CONTINUE)
        GameManager.scene_queue.put(SceneTypes.INTRODUCTION)

    def on_scene_exit(self):
        clear_screen()


