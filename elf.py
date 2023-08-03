from enum import Enum
from archer import Archer

class Elf:
    description = "Can impersonate humans, sabatage, can use magic, Strong late game"

    def __init__(self):
        pass

    class Units(Enum):
        ElvenArcher = 0
        ElvenScout = 1
        ElvenLord = 2
        
    class ElvenArcher(Archer):
        combat_range = Archer.combat_range + 1 
        def __init__(self):
            pass
