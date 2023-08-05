from enum import Enum
import pygame
import unit
from colors import Colors

class Elf:
    description = "Can impersonate humans, sabatage, can use magic, Strong late game"     
    main_unit_rect = pygame.Rect((0, 0, unit.Unit.unit_size, unit.Unit.unit_size))   
    color = Colors.ELF 

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

    class Lord(unit.MountedUnit):
        combat_range = unit.RangedUnit.combat_range + 1 
        combat_damage_low = unit.RangedUnit.combat_damage_low + 1
        combat_damage_high = unit.RangedUnit.combat_damage_high + 1
        def __init__(self):
            pass

    units = []
    units.append(dict(Name="Scout", Type=Scout, Color=Colors.ALICE_BLUE))
    units.append(dict(Name="Archer", Type=Archer, Color=Colors.PLUM))
    units.append(dict(Name="Ranger", Type=Ranger, Color=Colors.SCARLET))
    units.append(dict(Name="Lord", Type=Lord, Color=Colors.NAVY))
