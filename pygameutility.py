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

    # mouse
    # mouse_pointer = None
    # mouse_pointer_mask = None

    # logging
    logutils = None

    # rect(surface, color, rect, width=0, border_radius=0, 
    # border_top_left_radius=-1, border_top_right_radius=-1, 
    # border_bottom_left_radius=-1, border_bottom_right_radius=-1)
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
        FontName = Constants.FONT_NAME_DEFAULT
        FontSize = Constants.FONT_SIZE_DEFAULT_PX
        BgColor = Constants.Colors.GREEN
        FontColor = Constants.Colors.BLACK
        BorderColor = None   
        BorderSides = None  
        BorderRadius = 1
        BorderWidth = Constants.BORDER_SIZE_PX
        id = None   
        def __init__(self, tile=None):
            self.id = uuid4()

            if tile is not None:
                self.x = tile.x
                self.y = tile.y
                self.Width = tile.Width
                self.Height = tile.Height
                self.BgColor = tile.Type.value["BgColor"]

    def __init__(self, logutils):
        self.logutils = logutils
        self.logutils.log.debug("Initializing PygameUtilities() class")        
        
        pygame.init() # initialize the pygame module
        self.font = pygame.font.SysFont(Constants.FONT_NAME_DEFAULT, Constants.FONT_SIZE_DEFAULT_PX)
        self.surface = pygame.display.set_mode((Constants.SCREEN_WIDTH_PX, Constants.SCREEN_HEIGHT_PX))

        self.mouse_pointer = pygame.Surface((Constants.MOUSE_POINTER_SIZE_PX, Constants.MOUSE_POINTER_SIZE_PX))
        self.mouse_pointer.fill(Constants.Colors.MOUSE_POINTER_COLOR)
        self.mouse_pointer_mask = pygame.mask.from_surface(self.mouse_pointer)

        # hides mouse pointer provided by pygame
        #pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        pygame.mouse.set_cursor(Constants.MOUSE_CURSOR)

    def update_mouse(self, mouse_pos=None, mouse_pointer=None, tile=None):
        self.logutils.log.debug(f"Inside update_mouse: {inspect.currentframe().f_code.co_name}")
        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()

        if mouse_pointer is None:
            mouse_pointer = self.mouse_pointer

        x = mouse_pos[0]
        y = mouse_pos[1]
        if x <= Constants.SIDE_PANEL_WIDTH_PX:
            x = 0
        else:
            x -= Constants.SIDE_PANEL_WIDTH_PX

        if tile is not None:            
            rs = self.RectSettings()
            rs.x = x + Constants.WORD_SPACING_PX
            rs.y = y + Constants.WORD_SPACING_PX
            rs.FontSize = 12
            rs.Text = tile.TileDetails
            rs.Width = Constants.GRID_DETAILS_WIDTH_PX
            rs.Height = Constants.GRID_DETAILS_HEIGHT_PX
            rs.BgColor = Constants.Colors.GRID_DETAILS_COLOR
            rs.BorderRadius = 5
            rs = self.create_rect(rs, really_draw = True)
            pygame.display.update(rs.Rect)
            
        self.surface.blit(mouse_pointer, mouse_pos)

        return mouse_pos
    
    def loop_fonts(self, pgu):
        fonts = pygame.font.get_fonts()
        print(fonts)
        y = 10
        pgu.surface.fill(Constants.Colors.ALICE_BLUE) 
        for i in range(0, len(fonts)):            
            newfont = fonts[i]            
            self.logutils.log.debug(f"Inside loop_fonts: {inspect.currentframe().f_code.co_name}")
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
        self.logutils.log.debug(f"Inside draw_center_text: {inspect.currentframe().f_code.co_name}")
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

    def create_rect(self, rs, really_draw=True):
        self.logutils.log.debug(f"Inside create_rect: {inspect.currentframe().f_code.co_name}")
        if rs.Rect is None:
           rs.Rect = pygame.Rect(rs.x, rs.y, rs.Width, rs.Height) 

        # ensure these match always
        rs.x = rs.Rect.x
        rs.y = rs.Rect.y
        rs.Width = rs.Rect.width
        rs.Height = rs.Rect.height

        if really_draw:
            if rs.BorderColor is None:
                pygame.draw.rect(self.surface, rs.BgColor, rs.Rect, border_radius=rs.BorderRadius)
            else:
                pygame.draw.rect(self.surface, rs.BgColor, rs.Rect, rs.BorderWidth, border_radius=rs.BorderRadius)

        # add text
        if rs.Text is not None:  
            if rs.FontColor is None:
                rs.FontColor = Constants.Colors.NEON_GREEN

            if rs.FontName is not None:
                if rs.FontSize is None:
                    rs.FontSize == Constants.DEFAULT_FONT_SIZE                    
                rs.Font = pygame.font.SysFont(rs.FontName, rs.FontSize)
            elif rs.Font is None:
                rs.Font =  self.font

            if "\n" in rs.Text:
                self.place_text(rs.Text, rs.Rect.width, rs.x, rs.y, font=rs.Font, color=rs.FontColor)
            else:
                unit_text = rs.Font.render(rs.Text, True, rs.FontColor)
                rect = unit_text.get_rect(x=rs.x, y=rs.y)
                self.surface.blit(unit_text, rect)
        return rs

    # used for "gamebutton" class
    def create_rect_with_center_text(self, text, font, y, total_width):
        self.logutils.log.debug(f"Inside create_rect_with_center_text: {inspect.currentframe().f_code.co_name}")
        font_render = font.render(text, True, 'black')
        rect = font_render.get_rect(center=(total_width / 2, y))
        return rect

    def place_text(self, text, width, initial_x, initial_y, font, color=pygame.Color('black')):
        self.logutils.log.debug(f"Inside place_text: {inspect.currentframe().f_code.co_name}")
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
