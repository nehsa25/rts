from enum import Enum

from archer import Archer

class Goblin:
    description = "Create water tiles, Sail, Pillage from other players, Strong early game"
        
    class Units(Enum):
       Sailor = 0
       Pillager = 1
       GoblinCapt = 2

    class Pillager(Archer):
        combat_range = Archer.combat_range - 1 
        combat_damage_high = Archer.combat_damage_high + 1

        def __init__(self):
            pass