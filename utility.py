import random
from time import sleep
import time
import traceback
import pygame

# our stuff
from constants import Constants
from pygameutility import PygameUtilities
from names import Names
from unit import Unit
from tile import Tiles, Tile
from environment import Environment

class Utility:
    screen_border_rs = None # border
    sp_menu_rs = None # side panel
    spawn_rs = None # spawn point
    MenuTiles = [] 
    spawn_points = None
    obstacles = None  

    def __init__(self):
        self.MapTiles = Tiles()

    def create_border(self, pgu):
        if self.screen_border_rs is None:
            # create border
            self.screen_border_rs = pgu.RectSettings()
            self.screen_border_rs.Width = Constants.SCREEN_WIDTH
            self.screen_border_rs.Height = Constants.SCREEN_HEIGHT
            self.screen_border_rs.BgColor = Constants.Colors.ROYAL_PURPLE
            self.screen_border_rs.BorderColor = Constants.Colors.AQUA
            self.screen_border_rs.BorderWidth = Constants.BORDER_SIZE
        self.screen_border_rs = pgu.create_rect(self.screen_border_rs, ignore_side_panel=True, really_draw=True)

    # creates section of the map free for units spawn
    def draw_spawn_points(self, pgu, really_draw=True):
        pgu.update_mouse()

        if self.spawn_rs is None:
            spawn_point_rect = pgu.RectSettings()
            spawn_point_rect.BgColor = Constants.Colors.SPAWN_COLOR
            spawn_point_rect.FontSize = Constants.SP_BUTTON_TEXT_SIZE
            spawn_point_rect.BorderColor = Constants.Colors.PLUM
            spawn_point_rect.Rect = pygame.Rect(Constants.SPAWN_X, Constants.SPAWN_Y, Constants.SPAWN_WIDTH, Constants.SPAWN_HEIGHT) 
            self.spawn_rs = spawn_point_rect
        self.spawn_rs = pgu.create_rect(self.spawn_rs, ignore_side_panel=True, really_draw=really_draw)

    def create_water_tiles(self, pgu, gu, obstacles):
        start = time.perf_counter()
        num_tiles = 0
        for num_complete in range(Constants.NUM_WATER_TILES):
            print(f"create_water_tiles % Complete: {round(((num_complete / Constants.NUM_WATER_TILES) * 100), 2)}")
            num_tiles_remaining = Constants.NUM_WATER_TILES

            # start at a random point
            rand_node = random.choice(gu.Grid.nodes)
            rand_cord = random.choice(rand_node)
            grid_x = rand_cord.x
            grid_y = rand_cord.y

            # chose a random water size
            size = Constants.DensityTypes.get_random_size()
            density = 0
            if size == "tiny":
                density = random.randint(1, 2)
            elif size == "small":
                density = random.randint(2, 6)
            elif size == "medium":
                density = random.randint(6, 10)
            elif size == "large":
                density = random.randint(10, 30)
            elif size == "huge":
                density = random.randint(30, 100)

            while num_tiles <= density:
                side = Constants.BorderSides.get_random_side()
                if side == "left":
                    grid_x += -1
                elif side == "right":
                    grid_x += 1
                elif side == "top":
                    grid_y += -1
                elif side == "bottom":
                    grid_y += 1

                pixel_x = int(grid_x * Constants.UNIT_SIZE)
                pixel_y = int(grid_y * Constants.UNIT_SIZE)
                rect = pygame.Rect(pixel_x, pixel_y, Constants.UNIT_SIZE, Constants.UNIT_SIZE)
                collisions = [i["rect"] for i in obstacles]
                item = rect.collidelist(collisions)
                if item == -1:
                    print(f"picked water tile placement: {pixel_x}x{pixel_y}")

                    t = Tile()
                    t.Type = Environment.TileType.Water
                    t.Walkable = False
                    t.x = pixel_x
                    t.y = pixel_y
                    t.RectSettings = pgu.RectSettings()
                    t.RectSettings.Rect = rect
                    obstacles.append(t)
                    self.MapTiles.append(t)
                    num_tiles += 1
                    num_tiles_remaining -= 1

                if num_tiles_remaining <= 0:
                    break

            print(f"num water tiles placed for density: {density}: {num_tiles}")
            if num_tiles_remaining <= 0:
                break

            # start next "range" of water
            num_tiles = 0

        end = time.perf_counter()
        print(f"create_water_tiles: {round(60 - (end - start), 2)} second(s)")
        return obstacles, gu

    def create_mountain_tiles(self, grid, obstacles):
        start = time.perf_counter()
        num_tiles = 0

        for num_complete in range(Constants.NUM_MOUNTAIN_TILES):
            print(f"create_mountain_tiles % Complete: {round(((num_complete / Constants.NUM_MOUNTAIN_TILES) * 100), 2)}")
            # start at a random point
            rand_node = random.choice(grid.nodes)
            rand_cord = random.choice(rand_node)
            x = rand_cord.x
            y = rand_cord.y

            # chose a random water size
            size = Constants.DensityTypes.get_random_size()
            density = 0
            if size == "tiny":
                density = random.randint(1, 2)
            elif size == "small":
                density = random.randint(2, 6)
            elif size == "medium":
                density = random.randint(6, 10)
            elif size == "large":
                density = random.randint(10, 30)
            elif size == "huge":
                density = random.randint(30, 100)

            while num_tiles <= density:
                side = Constants.BorderSides.get_random_side()
                if side == "left":
                    x += -1
                elif side == "right":
                    x += 1
                elif side == "top":
                    y += -1
                elif side == "bottom":
                    y += 1

                final_x = x * Constants.UNIT_SIZE
                final_y = y * Constants.UNIT_SIZE
                rect = pygame.Rect(final_x, final_y, Constants.UNIT_SIZE, Constants.UNIT_SIZE)
                collisions = [i["rect"] for i in obstacles]
                item = rect.collidelist(collisions)
                if item == -1:
                    print(f"picked mountain tile placement: {final_x}x{final_y}")
                    obs_item = dict(name="mountain", rect=rect, walkable=False, coord=(final_x,final_y))
                    obstacles.append(obs_item)
                    self.MapTiles.append(obs_item)
                    num_tiles += 1
            num_tiles = 0
        end = time.perf_counter()
        print(f"create_mountain_tiles: {round(60 - (end - start), 2)} second(s)")
        return obstacles, grid

    def create_fire_tiles(self, grid, obstacles):
        start = time.perf_counter()
        num_tiles = 0

        for num_complete in range(Constants.NUM_FIRE_TILES):
            print(f"create_fire_tiles % Complete: {round(((num_complete / Constants.NUM_FIRE_TILES) * 100), 2)}")
            # start at a random point
            rand_node = random.choice(grid.nodes)
            rand_cord = random.choice(rand_node)
            x = rand_cord.x
            y = rand_cord.y

            # chose a random water size
            size = Constants.DensityTypes.get_random_size()
            density = 0
            if size == "tiny":
                density = random.randint(1, 2)
            elif size == "small":
                density = random.randint(2, 6)
            elif size == "medium":
                density = random.randint(6, 10)
            elif size == "large":
                density = random.randint(10, 30)
            elif size == "huge":
                density = random.randint(30, 100)

            while num_tiles <= density:
                side = Constants.BorderSides.get_random_side()
                if side == "left":
                    x += -1
                elif side == "right":
                    x += 1
                elif side == "top":
                    y += -1
                elif side == "bottom":
                    y += 1

                final_x = x * Constants.UNIT_SIZE
                final_y = y * Constants.UNIT_SIZE
                rect = pygame.Rect(final_x, final_y, Constants.UNIT_SIZE, Constants.UNIT_SIZE)
                collisions = [i["rect"] for i in obstacles]
                item = rect.collidelist(collisions)
                if item == -1:
                    print(f"picked fire tile placement: {final_x}x{final_y}")
                    obs_item = dict(name="fire", rect=rect, walkable=True, coord=(final_x,final_y))
                    obstacles.append(obs_item)
                    self.MapTiles.append(obs_item)
                    num_tiles += 1
            num_tiles = 0
        end = time.perf_counter()
        print(f"create_fire_tiles: {round(60 - (end - start), 2)} second(s)")
        return obstacles, grid

    def create_forest_tiles(self, grid, obstacles):
        start = time.perf_counter()
        num_tiles = 0

        for num_complete in range(Constants.NUM_FOREST_TILES):
            print(f"create_forest_tiles % Complete: {round(((num_complete / Constants.NUM_FOREST_TILES) * 100), 2)}")
            # start at a random point
            rand_node = random.choice(grid.nodes)
            rand_cord = random.choice(rand_node)
            x = rand_cord.x
            y = rand_cord.y

            # chose a random water size
            size = Constants.DensityTypes.get_random_size()
            density = 0
            if size == "tiny":
                density = random.randint(1, 2)
            elif size == "small":
                density = random.randint(2, 6)
            elif size == "medium":
                density = random.randint(6, 10)
            elif size == "large":
                density = random.randint(10, 30)
            elif size == "huge":
                density = random.randint(30, 100)

            while num_tiles <= density:
                side = Constants.BorderSides.get_random_side()
                if side == "left":
                    x += -1
                elif side == "right":
                    x += 1
                elif side == "top":
                    y += -1
                elif side == "bottom":
                    y += 1

                final_x = x * Constants.UNIT_SIZE
                final_y = y * Constants.UNIT_SIZE
                rect = pygame.Rect(final_x, final_y, Constants.UNIT_SIZE, Constants.UNIT_SIZE)
                collisions = [i["rect"] for i in obstacles]
                item = rect.collidelist(collisions)
                if item == -1:
                    print(f"picked forest tile placement: {final_x}x{final_y}")
                    obs_item = dict(name="forest", rect=rect, walkable=False, coord=(final_x,final_y))
                    obstacles.append(obs_item)
                    self.MapTiles.append(obs_item)
                    num_tiles += 1
            num_tiles = 0
        end = time.perf_counter()
        print(f"create_forest_tiles: {round(60 - (end - start), 2)} second(s)")
        return obstacles, grid

    def create_fog_tiles(self, grid, obstacles):
        start = time.perf_counter()
        num_tiles = 0

        for num_complete in range(Constants.NUM_FOG_TILES):
            print(f"create_fog_tiles % Complete: {round(((num_complete / Constants.NUM_FOG_TILES) * 100), 2)}")
            # start at a random point
            rand_node = random.choice(grid.nodes)
            rand_cord = random.choice(rand_node)
            x = rand_cord.x
            y = rand_cord.y

            # chose a random water size
            size = Constants.DensityTypes.get_random_size()
            density = 0
            if size == "tiny":
                density = random.randint(1, 2)
            elif size == "small":
                density = random.randint(2, 6)
            elif size == "medium":
                density = random.randint(6, 10)
            elif size == "large":
                density = random.randint(10, 30)
            elif size == "huge":
                density = random.randint(30, 100)

            while num_tiles <= density:
                side = Constants.BorderSides.get_random_side()
                if side == "left":
                    x += -1
                elif side == "right":
                    x += 1
                elif side == "top":
                    y += -1
                elif side == "bottom":
                    y += 1

                final_x = x * Constants.UNIT_SIZE
                final_y = y * Constants.UNIT_SIZE
                rect = pygame.Rect(final_x, final_y, Constants.UNIT_SIZE, Constants.UNIT_SIZE)
                collisions = [i["rect"] for i in obstacles]
                item = rect.collidelist(collisions)
                if item == -1:
                    print(f"picked fog tile placement: {final_x}x{final_y}")
                    obs_item = dict(name="fog", rect=rect, walkable=True, coord=(final_x,final_y))
                    obstacles.append(obs_item)
                    self.MapTiles.append(obs_item)
                    num_tiles += 1
            num_tiles = 0
        end = time.perf_counter()
        print(f"create_fog_tiles: {round(60 - (end - start), 2)} second(s)")
        return obstacles, grid
    
    def create_rain_tiles(self, grid, obstacles):
        start = time.perf_counter()
        num_tiles = 0

        for num_complete in range(Constants.NUM_RAIN_TILES):
            print(f"create_rain_tiles % Complete: {round(((num_complete / Constants.NUM_RAIN_TILES) * 100), 2)}")
            # start at a random point
            rand_node = random.choice(grid.nodes)
            rand_cord = random.choice(rand_node)
            x = rand_cord.x
            y = rand_cord.y

            # chose a random water size
            size = Constants.DensityTypes.get_random_size()
            density = 0
            if size == "tiny":
                density = random.randint(1, 2)
            elif size == "small":
                density = random.randint(2, 6)
            elif size == "medium":
                density = random.randint(6, 10)
            elif size == "large":
                density = random.randint(10, 30)
            elif size == "huge":
                density = random.randint(30, 100)

            while num_tiles <= density:
                side = Constants.BorderSides.get_random_side()
                if side == "left":
                    x += -1
                elif side == "right":
                    x += 1
                elif side == "top":
                    y += -1
                elif side == "bottom":
                    y += 1

                final_x = x * Constants.UNIT_SIZE
                final_y = y * Constants.UNIT_SIZE
                rect = pygame.Rect(final_x, final_y, Constants.UNIT_SIZE, Constants.UNIT_SIZE)
                collisions = [i["rect"] for i in obstacles]
                item = rect.collidelist(collisions)
                if item == -1:
                    print(f"picked rain tile placement: {final_x}x{final_y}")
                    obs_item = dict(name="rain", rect=rect, walkable=True, coord=(final_x,final_y))
                    obstacles.append(obs_item)
                    self.MapTiles.append(obs_item)
                    num_tiles += 1
            num_tiles = 0
        end = time.perf_counter()
        print(f"create_rain_tiles: {round(60 - (end - start), 2)} second(s)")
        return obstacles, grid
    
    def create_lava_tiles(self, grid, obstacles):
        start = time.perf_counter()
        num_tiles = 0

        for num_complete in range(Constants.NUM_LAVA_TILES):
            print(f"create_lava_tiles % Complete: {round(((num_complete / Constants.NUM_LAVA_TILES) * 100), 2)}")
            # start at a random point
            rand_node = random.choice(grid.nodes)
            rand_cord = random.choice(rand_node)
            x = rand_cord.x
            y = rand_cord.y

            # chose a random water size
            size = Constants.DensityTypes.get_random_size()
            density = 0
            if size == "tiny":
                density = random.randint(1, 2)
            elif size == "small":
                density = random.randint(2, 6)
            elif size == "medium":
                density = random.randint(6, 10)
            elif size == "large":
                density = random.randint(10, 30)
            elif size == "huge":
                density = random.randint(30, 100)

            while num_tiles <= density:
                side = Constants.BorderSides.get_random_side()
                if side == "left":
                    x += -1
                elif side == "right":
                    x += 1
                elif side == "top":
                    y += -1
                elif side == "bottom":
                    y += 1

                final_x = x * Constants.UNIT_SIZE
                final_y = y * Constants.UNIT_SIZE
                rect = pygame.Rect(final_x, final_y, Constants.UNIT_SIZE, Constants.UNIT_SIZE)
                collisions = [i["rect"] for i in obstacles]
                item = rect.collidelist(collisions)
                if item == -1:
                    print(f"picked lava tile placement: {final_x}x{final_y}")
                    obs_item = dict(name="lava", rect=rect, walkable=False, coord=(final_x,final_y))
                    obstacles.append(obs_item)
                    self.MapTiles.append(obs_item)
                    num_tiles += 1
            num_tiles = 0
        end = time.perf_counter()
        print(f"create_lava_tiles: {round(60 - (end - start), 2)} second(s)")
        return obstacles, grid
    
    def create_swamp_tiles(self, grid, obstacles):
        start = time.perf_counter()
        num_tiles = 0

        for num_complete in range(Constants.NUM_SWAMP_TILES):
            print(f"create_swamp_tiles % Complete: {round(((num_complete / Constants.NUM_SWAMP_TILES) * 100), 2)}")
            # start at a random point
            rand_node = random.choice(grid.nodes)
            rand_cord = random.choice(rand_node)
            x = rand_cord.x
            y = rand_cord.y

            # chose a random water size
            size = Constants.DensityTypes.get_random_size()
            density = 0
            if size == "tiny":
                density = random.randint(1, 2)
            elif size == "small":
                density = random.randint(2, 6)
            elif size == "medium":
                density = random.randint(6, 10)
            elif size == "large":
                density = random.randint(10, 30)
            elif size == "huge":
                density = random.randint(30, 100)

            while num_tiles <= density:
                side = Constants.BorderSides.get_random_side()
                if side == "left":
                    x += -1
                elif side == "right":
                    x += 1
                elif side == "top":
                    y += -1
                elif side == "bottom":
                    y += 1

                final_x = x * Constants.UNIT_SIZE
                final_y = y * Constants.UNIT_SIZE
                rect = pygame.Rect(final_x, final_y, Constants.UNIT_SIZE, Constants.UNIT_SIZE)
                collisions = [i["rect"] for i in obstacles]
                item = rect.collidelist(collisions)
                if item == -1:
                    print(f"picked swamp tile placement: {final_x}x{final_y}")
                    obs_item = dict(name="swamp", rect=rect, walkable=True, coord=(final_x,final_y))
                    obstacles.append(obs_item)
                    self.MapTiles.append(obs_item)
                    num_tiles += 1
            num_tiles = 0
        end = time.perf_counter()
        print(f"create_swamp_tiles: {round(60 - (end - start), 2)} second(s)")
        return obstacles, grid

    # returns all obstablces in a single list of dictionaries
    def create_terrain(self, pgu, grid, tiles):
        create_terrain_start = time.perf_counter()
        obstacles = []

        # for r in menu_rects:
        #     walkable = r["walkable"]
        #     # create side panel tiles
        #     height_start = 0
        #     height_end = int(r["rects"].Rect.height / Constants.UNIT_SIZE)
        #     width_start = 0
        #     width_end = int(r["rects"].Rect.width / Constants.UNIT_SIZE)
            
        #     for w in range(width_start, width_end):
        #         for h in range(height_start, height_end):
        #             print(f"(w,h): ({h},{w})")
        #             current_node = grid.nodes[h]
        #             current_coord = current_node[w]
        #             grid.node(current_coord.x, current_coord.y).walkable = False
        #             # rect_x = current_coord.x * Constants.UNIT_SIZE
        #             # rect_y = current_coord.y * Constants.UNIT_SIZE
        #             # rect = pygame.Rect(rect_x, rect_y, Constants.UNIT_SIZE, Constants.UNIT_SIZE)
        #             # obstacles.append(dict(name="panel", rect=rect, walkable=walkable))

        # create water tiles
        # obstacles, grid = self.create_water_tiles(pgu, grid, obstacles)
        # obstacles, grid = self.create_mountain_tiles(grid, obstacles)
        # obstacles, grid = self.create_swamp_tiles(grid, obstacles)
        # obstacles, grid = self.create_fire_tiles(grid, obstacles)
        # obstacles, grid = self.create_forest_tiles(grid, obstacles)
        # obstacles, grid = self.create_fog_tiles(grid, obstacles)
        # obstacles, grid = self.create_rain_tiles(grid, obstacles)
        # obstacles, grid = self.create_lava_tiles(grid, obstacles)

        create_terrain_end = time.perf_counter()
        print(f"create_terrain timings: {round(60 - (create_terrain_end - create_terrain_start), 2)} second(s)")
        return tiles

    def draw_terrain(self, pgu, tiles):
        draw_terrain_start = time.perf_counter()
        for tile in tiles:
            if tile.Type == Environment.TileType.Water:
                pygame.draw.rect(pgu.surface, Constants.Colors.AQUA, tile.RectSettings.Rect)
            elif tile.Type == Environment.TileType.Fire:
                pygame.draw.rect(pgu.surface, Constants.Colors.FIRE, tile.RectSettings.Rect)
            elif tile.Type == Environment.TileType.Mountain:
                pygame.draw.rect(pgu.surface, Constants.Colors.WHITE_MISTY, tile.RectSettings.Rect)
            elif tile.Type == Environment.TileType.Forest:
                pygame.draw.rect(pgu.surface, Constants.Colors.GREEN_DARK, tile.RectSettings.Rect)
            elif tile.Type == Environment.TileType.Rain:
                pygame.draw.rect(pgu.surface, Constants.Colors.RAIN, tile.RectSettings.Rect)
            elif tile.Type == Environment.TileType.Fog:
                pygame.draw.rect(pgu.surface, Constants.Colors.GRAY_IRON_MOUNTAIN, tile.RectSettings.Rect)
            elif tile.Type == Environment.TileType.Swamp:
                pygame.draw.rect(pgu.surface, Constants.Colors.OLIVE, tile.RectSettings.Rect)
            elif tile.Type == Environment.TileType.Lava:
                pygame.draw.rect(pgu.surface, Constants.Colors.LAVA, tile.RectSettings.Rect)
            elif tile.Type == Environment.TileType.Basic:
                pygame.draw.rect(pgu.surface, Constants.Colors.SANDY_BROWN, tile.RectSettings.Rect)
        draw_terrain_end = time.perf_counter()
        print(f"draw_terrain timings: {round(60 - (draw_terrain_end - draw_terrain_start), 2)} second(s)")

    # uses speed of unit
    # executor.submit(self.ut.move_unit_over_time, self.pgu, self.grid, army_unit, mouse_pos[0], mouse_pos[1]))
    def move_unit_over_time(self, pgu, gu, unit, end_x, end_y):
        gu.Grid.cleanup()
        default_speed = .35
        speed = default_speed - (unit.Type.speed * .1)
        start_x_grid = int(unit.rs.Rect.x  / Constants.UNIT_SIZE)
        start_y_grid = int(unit.rs.Rect.y  / Constants.UNIT_SIZE)
        end_x_grid = int(end_x / Constants.UNIT_SIZE)
        end_y_grid = int(end_y / Constants.UNIT_SIZE)
        start = gu.Grid.node(start_x_grid, start_y_grid)
        end = gu.Grid.node(end_x_grid, end_y_grid)
        print(f"Checking path: {start_x_grid}x{start_y_grid} to {end_x_grid}x{end_y_grid}")
        try:
            paths, runs = gu.Finder.find_path(start, end, gu.Grid)
        except Exception as e:
            print("find_path exception:")
            # print(f"paths: {str(paths)}")
            # print(f"runs: {str(runs)}")
            print(f"start: {str(start)}")
            print(f"end: {str(end)}")
            print(f"Grid: {str(gu.Grid)}")
            print(str(e))
            traceback.print_exc()

        return_msg = ""
        if len(paths) < 1:
            return_msg = f"{unit.Name}: I can't get there"
        else:
            print(f"Moving {unit.Name} at {round(speed, 2)} speed from ({start_x_grid}, {start_y_grid}) to ({end_x_grid}, {end_y_grid}), journey will take {runs} steps")
            print(f"paths: {paths}")
            x = unit.rs.Rect.x
            y = unit.rs.Rect.y
            oldrect = None 

            start = time.perf_counter()              
            for path in paths:       
                newrect = pygame.Rect(x, y, Constants.UNIT_SIZE, Constants.UNIT_SIZE)       
                print(f"Sleeping: {round(speed, 2)} seconds before moving {unit.Name} again ({unit})")
                sleep(speed)
                newrect.x = int(path[0] * Constants.UNIT_SIZE)
                newrect.y = int(path[1] * Constants.UNIT_SIZE)
                if oldrect is None:
                    print(f"{unit.Name} beginning travel to ({newrect.x}x{newrect.y})")
                else:
                    print(f"Moving {unit.Name} from ({oldrect.x}x{oldrect.y}) to ({newrect.x}x{newrect.y})")
                newrect = self.move_unit(pgu, oldrect, newrect, unit.rs.BgColor)
                oldrect = newrect
            unit.rs.Rect = oldrect
            end = time.perf_counter()
            return_msg = f"{unit.Name} arrived and their destination.  Commute took {round(end - start, 2)} second(s)"
        return return_msg

    # moves rect x,y cords
    def move_unit(self, pgu, prevrect, newrect, bg_color):

        # previous
        if prevrect is not None: 
            rs = pgu.RectSettings()
            rs.BgColor = Constants.Colors.GAME_MAP_COLOR
            rs.BorderColor = Constants.Colors.GAME_MAP_COLOR
            rs.Rect = prevrect
            pgu.create_rect(rs)  
            pygame.display.update(prevrect)

        # new
        rs = pgu.RectSettings()
        rs.BorderColor = Constants.Colors.GAME_MAP_COLOR
        rs.Rect = newrect
        rs.BgColor = bg_color
        pgu.create_rect(rs)      
        
        pygame.display.update(newrect)
        return newrect

    def update_selected_units_list(self, unit):
        newlist = self.selected_units
        unit_already_added = False
        for selected_unit in self.selected_units:
            if selected_unit.Name == unit.Name:
                unit_already_added = True
                break

        if unit_already_added:
            # newlist.remove(unit) # this is wrong
            pass
        else:
            newlist.append(unit)

        return newlist

    # create sides panel with army troop buttons
    def draw_side_panel(self, pgu, player, really_draw=True):
        mouse_pos = pgu.update_mouse()
        if self.sp_menu_rs is None:
            sp_menu_rs = pgu.RectSettings()
            sp_menu_rs.BgColor = Constants.Colors.POOP_BROWN
            sp_menu_rs.FontSize = Constants.SP_BUTTON_TEXT_SIZE
            sp_menu_rs.Width = Constants.SP_WIDTH
            sp_menu_rs.Height = pgu.surface.get_height()
            sp_menu_rs.BorderColor = Constants.Colors.GAME_BORDER_COLOR
            sp_menu_rs.BorderSides = [Constants.BorderSides.RIGHT]
            self.sp_menu_rs = sp_menu_rs
        self.sp_menu_rs = pgu.create_rect(self.sp_menu_rs, ignore_side_panel=True, really_draw=really_draw)

        # also draw guys..
        if really_draw:
            i = 1
            unit_button_list = []
            for unit in player.selected_race.units:
                unit_x = (Constants.SP_WIDTH / 2) / 2
                unit_y = 60 * i
                unit_width = Constants.SP_WIDTH / 2
                unit_height = unit_width
                rs = pgu.RectSettings()
                rs.Rect = pygame.Rect(unit_x, unit_y, unit_width, unit_height)
                rs.BgColor = player.selected_race.main_color
                rs.BorderColor = player.selected_race.secondary_color
                rs.Text = unit["Name"]
                rs.HintName = "unit button text"
                rs.FontSize = Constants.SP_BUTTON_TEXT_SIZE
                rs.Font = pygame.font.Font(None, rs.FontSize)                
                pgu.create_rect(rs, ignore_side_panel=True)

                # update our list to pass back
                unit_button_list.append(rs)
                i = i + 1

            if mouse_pos is not None:
                for unit_btn_rectsettings in unit_button_list:
                    if unit_btn_rectsettings.Rect.collidepoint(mouse_pos):
                        self.unit_button_highlighted(pgu, player, unit_btn_rectsettings)

    # the bottom panel shown when one or more units selected
    def create_bottom_panel(self, pgu, player):
        rs = pgu.RectSettings()
        rs.BgColor = Constants.Colors.COCOA
        rs.BorderColor = Constants.Colors.GAME_BORDER_COLOR
        rs.BorderSides = [Constants.BorderSides.TOP, Constants.BorderSides.LEFT]
        rs.FontSize = Constants.SP_BUTTON_TEXT_SIZE
        nudge = 2
        rs.x = Constants.SP_WIDTH  + nudge # start at end of SP panel
        rs.y = Constants.SCREEN_HEIGHT - Constants.BP_HEIGHT
        rs.Width = Constants.SCREEN_WIDTH - Constants.SP_WIDTH - nudge
        rs.Height = pgu.surface.get_height()
        rs.HintName = "bottom panel main"
        pgu.create_rect(rs, ignore_side_panel=True)

        # button for each guy
        i = 1
        unit_button_list = []
        for unit in player.army:
            unit_x = Constants.SP_WIDTH + Constants.PANEL_BUTTON_SPACING
            unit_y = rs.y + Constants.RECT_SIZE
            unit_width = Constants.SP_WIDTH / 2
            unit_height = unit_width
            rs = pgu.RectSettings()
            rs.Rect = pygame.Rect(unit_x, unit_y, unit_width, unit_height)
            rs.BgColor = player.selected_race.main_color
            rs.BorderColor = player.selected_race.secondary_color
            rs.Text = unit.Name
            rs.HintName = "unit button text"
            rs.FontSize = Constants.SP_BUTTON_TEXT_SIZE
            pgu.create_rect(rs, ignore_side_panel=True)

            # update our list to pass back
            unit_button_list.append(rs)
            i = i + 1

        return unit_button_list

    # highlights buttons on left side panel
    def unit_button_highlighted(self, pgu, player, rs):
        rs.FontColor = player.selected_race.hover_text_color
        rs.BgColor = player.selected_race.hover_color
        pgu.create_rect(rs, ignore_side_panel=True, really_draw=True)
        pgu.update_mouse()

    # changed border around unit to indicate it's "selected" - random color border
    def select_unit(self, pgu, unit):
        unit.rs.BorderColor = Constants.Colors.RANDOM
        unit.rs = pgu.create_rect(unit.rs)
        return unit

    # if a unit_type is specified, we consider this a "unit", otherwise, it's just a rect that could be used for anythign..
    def create_unit(self, pgu, player, unit_type, unit = None):
        if unit is None:
            unit = Unit()
            unit.rs = pgu.RectSettings()
            unit.rs.BgColor = player.selected_race.main_color
            unit.rs.BorderColor = player.selected_race.secondary_color
            unit.rs.x = random.randint(Constants.SPAWN_X, Constants.SPAWN_X + (Constants.SPAWN_WIDTH - Constants.UNIT_SIZE))
            unit.rs.y = random.randint(Constants.SPAWN_Y, Constants.SPAWN_Y + (Constants.SPAWN_HEIGHT - Constants.UNIT_SIZE))
            unit.rs.Width = Constants.UNIT_SIZE
            unit.rs.Height = Constants.UNIT_SIZE
            unit.Name = Names.generate_name(self)
            unit.Type = unit_type
            unit.rs.HintName = f"army unit on field: {unit.Name}" # just used for debugging

        # create new unit for this guy
        unit.rs = pgu.create_rect(unit.rs)

        # add to our army list
        found_unit = False
        for army_unit in player.army:
            if army_unit.Name == unit.Name:
                found_unit = True
                break
        if not found_unit:
            player.army.append(unit)

        return unit


