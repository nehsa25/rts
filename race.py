from enum import Enum

# our stuff
from goblin import GoblinFactory
from elf import ElvenFactory
from human import HumanFactory
from fae import FaeFactory
from dwarf import DwarvenFactory
from nyrriss import NyrrissFactory
from arguna import ArgunaFactory

class Race(object):
    races = None
    goblin_factory = None
    elven_factory = None
    human_factory = None
    dwarven_factory = None
    nyrriss_factory = None
    arguna_factory = None
    fae_factory = None

    def __init__(self):
        self.log_utils.log.info("Initializing Race() class")   
        self.goblin_factory = GoblinFactory(self.log_utils)
        self.elven_factory = ElvenFactory(self.log_utils)
        self.human_factory = HumanFactory(self.log_utils)
        self.fae_factory = FaeFactory(self.log_utils)
        self.dwarven_factory = DwarvenFactory(self.log_utils)
        self.nyrriss_factory = NyrrissFactory(self.log_utils)
        self.arguna_factory = ArgunaFactory(self.log_utils)
        
        self.races = [i.name for i in Race.Races]

    def get_race_by_name(self, name):
        if name.upper() == "GOBLIN":
            race = GoblinFactory(self.log_utils)
        elif name.upper() == "ELF":
            race = ElvenFactory(self.log_utils)
        elif name.upper() == "HUMAN":
            race = HumanFactory(self.log_utils)
        elif name.upper() == "FAE":
            race = FaeFactory(self.log_utils)
        elif name.upper() == "DWARF":
            race = DwarvenFactory(self.log_utils)
        elif name.upper() == "NYRRISS":
            race = NyrrissFactory(self.log_utils)
        elif name.upper() == "ARGUNA":
            race = ArgunaFactory(self.log_utils)
        return race

    class Races(Enum):
        GOBLIN = 0,    
        ELF = 1
        HUMAN = 2,
        FAE = 3,
        DWARF = 4,
        NYRRISS = 5,
        ARGUNA = 6
