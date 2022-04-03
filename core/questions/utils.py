from html import unescape
from unicodedata import category
import urllib
import json

from .trivia_question import TriviaQuestion

from .question_enums import QuestionType, TriviaQuestionDifficultyType, TriviaQuestionCategory

from random import choice

def _build_api_url(type:str, category:int, difficulty:str, amount:int=1, ):
    url = "https://opentdb.com/api.php?"
    amount = 1
    url = url + "&amount={}".format(1)
    url = url + "&type={}".format(type.lower()) if type != None else url
    url = url + "&category={}".format(category) if category != None else url
    url = url + "&difficulty={}".format(difficulty.lower()) if difficulty != None else url
    return url #e.g https://opentdb.com/api.php?amount=1&category=16&difficulty=easy&type=multiple

def get_question_from_api(type:str, category:int, difficulty:str, amount=1):

    url = _build_api_url(type, category, difficulty)

    with urllib.request.urlopen(url) as f:
        result = json.loads(f.read())
        result = result['results']

    question = unescape(result[0]['question'])
    incorrect_answers = [unescape(incorrect_answer) for incorrect_answer in result[0]['incorrect_answers']]
    correct_answers = [f"{unescape(result[0]['correct_answer'])}"]
    trivia_question = TriviaQuestion(question, correct_answers, incorrect_answers)

    return trivia_question

def get_random_question_from_api():
    type = choice(list(QuestionType)).name.lower()
    category = choice(list(TriviaQuestionCategory)).value
    difficulty = choice(list(TriviaQuestionDifficultyType)).name.lower()
    question = get_question_from_api(type, category, difficulty)
    return question
