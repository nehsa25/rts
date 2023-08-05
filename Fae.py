from enum import Enum
import pygame
import unit
from colors import Colors

class Fae:
    Discription = "Tricksters, Magic casters, Strong early to mid game"
    main_unit_rect = pygame.Rect((0, 0, unit.Unit.unit_size, unit.Unit.unit_size))  
    color = Colors.FAE

    class Shapeshifter(unit.MeleeUnit):
        def __init__(self):
            pass

    class Littlefolk(unit.MeleeUnit):
        def __init__(self):
            pass

    class HighFae(unit.MeleeUnit):
        def __init__(self):
            pass

    class BlightedFae(unit.MeleeUnit):
        speed = unit.MountedUnit.speed # fast motherfuckers
        def __init__(self):
            pass

    units = []
    units.append(dict(Name="Shapeshifter", Type=Shapeshifter, Color=Colors.SCARLET))
    units.append(dict(Name="Little Folk", Type=Littlefolk, Color=Colors.SCARLET))
    units.append(dict(Name="High Fae", Type=HighFae, Color=Colors.SCARLET))
    units.append(dict(Name="Blighted Fae", Type=BlightedFae, Color=Colors.SCARLET))
