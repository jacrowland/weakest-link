from threading import Timer
from typing import Deque
from ..scene_base import SceneBase
from ..scene_types import SceneTypes
from engine.game_manager import GameManager
from engine.sound.sound_manager import SoundManager
from engine.sound.sound_enums import Sounds, AudioType
from contestants.player import Player
from contestants.npc import NPC
from contestants.contestant_enums import PromptType
from questions.utils import get_random_question_from_api
from utils import print_with_delay, clear_screen
from images.utils import print_ascii_art_from_file
from time import sleep, time
from threading import Timer
from queue import Queue
from random import randrange
from contestants.utils import generate_random_npc_contestants
class RoundInfo():
    def __init__(self, contestants:list, number=1):
        self.number = number
        self.contestant_order = Queue()
        self.contestant_order.queue = Deque(contestants)
        self.timer = None
        self.questions = []
class RoundTimer(Timer):
    started_at = None
    def start(self):
        self.started_at = time()
        Timer.start(self)
    def elapsed(self)->float:
        return time() - self.started_at
    def remaining(self):
        return self.interval - self.elapsed()
    def _seconds_remaining(self):
        return self.remaining() // 60
    def _minutes_remaining(self):
        return self._seconds_remaining() // 60

def format_time(seconds_remaining:float)->str:
    minutes_remaining = int(seconds_remaining// 60)
    return f"{minutes_remaining}:{int(seconds_remaining - (minutes_remaining * 60))} remaining..."

class RegularRoundScene(SceneBase):
    def __init__(self):
        super(RegularRoundScene, self).__init__(scene_type=SceneTypes.REGULAR_ROUND)
        contestant_list = list(filter(lambda c: not c.eliminated, list(GameManager.contestants)))
        self.sorted_contestant_list = sorted(contestant_list, key=lambda c: c.name)
        self.round_info = RoundInfo(contestants = self.sorted_contestant_list)
        self.timer = RoundTimer(180, clear_screen)
        GameManager.rounds.add(self.round_info)

    def on_scene_enter(self):
        clear_screen()
        SoundManager.play_sound(Sounds.MAIN_THEME, loop=True, audio_type=AudioType.MUSIC_TRACK)
        GameManager.bank.reset_chain()
        self.play()

    def _introduce_round(self):
        print_ascii_art_from_file(r"assets\ascii_art\anne_lean_on_podium.txt", delay=0.15)
        print_with_delay("Host: Round One. Three minutes on the clock.")
        print_with_delay("Host: We will start with the contestant whose name is first alphabetically.")
        print_with_delay(f"Host: That's you {self.sorted_contestant_list[0].name}.")
        print_with_delay("Host: Let's play...")
        SoundManager.play_sound(Sounds.STING, loop=False, audio_type=AudioType.SFX)
        print_with_delay("Host: ...THE WEAKEST LINK.")
        Player.get_response(prompt_type=PromptType.CONTINUE)

    def _ask_questions(self):
        SoundManager.play_sound(Sounds.QUESTION_BED, loop=True, audio_type=AudioType.MUSIC_TRACK)
        self.timer.start()
        self._main_question_loop()
        SoundManager.play_sound(Sounds.STING, loop=False, audio_type=AudioType.SFX)
        print_with_delay("Host: Time's up!") 
        Player.get_response(prompt_type=PromptType.CONTINUE)

    def _main_question_loop(self):
        while self.timer.is_alive():
            print_with_delay(format_time(self.timer.remaining()))
            current_contestant = self.round_info.contestant_order.get()
            self.round_info.contestant_order.put(current_contestant)
            print_with_delay(f"\nHost: {current_contestant.name}.")
            trivia_question = get_random_question_from_api()
            self.round_info.questions.append(trivia_question)
            print_with_delay(f"Host: {trivia_question.question}\n")
            for i, choice in enumerate(trivia_question.choices):
                print_with_delay(f'{i+1}) {choice}')
            print()
            if isinstance(current_contestant, NPC):
                sleep(randrange(2, 5))
            response = current_contestant.get_response(PromptType.TRIVIA_QUESTION, prompt=trivia_question)
            print_with_delay(f"{current_contestant.name}: {response}")
            if trivia_question.check_answer(str(response)):
                print_with_delay("Host: Correct.")
            else:
                print_with_delay(f"Host: Nope. {trivia_question.correct_answers[0]}")
            clear_screen()
        
    def play(self):
        self._introduce_round()
        self._main_question_loop()
        self.on_scene_exit()

    def on_scene_exit(self):
        clear_screen()
