from contestants.player import Player
from scenes.scene_base import SceneBase
from queue import Queue
from bank import Bank

class GameManager():
    contestants = set()
    rounds = set()
    player:Player = None
    scene_queue = Queue()
    current_scene:SceneBase = None
    max_contestants = 7
    min_contestants = 1
    bank = Bank()