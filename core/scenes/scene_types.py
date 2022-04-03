import enum

class SceneTypes(enum.IntEnum):
    INTRODUCTION = 1
    SETUP = 2
    REGULAR_ROUND = 3
    FINAL_ROUND = 4
    SUDDEN_DEATH = 5
    ROUND_VOTING = 6
    WINNER_REVEAL = 7
    CONCLUSION = 8
    MAIN_MENU = 9