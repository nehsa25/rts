from enum import Enum
import pygame
import unit
from colors import Colors

class Fae(unit.Unit):
    Discription = "Tricksters, Magic casters, Strong early to mid game"
    main_color = Colors.FUCHSIA
    secondary_color = Colors.HUNTER_GREEN 
    hover_color = Colors.AQUA

    class Shapeshifter(unit.MeleeUnit):
        def __init__(self):
            pass

    class Littlefolk(unit.MeleeUnit):
        def __init__(self):
            pass

    class HighFae(unit.Hero):
        def __init__(self):
            pass

    class BlightedFae(unit.MeleeUnit):
        speed = unit.MountedUnit.speed # fast motherfuckers
        def __init__(self):
            pass

    hero_character = HighFae

    units = []
    units.append(dict(Name="Shapeshifter", Type=Shapeshifter, Color=main_color))
    units.append(dict(Name="Little Folk", Type=Littlefolk, Color=main_color))
    units.append(dict(Name="High Fae", Type=HighFae, Color=main_color))
    units.append(dict(Name="Blighted Fae", Type=BlightedFae, Color=main_color))
