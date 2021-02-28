import json 
import urllib.request
import html
import random

class Question():
    def __init__(self):
        self._question = None
        self._choices = []
        self._correctAnswer = None
        # Retrieve a question from the Open Trivia DB
        self.restrieveQuestion()
        # Randomise the order of the answers
        self.shuffleChoices()

    """
    retrieveQuestion(self)
    Pulls a question from the Open Trivia DB, cleans it up, and stores the result
    """
    def restrieveQuestion(self):
        #print(json.dumps(resultDict, indent = 4, sort_keys=True))
        with urllib.request.urlopen("https://opentdb.com/api.php?amount=1&type=multiple") as f:
            result = json.loads(f.read())
        
        # get data from json
        self._question = html.unescape(result['results'][0]['question'])
        self._choices = result['results'][0]['incorrect_answers']
        # unescape all the choices and add to one list
        for i in range(len(self._choices)):
            self._choices[i] = html.unescape(self._choices[i])
        self._correctAnswer = html.unescape(result['results'][0]['correct_answer'])
        self._choices.append(self._correctAnswer)

    """
    shuffleChoices(self)
    Randomises the position of the elements in the choices list
    """
    def shuffleChoices(self):
        random.shuffle(self._choices)
        
    @property
    def question(self):
        return self._question
    @property
    def choices(self):
        return self._choices
    @property
    def correctAnswer(self):
        return self._correctAnswer

