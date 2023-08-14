from constants import Constants
import unit

class Fae(unit.Unit):
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
        super().__init__(self.logutils)
        self.RectSettings.BgColor = self.main_color

    class Shapeshifter(unit.UnitTypes.MeleeUnit):
        def __init__(self):
            self.logutils.log.debug("Initializing Shapeshifter() class")

    class Littlefolk(unit.UnitTypes.MeleeUnit):
        def __init__(self):
            self.logutils.log.debug("Initializing Littlefolk() class")

    class HighFae(unit.UnitTypes.Hero):
        def __init__(self):
            self.logutils.log.debug("Initializing HighFae() class")

    class BlightedFae(unit.UnitTypes.MeleeUnit):
        speed = unit.UnitTypes.MountedUnit.speed + 1 # fast motherfuckers, they can run down horses
        def __init__(self):
            self.logutils.log.debug("Initializing BlightedFae() class")

    hero_character = HighFae

    units = []
    units.append(dict(Name="Shapeshifter", Type=Shapeshifter, Color=main_color))
    units.append(dict(Name="Little Folk", Type=Littlefolk, Color=main_color))
    units.append(dict(Name="High Fae", Type=HighFae, Color=main_color))
    units.append(dict(Name="Blighted Fae", Type=BlightedFae, Color=main_color))
