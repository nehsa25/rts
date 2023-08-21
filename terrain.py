from constants import Constants

# base class - don't used directly, use BASIC
class Terrain(object):
    background_color = Constants.Colors.TERRAIN_BASIC
    walkable = True

    def __init__(self, background_color, walkable):
        self.background_color = background_color
        self.walkable = walkable

# inherits from base class
class TerrainForest(Terrain):    
    name = "Forest"
    def __init__(self):
        super().__init__(Constants.Colors.TERRAIN_FOREST, False)

class TerrainWater(Terrain):
    name = "Water"
    def __init__(self):
        super().__init__(Constants.Colors.TERRAIN_RAIN, False)

class TerrainRain(Terrain):
    name = "Rain"
    def __init__(self):
        super().__init__(Constants.Colors.TERRAIN_RAIN, False)

class TerrainLava(Terrain):
    name = "Lava"
    def __init__(self):
        super().__init__(Constants.Colors.TERRAIN_LAVA, False)

class TerrainFog(Terrain):
    name = "Fog"
    def __init__(self):
        super().__init__(Constants.Colors.TERRAIN_FOG, True)

class TerrainFire(Terrain):
    name = "Fire"
    def __init__(self):
        super().__init__(Constants.Colors.TERRAIN_FIRE, True)

class TerrainMountain(Terrain):
    name = "Mountain"
    def __init__(self):
        super().__init__(Constants.Colors.TERRAIN_MOUNTAIN, False)

class TerrainSwamp(Terrain):
    name = "Swamp"
    def __init__(self):
        super().__init__(Constants.Colors.TERRAIN_SWAMP, True)

class TerrainBasic(Terrain):
    def __init__(self):
        super().__init__(Constants.Colors.TERRAIN_BASIC, True)
