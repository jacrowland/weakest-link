import enum

class Sounds(enum.Enum):
    STING = r"assets\sound\sfx\sting.mp3"
    MAIN_THEME = r"assets\sound\music\main_theme.mp3"
    SUDDEN_DEATH = r"assets\sound\music\sudden_death.mp3"
    WALK_OF_SHAME = r"assets\sound\music\walk_of_shame.mp3"
    QUESTION_BED = r"assets\sound\music\question_bed.mp3"
    CREDITS = r"assets\sound\music\credits.mp3"
    PENALITY_SHOOTOUT = r"assets\sound\music\penality_shootout.mp3"
    TYPING = r"assets\sound\sfx\typing.mp3"

class AudioType(enum.IntEnum):
    MUSIC_TRACK = 1
    SFX = 2
