from enum import Enum

class Environment(object):
    class levels(Enum):
        Subterranean = 0
        Ground = 1
        Air = 2
        Water = 3