import random
import pygame

# our stuff
from colors import Colors

class Utility:
    def draw_center_text(self, text, font, text_color, y):
        text = font.render(text, True, text_color)
        text_rect = text.get_rect(center=(self.SCREEN_WIDTH / 2, y))
        self.surface.blit(text, text_rect)    

    def get_center_text(self, text, font, y, total_width):
        text = font.render(text, True, 'black')
        return text.get_rect(center=(total_width / 2, y))
        
    def create_rect_with_border(self, rect, main_color, border_color = None, ignore_side_panel = False):
        
        # ensure rect not in side panel
        if not ignore_side_panel:        
            if rect.x <= self.SIDE_PANEL_WIDTH:
                rect.x = self.SIDE_PANEL_WIDTH

        unit = []
        unit.append(rect)
        
        border_width = 2
        pygame.draw.rect(self.surface, main_color, rect) # this is what actually causes the rect to show up on screen

        # left
        if border_color is not None:
            left_border_color = border_color
            bottom_border_color = border_color
            right_border_color = border_color
            top_border_color = border_color
        else:
            left_border_color = (random.choice(range(256)), random.choice(range(256)), random.choice(range(256)))
            bottom_border_color = (random.choice(range(256)), random.choice(range(256)), random.choice(range(256)))
            right_border_color = (random.choice(range(256)), random.choice(range(256)), random.choice(range(256)))
            top_border_color = (random.choice(range(256)), random.choice(range(256)), random.choice(range(256)))

        left_border_rect = pygame.Rect((rect.x-border_width, rect.y, border_width, rect.height))
        pygame.draw.rect(self.surface, left_border_color, left_border_rect) # this is what actually causes the rect to show up on screen
        unit.append(left_border_rect)

        # bottom        
        bottom_border_rect = pygame.Rect((rect.x, rect.y + rect.height, rect.width, border_width))
        pygame.draw.rect(self.surface, bottom_border_color, bottom_border_rect) # this is what actually causes the rect to show up on screen
        unit.append(bottom_border_rect)

        # right        
        right_border_rect = pygame.Rect((rect.x + rect.width, rect.y, border_width, rect.height))
        pygame.draw.rect(self.surface, right_border_color, right_border_rect) # this is what actually causes the rect to show up on screen
        unit.append(right_border_rect)

        # top        
        top_border_rect = pygame.Rect((rect.x, rect.y - border_width, rect.width, border_width))
        pygame.draw.rect(self.surface, top_border_color, top_border_rect) # this is what actually causes the rect to show up on screen
        unit.append(top_border_rect)

        # print(unit)
        return unit
        pass
    
    def move_unit(self, rect, x, y, main_color):
        rects = Utility.create_rect_with_border(self, rect, main_color)        
        for edge in rects:
            edge.move_ip(x, y)

    def update_rect_text(self, text, rect):
        # add text
        font = pygame.font.Font(None, self.SIDE_PANEL_TEXT)
        unit_text = font.render(text, True, Colors.BLACK)
        self.surface.blit(unit_text, rect)
        return rect        

    def create_side_panel(self):
        side_panel = pygame.Rect(0, 0, self.SIDE_PANEL_WIDTH, self.surface.get_height())
        side_panel_list = Utility.create_rect_with_border(self, side_panel, Colors.POOP_BROWN, Colors.BLACK, True)

        # button for each guy
        i = 1
        unit_list = []
        for unit in self.selected_race.units:
            unit_x = (self.SIDE_PANEL_WIDTH / 2) / 2
            unit_y = 60 * i
            unit_width = self.SIDE_PANEL_WIDTH / 2
            unit_height = unit_width
            unit_rect = pygame.Rect(unit_x, unit_y, unit_width, unit_height)
            Utility.create_rect_with_border(self, unit_rect, unit["Color"], Colors.HUNTER_GREEN, True)
            i = i + 1
            rect = Utility.update_rect_text(self, unit["Name"], unit_rect)

            # update our list to pass back
            unit_item = dict(name = unit["Name"], unit_rect = unit_rect)
            unit_list.append(unit_item)
            
        return side_panel_list, unit_list

    def unit_button_highlighted(self, unit):
        print(f"Hovered on: {unit}")
        pygame.draw.rect(self.surface, Colors.FUCHSIA, unit["unit_rect"]) 
