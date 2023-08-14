from constants import Constants
import unit

class Elf(unit.Unit):
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
        super().__init__(self.logutils)
        self.RectSettings.BgColor = self.main_color

    class Scout(unit.UnitTypes.RangedUnit):
        def __init__(self):
            self.logutils.log.debug("Initializing Scout() class")

    class Archer(unit.UnitTypes.RangedUnit):
        combat_range = unit.UnitTypes.RangedUnit.combat_range + 1 
        def __init__(self):
            self.logutils.log.debug("Initializing Archer() class")

    class Ranger(unit.UnitTypes.RangedUnit):
        combat_range = unit.UnitTypes.RangedUnit.combat_range + 1 
        speed = unit.UnitTypes.RangedUnit.speed + 2
        def __init__(self):
            self.logutils.log.debug("Initializing Ranger() class")

    class Lord(unit.UnitTypes.Hero):
        combat_range = unit.UnitTypes.RangedUnit.combat_range + 1 
        combat_damage_low = unit.UnitTypes.RangedUnit.combat_damage_low + 1
        combat_damage_high = unit.UnitTypes.RangedUnit.combat_damage_high + 1
        def __init__(self):
            self.logutils.log.debug("Initializing Lord() class")

    hero_character = Lord

    units = []
    units.append(dict(Name="Scout", Type=Scout, Color=main_color))
    units.append(dict(Name="Archer", Type=Archer, Color=main_color))
    units.append(dict(Name="Ranger", Type=Ranger, Color=main_color))
    units.append(dict(Name="Lord", Type=Lord, Color=main_color))
