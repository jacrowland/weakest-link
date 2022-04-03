from .question_enums import QuestionType

class Question():
    def __init__(self, type:QuestionType=None):
        self._question = None
        self._correct_answers = None
        self._incorrect_answers = None
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