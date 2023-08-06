

from enum import Enum
import pygame
import unit
from colors import Colors

class Dwarf:
    description = "Underground bases and tunnels, Defense, Strong late game, turtle playstyle"
    main_unit_rect = pygame.Rect((0, 0, unit.Unit.unit_size, unit.Unit.unit_size))  
    main_color = Colors.POOP_BROWN
    secondary_color = Colors.COCOA    

    class Miner(unit.MeleeUnit):
        def __init__(self):
            pass

    class CrossbowGuard(unit.RangedUnit):
        def __init__(self):
            pass

    class Warror(unit.MeleeUnit):
        def __init__(self):
            pass

    class DwarvenLord(unit.Hero):
        def __init__(self):
            pass

    class Servant(unit.MeleeUnit):
        def __init__(self):
            pass

    units = []
    units.append(dict(Name="Miner", Type=CrossbowGuard, Color=main_color))
    units.append(dict(Name="Crossbow Guard", Type=CrossbowGuard, Color=main_color))
    units.append(dict(Name="Warror", Type=Warror, Color=main_color))
    units.append(dict(Name="Dwarven Lord", Type=DwarvenLord, Color=main_color))
    units.append(dict(Name="Servant", Type=Servant, Color=main_color))
    