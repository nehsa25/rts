from constants import Constants
from unit import Unit, UnitTypes

class Human:
    description = "Land units focused, jack of all trades, Mid-game"
    main_color = Constants.Colors.YELLOW
    secondary_color = Constants.Colors.NAVY
    hover_color = Constants.Colors.NAVY 
    hover_text_color = Constants.Colors.YELLOW
    font = "baskervilleoldface"
    font_size = 36
    logutils = None

    def __init__(self, logutils):
        self.logutils = logutils
        self.logutils.log.debug("Initializing Human() class")

    class Farmer(Unit, UnitTypes.MeleeUnit):
        def __init__(self, logutils, pgu, player, unit_type):
            self.log_utils.log.debug("Initializing Farmer() class")
            super().__init__(logutils, pgu, player, unit_type)

    class Miner(Unit, UnitTypes.MeleeUnit):
        def __init__(self, logutils, pgu, player, unit_type):
            self.log_utils.log.debug("Initializing Miner() class")
            super().__init__(logutils, pgu, player, unit_type)

    class Fisherman(Unit, UnitTypes.MeleeUnit):
        def __init__(self, logutils, pgu, player, unit_type):
            self.log_utils.log.debug("Initializing Fisherman() class")
            super().__init__(logutils, pgu, player, unit_type)

    class Knight(Unit, UnitTypes.MountedUnit):
        def __init__(self, logutils, pgu, player, unit_type):
            self.log_utils.log.debug("Initializing Knight() class")
            super().__init__(logutils, pgu, player, unit_type)

    class Commander(Unit, UnitTypes.Hero):
        def __init__(self, logutils, pgu, player, unit_type):
            self.log_utils.log.debug("Initializing Commander() class")
            super().__init__(logutils, pgu, player, unit_type)

    class Archer(Unit, UnitTypes.RangedUnit):
        def __init__(self, logutils, pgu, player, unit_type):
            self.log_utils.log.debug("Initializing Archer() class")
            super().__init__(logutils, pgu, player, unit_type)

    hero_character = Commander
    
    units = []
    units.append(dict(Name="Farmer", Type=Farmer, Color=main_color))
    units.append(dict(Name="Miner", Type=Miner, Color=main_color))
    units.append(dict(Name="Fisherman", Type=Fisherman, Color=main_color))
    units.append(dict(Name="Knight", Type=Knight, Color=main_color))
    units.append(dict(Name="Archer", Type=Archer, Color=main_color))
