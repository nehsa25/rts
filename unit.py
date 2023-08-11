import pygame

# our stuff
from constants import Constants
from combattypes import CombatTypes
from environment import Environment
from pygameutility import PygameUtilities

# how much damage, how fast, ect
class Stats:
    combat_type = None
    combat_range = None
    combat_damage_low = None
    combat_damage_high = None
    attack_tiles = None
    move_tiles = None   

    def __init__(self):
        pass

    # def __init__(self, combat_type, combat_range, combat_damage_low, combat_damage_high, attack_tiles, move_tiles):
    #     self.combat_type = combat_type
    #     self.combat_range = combat_range
    #     self.combat_damage_low = combat_damage_low
    #     self.combat_damage_high = combat_damage_high
    #     self.attack_tiles = attack_tiles
    #     self.move_tiles = move_tiles

# probably will help with base skill sets
class UnitTypes:
    class Hero(Stats):
        combat_type = CombatTypes.melee
        attack_tiles = [Environment.levels.Ground, Environment.levels.Air]
        move_tiles = [Environment.levels.Ground]
        speed = 2
        def __init__(self):
            pass

    class MountedUnit(Stats):
        combat_type = CombatTypes.melee
        combat_range = 0
        combat_damage_low = 4
        combat_damage_high = 7
        speed = 3
        attack_tiles = [Environment.levels.Ground]
        move_tiles = [Environment.levels.Ground]
        def __init__(self):
            pass

    class MeleeUnit(Stats):
        combat_type = CombatTypes.melee
        combat_range = 0
        combat_damage_low = 3
        combat_damage_high = 6
        speed = 2
        attack_tiles = [Environment.levels.Ground]
        move_tiles = [Environment.levels.Ground]
        def __init__(self):
            pass

    class RangedUnit(Stats):
        combat_type = CombatTypes.ranged
        combat_range = 2 # 2 tiles
        combat_damage_low = 3
        combat_damage_high = 6
        speed = 1
        attack_tiles = [Environment.levels.Water, Environment.levels.Ground, Environment.levels.Air]
        move_tiles = [Environment.levels.Ground]
        def __init__(self):
            pass

# the whole can of worms
class Unit:
    Name = None
    Type = None
    Rect_Settings = None
    Moving_Thread = None # so we can change direction

    def __init__(self):
        self.Rect_Settings = PygameUtilities.RectSettings()
        self.Rect_Settings.Rect = pygame.Rect((Constants.SPAWN_X, Constants.SPAWN_Y, Constants.UNIT_SIZE, Constants.UNIT_SIZE)) 


