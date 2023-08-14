from enum import Enum
from typing import List

# our stuff
from constants import Constants
from terrain import Terrain

class Tiles(list):
    MapTiles = []

    def __init__(self):
        self.MapTiles = list[Tile]()

    def ConvertXYCoordToGridCoord(self, gridx, gridy):
        return int(gridx / Constants.UNIT_SIZE), int(gridy / Constants.UNIT_SIZE)
    
    def UpdateTile(self, NewTile):
        prev_tile = [i for i in self.MapTiles if (i.Grid_x == NewTile.Grid_x and i.Grid_y == NewTile.Grid_y) or (i.x == NewTile.x and i.y == NewTile.y)]
        if prev_tile is not []:
            self.MapTiles.remove(prev_tile[0])

        self.MapTiles.append(NewTile)

    def GetTile(self, gridx, gridy):
        tiles = [i for i in self.MapTiles if gridx == i.Grid_x and gridy == i.Grid_y]
        tile = None
        if len(tiles) > 0:
            tile = tiles[0]
        else:
            print(f"No tile found for grid coordinates: ({gridx}x{gridy})")
        
        return tile

    def CreateTile(self, pgu, x=None, y=None, gridx=None, gridy=None):
        t = Tile()
        if x is not None:
            t.x = x
            t.Grid_x = int(x / Constants.UNIT_SIZE)
        
        if y is not None:
            t.y = y
            t.Grid_y = int(y / Constants.UNIT_SIZE)
        
        if gridx is not None:
            t.x = int(gridx * Constants.UNIT_SIZE)
            t.Grid_x = gridx

        if gridy is not None:
            t.y = int(gridy * Constants.UNIT_SIZE)
            t.Grid_y = gridy

        if (t.x is None and t.y is None) or (t.Grid_x is None and t.Grid_y is None):
            raise Exception("You must pass either x/y or gridx/gridy coordinates")

        rs = pgu.RectSettings()
        rs.x = t.x
        rs.y = t.y
        rs.Width = t.Width
        rs.Height = t.Height
        # (self, rs, ignore_side_panel = False, really_draw = True):
        t.RectSettings = pgu.create_rect(rs)

        return t

    def GetTileByNodeCoord(self, gridx, gridy):
        for tile in self.MapTiles:
            print(f"get_tile_by_node_coords: {tile}")

class Tile:
    Walkable = None
    Level = None
    Type = None
    x = None
    y = None
    Grid_x = None
    Grid_y = None
    GridNode = None
    RectSettings = None
    UsableTile = True
    Width = Constants.UNIT_SIZE
    Height = Constants.UNIT_SIZE

    def __init__(self, x=None, y=None, gridx=None, gridy=None):
        self.Walkable = True
        self.Level = Terrain.Level.Ground
        self.Type = Terrain.Type.Basic
        self.x = x
        self.y = y
        self.Grid_x = gridx
        self.Grid_y = gridy

    
    def ConvertGridCoordToXYCoord(self):
        return int(self.Grid_x * Constants.UNIT_SIZE), int(self.Grid_y * Constants.UNIT_SIZE)
    
    def ConvertXYCoordToGridCoord(self):
        return int(self.x / Constants.UNIT_SIZE), int(self.y / Constants.UNIT_SIZE)
    