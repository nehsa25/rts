import random
import time
from uuid import uuid4
import pygame
from constants import Constants
from pathfinding.core.grid import Grid

class PygameUtilities:  
    font = None
    surface = None

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
                pygame.draw.rect(self.surface, rect_settings.BgColor, rect_settings.Rect)
                if rect_settings.BorderSides is None:
                    rect_settings.BorderSides = [Constants.BorderSides.ALL]
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
                if Constants.BorderSides.ALL in rect_settings.BorderSides or Constants.BorderSides.LEFT in rect_settings.BorderSides:
                    left_x = rect_settings.Rect.x
                    left_y = rect_settings.Rect.y
                    rect = pygame.Rect((left_x, left_y, rect_settings.BorderSize, rect_settings.Rect.height))
                    pygame.draw.rect(self.surface, left_border_color, rect) 

                # bottom   
                if Constants.BorderSides.ALL in rect_settings.BorderSides or Constants.BorderSides.BOTTOM in rect_settings.BorderSides:     
                    bottom_x = rect_settings.Rect.x + rect_settings.BorderSize
                    bottom_y = rect_settings.Rect.y + rect_settings.Rect.height - rect_settings.BorderSize
                    rect = pygame.Rect((bottom_x, bottom_y, rect_settings.Rect.width - rect_settings.BorderSize, rect_settings.BorderSize))
                    pygame.draw.rect(self.surface, bottom_border_color, rect)

                # right  
                if Constants.BorderSides.ALL in rect_settings.BorderSides or Constants.BorderSides.RIGHT in rect_settings.BorderSides:      
                    right_x = rect_settings.Rect.x + rect_settings.Rect.width - rect_settings.BorderSize
                    right_y = rect_settings.Rect.y
                    rect = pygame.Rect((right_x, right_y, rect_settings.BorderSize, rect_settings.Rect.height))
                    pygame.draw.rect(self.surface, right_border_color, rect) 

                # top
                if Constants.BorderSides.ALL in rect_settings.BorderSides or Constants.BorderSides.TOP in rect_settings.BorderSides:        
                    top_x = rect_settings.Rect.x + rect_settings.BorderSize
                    top_y = rect_settings.Rect.y
                    rect = pygame.Rect((top_x, top_y, rect_settings.Rect.width - rect_settings.BorderSize, rect_settings.BorderSize))
                    pygame.draw.rect(self.surface, top_border_color, rect) 

        return rect_settings

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

    def get_empty_grid(self):
        get_empty_start = time.perf_counter()   
        print(f"Generating grid based on {Constants.SCREEN_WIDTH}x{Constants.SCREEN_HEIGHT}")
        matrix = []      
        for y in range(0, Constants.SCREEN_HEIGHT, Constants.UNIT_SIZE):
            x_line = []
            for x in range(0, Constants.SCREEN_WIDTH, Constants.UNIT_SIZE):
                x_line.append(1)
            matrix.append(x_line)

        print("get_empty_grid: Generating pathfinding grid...")
        grid =  Grid(matrix = matrix)
        print("get_empty_grid: Done...")
        get_empty_end = time.perf_counter()
        print(f"get_empty_grid timings: {round(60 - (get_empty_end - get_empty_start), 2)} second(s)")
        return grid

    def show_grid(self, grid, mouse_pos):        
        show_grid_start = time.perf_counter()     
        self.surface.blit(self.mouse_pointer, mouse_pos)           
        for node in grid.nodes:
            for item in node:
                newx = item.x * Constants.UNIT_SIZE
                newy = item.y * Constants.UNIT_SIZE
                rect_settings = PygameUtilities.RectSettings()
                rect_settings.x = newx
                rect_settings.y = newy
                if item.walkable:
                    rect_settings.BgColor = Constants.Colors.GREEN_DARK
                else:
                    rect_settings.BgColor = Constants.Colors.BURNT_ORANGE
                rect_settings.BorderColor = Constants.Colors.NEON_GREEN
                rect_settings.BorderSize = 1
                self.create_rect(self, rect_settings, True)
        show_grid_end = time.perf_counter()
        print(f"show_grid timings: {round(60 - (show_grid_end - show_grid_start), 2)} second(s)")
