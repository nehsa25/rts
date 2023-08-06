# our stuff

from constants import Constants
from combattypes import CombatTypes
from environment import Environment

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
    def __init__(self):
        pass

    class Hero:
        combat_type = CombatTypes.melee
        attack_tiles = [Environment.levels.Ground, Environment.levels.Air]
        move_tiles = [Environment.levels.Ground]
        def __init__(self):
            pass

    class MountedUnit:
        combat_type = CombatTypes.melee
        combat_range = 0
        combat_damage_low = 4
        combat_damage_high = 7
        speed = 3
        attack_tiles = [Environment.levels.Ground]
        move_tiles = [Environment.levels.Ground]
        def __init__(self):
            pass

    class MeleeUnit:
        combat_type = CombatTypes.melee
        combat_range = 0
        combat_damage_low = 3
        combat_damage_high = 6
        speed = 2
        attack_tiles = [Environment.levels.Ground]
        move_tiles = [Environment.levels.Ground]
        def __init__(self):
            pass

    class RangedUnit:
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
    UNIT_SIZE = 15
    UNIT_BORDER_SIZE = 5
    Name = None
    Type = UnitTypes()
    Rect = None
    Stats = Stats()
    Spawn_POS = (Constants.SP_WIDTH, Constants.BORDER_SIZE)
    Rect_Settings = None

