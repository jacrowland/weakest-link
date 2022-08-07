from contestants.contestant_enums import PromptType
from contestants.player import Player
from utils import clear_screen
from questions.question import Question
from questions.question_enums import QuestionType
from scenes.rounds.utils import RoundInfo, Vote
from scenes.scene_base import SceneBase, SceneTypes
from contestants.npc import NPC
from contestants.player import Player
from time import sleep

#from .regular_round import RegularRoundScene

from utils import print_with_delay, get_contestant_from_name, get_remaining_contestants

from engine.game_manager import GameManager

class RoundEliminationScene(SceneBase):
    def __init__(self, round_info:RoundInfo):
        super().__init__(scene_type=SceneTypes.ROUND_VOTING)
        self.round_info = round_info

    def on_scene_enter(self):
        self.play()
    
    def on_scene_exit(self):
        return super().on_scene_exit()

    def play(self):
        print_with_delay("Host: Now it is time for you to vote for who you believe was the weakest link in that round...")

        question = Question("Who do you vote for?", correct_answers=[c.name for c in self.round_info.participanting_contestants], incorrect_answers=[], type=QuestionType.MULTIPLE)
        
        print_with_delay(f"Host: {question.question}\n")
        for i, choice in enumerate(question.correct_answers):
            print_with_delay(f'{i+1}) {choice}')
        print()
        
        for contestant in self.round_info.participanting_contestants:
            if isinstance(contestant, NPC):
                contestant_voted_for = contestant.get_response(PromptType.VOTE, prompt=self.round_info)
            elif isinstance(contestant, Player):
                response = contestant.get_response(PromptType.STRING, prompt=self.round_info, input_txt="[Type out your vote] > ", default_response="")
                contestant_voted_for = get_contestant_from_name(response, list(self.round_info.participanting_contestants))
            
            if not contestant_voted_for is None:
                vote = Vote(contestant, contestant_voted_for)
                self.round_info.votes.add(vote)

        clear_screen()

        print_with_delay("Host: Show us your votes.\n")

        for vote in self.round_info.votes:
            print_with_delay(f"{vote.caster.name}: {vote.vote.name}")

        GameManager.player.get_response(PromptType.CONTINUE)
        clear_screen()

        print_with_delay(f"Host: That round {self.round_info.strongest_link[0].name} was the strongest link.")
        sleep(1)
        print_with_delay(f"Host: {self.round_info.weakest_link[0].name} was statistically the weakest link that round...")
        sleep(0.5)
        print_with_delay("Host: ...but it is the votes that count.")
        GameManager.player.get_response(PromptType.CONTINUE)
        clear_screen()

        num_votes, contestant_to_eliminate = self.round_info.most_votes
        print_with_delay(f"Host: With {num_votes} votes. {contestant_to_eliminate.name} is the weakest link.")
        print_with_delay(f"Host: Goodbye.", delay=0.3)
        contestant_to_eliminate.eliminated = True
        print_with_delay(f"{contestant_to_eliminate.name} has been eliminated from the competition.")
        GameManager.player.get_response(PromptType.CONTINUE)

        """
        if len(get_remaining_contestants(GameManager.contestants)) > 2:
            GameManager.scene_queue.put(RegularRoundScene(self.round_info.number + 1))
        """

        # if only two remaining then start the FINAL ROUND 
        # else start a new REGULAR ROUND




            
        

