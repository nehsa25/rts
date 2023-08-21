from constants import Constants
from unit import UnitTypes, Unit

class ElvenFactory(Unit):
    name = "Wood Elves"
    description = "Can impersonate humans, sabatage, can use magic, Strong late game"     
    main_color = Constants.Colors.ALICE_BLUE
    secondary_color = Constants.Colors.YELLOW 
    hover_color = Constants.Colors.ALICE_BLUE
    hover_text_color = Constants.Colors.AQUA
    font = "frenchscript"
    font_size = 36 + 16
    log_utils = None

    def __init__(self, log_utils):
        self.log_utils = log_utils
        self.log_utils.log.debug("Initializing Elf() class")

    class Scout( UnitTypes.RangedUnit):
        def __init__(self):
            self.log_utils.log.debug("Initializing Scout() class")

    class Archer(UnitTypes.RangedUnit):
        combat_range = UnitTypes.RangedUnit.combat_range + 1 
        def __init__(self):
            self.log_utils.log.debug("Initializing Archer() class")

    class Ranger(UnitTypes.RangedUnit):
        combat_range = UnitTypes.RangedUnit.combat_range + 1 
        speed = UnitTypes.RangedUnit.speed + 2
        def __init__(self):
            self.log_utils.log.debug("Initializing Ranger() class")

    class Lord(UnitTypes.Hero):
        combat_range = UnitTypes.RangedUnit.combat_range + 1 
        combat_damage_low = UnitTypes.RangedUnit.combat_damage_low + 1
        combat_damage_high = UnitTypes.RangedUnit.combat_damage_high + 1
        def __init__(self, log_utils, pgu, player, unit_type):
            self.log_utils.log.debug("Initializing Lord() class")

    hero = Lord

    units = []
    units.append(dict(Name="Scout", Type=Scout, Color=main_color))
    units.append(dict(Name="Archer", Type=Archer, Color=main_color))
    units.append(dict(Name="Ranger", Type=Ranger, Color=main_color))
    units.append(dict(Name="Lord", Type=Lord, Color=main_color))
