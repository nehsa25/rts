

from enum import Enum
import pygame
import unit
from colors import Colors

class Dwarf:
    description = "Underground bases and tunnels, Defense, Strong late game, turtle playstyle"
    main_unit_rect = pygame.Rect((0, 0, unit.Unit.unit_size, unit.Unit.unit_size))  
    color = Colors.DWARF

    class Units(Enum):
        Miner = 0
        Warror = 1 
        DwarvenLord = 2

    class Miner(unit.MeleeUnit):
        def __init__(self):
            pass

    class CrossbowGuard(unit.RangedUnit):
        def __init__(self):
            pass

    class Warror(unit.MeleeUnit):
        def __init__(self):
            pass

    class DwarvenLord(unit.MeleeUnit):
        def __init__(self):
            pass

    class Servant(unit.MeleeUnit):
        def __init__(self):
            pass

    units = []
    units.append(dict(Name="Miner", Type=CrossbowGuard, Color=Colors.BLACK))
    units.append(dict(Name="Crossbow Guard", Type=CrossbowGuard, Color=Colors.BLACK))
    units.append(dict(Name="Warror", Type=Warror, Color=Colors.BLACK))
    units.append(dict(Name="Dwarven Lord", Type=DwarvenLord, Color=Colors.BLACK))
    units.append(dict(Name="Servant", Type=Servant, Color=Colors.BLACK))
    