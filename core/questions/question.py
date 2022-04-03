from .question_enums import QuestionType

class Question():
    def __init__(self, question:str, correct_answers:list[str], incorrect_answers:list[str], type:str=None):
        self._question = question
        self._correct_answers = correct_answers
        self._incorrect_answers = incorrect_answers
        self._type = type

    @property
    def question(self):
        return self._question

    @property
    def correct_answers(self):
        return self._correct_answers
    
    @property
    def incorrect_answers(self):
        return self._incorrect_answers