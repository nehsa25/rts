

# constants
from enum import Enum
import random

import pygame

# fonts = ['arial', 'arialblack', 'bahnschrift', 'calibri', 'cambria', 'cambriamath', 'candara', 'comicsansms', 
# 'consolas', 'constantia', 'corbel', 'couriernew', 'ebrima', 'franklingothicmedium', 'gabriola', 'gadugi', 'georgia', 
# 'impact', 'inkfree', 'javanesetext', 'leelawadeeui', 'leelawadeeuisemilight', 'lucidaconsole', 'lucidasans', 'malgungothic', 
# 'malgungothicsemilight', 'microsofthimalaya', 'microsoftjhenghei', 'microsoftjhengheiui', 'microsoftnewtailue', 'microsoftphagspa', 
# 'microsoftsansserif', 'microsofttaile', 'microsoftyahei', 'microsoftyaheiui', 'microsoftyibaiti', 'mingliuextb', 
# 'pmingliuextb', 'mingliuhkscsextb', 'mongolianbaiti', 'msgothic', 'msuigothic', 'mspgothic', 'mvboli', 'myanmartext', 
# 'nirmalaui', 'nirmalauisemilight', 'palatinolinotype', 'segoefluenticons', 'segoemdl2assets', 'segoeprint', 'segoescript', 
# 'segoeui', 'segoeuiblack', 'segoeuiemoji', 'segoeuihistoric', 'segoeuisemibold', 'segoeuisemilight', 'segoeuisymbol', 
# 'segoeuivariable', 'simsun', 'nsimsun', 'simsunextb', 'sitkatext', 'sylfaen', 'symbol', 'tahoma', 'timesnewroman', 'trebuchetms', 
# 'verdana', 'webdings', 'wingdings', 'yugothic', 'yugothicuisemibold', 'yugothicui', 'yugothicmedium', 'yugothicuiregular', 'yugothicregular', 
# 'yugothicuisemilight', 'holomdl2assets', 'agencyfb', 'algerian', 'bookantiqua', 'arialrounded', 'baskervilleoldface', 'bauhaus93', 'bell', 
# 'bernardcondensed', 'bodoni', 'bodoniblack', 'bodonicondensed', 'bodonipostercompressed', 'bookmanoldstyle', 'bradleyhanditc', 'britannic', 
# 'berlinsansfb', 'berlinsansfbdemi', 'broadway', 'brushscript', 'bookshelfsymbol7', 'californianfb', 'calisto', 'castellar', 'centuryschoolbook', 
# 'centaur', 'century', 'chiller', 'colonna', 'cooperblack', 'copperplategothic', 'curlz', 'dubai', 'dubaimedium', 'dubairegular', 'elephant', 
# 'engravers', 'erasitc', 'erasdemiitc', 'erasmediumitc', 'felixtitling', 'forte', 'franklingothicbook', 'franklingothicdemi', 'franklingothicdemicond', 
# 'franklingothicheavy', 'franklingothicmediumcond', 'freestylescript', 'frenchscript', 'footlight', 'garamond', 'gigi', 'gillsans', 'gillsanscondensed', 
# 'gillsansultracondensed', 'gillsansultra', 'gloucesterextracondensed', 'gillsansextcondensed', 'centurygothic', 'goudyoldstyle', 'goudystout', 
# 'harlowsolid', 'harrington', 'haettenschweiler', 'hightowertext', 'imprintshadow', 'informalroman', 'blackadderitc', 'edwardianscriptitc', 'kristenitc', 
# 'jokerman', 'juiceitc', 'kunstlerscript', 'widelatin', 'lucidabright', 'lucidacalligraphy', 'lucidafaxregular', 'lucidafax', 'lucidahandwriting', 
# 'lucidasansregular', 'lucidasansroman', 'lucidasanstypewriterregular', 'lucidasanstypewriter', 'lucidasanstypewriteroblique', 'magneto', 'maiandragd', 
# 'maturascriptcapitals', 'mistral', 'modernno20', 'monotypecorsiva', 'niagaraengraved', 'niagarasolid', 'ocraextended', 'oldenglishtext', 'onyx', 'msoutlook', 
# 'palacescript', 'papyrus', 'parchment', 'perpetua', 'perpetuatitling', 'playbill', 'poorrichard', 'pristina', 'rage', 'ravie', 'msreferencesansserif', 
# 'msreferencespecialty', 'rockwellcondensed', 'rockwell', 'rockwellextra', 'script', 'showcardgothic', 'snapitc', 'stencil', 'twcen', 'twcencondensed', 
# 'twcencondensedextra', 'tempussansitc', 'vinerhanditc', 'vivaldi', 'vladimirscript', 'wingdings2', 'wingdings3', 'extra', 'nina', 'segoecondensed']

