import concurrent.futures
import time
import random
from uuid import uuid4
import pygame
from enum import Enum
from pathfinding.finder.a_star import AStarFinder, DiagonalMovement
from pathfinding.core.grid import Grid

# our stuff
from constants import Constants
from terrain import TerrainBasic, TerrainFire, TerrainFog, TerrainLava, TerrainMountain, TerrainRain, TerrainSwamp, TerrainWater, TerrainForest
from tileutility import TileUtility

class Tiles(object):
    finder = None
    grid = None
    grid_matrix = None
    map_tiles = []
    tu = None
    terrain_water = None
    terrain_fire = None
    terrain_swamp = None
    terrain_forest = None
    terrain_fog = None
    terrain_rain = None
    terrain_lava = None
    terrain_mountain = None
    details_node = None # used to prevent refreshing tile unless we need to
    details_node_coord = None # used to prevent refreshing tile unless we need to
    mouse_hover_time = time.time()

    def __init__(self):
        self.log_utils.log.info("Initializing Tiles() class")
        self.finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        self.tu = TileUtility(self.log_utils)
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

    def load_grid(self, load_env = True):
        self.log_utils.log.debug(f"load_grid: enter")

        self.map_tiles = self.create_tiles()
        
        # ensure map meets basic criterias (NOT IMPLEMENTED)
        usable_map = False   

        while not usable_map:
            # generate our obstacles
            if load_env:
                self.add_terrain_to_tiles()

                self.create_grid()

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
    def create_tiles(self):
        self.log_utils.log.debug(f"create_tiles: enter")
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

    # 2. adds in some terrain
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
        self.create_terrain_globes(self.terrain_water, Tile.level.ground, Constants.NUM_WATER_TILES)
        self.create_terrain_globes(self.terrain_mountain, Tile.level.ground,Constants.NUM_MOUNTAIN_TILES)
        self.create_terrain_globes(self.terrain_swamp, Tile.level.ground, Constants.NUM_SWAMP_TILES)
        self.create_terrain_globes(self.terrain_fire, Tile.level.ground, Constants.NUM_FIRE_TILES)
        self.create_terrain_globes(self.terrain_forest, Tile.level.ground, Constants.NUM_FOREST_TILES)
        self.create_terrain_globes(self.terrain_fog, Tile.level.ground, Constants.NUM_FOG_TILES)
        self.create_terrain_globes(self.terrain_rain, Tile.level.ground, Constants.NUM_RAIN_TILES)
        self.create_terrain_globes(self.terrain_lava, Tile.level.ground, Constants.NUM_LAVA_TILES)

        create_terrain_end = time.perf_counter()
        self.log_utils.log.info(f"add_terrain_to_tiles timings: {round((create_terrain_end - create_terrain_start), 2)} second(s)")
        return self.map_tiles

    def create_grid_matrix_thread(self, y_gd):
        self.log_utils.log.debug(f"create_grid_matrix_thread: enter")
        x_line = []
        for x_gd in range(0, Constants.GAME_GRID_NODES):
            # get our tile so we can see terrain type
            tile = self.get_tile(x_gd, y_gd)
            x_line.append(tile.terrain.cost) # this needs to be cost
        self.log_utils.log.debug(f"create_grid_matrix_thread: exit")
        return x_line

    # called as executor thread from create_tiles
    def thread_create_tiles(self, y_gd):
        # self.log_utils.log.info(f"loop_tiles: enter, y range: {y}")
        tiles = []
        for x_gd in range(0, Constants.GAME_GRID_NODES):
            #self.log_utils.log.info(f"create_tiles x_gd % Complete: {round(((x_num_complete / Constants.GAME_GRID_NODES) * 100), 2)}")
            tiles.append(self.create_tile(x_gd=x_gd, y_gd=y_gd))
        return tiles
    
    # 3. create grid
    def create_grid(self):
        self.log_utils.log.info(f"create_grid: enter")
        get_empty_grid_start = time.perf_counter()
        max_y = Constants.GAME_GRID_NODES
        max_x = Constants.GAME_GRID_NODES
        self.log_utils.log.info(f"Generating grid based on {max_x}x{max_y} ({max_x*max_y} total nodes)")
        self.log_utils.log.info(f"Creating grid matrix")
        matrix = []
        loading_threads = []        
        executor = concurrent.futures.ThreadPoolExecutor()    
        #num_workers = 100    
        #executor._max_workers = num_workers
        self.log_utils.log.info(f"create_grid matrix num_workers: {executor._max_workers}")
        get_empty_grid_matrix_start = time.perf_counter()
        loading = False
        if not loading:
            for y in range(0, Constants.GAME_GRID_NODES):
                loading_threads.append(executor.submit(self.create_grid_matrix_thread, y))
                loading = True # whether thread started
        get_empty_grid_matrix_end = time.perf_counter()
        self.log_utils.log.debug(f"create_grid matrix timings: {round((get_empty_grid_matrix_end - get_empty_grid_matrix_start), 2)} second(s)")

        # wait until done..
        grid_created = False
        while not grid_created:
            for future in loading_threads:
                state = future._state     
                if state == "PENDING":
                    state = "INITIALIZING"
                elif state == "RUNNING":
                    state = "LOADING"
                elif state == "FINISHED":                        
                    result = future.result()
                    self.log_utils.log.info(f"Extending grid matrix list with our thread result")
                    matrix.append(result)
                    loading_threads.remove(future)
                    if len(loading_threads) <= 0:
                        grid_created = True
        self.log_utils.log.info(f"Done creating grid matrix")
        self.log_utils.log.info(f"matrix: {matrix}")
        self.log_utils.log.info(f"Creating grid")
        self.grid_matrix = matrix
        get_pathfinding_grid_start = time.perf_counter()
        self.grid = Grid(matrix = self.grid_matrix)
        get_pathfinding_grid_end = time.perf_counter()
        self.log_utils.log.info(f"Done creating grid")
        self.log_utils.log.debug(f"get_pathfinding_grid_start matrix timings: {round((get_pathfinding_grid_end - get_pathfinding_grid_start), 2)} second(s)")

        self.log_utils.log.info(f"Associating grid with tiles")
        tiles = self.map_tiles[:]
        for tile in tiles:
            tile.grid_node = self.grid.node(tile.primary_rs.x_gd, tile.primary_rs.y_gd)
        self.map_tiles = tiles[:]

        self.log_utils.log.info(f"Done associating grid")
        get_empty_grid_end = time.perf_counter()
        self.log_utils.log.info(f"create_grid timings: {round((get_empty_grid_end - get_empty_grid_start), 2)} second(s)")

    def show_tile_details(self):     
        self.log_utils.log.debug(f"show_tile_details: enter")        
        mouse_pos = self.update_mouse()   
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        grid_coords = self.tu.ConvertXYCoordToGridCoord(mouse_x, mouse_y)
        current_time = time.time()
        if self.details_node != grid_coords and current_time - self.mouse_hover_time > 5:
            self.mouse_hover_time = time.time()
            show_grid_start = time.perf_counter()  
            self.details_node_coord = grid_coords
            self.details_node = self.get_tile(grid_coords[0], grid_coords[1])
            show_grid_end = time.perf_counter()
            self.log_utils.log.info(f"show_tile_details: exit, timings: {round((show_grid_end - show_grid_start), 2)} second(s)")
            
        if self.details_node is not None:
            self.create_rect(self.details_node.details_rs, border_only=False)  

    def get_tile(self, gridx, gridy):
        self.log_utils.log.debug(f"get_tile: enter")
        tiles = [i for i in self.map_tiles if gridx == i.primary_rs.x_gd and gridy == i.primary_rs.y_gd]
        tile = None
        if len(tiles) > 0:
            tile = tiles[0]
        # else:
        #     self.log_utils.log.warn(f"No tile found for grid coordinates: ({gridx}x{gridy})")
        
        return tile

    def update_tile(self, newtile):
        newtiles = self.map_tiles[:]
        for tile in newtiles:
            if tile.primary_rs.x_gd == newtile.primary_rs.x_gd and tile.primary_rs.y_gd == newtile.primary_rs.y_gd:
                tile = newtile
                break
        self.map_tiles = newtiles[:]

    # looks good for water?
    def create_terrain_globes(self, terrain_type, level, num_terrain_needed):
        self.log_utils.log.info(f"create_terrain_globes: enter, terrain: {terrain_type.name}")
        start = time.perf_counter()
        num_placed = 0
        while num_placed < num_terrain_needed:
            self.log_utils.log.debug(f"create_terrain_globes ({terrain_type.name}) % Complete: {round(((num_placed / num_terrain_needed) * 100), 2)}")

            # start at a random point
            rand_x_gd = random.randrange(0, Constants.GAME_GRID_NODES)
            rand_y_gd = random.randrange(0, Constants.GAME_GRID_NODES)

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
            orig_rand_x = rand_x_gd  
            orig_rand_y = rand_y_gd 
            while body_num_tiles < body_size and num_placed < num_terrain_needed:
                # if num_placed >= type_num:
                #     break
                good_tile = False
                while not good_tile and num_placed < num_terrain_needed:
                    side = Constants.BorderSides.get_random_side()
                    previous_side = None
                    while side != previous_side and num_placed < num_terrain_needed:
                         # ensure we can't go same way twice
                        if previous_side == side:
                            continue
                        else:
                            previous_side = side

                        if side == "left":
                            rand_x_gd += -1
                        elif side == "right":
                            rand_x_gd += 1
                        elif side == "top":
                            rand_y_gd += -1
                        elif side == "bottom":
                            rand_y_gd += 1

                        if rand_x_gd >= Constants.GAME_GRID_NODES or rand_x_gd < 0:
                            rand_x_gd = orig_rand_x
                            continue

                        if rand_y_gd >= Constants.GAME_GRID_NODES or rand_y_gd < 0: 
                            rand_y_gd = orig_rand_y
                            continue

                        good_tile = True

                        # (self, terrain, level, x_gd, y_gd):
                        self.update_terrain(terrain_type, level, rand_x_gd, rand_y_gd)
                        body_num_tiles += 1
                        num_placed += 1
                        break            
            self.log_utils.log.debug(f"Wanted {terrain_type.name} tiles for body size \"{size}\": {body_size}, got: {body_num_tiles}, num_placed: {num_placed} or {num_terrain_needed}, % Complete: {round(((num_placed / num_terrain_needed) * 100), 2)}")
        end = time.perf_counter()
        self.log_utils.log.info(f"create_terrain_globes ({terrain_type.name}): {round((end - start), 2)} second(s)")

    def GetTileByNodeCoord(self, gridx, gridy):
        self.log_utils.log.info(f"GetTileByNodeCoord: enter, grid: ({gridx}x{gridy})")
        tiles = [i for i in self.map_tiles if i.x_gd == gridx and i.y_gd == gridy]
        tile = None
        if len(tiles) > 0:
            tile = tiles[0]
        return tile            

    def update_terrain(self, terrain, level, x_gd, y_gd):
        self.log_utils.log.debug(f"update_terrain: enter: ({x_gd}x{y_gd}) to: {terrain.name}")
        update_terrain_start = time.perf_counter()
        tile = self.get_tile(x_gd, y_gd)
        tile.terrain = terrain
        tile.primary_rs.background_color = terrain.background_color
        xy_coords = self.tu.ConvertGridCoordToXYCoord(x_gd, y_gd)
        tile.details_rs.text = tile.update_details_text(xy_coords[0], xy_coords[0], x_gd, y_gd, terrain, level.name)
        self.update_tile(tile)        
        update_terrain_end = time.perf_counter()
        self.log_utils.log.debug(f"update_terrain: exit, timings: {round((update_terrain_end - update_terrain_start), 2)} second(s)")

    def draw_terrain_tiles(self, pgu):
        self.log_utils.log.info(f"draw_terrain_tiles: enter")
        draw_terrain_start = time.perf_counter()

        for tile in self.map_tiles:
            if not self.show_grid:
                pygame.draw.rect(self.surface, tile.primary_rs.background_color, tile.primary_rs.rect)
            else:
                if tile.grid_node.walkable:
                    pygame.draw.rect(self.surface,
                                     Constants.Colors.NEON_GREEN,
                                     tile.primary_rs.rect,
                                     Constants.GRID_BORDER_WIDTH_PX, 
                                     border_top_left_radius=Constants.BORDER_RADIUS,
                                     border_top_right_radius=Constants.BORDER_RADIUS,
                                     border_bottom_left_radius=Constants.BORDER_RADIUS, 
                                     border_bottom_right_radius=Constants.BORDER_RADIUS
                    )
                else:
                    if tile.terrain.walkable:
                        pygame.draw.rect(self.surface, 
                                        Constants.Colors.NEON_GREEN,
                                        tile.primary_rs.rect, 
                                        Constants.GRID_BORDER_WIDTH_PX,
                                        border_top_left_radius=0,
                                        border_top_right_radius=0,
                                        border_bottom_left_radius=0, 
                                        border_bottom_right_radius=0)
                    else:
                        pygame.draw.rect(self.surface, 
                                        Constants.Colors.BURNT_ORANGE,
                                        tile.primary_rs.rect, 
                                        Constants.GRID_BORDER_WIDTH_PX,
                                        border_top_left_radius=0,
                                        border_top_right_radius=0,
                                        border_bottom_left_radius=0, 
                                        border_bottom_right_radius=0)

            # add text
            unit_text = None
            if tile.primary_rs.text is not None:  
                if tile.primary_rs.font_color is None:
                    tile.primary_rs.font_color = Constants.Colors.NEON_GREEN

                if tile.primary_rs.font_name is not None:
                    if tile.primary_rs.font_size is None:
                        tile.primary_rs.font_size == Constants.FONT_SIZE_DEFAULT_PX                    
                    tile.primary_rs.font = pygame.font.SysFont(tile.primary_rs.font_name, tile.primary_rs.font_size)
                elif tile.primary_rs.font is None:
                    tile.primary_rs.font =  self.font

                if "\n" in tile.primary_rs.text:
                    self.place_text(tile.primary_rs.text, tile.primary_rs.rect.width, tile.primary_rs.x, tile.primary_rs.y, 
                                    font=tile.primary_rs.font, color=tile.primary_rs.font_color)
                else:
                    unit_text = tile.primary_rs.font.render(tile.primary_rs.text, True, tile.primary_rs.font_color)                    
                    rect = unit_text.get_rect(x=tile.primary_rs.x, y=tile.primary_rs.y)
                    rect.center = tile.primary_rs.rect.center
                    self.surface.blit(unit_text, rect) # self.surface.blit(tile.primary_rs.rect, unit_text)
                    
        draw_terrain_end = time.perf_counter()
        self.log_utils.log.info(f"draw_terrain_tiles timings: {round((draw_terrain_end - draw_terrain_start), 2)} second(s)")

    # takes either:
    # 1. an RectSettings object
    # 2. xy coords
    # 3. x_gd,y_gd coords
    def create_tile(self, rs=None, x=None, y=None, x_gd=None, y_gd=None, terrain=None, text=None):
        self.log_utils.log.debug("create_tile: enter")
        tile = Tile(self.log_utils, 
                    x_gd=x_gd, 
                    y_gd=y_gd,
                    terrain=terrain,
                    text=text)    
        self.log_utils.log.debug("create_tile: exit")
        return tile
        
