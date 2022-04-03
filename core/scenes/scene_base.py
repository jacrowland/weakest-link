from abc import ABC, abstractmethod

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

class SceneBase(ABC):
    def __init__(self, scene_type:SceneTypes):
        self._scene_type = scene_type

    @abstractmethod
    def on_scene_enter(self):
        pass

    @abstractmethod
    def play(self):
        """
        Main control loop for the scene
        """
        pass

    @abstractmethod
    def on_scene_exit(self):
        pass