class Constants:
    GAME_NAME = "Unhinged RTS"
    SCREEN_WIDTH_PX = 1366
    SCREEN_HEIGHT_PX = 768    
    GAME_MAIN_BORDER_SIZE_PX = 5
    BORDER_SIZE_PX = 5
    LOADING_MSG = "Loading".upper()

    # game grid nodes
    GAME_GRID_NODES = 500

    # UNIT
    UNIT_SIZE_GD = 1
    WIDTH_STEP = UNIT_SIZE_GD # not used
    HEIGHT_STEP = UNIT_SIZE_GD # not used

    # grid details when middle mouse is pressed
    GRID_DETAILS_WIDTH_PX = 300
    GRID_DETAILS_HEIGHT_PX = 400

    # Environment - testing
    # NUM_WATER_TILES = 2
    # NUM_FIRE_TILES = 2 # walkable
    # NUM_MOUNTAIN_TILES = 2
    # NUM_SWAMP_TILES = 2
    # NUM_FOREST_TILES = 2
    # NUM_FOG_TILES = 2 # walkable
    # NUM_RAIN_TILES = 2 # walkable
    # NUM_LAVA_TILES = 2

    # Environment - realisic
    NUM_WATER_TILES = 128
    NUM_FIRE_TILES = 29 # walkable
    NUM_MOUNTAIN_TILES = 58
    NUM_SWAMP_TILES = 26
    NUM_FOREST_TILES = 42
    NUM_FOG_TILES = 69 # walkable
    NUM_RAIN_TILES = 75 # walkable
    NUM_LAVA_TILES = 29

    # main game side panel
    SIDE_PANEL_WIDTH_PX = 100   
    SP_BUTTON_TEXT_SIZE_PX = 12 
    SP_BORDER_SIZE = BORDER_SIZE_PX

    # main game bottom panel
    BP_HEIGHT_PX = 100
    BP_BUTTON_TEXT_SIZE_PX = 12 
    BP_BORDER_SIZE = BORDER_SIZE_PX

    # spacers
    PANEL_BUTTON_SPACING_PX = 50  
    WORD_SPACING_PX = 5  
    MENU_SPACING_PX = 60

    # mouse
    MOUSE_POINTER_SIZE_PX = 1
    MOUSE_CURSOR = pygame.cursors.diamond   

    # SPAWN
    SPAWN_GRID_X = 1
    SPAWN_GRID_Y = 1
    SPAWN_SIZE = 10

    # fonts
    FONT_NAME_DEFAULT = "century"
    TITLE_FONT = "showcardgothic"
    TROOP_FONT = "rage"

    # font sizes    
    FONT_SIZE_DEFAULT_PX = 24
    FONT_SIZE_MENU_PX = 48
    FONT_SIZE_TITLE_PX = 60
    
    # map select
    MAP_MENU_LEFT_WIDTH_PX = 200

    # our colors
    class Colors:
        # rgb
        BLACK = (0, 0, 0)

        #whites
        WHITE = (255, 255, 255) 
        WHITE_MISTY = (232, 241, 241)

        SALMON = (250, 128, 114)    
        FUCHSIA = (255, 0, 255)

        # reds
        RED = (255, 0, 0)
        SCARLET = (255, 36, 0)
        CRIMSON = (139, 0, 0)    
        FIRE_TERRAIN = (255,90,0)   
        LAVA = (207, 16, 32)

        # blues
        BLUE = (0, 0, 255)
        NAVY = (75,104,184) 
        ALICE_BLUE = (240,248,255)  
        AQUA = (0,255,255)      
        DODGER = (30,144,255)
        WATER = (212, 241, 249)
        RAIN = (56, 60, 63)

        # browns
        COCOA = (53,40,30)
        POOP_BROWN = (123, 92, 0)    
        SIENNA = (160,82,45)
        MOCCASIN = (255,228,181)
        SANDY_BROWN = (244, 164, 96)

        # greens
        GREEN = (0, 255, 0)
        HUNTER_GREEN = (53, 94, 59)
        NEON_GREEN = (57,255,20)
        GREEN_DARK = (1, 50, 32)
        OLIVE = (128,128,0)
        PEA_GREEN = (96, 160, 76)
        PUTRID_GREEN = (137,165,114)

        # purples
        PLUM = (221,160,221)
        ROYAL_PURPLE = (75,0,110)
        MAROON = (128, 0, 0) 
        DARK_PURPLE = (48,25,52)
    
        # yellows
        ROYAL_GOLD = (255, 188, 0)
        YELLOW = (255, 244, 79)

        # oranges
        BURNT_ORANGE = (204, 85, 0)

        # grays
        GRAY_IRON_MOUNTAIN = (87, 85, 83)
        GRAY_DARK = (64, 64, 64)

        # main colors
        GAME_MAIN_COLOR = DARK_PURPLE
        GAME_MAP_COLOR = HUNTER_GREEN
        GAME_BORDER_COLOR = BLACK
        GAME_TEXT_COLOR = ROYAL_GOLD
        MOUSE_POINTER_COLOR = ROYAL_GOLD
        GAME_MAIN_BORDER_COLOR = GAME_BORDER_COLOR    
        SPAWN_COLOR = BURNT_ORANGE    
        GRID_DETAILS_COLOR = SIENNA

        # terrain colors
        TERRAIN_BASIC = SANDY_BROWN
        TERRAIN_LAVA = LAVA
        TERRAIN_FIRE = CRIMSON
        TERRAIN_MOUNTAIN = WHITE_MISTY
        TERRAIN_RAIN = RAIN
        TERRAIN_WATER = AQUA
        TERRAIN_FOG = GRAY_IRON_MOUNTAIN
        TERRAIN_SWAMP = PUTRID_GREEN
        TERRAIN_FOREST = HUNTER_GREEN



        RANDOM = 1

    # indicates what borders to created, used by create_rect function
    class BorderSides(Enum):
        ALL = 0
        LEFT = 1
        TOP = 2
        RIGHT = 3
        BOTTOM = 4

        @classmethod
        def get_random_side(cls):
            side = 'all'
            while side == 'all':
                side = random.choice(cls._member_names_).lower()
            return side.lower()

    # used to determine how big of water pools to make
    class DensityTypes(Enum):
        Tiny = 0
        Small = 1
        Medium = 2
        Large = 3
        Huge = 4

        @classmethod
        def get_random_size(cls):
            size = random.choice(cls._member_names_).lower()
            return size.lower()
