from os import system, name
from time import sleep
from contestants.contestant_base import Contestant

from engine.sound.sound_manager import SoundManager
from engine.sound.sound_enums import Sounds, AudioType
from engine.game_manager import GameManager

def clear_screen():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def print_with_delay(text:str, delay=0.05, end="\n"):
    for char in text:
        print(char, end="")
        sleep(delay)
    print(end=end)

def get_contestant_from_name(name:str, contestants:list)->Contestant:
    lst = [c for c in contestants if c.name.lower() == name.lower()]
    if len(lst) > 0:
        return lst[0]
    else:
        return None

def format_time(seconds_remaining:float)->str:
    minutes_remaining = int(seconds_remaining// 60)
    remainder_seconds = int(seconds_remaining - (minutes_remaining * 60))
    if len(str(remainder_seconds)) == 1:
        remainder_seconds = f'0{remainder_seconds}'
    return f"{minutes_remaining}:{remainder_seconds} remaining..."

def get_remaining_contestants(contestants):
    return list(filter(lambda c: not c.eliminated, list(GameManager.contestants)))