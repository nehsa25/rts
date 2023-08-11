import random
from time import sleep
import time
from uuid import uuid4
import pygame
from enum import Enum
from pathfinding.finder.a_star import AStarFinder

# our stuff
from constants import Constants
from names import Names
from unit import Unit
from pygameutility import PygameUtilities

class Utility:
    finder = AStarFinder()

    side_panel_rects = None
    spawn_points = None

    # mouse
    mouse_pointer = None
    mouse_pointer_mask = None


    def __init__(self):
        self.finder = AStarFinder()

        self.mouse_pointer = pygame.Surface((Constants.MOUSE_POINTER_SIZE, Constants.MOUSE_POINTER_SIZE))
        self.mouse_pointer.fill(Constants.Colors.MOUSE_POINTER_COLOR)
        self.mouse_pointer_mask = pygame.mask.from_surface(self.mouse_pointer)

        # hides mouse pointer provided by pygame
        # pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

    def load_grid(self, pgu, grid, load_env = True):
        #  refresh side panel / highlight a unit that's hovered over
        if self.side_panel_rects is None:
            self.side_panel_rects = self.draw_side_panel(pgu, really_draw=False)

        # spawn points
        if self.spawn_points is None:
            self.spawn_points = self.draw_spawn_points(pgu, really_draw=False)

        usable_map = False

        # get grid of screen based on unit size
        grid = pgu.get_empty_grid()
        while not usable_map:
            # generate our obstacles
            obstacles = []
            if load_env:
                menu_list = []
                menu_list.append(dict(rects=self.side_panel_rects, walkable=False))
                menu_list.append(dict(rects=self.spawn_points, walkable=True))
                obstacles = self.create_terrain(grid, menu_list)

                # # update grid with nodes we cannot walk on
                grid = self.update_grid_with_terrain(grid, obstacles)

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

            print(f"Map created is: {usable_map}")
            grid.cleanup()

        print(f"usable_map: {usable_map}, runs: {runs}")        
        return grid, obstacles

    # creates section of the map free for units spawn
    def draw_spawn_points(self, pgu, really_draw = True):
        self.update_mouse(pgu)
        rect_settings = pgu.RectSettings()
        rect_settings.BgColor = Constants.Colors.ALICE_BLUE
        rect_settings.FontSize = Constants.SP_BUTTON_TEXT_SIZE
        rect_settings.BorderColor = Constants.Colors.PLUM
        rect_settings.Rect = pygame.Rect(Constants.UNIT_SPAWN_X, Constants.UNIT_SPAWN_Y, Constants.SPAWN_WIDTH, Constants.SPAWN_HEIGHT)        
        return pgu.create_rect(rect_settings, ignore_side_panel=True, really_draw=really_draw)

    def update_mouse(self, pgu, mouse_pos=None, mouse_pointer = None):
        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()

        if mouse_pointer is None:
            mouse_pointer = self.mouse_pointer

        pgu.surface.blit(mouse_pointer, mouse_pos)

        return mouse_pos

    def create_water_tiles(self, grid, obstacles):
        start = time.perf_counter()
        num_tiles = 0
        for num_complete in range(Constants.NUM_WATER_TILES):
            print(f"create_water_tiles % Complete: {round(((num_complete / Constants.NUM_WATER_TILES) * 100), 2)}")

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
                    y += 1
                elif side == "bottom":
                    y += -1

                final_x = x * Constants.UNIT_SIZE
                final_y = y * Constants.UNIT_SIZE
                rect = pygame.Rect(final_x, final_y, Constants.UNIT_SIZE, Constants.UNIT_SIZE)
                collisions = [i["rect"] for i in obstacles]
                item = rect.collidelist(collisions)
                if item == -1:
                    print(f"picked water tile placement: {final_x}x{final_y}")
                    obstacles.append(dict(name="water", rect=rect, walkable=False))
                    num_tiles += 1

            print(f"num water tiles placed for {density}: {num_tiles}")

            # start next "range" of water
            num_tiles = 0

        end = time.perf_counter()
        print(f"create_water_tiles: {round(60 - (end - start), 2)} second(s)")
        return obstacles

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
                    y += 1
                elif side == "bottom":
                    y += -1

                final_x = x * Constants.UNIT_SIZE
                final_y = y * Constants.UNIT_SIZE
                rect = pygame.Rect(final_x, final_y, Constants.UNIT_SIZE, Constants.UNIT_SIZE)
                collisions = [i["rect"] for i in obstacles]
                item = rect.collidelist(collisions)
                if item == -1:
                    print(f"picked mountain tile placement: {final_x}x{final_y}")
                    obstacles.append(dict(name="mountain", rect=rect, walkable=False))
                    num_tiles += 1
            num_tiles = 0
        end = time.perf_counter()
        print(f"create_mountain_tiles: {round(60 - (end - start), 2)} second(s)")
        return obstacles

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
                    y += 1
                elif side == "bottom":
                    y += -1

                final_x = x * Constants.UNIT_SIZE
                final_y = y * Constants.UNIT_SIZE
                rect = pygame.Rect(final_x, final_y, Constants.UNIT_SIZE, Constants.UNIT_SIZE)
                collisions = [i["rect"] for i in obstacles]
                item = rect.collidelist(collisions)
                if item == -1:
                    print(f"picked fire tile placement: {final_x}x{final_y}")
                    obstacles.append(dict(name="fire", rect=rect, walkable=False))
                    num_tiles += 1
            num_tiles = 0
        end = time.perf_counter()
        print(f"create_fire_tiles: {round(60 - (end - start), 2)} second(s)")
        return obstacles

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
                    y += 1
                elif side == "bottom":
                    y += -1

                final_x = x * Constants.UNIT_SIZE
                final_y = y * Constants.UNIT_SIZE
                rect = pygame.Rect(final_x, final_y, Constants.UNIT_SIZE, Constants.UNIT_SIZE)
                collisions = [i["rect"] for i in obstacles]
                item = rect.collidelist(collisions)
                if item == -1:
                    print(f"picked forest tile placement: {final_x}x{final_y}")
                    obstacles.append(dict(name="forest", rect=rect, walkable=False))
                    num_tiles += 1
            num_tiles = 0
        end = time.perf_counter()
        print(f"create_forest_tiles: {round(60 - (end - start), 2)} second(s)")
        return obstacles

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
                    y += 1
                elif side == "bottom":
                    y += -1

                final_x = x * Constants.UNIT_SIZE
                final_y = y * Constants.UNIT_SIZE
                rect = pygame.Rect(final_x, final_y, Constants.UNIT_SIZE, Constants.UNIT_SIZE)
                collisions = [i["rect"] for i in obstacles]
                item = rect.collidelist(collisions)
                if item == -1:
                    print(f"picked fog tile placement: {final_x}x{final_y}")
                    obstacles.append(dict(name="fog", rect=rect, walkable=True))
                    num_tiles += 1
            num_tiles = 0
        end = time.perf_counter()
        print(f"create_fog_tiles: {round(60 - (end - start), 2)} second(s)")
        return obstacles
    
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
                    y += 1
                elif side == "bottom":
                    y += -1

                final_x = x * Constants.UNIT_SIZE
                final_y = y * Constants.UNIT_SIZE
                rect = pygame.Rect(final_x, final_y, Constants.UNIT_SIZE, Constants.UNIT_SIZE)
                collisions = [i["rect"] for i in obstacles]
                item = rect.collidelist(collisions)
                if item == -1:
                    print(f"picked rain tile placement: {final_x}x{final_y}")
                    obstacles.append(dict(name="rain", rect=rect, walkable=True))
                    num_tiles += 1
            num_tiles = 0
        end = time.perf_counter()
        print(f"create_rain_tiles: {round(60 - (end - start), 2)} second(s)")
        return obstacles
    
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
                    y += 1
                elif side == "bottom":
                    y += -1

                final_x = x * Constants.UNIT_SIZE
                final_y = y * Constants.UNIT_SIZE
                rect = pygame.Rect(final_x, final_y, Constants.UNIT_SIZE, Constants.UNIT_SIZE)
                collisions = [i["rect"] for i in obstacles]
                item = rect.collidelist(collisions)
                if item == -1:
                    print(f"picked lava tile placement: {final_x}x{final_y}")
                    obstacles.append(dict(name="lava", rect=rect, walkable=False))
                    num_tiles += 1
            num_tiles = 0
        end = time.perf_counter()
        print(f"create_lava_tiles: {round(60 - (end - start), 2)} second(s)")
        return obstacles
    
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
                    y += 1
                elif side == "bottom":
                    y += -1

                final_x = x * Constants.UNIT_SIZE
                final_y = y * Constants.UNIT_SIZE
                rect = pygame.Rect(final_x, final_y, Constants.UNIT_SIZE, Constants.UNIT_SIZE)
                collisions = [i["rect"] for i in obstacles]
                item = rect.collidelist(collisions)
                if item == -1:
                    print(f"picked swamp tile placement: {final_x}x{final_y}")
                    obstacles.append(dict(name="swamp", rect=rect, walkable=True))
                    num_tiles += 1
            num_tiles = 0
        end = time.perf_counter()
        print(f"create_swamp_tiles: {round(60 - (end - start), 2)} second(s)")
        return obstacles

    # returns all obstablces in a single list of dictionaries
    def create_terrain(self, grid, menu_rects):
        create_terrain_start = time.perf_counter()
        obstacles = []

        for r in menu_rects:
            walkable = r["walkable"]
            # create side panel tiles
            for h in range(0, int(r["rects"].Rect.height / Constants.UNIT_SIZE)):
                for w in range(0, int(r["rects"].Rect.width / Constants.UNIT_SIZE)):
                    rand_node = grid.nodes[h]
                    rand_cord = rand_node[w]
                    rect = pygame.Rect(rand_cord.x * Constants.UNIT_SIZE, rand_cord.y * Constants.UNIT_SIZE, Constants.UNIT_SIZE, Constants.UNIT_SIZE)
                    obstacles.append(dict(name="panel", rect=rect, walkable=walkable))

        # create water tiles
        obstacles = self.create_water_tiles(grid, obstacles)
        obstacles = self.create_mountain_tiles(grid, obstacles)
        obstacles = self.create_swamp_tiles(grid, obstacles)
        obstacles = self.create_fire_tiles(grid, obstacles)
        obstacles = self.create_forest_tiles(grid, obstacles)
        obstacles = self.create_fog_tiles(grid, obstacles)
        obstacles = self.create_rain_tiles(grid, obstacles)
        obstacles = self.create_lava_tiles(grid, obstacles)

        create_terrain_end = time.perf_counter()
        print(f"create_terrain timings: {round(60 - (create_terrain_end - create_terrain_start), 2)} second(s)")
        return obstacles

    def draw_terrain(self, pgu, obstacles):
        draw_terrain_start = time.perf_counter()
        for obstacle in obstacles:
            if obstacle["name"].lower() == "water": # create random "water" obstacles
                pygame.draw.rect(pgu.surface, Constants.Colors.AQUA, obstacle["rect"])
            elif obstacle["name"].lower() == "fire": # create random "fire" obstacles
                pygame.draw.rect(pgu.surface, Constants.Colors.FIRE, obstacle["rect"])
            elif obstacle["name"].lower() == "mountain": # create random "mountain" obstacles
                pygame.draw.rect(pgu.surface, Constants.Colors.WHITE_MISTY, obstacle["rect"])
            elif obstacle["name"].lower() == "swamp": # create random "mountain" obstacles
                pygame.draw.rect(pgu.surface, Constants.Colors.GREEN_DARK, obstacle["rect"])
            elif obstacle["name"].lower() == "rain": # create random "mountain" obstacles
                pygame.draw.rect(pgu.surface, Constants.Colors.GREEN_DARK, obstacle["rect"])
            elif obstacle["name"].lower() == "fog": # create random "mountain" obstacles
                pygame.draw.rect(pgu.surface, Constants.Colors.GREEN_DARK, obstacle["rect"])
            elif obstacle["name"].lower() == "forest": # create random "mountain" obstacles
                pygame.draw.rect(pgu.surface, Constants.Colors.GREEN_DARK, obstacle["rect"])
            elif obstacle["name"].lower() == "lava": # create random "mountain" obstacles
                pygame.draw.rect(pgu.surface, Constants.Colors.LAVA, obstacle["rect"])
        draw_terrain_end = time.perf_counter()
        # print(f"draw_terrain timings: {round(60 - (draw_terrain_end - draw_terrain_start), 2)} second(s)")
        # pygame.display.flip()
        # pass

    def update_grid_with_terrain(self, grid, obstacle_types):
        get_grid_start = time.perf_counter()
        print("get_grid: Updating pathfinding grid with terrain...")
        UNIT_CAN_MOVE = True
        UNIT_CANNOT_MOVE = False

        collisions = [i["rect"] for i in obstacle_types if i["walkable"] == False]
        for node in grid.nodes:
            for item in node:
                rect = pygame.Rect(item.x * Constants.UNIT_SIZE, item.y * Constants.UNIT_SIZE, Constants.UNIT_SIZE, Constants.UNIT_SIZE)
                collide = rect.collidelist(collisions)
                if collide == -1:
                    item.walkable = UNIT_CAN_MOVE
                else:
                    item.walkable = UNIT_CANNOT_MOVE
        get_grid_end = time.perf_counter()
        print("get_grid: Done")
        print(f"get_grid timings: {round(60 - (get_grid_end - get_grid_start), 2)} second(s)")
        return grid

    # uses speed of unit
    def move_unit_over_time(self, pgu, grid, unit, end_x, end_y):
        grid.cleanup()
        default_speed = .35
        speed = default_speed - (unit.Type.speed * .1)
        start_x_grid = int(unit.Rect_Settings.Rect.x  / Constants.UNIT_SIZE)
        start_y_grid = int(unit.Rect_Settings.Rect.y  / Constants.UNIT_SIZE)
        end_x_grid = int(end_x / Constants.UNIT_SIZE)
        end_y_grid = int(end_y / Constants.UNIT_SIZE)
        start = grid.node(start_x_grid, start_y_grid)
        end = grid.node(end_x_grid, end_y_grid)
        print(f"Checking path: {start_x_grid}x{start_y_grid} to {end_x_grid}x{end_y_grid}")
        paths, runs = self.finder.find_path(start, end, grid)
        print(f"Moving {unit.Name} at {round(speed, 2)} speed from ({start_x_grid}, {start_y_grid}) to ({end_x_grid}, {end_y_grid}), journey will take {runs} steps")
        print(f"paths: {paths}")
        x = unit.Rect_Settings.Rect.x
        y = unit.Rect_Settings.Rect.y
        oldrect = None 
              
        for path in paths:       
            newrect = pygame.Rect(x, y, Constants.UNIT_SIZE, Constants.UNIT_SIZE)       
            print(f"Sleeping: {round(speed, 3)} seconds before moving {unit.Name} again")
            sleep(speed)
            newrect.x = int(path[0] * Constants.UNIT_SIZE)
            newrect.y = int(path[1] * Constants.UNIT_SIZE)
            print(f"moving unit to ({newrect.x}x{newrect.y})")
            newrect = self.move_unit(pgu, oldrect, newrect, unit.Rect_Settings.BgColor)
            oldrect = newrect
        unit.Rect_Settings.Rect = oldrect
        return f"{unit.Name} done moving"

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
            pygame.display.flip()

        # new
        rs = pgu.RectSettings()
        rs.BorderColor = Constants.Colors.GAME_MAP_COLOR
        rs.Rect = newrect
        rs.BgColor = bg_color
        pgu.create_rect(rs)      
        
        pygame.display.update(newrect)
        pygame.display.flip()
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
    def draw_side_panel(self, pgu, player = None, rect_settings = None, really_draw = True):
        mouse_pos = self.update_mouse(pgu)
        if rect_settings is None:
            rect_settings = pgu.RectSettings()
            rect_settings.BgColor = Constants.Colors.POOP_BROWN
            rect_settings.FontSize = Constants.SP_BUTTON_TEXT_SIZE
            rect_settings.Rect = pygame.Rect(0, 0, Constants.SP_WIDTH, pgu.surface.get_height())
            rect_settings.BorderColor = Constants.Colors.GAME_BORDER
            rect_settings.BorderSides = [Constants.BorderSides.RIGHT]

        side_panel_rect_settings = pgu.create_rect(rect_settings, ignore_side_panel=True, really_draw=really_draw)
        if really_draw:
            # button for each guy
            i = 1
            unit_button_list = []
            for unit in player.selected_race.units:
                unit_x = (Constants.SP_WIDTH / 2) / 2
                unit_y = 60 * i
                unit_width = Constants.SP_WIDTH / 2
                unit_height = unit_width

                rect_settings = pgu.RectSettings()
                rect_settings.Rect = pygame.Rect(unit_x, unit_y, unit_width, unit_height)
                rect_settings.BgColor = player.selected_race.main_color
                rect_settings.BorderColor = player.selected_race.secondary_color
                rect_settings.Text = unit["Name"]
                rect_settings.HintName = "unit button text"
                rect_settings.FontSize = Constants.SP_BUTTON_TEXT_SIZE

                pgu.create_rect(rect_settings, ignore_side_panel=True)
                pgu.update_rect_with_text(rect_settings)

                # update our list to pass back
                unit_button_list.append(rect_settings)
                i = i + 1

            if mouse_pos is not None:
                for unit_btn_rectsettings in unit_button_list:
                    if unit_btn_rectsettings.Rect.collidepoint(mouse_pos):
                        self.unit_button_highlighted(pgu, player, unit_btn_rectsettings)

        return side_panel_rect_settings

    # the bottom panel shown when one or more units selected
    def create_bottom_panel(self, pgu, player):
        rect_settings = pgu.RectSettings()
        rect_settings.BgColor = Constants.Colors.COCOA
        rect_settings.BorderColor = Constants.Colors.GAME_BORDER
        rect_settings.BorderSides = [Constants.BorderSides.TOP, Constants.BorderSides.LEFT]
        rect_settings.FontSize = Constants.SP_BUTTON_TEXT_SIZE
        nudge = 2
        rect_settings.x = Constants.SP_WIDTH  + nudge # start at end of SP panel
        rect_settings.y = Constants.SCREEN_HEIGHT - Constants.BP_HEIGHT
        rect_settings.width = Constants.SCREEN_WIDTH - Constants.SP_WIDTH - nudge
        rect_settings.height = pgu.surface.get_height()
        rect_settings.HintName = "bottom panel main"
        pgu.create_rect(rect_settings, ignore_side_panel=True)

        # button for each guy
        i = 1
        unit_button_list = []
        for unit in player.army:
            unit_x = Constants.SP_WIDTH + Constants.PANEL_BUTTON_SPACING
            unit_y = rect_settings.y + Constants.RECT_SIZE
            unit_width = Constants.SP_WIDTH / 2
            unit_height = unit_width

            rect_settings = pgu.RectSettings()
            rect_settings.Rect = pygame.Rect(unit_x, unit_y, unit_width, unit_height)
            rect_settings.BgColor = player.selected_race.main_color
            rect_settings.BorderColor = player.selected_race.secondary_color
            rect_settings.Text = unit.Name
            rect_settings.HintName = "unit button text"
            rect_settings.FontSize = Constants.SP_BUTTON_TEXT_SIZE

            pgu.create_rect(rect_settings, ignore_side_panel=True)
            pgu.update_rect_with_text(rect_settings)

            # update our list to pass back
            unit_button_list.append(rect_settings)
            i = i + 1

        return unit_button_list

    # highlights buttons on left side panel
    def unit_button_highlighted(self, pgu, player, unit_btn_rectsettings):
        self.update_mouse(pgu)
        unit_btn_rectsettings.FontColor =  player.selected_race.hover_text_color
        pygame.draw.rect(pgu.surface, player.selected_race.hover_color, unit_btn_rectsettings.Rect)
        pgu.update_rect_with_text(unit_btn_rectsettings)

    # changed border around unit to indicate it's "selected" - random color border
    def select_unit(self, pgu, unit):
        unit.Rect_Settings.BorderColor = Constants.Colors.RANDOM
        unit.Rect_Settings = pgu.create_rect(unit.Rect_Settings)
        return unit

    # if a unit_type is specified, we consider this a "unit", otherwise, it's just a rect that could be used for anythign..
    def create_unit(self, pgu, player, unit_type, unit = None):
        if unit is None:
            unit = Unit()
            unit.Rect_Settings = pgu.RectSettings()
            unit.Rect_Settings.BgColor = player.selected_race.main_color
            unit.Rect_Settings.BorderColor = player.selected_race.secondary_color
            unit.Rect_Settings.x = random.randint(Constants.UNIT_SPAWN_X, Constants.UNIT_SPAWN_X + Constants.SPAWN_WIDTH)
            unit.Rect_Settings.y = random.randint(Constants.UNIT_SPAWN_Y, Constants.UNIT_SPAWN_Y + Constants.SCREEN_HEIGHT)
            unit.Rect_Settings.width = Constants.UNIT_SIZE
            unit.Rect_Settings.height = Constants.UNIT_SIZE
            unit.Name = Names.generate_name(self)
            unit.Type = unit_type
            unit.Rect_Settings.HintName = f"army unit on field: {unit.Name}" # just used for debugging

        # create new unit for this guy
        unit.Rect_Settings = pgu.create_rect(unit.Rect_Settings)

        # add to our army list
        found_unit = False
        for army_unit in player.army:
            if army_unit.Name == unit.Name:
                found_unit = True
                break
        if not found_unit:
            player.army.append(unit)

        return unit


