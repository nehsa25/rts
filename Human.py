from constants import Constants
from unit import Unit, UnitTypes

class HumanFactory(Unit):
    name = "Humans"
    description = "Land units focused, jack of all trades, Mid-game"
    main_color = Constants.Colors.YELLOW
    secondary_color = Constants.Colors.NAVY
    hover_color = Constants.Colors.NAVY 
    hover_text_color = Constants.Colors.YELLOW
    font = "baskervilleoldface"
    font_size = 36
    log_utils = None

    def __init__(self, log_utils):
        self.log_utils = log_utils
        self.log_utils.log.debug("Initializing Human() class")

    class Farmer(UnitTypes.MeleeUnit):
        def __init__(self):
            self.log_utils.log.debug("Initializing Farmer() class")

    class Miner(UnitTypes.MeleeUnit):
        def __init__(self):
            self.log_utils.log.debug("Initializing Miner() class")

    class Fisherman(UnitTypes.MeleeUnit):
        def __init__(self):
            self.log_utils.log.debug("Initializing Fisherman() class")

    class Knight(UnitTypes.MountedUnit):
        def __init__(self):
            self.log_utils.log.debug("Initializing Knight() class")

    class Commander(UnitTypes.Hero):
        def __init__(self):
            self.log_utils.log.debug("Initializing Commander() class")

    class Archer(UnitTypes.RangedUnit):
        def __init__(self):
            self.log_utils.log.debug("Initializing Archer() class")

    hero = Commander
    
    units = []
    units.append(dict(Name="Farmer", Type=Farmer, Color=main_color))
    units.append(dict(Name="Miner", Type=Miner, Color=main_color))
    units.append(dict(Name="Fisherman", Type=Fisherman, Color=main_color))
    units.append(dict(Name="Knight", Type=Knight, Color=main_color))
    units.append(dict(Name="Archer", Type=Archer, Color=main_color))
