from questions.trivia_question import TriviaQuestionCategory
import enum

class NPCPersonality():
    def __init__(self, name:str, strength_categories:set(TriviaQuestionCategory), weakness_categories:set(TriviaQuestionCategory), cautiousness:int, hostility:int):
        self._name = name
        self._strength_categories = strength_categories
        self._weakness_categories = weakness_categories
        self._cautiousness = 0.5
        self._hostility = 0.5
        self._strength_category_multiplier = 2 # double chances
        self._weakness_category_multiplier = 0.5 # chances are halved

    @property
    def strength_categories(self):
        return self._strength_categories

    @property
    def weakness_categories(self):
        return self._weakness_categories

    @property
    def cautiousness(self):
        return self._cautiousness

    @property
    def hostility(self):
        return self._hostility

    @property
    def strength_category_multiplier(self):
        return self._strength_category_multiplier

    @property
    def weakness_category_multiplier(self):
        return self._weakness_category_multiplier
    

class BoardGameEnthusiast(NPCPersonality):
    def __init__(self):
        super().__init__("BoardGameEnthusiast", 
                        strength_categories={TriviaQuestionCategory.BOARD_GAMES, TriviaQuestionCategory.BOOKS, TriviaQuestionCategory.HISTORY, TriviaQuestionCategory.MYTHOLOGY},
                        weakness_categories={TriviaQuestionCategory.SPORTS, TriviaQuestionCategory.MUSIC},
                        cautiousness=1,
                        hostility=0.5)

class Techie(NPCPersonality):
    def __init__(self):
        super().__init__("Techie",
        strength_categories={TriviaQuestionCategory.COMPUTERS, TriviaQuestionCategory.GADGETS, TriviaQuestionCategory.VIDEO_GAMES},
        weakness_categories={TriviaQuestionCategory.SPORTS, TriviaQuestionCategory.CELEBRITIES},
        cautiousness=0.2,
        hostility=0.75
        )

class PersonalityType(enum.Enum):
    GENERIC = NPCPersonality
    BOARD_GAME_ENTHUSIAST =  BoardGameEnthusiast
    TECHIE = Techie
    
