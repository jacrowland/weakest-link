from abc import ABC, abstractmethod
from .contestant_enums import PromptType

class Contestant(ABC):
    def __init__(self, name:str, location:str, occupation:str):
        self._name = name
        self._location = location
        self._occupation = occupation
        self._eliminated = False

    def __str__(self):
        return f'Name: {self.name}\nLocation: {self._location}\nOccupation: {self._occupation}'

    @abstractmethod
    def get_response(self, prompt_type:PromptType, prompt, default_response=0)->str:
        pass

    @property
    def name(self):
        return self._name

    @property
    def location(self):
        return self._location
    
    @property
    def occupation(self):
        return self._occupation
    
    @property
    def eliminated(self):
        return self._eliminated

    @eliminated.setter
    def eliminated(self, status:bool):
        self._eliminated = status

