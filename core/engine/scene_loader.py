from scenes.scene_base import SceneTypes


from scenes.introduction import IntroductionScene
from scenes.main_menu import MainMenuScene
from scenes.session_setup import SessionSetupScene
from engine.game_manager import GameManager

class SceneLoader():
    @classmethod
    def load_scene(self, scene_type:SceneTypes):
        
        if scene_type is SceneTypes.INTRODUCTION:
            new_scene = IntroductionScene()
        elif scene_type is SceneTypes.SETUP:
            new_scene = SessionSetupScene()    
        elif scene_type is SceneTypes.MAIN_MENU:
            new_scene = MainMenuScene()

        if GameManager.current_scene:
            GameManager.current_scene.on_scene_exit()

        GameManager.current_scene = new_scene
        GameManager.current_scene.on_scene_enter()

    