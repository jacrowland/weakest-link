from os import system, name
from time import sleep

def clear_screen():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def print_with_delay(text:str, delay=0.05, end="\n"):
    """
    if ":" in text:
        new_thread = multiprocessing.Process(target=say, args=((text.split(":")[1]),), daemon=True)
        new_thread.start()
    """
    for char in text:
        print(char, end="")
        sleep(delay)
    print(end=end)

