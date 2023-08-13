from enum import Enum
from typing import List

# our stuff
from constants import Constants
from environment import Environment

class Tiles(list):
    MapTiles = []

    def __init__(self):
        self.MapTiles = list[Tile]()

    def CreateNewTile(self, pgu, x=None, y=None, gridx=None, gridy=None):
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
        self.Level = Environment.Level.Ground
        self.Type = Environment.TileType.Basic
        self.x = x
        self.y = y
        self.Grid_x = gridx
        self.Grid_y = gridy

    ### Returns tuple of coords in XY coordinate form
    def ConvertGridCoordToXYCoord(self, gridx, gridy):
        return int(gridx * Constants.UNIT_SIZE), int(gridy * Constants.UNIT_SIZE)
    
    ### Returns tuple of coords in grid XY coordinate form
    def ConvertXYCoordToGridCoords(self, x, y):
        return int(x / Constants.UNIT_SIZE), int(y / Constants.UNIT_SIZE)
    