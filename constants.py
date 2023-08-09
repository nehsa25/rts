

# constants
from enum import Enum
import random

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
    GAME_NAME = "Unhinged"
    PANEL_BUTTON_SPACING = 50    
    BORDER_SIZE = 5
    DEFAULT_FONT_NAME = "century"
    LOADING_MSG = "Loading".upper()

    # Environment
    NUM_WATER_TILES = 25
    NUM_FIRE_TILES = 5
    NUM_MOUNTAIN_TILES = 70
    NUM_SWAMP_TILES = 10

    # main game side panel
    SP_WIDTH = 100   
    SP_BUTTON_TEXT_SIZE = 12 
    SP_BORDER_SIZE = BORDER_SIZE

    # main game bottom panel
    BP_HEIGHT = 100
    BP_BUTTON_TEXT_SIZE = 12 
    BP_BORDER_SIZE = BORDER_SIZE

    # main game window    
    RECT_SIZE = 25
    RECT_BORDER_SIZE = 2
    MOUSE_POINTER_SIZE = 5    
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768   
    FONT_SIZE = 20
    MENU_SPACING = 60
    UNIT_SPAWN_X = SP_WIDTH + RECT_BORDER_SIZE + PANEL_BUTTON_SPACING
    UNIT_SPAWN_Y = 25
    GAME_MAIN_BORDER_SIZE = 5

    # title screen
    TITLE_SCREEN_FONT_SIZE = 60
    TITLE_FONT = "showcardgothic" #rage is cool

    # UNIT
    UNIT_SIZE = 15
    UNIT_BORDER_SIZE = 5
    UNIT_SPAWN_X = SP_WIDTH + 100
    UNIT_SPAWN_Y = 100

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
        FIRE = (255,90,0)   

        # blues
        BLUE = (0, 0, 255)
        NAVY = (75,104,184) 
        ALICE_BLUE = (240,248,255)  
        AQUA = (0,255,255)      

        # browns
        COCOA = (53,40,30)
        POOP_BROWN = (123, 92, 0)    

        # greens
        GREEN = (0, 255, 0)
        HUNTER_GREEN = (53, 94, 59)
        NEON_GREEN = (57,255,20)
        GREEN_DARK = (1, 50, 32)

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
        GAME_BORDER = BLACK
        GAME_TEXT_COLOR = ROYAL_GOLD
        MOUSE_POINTER_COLOR = WHITE
        GAME_MAIN_BORDER_COLOR = GAME_BORDER        
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
