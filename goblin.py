from constants import Constants
from unit import Unit, UnitTypes

class Goblin(Unit):
    description = "Create water tiles, Sail, Pillage from other players, Strong early game, Naval"
    main_color = Constants.Colors.CRIMSON
    secondary_color = Constants.Colors.BLACK
    hover_color = Constants.Colors.ALICE_BLUE 
    hover_text_color = Constants.Colors.CRIMSON    
    font = "copperplategothic"
    font_size = 36

    def __init__(self):
        super().__init__()
        self.rs.BgColor = self.main_color

    class Sailor(UnitTypes.MeleeUnit):
        def __init__(self):
            pass

    class Pillager(UnitTypes.RangedUnit):
        combat_range = UnitTypes.RangedUnit.combat_range - 1 
        combat_damage_high = UnitTypes.RangedUnit.combat_damage_high + 1
        def __init__(self):
            pass

    class GoblinCaptain(UnitTypes.MeleeUnit):
        combat_damage_low = UnitTypes.MeleeUnit.combat_damage_low + 2
        combat_damage_high = UnitTypes.MeleeUnit.combat_damage_high + 2
        def __init__(self):
            pass

    class King(UnitTypes.Hero):
        combat_damage_low = UnitTypes.MeleeUnit.combat_damage_low + 3
        combat_damage_high = UnitTypes.MeleeUnit.combat_damage_high + 3
        speed = UnitTypes.MeleeUnit.speed + 1
        def __init__(self):
            pass

    hero_character = King

    units = []
    units.append(dict(Name="Sailor", Type=Sailor, Color=main_color))
    units.append(dict(Name="Pillager", Type=Pillager, Color=main_color))
    units.append(dict(Name="Captain", Type=GoblinCaptain, Color=main_color))
    units.append(dict(Name="Goblin King", Type=King, Color=main_color))
