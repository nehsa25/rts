from constants import Constants
import unit
import pygame

class Goblin(unit.Unit):
    description = "Create water tiles, Sail, Pillage from other players, Strong early game, Naval"
    main_color = Constants.Colors.CRIMSON
    secondary_color = Constants.Colors.BLACK
    hover_color = Constants.Colors.ALICE_BLUE 
    hover_text_color = Constants.Colors.CRIMSON    
    spawn_rect = None
    font = "copperplategothic"
    font_size = 36

    def __init__(self, spawn_x = Constants.SP_WIDTH):
        self.spawn_rect = pygame.Rect((spawn_x, 0, unit.Unit.UNIT_SIZE, unit.Unit.UNIT_SIZE))  

    class Sailor(unit.UnitTypes.MeleeUnit):
        def __init__(self):
            pass

    class Pillager(unit.UnitTypes.RangedUnit):
        combat_range = unit.UnitTypes.RangedUnit.combat_range - 1 
        combat_damage_high = unit.UnitTypes.RangedUnit.combat_damage_high + 1
        def __init__(self):
            pass

    class GoblinCaptain(unit.UnitTypes.MeleeUnit):
        combat_damage_low = unit.UnitTypes.MeleeUnit.combat_damage_low + 2
        combat_damage_high = unit.UnitTypes.MeleeUnit.combat_damage_high + 2
        def __init__(self):
            pass

    class King(unit.UnitTypes.Hero):
        combat_damage_low = unit.UnitTypes.MeleeUnit.combat_damage_low + 3
        combat_damage_high = unit.UnitTypes.MeleeUnit.combat_damage_high + 3
        speed = unit.UnitTypes.MeleeUnit.speed + 1
        def __init__(self):
            pass

    hero_character = King

    units = []
    units.append(dict(Name="Sailor", Type=Sailor, Color=main_color))
    units.append(dict(Name="Pillager", Type=Pillager, Color=main_color))
    units.append(dict(Name="Captain", Type=GoblinCaptain, Color=main_color))
    units.append(dict(Name="Goblin King", Type=King, Color=main_color))
