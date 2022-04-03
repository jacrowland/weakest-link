from random import shuffle
from .question import Question, QuestionType
from .question_enums import QuestionType, TriviaQuestionCategory, TriviaQuestionDifficultyType

class TriviaQuestion(Question):
    def __init__(self, question, correct_answers, incorrect_answers, type, difficulty, category):
        super().__init__(type)
        self._difficulty = difficulty
        self._category = category
        self._choices = shuffle([*self.incorrect_answers, *self._correct_answers])

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
    question = TriviaQuestion(TriviaQuestionDifficultyType.EASY, QuestionType.MULTIPLE, TriviaQuestionCategory.ANIMALS)
    print(question)
