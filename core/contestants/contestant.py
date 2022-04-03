import enum
from abc import ABC, abstractmethod
from random import choice
from unicodedata import name
from questions.trivia_question import TriviaQuestion
from contestants.personality import PersonalityType

import names

class PromptTypes(enum.IntEnum):
    TRIVIA_QUESTION = 1
    VOTE = 2
    BANK = 3
    NUMBER = 4
    STRING = 5
    CONTINUE = 6

class ContestantType(enum.IntEnum):
    PLAYER = 1
    NPC = 2

class Contestant(ABC):
    def __init__(self, name:str, location:str, occupation:str):
        self._name = name
        self._location = location
        self._occupation = occupation

    def __str__(self):
        return f'Name: {self.name}\nLocation: {self._location}\nOccupation: {self._occupation}'

    @abstractmethod
    def get_response(self, prompt_type:PromptTypes, prompt, default_response=0)->str:
        pass

    @property
    def name(self):
        return self._name

    @property
    def location(self):
        return self._location
    
    @property
    def occupation(self):
        return self._occupation

class NPC(Contestant):
    def __init__(self, name:str, location:str, occupation:str, personality_type:PersonalityType=PersonalityType.GENERIC):
        super().__init__(name, location, occupation)
        self.personality_type = personality_type

    def get_response(self, prompt_type: PromptTypes, prompt) -> str:
        response = 0
        if prompt_type is PromptTypes.TRIVIA_QUESTION:
            response = self._answer_trivia_question(prompt)
        elif prompt_type is PromptTypes.VOTE:
            # get all contestants from the round manager
            # filter out yourself
            # rank based on
            #   how many questions they got right (cautiousness)
            #   how many times they have voted against you (hostility)
            pass
        elif prompt_type is PromptTypes.BANK:
            # get bank from round manager
            # choose if they want to bank based on how cautious the NPC is
            # inverse likelihood based on current bank position
                # the higher the bank is the MORE likely a cautious NPC will choose to bank
            pass

        return response

    def _answer_trivia_question(self, question:TriviaQuestion):
        answer = question.choices[0]
        """
        if (question._category in personalities[self.personality_type].strength_categories):
            answer = choice(question.correct_answers)
        elif (question._category in personalities[self.personality_type]._weakness_categories):
            answer = choice(question.incorrect_answers)
        else:
            answer = choice(question.choices)
        """
        # get the current question from the round manager
            # calculate the likelyhood that they get the answer correct
                #   if it is a strength the chance is increased
                #   if it is a weakness the chance is decreased
            # if they are likely to not get it right
                # return a random incorrect answer
            # else
                # return correct answer
        return answer

    def _calculate_probability(self):
        return 0

class Player(Contestant):
    def __init__(self, name:str, location:str, occupation:str):
        super().__init__(name=name, location=location, occupation=occupation)
    
    @classmethod
    def get_response(self, prompt_type:PromptTypes=PromptTypes.CONTINUE, prompt=None, input_txt:str="> ", default_response=0) -> str:
        valid_response = False

        while not valid_response:
            response = input(input_txt).strip()
            if prompt_type is PromptTypes.NUMBER:
                if response.isnumeric():
                    valid_response = True
                else:
                    print("You must enter a number.")
            if prompt_type is PromptTypes.STRING:
                if response == '':
                    response = default_response
                valid_response = True
            elif prompt_type is PromptTypes.CONTINUE:
                valid_response = True
                response = default_response
                    
        return response
