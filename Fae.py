from constants import Constants
from unit import Unit, UnitTypes

class FaeFactory(Unit):
    name = "Fae"
    description = "Tricksters, Magic casters, Strong early to mid game"
    main_color = Constants.Colors.FUCHSIA
    secondary_color = Constants.Colors.HUNTER_GREEN 
    hover_color = Constants.Colors.MAROON
    hover_text_color = Constants.Colors.FUCHSIA
    font = "blackadderitc"
    font_size = 36 + 16
    log_utils = None

    def __init__(self, log_utils):
        self.log_utils = log_utils
        self.log_utils.log.debug("Initializing Fae() class")

    class Shapeshifter(UnitTypes.MeleeUnit):
        def __init__(self):
            self.log_utils.log.debug("Initializing Shapeshifter() class")

    class Littlefolk(UnitTypes.MeleeUnit):
        def __init__(self):
            self.log_utils.log.debug("Initializing Littlefolk() class")

    class HighFae(UnitTypes.Hero):
        def __init__(self):
            self.log_utils.log.debug("Initializing HighFae() class")

    class BlightedFae(UnitTypes.MeleeUnit):
        speed = UnitTypes.MountedUnit.speed + 1 # fast motherfuckers, they can run down horses
        def __init__(self):
            self.log_utils.log.debug("Initializing BlightedFae() class")

    hero = HighFae

    units = []
    units.append(dict(Name="Shapeshifter", Type=Shapeshifter, Color=main_color))
    units.append(dict(Name="Little Folk", Type=Littlefolk, Color=main_color))
    units.append(dict(Name="High Fae", Type=HighFae, Color=main_color))
    units.append(dict(Name="Blighted Fae", Type=BlightedFae, Color=main_color))
