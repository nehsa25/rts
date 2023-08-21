import concurrent.futures
import time
import pygame
import random

# our stuff
from gamedata import GameData
from constants import Constants
from logutiliites import LogUtilities

class unhingedrts(object):
    # main window title
    main_caption = f"{Constants.GAME_NAME} - GLHF!"
    logo = None
    running = True
    game_data = None
    hero_unit_created = False
    loading_msg = ""
    selected_units = [] # units on the screen that have been clicked on
    selected_map = None

    def __init__(self):
        self.log_utils = LogUtilities()
        self.game_data = GameData(self.log_utils)  

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
            self.game_data.surface.fill(Constants.Colors.GAME_MAIN_COLOR) # blank out screen to allow refresh
            self.game_data.create_border()
            mouse_pos = self.game_data.update_mouse()

            # title screen text
            self.game_data.draw_center_text(
                Constants.GAME_NAME, 
                Constants.Colors.GAME_TEXT_COLOR, 
                Constants.SCREEN_HEIGHT_PX / 2 - Constants.FONT_SIZE_DEFAULT_PX, 
                font_name = Constants.TITLE_FONT, 
                font_size = Constants.FONT_SIZE_TITLE_PX
            )        

            self.game_data.draw_center_text(
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
            self.game_data.surface.fill(Constants.Colors.GAME_MAIN_COLOR) # blank out screen to allow refresh
            self.game_data.create_border()
            mouse_pos = self.game_data.update_mouse()
            self.game_data.draw_center_text("Select your Race", Constants.Colors.GAME_TEXT_COLOR, select_your_race_text_y, Constants.FONT_NAME_DEFAULT, font_size)
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
            random_button = self.game_data.game_button(self.game_data,rect, 
                                                 race_name,
                                                 font=def_font,
                                                 base_color="White",
                                                 hovering_color=Constants.Colors.DODGER)   
   
            random_button.change_color(mouse_pos)
            random_button.update(self.game_data.surface)
            race_buttons.append(dict(name="random", button=random_button))

            # our races
            for i in range(0, len(self.game_data.races)):
                current_race = self.game_data.races[i]
                race = self.game_data.get_race_by_name(current_race)
                race_font = pygame.font.SysFont(race.font, race.font_size)
                race_button_rect = self.game_data.create_rect_with_center_text(race.name, 
                                                                        race_font,
                                                                        select_your_race_text_y + y_spacer + (Constants.MENU_SPACING_PX * i+1), 
                                                                        Constants.SCREEN_WIDTH_PX)            
                race_button = self.game_data.game_button(self.game_data, 
                                                   race_button_rect, 
                                                   race.name,
                                                   font=race_font,
                                                   base_color="White", 
                                                   hovering_color=race.hover_text_color)      
                race_button.change_color(mouse_pos)
                race_button.update(self.game_data.surface)
                race_buttons.append(dict(name=race, button=race_button))

            # event loop for option selection screen
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for race_button in race_buttons:
                        if race_button["button"].check_position(mouse_pos):
                            selected_race = race_button["name"]

                            # support random case
                            if selected_race == "random":
                                race_string = random.choice(self.game_data.races)
                                selected_race = self.game_data.get_race_by_name(race_string)                               
                            
                            self.game_data.player.selected_race = selected_race
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
            self.game_data.surface.fill(Constants.Colors.GAME_MAIN_COLOR) # blank out screen to allow refresh
            self.game_data.create_border()
            mouse_pos = self.game_data.update_mouse()

            pause_y = Constants.SCREEN_HEIGHT_PX / 2 - Constants.FONT_SIZE_DEFAULT_PX
            font = pygame.font.SysFont(Constants.FONT_NAME_DEFAULT, Constants.FONT_SIZE_DEFAULT_PX)

            show_grid_rect = self.game_data.create_rect_with_center_text("Show Grid", font, pause_y, Constants.SCREEN_WIDTH_PX)
            show_grid = self.game_data.game_button(self.game_data,
                                             show_grid_rect, 
                                             text_input="Choose Race", 
                                             font=font, 
                                             base_color="White", 
                                             hovering_color=Constants.Colors.ROYAL_PURPLE)
            show_grid.change_color(mouse_pos)
            show_grid.update(self.game_data.surface)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.log_utils.log.debug(f"mouse down: {event}")
                    if show_grid.check_position(mouse_pos):
                        options_loop_running = False
                        self.hero_unit_created = False
                        self.game_data_select_loop()
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
            self.game_data.surface.fill(Constants.Colors.GAME_MAIN_COLOR) # blank out screen to allow refresh
            self.game_data.create_border()
            mouse_pos = self.game_data.update_mouse()

            pause_y = Constants.SCREEN_HEIGHT_PX / 2 - Constants.FONT_SIZE_DEFAULT_PX
            font = pygame.font.SysFont(Constants.FONT_NAME_DEFAULT, 48)

            race_button_rect = self.game_data.create_rect_with_center_text("Choose Race", font, pause_y, Constants.SCREEN_WIDTH_PX)
            race_button = self.game_data.game_button(self.game_data,
                                               race_button_rect, 
                                               text_input="Choose Race", 
                                               font=font, base_color="White", 
                                               hovering_color=Constants.Colors.ROYAL_PURPLE)
            race_button.change_color(mouse_pos)
            race_button.update(self.game_data.surface)

            options_rect = self.game_data.create_rect_with_center_text("Options", font, pause_y + (Constants.MENU_SPACING_PX * 1), Constants.SCREEN_WIDTH_PX)
            options_button = self.game_data.game_button(self.game_data, 
                                                  options_rect, 
                                                  text_input="Options", 
                                                  font=font, 
                                                  base_color="White", 
                                                  hovering_color=Constants.Colors.ROYAL_PURPLE)
            options_button.change_color(mouse_pos)
            options_button.update(self.game_data.surface)

            quit_button_rect = self.game_data.create_rect_with_center_text("Quit", font, pause_y + (Constants.MENU_SPACING_PX * 2), Constants.SCREEN_WIDTH_PX)
            quit_button = self.game_data.game_button(self.game_data,
                                               quit_button_rect, 
                                               text_input="Quit", 
                                               font=font, 
                                               base_color="White", 
                                               hovering_color=Constants.Colors.ROYAL_PURPLE)
            quit_button.change_color(mouse_pos)
            quit_button.update(self.game_data.surface)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.log_utils.log.debug(f"mouse down: {event}")
                    if race_button.check_position(mouse_pos):
                        pause_game_menu_loop_running = False
                        self.hero_unit_created = False
                        self.game_data_select_loop()
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
            self.game_data.surface.fill(Constants.Colors.GAME_MAIN_COLOR) # blank out screen to allow refresh
            self.game_data.create_border()
            mouse_pos = self.game_data.update_mouse()
            
            # main font
            font_size = 72
            loading_rect_y = Constants.SCREEN_HEIGHT_PX / 2 - font_size
            text = Constants.LOADING_MSG
            rect = self.game_data.draw_center_text(text, Constants.Colors.ROYAL_GOLD, loading_rect_y, font_name = Constants.FONT_NAME_DEFAULT, font_size = font_size)

            font_size = 36
            loading_rect_y = (Constants.SCREEN_HEIGHT_PX / 4 - font_size) * 3
            text = ""
            if self.loading_msg !=  "":
                text = self.loading_msg               
            self.game_data.draw_center_text(text, Constants.Colors.CRIMSON, loading_rect_y, font_name = Constants.FONT_NAME_DEFAULT, font_size = font_size)

            # update entire display
            pygame.display.flip()

            # the work..
            if not loading:
                load_env = True # load obstacles or not
                loading_threads.append(executor.submit(self.game_data.load_grid, load_env))
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
            self.game_data.surface.fill(Constants.Colors.GAME_MAIN_COLOR) # blank out screen to allow refresh
            self.game_data.create_border()
            mouse_pos = self.game_data.update_mouse()            
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
        #     self.ut.create_unit(self.game_data, self.player, troop["Type"])
        #     pass

        game_init_end = time.perf_counter()
        self.log_utils.log.debug(f"Game initialization ended in {round(game_init_end - game_init_start, 2)} second(s)")

        while main_game_running:
            game_start = time.perf_counter()

            # slow things down
            clock.tick(60)

            self.game_data.surface.fill(Constants.Colors.GAME_MAP_COLOR) # blank out screen to allow refresh
            #self.game_data.create_border()
            mouse_pos = self.game_data.update_mouse()

            # create terrain environment
            self.game_data.DrawTerrainTiles(self.game_data)

            # # check for fire damage
            # for army_unit in self.player.army:
            #     if obstacles.colliderect(army_unit.RectSettings.Rect):
            #         self.logutils.log.debug("YOU BURNT! - this should be move to somewhere else and slowed down to something like once hurt per .5 second")

            # add mouse pointer
            self.game_data.update_mouse(mouse_pos, self.game_data.cursor)
            
            self.game_data.check_for_fast_events()

            # scan for selected units on each redraw
            for selected_unit in self.selected_units:
                self.ut.select_unit(self.game_data, selected_unit)
                # if we have a unit selected, show it in the bottom window
                if len(self.selected_units) > 0:
                    self.ut.create_bottom_panel(self.game_data, self.player)
            
            #  refresh side panel / highlight a unit that's hovered over
            self.game_data.draw_side_panel(player=self.game_data.player)

            # refresh spawn point
            self.game_data.draw_spawn_points()

            # create initial unit
            if self.hero_unit_created:
                # draw units on field
                for army_unit in self.game_data.player.army:
                    army_unit.draw_unit(self.game_data.surface, army_unit.main_color, army_unit.tile.tile_rect_settings.rect)
                    # player.selected_race.main_color, self.tile.tile_rect_settings.rect)
            else:
                hero_unit = self.game_data.player.selected_race.create_unit(self.game_data.player.selected_race.hero, 
                                                                            self.game_data.map_tiles)

                hero_unit.attack_tile(3,5)
                self.game_data.player.army = hero_unit.add_to_army(self.game_data.player)
                self.hero_unit_created = True

            if self.game_data.show_grid:
                self.game_data.show_tile_details()

            # draw border last to cover anything up
            self.game_data.create_border()

            self.game_data.scan_for_slow_events()

            game_end = time.perf_counter()
            # self.log_utils.log.info(f"FPS: {round((game_end - game_start), 2)} second(s)")
            pygame.display.flip()

    def main(self):    
        self.log_utils.log.debug(f"Inside main")      
        first_opened = True
        while self.running:
            if first_opened:
                first_opened = self.title_loop()
            elif self.game_data.player.selected_race is None:
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
