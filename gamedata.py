
from menu import Menu
from race import Race
from events import Events
from tile import Tiles
from utility import Utility
from pygameutility import PygameUtilities
from player import Player
from unit import Unit


class GameData(PygameUtilities, 
               Events, 
               Utility, 
               Tiles, 
               Menu,
               Race,
               Unit):
    selected_units = []
    player = None
    log_utils = None
    race = None
    show_grid = False
    showing_grid = False

    def __init__(self, log_utils):
        self.log_utils = log_utils
        self.log_utils.log.info("Initializing GameData() class")
        PygameUtilities.__init__(self)
        Events.__init__(self)
        Utility.__init__(self)
        Tiles.__init__(self)
        Menu.__init__(self)
        Race.__init__(self)
        Unit.__init__(self)

        self.player = Player(log_utils)
