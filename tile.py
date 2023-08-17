import inspect
import time
import random
import pygame
from enum import Enum
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.grid import Grid

# our stuff
from constants import Constants

class Tiles:
    Finder = None
    Grid = None
    GridMatrix = None
    MapTiles = []
    logutils = None

    def __init__(self, logutils):
        self.logutils = logutils
        self.logutils.log.debug("Initializing Tiles() class")
        self.Finder = AStarFinder()
        self.MapTiles = list[Tile]()

    def ConvertXYCoordToGridCoord(self, x, y):
        self.logutils.log.debug(f"Inside ConvertXYCoordToGridCoord: {inspect.currentframe().f_code.co_name}")
        gridx = 0   
        tile = self.GetTile(0,0)
        if x > Constants.SIDE_PANEL_WIDTH_PX:
            gridx = int(x / tile.Width)
        gridy = int(y / tile.Height)
        return gridx, gridy
    
    def UpdateTile(self, NewTile):
        self.logutils.log.debug(f"Inside UpdateTile: {inspect.currentframe().f_code.co_name}")   
        prev_tile = self.GetTile(NewTile.Grid_x, NewTile.Grid_y)
        self.MapTiles.remove(prev_tile)

        if NewTile.GridNode is None:
            NewTile.GridNode = self.GetNodeByNodeCoord(NewTile.Grid_x, NewTile.Grid_y, self.Grid)

        self.MapTiles.append(NewTile)

    def load_grid(self, pgu, ut, player, load_env = True):
        self.logutils.log.info(f"Inside load_grid: {inspect.currentframe().f_code.co_name}") 
        # get grid of screen based on unit size
        self.Grid = self.get_empty_grid(pgu)   

        # ensure map meets basic criterias (NOT IMPLEMENTED)
        usable_map = False     
        while not usable_map:
            # generate our obstacles
            if load_env:
                self.Grid = self.CreateTerrainTiles(pgu, self.Grid)

                # update grid with nodes we cannot walk on
                self.Grid = self.UpdateGridWithTerrain(self.Grid)

            usable_map = True
            runs = 0

            #  refresh side panel / highlight a unit that's hovered over
            ut.draw_side_panel(pgu, player, really_draw=False)

            # spawn points
            ut.draw_spawn_points(pgu, self, really_draw=False)

            # # ensure usable map - also ensure we have a route to the other side of screen
            # unit_spawn_x = int(Constants.UNIT_SPAWN_X / Constants.UNIT_SIZE)
            # unit_spawn_y = int(Constants.UNIT_SPAWN_Y / Constants.UNIT_SIZE)
            # start = grid.node(unit_spawn_x, unit_spawn_y)
            # end_cord_x = int((Constants.SCREEN_WIDTH-Constants.BORDER_SIZE) / Constants.UNIT_SIZE)
            # end_cord_y = int((Constants.SCREEN_HEIGHT-Constants.BORDER_SIZE) / Constants.UNIT_SIZE)
            # end = grid.node(end_cord_x, end_cord_y)
            # paths, runs = self.finder.find_path(start, end, grid)

            # if len(paths) > 1:
            #     usable_map = True
            # else:
            #     usable_map = False

            self.logutils.log.debug(f"Map created is: {usable_map}")
            self.Grid.cleanup()
        return f"usable_map: {usable_map}, runs: {runs}"
    
    def get_empty_grid(self, pgu):
        max_y = Constants.GAME_SIZE_HEIGHT_GD
        max_x = Constants.GAME_SIZE_WIDTH_GD
        y_step = Constants.HEIGHT_STEP
        x_step = Constants.WIDTH_STEP
        self.logutils.log.info(f"Inside get_empty_grid: {inspect.currentframe().f_code.co_name}")
        get_empty_start = time.perf_counter()   
        self.logutils.log.info(f"Generating grid based on {max_x}x{max_y} (step: ({y_step}x{x_step})")
        matrix = []  

        for _ in range(0, max_y, y_step):
            x_line = []
            for _ in range(0, max_x, x_step):
                x_line.append(1)
            matrix.append(x_line)

        # based on res    
        # for y in range(0, Constants.SCREEN_HEIGHT, Constants.UNIT_SIZE):
        #     x_line = []
        #     for x in range(0, Constants.SCREEN_WIDTH, Constants.UNIT_SIZE):
        #         x_line.append(1)
        #     matrix.append(x_line)

        self.logutils.log.info(f"get_empty_grid: Generating pathfinding grid based on matrix:\n{matrix}")
        self.GridMatrix = matrix
        self.Grid = Grid(matrix = self.GridMatrix)
        for node in self.Grid.nodes:
            for item in node:
                item.walkable = True
                t = Tile(self.logutils, pgu, gridx=item.x, gridy=item.y, grid=self.Grid)
                t.GridNode = item
                self.logutils.log.debug(f"get_empty_grid: created basic tile: ({t.x}x{t.y})")
                self.MapTiles.append(t)

        self.logutils.log.info("get_empty_grid: Done...")
        get_empty_end = time.perf_counter()
        self.logutils.log.debug(f"get_empty_grid timings: {round(60 - (get_empty_end - get_empty_start), 2)} second(s)")

        return self.Grid
    
    def GetUniqueTerrain(self):
        tiles = [i for i in self.MapTiles if i.Type != Tile.Type.Basic]
        #print(f"Unique tiles on map: {len(tiles)}")
        result = ""
        for tile in tiles:
            result += f"  {tile.Type}, XY:({tile.x}x{tile.y}), Grid:({tile.Grid_x}x{tile.Grid_y})\n"
        return result

    def show_grid(self, pgu):     
        self.logutils.log.debug(f"Inside show_grid: {inspect.currentframe().f_code.co_name}")
        pgu.surface.fill(Constants.Colors.GAME_MAP_COLOR) 
        show_grid_start = time.perf_counter()  
        self.logutils.log.debug("Showing grid")   
        mouse_pos = pgu.update_mouse()   
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]

        details_node = None
        for tile in self.MapTiles:
            self.logutils.log.debug(f"tile.x == mouse_pos[0]: {tile.x == mouse_pos[0]}, tile.y == mouse_pos[1]: {tile.y == mouse_pos[1]}")
            rs = pgu.RectSettings()
            rs.x = tile.x
            rs.y = tile.y
            rs.Width = tile.Width
            rs.Height = tile.Height
            if tile.GridNode.walkable:
                rs.BgColor = Constants.Colors.GREEN_DARK
            else:
                rs.BgColor = Constants.Colors.BURNT_ORANGE
            rs.BorderColor = Constants.Colors.NEON_GREEN
            rs.BorderSize = 1
            pgu.create_rect(rs)

            gridcord = self.ConvertXYCoordToGridCoord(mouse_x, mouse_y)
            if tile.Grid_x == gridcord[0] and tile.Grid_y == gridcord[1]:
                details_node = tile
        show_grid_end = time.perf_counter()   

        if details_node is not None:
            pgu.update_mouse(tile=details_node)  
        self.logutils.log.debug(f"show_grid timings: {round(60 - (show_grid_end - show_grid_start), 2)} second(s)")

    def UpdateGridWithTerrain(self, grid):
        self.logutils.log.info(f"Inside UpdateGridWithTerrain: {inspect.currentframe().f_code.co_name}")
        get_grid_start = time.perf_counter()
        self.logutils.log.debug("get_grid: Updating pathfinding grid with terrain...")
        for node in grid.nodes:
            for item in node:
                current_node = self.GetTileByNodeCoord(item.x, item.y)
                unwalkable_tiletypes = [i for i in Tile.Type if i.value["Walkable"] == False]
                if current_node.Type in unwalkable_tiletypes:
                    item.walkable = False
                else:
                    item.walkable = True

        get_grid_end = time.perf_counter()
        self.logutils.log.debug(f"get_grid timings: {round(60 - (get_grid_end - get_grid_start), 2)} second(s)")
        return grid

    def GetTileWidth(self):
        return self.MapTiles[0].Width
    
    def GetTile(self, gridx, gridy):
        self.logutils.log.debug(f"Inside GetTile: {inspect.currentframe().f_code.co_name}")
        tiles = [i for i in self.MapTiles if gridx == i.Grid_x and gridy == i.Grid_y]
        tile = None
        if len(tiles) > 0:
            tile = tiles[0]
        else:
            self.logutils.log.debug(f"No tile found for grid coordinates: ({gridx}x{gridy})")
        
        return tile

    def CreateRandomTiles(self, pgu, grid, terrain_type, type_num):
        self.logutils.log.info(f"Inside CreateRandomTiles: {inspect.currentframe().f_code.co_name}")
        start = time.perf_counter()
        body_num_tiles = 0
        for num_complete in range(type_num):
            self.logutils.log.debug(f"CreateRandomTiles ({terrain_type.name}) % Complete: {round(((num_complete / type_num) * 100), 2)}")
            num_tiles_remaining = type_num

            # start at a random point
            rand_node = random.choice(grid.nodes)
            rand_cord = random.choice(rand_node)
            grid_x = rand_cord.x
            grid_y = rand_cord.y

            # chose a random water size
            size = Constants.DensityTypes.get_random_size()
            body_size = 0
            if size == "tiny":
                body_size = random.randint(1, 2)
            elif size == "small":
                body_size = random.randint(2, 6)
            elif size == "medium":
                body_size = random.randint(6, 10)
            elif size == "large":
                body_size = random.randint(10, 30)
            elif size == "huge":
                body_size = random.randint(30, 100)

            while body_num_tiles <= body_size:
                side = Constants.BorderSides.get_random_side()
                if side == "left":
                    grid_x += -1
                elif side == "right":
                    grid_x += 1
                elif side == "top":
                    grid_y += -1
                elif side == "bottom":
                    grid_y += 1

                tile = self.GetTile(grid_x, grid_y)

                # ensure we don't get off track
                if tile is None:
                    break

                # if the tile is basic we can use it for something else..
                if tile.Type == Tile.Type.Basic:
                    self.logutils.log.debug(f"picked {terrain_type} tile placement: {grid_x}x{grid_y}")
                    t = Tile(self.logutils, pgu, gridx=grid_x, gridy=grid_y, grid=self.Grid)
                    t.Type = terrain_type
                    self.UpdateTile(t)
                    body_num_tiles += 1
                    num_tiles_remaining -= 1

                if num_tiles_remaining <= 0:
                    break

            self.logutils.log.debug(f"Wanted tiles for density size \"{size}\": {body_size}, got: {body_num_tiles}")
            if num_tiles_remaining <= 0:
                break

            # start next "body" of water
            body_num_tiles = 0

        end = time.perf_counter()
        self.logutils.log.debug(f"CreateRandomTiles ({terrain_type.name}): {round(60 - (end - start), 2)} second(s)")
        return grid

    # returns all obstablces in a single list of dictionaries
    def CreateTerrainTiles(self, pgu, grid):
        self.logutils.log.info(f"Inside CreateTerrainTiles: {inspect.currentframe().f_code.co_name}")
        create_terrain_start = time.perf_counter()

        # for r in menu_rects:
        #     walkable = r["walkable"]
        #     # create side panel tiles
        #     height_start = 0
        #     height_end = int(r["rects"].Rect.height / Constants.UNIT_SIZE)
        #     width_start = 0
        #     width_end = int(r["rects"].Rect.width / Constants.UNIT_SIZE)

        #     for w in range(width_start, width_end):
        #         for h in range(height_start, height_end):
        #             self.logutils.log.debug(f"(w,h): ({h},{w})")
        #             current_node = grid.nodes[h]
        #             current_coord = current_node[w]
        #             grid.node(current_coord.x, current_coord.y).walkable = False
        #             # rect_x = current_coord.x * Constants.UNIT_SIZE
        #             # rect_y = current_coord.y * Constants.UNIT_SIZE
        #             # rect = pygame.Rect(rect_x, rect_y, Constants.UNIT_SIZE, Constants.UNIT_SIZE)
        #             # obstacles.append(dict(name="panel", rect=rect, walkable=walkable))

        # create water tiles
        grid = self.CreateRandomTiles(pgu, grid, Tile.Type.Water, Constants.NUM_WATER_TILES)
        grid = self.CreateRandomTiles(pgu, grid, Tile.Type.Mountain, Constants.NUM_MOUNTAIN_TILES)
        grid = self.CreateRandomTiles(pgu, grid, Tile.Type.Swamp, Constants.NUM_SWAMP_TILES)
        grid = self.CreateRandomTiles(pgu, grid, Tile.Type.Fire, Constants.NUM_FIRE_TILES)
        grid = self.CreateRandomTiles(pgu, grid, Tile.Type.Forest, Constants.NUM_FOREST_TILES)
        grid = self.CreateRandomTiles(pgu, grid, Tile.Type.Fog, Constants.NUM_FOG_TILES)
        grid = self.CreateRandomTiles(pgu, grid, Tile.Type.Rain, Constants.NUM_RAIN_TILES)
        grid = self.CreateRandomTiles(pgu, grid, Tile.Type.Lava, Constants.NUM_LAVA_TILES)

        create_terrain_end = time.perf_counter()
        self.logutils.log.debug(f"create_terrain timings: {round(60 - (create_terrain_end - create_terrain_start), 2)} second(s)")
        return grid

    def GetTileByNodeCoord(self, gridx, gridy):
        self.logutils.log.debug(f"Inside GetTileByNodeCoord ({gridx}x{gridy}): {inspect.currentframe().f_code.co_name}")
        tiles = [i for i in self.MapTiles if i.Grid_x == gridx and i.Grid_y == gridy]
        tile = None
        if len(tiles) > 0:
            tile = tiles[0]
        return tile            

    def GetNodeByNodeCoord(self, gridx, gridy, grid):
        current_node = grid.nodes[gridy]
        return current_node[gridx]

    def DrawTerrainTiles(self, pgu):
        self.logutils.log.debug(f"Inside DrawTerrainTiles: {inspect.currentframe().f_code.co_name}")
        draw_terrain_start = time.perf_counter()
        for tile in self.MapTiles:
            if tile.Type == Tile.Type.Water:
                pygame.draw.rect(pgu.surface, Constants.Colors.AQUA, tile.RectSettings.Rect)
            elif tile.Type == Tile.Type.Fire:
                pygame.draw.rect(pgu.surface, Constants.Colors.FIRE, tile.RectSettings.Rect)
            elif tile.Type == Tile.Type.Mountain:
                pygame.draw.rect(pgu.surface, Constants.Colors.WHITE_MISTY, tile.RectSettings.Rect)
            elif tile.Type == Tile.Type.Forest:
                pygame.draw.rect(pgu.surface, Constants.Colors.GREEN_DARK, tile.RectSettings.Rect)
            elif tile.Type == Tile.Type.Rain:
                pygame.draw.rect(pgu.surface, Constants.Colors.RAIN, tile.RectSettings.Rect)
            elif tile.Type == Tile.Type.Fog:
                pygame.draw.rect(pgu.surface, Constants.Colors.GRAY_IRON_MOUNTAIN, tile.RectSettings.Rect)
            elif tile.Type == Tile.Type.Swamp:
                pygame.draw.rect(pgu.surface, Constants.Colors.OLIVE, tile.RectSettings.Rect)
            elif tile.Type == Tile.Type.Lava:
                pygame.draw.rect(pgu.surface, Constants.Colors.LAVA, tile.RectSettings.Rect)
            elif tile.Type == Tile.Type.Basic:
                pygame.draw.rect(pgu.surface, Constants.Colors.SANDY_BROWN, tile.RectSettings.Rect)
        draw_terrain_end = time.perf_counter()
        # print(f"DrawTerrainTiles timings: {round(60 - (draw_terrain_end - draw_terrain_start), 2)} second(s)")

