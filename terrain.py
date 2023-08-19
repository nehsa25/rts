from constants import Constants

# base class - don't used directly, use BASIC
class Terrain:
    background_color = Constants.Colors.TERRAIN_BASIC
    walkable = True

    def __init__(self, background_color, walkable):
        self.background_color = background_color
        self.walkable = walkable

# inherits from base class
class TerrainForest(Terrain):    
    num_tiles = 0
    name = "Forest"
    def __init__(self, num_tiles):
        super().__init__(Constants.Colors.TERRAIN_FOREST, False)

class TerrainWater(Terrain):
    num_tiles = 0
    name = "Water"
    def __init__(self, num_tiles):
        super().__init__(Constants.Colors.TERRAIN_RAIN, False)

class TerrainRain(Terrain):
    num_tiles = 0
    name = "Rain"
    def __init__(self, num_tiles):
        super().__init__(Constants.Colors.TERRAIN_RAIN, False)

class TerrainLava(Terrain):
    num_tiles = 0
    name = "Lava"
    def __init__(self, num_tiles):
        super().__init__(Constants.Colors.TERRAIN_LAVA, False)

class TerrainFog(Terrain):
    num_tiles = 0
    name = "Fog"
    def __init__(self, num_tiles):
        super().__init__(Constants.Colors.TERRAIN_FOG, True)

class TerrainFire(Terrain):
    num_tiles = 0
    name = "Fire"
    def __init__(self, num_tiles):
        super().__init__(Constants.Colors.TERRAIN_FIRE, True)

class TerrainMountain(Terrain):
    num_tiles = 0
    name = "Mountain"
    def __init__(self, num_tiles):
        super().__init__(Constants.Colors.TERRAIN_MOUNTAIN, False)

class TerrainSwamp(Terrain):
    num_tiles = 0
    name = "Swamp"
    def __init__(self, num_tiles):
        super().__init__(Constants.Colors.TERRAIN_SWAMP, True)

class TerrainBasic(Terrain):
    def __init__(self):
        super().__init__(Constants.Colors.TERRAIN_BASIC, True)
