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

    class Shapeshifter(unit.UnitTypes.MeleeUnit):
        def __init__(self):
            pass

    class Littlefolk(unit.UnitTypes.MeleeUnit):
        def __init__(self):
            pass

    class HighFae(unit.UnitTypes.Hero):
        def __init__(self):
            pass

    class BlightedFae(unit.UnitTypes.MeleeUnit):
        speed = unit.UnitTypes.MountedUnit.speed + 1 # fast motherfuckers, they can run down horses
        def __init__(self):
            pass

    hero_character = HighFae

    units = []
    units.append(dict(Name="Shapeshifter", Type=Shapeshifter, Color=main_color))
    units.append(dict(Name="Little Folk", Type=Littlefolk, Color=main_color))
    units.append(dict(Name="High Fae", Type=HighFae, Color=main_color))
    units.append(dict(Name="Blighted Fae", Type=BlightedFae, Color=main_color))
