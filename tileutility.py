from math import floor
from constants import Constants

class TileUtility(object):
    log_utils = None

    def __init__(self, log_utils):
        self.log_utils = log_utils
        self.log_utils.log.debug(f"Initializing TileUtility() class")

    def ConvertXYCoordToGridCoord(self, x, y):
        self.log_utils.log.debug(f"ConvertXYCoordToGridCoord: enter")
        gridx = 0   
        if x > Constants.SIDE_PANEL_WIDTH_PX:
            gridx = int(floor((x - Constants.SIDE_PANEL_WIDTH_PX) / Constants.TILE_WIDTH_PX))
            gridx2 = int((x - Constants.SIDE_PANEL_WIDTH_PX) / Constants.TILE_WIDTH_PX)
        gridy = floor(y / Constants.TILE_HEIGHT_PX)
        return gridx, gridy

    def ConvertGridCoordToXYCoord(self, x_gd, y_gd):
        x = Constants.SIDE_PANEL_WIDTH_PX + (x_gd * Constants.TILE_WIDTH_PX)
        y = y_gd * Constants.TILE_HEIGHT_PX
        return (x,y)