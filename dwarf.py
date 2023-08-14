

from constants import Constants
import unit

class Dwarf(unit.Unit):
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
        super().__init__(self.logutils)
        self.RectSettings.BgColor = self.main_color

    class Miner(unit.UnitTypes.MeleeUnit):
        def __init__(self):
            self.logutils.log.debug("Initializing Miner() class")

    class CrossbowGuard(unit.UnitTypes.RangedUnit):
        def __init__(self):
            self.logutils.log.debug("Initializing CrossbowGuard() class")

    class Warror(unit.UnitTypes.MeleeUnit):
        def __init__(self):
            self.logutils.log.debug("Initializing Warror() class")

    class DwarvenLord(unit.UnitTypes.Hero):
        def __init__(self):
            self.logutils.log.debug("Initializing DwarvenLord() class")

    class Servant(unit.UnitTypes.MeleeUnit):
        def __init__(self):
            self.logutils.log.debug("Initializing Servant() class")

    hero_character = DwarvenLord

    units = []
    units.append(dict(Name="Miner", Type=CrossbowGuard, Color=main_color))
    units.append(dict(Name="Crossbow Guard", Type=CrossbowGuard, Color=main_color))
    units.append(dict(Name="Warror", Type=Warror, Color=main_color))
    units.append(dict(Name="Dwarven Lord", Type=DwarvenLord, Color=main_color))
    units.append(dict(Name="Servant", Type=Servant, Color=main_color))
    