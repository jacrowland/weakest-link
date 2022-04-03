import enum

class QuestionType(enum.IntEnum):
    BOOLEAN = 1
    MULTIPLE = 2


class TriviaQuestionDifficulties(enum.IntEnum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

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