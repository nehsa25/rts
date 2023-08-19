import concurrent.futures
import time
import pygame
import random

# our stuff
from utility import Utility
from gamedata import GameData
from elf import Elf
from goblin import Goblin
from human import Human
from fae import Fae
from dwarf import Dwarf
from arguna import Arguna
from nyrriss import Nyrriss
from constants import Constants
from pygameutility import PygameUtilities
from tile import Tiles
from logutiliites import LogUtilities
from unit import Unit
from events import Events
from gamedata import GameData
from menu import Menu
from race import Race

class unhingedrts:
    # main window title
    main_caption = f"{Constants.GAME_NAME} - GLHF!"
    logo = None
    running = True
    game_data = None
    events = None
    menu = None
    race = None
    hero_unit_created = False
    loading_msg = ""
    selected_units = [] # units on the screen that have been clicked on
    selected_map = None
    
    def __init__(self):
        self.log_utils = LogUtilities()
        self.pgu = PygameUtilities(self.log_utils)
        self.ut = Utility(self.log_utils, self.pgu)
        self.game_data = GameData(self.log_utils)  
        self.tiles = Tiles(self.log_utils)
        self.events = Events(self.log_utils, self.pgu)
        self.menu = Menu(self.log_utils, self.pgu) 
        self.race = Race(self.log_utils)

        #logo
        self.logo = pygame.image.load("logo.png")
        pygame.display.set_icon(self.logo)
        pygame.display.set_caption(Constants.GAME_NAME) 
        
    # title screen
    def title_loop(self):
        self.log_utils.log.debug(f"Inside title_loop")
        first_open_running = True         
        pygame.display.set_caption("Welcome!")

        while first_open_running:
            self.pgu.surface.fill(Constants.Colors.GAME_MAIN_COLOR) # blank out screen to allow refresh
            self.menu.create_border()
            mouse_pos = self.pgu.update_mouse()

            # title screen text
            self.pgu.draw_center_text(
                Constants.GAME_NAME, 
                Constants.Colors.GAME_TEXT_COLOR, 
                Constants.SCREEN_HEIGHT_PX / 2 - Constants.FONT_SIZE_DEFAULT_PX, 
                font_name = Constants.TITLE_FONT, 
                font_size = Constants.FONT_SIZE_TITLE_PX
            )        

            self.pgu.draw_center_text(
                "press SPACE or CLICK to begin!", 
                Constants.Colors.GAME_TEXT_COLOR,
                Constants.SCREEN_HEIGHT_PX - Constants.FONT_SIZE_DEFAULT_PX - 50,
                font_size=16
            )

            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    first_open_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        first_open_running = False
                        break
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    first_open_running = False
                    self.running = False
                    break
            pygame.display.flip()
        return False
    
    # race select screen
    def race_select_loop(self):
        self.log_utils.log.debug(f"Inside race_select_loop")
        race_select_running = True 
        pygame.display.set_caption("Select your Race")
        font_size = 60
        base_height = Constants.SCREEN_HEIGHT_PX / 2 - font_size # true center height # .5 of 1024 = 512
        select_your_race_text_y = base_height / 2 # .5 of 512 = 256

        while race_select_running:
            self.pgu.surface.fill(Constants.Colors.GAME_MAIN_COLOR) # blank out screen to allow refresh
            self.menu.create_border()
            mouse_pos = self.pgu.update_mouse()
            self.pgu.draw_center_text("Select your Race", Constants.Colors.GAME_TEXT_COLOR, select_your_race_text_y, Constants.FONT_NAME_DEFAULT, font_size)
            y_spacer = 100
            x_spacer = 200

            # buttons!
            race_buttons = []

            # random
            race_name = "(Random)"
            def_font = pygame.font.SysFont(Constants.FONT_NAME_DEFAULT, Constants.FONT_SIZE_DEFAULT_PX) # only using Goblin font size here
            font_render = def_font.render("Random", True, 'black')
            rand_x = (Constants.SCREEN_WIDTH_PX / 2 + x_spacer)
            rand_y = (Constants.SCREEN_HEIGHT_PX / 2)
            rect = font_render.get_rect(x=rand_x,y=rand_y)
            random_button = self.pgu.game_button(self.pgu,rect, 
                                                 race_name,
                                                 font=def_font,
                                                 base_color="White",
                                                 hovering_color=Constants.Colors.DODGER)   
   
            random_button.change_color(mouse_pos)
            random_button.update(self.pgu.surface)
            race_buttons.append(dict(name="random", button=random_button))

            # our races
            for i in range(0, len(self.race.races)):
                current_race = self.race.races[i]
                race = self.race.get_race_by_name(current_race)
                race_font = pygame.font.SysFont(race.font, race.font_size)
                race_button_rect = self.pgu.create_rect_with_center_text(race.name, 
                                                                        race_font,
                                                                        select_your_race_text_y + y_spacer + (Constants.MENU_SPACING_PX * i+1), 
                                                                        Constants.SCREEN_WIDTH_PX)            
                race_button = self.pgu.game_button(self.pgu, 
                                                   race_button_rect, 
                                                   race.name,
                                                   font=race_font,
                                                   base_color="White", 
                                                   hovering_color=race.hover_text_color)      
                race_button.change_color(mouse_pos)
                race_button.update(self.pgu.surface)
                race_buttons.append(dict(name=race, button=race_button))

            # event loop for option selection screen
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for race_button in race_buttons:
                        if race_button["button"].check_position(mouse_pos):
                            selected_race = race_button["name"]

                            # support random case
                            if selected_race == "random":
                                race_string = random.choice(self.race.races)
                                selected_race = self.race.get_race_by_name(race_string)
                            else:
                                selected_race = race_button["button"]
                            self.game_data.Player.selected_race = selected_race
                            race_select_running = False
                if event.type == pygame.QUIT:
                    race_select_running = False
                    self.running = False
            pygame.display.flip()

    # options
    def options_loop(self):
        self.log_utils.log.debug(f"Inside options_loop")
        options_loop_running = True 
        pygame.display.set_caption(f"Options")

        while options_loop_running:
            self.pgu.surface.fill(Constants.Colors.GAME_MAIN_COLOR) # blank out screen to allow refresh
            self.menu.create_border()
            mouse_pos = self.pgu.update_mouse()

            pause_y = Constants.SCREEN_HEIGHT_PX / 2 - Constants.FONT_SIZE_DEFAULT_PX
            font = pygame.font.SysFont(Constants.FONT_NAME_DEFAULT, Constants.DEFAULT_FONT_SIZE)

            show_grid_rect = self.pgu.create_rect_with_center_text("Show Grid", font, pause_y, Constants.SCREEN_WIDTH_PX)
            show_grid = self.pgu.game_button(self.pgu,
                                             show_grid_rect, 
                                             text_input="Choose Race", 
                                             font=font, 
                                             base_color="White", 
                                             hovering_color=Constants.Colors.ROYAL_PURPLE)
            show_grid.change_color(mouse_pos)
            show_grid.update(self.pgu.surface)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.log_utils.log.debug(f"mouse down: {event}")
                    if show_grid.check_position(mouse_pos):
                        options_loop_running = False
                        self.hero_unit_created = False
                        self.race_select_loop()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.log_utils.log.debug(f"mouse up: {event}")
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        options_loop_running = False # unpause
                        pygame.display.set_caption(self.main_caption)
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    options_loop_running = False
                    self.running = False
            
            pygame.display.flip()

    # pause screen (when you press esc)
    def pause_game_menu_loop(self):
        self.log_utils.log.debug(f"Inside pause_game_menu_loop")
        pause_game_menu_loop_running = True 
        pygame.display.set_caption(f"Paused!")

        while pause_game_menu_loop_running:
            self.pgu.surface.fill(Constants.Colors.GAME_MAIN_COLOR) # blank out screen to allow refresh
            self.menu.create_border()
            mouse_pos = self.pgu.update_mouse()

            pause_y = Constants.SCREEN_HEIGHT_PX / 2 - Constants.FONT_SIZE_DEFAULT_PX
            font = pygame.font.SysFont(Constants.FONT_NAME_DEFAULT, 48)

            race_button_rect = self.pgu.create_rect_with_center_text("Choose Race", font, pause_y, Constants.SCREEN_WIDTH_PX)
            race_button = self.pgu.game_button(self.pgu,
                                               race_button_rect, 
                                               text_input="Choose Race", 
                                               font=font, base_color="White", 
                                               hovering_color=Constants.Colors.ROYAL_PURPLE)
            race_button.change_color(mouse_pos)
            race_button.update(self.pgu.surface)

            options_rect = self.pgu.create_rect_with_center_text("Options", font, pause_y + (Constants.MENU_SPACING_PX * 1), Constants.SCREEN_WIDTH_PX)
            options_button = self.pgu.game_button(self.pgu, 
                                                  options_rect, 
                                                  text_input="Options", 
                                                  font=font, 
                                                  base_color="White", 
                                                  hovering_color=Constants.Colors.ROYAL_PURPLE)
            options_button.change_color(mouse_pos)
            options_button.update(self.pgu.surface)

            quit_button_rect = self.pgu.create_rect_with_center_text("Quit", font, pause_y + (Constants.MENU_SPACING_PX * 2), Constants.SCREEN_WIDTH_PX)
            quit_button = self.pgu.game_button(self.pgu,
                                               quit_button_rect, 
                                               text_input="Quit", 
                                               font=font, 
                                               base_color="White", 
                                               hovering_color=Constants.Colors.ROYAL_PURPLE)
            quit_button.change_color(mouse_pos)
            quit_button.update(self.pgu.surface)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.log_utils.log.debug(f"mouse down: {event}")
                    if race_button.check_position(mouse_pos):
                        pause_game_menu_loop_running = False
                        self.hero_unit_created = False
                        self.race_select_loop()
                    if options_button.check_position(mouse_pos):
                        # pause_game_menu_loop_running = False
                        self.options_loop()
                    if quit_button.check_position(mouse_pos):
                        pause_game_menu_loop_running = False
                        self.running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    self.log_utils.log.debug(f"mouse up: {event}")
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause_game_menu_loop_running = False # unpause
                        pygame.display.set_caption(self.main_caption)
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    pause_game_menu_loop_running = False
                    self.running = False
            
            pygame.display.flip()

    # loading screen
    def loading_screen_loop(self):
        self.log_utils.log.debug(f"Inside loading_screen_loop")
        loading_screen_loop_running = True 
        pygame.display.set_caption(f"Loading!")

        clock = pygame.time.Clock()
        self.log_utils.log.debug(f"Started clock: {clock}")

        loading_threads = []
        executor = concurrent.futures.ThreadPoolExecutor()
        executor._max_workers = 1
        state = ""
        loading = False
        show_complete = False
        while loading_screen_loop_running:            
            clock.tick(60)
            self.pgu.surface.fill(Constants.Colors.GAME_MAIN_COLOR) # blank out screen to allow refresh
            self.menu.create_border()
            mouse_pos = self.pgu.update_mouse()
            
            # main font
            font_size = 72
            loading_rect_y = Constants.SCREEN_HEIGHT_PX / 2 - font_size
            text = Constants.LOADING_MSG
            rect = self.pgu.draw_center_text(text, Constants.Colors.ROYAL_GOLD, loading_rect_y, font_name = Constants.FONT_NAME_DEFAULT, font_size = font_size)

            font_size = 36
            loading_rect_y = (Constants.SCREEN_HEIGHT_PX / 4 - font_size) * 3
            text = ""
            if self.loading_msg !=  "":
                text = self.loading_msg               
            self.pgu.draw_center_text(text, Constants.Colors.CRIMSON, loading_rect_y, font_name = Constants.FONT_NAME_DEFAULT, font_size = font_size)

            # update entire display
            pygame.display.flip()

            # the work..
            if not loading:
                load_env = True # load obstacles or not
                loading_threads.append(executor.submit(self.tiles.load_grid, self.pgu, self.ut, self.game_data, load_env))
                loading = True # whether thread started

            # check if done..
            for future in loading_threads:
                state = future._state     
                if state == "PENDING":
                    state = "INITIALIZING"
                elif state == "RUNNING":
                    state = "LOADING"
                elif state == "FINISHED":                        
                    state = "COMPLETE"
                    self.loading_msg = "Get ready!".upper()  
                    result = future.result()        
                    self.log_utils.log.debug(f"Loading complete: {result}")             
                    loading_screen_loop_running = False

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.log_utils.log.debug(f"mouse down: {event}")
            if event.type == pygame.MOUSEBUTTONUP:
                self.log_utils.log.debug(f"mouse up: {event}")
            if event.type == pygame.KEYDOWN:
                self.log_utils.log.debug(f"key down: {event}")
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                loading_screen_loop_running = False
                self.running = False

    # map loading screen
    def map_select_loop(self):
        self.log_utils.log.debug(f"Inside map_select_loop")
        map_select_loop_running = True 
        pygame.display.set_caption(f"Map Selection")

        while map_select_loop_running:
            self.pgu.surface.fill(Constants.Colors.GAME_MAIN_COLOR) # blank out screen to allow refresh
            self.menu.create_border()
            mouse_pos = self.pgu.update_mouse()            
            pygame.display.flip()

    # the game..
    def main_game_loop(self):   
        self.log_utils.log.debug(f"Inside main_game_loop")     
        game_init_start = time.perf_counter()
        main_game_running = True 

        clock = pygame.time.Clock()
        self.log_utils.log.debug(f"main_game_loop: Started clock: {clock}")

        self.loading_screen_loop()

        pygame.display.set_caption(self.main_caption)

        # similate army
        # for i in range(0, 3):
        #     troop = random.choice(self.GameData.Player.selected_race.units)
        #     self.ut.create_unit(self.pgu, self.player, troop["Type"])
        #     pass

        game_init_end = time.perf_counter()
        self.log_utils.log.debug(f"Game initialization ended in {round(game_init_end - game_init_start, 2)} second(s)")

        while main_game_running:
            game_start = time.perf_counter()

            # slow things down
            clock.tick(60)

            self.pgu.surface.fill(Constants.Colors.GAME_MAP_COLOR) # blank out screen to allow refresh
            #self.menu.create_border()
            mouse_pos = self.pgu.update_mouse()

            # create terrain environment
            self.tiles.DrawTerrainTiles(self.pgu)

            # # check for fire damage
            # for army_unit in self.player.army:
            #     if obstacles.colliderect(army_unit.RectSettings.Rect):
            #         self.logutils.log.debug("YOU BURNT! - this should be move to somewhere else and slowed down to something like once hurt per .5 second")

            # add mouse pointer
            self.pgu.update_mouse(mouse_pos, self.pgu.cursor)
            
            self.events.check_for_events(self.tiles)

            # scan for selected units on each redraw
            for selected_unit in self.selected_units:
                self.ut.select_unit(self.pgu, selected_unit)
                # if we have a unit selected, show it in the bottom window
                if len(self.selected_units) > 0:
                    self.ut.create_bottom_panel(self.pgu, self.player)
            
            #  refresh side panel / highlight a unit that's hovered over
            self.menu.draw_side_panel(self.pgu, player=self.game_data.Player)

            # refresh spawn point
            self.ut.draw_spawn_points(self.tiles.tile_width, self.tiles.tile_height)

            # create initial unit
            if self.hero_unit_created:
                # draw units on field
                for army_unit in self.game_data.Player.army:
                    army_unit.DrawUnit(self.game_data.Player)
            else:
                hero_unit = Unit(self.log_utils, self.pgu, unit_type=self.game_data.Player.selected_race.hero_character, tiles=self.tiles)

                hero_unit.AttackTile(3,5)
                self.game_data.Player.army = hero_unit.AddToArmy(self.game_data.Player)
                self.hero_unit_created = True

            # draw border last to cover anything up
            self.menu.create_border()

            # event handling, gets all event from the event queue.  These events are only fired once so good for menus or single movement but not for continuous
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.events.mouse_left_single_event(event, self.game_data.Player, self.ut, self.tiles, self.game_data)
                    if event.button == 2:
                        self.events.mouse_middle_single_event(event)
                    if event.button == 3:
                        self.events.mouse_right_single_event(event)
                if event.type == pygame.MOUSEBUTTONUP:
                    self.log_utils.log.debug(f"mouse up: {event}")
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_game_menu_loop()
                        if self.running == False:
                            main_game_running = False
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    main_game_running = False
                    self.running = False

            game_end = time.perf_counter()
            # print(f"FPS: {round(60 - (game_end - game_start), 2)} second(s)")
            pygame.display.flip()

    def main(self):    
        self.log_utils.log.debug(f"Inside main")      
        first_opened = True
        while self.running:
            if first_opened:
                first_opened = self.title_loop()
            elif self.game_data.Player.selected_race is None:
                self.race_select_loop()
            # elif self.selected_map is None:
            #     self.map_select_loop()   
            else:
                self.main_game_loop()            
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    main_start = time.perf_counter()
    unhinged = unhingedrts()
    unhinged.main()
    main_end = time.perf_counter()
    print(f"Finished in {round(main_end - main_start, 2)} second(s)")

