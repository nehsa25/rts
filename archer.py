from combattypes import CombatTypes
from unit import Unit

class Archer(Unit):
    combat_type = CombatTypes.ranged
    combat_range = 2 # 2 tiles
    combat_damage_low = 3
    combat_damage_high = 6

    def __init__(self):
        pass
