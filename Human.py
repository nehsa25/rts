from enum import Enum
import pygame
import unit

class Human:
    description = "Land units focused, jack of all trades, Mid-game"

    class Units(Enum):
        Farmer = 0        
        miner = 1
        Fisherman = 2
        Knight = 3
        archer = 4

    class Archer(unit.RangedUnit):
        rect = pygame.Rect((0, 0, unit.Unit.unit_size, unit.Unit.unit_size))
        color = (73, 155, 30)
        def __init__(self):
            pass