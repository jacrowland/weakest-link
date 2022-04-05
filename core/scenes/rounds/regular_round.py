from typing import Deque

from contestants.utils import generate_random_npc_contestants
from scenes.rounds.round_elimination import RoundEliminationScene
from questions.utils import get_random_question_from_api
from ..scene_base import SceneBase
from ..scene_types import SceneTypes
from engine.game_manager import GameManager
from engine.sound.sound_manager import SoundManager
from engine.sound.sound_enums import Sounds, AudioType
from contestants.player import Player
from contestants.npc import NPC
from contestants.contestant_enums import PromptType
from utils import print_with_delay, clear_screen, format_time, get_remaining_contestants
from .utils import RoundTimer, RoundInfo, RoundQuestionResponse
from images.utils import print_ascii_art_from_file
from time import sleep

class RegularRoundScene(SceneBase):
    def __init__(self, round_length=180, round_number=1):

        GameManager.contestants = generate_random_npc_contestants(3)
        GameManager.player = Player("Jacob", "Auckland", "Student")
        GameManager.contestants.add(GameManager.player)

        super(RegularRoundScene, self).__init__(scene_type=SceneTypes.REGULAR_ROUND)
        contestant_list = get_remaining_contestants(GameManager.contestants)
        self.sorted_contestant_list = sorted(contestant_list, key=lambda c: c.name)
        self.round_info = RoundInfo(contestants = self.sorted_contestant_list, number=round_number)
        self.timer = RoundTimer(round_length, clear_screen)
        GameManager.rounds.add(self.round_info)

    def on_scene_enter(self):
        clear_screen()
        SoundManager.play_sound(Sounds.MAIN_THEME, loop=True, audio_type=AudioType.MUSIC_TRACK)
        GameManager.bank.reset_chain()
        self.play()

    def _introduce_round(self):
        print_ascii_art_from_file(r"assets\ascii_art\anne_lean_on_podium.txt", delay=0.15)
        print_with_delay(f"Host: Round {self.round_info.number}.")
        print_with_delay("Host: We will start with the contestant whose name is first alphabetically.")
        print_with_delay(f"Host: That's you {self.sorted_contestant_list[0].name}.")
        print_with_delay("Host: With three minutes on the clock. Let's play...")
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
            if not self.timer.is_alive():
                break

            # Get contestant from start of queue and add to back (allows loop)
            current_contestant = self.round_info.contestant_order.get()
            self.round_info.contestant_order.put(current_contestant)
            print_with_delay(f"Host: {current_contestant.name}.\n")

            print_with_delay(format_time(self.timer.remaining()))
            self._bank(current_contestant)

            if not self.timer.is_alive():
                break

            print_with_delay(f"{format_time(self.timer.remaining())}\n", delay=0)
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

            if not self.timer.is_alive():
                break

            response = current_contestant.get_response(prompt_type=PromptType.TRIVIA_QUESTION, prompt=trivia_question)
            round_question_response = RoundQuestionResponse(trivia_question, current_contestant, trivia_question.check_answer(str(response)))
            
            self.round_info.questions_responses.append(round_question_response)

            print_with_delay(f"{current_contestant.name}: {response}")

            if round_question_response.is_correct:
                print_with_delay("Host: That is the correct answer.")
            else:
                print_with_delay(f"Host: Nope. The correct answer is {trivia_question.correct_answers[0]}.")
            if isinstance(current_contestant, NPC):
                sleep(3)
            else:
                GameManager.player.get_response(PromptType.CONTINUE)

        clear_screen()
        SoundManager.play_sound(Sounds.STING, loop=False, audio_type=AudioType.SFX)
        print_with_delay(f"Host: Time's up.\n")
        print_with_delay(f"Host: In this round you managed to bank ${self.round_info.amount_banked}\n")
        GameManager.player.get_response(PromptType.CONTINUE)
        
    def play(self):
        #self._introduce_round()
        self._main_question_loop()
        GameManager.scene_queue.put(RoundEliminationScene(self.round_info))
        self.on_scene_exit()

    def on_scene_exit(self):
        clear_screen()
        SoundManager.stop_playing()
        pass
