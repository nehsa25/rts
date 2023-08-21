from constants import Constants
from unit import Unit, UnitTypes

class ArgunaFactory(Unit):
    name = "Arguna"
    description = "Big bulking guys maybe?"
    main_color = Constants.Colors.COCOA
    secondary_color = Constants.Colors.BURNT_ORANGE
    hover_color = Constants.Colors.BLACK 
    hover_text_color = Constants.Colors.BURNT_ORANGE
    #font = "vinerhanditc"
    font = "impact"
    font_size = 36
    log_utils = None

    def __init__(self, log_utils):
        self.log_utils = log_utils
        self.log_utils.log.debug("Initializing Arguna() class")

    class Argn(UnitTypes.MeleeUnit):
        def __init__(self):
            self.log_utils.log.debug("Initializing Argn() class")
    
    class Argnamont(UnitTypes.RangedUnit):
        def __init__(self):
            self.log_utils.log.debug("Initializing Argnamont() class")

    hero = Argnamont
    
    units = []
    units.append(dict(Name="Argn", Type=Argn, Color=main_color))
    units.append(dict(Name="Argnamont", Type=Argnamont, Color=main_color))
