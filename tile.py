from enum import Enum
from typing import List

# our stuff
from constants import Constants
from environment import Environment

class Tiles(list):
    Tiles = None

    def __init__(self):
        self.Tiles = list[Tile]()

    def get_tile_by_node_coords(self, gridx, gridy):
        for tile in self.Tiles:
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
    NonPlayableTile = True

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
    