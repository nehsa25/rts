from enum import Enum
import pygame
import unit
from colors import Colors

class Human(unit.Unit):
    description = "Land units focused, jack of all trades, Mid-game"
    main_color = Colors.YELLOW
    secondary_color = Colors.NAVY
    hover_color = Colors.ALICE_BLUE 

    class Farmer(unit.MeleeUnit):
        def __init__(self):
            pass

    class Miner(unit.MeleeUnit):
        def __init__(self):
            pass

    class Fisherman(unit.MeleeUnit):
        def __init__(self):
            pass

    class Knight(unit.MountedUnit):
        def __init__(self):
            pass

    class Commander(unit.Hero):
        def __init__(self):
            pass

    class Archer(unit.RangedUnit):
        def __init__(self):
            pass

    hero_character = Commander
    
    units = []
    units.append(dict(Name="Farmer", Type=Farmer, Color=main_color))
    units.append(dict(Name="Miner", Type=Miner, Color=main_color))
    units.append(dict(Name="Fisherman", Type=Fisherman, Color=main_color))
    units.append(dict(Name="Knight", Type=Knight, Color=main_color))
    units.append(dict(Name="Archer", Type=Archer, Color=main_color))
