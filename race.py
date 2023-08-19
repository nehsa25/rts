from enum import Enum

# our stuff
from goblin import Goblin
from elf import Elf
from human import Human
from fae import Fae
from dwarf import Dwarf
from nyrriss import Nyrriss
from arguna import Arguna

class Race:
    log_utils = None
    races = None

    def __init__(self, log_utils):
        self.log_utils = log_utils
        self.log_utils.log.debug("Initializing Race() class")     
        self.races = [i.name for i in Race.Races]

    def get_race_by_name(self, name):
        if name.upper() == "GOBLIN":
            race = Goblin(self.log_utils)
        elif name.upper() == "ELF":
            race = Elf(self.log_utils)
        elif name.upper() == "HUMAN":
            race = Human(self.log_utils)
        elif name.upper() == "FAE":
            race = Fae(self.log_utils)
        elif name.upper() == "DWARF":
            race = Dwarf(self.log_utils)
        elif name.upper() == "NYRRISS":
            race = Nyrriss(self.log_utils)
        elif name.upper() == "ARGUNA":
            race = Arguna(self.log_utils)
        return race


    class Races(Enum):
        GOBLIN = 0,    
        ELF = 1
        HUMAN = 2,
        FAE = 3,
        DWARF = 4,
        NYRRISS = 5,
        ARGUNA = 6
