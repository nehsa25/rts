import random
from time import sleep
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

    # indicates what borders to created, used by create_rect function
    class BorderSides(Enum):
        ALL = 0
        LEFT = 1
        TOP = 2
        RIGHT = 3
        BOTTOM = 4

    class RectSettings:        
        x = 0
        y = 0
        width = 50
        height = 50
        HintName = None
        Rect = None
        Text = None
        Rect = None
        Font = Constants.DEFAULT_FONT
        Font_Size = Constants.FONT_SIZE
        BG_Color = Constants.Colors.GREEN
        Font_Color = Constants.Colors.BLACK
        BorderColor = None   
        BorderSides = None  
        id = None   
        def __init__(self):
            id = uuid4()

    def draw_center_text(self, text, text_color, y, font_name = None, font_size = None):
        default_font_size = Constants.FONT_SIZE
        if font_size is None:
            font_size = default_font_size            

        if font_name is None:
            font = pygame.font.SysFont(Constants.DEFAULT_FONT, font_size)            
        else:
            font =pygame.font.SysFont(font_name, font_size)

        text = font.render(text, True, text_color)
        text_rect = text.get_rect(center=(Constants.SCREEN_WIDTH / 2, y))
        self.surface.blit(text, text_rect)    

    def create_rect_with_center_text(self, text, font, y, total_width):
        text = font.render(text, True, 'black')
        return text.get_rect(center=(total_width / 2, y))

    def update_rect_with_text(self, rect_settings):
        # add text
        font = pygame.font.Font(None, rect_settings.Font_Size)
        unit_text = font.render(rect_settings.Text, True, rect_settings.Font_Color)
        self.surface.blit(unit_text, rect_settings.Rect)  

    def create_rect(self, rect_settings, ignore_side_panel = False):
        if rect_settings.Rect is None:
           rect_settings.Rect = pygame.Rect(rect_settings.x, rect_settings.y, rect_settings.width, rect_settings.height) 

        # ensure rect not in side panel
        if not ignore_side_panel:        
            if rect_settings.Rect.x < Constants.SP_WIDTH:
                rect_settings.Rect.x = Constants.SP_WIDTH

        pygame.draw.rect(self.surface, rect_settings.BG_Color, rect_settings.Rect) # this is what actually causes the rect to show up on screen

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
                left_border_rect = pygame.Rect((rect_settings.Rect.x-Constants.RECT_BORDER_SIZE, rect_settings.Rect.y, Constants.RECT_BORDER_SIZE, rect_settings.Rect.height))
                pygame.draw.rect(self.surface, left_border_color, left_border_rect) 

            # bottom   
            if Utility.BorderSides.ALL in rect_settings.BorderSides or Utility.BorderSides.BOTTOM in rect_settings.BorderSides:     
                bottom_border_rect = pygame.Rect((rect_settings.Rect.x, rect_settings.Rect.y + rect_settings.Rect.height, rect_settings.Rect.width, Constants.RECT_BORDER_SIZE))
                pygame.draw.rect(self.surface, bottom_border_color, bottom_border_rect)

            # right  
            if Utility.BorderSides.ALL in rect_settings.BorderSides or Utility.BorderSides.RIGHT in rect_settings.BorderSides:      
                right_border_rect = pygame.Rect((rect_settings.Rect.x + rect_settings.Rect.width, rect_settings.Rect.y, Constants.RECT_BORDER_SIZE, rect_settings.Rect.height))
                pygame.draw.rect(self.surface, right_border_color, right_border_rect) 

            # top
            if Utility.BorderSides.ALL in rect_settings.BorderSides or Utility.BorderSides.TOP in rect_settings.BorderSides:        
                top_border_rect = pygame.Rect((rect_settings.Rect.x, rect_settings.Rect.y - Constants.RECT_BORDER_SIZE, rect_settings.Rect.width, Constants.RECT_BORDER_SIZE))
                pygame.draw.rect(self.surface, top_border_color, top_border_rect) 

        return rect_settings

    # def draw_grid(self):
    #     blockSize = 1

    #     sp_total_width = Constants.SP_BORDER_SIZE + Constants.SP_WIDTH
    #     remaining_x_total_width = Constants.SCREEN_WIDTH - sp_total_width
    #     total_height = Constants.SCREEN_HEIGHT - (Constants.SP_BORDER_SIZE * 2) - Constants.BP_HEIGHT

    #     for x in range(remaining_x_total_width):
    #         x = x + sp_total_width
    #         for y in range(total_height):
    #             print(f"drawing: {x}, {y}")
    #             rect = pygame.Rect(x, y, blockSize, blockSize)
    #             pygame.draw.rect(self.surface, Constants.Colors.NEON_GREEN, rect, 1)

    def get_grid(self, obstacles):
        UNIT_CAN_MOVE = 1
        UNIT_CANNOT_MOVE = 0
        total_width = Constants.SCREEN_WIDTH
        total_height = Constants.SCREEN_HEIGHT
        matrix = []
        x_line = []
        
        num_Xs = total_width
        num_Ys = total_height

        y = 0
        for x in range(num_Xs):
            if x in range(0, Constants.SP_WIDTH + Constants.SP_BORDER_SIZE):
                x_line.append(UNIT_CANNOT_MOVE)
            else:
                rect = pygame.Rect(x, y, 1, 1) 
                collide = rect.collidelist(obstacles)
                if collide == -1:
                    x_line.append(UNIT_CAN_MOVE)
                else:
                    x_line.append(UNIT_CANNOT_MOVE)

        for y in range(num_Ys):
            matrix.append(x_line)

        return Grid(matrix = matrix)

    # uses speed of unit
    def move_unit_over_time(self, unit, end_x, end_y):
        default_speed = 1
        speed = default_speed - (unit.Type.speed * .1)        
        start_x_grid = int(unit.Rect_Settings.x)
        start_y_grid = int(unit.Rect_Settings.y)
        end_x_grid = int(end_x)
        end_y_grid = int(end_y)

        print(f"Moving {unit.Name} at {speed} speed from ({start_x_grid}, {start_y_grid}) to ({end_x_grid}, {end_y_grid})")

        start = self.grid.node(start_x_grid, start_y_grid)
        end = self.grid.node(end_x_grid, end_y_grid)
        finder = AStarFinder()
        paths, runs = finder.find_path(start, end, self.grid)
        print(paths)
        for path in paths:
            print(f"Sleeping: {speed} seconds before moving {unit.Name} again")
            sleep(speed)
            Utility.move_unit(self, unit, path[0], path[1])
        print(f"number runs path will take: {runs}")

    # moves rect x,y cords
    def move_unit(self, unit, x, y):
        unit.Rect_Settings.x = x
        unit.Rect_Settings.y = y
        unit.Rect_Settings.Rect = None
        Utility.create_rect(self, unit.Rect_Settings)        

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
    def create_side_panel(self):
        rect_settings = Utility.RectSettings()
        rect_settings.BG_Color = Constants.Colors.POOP_BROWN
        rect_settings.Font_Size = Constants.SP_BUTTON_TEXT_SIZE
        rect_settings.Rect = pygame.Rect(0, 0, Constants.SP_WIDTH, self.surface.get_height())
        rect_settings.BorderColor = Constants.Colors.GAME_BORDER
        rect_settings.BorderSides = [Utility.BorderSides.RIGHT]
        Utility.create_rect(self, rect_settings, ignore_side_panel=True)

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
            rect_settings.BG_Color = self.player.selected_race.main_color
            rect_settings.BorderColor = self.player.selected_race.secondary_color
            rect_settings.Text = unit["Name"]
            rect_settings.HintName = "unit button text"
            rect_settings.Font_Size = Constants.SP_BUTTON_TEXT_SIZE

            Utility.create_rect(self, rect_settings, ignore_side_panel=True)            
            Utility.update_rect_with_text(self, rect_settings)

            # update our list to pass back
            unit_button_list.append(rect_settings)
            i = i + 1
            
        return unit_button_list

    # the bottom panel shown when one or more units selected
    def create_bottom_panel(self):
        rect_settings = Utility.RectSettings()
        rect_settings.BG_Color = Constants.Colors.COCOA
        rect_settings.BorderColor = Constants.Colors.GAME_BORDER
        rect_settings.BorderSides = [Utility.BorderSides.TOP, Utility.BorderSides.LEFT]
        rect_settings.Font_Size = Constants.SP_BUTTON_TEXT_SIZE
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
            rect_settings.BG_Color = self.player.selected_race.main_color
            rect_settings.BorderColor = self.player.selected_race.secondary_color
            rect_settings.Text = unit.Name
            rect_settings.HintName = "unit button text"
            rect_settings.Font_Size = Constants.SP_BUTTON_TEXT_SIZE

            Utility.create_rect(self, rect_settings, ignore_side_panel=True)            
            Utility.update_rect_with_text(self, rect_settings)

            # update our list to pass back
            unit_button_list.append(rect_settings)
            i = i + 1
            
        return unit_button_list

    def unit_button_highlighted(self, rect_settings):
        rect_settings.Font_Color =  self.player.selected_race.hover_text_color
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
            unit.Rect_Settings.BG_Color = self.player.selected_race.main_color
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


