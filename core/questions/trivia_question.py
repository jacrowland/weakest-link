from ctypes.wintypes import BOOLEAN
import enum
import json
from secrets import choice
import urllib.request
from html import unescape
from random import shuffle

from questions.question import Question, QuestionTypes, question_types

class TriviaQuestionDifficulties(enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class TriviaQuestionCategory(enum.IntEnum):
    GENERAL_KNOWLEDGE = 9
    BOOKS = 10
    FILM = 11
    MUSIC = 12
    MUSICALS_AND_THEATRE = 13
    TELEVISION = 14
    VIDEO_GAMES = 15
    BOARD_GAMES = 16
    SCIENCE_AND_NATURE = 17
    COMPUTERS = 18
    MATHEMATICS = 19
    MYTHOLOGY = 20
    SPORTS = 21
    GEOGRAPHY = 22
    HISTORY = 23
    POLITICS = 24
    ART = 25
    CELEBRITIES = 26
    ANIMALS = 27
    VEHICLES = 28
    COMICS = 29
    GADGETS = 30
    JAPANESE_ANIME = 31

class TriviaQuestion(Question):
    def __init__(self, difficulty:TriviaQuestionDifficulties=None, 
                        type:QuestionTypes=None, 
                        category:TriviaQuestionCategory=None):
        super().__init__(type)
        self._difficulty = difficulty
        self._category = category
        self._choices = None
        self._get_question_from_api()

    def _build_api_url(self):
        url = "https://opentdb.com/api.php?"
        amount = 1
        url = url + "&amount={}".format(amount)
        #https://opentdb.com/api.php?amount=1&category=16&difficulty=easy&type=multiple

        if self._type != None:
            url = url + "&type={}".format(question_types[self._type])
        if self._category != None:
            url = url + "&category={}".format(self._category)
        if self._difficulty != None:
            url = url + "&difficulty={}".format(self._difficulty.value)

        return url

    def _get_question_from_api(self):
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
    question = TriviaQuestion(TriviaQuestionDifficulties.EASY, QuestionTypes.MULTIPLE, TriviaQuestionCategory.ANIMALS)
    #import sys
    #print(sys.argv[1])
    print(question)
