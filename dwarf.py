

from constants import Constants
from unit import Unit, UnitTypes

class Dwarf:
    description = "Underground bases and tunnels, Defense, Strong late game, turtle playstyle"
    main_color = Constants.Colors.POOP_BROWN
    secondary_color = Constants.Colors.COCOA   
    hover_color = Constants.Colors.COCOA 
    hover_text_color = Constants.Colors.POOP_BROWN
    font = "hightowertext"
    font_size = 36
    logutils = None

    def __init__(self, logutils):
        self.logutils = logutils
        self.logutils.log.debug("Initializing Dwarf() class")

    class Miner(Unit, UnitTypes.MeleeUnit):
        def __init__(self, logutils, pgu, player, unit_type):
            self.logutils.log.debug("Initializing Miner() class")
            super().__init__(logutils, pgu, player, unit_type)

    class CrossbowGuard(Unit, UnitTypes.RangedUnit):
        def __init__(self, logutils, pgu, player, unit_type):
            self.logutils.log.debug("Initializing CrossbowGuard() class")
            super().__init__(logutils, pgu, player, unit_type)

    class Warror(Unit, UnitTypes.MeleeUnit):
        def __init__(self, logutils, pgu, player, unit_type):
            self.logutils.log.debug("Initializing Warror() class")
            super().__init__(logutils, pgu, player, unit_type)

    class DwarvenLord(Unit, UnitTypes.Hero):
        def __init__(self, logutils, pgu, player, unit_type):
            self.logutils.log.debug("Initializing DwarvenLord() class")
            super().__init__(logutils, pgu, player, unit_type)

    class Servant(Unit, UnitTypes.MeleeUnit):
        def __init__(self, logutils, pgu, player, unit_type):
            self.logutils.log.debug("Initializing Servant() class")
            super().__init__(logutils, pgu, player, unit_type)

    hero_character = DwarvenLord

    units = []
    units.append(dict(Name="Miner", Type=CrossbowGuard, Color=main_color))
    units.append(dict(Name="Crossbow Guard", Type=CrossbowGuard, Color=main_color))
    units.append(dict(Name="Warror", Type=Warror, Color=main_color))
    units.append(dict(Name="Dwarven Lord", Type=DwarvenLord, Color=main_color))
    units.append(dict(Name="Servant", Type=Servant, Color=main_color))
    