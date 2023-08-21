from constants import Constants
from unit import Unit, UnitTypes

class NyrrissFactory(Unit):
    name = "Nyrriss"
    description = "Snakes/poison"
    main_color = Constants.Colors.PEA_GREEN
    secondary_color = Constants.Colors.MOCCASIN
    hover_color = Constants.Colors.FUCHSIA 
    hover_text_color = Constants.Colors.PUTRID_GREEN
    font = "mvboli"
    font_size = 36
    log_utils = None
    
    def __init__(self, log_utils):
        self.log_utils = log_utils
        self.log_utils.log.debug("Initializing Nyrriss() class")

    class Shaman(UnitTypes.RangedUnit):
        def __init__(self):
            self.log_utils.log.debug("Initializing Shaman() class")

    class GodKing(UnitTypes.RangedUnit):
        def __init__(self):
            self.log_utils.log.debug("Initializing GodKing() class")

    hero = GodKing
    
    units = []
    units.append(dict(Name="Shaman", Type=Shaman, Color=main_color))
    units.append(dict(Name="GodKing", Type=GodKing, Color=main_color))
