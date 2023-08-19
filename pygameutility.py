import inspect
import random
from time import sleep
from uuid import uuid4
import pygame

# our stuff
from constants import Constants

class PygameUtilities:  
    font = None
    surface = None
    screen_border_rs = None
    font = None
    cursor_type = None
    cursor = None

    # mouse
    # mouse_pointer = None
    # mouse_pointer_mask = None

    # logging
    logutils = None

    # rect(surface, color, rect, width=0, border_radius=0, 
    # border_top_left_radius=-1, border_top_right_radius=-1, 
    # border_bottom_left_radius=-1, border_bottom_right_radius=-1)
    class tile_rect_settings:  
        x = None
        y = None  
        grid_x = None
        grid_y = None    
        width = None
        height = None
        hint_name = None
        rect = None
        text = None
        font = None
        font_name = Constants.FONT_NAME_DEFAULT
        font_size = Constants.FONT_SIZE_DEFAULT_PX
        background_color = Constants.Colors.GREEN
        font_color = Constants.Colors.BLACK
        border_color = None   
        border_sides = None  
        border_radius = 3
        border_width = Constants.BORDER_SIZE_PX
        def __init__(self, grid_x, grid_y, tile_width, tile_height, background_color):
            self.x = Constants.SIDE_PANEL_WIDTH_PX + (grid_x * tile_width)
            self.y = grid_y * tile_height
            self.grid_x = grid_x
            self.grid_y = grid_y
            self.background_color = background_color
            self.width = tile_width
            self.height = tile_height
            self.rect = pygame.Rect(self.x, self.y, tile_width, tile_height) 
            print(f"Created new tile of coordinates: XY: ({self.x}x{self.y}), GRID: ({self.grid_x}x{self.grid_y})")

    class game_button():
        pgu = None
        def __init__(self, pgu, rect, text_input, font, base_color, hovering_color):
            self.pgu = pgu
            self.image = None
            self.font = font
            self.base_color = base_color
            self.hovering_color = hovering_color
            self.text_input = text_input
            self.text = self.font.render(self.text_input, True, self.base_color)
            self.text_rect = rect

        def update(self, screen):
            screen.blit(self.text, self.text_rect)

        def check_position(self, position):
            if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top, self.text_rect.bottom):
                return True
            return False

        def change_color(self, position):
            if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top, self.text_rect.bottom):
                self.pgu.cursor_type = pygame.cursors.ball
                self.text = self.font.render(self.text_input, True, self.hovering_color)
            else:
                self.pgu.cursor_type = Constants.MOUSE_CURSOR
                self.text = self.font.render(self.text_input, True, self.base_color)

    def __init__(self, logutils):
        self.logutils = logutils
        self.logutils.log.debug("Initializing PygameUtilities() class")        
        
        pygame.init() # initialize the pygame module
        self.font = pygame.font.SysFont(Constants.FONT_NAME_DEFAULT, Constants.FONT_SIZE_DEFAULT_PX)
        self.surface = pygame.display.set_mode((Constants.SCREEN_WIDTH_PX, Constants.SCREEN_HEIGHT_PX))
        self.cursor_type = Constants.MOUSE_CURSOR

        # self.mouse_pointer = pygame.Surface((Constants.MOUSE_POINTER_SIZE_PX, Constants.MOUSE_POINTER_SIZE_PX))
        # self.mouse_pointer.fill(Constants.Colors.MOUSE_POINTER_COLOR)
        # self.mouse_pointer_mask = pygame.mask.from_surface(self.mouse_pointer)

        # hides mouse pointer provided by pygame
        #pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        self.cursor = pygame.mouse.set_cursor(self.cursor_type)

    def update_mouse(self, mouse_pos=None, mouse_pointer=None, tile=None):
        self.logutils.log.debug(f"Inside update_mouse")
        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()

        x = mouse_pos[0]
        y = mouse_pos[1]
        if x <= Constants.SIDE_PANEL_WIDTH_PX:
            x = 0
        else:
            x -= Constants.SIDE_PANEL_WIDTH_PX

        if tile is not None:   
            tile.display_details()         


        return mouse_pos
    
    def loop_fonts(self, pgu):
        fonts = pygame.font.get_fonts()
        print(fonts)
        y = 10
        pgu.surface.fill(Constants.Colors.ALICE_BLUE) 
        for i in range(0, len(fonts)):            
            newfont = fonts[i]            
            self.logutils.log.debug(f"Inside loop_fonts")
            rand_x = random.randint(0, 800)
            font = pygame.font.SysFont(newfont, 36)  
            text = font.render(f"Arguna ({newfont})", True, 'black')
            word_width, word_height = text.get_size()
            print(f"font: {newfont}")
            y += word_height + (Constants.WORD_SPACING_PX*2)
            rect = text.get_rect(x=rand_x, y=y)
            self.surface.blit(text, rect)
            y += 30
            if y >= Constants.SCREEN_HEIGHT_PX:
                pygame.display.flip()
                y = 10
                sleep(3)
                pgu.surface.fill(Constants.Colors.ALICE_BLUE) 

    def draw_center_text(self, text, text_color, y, font_name = None, font_size = None):
        self.logutils.log.debug(f"Inside draw_center_text")
        default_font_size = Constants.FONT_SIZE_DEFAULT_PX
        if font_size is None:
            font_size = default_font_size            

        if font_name is None:
            font = pygame.font.SysFont(Constants.FONT_NAME_DEFAULT, font_size)            
        else:
            font =pygame.font.SysFont(font_name, font_size)

        text = font.render(text, True, text_color)
        text_rect = text.get_rect(center=(Constants.SCREEN_WIDTH_PX / 2, y))
        self.surface.blit(text, text_rect)    

    def create_rect(self, rs, border_only=False):
        self.logutils.log.debug(f"Inside create_rect")
        x = rs.grid_x * rs.width
        y = rs.grid_y * rs.height
        if rs.rect is None:
           rs.rect = pygame.Rect(x, y, rs.width, rs.height) 

        # ensure these match always
        rs.width = rs.rect.width
        rs.height = rs.rect.height

        if not border_only:
            pygame.draw.rect(self.surface, rs.background_color, rs.rect)
        else:
            if rs.border_color is None:
                pygame.draw.rect(self.surface, rs.background_color, rs.rect, rs.border_width, border_radius=rs.border_radius)
            else:
                pygame.draw.rect(self.surface, rs.border_color, rs.rect, rs.border_width, border_radius=rs.border_radius)

        # add text
        if rs.text is not None:  
            if rs.font_color is None:
                rs.font_color = Constants.Colors.NEON_GREEN

            if rs.font_name is not None:
                if rs.font_size is None:
                    rs.font_size == Constants.DEFAULT_FONT_SIZE                    
                rs.font = pygame.font.SysFont(rs.font_name, rs.font_size)
            elif rs.font is None:
                rs.font =  self.font

            if "\n" in rs.text:
                self.place_text(rs.text, rs.rect.width, rs.x, rs.y, font=rs.font, color=rs.font_color)
            else:
                unit_text = rs.font.render(rs.text, True, rs.font_color)
                rect = unit_text.get_rect(x=rs.x, y=rs.y)
                self.surface.blit(unit_text, rect)
        return rs

    # used for "gamebutton" class
    def create_rect_with_center_text(self, text, font, y, total_width):
        self.logutils.log.debug(f"Inside create_rect_with_center_text")
        font_render = font.render(text, True, 'black')
        rect = font_render.get_rect(center=(total_width / 2, y))
        return rect

    def place_text(self, text, width, initial_x, initial_y, font, color=pygame.Color('black')):
        self.logutils.log.debug(f"Inside place_text")
        words = text.split(' ')
        space = font.size(' ')[0]
        initial_x += Constants.WORD_SPACING_PX
        initial_y += Constants.WORD_SPACING_PX
        x = initial_x
        y = initial_y
        for word in words:
            newlines = word.split("\n")
            for i in range(0, len(newlines)):
                word_surface = font.render(newlines[i], 0, color)
                word_width, word_height = word_surface.get_size()
                word_height += Constants.WORD_SPACING_PX
                self.logutils.log.debug(newlines[i])

                if i > 0: # a new line
                    x = initial_x
                    y += word_height
                else:
                    if x + word_width >= (x + width - Constants.WORD_SPACING_PX):
                        x = initial_x
                        y += word_height
                self.surface.blit(word_surface, (x, y))
                x += word_width + space
