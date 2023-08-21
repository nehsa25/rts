

from constants import Constants
from unit import Unit, UnitTypes

class DwarvenFactory(Unit):
    name = "Dwarves"
    description = "Underground bases and tunnels, Defense, Strong late game, turtle playstyle"
    main_color = Constants.Colors.POOP_BROWN
    secondary_color = Constants.Colors.COCOA   
    hover_color = Constants.Colors.COCOA 
    hover_text_color = Constants.Colors.POOP_BROWN
    font = "hightowertext"
    font_size = 36
    log_utils = None

    def __init__(self, log_utils):
        self.log_utils = log_utils
        self.log_utils.log.debug("Initializing Dwarf() class")

    class Miner(UnitTypes.MeleeUnit):
        def __init__(self):
            self.log_utils.log.debug("Initializing Miner() class")

    class CrossbowGuard(UnitTypes.RangedUnit):
        def __init__(self):
            self.log_utils.log.debug("Initializing CrossbowGuard() class")

    class Warror(UnitTypes.MeleeUnit):
        def __init__(self):
            self.log_utils.log.debug("Initializing Warror() class")

    class DwarvenLord(UnitTypes.Hero):
        def __init__(self):
            self.log_utils.log.debug("Initializing DwarvenLord() class")

    class Servant(UnitTypes.MeleeUnit):
        def __init__(self):
            self.log_utils.log.debug("Initializing Servant() class")

    hero = DwarvenLord

    units = []
    units.append(dict(Name="Miner", Type=CrossbowGuard, Color=main_color))
    units.append(dict(Name="Crossbow Guard", Type=CrossbowGuard, Color=main_color))
    units.append(dict(Name="Warror", Type=Warror, Color=main_color))
    units.append(dict(Name="Dwarven Lord", Type=DwarvenLord, Color=main_color))
    units.append(dict(Name="Servant", Type=Servant, Color=main_color))
    