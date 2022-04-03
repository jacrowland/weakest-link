from asyncore import loop
from pickle import TRUE
from time import sleep
from turtle import clear, delay
from engine.sound_manager import SoundManager, AudioType
from scenes.scene_base import SceneBase, SceneTypes

from engine.game_manager import GameManager
from engine.sound_manager import SoundManager, Sounds, AudioType
from contestants.contestant import Player, PromptTypes, NPC

from utils import print_with_delay, clear_screen
from images.utils import print_ascii_art_from_file, get_ascii_image, print_ascii_art




class IntroductionScene(SceneBase):
    def __init__(self):
        super(IntroductionScene, self).__init__(scene_type=SceneTypes.INTRODUCTION)
        SoundManager.play_sound(Sounds.CREDITS, loop=True, audio_type=AudioType.MUSIC_TRACK)

    def on_scene_enter(self):
        clear_screen()
        self.play()

    def play(self):
        print_ascii_art_from_file(r"assets\ascii_art\anne.txt", delay=0.15)
        print_with_delay("Host: Welcome to The Weakest Link.")
        print_with_delay(f'Host: In today\'s show our {len(list(GameManager.contestants))} contestants will win up to $10,000.')
        Player.get_response(prompt_type=PromptTypes.CONTINUE)
        clear_screen()
        print_with_delay('Host: The others will leave with nothing when voted off as the...')
        SoundManager.play_sound(Sounds.STING, loop=False, audio_type=AudioType.SFX)
        print_ascii_art_from_file(r"assets\ascii_art\logo.txt", delay=0.15)
        Player.get_response(prompt_type=PromptTypes.CONTINUE)
        clear_screen()

        print_with_delay('Host: Any of the contestants in the studio here today could win up to $10,000.')
        print_with_delay('Host: They\'ve only just met but to get the prize money they\'ll have to work together.')
        print_with_delay('Host: However, most will leave with nothing.')
        print_with_delay('Host: Round by round we lose the player VOTED...')
        print_with_delay('...THE WEAKEST LINK!')

        Player.get_response(prompt_type=PromptTypes.CONTINUE)

        clear_screen()

        print_with_delay("Host: Let's meet the team.")

        Player.get_response(prompt_type=PromptTypes.CONTINUE)

        for contestant in GameManager.contestants:
            if isinstance(contestant, NPC):
                print_with_delay(f"{contestant.name}: Hi I'm {contestant.name}. I am from {contestant.location} and I am a {contestant.occupation}")
            elif isinstance(contestant, Player):
                print("[Introduce yourself to the contestants]")
                Player.get_response(PromptTypes.STRING)

        Player.get_response(PromptTypes.CONTINUE)

        clear_screen()




        # when some condition is met transition to the next scene
        self.on_scene_exit()

    def on_scene_exit(self):
        clear_screen()


