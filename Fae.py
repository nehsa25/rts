from constants import Constants
from unit import Unit, UnitTypes

class Fae:
    Discription = "Tricksters, Magic casters, Strong early to mid game"
    main_color = Constants.Colors.FUCHSIA
    secondary_color = Constants.Colors.HUNTER_GREEN 
    hover_color = Constants.Colors.MAROON
    hover_text_color = Constants.Colors.FUCHSIA
    font = "blackadderitc"
    font_size = 36 + 16
    logutils = None

    def __init__(self, logutils):
        self.logutils = logutils
        self.logutils.log.debug("Initializing Fae() class")

    class Shapeshifter(Unit, UnitTypes.MeleeUnit):
        def __init__(self, logutils, pgu, player, unit_type):
            self.log_utils.log.debug("Initializing Shapeshifter() class")
            super().__init__(logutils, pgu, player, unit_type)

    class Littlefolk(Unit, UnitTypes.MeleeUnit):
        def __init__(self, logutils, pgu, player, unit_type):
            self.log_utils.log.debug("Initializing Littlefolk() class")
            super().__init__(logutils, pgu, player, unit_type)

    class HighFae(Unit, UnitTypes.Hero):
        def __init__(self, logutils, pgu, player, unit_type):
            self.log_utils.log.debug("Initializing HighFae() class")
            super().__init__(logutils, pgu, player, unit_type)

    class BlightedFae(Unit, UnitTypes.MeleeUnit):
        speed = UnitTypes.MountedUnit.speed + 1 # fast motherfuckers, they can run down horses
        def __init__(self, logutils, pgu, player, unit_type):
            self.log_utils.log.debug("Initializing BlightedFae() class")
            super().__init__(logutils, pgu, player, unit_type)

    hero_character = HighFae

    units = []
    units.append(dict(Name="Shapeshifter", Type=Shapeshifter, Color=main_color))
    units.append(dict(Name="Little Folk", Type=Littlefolk, Color=main_color))
    units.append(dict(Name="High Fae", Type=HighFae, Color=main_color))
    units.append(dict(Name="Blighted Fae", Type=BlightedFae, Color=main_color))
