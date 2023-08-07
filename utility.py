import random
from uuid import uuid4
import pygame

# our stuff
from constants import Constants
from names import Names
from unit import Unit

class Utility:
    class RectSettings:        
        x = 0
        y = 0
        width = 50
        height = 50
        HintName = None
        Rect = None
        Text = None
        Rect = None
        Font = "arialblack"
        Font_Size = Constants.FONT_SIZE
        BG_Color = Constants.Colors.GREEN
        Font_Color = Constants.Colors.BLACK
        BorderColor = None     
        id = None   
        def __init__(self):
            id = uuid4()

    def draw_center_text(self, text, text_color, y, font = None, font_size = None):
        default_font_size = Constants.FONT_SIZE
        if font_size is None:
            font_size = default_font_size            

        if font is None:
            font = pygame.font.SysFont("arialblack", font_size)

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
            left_border_rect = pygame.Rect((rect_settings.Rect.x-Constants.RECT_BORDER_SIZE, rect_settings.Rect.y, Constants.RECT_BORDER_SIZE, rect_settings.Rect.height))
            pygame.draw.rect(self.surface, left_border_color, left_border_rect) 

            # bottom        
            bottom_border_rect = pygame.Rect((rect_settings.Rect.x, rect_settings.Rect.y + rect_settings.Rect.height, rect_settings.Rect.width, Constants.RECT_BORDER_SIZE))
            pygame.draw.rect(self.surface, bottom_border_color, bottom_border_rect)

            # right        
            right_border_rect = pygame.Rect((rect_settings.Rect.x + rect_settings.Rect.width, rect_settings.Rect.y, Constants.RECT_BORDER_SIZE, rect_settings.Rect.height))
            pygame.draw.rect(self.surface, right_border_color, right_border_rect) 

            # top        
            top_border_rect = pygame.Rect((rect_settings.Rect.x, rect_settings.Rect.y - Constants.RECT_BORDER_SIZE, rect_settings.Rect.width, Constants.RECT_BORDER_SIZE))
            pygame.draw.rect(self.surface, top_border_color, top_border_rect) 

        return rect_settings

    def move_unit(self, rect, x, y, main_color):
        rect.move_ip(x, y)
        Utility.create_rect(self, rect, main_color, main_color)        

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

    def create_side_panel(self):
        rect_settings = Utility.RectSettings()
        rect_settings.BG_Color = Constants.Colors.POOP_BROWN
        rect_settings.Font_Size = Constants.SP_BUTTON_TEXT_SIZE
        rect_settings.Rect = pygame.Rect(0, 0, Constants.SP_WIDTH, self.surface.get_height())
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
        rect_settings.BG_Color = Constants.Colors.POOP_BROWN
        rect_settings.Font_Size = Constants.SP_BUTTON_TEXT_SIZE
        rect_settings.x = Constants.SP_WIDTH # start at end of SP panel
        rect_settings.y = Constants.SCREEN_HEIGHT - Constants.BP_HEIGHT
        rect_settings.width = Constants.SCREEN_WIDTH - Constants.SP_WIDTH
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
        print(f"select_unit: {unit}")
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
            unit.Rect_Settings.HintName = f"army unit on field: {unit.Name}" # just used for debugging
            unit.Rect_Settings.x = Constants.UNIT_SPAWN_X
            unit.Rect_Settings.y = Constants.UNIT_SPAWN_Y
            unit.Rect_Settings.width = Constants.RECT_SIZE
            unit.Rect_Settings.height = Constants.RECT_SIZE
            unit.Name = Names.generate_name(self)
            unit.Type = unit_type
        
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


