from enum import Enum
import unit

class Human:
    Discription = "Land units focused, jack of all trades, Mid-game"
        
    class Units(Enum):
        Farmer = 0        
        miner = 1
        Fisherman = 2
        Knight = 3
        archer = 4

    class Archer(unit.RangedUnit):
        def __init__(self):
            pass