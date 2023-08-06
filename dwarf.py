

from enum import Enum
import pygame
import unit
from colors import Colors

class Dwarf(unit.Unit):
    description = "Underground bases and tunnels, Defense, Strong late game, turtle playstyle"
    main_color = Colors.POOP_BROWN
    secondary_color = Colors.COCOA   
    hover_color = Colors.BLUE 

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

    hero_character = DwarvenLord

    units = []
    units.append(dict(Name="Miner", Type=CrossbowGuard, Color=main_color))
    units.append(dict(Name="Crossbow Guard", Type=CrossbowGuard, Color=main_color))
    units.append(dict(Name="Warror", Type=Warror, Color=main_color))
    units.append(dict(Name="Dwarven Lord", Type=DwarvenLord, Color=main_color))
    units.append(dict(Name="Servant", Type=Servant, Color=main_color))
    