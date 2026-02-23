from enum import Enum

import pygame

from utils.utils import get_project_root


class SoundType(Enum):
    Food = 1
    Gold = 2
    Weapon = 3
    Enemy = 4
    Ghost = 5
    Mimic = 6
    Ogre = 7
    SnakeMage = 8
    Vampire = 9
    Zombie = 10
    Character = 11
    Door = 12
    Key = 13
    Potion = 14
    Scroll = 15
    Level = 16


class SoundUsage(Enum):
    add = 1
    use = 2
    hit = 3
    miss = 4
    engaged = 5
    closed = 6
    open = 7


class SoundController:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    @classmethod
    def get_instance(cls):
        return cls.__instance

    def __init__(self):
        pygame.init()
        self.sounds = {
            (SoundType.Food, SoundUsage.add): pygame.mixer.Sound(str(get_project_root() / "misc/sounds/add_food.ogg")),
            (SoundType.Food, SoundUsage.use): pygame.mixer.Sound(str(get_project_root() / "misc/sounds/use_food.ogg")),
            (SoundType.Gold, SoundUsage.add): pygame.mixer.Sound(str(get_project_root() / "misc/sounds/add_gold.ogg")),
            (SoundType.Weapon, SoundUsage.add): pygame.mixer.Sound(str(get_project_root() / "misc/sounds/add_weapon.ogg")),
            (SoundType.Weapon, SoundUsage.use): pygame.mixer.Sound(str(get_project_root() / "misc/sounds/use_weapon.ogg")),
            (SoundType.Enemy, SoundUsage.miss): pygame.mixer.Sound(str(get_project_root() / "misc/sounds/miss_sound.ogg")),
            (SoundType.Enemy, SoundUsage.engaged): pygame.mixer.Sound(
                str(get_project_root() / "misc/sounds/enemy_engaged.ogg")
            ),
            (SoundType.Ghost, SoundUsage.hit): pygame.mixer.Sound(str(get_project_root() / "misc/sounds/hit_ghost.ogg")),
            (SoundType.Mimic, SoundUsage.hit): pygame.mixer.Sound(str(get_project_root() / "misc/sounds/hit_ogre.ogg")),
            (SoundType.Ogre, SoundUsage.hit): pygame.mixer.Sound(str(get_project_root() / "misc/sounds/hit_ogre.ogg")),
            (SoundType.SnakeMage, SoundUsage.hit): pygame.mixer.Sound(
                str(get_project_root() / "misc/sounds/hit_snake_mage.ogg")
            ),
            (SoundType.Vampire, SoundUsage.hit): pygame.mixer.Sound(str(get_project_root() / "misc/sounds/hit_vampire.ogg")),
            (SoundType.Zombie, SoundUsage.hit): pygame.mixer.Sound(str(get_project_root() / "misc/sounds/hit_zombie.ogg")),
            (SoundType.Character, SoundUsage.hit): pygame.mixer.Sound(
                str(get_project_root() / "misc/sounds/hit_character.ogg")
            ),
            (SoundType.Character, SoundUsage.miss): pygame.mixer.Sound(
                str(get_project_root() / "misc/sounds/miss_sound.ogg")
            ),
            (SoundType.Door, SoundUsage.closed): pygame.mixer.Sound(str(get_project_root() / "misc/sounds/door_closed.ogg")),
            (SoundType.Door, SoundUsage.open): pygame.mixer.Sound(str(get_project_root() / "misc/sounds/door_open.ogg")),
            (SoundType.Key, SoundUsage.add): pygame.mixer.Sound(str(get_project_root() / "misc/sounds/key_add.ogg")),
            (SoundType.Potion, SoundUsage.add): pygame.mixer.Sound(str(get_project_root() / "misc/sounds/potion_add.ogg")),
            (SoundType.Potion, SoundUsage.use): pygame.mixer.Sound(str(get_project_root() / "misc/sounds/potion_use.ogg")),
            (SoundType.Scroll, SoundUsage.add): pygame.mixer.Sound(str(get_project_root() / "misc/sounds/scroll_add.ogg")),
            (SoundType.Scroll, SoundUsage.use): pygame.mixer.Sound(str(get_project_root() / "misc/sounds/scroll_use.ogg")),
            (SoundType.Level, SoundUsage.open): pygame.mixer.Sound(str(get_project_root() / "misc/sounds/next_level.ogg")),
            (SoundType.Character, SoundUsage.add): pygame.mixer.Sound(str(get_project_root() / "misc/sounds/level_up.ogg")),
        }
        pygame.mixer.music.load(str(get_project_root() / "misc/sounds/background.ogg"))
        self.intro = pygame.mixer.Sound(str(get_project_root() / "misc/sounds/intro_2.ogg"))
        self.game_over = pygame.mixer.Sound(str(get_project_root() / "misc/sounds/gameover.ogg"))
        self.win = pygame.mixer.Sound(str(get_project_root() / "misc/sounds/win.ogg"))

        self.mute(1)

    @staticmethod
    def play_background() -> None:
        pygame.mixer.music.play(loops=-1)

    @staticmethod
    def stop_background() -> None:
        pygame.mixer.music.stop()

    def get_sound(self, object_type, usage):
        return self.sounds.get((object_type, usage))

    def mute(self, volume):
        pygame.mixer.music.set_volume(volume * 0.4)
        for sound in self.sounds.values():
            sound.set_volume(volume * 0.7)
        self.game_over.set_volume(volume * 0.7)
        self.win.set_volume(volume * 0.7)
        self.intro.set_volume(volume * 0.7)
