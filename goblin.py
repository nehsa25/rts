from enum import Enum
import pygame
import unit
from colors import Colors

class Goblin:
    description = "Create water tiles, Sail, Pillage from other players, Strong early game"
    main_unit_rect = pygame.Rect((0, 0, unit.Unit.unit_size, unit.Unit.unit_size))
    color = (193, 155, 30)

    class Sailor(unit.MeleeUnit):
        def __init__(self):
            pass

    class Pillager(unit.RangedUnit):        
        combat_range = unit.RangedUnit.combat_range - 1 
        combat_damage_high = unit.RangedUnit.combat_damage_high + 1
        def __init__(self):
            pass

    class GoblinCaptain(unit.MeleeUnit):
        combat_damage_low = unit.MeleeUnit.combat_damage_low + 2
        combat_damage_high = unit.MeleeUnit.combat_damage_high + 2
        def __init__(self):
            pass

    units = []
    units.append(dict(Name="Sailor", Type=Sailor, Color=Colors.CRIMSON))
    units.append(dict(Name="Pillager", Type=Pillager, Color=Colors.CRIMSON))
    units.append(dict(Name="GoblinCaptain", Type=GoblinCaptain, Color=Colors.CRIMSON))
