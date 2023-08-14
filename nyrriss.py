from constants import Constants
import unit

class Nyrriss(unit.Unit):
    description = "Snakes/poison"
    main_color = Constants.Colors.PEA_GREEN
    secondary_color = Constants.Colors.MOCCASIN
    hover_color = Constants.Colors.FUCHSIA 
    hover_text_color = Constants.Colors.ALICE_BLUE
    font = "mvboli"
    font_size = 36
    logutils = None

    def __init__(self, logutils):
        self.logutils = logutils
        self.logutils.log.debug("Initializing Nyrriss() class")
        super().__init__(self.logutils)
        self.RectSettings.BgColor = self.main_color

    class Shaman(unit.UnitTypes.RangedUnit):
        def __init__(self):
            self.logutils.log.debug("Initializing Shaman() class")

    class GodKing(unit.UnitTypes.RangedUnit):
        def __init__(self):
            self.logutils.log.debug("Initializing GodKing() class")

    hero_character = GodKing
    
    units = []
    units.append(dict(Name="Shaman", Type=Shaman, Color=main_color))
    units.append(dict(Name="GodKing", Type=GodKing, Color=main_color))
