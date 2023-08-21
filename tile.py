import concurrent.futures
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

class Tiles(object):
    finder = None
    grid = None
    grid_matrix = None
    map_tiles = []
    terrain_water = None
    terrain_fire = None
    terrain_swamp = None
    terrain_forest = None
    terrain_fog = None
    terrain_rain = None
    terrain_lava = None
    terrain_mountain = None

    # rect(surface, color, rect, width=0, border_radius=0, 
    # border_top_left_radius=-1, border_top_right_radius=-1, 
    # border_bottom_left_radius=-1, border_bottom_right_radius=-1)
    class PGSettings:  
        log_utils = None
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
        border_color = None   
        border_sides = None  
        border_radius = 3
        border_width = Constants.BORDER_SIZE_PX
        terrain = None
        def __init__(self, log_utils, grid_x, grid_y, tile_width, tile_height, terrain=TerrainBasic()):
            self.log_utils = log_utils
            self.x = Constants.SIDE_PANEL_WIDTH_PX + (grid_x * tile_width)
            self.y = grid_y * tile_height
            self.grid_x = grid_x
            self.grid_y = grid_y
            self.background_color = terrain.background_color
            self.width = tile_width
            self.height = tile_height
            self.rect = pygame.Rect(self.x, self.y, tile_width, tile_height) 
            self.terrain = terrain
            #self.log_utils.log.info(f"Initializing PGSettings() class, coordinates: XY: ({self.x}x{self.y}), GRID: ({self.grid_x}x{self.grid_y})")

    def __init__(self):
        self.log_utils.log.info("Initializing Tiles() class")
        self.finder = AStarFinder()
        self.map_tiles = list[Tile]()
        
        # initialize our terrains
        self.terrain_water = TerrainWater()
        self.terrain_fire = TerrainFire()
        self.terrain_swamp = TerrainSwamp()
        self.terrain_forest = TerrainForest()
        self.terrain_fog = TerrainFog()
        self.terrain_rain = TerrainRain()
        self.terrain_lava = TerrainLava()
        self.terrain_mountain = TerrainMountain()

    def ConvertXYCoordToGridCoord(self, x, y):
        self.log_utils.log.info(f"ConvertXYCoordToGridCoord: enter")
        gridx = 0   
        if x > Constants.SIDE_PANEL_WIDTH_PX:
            gridx = int(x / Constants.TILE_WIDTH_PX)
        gridy = int(y / Constants.TILE_HEIGHT_PX)
        return gridx, gridy

    def load_grid(self, load_env = True):
        self.log_utils.log.info(f"load_grid: enter")

        self.map_tiles = self.create_tiles()
        
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
    

    # called as executor thread from create_tiles
    def thread_create_tiles(self, y):
        # self.log_utils.log.info(f"loop_tiles: enter, y range: {y}")
        tiles = []
        for grid_x in range(0, Constants.GAME_GRID_NODES):
            #self.log_utils.log.info(f"create_tiles grid_x % Complete: {round(((x_num_complete / Constants.GAME_GRID_NODES) * 100), 2)}")

            rs = self.PGSettings(self.log_utils, 
                                        grid_x, 
                                        y, 
                                        Constants.TILE_WIDTH_PX, 
                                        Constants.TILE_HEIGHT_PX)

            t = Tile(self.log_utils, rs)
            tiles.append(t)
            
        return tiles

    # 1. creates tiles
    def create_tiles(self):
        self.log_utils.log.info(f"create_tiles: enter")
        create_tiles_start = time.perf_counter()
        tiles = []
        loading_threads = []

        #num_workers = 100
        executor = concurrent.futures.ThreadPoolExecutor()        
        #executor._max_workers = num_workers
        self.log_utils.log.info(f"num_workers: {executor._max_workers}")
        #self.log_utils.log.info(f"create_tiles started with {num_workers} thread worker(s)")

        loading = False
        if not loading:
            for y in range(0, Constants.GAME_GRID_NODES):
                loading_threads.append(executor.submit(self.thread_create_tiles, y))
            loading = True # whether thread started

            # check if done..
            tiles_created = False
            while not tiles_created:
                for future in loading_threads:
                    state = future._state     
                    if state == "PENDING":
                        state = "INITIALIZING"
                    elif state == "RUNNING":
                        state = "LOADING"
                    elif state == "FINISHED":                        
                        result = future.result()
                        self.log_utils.log.info(f"Extending tile list with our thread result")
                        tiles.extend(result)
                        loading_threads.remove(future)
                        if len(loading_threads) <= 0:
                            tiles_created = True

        create_tiles_end = time.perf_counter()
        self.log_utils.log.info(f"create_tiles timings: {round((create_tiles_end - create_tiles_start), 2)} second(s)")
        return tiles

    # 2. create empty grid
    def get_empty_grid(self):
        self.log_utils.log.info(f"get_empty_grid: enter")
        get_empty_grid_start = time.perf_counter()
        max_y = Constants.GAME_GRID_NODES
        max_x = Constants.GAME_GRID_NODES
        self.log_utils.log.info(f"Generating grid based on {max_x}x{max_y} ({max_x*max_y} total nodes)")
        self.log_utils.log.info(f"Creating grid matrix")
        matrix = []
        for _ in range(0, max_y):
            x_line = []
            for _ in range(0, max_x):
                x_line.append(1)
            matrix.append(x_line)
        self.log_utils.log.info(f"Done creating grid matrix")
        self.log_utils.log.info(f"Creating grid")
        self.grid_matrix = matrix
        self.grid = Grid(matrix = self.grid_matrix)
        self.log_utils.log.info(f"Done creating grid")
        get_empty_grid_end = time.perf_counter()
        self.log_utils.log.info(f"get_empty_grid timings: {round((get_empty_grid_end - get_empty_grid_start), 2)} second(s)")
    
    # 3. adds in some terrain
    def add_terrain_to_tiles(self):
        self.log_utils.log.info(f"add_terrain_to_tiles: enter")
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
        self.create_terrain_globes( self.terrain_water, Constants.NUM_WATER_TILES)
        self.create_terrain_globes(self.terrain_mountain, Constants.NUM_MOUNTAIN_TILES)
        self.create_terrain_globes(self.terrain_swamp, Constants.NUM_SWAMP_TILES)
        self.create_terrain_globes(self.terrain_fire, Constants.NUM_FIRE_TILES)
        self.create_terrain_globes(self.terrain_forest, Constants.NUM_FOREST_TILES)
        self.create_terrain_globes(self.terrain_fog, Constants.NUM_FOG_TILES)
        self.create_terrain_globes(self.terrain_rain, Constants.NUM_RAIN_TILES)
        self.create_terrain_globes(self.terrain_lava, Constants.NUM_LAVA_TILES)

        create_terrain_end = time.perf_counter()
        self.log_utils.log.info(f"add_terrain_to_tiles timings: {round((create_terrain_end - create_terrain_start), 2)} second(s)")
        return self.map_tiles

    # 4. Update tiles
    def update_tiles(self):
        self.log_utils.log.debug(f"update_tiles: enter")
        update_tiles_start = time.perf_counter()
        total_nodes = len(self.map_tiles)

        for i in range(0, total_nodes):
            self.log_utils.log.debug(f"update_tiles: {i} of {total_nodes}")
            tile = self.map_tiles[i]
            node = self.grid.node(tile.tile_rect_settings.grid_x, tile.tile_rect_settings.grid_y)
            if tile.terrain.walkable == True:
                node.walkable = True
            else:
                node.walkable = False
            tile.grid_node = node
            tile.tile_details += f"walkable: {tile.grid_node.walkable}\n"
        update_tiles_end = time.perf_counter()
        self.log_utils.log.info(f"update_tiles timings: {round((update_tiles_end - update_tiles_start), 2)} second(s)")

    def GetUniqueTerrain(self):
        self.log_utils.log.info(f"GetUniqueTerrain: enter")
        tiles = [i for i in self.map_tiles if i.type != Tile.type.Basic]
        #self.log_utils.log.info(f"Unique tiles on map: {len(tiles)}")
        result = ""
        for tile in tiles:
            result += f"  {tile.type}, XY:({tile.x}x{tile.y}), Grid:({tile.tile_rect_settings.grid_x}x{tile.tile_rect_settings.grid_y})\n"
        return result
    
    def show_tile_details(self):     
        self.log_utils.log.info(f"show_grid: enter")
        show_grid_start = time.perf_counter()  
        self.log_utils.log.debug("Showing grid")   
        mouse_pos = self.update_mouse()   
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        grid_coords = self.ConvertXYCoordToGridCoord(mouse_x, mouse_y)
        self.log_utils.log.info(f"show_grid: getting details node")
        detail_tile = self.get_tile(grid_coords[0], grid_coords[1])
        self.update_mouse(tile=detail_tile)
        show_grid_end = time.perf_counter()
        self.log_utils.log.info(f"show_grid timings: {round((show_grid_end - show_grid_start), 2)} second(s)")

    def UpdateGridWithTerrain(self, grid):
        self.log_utils.log.info(f"UpdateGridWithTerrain: enter")
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
        self.log_utils.log.info(f"get_grid timings: {round((get_grid_end - get_grid_start), 2)} second(s)")
        return grid

    def get_tile(self, gridx, gridy):
        self.log_utils.log.debug(f"get_tile: enter")
        tiles = [i for i in self.map_tiles if gridx == i.tile_rect_settings.grid_x and gridy == i.tile_rect_settings.grid_y]
        tile = None
        if len(tiles) > 0:
            tile = tiles[0]
        else:
            self.log_utils.log.warn(f"No tile found for grid coordinates: ({gridx}x{gridy})")
        
        return tile

    # looks good for water?
    def create_terrain_globes(self, terrain_type, type_num):
        self.log_utils.log.info(f"create_terrain_globes: enter, terrain: {terrain_type.name}")
        start = time.perf_counter()
        num_placed = 0
        while num_placed < type_num:
            self.log_utils.log.debug(f"create_terrain_globes ({terrain_type.name}) % Complete: {round(((num_placed / type_num) * 100), 2)}")

            # start at a random point
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

            body_num_tiles = 0
            orig_rand_x = rand_x  
            orig_rand_y = rand_y 
            while body_num_tiles < body_size:
                # if num_placed >= type_num:
                #     break
                good_tile = False
                while not good_tile:
                    side = Constants.BorderSides.get_random_side()
                    previous_side = None
                    while side != previous_side:
                         # ensure we can't go same way twice
                        if previous_side == side:
                            continue
                        else:
                            previous_side = side

                        if side == "left":
                            rand_x += -1
                        elif side == "right":
                            rand_x += 1
                        elif side == "top":
                            rand_y += -1
                        elif side == "bottom":
                            rand_y += 1

                        if rand_x >= Constants.GAME_GRID_NODES or rand_x < 0:
                            rand_x = orig_rand_x
                            continue

                        if rand_y >= Constants.GAME_GRID_NODES or rand_y < 0: 
                            rand_y = orig_rand_y
                            continue

                        good_tile = True

                        tile = self.get_tile(rand_x, rand_y)
                        # self.log_utils.log.info(f"picked {terrain_type.name} tile placement: {tile.tile_rect_settings.grid_x}x{tile.tile_rect_settings.grid_y}")
                        tile.terrain = terrain_type
                        body_num_tiles += 1
                        break


            num_placed += body_num_tiles
            self.log_utils.log.info(f"Wanted {terrain_type.name} tiles for body size \"{size}\": {body_size}, got: {body_num_tiles}, num_complete: {num_placed}, type_num: {type_num}, % Complete: {round(((num_placed / type_num) * 100), 2)}")
        end = time.perf_counter()
        self.log_utils.log.info(f"create_terrain_globes ({terrain_type.name}): {round((end - start), 2)} second(s)")

    def GetTileByNodeCoord(self, gridx, gridy):
        self.log_utils.log.info(f"GetTileByNodeCoord: enter, grid: ({gridx}x{gridy})")
        tiles = [i for i in self.map_tiles if i.grid_x == gridx and i.grid_y == gridy]
        tile = None
        if len(tiles) > 0:
            tile = tiles[0]
        return tile            

    def DrawTerrainTiles(self, pgu):
        self.log_utils.log.debug(f"DrawTerrainTiles: enter")
        draw_terrain_start = time.perf_counter()
        for tile in self.map_tiles:
            if not self.show_grid:
                pygame.draw.rect(self.surface, tile.tile_rect_settings.background_color, tile.tile_rect_settings.rect)
            else:
                pygame.draw.rect(self.surface, Constants.Colors.NEON_GREEN, tile.tile_rect_settings.rect, Constants.GRID_BORDER_WIDTH_PX, border_radius=Constants.BORDER_RADIUS)
        draw_terrain_end = time.perf_counter()
        self.log_utils.log.debug(f"DrawTerrainTiles timings: {round((draw_terrain_end - draw_terrain_start), 2)} second(s)")

class Tile(object):
    level = None
    grid_node = None
    tile_rect_settings = None
    usable_tile = True
    tile_details = ""
    units = []
    terrain = None
    log_utils = None

    class level(Enum):
        subterranean = 0
        ground = 1
        air = 2
        sea = 3

    def __init__(self, log_utils, rs):
        self.log_utils = log_utils
        self.log_utils.log.debug("Initializing Tile() class")
        self.level = Tile.level.ground
        self.terrain = rs.terrain
        rs.text = f"({rs.grid_x}x{rs.grid_y})"
        self.tile_details = f"Coordinates: ({rs.x}, {rs.y})\n"
        self.tile_details += f"Grid node: ({rs.grid_x}, {rs.grid_y})\n"
        self.tile_details += f"Units: {len(self.units)}\n"
        self.tile_rect_settings = rs
        # self.tile_details += f"Unique Terrain: {self.GetUniqueTerrain()}\n"

    def draw_tile(self, border_only):
        self.pgu.create_rect(self.tile_rect_settings, border_only)        

    def GetNodeWidth(self):
        return self.tile_rect_settings.width
