import pygame
from combattypes import CombatTypes
from environment import Environment

class Unit:
    combat_type = None
    combat_range = None
    combat_damage_low = None
    combat_damage_high = None
    attack_tiles = None
    move_tiles = None
    unit_size = 5
    spawn_rect = None
    
    def __init__(self, combat_type, combat_range, combat_damage_low, combat_damage_high, attack_tiles, move_tiles):
        self.combat_type = combat_type
        self.combat_range = combat_range
        self.combat_damage_low = combat_damage_low
        self.combat_damage_high = combat_damage_high
        self.attack_tiles = attack_tiles
        self.move_tiles = move_tiles

class Hero(Unit):
    combat_type = CombatTypes.melee
    attack_tiles = [Environment.levels.Ground, Environment.levels.Air]
    move_tiles = [Environment.levels.Ground]
    def __init__(self):
        pass

class MountedUnit(Unit):
    combat_type = CombatTypes.melee
    combat_range = 0
    combat_damage_low = 4
    combat_damage_high = 7
    speed = 3
    attack_tiles = [Environment.levels.Ground]
    move_tiles = [Environment.levels.Ground]
    def __init__(self):
        pass

class MeleeUnit(Unit):
    combat_type = CombatTypes.melee
    combat_range = 0
    combat_damage_low = 3
    combat_damage_high = 6
    speed = 2
    attack_tiles = [Environment.levels.Ground]
    move_tiles = [Environment.levels.Ground]
    def __init__(self):
        pass

class RangedUnit(Unit):
    combat_type = CombatTypes.ranged
    combat_range = 2 # 2 tiles
    combat_damage_low = 3
    combat_damage_high = 6
    speed = 1
    attack_tiles = [Environment.levels.Water, Environment.levels.Ground, Environment.levels.Air]
    move_tiles = [Environment.levels.Ground]
    def __init__(self):
        pass