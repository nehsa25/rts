from constants import Constants
from unit import Unit, UnitTypes

class GoblinFactory(Unit):
    name = "Goblins"
    description = "Create water tiles, Sail, Pillage from other players, Strong early game, Naval"
    main_color = Constants.Colors.CRIMSON
    secondary_color = Constants.Colors.BLACK
    hover_color = Constants.Colors.ALICE_BLUE 
    hover_text_color = Constants.Colors.CRIMSON    
    font = "copperplategothic"
    font_size = 36
    log_utils = None

    def __init__(self, log_utils):
        self.log_utils = log_utils
        self.log_utils.log.debug("Initializing Goblin() class")

    class Sailor(UnitTypes.MeleeUnit):
        def __init__(self):            
            self.log_utils.log.debug("Initializing Sailor() class")

    class Pillager(UnitTypes.RangedUnit):
        combat_range = UnitTypes.RangedUnit.combat_range - 1 
        combat_damage_high = UnitTypes.RangedUnit.combat_damage_high + 1
        def __init__(self):    
            self.log_utils.log.debug("Initializing Pillager() class")

    class GoblinCaptain(UnitTypes.MeleeUnit):
        combat_damage_low = UnitTypes.MeleeUnit.combat_damage_low + 2
        combat_damage_high = UnitTypes.MeleeUnit.combat_damage_high + 2
        def __init__(self):    
            self.log_utils.log.debug("Initializing GoblinCaptain() class")

    class King(UnitTypes.Hero):
        combat_damage_low = UnitTypes.MeleeUnit.combat_damage_low + 3
        combat_damage_high = UnitTypes.MeleeUnit.combat_damage_high + 3
        speed = UnitTypes.MeleeUnit.speed + 1
        def __init__(self):    
            self.log_utils.log.debug("Initializing King() class")

    hero = King

    units = []
    units.append(dict(Name="Sailor", Type=Sailor, Color=main_color))
    units.append(dict(Name="Pillager", Type=Pillager, Color=main_color))
    units.append(dict(Name="Captain", Type=GoblinCaptain, Color=main_color))
    units.append(dict(Name="Goblin King", Type=King, Color=main_color))
