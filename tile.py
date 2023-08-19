import inspect
import time
import random
from uuid import uuid4
import pygame
from enum import Enum
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.grid import Grid

# our stuff
from constants import Constants
from terrain import TerrainBasic, TerrainFire, TerrainFog, TerrainLava, TerrainMountain, TerrainRain, TerrainSwamp, TerrainWater, TerrainForest

class Tiles:
    finder = None
    grid = None
    grid_matrix = None
    map_tiles = []
    map_detail_tiles = []
    log_utils = None
    total_tile_width = None
    total_tile_height = None
    tile_width = None
    tile_height = None

    terrain_water = None
    terrain_fire = None
    terrain_swamp = None
    terrain_forest = None
    terrain_fog = None
    terrain_rain = None
    terrain_lava = None
    terrain_mountain = None

    def __init__(self, log_utils):
        self.log_utils = log_utils
        self.log_utils.log.debug("Initializing Tiles() class")
        self.finder = AStarFinder()
        self.map_tiles = list[Tile]()

        # initialize our terrains
        self.terrain_water = TerrainWater(Constants.NUM_WATER_TILES)
        self.terrain_fire = TerrainFire(Constants.NUM_FIRE_TILES)
        self.terrain_swamp = TerrainSwamp(Constants.NUM_SWAMP_TILES)
        self.terrain_forest = TerrainForest(Constants.NUM_FOREST_TILES)
        self.terrain_fog = TerrainFog(Constants.NUM_FOG_TILES)
        self.terrain_rain = TerrainRain(Constants.NUM_RAIN_TILES)
        self.terrain_lava = TerrainLava(Constants.NUM_LAVA_TILES)
        self.terrain_mountain = TerrainMountain(Constants.NUM_LAVA_TILES)

        # calculate width
        self.tile_width = int(((Constants.SCREEN_WIDTH_PX - Constants.SIDE_PANEL_WIDTH_PX) / Constants.GAME_GRID_NODES) * Constants.WIDTH_STEP)
        self.tile_height = int((Constants.SCREEN_HEIGHT_PX / Constants.GAME_GRID_NODES) * Constants.HEIGHT_STEP)

    def ConvertXYCoordToGridCoord(self, x, y):
        self.log_utils.log.debug(f"Inside ConvertXYCoordToGridCoord")
        gridx = 0   
        tile = self.GetTile(0,0)
        if x > Constants.SIDE_PANEL_WIDTH_PX:
            gridx = int(x / self.tile_width)
        gridy = int(y / self.tile_width)
        return gridx, gridy
    
    def UpdateTile(self, NewTile):
        self.log_utils.log.debug(f"Inside UpdateTile")   
        prev_tile = self.GetTile(Newtile.tile_rect_settings.grid_x, Newtile.tile_rect_settings.grid_y)
        if prev_tile is not None:
            self.map_tiles.remove(prev_tile)

        if NewTile.GridNode is None:
            NewTile.GridNode = self.GetNodeByNodeCoord(Newtile.tile_rect_settings.grid_x, Newtile.tile_rect_settings.grid_y, self.grid)

        self.map_tiles.append(NewTile)
    
    def load_grid(self, pgu, ut, game_data, load_env = True):
        self.log_utils.log.info(f"Inside load_grid") 

        self.map_tiles = self.create_tiles(pgu)
        
        # ensure map meets basic criterias (NOT IMPLEMENTED)
        usable_map = False   

        while not usable_map:
            # generate our obstacles
            if load_env:
                self.add_terrain_to_tiles()

                self.get_empty_grid()

                self.update_tiles()

            usable_map = True
            runs = 0

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

            self.log_utils.log.debug(f"Map created is: {usable_map}")
            self.grid.cleanup()
        return f"usable_map: {usable_map}, runs: {runs}"
    
    # 1. creates tiles
    def create_tiles(self, pgu):
        tiles = []
        for y in range(0, Constants.GAME_GRID_NODES):
            for x in range(0, Constants.GAME_GRID_NODES):
                t = Tile(self.log_utils, x, y, self.tile_width, self.tile_height)
                tiles.append(t)

        print(tiles)
        return tiles

    # 2. create empty grid
    def get_empty_grid(self):
        max_y = Constants.GAME_GRID_NODES
        max_x = Constants.GAME_GRID_NODES
        y_step = Constants.HEIGHT_STEP
        x_step = Constants.WIDTH_STEP
        self.log_utils.log.info(f"Inside get_empty_grid")
        get_empty_start = time.perf_counter()   
        self.log_utils.log.info(f"Generating grid based on {max_x}x{max_y} (step: ({y_step}x{x_step})")
        matrix = []  

        for _ in range(0, max_y, y_step):
            x_line = []
            for _ in range(0, max_x, x_step):
                x_line.append(1)
            matrix.append(x_line)

        self.log_utils.log.info(f"get_empty_grid: Generating pathfinding grid based on matrix:\n{matrix}")
        self.grid_matrix = matrix
        self.grid = Grid(matrix = self.grid_matrix)
    
    # 3. adds in some terrain
    def add_terrain_to_tiles(self):
        self.log_utils.log.info(f"Inside CreateTerrainTiles")
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
        tiles = self.CreateRandomTiles(self.map_tiles, self.terrain_water, Constants.NUM_WATER_TILES)
        tiles = self.CreateRandomTiles(self.map_tiles, self.terrain_mountain, Constants.NUM_MOUNTAIN_TILES)
        tiles = self.CreateRandomTiles(self.map_tiles, self.terrain_swamp, Constants.NUM_SWAMP_TILES)
        tiles = self.CreateRandomTiles(self.map_tiles, self.terrain_fire, Constants.NUM_FIRE_TILES)
        tiles = self.CreateRandomTiles(self.map_tiles, self.terrain_forest, Constants.NUM_FOREST_TILES)
        tiles = self.CreateRandomTiles(self.map_tiles, self.terrain_fog, Constants.NUM_FOG_TILES)
        tiles = self.CreateRandomTiles(self.map_tiles, self.terrain_rain, Constants.NUM_RAIN_TILES)
        tiles = self.CreateRandomTiles(self.map_tiles, self.terrain_lava, Constants.NUM_LAVA_TILES)

        create_terrain_end = time.perf_counter()
        self.log_utils.log.debug(f"create_terrain timings: {round(60 - (create_terrain_end - create_terrain_start), 2)} second(s)")
        return self.map_tiles

    # 4. Update tiles
    def update_tiles(self):
        for tile in self.map_tiles:
            node = self.grid.node(tile.tile_rect_settings.grid_x, tile.tile_rect_settings.grid_y)
            if tile.terrain.walkable == True:
                node.walkable = True
            else:
                node.walkable = False
            tile.grid_node = node

    # 5. Create detail tiles


    def GetUniqueTerrain(self):
        tiles = [i for i in self.map_tiles if i.type != Tile.type.Basic]
        #print(f"Unique tiles on map: {len(tiles)}")
        result = ""
        for tile in tiles:
            result += f"  {tile.type}, XY:({tile.x}x{tile.y}), Grid:({tile.tile_rect_settings.grid_x}x{tile.tile_rect_settings.grid_y})\n"
        return result
    
    def show_grid(self, pgu):     
        self.log_utils.log.debug(f"Inside show_grid")
        pgu.surface.fill(Constants.Colors.GAME_MAP_COLOR) 
        show_grid_start = time.perf_counter()  
        self.log_utils.log.debug("Showing grid")   
        mouse_pos = pgu.update_mouse()   
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        grid_coords = self.ConvertXYCoordToGridCoord(mouse_x, mouse_y)
        detail_node = None
        for tile in self.map_detail_tiles:
            tile.draw_tile(pgu)
            if tile is not None:
                if tile.tile_rect_settings.grid_x == grid_coords[0] and tile.tile_rect_settings.grid_y == grid_coords[1]:
                    detail_node = tile
                    
        pgu.update_mouse(tile=detail_node)  
        show_grid_end = time.perf_counter()   


        self.log_utils.log.debug(f"show_grid timings: {round(60 - (show_grid_end - show_grid_start), 2)} second(s)")

    def UpdateGridWithTerrain(self, grid):
        self.log_utils.log.info(f"Inside UpdateGridWithTerrain")
        get_grid_start = time.perf_counter()
        self.log_utils.log.debug("get_grid: Updating pathfinding grid with terrain...")
        for node in grid.nodes:
            for item in node:
                current_node = self.GetTileByNodeCoord(item.x, item.y)
                unwalkable_tiletypes = [i for i in Tile.type if i.value["Walkable"] == False]
                if current_node.type in unwalkable_tiletypes:
                    item.walkable = False
                else:
                    item.walkable = True

        get_grid_end = time.perf_counter()
        self.log_utils.log.debug(f"get_grid timings: {round(60 - (get_grid_end - get_grid_start), 2)} second(s)")
        return grid

    def GetTile(self, gridx, gridy):
        self.log_utils.log.debug(f"Inside GetTile")
        tiles = [i for i in self.map_tiles if gridx == i.tile_rect_settings.grid_x and gridy == i.tile_rect_settings.grid_y]
        tile = None
        if len(tiles) > 0:
            tile = tiles[0]
        else:
            self.log_utils.log.debug(f"No tile found for grid coordinates: ({gridx}x{gridy})")
        
        return tile

    def CreateRandomTiles(self, tiles, terrain_type, type_num):
        self.log_utils.log.info(f"Inside CreateRandomTiles: {terrain_type.name}")
        start = time.perf_counter()
        body_num_tiles = 0
        num_tiles_remaining = type_num
        for num_complete in range(type_num):
            self.log_utils.log.debug(f"CreateRandomTiles ({terrain_type.name}) % Complete: {round(((num_complete / type_num) * 100), 2)}")

            # start at a random point
            xadjustment = 0
            yadjustment = 0
            rand_x = random.randrange(0, Constants.GAME_GRID_NODES)
            rand_y = random.randrange(0, Constants.GAME_GRID_NODES)

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

            start_new = False
            while (body_num_tiles <= body_size) and not start_new:
                side = Constants.BorderSides.get_random_side()
                if side == "left":
                    xadjustment += -1
                elif side == "right":
                    xadjustment += 1
                elif side == "top":
                    yadjustment += -1
                elif side == "bottom":
                    yadjustment += 1

                rand_x += xadjustment
                rand_y += yadjustment

                for tile in tiles:
                    if (rand_x < 0 or rand_x > Constants.GAME_GRID_NODES) or (rand_y < 0 or rand_y > Constants.GAME_GRID_NODES):
                        start_new = True
                        break
                    if (tile.tile_rect_settings.grid_x == rand_x and tile.tile_rect_settings.grid_y == rand_y) and num_tiles_remaining >= 1:
                        print(f"picked {terrain_type.name} tile placement: {tile.tile_rect_settings.grid_x}x{tile.tile_rect_settings.grid_y}")
                        tile.terrain = terrain_type
                        num_tiles_remaining -= 1
                        body_num_tiles += 1
                        break

            self.log_utils.log.debug(f"Wanted tiles for density size \"{size}\": {body_size}, got: {body_num_tiles}")
            if num_tiles_remaining <= 0:
                break

        end = time.perf_counter()
        self.log_utils.log.debug(f"CreateRandomTiles ({terrain_type.name}): {round(60 - (end - start), 2)} second(s)")
        return tiles

    def GetTileByNodeCoord(self, gridx, gridy):
        self.log_utils.log.debug(f"Inside GetTileByNodeCoord ({gridx}x{gridy})")
        tiles = [i for i in self.map_tiles if i.grid_x == gridx and i.grid_y == gridy]
        tile = None
        if len(tiles) > 0:
            tile = tiles[0]
        return tile            

    def GetNodeByNodeCoord(self, gridx, gridy, grid):
        current_node = grid.nodes[gridy]
        return current_node[gridx]

    def DrawTerrainTiles(self, pgu):
        self.log_utils.log.debug(f"Inside DrawTerrainTiles")
        draw_terrain_start = time.perf_counter()
        for tile in self.map_tiles:
            pygame.draw.rect(pgu.surface, tile.terrain.background_color, tile.tile_rect_settings.rect)
        draw_terrain_end = time.perf_counter()
        # print(f"DrawTerrainTiles timings: {round(60 - (draw_terrain_end - draw_terrain_start), 2)} second(s)")

