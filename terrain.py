from constants import Constants

# base class - don't used directly, use BASIC
class Terrain(object):
    background_color = Constants.Colors.TERRAIN_BASIC
    walkable = True
    cost = None
    name = None

    def __init__(self, name, background_color, walkable, cost):
        self.background_color = background_color
        self.walkable = walkable
        self.cost = cost

# inherits from base class
class TerrainForest(Terrain):    
    name = "Forest"
    def __init__(self):
        super().__init__(self.name, Constants.Colors.TERRAIN_FOREST, walkable=False, cost=-1)

class TerrainWater(Terrain):
    name = "Water"
    def __init__(self):
        super().__init__(self.name, Constants.Colors.TERRAIN_RAIN, walkable=True, cost=1000)

class TerrainRain(Terrain):
    name = "Rain"
    def __init__(self):
        super().__init__(self.name, Constants.Colors.TERRAIN_RAIN, walkable=True, cost=50)

class TerrainLava(Terrain):
    name = "Lava"
    def __init__(self):
        super().__init__(self.name, Constants.Colors.TERRAIN_LAVA, walkable=False, cost=-3)

class TerrainFog(Terrain):
    name = "Fog"
    def __init__(self):
        super().__init__(self.name, Constants.Colors.TERRAIN_FOG, walkable=True, cost=10)

class TerrainFire(Terrain):
    name = "Fire"
    def __init__(self):
        super().__init__(self.name, Constants.Colors.TERRAIN_FIRE, walkable=True, cost=1500)

class TerrainMountain(Terrain):
    name = "Mountain"
    def __init__(self):
        super().__init__(self.name, Constants.Colors.TERRAIN_MOUNTAIN, walkable=False, cost=-2)

class TerrainSwamp(Terrain):
    name = "Swamp"
    def __init__(self):
        super().__init__(self.name, Constants.Colors.TERRAIN_SWAMP, walkable=True, cost=100)

class TerrainBasic(Terrain):
    name = "Basic"
    def __init__(self):
        super().__init__(self.name, Constants.Colors.TERRAIN_BASIC, walkable=True, cost=1)
