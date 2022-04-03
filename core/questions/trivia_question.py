import enum
import json
import urllib.request
from html import unescape
from random import shuffle
from .question import Question, QuestionType
from .question_enums import QuestionType, TriviaQuestionCategory, TriviaQuestionDifficulties

class TriviaQuestion(Question):
    def __init__(self, difficulty:TriviaQuestionDifficulties=None, 
                        type:QuestionType=None, 
                        category:TriviaQuestionCategory=None):
        super().__init__(type)
        self._difficulty = difficulty
        self._category = category
        self._choices = None
        self._get_question_from_api()

    def _build_api_url(self): # TODO : Refactor out of this class
        url = "https://opentdb.com/api.php?"
        amount = 1
        url = url + "&amount={}".format(1)
        url = url + "&type={}".format(self._type.name.lower()) if self._type != None else url
        url = url + "&category={}".format(self._category) if self._category != None else url
        url = url + "&difficulty={}".format(self._difficulty.name.lower()) if self._difficulty != None else url
        return url #e.g https://opentdb.com/api.php?amount=1&category=16&difficulty=easy&type=multiple

    def _get_question_from_api(self): # TODO : Refactor out of this class
        with urllib.request.urlopen(self._build_api_url()) as f:
            result = json.loads(f.read())
            result = result['results']
            self._question = unescape(result[0]['question'])
            self._incorrect_answers = [unescape(incorrect_answer) for incorrect_answer in result[0]['incorrect_answers']]
            self._correct_answers = [f"{unescape(result[0]['correct_answer'])}"]
            self._choices = [*self.incorrect_answers, *self._correct_answers]
            self._shuffle_choices()

    def check_answer(self, response:str)->bool:
        return response.lower() in [answer.lower() for answer in self.correct_answers]

    @property
    def choices(self)->list[str]:
        return self._choices

    @property
    def category(self):
        return self._category

    @property
    def difficulty(self):
        return self._difficulty
    
    def _shuffle_choices(self):
        shuffle(self._choices)

    def __str__(self):
        return "Question: {0}\nCorrect Answers: {1}\nIncorrect Answers: {2}".format(self._question, self._correct_answers, self._incorrect_answers)

if __name__ == "__main__":
    question = TriviaQuestion(TriviaQuestionDifficulties.EASY, QuestionType.MULTIPLE, TriviaQuestionCategory.ANIMALS)
    print(question)