class Tile:
    level = None
    grid_node = None
    tile_rect_settings = None
    usable_tile = True
    log_utils = None
    tile_details = ""
    units = []
    terrain = None

    class level(Enum):
        subterranean = 0
        ground = 1
        air = 2
        sea = 3

    # rect(surface, color, rect, width=0, border_radius=0, 
    # border_top_left_radius=-1, border_top_right_radius=-1, 
    # border_bottom_left_radius=-1, border_bottom_right_radius=-1)
    class tile_rect_settings:  
        x = None
        y = None  
        grid_x = None
        grid_y = None    
        width = None
        height = None
        hint_name = None
        rect = None
        text = None
        font = None
        font_name = Constants.FONT_NAME_DEFAULT
        font_size = Constants.FONT_SIZE_DEFAULT_PX
        background_color = Constants.Colors.GREEN
        font_color = Constants.Colors.BLACK
        BorderColor = None   
        BorderSides = None  
        BorderRadius = 3
        BorderWidth = Constants.BORDER_SIZE_PX

        def __init__(self, grid_x, grid_y, tile_width, tile_height, background_color):
            self.x = grid_x + tile_width
            self.y = grid_y + tile_height
            self.grid_x = grid_x
            self.grid_y = grid_y
            self.background_color = background_color
            self.tile_width = tile_width
            self.tile_height = tile_height
            self.rect = pygame.Rect(self.x, self.y, tile_width, tile_height) 

    def __init__(self, log_utils, grid_x, grid_y, tile_width, tile_height, terrain=TerrainBasic()):    
        self.log_utils = log_utils
        self.log_utils.log.debug("Initializing Tile() class")
        self.level = Tile.level.ground
        # self.tile_details = f"Coordinates: ({self.x}, {self.y})\n"
        # self.tile_details += f"Grid node: ({self.grid_x}, {self.grid_y})\n"
        # self.tile_details += f"walkable: {self.GridNode.walkable}\n"
        self.tile_details += f"Units: {len(self.units)}\n"
        # self.tile_details += f"Unique Terrain: {self.GetUniqueTerrain()}\n"
        self.terrain = terrain
        self.tile_rect_settings = Tile.tile_rect_settings(grid_x, grid_y, tile_width, tile_height, self.terrain.background_color)

    def draw_tile(self, pgu):
        pgu.create_rect(self.tile_rect_settings)        

    def GetNodeWidth(self):
        return self.tile_rect_settings.width
