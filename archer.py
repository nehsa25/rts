from combattypes import CombatTypes
from environment import Environment
from unit import Unit

class Archer(Unit):
    combat_type = CombatTypes.ranged
    combat_range = 2 # 2 tiles
    combat_damage_low = 3
    combat_damage_high = 6
    attack_tiles = [Environment.levels.Subterranean, Environment.levels.Water, Environment.levels.Ground, Environment.levels.Air]
    move_tiles = [Environment.levels.Ground]

    def __init__(self):
        pass
