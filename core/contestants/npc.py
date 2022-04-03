from .contestant_base import Contestant
from .personality import PersonalityType
from .contestant_enums import PromptType
from questions.trivia_question import TriviaQuestion

class NPC(Contestant):
    def __init__(self, name:str, location:str, occupation:str, personality_type:PersonalityType=PersonalityType.GENERIC):
        super().__init__(name, location, occupation)
        self.personality_type = personality_type

    def get_response(self, prompt_type: PromptType, prompt) -> str:
        response = 0
        if prompt_type is PromptType.TRIVIA_QUESTION:
            response = self._answer_trivia_question(prompt)
        elif prompt_type is PromptType.VOTE:
            # get all contestants from the round manager
            # filter out yourself
            # rank based on
            #   how many questions they got right (cautiousness)
            #   how many times they have voted against you (hostility)
            pass
        elif prompt_type is PromptType.BANK:
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
