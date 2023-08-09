import random
from time import sleep
import time
from uuid import uuid4
import pygame
from enum import Enum
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.grid import Grid

# our stuff
from constants import Constants
from names import Names
from unit import Unit

class Utility:
    finder = AStarFinder()

    # used to determine how big of water pools to make
    class DensityTypes(Enum):
        Tiny = 0
        Small = 1
        Medium = 2
        Large = 3
        Huge = 4

        @classmethod
        def get_random_size(cls):
            side = random.choice(cls._member_names_).lower()
            return side.lower()

    # indicates what borders to created, used by create_rect function
    class BorderSides(Enum):
        ALL = 0
        LEFT = 1
        TOP = 2
        RIGHT = 3
        BOTTOM = 4

        # assist with building terrain
        @classmethod
        def get_random_side(cls):
            side = random.choice(cls._member_names_).lower()
            return side.lower()

    class RectSettings:        
        x = 0
        y = 0
        width = 50
        height = 50
        HintName = None
        Rect = None
        Text = None
        Rect = None
        FontName = Constants.DEFAULT_FONT_NAME
        FontSize = Constants.FONT_SIZE
        BgColor = Constants.Colors.GREEN
        FontColor = Constants.Colors.BLACK
        BorderColor = None   
        BorderSides = None  
        BorderSize = Constants.RECT_BORDER_SIZE
        id = None   
        def __init__(self):
            id = uuid4()

    def draw_center_text(self, text, text_color, y, font_name = None, font_size = None):
        default_font_size = Constants.FONT_SIZE
        if font_size is None:
            font_size = default_font_size            

        if font_name is None:
            font = pygame.font.SysFont(Constants.DEFAULT_FONT_NAME, font_size)            
        else:
            font =pygame.font.SysFont(font_name, font_size)

        text = font.render(text, True, text_color)
        text_rect = text.get_rect(center=(Constants.SCREEN_WIDTH / 2, y))
        self.surface.blit(text, text_rect)    

    # used for "gamebutton" class
    def create_rect_with_center_text(self, text, font, y, total_width):
        font_render = font.render(text, True, 'black')
        rect = font_render.get_rect(center=(total_width / 2, y))
        return rect

    def update_rect_with_text(self, rect_settings):
        # add text
        font = pygame.font.Font(None, rect_settings.FontSize)
        unit_text = font.render(rect_settings.Text, True, rect_settings.FontColor)
        self.surface.blit(unit_text, rect_settings.Rect)  

    def load_grid(self):
                # get grid of screen based on unit size
                self.grid = Utility.get_empty_grid(self)
                
                #  refresh side panel / highlight a unit that's hovered over
                self.side_panel_rects = Utility.draw_side_panel(self, really_draw=False)

                # generate our obstacles
                self.obstacles = Utility.create_terrain(self, self.grid, self.side_panel_rects)

                # update grid with nodes we cannot walk on
                self.grid = Utility.update_grid_with_terrain(self, self.grid, self.obstacles)
                
    def loop_fonts(self, font_name, y):
            rand_x = random.randint(0, 800)
            font = pygame.font.SysFont(font_name, 36)  
            text = font.render(f"Human ({font_name})", True, 'black')
            rect = text.get_rect(x=rand_x, y=y)
            self.surface.blit(text, rect)

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
            size = Utility.DensityTypes.get_random_size() 
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
                side = Utility.BorderSides.get_random_side()                 
                if side == "left":
                    x += -1
                elif side == "right":
                    x += 1
                elif side == "top":
                    y += 1
                elif side == "bottom":
                    y += -1
   
                final_x = x * Unit.UNIT_SIZE
                final_y = y * Unit.UNIT_SIZE
                rect = pygame.Rect(final_x, final_y, Unit.UNIT_SIZE, Unit.UNIT_SIZE)
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
            size = Utility.DensityTypes.get_random_size() 
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
                side = Utility.BorderSides.get_random_side()                 
                if side == "left":
                    x += -1
                elif side == "right":
                    x += 1
                elif side == "top":
                    y += 1
                elif side == "bottom":
                    y += -1
   
                final_x = x * Unit.UNIT_SIZE
                final_y = y * Unit.UNIT_SIZE
                rect = pygame.Rect(final_x, final_y, Unit.UNIT_SIZE, Unit.UNIT_SIZE)
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
            size = Utility.DensityTypes.get_random_size() 
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
                side = Utility.BorderSides.get_random_side()                 
                if side == "left":
                    x += -1
                elif side == "right":
                    x += 1
                elif side == "top":
                    y += 1
                elif side == "bottom":
                    y += -1
   
                final_x = x * Unit.UNIT_SIZE
                final_y = y * Unit.UNIT_SIZE
                rect = pygame.Rect(final_x, final_y, Unit.UNIT_SIZE, Unit.UNIT_SIZE)
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
            size = Utility.DensityTypes.get_random_size() 
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
                side = Utility.BorderSides.get_random_side()                 
                if side == "left":
                    x += -1
                elif side == "right":
                    x += 1
                elif side == "top":
                    y += 1
                elif side == "bottom":
                    y += -1
   
                final_x = x * Unit.UNIT_SIZE
                final_y = y * Unit.UNIT_SIZE
                rect = pygame.Rect(final_x, final_y, Unit.UNIT_SIZE, Unit.UNIT_SIZE)
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
    
    def create_rect(self, rect_settings, ignore_side_panel = False, really_draw = True):
        if rect_settings.Rect is None:
           rect_settings.Rect = pygame.Rect(rect_settings.x, rect_settings.y, rect_settings.width, rect_settings.height) 

        # ensure rect not in side panel
        if not ignore_side_panel:        
            if rect_settings.Rect.x < Constants.SP_WIDTH:
                rect_settings.Rect.x = Constants.SP_WIDTH

        if really_draw:
            pygame.draw.rect(self.surface, rect_settings.BgColor, rect_settings.Rect) # this is what actually causes the rect to show up on screen

            if rect_settings.BorderColor is not None:
                if rect_settings.BorderSides is None:
                    rect_settings.BorderSides = [Utility.BorderSides.ALL]
                if rect_settings.BorderColor is not Constants.Colors.RANDOM:
                    left_border_color = rect_settings.BorderColor
                    bottom_border_color = rect_settings.BorderColor
                    right_border_color = rect_settings.BorderColor
                    top_border_color = rect_settings.BorderColor
                else:                
                    left_border_color = (random.choice(range(256)), random.choice(range(256)), random.choice(range(256)))                
                    bottom_border_color = (random.choice(range(256)), random.choice(range(256)), random.choice(range(256)))                
                    right_border_color = (random.choice(range(256)), random.choice(range(256)), random.choice(range(256)))                
                    top_border_color = (random.choice(range(256)), random.choice(range(256)), random.choice(range(256)))

                # left
                if Utility.BorderSides.ALL in rect_settings.BorderSides or Utility.BorderSides.LEFT in rect_settings.BorderSides:
                    left_border_rect = pygame.Rect((rect_settings.Rect.x-rect_settings.BorderSize, rect_settings.Rect.y, rect_settings.BorderSize, rect_settings.Rect.height))
                    pygame.draw.rect(self.surface, left_border_color, left_border_rect) 

                # bottom   
                if Utility.BorderSides.ALL in rect_settings.BorderSides or Utility.BorderSides.BOTTOM in rect_settings.BorderSides:     
                    bottom_border_rect = pygame.Rect((rect_settings.Rect.x, rect_settings.Rect.y + rect_settings.Rect.height, rect_settings.Rect.width, rect_settings.BorderSize))
                    pygame.draw.rect(self.surface, bottom_border_color, bottom_border_rect)

                # right  
                if Utility.BorderSides.ALL in rect_settings.BorderSides or Utility.BorderSides.RIGHT in rect_settings.BorderSides:      
                    right_border_rect = pygame.Rect((rect_settings.Rect.x + rect_settings.Rect.width, rect_settings.Rect.y, rect_settings.BorderSize, rect_settings.Rect.height))
                    pygame.draw.rect(self.surface, right_border_color, right_border_rect) 

                # top
                if Utility.BorderSides.ALL in rect_settings.BorderSides or Utility.BorderSides.TOP in rect_settings.BorderSides:        
                    top_border_rect = pygame.Rect((rect_settings.Rect.x, rect_settings.Rect.y - rect_settings.BorderSize, rect_settings.Rect.width, rect_settings.BorderSize))
                    pygame.draw.rect(self.surface, top_border_color, top_border_rect) 

        return rect_settings

    # returns all obstablces in a single list of dictionaries
    def create_terrain(self, grid, side_panel_rect):
        create_terrain_start = time.perf_counter()  
        obstacles = []

        # create side panel tiles
        for h in range(0, int(side_panel_rect.Rect.height / Unit.UNIT_SIZE)):
            for w in range(0, int(side_panel_rect.Rect.width / Unit.UNIT_SIZE)):
                rand_node = grid.nodes[h]
                rand_cord = rand_node[w]
                rect = pygame.Rect(rand_cord.x * Unit.UNIT_SIZE, rand_cord.y * Unit.UNIT_SIZE, Unit.UNIT_SIZE, Unit.UNIT_SIZE)
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

    def show_grid(self, grid, mouse_pos):        
        show_grid_start = time.perf_counter()     
        self.surface.blit(self.mouse_pointer, mouse_pos)           
        for node in grid.nodes:
            for item in node:
                newx = item.x * Unit.UNIT_SIZE
                newy = item.y * Unit.UNIT_SIZE
                rect_settings = Utility.RectSettings()
                rect_settings.x = newx
                rect_settings.y = newy
                if item.walkable:
                    rect_settings.BgColor = Constants.Colors.GREEN_DARK
                else:
                    rect_settings.BgColor = Constants.Colors.BURNT_ORANGE
                rect_settings.BorderColor = Constants.Colors.NEON_GREEN
                rect_settings.BorderSize = 1
                Utility.create_rect(self, rect_settings, True)
        show_grid_end = time.perf_counter()
        print(f"show_grid timings: {round(60 - (show_grid_end - show_grid_start), 2)} second(s)")

        # for x in range(0, Constants.SCREEN_WIDTH, Unit.UNIT_SIZE): 
        #     for y in range(0, Constants.SCREEN_HEIGHT, Unit.UNIT_SIZE):
        #         print(f"drawing point: {x}, {y}") # (0, 0), (0, 15)
        #         rect = pygame.Rect(x, y, Unit.UNIT_SIZE-1, Unit.UNIT_SIZE-1)
        #         pygame.draw.rect(self.surface, Constants.Colors.BLACK, rect, Unit.UNIT_SIZE)

    def get_empty_grid(self):
        get_empty_start = time.perf_counter()   
        print(f"Generating grid based on {Constants.SCREEN_WIDTH}x{Constants.SCREEN_HEIGHT}")
        matrix = []      
        for y in range(0, Constants.SCREEN_HEIGHT, Unit.UNIT_SIZE):
            x_line = []
            for x in range(0, Constants.SCREEN_WIDTH, Unit.UNIT_SIZE):
                print(f"Point: {x}x{y}")
                x_line.append(1)
            matrix.append(x_line)

        print("get_empty_grid: Generating pathfinding grid...")
        grid =  Grid(matrix = matrix)
        print("get_empty_grid: Done...")
        get_empty_end = time.perf_counter()
        print(f"get_empty_grid timings: {round(60 - (get_empty_end - get_empty_start), 2)} second(s)")
        return grid

    def update_grid_with_terrain(self, grid, obstacle_types):
        get_grid_start = time.perf_counter() 
        print("get_grid: Updating pathfinding grid with terrain...")
        UNIT_CAN_MOVE = True
        UNIT_CANNOT_MOVE = False     
        for node in grid.nodes:
            for item in node:
                collisions = [i["rect"] for i in obstacle_types]
                rect = pygame.Rect(item.x * Unit.UNIT_SIZE, item.y * Unit.UNIT_SIZE, Unit.UNIT_SIZE, Unit.UNIT_SIZE)
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
        start_x_grid = int(unit.Rect_Settings.x  / Unit.UNIT_SIZE)
        start_y_grid = int(unit.Rect_Settings.y  / Unit.UNIT_SIZE)
        end_x_grid = int(end_x / Unit.UNIT_SIZE)
        end_y_grid = int(end_y / Unit.UNIT_SIZE)

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
            Utility.move_unit(self, unit, path[0] * Unit.UNIT_SIZE, path[1] * Unit.UNIT_SIZE)
            
            if prev_path is not None:
                rs = Utility.RectSettings()
                rs.x = prev_path[0] * Unit.UNIT_SIZE
                rs.y = prev_path[1] * Unit.UNIT_SIZE
                rs.BgColor = Constants.Colors.YELLOW
                rs.Rect = None
                rect_settings = Utility.create_rect(self, unit.Rect_Settings)
                pygame.display.flip()
            
            # allows wiping out previous path 
            prev_path = path
        return f"{unit.Name} done moving"

    # moves rect x,y cords
    def move_unit(self, unit, x, y):
        unit.Rect_Settings.x = x
        unit.Rect_Settings.y = y
        unit.Rect_Settings.Rect = None
        rect_settings = Utility.create_rect(self, unit.Rect_Settings)
        pygame.display.update(rect_settings.Rect)  

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
            rect_settings = Utility.RectSettings()
            rect_settings.BgColor = Constants.Colors.POOP_BROWN
            rect_settings.FontSize = Constants.SP_BUTTON_TEXT_SIZE
            rect_settings.Rect = pygame.Rect(0, 0, Constants.SP_WIDTH, self.surface.get_height())
            rect_settings.BorderColor = Constants.Colors.GAME_BORDER
            rect_settings.BorderSides = [Utility.BorderSides.RIGHT]
        
        side_panel_rect_settings = Utility.create_rect(self, rect_settings, ignore_side_panel=True, really_draw=really_draw)
        if really_draw:
            # button for each guy
            i = 1
            unit_button_list = []
            for unit in self.player.selected_race.units:
                unit_x = (Constants.SP_WIDTH / 2) / 2
                unit_y = 60 * i
                unit_width = Constants.SP_WIDTH / 2
                unit_height = unit_width

                rect_settings = Utility.RectSettings()
                rect_settings.Rect = pygame.Rect(unit_x, unit_y, unit_width, unit_height)
                rect_settings.BgColor = self.player.selected_race.main_color
                rect_settings.BorderColor = self.player.selected_race.secondary_color
                rect_settings.Text = unit["Name"]
                rect_settings.HintName = "unit button text"
                rect_settings.FontSize = Constants.SP_BUTTON_TEXT_SIZE

                Utility.create_rect(self, rect_settings, ignore_side_panel=True)            
                Utility.update_rect_with_text(self, rect_settings)

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
        rect_settings = Utility.RectSettings()
        rect_settings.BgColor = Constants.Colors.COCOA
        rect_settings.BorderColor = Constants.Colors.GAME_BORDER
        rect_settings.BorderSides = [Utility.BorderSides.TOP, Utility.BorderSides.LEFT]
        rect_settings.FontSize = Constants.SP_BUTTON_TEXT_SIZE
        nudge = 2
        rect_settings.x = Constants.SP_WIDTH  + nudge # start at end of SP panel
        rect_settings.y = Constants.SCREEN_HEIGHT - Constants.BP_HEIGHT
        rect_settings.width = Constants.SCREEN_WIDTH - Constants.SP_WIDTH - nudge
        rect_settings.height = self.surface.get_height()
        rect_settings.HintName = "bottom panel main"
        Utility.create_rect(self, rect_settings, ignore_side_panel=True)

        # button for each guy
        i = 1
        unit_button_list = []
        for unit in self.player.army:
            unit_x = Constants.SP_WIDTH + Constants.PANEL_BUTTON_SPACING
            unit_y = rect_settings.y + Constants.RECT_SIZE
            unit_width = Constants.SP_WIDTH / 2
            unit_height = unit_width

            rect_settings = Utility.RectSettings()
            rect_settings.Rect = pygame.Rect(unit_x, unit_y, unit_width, unit_height)
            rect_settings.BgColor = self.player.selected_race.main_color
            rect_settings.BorderColor = self.player.selected_race.secondary_color
            rect_settings.Text = unit.Name
            rect_settings.HintName = "unit button text"
            rect_settings.FontSize = Constants.SP_BUTTON_TEXT_SIZE

            Utility.create_rect(self, rect_settings, ignore_side_panel=True)            
            Utility.update_rect_with_text(self, rect_settings)

            # update our list to pass back
            unit_button_list.append(rect_settings)
            i = i + 1
            
        return unit_button_list

    # highlights buttons on left side panel
    def unit_button_highlighted(self, rect_settings, mouse_pos):
        self.surface.blit(self.mouse_pointer, mouse_pos)
        rect_settings.FontColor =  self.player.selected_race.hover_text_color
        pygame.draw.rect(self.surface, self.player.selected_race.hover_color, rect_settings.Rect) 
        Utility.update_rect_with_text(self, rect_settings)
    
    # changed border around unit to indicate it's "selected" - random color border
    def select_unit(self, unit):
        unit.Rect_Settings.BorderColor = Constants.Colors.RANDOM
        unit.Rect_settings = Utility.create_rect(self, unit.Rect_Settings)
        return unit

    # if a unit_type is specified, we consider this a "unit", otherwise, it's just a rect that could be used for anythign..
    def create_unit(self, unit_type, unit = None):

        if unit is None:
            unit = Unit()
            unit.Rect_Settings = Utility.RectSettings()
            unit.Rect_Settings.BgColor = self.player.selected_race.main_color
            unit.Rect_Settings.BorderColor = self.player.selected_race.secondary_color            
            unit.Rect_Settings.x = Constants.UNIT_SPAWN_X
            unit.Rect_Settings.y = Constants.UNIT_SPAWN_Y
            unit.Rect_Settings.width = Unit.UNIT_SIZE
            unit.Rect_Settings.height = Unit.UNIT_SIZE
            unit.Name = Names.generate_name(self)
            unit.Type = unit_type
            unit.Rect_Settings.HintName = f"army unit on field: {unit.Name}" # just used for debugging
        
        # create new unit for this guy        
        unit.Rect_Settings = Utility.create_rect(self, unit.Rect_Settings)
            
        # add to our army list
        found_unit = False
        for army_unit in self.player.army:
            if army_unit.Name == unit.Name:
                found_unit = True
                break
        if not found_unit:
            self.player.army.append(unit)

        return unit


