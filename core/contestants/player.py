from .contestant_base import Contestant
from .contestant_enums import PromptType

class Player(Contestant):
    def __init__(self, name:str, location:str, occupation:str):
        super().__init__(name=name, location=location, occupation=occupation)
    
    @classmethod
    def get_response(self, prompt_type:PromptType=PromptType.CONTINUE, prompt=None, input_txt:str="> ", default_response=0) -> str:
        valid_response = False
        while not valid_response:
            response = input(input_txt).strip()
            if prompt_type is PromptType.NUMBER:
                if response.isnumeric():
                    valid_response = True
                else:
                    print("You must enter a number.")
            if prompt_type is PromptType.STRING or prompt_type is PromptType.TRIVIA_QUESTION:
                if response == '':
                    response = default_response
                valid_response = True
            elif prompt_type is PromptType.CONTINUE:
                valid_response = True
                response = default_response 
            elif prompt_type is PromptType.VOTE:
                raise NotImplemented("Player PromptType.VOTE not implemented")
            elif prompt_type is PromptType.BANK:
                valid_response = True
                # TODO : FIX THIS

        return response