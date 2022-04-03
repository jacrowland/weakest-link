from contestants.player import Player
from scenes.scene_base import SceneBase

from queue import Queue

class GameManager():
    contestants = set()
    scene_queue = Queue()
    current_scene:SceneBase = None
    player:Player = None
    max_contestants = 7
    min_contestants = 1
    