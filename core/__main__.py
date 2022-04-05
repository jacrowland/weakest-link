from scenes.rounds.regular_round import RegularRoundScene
from engine.game_manager import GameManager
from engine.scene_loader import load_scene
from scenes.main_menu import MainMenuScene

if __name__ == "__main__":
    GameManager.scene_queue.put(MainMenuScene())
    while not GameManager.scene_queue.empty():
        current_scene = GameManager.scene_queue.get()
        load_scene(current_scene)
    input()