from constants import Constants
from unit import Unit, UnitTypes

class Arguna(Unit):
    description = "Big bulking guys maybe?"
    main_color = Constants.Colors.COCOA
    secondary_color = Constants.Colors.BURNT_ORANGE
    hover_color = Constants.Colors.BLACK 
    hover_text_color = Constants.Colors.BURNT_ORANGE
    #font = "vinerhanditc"
    font = "impact"
    font_size = 36
    logutils = None

    def __init__(self, logutils):
        self.logutils = logutils
        self.logutils.log.debug("Initializing Arguna() class")

    class Argn(Unit, UnitTypes.MeleeUnit):
        def __init__(self, logutils, pgu, player, unit_type):
            self.log_utils.log.debug("Initializing Argn() class")
            super().__init__(logutils, pgu, player, unit_type)

    class Argnamont(Unit, UnitTypes.RangedUnit):
        def __init__(self, logutils, pgu, player, unit_type):
            self.log_utils.log.debug("Initializing Argnamont() class")
            super().__init__(logutils, pgu, player, unit_type)

    hero_character = Argnamont
    
    units = []
    units.append(dict(Name="Argn", Type=Argn, Color=main_color))
    units.append(dict(Name="Argnamont", Type=Argnamont, Color=main_color))
