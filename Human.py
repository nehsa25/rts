from constants import Constants
import unit

class Human(unit.Unit):
    description = "Land units focused, jack of all trades, Mid-game"
    main_color = Constants.Colors.YELLOW
    secondary_color = Constants.Colors.NAVY
    hover_color = Constants.Colors.NAVY 
    hover_text_color = Constants.Colors.YELLOW
    font = "baskervilleoldface"
    font_size = 36

    class Farmer(unit.UnitTypes.MeleeUnit):
        def __init__(self):
            pass

    class Miner(unit.UnitTypes.MeleeUnit):
        def __init__(self):
            pass

    class Fisherman(unit.UnitTypes.MeleeUnit):
        def __init__(self):
            pass

    class Knight(unit.UnitTypes.MountedUnit):
        def __init__(self):
            pass

    class Commander(unit.UnitTypes.Hero):
        def __init__(self):
            pass

    class Archer(unit.UnitTypes.RangedUnit):
        def __init__(self):
            pass

    hero_character = Commander
    
    units = []
    units.append(dict(Name="Farmer", Type=Farmer, Color=main_color))
    units.append(dict(Name="Miner", Type=Miner, Color=main_color))
    units.append(dict(Name="Fisherman", Type=Fisherman, Color=main_color))
    units.append(dict(Name="Knight", Type=Knight, Color=main_color))
    units.append(dict(Name="Archer", Type=Archer, Color=main_color))
