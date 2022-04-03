import enum

class PromptType(enum.IntEnum):
    TRIVIA_QUESTION = 1
    VOTE = 2
    BANK = 3
    NUMBER = 4
    STRING = 5
    CONTINUE = 6

class ContestantType(enum.IntEnum):
    PLAYER = 1
    NPC = 2

