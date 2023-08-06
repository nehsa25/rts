import pygame
import unit
from colors import Colors
from constants import Constants

class Goblin(unit.Unit):
    description = "Create water tiles, Sail, Pillage from other players, Strong early game"
    main_color = Colors.CRIMSON
    secondary_color = Colors.BLACK
    hover_color = Colors.HUNTER_GREEN 
    spawn_rect = None

    def __init__(self, spawn_x = Constants.SIDE_PANEL_WIDTH):
        self.spawn_rect = pygame.Rect((spawn_x, 0, unit.Unit.unit_size, unit.Unit.unit_size))  

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

    class King(unit.Hero):
        combat_damage_low = unit.MeleeUnit.combat_damage_low + 3
        combat_damage_high = unit.MeleeUnit.combat_damage_high + 3
        speed = unit.MeleeUnit.speed + 1
        def __init__(self):
            pass

    hero_character = King

    units = []
    units.append(dict(Name="Sailor", Type=Sailor, Color=main_color))
    units.append(dict(Name="Pillager", Type=Pillager, Color=main_color))
    units.append(dict(Name="Captain", Type=GoblinCaptain, Color=main_color))
    units.append(dict(Name="Goblin King", Type=King, Color=main_color))
