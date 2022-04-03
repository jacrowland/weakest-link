from abc import ABC, abstractmethod
from .scene_types import SceneTypes

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


