import random
import pygame

# our stuff
from constants import Constants
from unit import Unit

class Utility:
    class RectSettings:        
        RECT_SIZE = 5
        RECT_BORDER_SIZE = 2
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
        def __init__(self):
            pass

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
            left_border_rect = pygame.Rect((rect_settings.Rect.x-Utility.RectSettings.RECT_BORDER_SIZE, rect_settings.Rect.y, Utility.RectSettings.RECT_BORDER_SIZE, rect_settings.Rect.height))
            pygame.draw.rect(self.surface, left_border_color, left_border_rect) 

            # bottom        
            bottom_border_rect = pygame.Rect((rect_settings.Rect.x, rect_settings.Rect.y + rect_settings.Rect.height, rect_settings.Rect.width, Utility.RectSettings.RECT_BORDER_SIZE))
            pygame.draw.rect(self.surface, bottom_border_color, bottom_border_rect)

            # right        
            right_border_rect = pygame.Rect((rect_settings.Rect.x + rect_settings.Rect.width, rect_settings.Rect.y, Utility.RectSettings.RECT_BORDER_SIZE, rect_settings.Rect.height))
            pygame.draw.rect(self.surface, right_border_color, right_border_rect) 

            # top        
            top_border_rect = pygame.Rect((rect_settings.Rect.x, rect_settings.Rect.y - Utility.RectSettings.RECT_BORDER_SIZE, rect_settings.Rect.width, Utility.RectSettings.RECT_BORDER_SIZE))
            pygame.draw.rect(self.surface, top_border_color, top_border_rect) 

        return rect_settings

    def move_unit(self, rect, x, y, main_color):
        rect.move_ip(x, y)
        Utility.create_rect(self, rect, main_color, main_color)        

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

    def unit_button_highlighted(self, rect_settings):
        rect_settings.Font_Color =  self.player.selected_race.hover_text_color
        pygame.draw.rect(self.surface, self.player.selected_race.hover_color, rect_settings.Rect) 
        Utility.update_rect_with_text(self, rect_settings)
    
    # changed border around unit to indicate it's "selected" - random color border
    def select_unit(self, unit):
        print(f"select_unit: {unit}")
        # change border, skip [0] as it's the "Main" rect
        first = True
        for unit_item in unit:
            if first == True:
                first = False
            else:
                for newunit in unit["unit_rect"]:
                    # rect_settings = Utility.RectSettings()
                    # rect_settings.BG_Color = self.player.selected_race.main_color
                    # rect_settings.BorderColor = Constants.Colors.RANDOM
                    print("refactor this..")

    # if a unit_type is specified, we consider this a "unit", otherwise, it's just a rect that could be used for anythign..
    def create_unit(self, unit_name, unit_type):
        rect_settings = Utility.RectSettings()
        rect_settings.BG_Color = self.player.selected_race.main_color
        rect_settings.BorderColor = self.player.selected_race.secondary_color
        rect_settings.HintName = unit_name # just used for debugging
        rect_settings = Utility.create_rect(self, rect_settings)
        unit = Unit()
        unit.Name = unit_name
        unit.Rect = rect_settings.Rect
        unit.Type = unit_type
            
        # add to our army list
        found_unit = False
        for army_unit in self.player.army:
            if army_unit.Name == unit_name:
                found_unit = True
                break
        if not found_unit:
            self.player.army.append(unit)

        return unit