class Tile(object):
    level = None
    grid_node = None
    primary_rs = None # main grid
    details_rs = None # for the details node
    usable_tile = True
    tile_details = ""
    units = []
    terrain = None
    log_utils = None
    tu = None

    # rect(surface, color, rect, width=0, border_radius=0, 
    # border_top_left_radius=-1, border_top_right_radius=-1, 
    # border_bottom_left_radius=-1, border_bottom_right_radius=-1)
    class RectSettings:  
        log_utils = None
        x = None
        y = None  
        x_gd = None
        y_gd = None    
        width_px = Constants.TILE_WIDTH_PX
        height_px = Constants.TILE_HEIGHT_PX
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
        def __init__(self, log_utils, x_gd, y_gd, x, y, text="", terrain=None, background_color=None, border_radius=None, font_size=None, width_px=None, height_px=None):
            self.log_utils = log_utils
            self.x = x
            self.y = y
            self.x_gd = x_gd
            self.y_gd = y_gd
            self.text = text

            if border_radius is not None:
                self.border_radius = border_radius

            if font_size is not None:
                self.font_size = font_size

            if terrain is None:
                self.background_color = Constants.Colors.DARK_PURPLE
            else:
                self.background_color = terrain.background_color

            # overwritten by grid
            if width_px is None:
                width_px = self.width_px

            if height_px is None:
                height_px = self.height_px

            # override with supplied background
            if background_color is not None:
                self.background_color = background_color
            self.rect = pygame.Rect(self.x, self.y, width_px, height_px) 
            self.terrain = terrain
            self.log_utils.log.debug(f"Initializing PGSettings() class, coordinates: XY: ({self.x}x{self.y}), GRID: ({self.x_gd}x{self.y_gd})")

    class level(Enum):
        subterranean = 0
        ground = 1
        air = 2
        sea = 3

    def __init__(self, log_utils, rs=None, x=None, y=None, x_gd=None, y_gd=None, terrain=None, text=None):
        self.log_utils = log_utils
        self.log_utils.log.debug("Initializing new Tile()")
        self.tu = TileUtility(self.log_utils)
        self.level = Tile.level.ground # not used, may allow "sky tiles later"

        # if rs is none than we need either xy or grid xy coords
        if rs is None:
            if (x is None and y is None) and (x_gd is None and y_gd) is None:
                raise "nope!"
            
            # generate x_gd and y_gd if we got xy coords
            if (x is not None and y is not None) and (x_gd is None and y_gd is None):
                grid_coords = self.tu.ConvertXYCoordToGridCoord(x, y)
                x_gd = grid_coords[0]
                y_gd = grid_coords[1]

            if x is None and y is None:
                xy_coords = self.tu.ConvertGridCoordToXYCoord(x_gd, y_gd)
                x = xy_coords[0]
                y = xy_coords[1]

            # check terrain
            if terrain is None:
                self.terrain = TerrainBasic()

            # check text
            if text is None:
                text=f"({x}x{y})\n({x_gd}x{y_gd})"

            rs = self.RectSettings(self.log_utils, 
                                        x_gd=x_gd, 
                                        y_gd=y_gd, 
                                        x=x,
                                        y=y,
                                        terrain=self.terrain)
            
            # this is when the grid mode is enabled
            tile_details = self.update_details_text(x, y, x_gd, y_gd, self.terrain, self.level.name)
            details_spacer = 100
            new_x_px = x + details_spacer
            new_y_px = y
            new_x_gd = x_gd,
            new_y_gd = y_gd, 
            new_text = tile_details
            new_background_color = Constants.Colors.GRID_DETAILS_COLOR
            new_border_radius = 25
            new_font_size = Constants.FONT_SIZE_GRID_DETAILS
            details_rs = self.RectSettings(self.log_utils, 
                                           text=new_text, 
                                           x_gd=new_x_gd, 
                                           y_gd=new_y_gd, 
                                           x=new_x_px, 
                                           y=new_y_px, 
                                           background_color=new_background_color, 
                                           border_radius=new_border_radius, 
                                           font_size=new_font_size,
                                           width_px=Constants.GRID_DETAILS_WIDTH_PX,
                                           height_px=Constants.GRID_DETAILS_HEIGHT_PX)
            details_rs.font_size = 12
        self.primary_rs = rs
        self.details_rs = details_rs

    def update_details_text(self, x, y, x_gd, y_gd, terrain, level_name):
        tile_details = f"Coordinates: ({x}, {y})\n"
        tile_details += f"Grid node: ({x_gd}, {y_gd})\n"
        tile_details += f"Terrain: {terrain.name}\n"
        tile_details += f"Level: {level_name}\n"
        tile_details += f"Walkable: {terrain.walkable}\n"
        tile_details += f"Cost: {terrain.cost}\n"
        return tile_details

    def draw_tile(self, border_only):
        self.pgu.create_rect(self.primary_rs, border_only)        

    def GetNodeWidth(self):
        return self.primary_rs.width
