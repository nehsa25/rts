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
from pygameutility import PyGameUtility

class Utility:
    finder = AStarFinder()

    def load_grid(self):
                # get grid of screen based on unit size
                self.grid = PyGameUtility.get_empty_grid(self)
                
                #  refresh side panel / highlight a unit that's hovered over
                self.side_panel_rects = Utility.draw_side_panel(self, really_draw=False)

                # generate our obstacles
                self.obstacles = Utility.create_terrain(self, self.grid, self.side_panel_rects)

                # update grid with nodes we cannot walk on
                self.grid = Utility.update_grid_with_terrain(self, self.grid, self.obstacles)
                
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
                    obstacles.append(dict(name="water", rect = rect))
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
                    obstacles.append(dict(name="mountain", rect = rect))
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
                    obstacles.append(dict(name="fire", rect = rect))
                    num_tiles += 1
            num_tiles = 0
        end = time.perf_counter()
        print(f"create_fire_tiles: {round(60 - (end - start), 2)} second(s)")
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
                    obstacles.append(dict(name="swamp", rect = rect))
                    num_tiles += 1
            num_tiles = 0
        end = time.perf_counter()
        print(f"create_swamp_tiles: {round(60 - (end - start), 2)} second(s)")
        return obstacles

    # returns all obstablces in a single list of dictionaries
    def create_terrain(self, grid, side_panel_rect):
        create_terrain_start = time.perf_counter()  
        obstacles = []

        # create side panel tiles
        for h in range(0, int(side_panel_rect.Rect.height / Constants.UNIT_SIZE)):
            for w in range(0, int(side_panel_rect.Rect.width / Constants.UNIT_SIZE)):
                rand_node = grid.nodes[h]
                rand_cord = rand_node[w]
                rect = pygame.Rect(rand_cord.x * Constants.UNIT_SIZE, rand_cord.y * Constants.UNIT_SIZE, Constants.UNIT_SIZE, Constants.UNIT_SIZE)
                obstacles.append(dict(name="panel", rect = rect))

        # create water tiles
        obstacles = Utility.create_water_tiles(self, grid, obstacles)
        obstacles = Utility.create_mountain_tiles(self, grid, obstacles)
        obstacles = Utility.create_swamp_tiles(self, grid, obstacles)
        obstacles = Utility.create_fire_tiles(self, grid, obstacles)

        create_terrain_end = time.perf_counter() 
        print(f"create_terrain timings: {round(60 - (create_terrain_end - create_terrain_start), 2)} second(s)")
        return obstacles

    def draw_terrain(self, obstacles):
        draw_terrain_start = time.perf_counter() 
        for obstacle in obstacles:                 
            if obstacle["name"].lower() == "water": # create random "water" obstacles
                pygame.draw.rect(self.surface, Constants.Colors.AQUA, obstacle["rect"])
            elif obstacle["name"].lower() == "fire": # create random "fire" obstacles 
                pygame.draw.rect(self.surface, Constants.Colors.FIRE, obstacle["rect"])
            elif obstacle["name"].lower() == "mountain": # create random "mountain" obstacles
                pygame.draw.rect(self.surface, Constants.Colors.WHITE_MISTY, obstacle["rect"])
            elif obstacle["name"].lower() == "swamp": # create random "mountain" obstacles
                pygame.draw.rect(self.surface, Constants.Colors.GREEN_DARK, obstacle["rect"])
        draw_terrain_end = time.perf_counter() 
        # print(f"draw_terrain timings: {round(60 - (draw_terrain_end - draw_terrain_start), 2)} second(s)")
        # pygame.display.flip()
        # pass

    def update_grid_with_terrain(self, grid, obstacle_types):
        get_grid_start = time.perf_counter() 
        print("get_grid: Updating pathfinding grid with terrain...")
        UNIT_CAN_MOVE = True
        UNIT_CANNOT_MOVE = False     
        for node in grid.nodes:
            for item in node:
                collisions = [i["rect"] for i in obstacle_types]
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
    def move_unit_over_time(self, grid, unit, end_x, end_y):
        default_speed = .35
        speed = default_speed - (unit.Type.speed * .1)        
        start_x_grid = int(unit.Rect_Settings.x  / Constants.UNIT_SIZE)
        start_y_grid = int(unit.Rect_Settings.y  / Constants.UNIT_SIZE)
        end_x_grid = int(end_x / Constants.UNIT_SIZE)
        end_y_grid = int(end_y / Constants.UNIT_SIZE)

        print(f"Moving {unit.Name} at {speed} speed from ({start_x_grid}, {start_y_grid}) to ({end_x_grid}, {end_y_grid})")

        start = grid.node(start_x_grid, start_y_grid)
        end = grid.node(end_x_grid, end_y_grid)
        paths, runs = Utility.finder.find_path(start, end, grid)
        print(f"number \"runs\" path will take: {runs}")
        print(paths)
        prev_path = None
        for path in paths:
            print(f"Sleeping: {round(speed, 3)} seconds before moving {unit.Name} again")
            sleep(speed)
            Utility.move_unit(self, unit, path[0] * Constants.UNIT_SIZE, path[1] * Constants.UNIT_SIZE)
            
            if prev_path is not None:
                rs = PyGameUtility.RectSettings()
                rs.x = prev_path[0] * Constants.UNIT_SIZE
                rs.y = prev_path[1] * Constants.UNIT_SIZE
                rs.BgColor = Constants.Colors.YELLOW
                rs.Rect = None
                rect_settings = PyGameUtility.create_rect(self, unit.Rect_Settings)
                pygame.display.flip()
            
            # allows wiping out previous path 
            prev_path = path
        return f"{unit.Name} done moving"

    # moves rect x,y cords
    def move_unit(self, unit, x, y):
        unit.Rect_Settings.x = x
        unit.Rect_Settings.y = y
        unit.Rect_Settings.Rect = None
        rect_settings = PyGameUtility.create_rect(self, unit.Rect_Settings)

        print(f"move_unit: {rect_settings.Rect.x}x{rect_settings.Rect.y}")
        pygame.display.update(rect_settings.Rect)  
        pygame.display.flip()
    
        # unit.Rect_Settings.Rect.move_ip(x,y)
        # pygame.display.update(unit.Rect_Settings.Rect)  
        # pygame.display.flip()

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
    def draw_side_panel(self, mouse_pos = None, rect_settings = None, really_draw = True):
        if rect_settings is None:
            rect_settings = PyGameUtility.RectSettings()
            rect_settings.BgColor = Constants.Colors.POOP_BROWN
            rect_settings.FontSize = Constants.SP_BUTTON_TEXT_SIZE
            rect_settings.Rect = pygame.Rect(0, 0, Constants.SP_WIDTH, self.surface.get_height())
            rect_settings.BorderColor = Constants.Colors.GAME_BORDER
            rect_settings.BorderSides = [Constants.BorderSides.RIGHT]
        
        side_panel_rect_settings = PyGameUtility.create_rect(self, rect_settings, ignore_side_panel=True, really_draw=really_draw)
        if really_draw:
            # button for each guy
            i = 1
            unit_button_list = []
            for unit in self.player.selected_race.units:
                unit_x = (Constants.SP_WIDTH / 2) / 2
                unit_y = 60 * i
                unit_width = Constants.SP_WIDTH / 2
                unit_height = unit_width

                rect_settings = PyGameUtility.RectSettings()
                rect_settings.Rect = pygame.Rect(unit_x, unit_y, unit_width, unit_height)
                rect_settings.BgColor = self.player.selected_race.main_color
                rect_settings.BorderColor = self.player.selected_race.secondary_color
                rect_settings.Text = unit["Name"]
                rect_settings.HintName = "unit button text"
                rect_settings.FontSize = Constants.SP_BUTTON_TEXT_SIZE

                PyGameUtility.create_rect(self, rect_settings, ignore_side_panel=True)            
                PyGameUtility.update_rect_with_text(self, rect_settings)

                # update our list to pass back
                unit_button_list.append(rect_settings)
                i = i + 1
                
            if mouse_pos is not None:
                for unit_button in unit_button_list:
                    if unit_button.Rect.collidepoint(mouse_pos):
                        Utility.unit_button_highlighted(self, unit_button, mouse_pos)    

        return side_panel_rect_settings
    
    # the bottom panel shown when one or more units selected
    def create_bottom_panel(self):
        rect_settings = PyGameUtility.RectSettings()
        rect_settings.BgColor = Constants.Colors.COCOA
        rect_settings.BorderColor = Constants.Colors.GAME_BORDER
        rect_settings.BorderSides = [Constants.BorderSides.TOP, Constants.BorderSides.LEFT]
        rect_settings.FontSize = Constants.SP_BUTTON_TEXT_SIZE
        nudge = 2
        rect_settings.x = Constants.SP_WIDTH  + nudge # start at end of SP panel
        rect_settings.y = Constants.SCREEN_HEIGHT - Constants.BP_HEIGHT
        rect_settings.width = Constants.SCREEN_WIDTH - Constants.SP_WIDTH - nudge
        rect_settings.height = self.surface.get_height()
        rect_settings.HintName = "bottom panel main"
        PyGameUtility.create_rect(self, rect_settings, ignore_side_panel=True)

        # button for each guy
        i = 1
        unit_button_list = []
        for unit in self.player.army:
            unit_x = Constants.SP_WIDTH + Constants.PANEL_BUTTON_SPACING
            unit_y = rect_settings.y + Constants.RECT_SIZE
            unit_width = Constants.SP_WIDTH / 2
            unit_height = unit_width

            rect_settings = PyGameUtility.RectSettings()
            rect_settings.Rect = pygame.Rect(unit_x, unit_y, unit_width, unit_height)
            rect_settings.BgColor = self.player.selected_race.main_color
            rect_settings.BorderColor = self.player.selected_race.secondary_color
            rect_settings.Text = unit.Name
            rect_settings.HintName = "unit button text"
            rect_settings.FontSize = Constants.SP_BUTTON_TEXT_SIZE

            PyGameUtility.create_rect(self, rect_settings, ignore_side_panel=True)            
            PyGameUtility.update_rect_with_text(self, rect_settings)

            # update our list to pass back
            unit_button_list.append(rect_settings)
            i = i + 1
            
        return unit_button_list

    # highlights buttons on left side panel
    def unit_button_highlighted(self, rect_settings, mouse_pos):
        self.surface.blit(self.mouse_pointer, mouse_pos)
        rect_settings.FontColor =  self.player.selected_race.hover_text_color
        pygame.draw.rect(self.surface, self.player.selected_race.hover_color, rect_settings.Rect) 
        PyGameUtility.update_rect_with_text(self, rect_settings)
    
    # changed border around unit to indicate it's "selected" - random color border
    def select_unit(self, unit):
        unit.Rect_Settings.BorderColor = Constants.Colors.RANDOM
        unit.Rect_settings = PyGameUtility.create_rect(self, unit.Rect_Settings)
        return unit

    # if a unit_type is specified, we consider this a "unit", otherwise, it's just a rect that could be used for anythign..
    def create_unit(self, unit_type, unit = None):

        if unit is None:
            unit = Unit()
            unit.Rect_Settings = PyGameUtility.RectSettings()
            unit.Rect_Settings.BgColor = self.player.selected_race.main_color
            unit.Rect_Settings.BorderColor = self.player.selected_race.secondary_color            
            unit.Rect_Settings.x = Constants.UNIT_SPAWN_X
            unit.Rect_Settings.y = Constants.UNIT_SPAWN_Y
            unit.Rect_Settings.width = Constants.UNIT_SIZE
            unit.Rect_Settings.height = Constants.UNIT_SIZE
            unit.Name = Names.generate_name(self)
            unit.Type = unit_type
            unit.Rect_Settings.HintName = f"army unit on field: {unit.Name}" # just used for debugging
        
        # create new unit for this guy        
        unit.Rect_Settings = PyGameUtility.create_rect(self, unit.Rect_Settings)
            
        # add to our army list
        found_unit = False
        for army_unit in self.player.army:
            if army_unit.Name == unit.Name:
                found_unit = True
                break
        if not found_unit:
            self.player.army.append(unit)

        return unit


