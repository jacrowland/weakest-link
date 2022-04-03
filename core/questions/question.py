import enum

class QuestionTypes(enum.IntEnum):
    BOOLEAN = 1
    MULTIPLE = 2

question_types = {}
question_types[QuestionTypes.BOOLEAN] = "boolean"
question_types[QuestionTypes.MULTIPLE] = "multiple"

class Question():
    def __init__(self, type:QuestionTypes=None):
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