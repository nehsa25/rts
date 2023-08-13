from enum import Enum

class Environment:
    class Level(Enum):
        Subterranean = 0
        Ground = 1
        Air = 2
        Sea = 3
        
    class TileType(Enum):
        Lava = 0
        Mountain = 1
        Water = 2
        Rain = 3
        Fog = 4
        Forest = 5
        Swamp = 6
        Basic = 7 # nothing special