class Tile:
    Level = None
    Type = None
    x = None
    y = None
    Grid_x = None
    Grid_y = None
    GridNode = None
    RectSettings = None
    UsableTile = True
    Width = None
    Height = None
    logutils = None
    TileDetails = ""
    Units = []

    class Level(Enum):
        Subterranean = 0
        Ground = 1
        Air = 2
        Sea = 3

    class Type(Enum):
        Basic = dict(BgColor=Constants.Colors.SANDY_BROWN, Walkable=True) # nothing special
        Lava = dict(BgColor=Constants.Colors.LAVA, Walkable=False)
        Mountain = dict(BgColor=Constants.Colors.WHITE_MISTY, Walkable=False)
        Water = dict(BgColor=Constants.Colors.AQUA, Walkable=False)
        Rain = dict(BgColor=Constants.Colors.WATER, Walkable=True)
        Fog = dict(BgColor=Constants.Colors.GRAY_IRON_MOUNTAIN, Walkable=True)
        Forest = dict(BgColor=Constants.Colors.HUNTER_GREEN, Walkable=False)
        Swamp = dict(BgColor=Constants.Colors.GREEN_DARK, Walkable=True)
        Fire = dict(BgColor=Constants.Colors.BURNT_ORANGE, Walkable=True)
    
    def __init__(self, logutils, pgu, gridx, gridy, grid):
        self.logutils = logutils
        self.logutils.log.debug("Initializing Tile() class")
        self.Width = int(((Constants.SCREEN_WIDTH_PX - Constants.SIDE_PANEL_WIDTH_PX) / Constants.GAME_SIZE_WIDTH_GD) * Constants.WIDTH_STEP)
        self.Height = int((Constants.SCREEN_HEIGHT_PX / Constants.GAME_SIZE_HEIGHT_GD) * Constants.HEIGHT_STEP)
        self.Level = Tile.Level.Ground
        self.Type = Tile.Type.Basic
        self.Grid_x = gridx
        self.Grid_y = gridy
        self.x = self.CalculateX(gridx)
        self.y = gridy * self.Height
        self.GridNode = grid.node(gridx, gridy)  
        self.TileDetails = f"Coordinates: ({self.x}, {self.y})\n"
        self.TileDetails += f"Grid node: ({self.Grid_x}, {self.Grid_y})\n"
        self.TileDetails += f"walkable: {self.GridNode.walkable}\n"
        self.TileDetails += f"Type: {self.Type}\n"
        self.TileDetails += f"Units: {len(self.Units)}\n"
        # self.TileDetails += f"Unique Terrain: {self.GetUniqueTerrain()}\n"

        # actual rect
        rs = pgu.RectSettings()
        rs.x = self.x
        rs.y = self.y
        rs.Width = self.Width
        rs.Height = self.Height
        self.RectSettings = pgu.create_rect(rs)

    def CalculateX(self, gridx):
        x = Constants.SIDE_PANEL_WIDTH_PX + (gridx * self.Width)
        print(f"CalculateNodeX: {gridx} -> {x}")
        return x

    # def GetNodeWidth(self):
    #     return self.CalculateX(0)
