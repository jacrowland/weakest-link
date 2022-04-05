from threading import Timer
from typing import Deque

from bank import Bank

from questions.question import Question
from questions.utils import get_random_question_from_api

from ..scene_base import SceneBase
from ..scene_types import SceneTypes
from engine.game_manager import GameManager
from engine.sound.sound_manager import SoundManager
from engine.sound.sound_enums import Sounds, AudioType

from contestants.player import Player
from contestants.npc import NPC
from contestants.contestant_enums import PromptType
from contestants.utils import generate_random_npc_contestants

from utils import print_with_delay, clear_screen
from images.utils import print_ascii_art_from_file
from time import sleep, time
from threading import Timer
from queue import Queue
from random import randrange


class RoundInfo():
    def __init__(self, contestants:list, number=1):
        self.number = number
        self.contestant_order = Queue()
        self.contestant_order.queue = Deque(contestants)
        self.timer = None
        self.questions = []
        self.votes = None # (Caster:Contestant, Vote:Contestant)
        self.amount_banked = 0

class RoundQuestionResponse():
    __slots__ = ("question", "contestant", "is_correct")
    def __init__(self, question:Question, contestant, is_correct):
        self.question = question
        self.contestant = contestant
        self.is_correct = is_correct

class RoundTimer(Timer):
    started_at = None
    def start(self):
        self.started_at = time()
        Timer.start(self)
    def elapsed(self)->float:
        return time() - self.started_at
    def remaining(self):
        remaining = (self.interval - self.elapsed()) if self.is_alive() else 0
        return remaining
        
    def _seconds_remaining(self):
        return self.remaining() // 60
    def _minutes_remaining(self):
        return self._seconds_remaining() // 60

def format_time(seconds_remaining:float)->str:
    minutes_remaining = int(seconds_remaining// 60)
    remainder_seconds = int(seconds_remaining - (minutes_remaining * 60))
    if len(str(remainder_seconds)) == 1:
        remainder_seconds = f'0{remainder_seconds}'
    return f"{minutes_remaining}:{remainder_seconds} remaining..."

class RegularRoundScene(SceneBase):
    def __init__(self, round_length=180):

        #GameManager.contestants = generate_random_npc_contestants(3)
        #GameManager.player = Player("Jacob", "Auckland", "Student")

        super(RegularRoundScene, self).__init__(scene_type=SceneTypes.REGULAR_ROUND)
        contestant_list = list(filter(lambda c: not c.eliminated, list(GameManager.contestants)))
        self.sorted_contestant_list = sorted(contestant_list, key=lambda c: c.name)
        self.round_info = RoundInfo(contestants = self.sorted_contestant_list)
        self.timer = RoundTimer(round_length, clear_screen)
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

    def _bank(self, current_contestant=GameManager.player):
        print("\n", GameManager.bank, "\n")
        bank_response = current_contestant.get_response(PromptType.BANK, default_response="Bank!")
        print_with_delay(f"{current_contestant.name}: {bank_response}")
        if bank_response == "Bank!":
            amount_banked = GameManager.bank.save()
            self.round_info.amount_banked += amount_banked
            print("\n", GameManager.bank, "\n")
        sleep(2)
        clear_screen()

    def _main_question_loop(self):
        self.timer.start()
        while self.timer.is_alive():
            clear_screen()
            # Get contestant from start of queue and add to back (allows loop)
            current_contestant = self.round_info.contestant_order.get()
            self.round_info.contestant_order.put(current_contestant)
            print_with_delay(f"Host: {current_contestant.name}.")

            print_with_delay(format_time(self.timer.remaining()))
            self._bank(current_contestant)
            print_with_delay(f"{format_time(self.timer.remaining())}\n")
            try:
                trivia_question = get_random_question_from_api()
            except Exception:
                print("Could not retrieve question from OTDB. Ending question time...")
                sleep(3)
                break
            print_with_delay(f"Host: {trivia_question.question}\n")
            for i, choice in enumerate(trivia_question.choices):
                print_with_delay(f'{i+1}) {choice}')
            print()
            response = current_contestant.get_response(prompt_type=PromptType.TRIVIA_QUESTION, prompt=trivia_question)
            round_question_response = RoundQuestionResponse(trivia_question, current_contestant, trivia_question.check_answer(str(response)))
            print_with_delay(f"{current_contestant.name}: {response}")
            if round_question_response.is_correct:
                print_with_delay("Host: That is the correct answer.")
            else:
                print_with_delay(f"Host: Nope. The correct answer is {trivia_question.correct_answers[0]}.")
            if isinstance(current_contestant, NPC):
                sleep(2)
            else:
                GameManager.player.get_response(PromptType.CONTINUE)

        clear_screen()
        SoundManager.play_sound(Sounds.STING, loop=False, audio_type=AudioType.SFX)
        print_with_delay(f"Host: Time's up.\n")
        GameManager.player.get_response(PromptType.CONTINUE)
        print_with_delay(f"Host: In this round you managed to bank ${self.round_info.amount_banked}\n")
        GameManager.player.get_response(PromptType.CONTINUE)

        
    def play(self):
        self._introduce_round()
        self._main_question_loop()
        #GameManager.scene_queue.put(RoundEliminationScene(self.round_info))
        self.on_scene_exit()

    def on_scene_exit(self):
        clear_screen()
