from engine.game_manager import GameManager
from engine.scene_loader import SceneLoader
from scenes.scene_base import SceneTypes

if __name__ == "__main__":
    GameManager.scene_queue.put(SceneTypes.INTRODUCTION)
    while not GameManager.scene_queue.empty():
        current_scene_type = GameManager.scene_queue.get()
        SceneLoader.load_scene(current_scene_type)
    input()
