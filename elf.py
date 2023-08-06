from enum import Enum
import pygame
import unit
from colors import Colors

class Elf(unit.Unit):
    description = "Can impersonate humans, sabatage, can use magic, Strong late game"     
    main_color = Colors.ALICE_BLUE
    secondary_color = Colors.YELLOW 
    hover_color = Colors.CRIMSON

    class Scout(unit.RangedUnit):
        def __init__(self):
            pass

    class Archer(unit.RangedUnit):
        combat_range = unit.RangedUnit.combat_range + 1 
        def __init__(self):
            pass

    class Ranger(unit.RangedUnit):
        combat_range = unit.RangedUnit.combat_range + 1 
        speed = unit.RangedUnit.speed + 2
        def __init__(self):
            pass

    class Lord(unit.Hero):
        combat_range = unit.RangedUnit.combat_range + 1 
        combat_damage_low = unit.RangedUnit.combat_damage_low + 1
        combat_damage_high = unit.RangedUnit.combat_damage_high + 1
        def __init__(self):
            pass

    hero_character = Lord

    units = []
    units.append(dict(Name="Scout", Type=Scout, Color=main_color))
    units.append(dict(Name="Archer", Type=Archer, Color=main_color))
    units.append(dict(Name="Ranger", Type=Ranger, Color=main_color))
    units.append(dict(Name="Lord", Type=Lord, Color=main_color))
