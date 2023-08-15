from constants import Constants
from unit import UnitTypes, Unit

class Elf:
    description = "Can impersonate humans, sabatage, can use magic, Strong late game"     
    main_color = Constants.Colors.ALICE_BLUE
    secondary_color = Constants.Colors.YELLOW 
    hover_color = Constants.Colors.ALICE_BLUE
    hover_text_color = Constants.Colors.AQUA
    font = "frenchscript"
    font_size = 36 + 16
    logutils = None

    def __init__(self, logutils):
        self.logutils = logutils
        self.logutils.log.debug("Initializing Fae() class")

    class Scout(Unit, UnitTypes.RangedUnit):
        def __init__(self, logutils, pgu, player, unit_type):
            self.logutils.log.debug("Initializing Scout() class")
            super().__init__(logutils, pgu, player, unit_type)

    class Archer(Unit, UnitTypes.RangedUnit):
        combat_range = UnitTypes.RangedUnit.combat_range + 1 
        def __init__(self, logutils, pgu, player, unit_type):
            self.logutils.log.debug("Initializing Archer() class")
            super().__init__(logutils, pgu, player, unit_type)

    class Ranger(Unit, UnitTypes.RangedUnit):
        combat_range = UnitTypes.RangedUnit.combat_range + 1 
        speed = UnitTypes.RangedUnit.speed + 2
        def __init__(self, logutils, pgu, player, unit_type):
            self.logutils.log.debug("Initializing Ranger() class")
            super().__init__(logutils, pgu, player, unit_type)

    class Lord(Unit, UnitTypes.Hero):
        combat_range = UnitTypes.RangedUnit.combat_range + 1 
        combat_damage_low = UnitTypes.RangedUnit.combat_damage_low + 1
        combat_damage_high = UnitTypes.RangedUnit.combat_damage_high + 1
        def __init__(self, logutils, pgu, player, unit_type):
            self.logutils.log.debug("Initializing Lord() class")
            super().__init__(logutils, pgu, player, unit_type)

    hero_character = Lord

    units = []
    units.append(dict(Name="Scout", Type=Scout, Color=main_color))
    units.append(dict(Name="Archer", Type=Archer, Color=main_color))
    units.append(dict(Name="Ranger", Type=Ranger, Color=main_color))
    units.append(dict(Name="Lord", Type=Lord, Color=main_color))
