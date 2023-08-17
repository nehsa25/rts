

from constants import Constants
import unit

class Dwarf(unit.Unit):
    description = "Underground bases and tunnels, Defense, Strong late game, turtle playstyle"
    main_color = Constants.Colors.POOP_BROWN
    secondary_color = Constants.Colors.COCOA   
    hover_color = Constants.Colors.BLUE 
    hover_text_color = Constants.Colors.ALICE_BLUE

    class Miner(unit.UnitTypes.MeleeUnit):
        def __init__(self):
            pass

    class CrossbowGuard(unit.UnitTypes.RangedUnit):
        def __init__(self):
            pass

    class Warror(unit.UnitTypes.MeleeUnit):
        def __init__(self):
            pass

    class DwarvenLord(unit.UnitTypes.Hero):
        def __init__(self):
            pass

    class Servant(unit.UnitTypes.MeleeUnit):
        def __init__(self):
            pass

    hero_character = DwarvenLord

    units = []
    units.append(dict(Name="Miner", Type=CrossbowGuard, Color=main_color))
    units.append(dict(Name="Crossbow Guard", Type=CrossbowGuard, Color=main_color))
    units.append(dict(Name="Warror", Type=Warror, Color=main_color))
    units.append(dict(Name="Dwarven Lord", Type=DwarvenLord, Color=main_color))
    units.append(dict(Name="Servant", Type=Servant, Color=main_color))
    