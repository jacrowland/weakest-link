from audioop import reverse
from queue import Queue
from threading import Timer
from time import time
from random import randrange
from typing import Deque
from contestants.contestant_base import Contestant

from engine.game_manager import GameManager
from questions.question import Question

class Vote():
    __slots__ = ("_caster", "_vote")
    def __init__(self, contestant:Contestant, vote:Contestant):
        self._caster = contestant
        self._vote = vote
    
    @property
    def caster(self)->Contestant:
        return self._caster
    
    @property
    def vote(self)->Contestant:
        return self._vote

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

class RoundInfo():
    def __init__(self, contestants:list, number=1):
        self.number = number
        self.participanting_contestants = contestants
        self.questions_responses = []
        self.votes = set() # (Caster:Contestant, Vote:Contestant)
        self.amount_banked = 0

        self.contestant_order = Queue() # TODO: remove attribute from this class
        self.contestant_order.queue = Deque(contestants)

    @property
    def most_votes(self):
        if len(self.votes) > 0:
            tally = {}
            for vote in self.votes:
                contestant = vote.vote
                tally[contestant] = 1 if contestant not in tally else tally[contestant] + 1
            return sorted(enumerate(tally), key=lambda tup: tup[0], reverse=True)[0]
        else:
            return None

    def _calculate_round_contestant_statistics(self, contestant):
        questions_answered = [q for q in self.questions_responses if q.contestant == contestant]
        num_correct = len([q for q in questions_answered if q.is_correct])
        num_incorrect = len(questions_answered) - num_correct

        per_correct = num_correct / len(questions_answered) if len(questions_answered) > 0 else 0
        per_incorrect = num_incorrect / len(questions_answered) if len(questions_answered) > 0 else 0

        round_statistics_dict = {
            "round_number": self.number,
            "num_correct": num_correct,
            "per_correct": per_correct,
            "num_incorrect": num_incorrect,
            "per_incorrect": per_incorrect,
            "total_questions_answered": len(questions_answered)         
        }
        return round_statistics_dict

    @property
    def strongest_link(self):
        # TODO: Deal with ties
        lst = [(c, self._calculate_round_contestant_statistics(c)["per_correct"]) for c in self.participanting_contestants]
        return sorted(lst, key=lambda tup: tup[1])[0]

    @property
    def weakest_link(self):
        # TODO: Deal with ties
        lst = [(c, self._calculate_round_contestant_statistics(c)["per_incorrect"]) for c in self.participanting_contestants]
        return sorted(lst, key=lambda tup: tup[1])[0]

class RoundQuestionResponse():
    __slots__ = ("question", "contestant", "is_correct")
    def __init__(self, question:Question, contestant:Contestant, is_correct:bool):
        self.question = question
        self.contestant = contestant
        self.is_correct = is_correct



