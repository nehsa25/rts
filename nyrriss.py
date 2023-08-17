from constants import Constants
from unit import Unit, UnitTypes

class Nyrriss(Unit):
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

    class Shaman(Unit, UnitTypes.RangedUnit):
        def __init__(self, logutils, pgu, player, unit_type):
            self.logutils.log.debug("Initializing Shaman() class")
            super().__init__(logutils, pgu, player, unit_type)

    class GodKing(Unit, UnitTypes.RangedUnit):
        def __init__(self, logutils, pgu, player, unit_type):
            self.logutils.log.debug("Initializing GodKing() class")
            super().__init__(logutils, pgu, player, unit_type)

    hero_character = GodKing
    
    units = []
    units.append(dict(Name="Shaman", Type=Shaman, Color=main_color))
    units.append(dict(Name="GodKing", Type=GodKing, Color=main_color))
