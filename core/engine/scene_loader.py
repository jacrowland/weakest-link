
from engine.game_manager import GameManager

def load_scene(scene):
    if GameManager.current_scene:
        GameManager.current_scene.on_scene_exit()
    GameManager.current_scene = scene
    GameManager.current_scene.on_scene_enter()