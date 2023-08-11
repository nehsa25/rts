import random
import time
from uuid import uuid4
import pygame
from constants import Constants

class PygameUtilities:  
    font = None
    surface = None

    class RectSettings:        
        x = 0
        y = 0
        Width = 50
        Height = 50
        HintName = None
        Rect = None
        Text = None
        Rect = None
        Font = None
        FontName = Constants.DEFAULT_FONT_NAME
        FontSize = Constants.FONT_SIZE
        BgColor = Constants.Colors.GREEN
        FontColor = Constants.Colors.BLACK
        BorderColor = None   
        BorderSides = None  
        BorderSize = Constants.RECT_BORDER_SIZE
        id = None   
        def __init__(self):
            self.id = uuid4()

    def __init__(self):
        pygame.init() # initialize the pygame module
        self.font = pygame.font.SysFont(Constants.DEFAULT_FONT_NAME, Constants.FONT_SIZE)
        self.surface = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))

    def loop_fonts(self, font_name, y):
        rand_x = random.randint(0, 800)
        font = pygame.font.SysFont(font_name, 36)  
        text = font.render(f"Human ({font_name})", True, 'black')
        rect = text.get_rect(x=rand_x, y=y)
        self.surface.blit(text, rect)

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

    def create_rect(self, rs, ignore_side_panel = False, really_draw = True):
        if rs.Rect is None:
           rs.Rect = pygame.Rect(rs.x, rs.y, rs.Width, rs.Height) 

        # ensure these match always
        rs.x = rs.Rect.x
        rs.y = rs.Rect.y
        rs.Width = rs.Rect.width
        rs.Height = rs.Rect.height

        # ensure rect not in side panel
        if not ignore_side_panel:        
            if rs.Rect.x < Constants.SP_WIDTH:
                rs.Rect.x = Constants.SP_WIDTH

        if really_draw:
            pygame.draw.rect(self.surface, rs.BgColor, rs.Rect) # this is what actually causes the rect to show up on screen
            if rs.BorderColor is not None:
                pygame.draw.rect(self.surface, rs.BgColor, rs.Rect)
                if rs.BorderSides is None:
                    rs.BorderSides = [Constants.BorderSides.ALL]
                if rs.BorderColor is not Constants.Colors.RANDOM:
                    left_border_color = rs.BorderColor
                    bottom_border_color = rs.BorderColor
                    right_border_color = rs.BorderColor
                    top_border_color = rs.BorderColor
                else:                
                    left_border_color = (random.choice(range(256)), random.choice(range(256)), random.choice(range(256)))                
                    bottom_border_color = (random.choice(range(256)), random.choice(range(256)), random.choice(range(256)))                
                    right_border_color = (random.choice(range(256)), random.choice(range(256)), random.choice(range(256)))                
                    top_border_color = (random.choice(range(256)), random.choice(range(256)), random.choice(range(256)))

                # left
                if Constants.BorderSides.ALL in rs.BorderSides or Constants.BorderSides.LEFT in rs.BorderSides:
                    left_x = rs.Rect.x
                    left_y = rs.Rect.y
                    rect = pygame.Rect((left_x, left_y, rs.BorderSize, rs.Rect.height))
                    pygame.draw.rect(self.surface, left_border_color, rect) 

                # bottom   
                if Constants.BorderSides.ALL in rs.BorderSides or Constants.BorderSides.BOTTOM in rs.BorderSides:     
                    bottom_x = rs.Rect.x + rs.BorderSize
                    bottom_y = rs.Rect.y + rs.Rect.height - rs.BorderSize
                    rect = pygame.Rect((bottom_x, bottom_y, rs.Rect.width - rs.BorderSize, rs.BorderSize))
                    pygame.draw.rect(self.surface, bottom_border_color, rect)

                # right  
                if Constants.BorderSides.ALL in rs.BorderSides or Constants.BorderSides.RIGHT in rs.BorderSides:      
                    right_x = rs.Rect.x + rs.Rect.width - rs.BorderSize
                    right_y = rs.Rect.y
                    rect = pygame.Rect((right_x, right_y, rs.BorderSize, rs.Rect.height))
                    pygame.draw.rect(self.surface, right_border_color, rect) 

                # top
                if Constants.BorderSides.ALL in rs.BorderSides or Constants.BorderSides.TOP in rs.BorderSides:        
                    top_x = rs.Rect.x + rs.BorderSize
                    top_y = rs.Rect.y
                    rect = pygame.Rect((top_x, top_y, rs.Rect.width - rs.BorderSize, rs.BorderSize))
                    pygame.draw.rect(self.surface, top_border_color, rect) 

        # add text
        if rs.Text is not None:  
            if rs.FontColor is None:
                rs.FontColor = Constants.Colors.NEON_GREEN
            if rs.Font is None:
                rs.Font =  self.font

            # unit_text = rs.Font.render(rs.Text, True, rs.FontColor)
            # rect = unit_text.get_rect(x=rs.x, y=rs.y)
            # self.surface.blit(unit_text, rect)

            self.place_text(rs.Text, rs.x, rs.y, font=rs.Font, color=rs.FontColor)

        return rs

    # used for "gamebutton" class
    def create_rect_with_center_text(self, text, font, y, total_width):
        font_render = font.render(text, True, 'black')
        rect = font_render.get_rect(center=(total_width / 2, y))
        return rect

    def place_text(self, text, initial_x, initial_y, font, color=pygame.Color('black')):
        words = [word.split(' ') for word in text.splitlines()] 
        space = font.size(' ')[0]
        max_width, max_height = self.surface.get_size()
        x = initial_x
        y = initial_y
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = initial_x  # Reset the x.
                    y += word_height  # Start on new row.
                self.surface.blit(word_surface, (x, y))
                x += word_width + space
            x = initial_x # Reset the x.
            y += word_height  # Start on new row.
