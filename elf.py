from enum import Enum
import unit

class Elf:
    description = "Can impersonate humans, sabatage, can use magic, Strong late game"

    def __init__(self):
        pass

    class Units(Enum):
        Archer = 0
        Scout = 1
        Lord = 2
        
    class Scout(unit.RangedUnit):
        def __init__(self):
            pass

    class Archer(unit.RangedUnit):
        combat_range = unit.RangedUnit.combat_range + 1 
        def __init__(self):
            pass

    class Lord(unit.RangedUnit):
        combat_range = unit.RangedUnit.combat_range + 1 
        combat_damage_low = unit.RangedUnit.combat_damage_low + 1
        combat_damage_high = unit.RangedUnit.combat_damage_high + 1
        def __init__(self):
            pass
