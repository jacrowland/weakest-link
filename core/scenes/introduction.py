
from contestants.contestant_base import Contestant
from .scene_base import SceneBase
from .scene_types import SceneTypes
from engine.game_manager import GameManager
from engine.sound.sound_manager import SoundManager
from engine.sound.sound_enums import Sounds, AudioType
from contestants.player import Player
from contestants.npc import NPC
from contestants.contestant_enums import PromptType

from bank import Bank

from utils import print_with_delay, clear_screen
from images.utils import print_ascii_art_from_file

from time import sleep

from .rounds.regular_round import RegularRoundScene

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
        Player.get_response(prompt_type=PromptType.CONTINUE)
        clear_screen()
        print_with_delay('Host: The others will leave with nothing when voted off as the...')
        SoundManager.play_sound(Sounds.STING, loop=False, audio_type=AudioType.SFX)
        print_ascii_art_from_file(r"assets\ascii_art\logo.txt", delay=0.15)
        Player.get_response(prompt_type=PromptType.CONTINUE)
        clear_screen()

        print_with_delay('Host: Any of the contestants in the studio here today could win up to $10,000.')
        print_with_delay('Host: They\'ve only just met but to get the prize money they\'ll have to work together.')
        print_with_delay('Host: However, most will leave with nothing.')
        print_with_delay('Host: Round by round we lose the player VOTED...')
        print_with_delay('...THE WEAKEST LINK!')

        Player.get_response(prompt_type=PromptType.CONTINUE)

        clear_screen()

        print_with_delay("Host: Let's meet the team.")

        Player.get_response(prompt_type=PromptType.CONTINUE)

        clear_screen()

        print_ascii_art_from_file(r"assets\ascii_art\contestant_at_podium.txt", delay=0.15)
        for contestant in GameManager.contestants:
            if isinstance(contestant, Contestant):
                print_with_delay(f"{contestant.name}: Hi I'm {contestant.name}. I am from {contestant.location} and I am a {contestant.occupation}")
                sleep(1)

        clear_screen()

        print_with_delay('Host: Now the rules.')
        print_with_delay('Host: In each round the aim is to answer enough questions correctly to reach our $1000 target within the time limit.')
        print_with_delay('Host: The fastest way is to create a chain of nine correct answers.')


        example_bank = Bank()
        example_bank.current_pos = 6
        print()
        for i in range(3):
            print(example_bank, "\n")
            example_bank.increment()
            sleep(1)

        Player.get_response(PromptType.CONTINUE)


        print_with_delay('Host: Get your question wrong and you break the chain and you lose all the money in that chain.')

        example_bank.reset_chain()
        print("\n", example_bank, "\n")

        Player.get_response(PromptType.CONTINUE)

        print_with_delay('Host: But if you say BANK! before the question is asked the money is safe.')

        example_bank.current_pos = 8
        print("\n", example_bank, "\n")
        print("\n> Bank!")
        sleep(1)
        example_bank.save()
        print(example_bank, "\n")

        print_with_delay('Host: However, you start a new chain from scratch.')
        print_with_delay('Host: At the end of the round only money that has been banked can be taken forward.')

        Player.get_response(PromptType.CONTINUE)

        GameManager.scene_queue.put(RegularRoundScene())

        self.on_scene_exit()

    def on_scene_exit(self):
        clear_screen()


