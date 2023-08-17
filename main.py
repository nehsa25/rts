import concurrent.futures
import time
import pygame
import inspect

# our stuff
from utility import Utility
from gamedata import GameData
from elf import Elf
from goblin import Goblin
from human import Human
from fae import Fae
from dwarf import Dwarf
from arguna import Arguna
from gamebutton import GameButton
from nyrriss import Nyrriss
from constants import Constants
from pygameutility import PygameUtilities
from tile import Tiles
from logutiliites import LogUtilities
from unit import Unit
from events import Events
from gamedata import GameData

class unhingedrts:
    # main window title
    main_caption = f"{Constants.GAME_NAME} - GLHF!"
    logo = None
    running = True
    GameData = None
    events = None
    hero_unit_created = False
    loading_msg = ""
    selected_units = [] # units on the screen that have been clicked on
    selected_map = None
    
    def __init__(self):
        self.logutils = LogUtilities()
        self.pgu = PygameUtilities(self.logutils)
        self.ut = Utility(self.logutils)
        self.GameData = GameData(self.logutils)  
        self.tiles = Tiles(self.logutils)
        self.events = Events(self.logutils, self.pgu)

        #logo
        self.logo = pygame.image.load("logo.png")
        pygame.display.set_icon(self.logo)
        pygame.display.set_caption(Constants.GAME_NAME) 
        
    # title screen
    def title_loop(self):
        self.logutils.log.debug(f"Inside title_loop: {inspect.currentframe().f_code.co_name}")
        first_open_running = True         
        pygame.display.set_caption("Welcome!")

        while first_open_running:
            self.pgu.surface.fill(Constants.Colors.GAME_MAIN_COLOR) # blank out screen to allow refresh

            # draw border
            self.ut.create_border(self.pgu)

            self.pgu.update_mouse()

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
        self.logutils.log.debug(f"Inside race_select_loop: {inspect.currentframe().f_code.co_name}")
        race_select_running = True 
        pygame.display.set_caption("Select your Race")
        font_size = 60
        base_height = Constants.SCREEN_HEIGHT_PX / 2 - font_size # true center height # .5 of 1024 = 512
        text_height = base_height / 2 # .5 of 512 = 256

        while race_select_running:
            self.pgu.surface.fill(Constants.Colors.GAME_MAIN_COLOR) # blank out screen to allow refresh

            # draw border
            self.ut.create_border(self.pgu)

            # get mouse info
            mouse_pos = pygame.mouse.get_pos()          
            self.pgu.update_mouse(mouse_pos)

            # buttons!
            self.pgu.draw_center_text("Select your Race", Constants.Colors.GAME_TEXT_COLOR, text_height, Constants.FONT_NAME_DEFAULT, font_size)

            # goblin
            race_name = "Goblins"
            goblin_button_rect = self.pgu.create_rect_with_center_text(race_name, 
                                                                      pygame.font.SysFont(Goblin.font, Goblin.font_size),
                                                                      text_height + (Constants.MENU_SPACING_PX * 2), 
                                                                      Constants.SCREEN_WIDTH_PX)            
            goblin_button = GameButton(goblin_button_rect, race_name, 
                                        font=pygame.font.SysFont(Goblin.font, Goblin.font_size),
                                            base_color="White", hovering_color=Goblin.hover_text_color)      
            goblin_button.change_color(mouse_pos)
            goblin_button.update(self.pgu.surface)

            race_name = "Wood Elves"
            elf_button_rect = self.pgu.create_rect_with_center_text(race_name, 
                                                                   pygame.font.SysFont(Elf.font, Elf.font_size), 
                                                                   text_height + (Constants.MENU_SPACING_PX * 3),
                                                                   Constants.SCREEN_WIDTH_PX)
            elf_button = GameButton(elf_button_rect, text_input=race_name, 
                                    font=pygame.font.SysFont(Elf.font, Elf.font_size), 
                                        base_color="White", hovering_color=Elf.hover_text_color)
            elf_button.change_color(mouse_pos)
            elf_button.update(self.pgu.surface)

            race_name = "Humans"
            human_button_rect = self.pgu.create_rect_with_center_text(race_name, 
                                                                     pygame.font.SysFont(Human.font, Human.font_size), 
                                                                     text_height + (Constants.MENU_SPACING_PX * 4), 
                                                                     Constants.SCREEN_WIDTH_PX)
            human_button = GameButton(human_button_rect, text_input=race_name, 
                                      font=pygame.font.SysFont(Human.font, Human.font_size), 
                                        base_color="White", hovering_color=Human.hover_text_color)
            human_button.change_color(mouse_pos)
            human_button.update(self.pgu.surface)

            race_name = "Fae"
            fae_button_rect = self.pgu.create_rect_with_center_text(race_name, 
                                                                   pygame.font.SysFont(Fae.font, Fae.font_size), 
                                                                   text_height + (Constants.MENU_SPACING_PX * 5),
                                                                   Constants.SCREEN_WIDTH_PX)
            fae_button = GameButton(fae_button_rect, text_input=race_name, 
                                    font=pygame.font.SysFont(Fae.font, Fae.font_size), 
                                        base_color="White", hovering_color=Fae.hover_text_color)
            fae_button.change_color(mouse_pos)
            fae_button.update(self.pgu.surface)

            race_name = "Dwarve"
            dwarf_button_rect = self.pgu.create_rect_with_center_text(race_name.upper(), 
                                                                     pygame.font.SysFont(Dwarf.font, Dwarf.font_size), 
                                                                     text_height + (Constants.MENU_SPACING_PX * 6), 
                                                                     Constants.SCREEN_WIDTH_PX)
            dwarf_button = GameButton(dwarf_button_rect, text_input=race_name.upper(), 
                                      font=pygame.font.SysFont(Dwarf.font, Dwarf.font_size), 
                                        base_color="White", hovering_color=Dwarf.hover_text_color)
            dwarf_button.change_color(mouse_pos)
            dwarf_button.update(self.pgu.surface)

            race_name = "Nyrriss"
            nyrriss_button_rect = self.pgu.create_rect_with_center_text(race_name, 
                                                                     pygame.font.SysFont(Nyrriss.font, Nyrriss.font_size), 
                                                                     text_height + (Constants.MENU_SPACING_PX * 7), 
                                                                     Constants.SCREEN_WIDTH_PX)
            nyrriss_button = GameButton(nyrriss_button_rect, text_input=race_name, 
                                        font=pygame.font.SysFont(Nyrriss.font, Nyrriss.font_size), 
                                            base_color="White", hovering_color=Nyrriss.hover_text_color)
            nyrriss_button.change_color(mouse_pos)
            nyrriss_button.update(self.pgu.surface)

            race_name = "Arguna"
            arguna_button_rect = self.pgu.create_rect_with_center_text(race_name, 
                                                                     pygame.font.SysFont(Nyrriss.font, Nyrriss.font_size), 
                                                                     text_height + (Constants.MENU_SPACING_PX * 8), 
                                                                     Constants.SCREEN_WIDTH_PX)
            arguna_button = GameButton(arguna_button_rect, text_input=race_name, 
                                        font=pygame.font.SysFont(Arguna.font, Arguna.font_size), 
                                            base_color="White", hovering_color=Arguna.hover_text_color)
            arguna_button.change_color(mouse_pos)
            arguna_button.update(self.pgu.surface)


            # event loop for option selection screen
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if goblin_button.check_position(mouse_pos):
                        self.GameData.Player.selected_race = Goblin(self.logutils)
                        race_select_running = False
                    if elf_button.check_position(mouse_pos):
                        self.GameData.Player.selected_race = Elf(self.logutils)
                        race_select_running = False
                    if human_button.check_position(mouse_pos):
                        self.GameData.Player.selected_race = Human(self.logutils)
                        race_select_running = False    
                    if fae_button.check_position(mouse_pos):
                        self.GameData.Player.selected_race = Fae(self.logutils)
                        race_select_running = False  
                    if dwarf_button.check_position(mouse_pos):
                        self.GameData.Player.selected_race = Dwarf(self.logutils)
                        race_select_running = False   
                    if nyrriss_button.check_position(mouse_pos):
                        self.GameData.Player.selected_race = Nyrriss(self.logutils)
                        race_select_running = False          
                    if arguna_button.check_position(mouse_pos):
                        self.GameData.Player.selected_race = Arguna(self.logutils)
                        race_select_running = False   

                if event.type == pygame.QUIT:
                    race_select_running = False
                    self.running = False
            pygame.display.flip()

    # options
    def options_loop(self):
        self.logutils.log.debug(f"Inside options_loop: {inspect.currentframe().f_code.co_name}")
        options_loop_running = True 
        pygame.display.set_caption(f"Options")

        while options_loop_running:
            self.pgu.surface.fill(Constants.Colors.GAME_MAIN_COLOR) # blank out screen to allow refresh

            # draw border
            self.ut.create_border(self.pgu)

            mouse_pos = pygame.mouse.get_pos()
            self.pgu.update_mouse(mouse_pos)

            pause_y = Constants.SCREEN_HEIGHT_PX / 2 - Constants.FONT_SIZE_DEFAULT_PX
            font = pygame.font.SysFont(Constants.FONT_NAME_DEFAULT, Constants.DEFAULT_FONT_SIZE)

            show_grid_rect = self.pgu.create_rect_with_center_text("Show Grid", font, pause_y, Constants.SCREEN_WIDTH_PX)
            show_grid = GameButton(show_grid_rect, text_input="Choose Race", font=font, base_color="White", hovering_color=Constants.Colors.ROYAL_PURPLE)
            show_grid.change_color(mouse_pos)
            show_grid.update(self.pgu.surface)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.logutils.log.debug(f"mouse down: {event}")
                    if show_grid.check_position(mouse_pos):
                        options_loop_running = False
                        self.hero_unit_created = False
                        self.race_select_loop()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.logutils.log.debug(f"mouse up: {event}")
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
        self.logutils.log.debug(f"Inside pause_game_menu_loop: {inspect.currentframe().f_code.co_name}")
        pause_game_menu_loop_running = True 
        pygame.display.set_caption(f"Paused!")

        while pause_game_menu_loop_running:
            self.pgu.surface.fill(Constants.Colors.GAME_MAIN_COLOR) # blank out screen to allow refresh

            # draw border
            self.ut.create_border(self.pgu)

            mouse_pos = pygame.mouse.get_pos()
            self.pgu.update_mouse(mouse_pos)

            pause_y = Constants.SCREEN_HEIGHT_PX / 2 - Constants.FONT_SIZE_DEFAULT_PX
            font = pygame.font.SysFont(Constants.FONT_NAME_DEFAULT, 48)

            race_button_rect = self.pgu.create_rect_with_center_text("Choose Race", font, pause_y, Constants.SCREEN_WIDTH_PX)
            race_button = GameButton(race_button_rect, text_input="Choose Race", font=font, base_color="White", hovering_color=Constants.Colors.ROYAL_PURPLE)
            race_button.change_color(mouse_pos)
            race_button.update(self.pgu.surface)

            options_rect = self.pgu.create_rect_with_center_text("Options", font, pause_y + (Constants.MENU_SPACING_PX * 1), Constants.SCREEN_WIDTH_PX)
            options_button = GameButton(options_rect, text_input="Options", font=font, base_color="White", hovering_color=Constants.Colors.ROYAL_PURPLE)
            options_button.change_color(mouse_pos)
            options_button.update(self.pgu.surface)

            quit_button_rect = self.pgu.create_rect_with_center_text("Quit", font, pause_y + (Constants.MENU_SPACING_PX * 2), Constants.SCREEN_WIDTH_PX)
            quit_button = GameButton(quit_button_rect, text_input="Quit", font=font, base_color="White", hovering_color=Constants.Colors.ROYAL_PURPLE)
            quit_button.change_color(mouse_pos)
            quit_button.update(self.pgu.surface)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.logutils.log.debug(f"mouse down: {event}")
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
                    self.logutils.log.debug(f"mouse up: {event}")
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
        self.logutils.log.debug(f"Inside loading_screen_loop: {inspect.currentframe().f_code.co_name}")
        loading_screen_loop_running = True 
        pygame.display.set_caption(f"Loading!")

        clock = pygame.time.Clock()
        self.logutils.log.debug(f"Started clock: {clock}")

        loading_threads = []
        executor = concurrent.futures.ThreadPoolExecutor()
        executor._max_workers = 1
        state = ""
        loading = False
        show_complete = False
        while loading_screen_loop_running:            
            clock.tick(60)                

            # blank out screen to allow refresh
            self.pgu.surface.fill(Constants.Colors.GAME_MAIN_COLOR) 

            # draw border
            self.ut.create_border(self.pgu)

            # mouse
            self.pgu.update_mouse()
            
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
                loading_threads.append(executor.submit(self.tiles.load_grid, self.pgu, self.ut, self.GameData, load_env))
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
                    self.logutils.log.debug(f"Loading complete: {result}")             
                    loading_screen_loop_running = False

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.logutils.log.debug(f"mouse down: {event}")
            if event.type == pygame.MOUSEBUTTONUP:
                self.logutils.log.debug(f"mouse up: {event}")
            if event.type == pygame.KEYDOWN:
                self.logutils.log.debug(f"key down: {event}")
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                loading_screen_loop_running = False
                self.running = False

    # map loading screen
    def map_select_loop(self):
        self.logutils.log.debug(f"Inside map_select_loop: {inspect.currentframe().f_code.co_name}")
        map_select_loop_running = True 
        pygame.display.set_caption(f"Map Selection")

        while map_select_loop_running:
            self.pgu.surface.fill(Constants.Colors.GAME_MAIN_COLOR) # blank out screen to allow refresh

            # draw border
            self.ut.create_border(self.pgu)

            mouse_pos = pygame.mouse.get_pos()
            self.pgu.update_mouse(mouse_pos)
            
            pygame.display.flip()

    # the game..
    def main_game_loop(self):   
        self.logutils.log.debug(f"Inside main_game_loop: {inspect.currentframe().f_code.co_name}")     
        game_init_start = time.perf_counter()
        main_game_running = True 

        clock = pygame.time.Clock()
        self.logutils.log.debug(f"main_game_loop: Started clock: {clock}")

        self.loading_screen_loop()

        pygame.display.set_caption(self.main_caption)

        # similate army
        # for i in range(0, 3):
        #     troop = random.choice(self.GameData.Player.selected_race.units)
        #     self.ut.create_unit(self.pgu, self.player, troop["Type"])
        #     pass

        game_init_end = time.perf_counter()
        self.logutils.log.debug(f"Game initialization ended in {round(game_init_end - game_init_start, 2)} second(s)")

        while main_game_running:
            game_start = time.perf_counter()

            # slow things down
            clock.tick(60)

            # blank out screen so we can redraw it
            self.pgu.surface.fill(Constants.Colors.GAME_MAP_COLOR) 

            # mouse position
            mouse_pos = pygame.mouse.get_pos()

            # create terrain environment
            self.tiles.DrawTerrainTiles(self.pgu)

            # # check for fire damage
            # for army_unit in self.player.army:
            #     if obstacles.colliderect(army_unit.RectSettings.Rect):
            #         self.logutils.log.debug("YOU BURNT! - this should be move to somewhere else and slowed down to something like once hurt per .5 second")

            # add mouse pointer
            self.pgu.update_mouse(mouse_pos, self.pgu.mouse_pointer)
            
            self.events.check_for_events(self.tiles)

            # scan for selected units on each redraw
            for selected_unit in self.selected_units:
                self.ut.select_unit(self.pgu, selected_unit)
                # if we have a unit selected, show it in the bottom window
                if len(self.selected_units) > 0:
                    self.ut.create_bottom_panel(self.pgu, self.player)
            
            #  refresh side panel / highlight a unit that's hovered over
            self.ut.draw_side_panel(self.pgu, player=self.GameData.Player)

            # refresh spawn point
            self.ut.draw_spawn_points(self.pgu, tiles=self.tiles)

            # create initial unit
            if self.hero_unit_created:
                # draw units on field
                for army_unit in self.GameData.Player.army:
                    army_unit.DrawUnit(self.pgu)
            else:
                hero_unit = Unit(self.logutils, self.pgu, self.GameData.Player, unit_type=self.GameData.Player.selected_race.hero_character, tiles=self.tiles)

                hero_unit.AttackTile(3,5)
                self.GameData.Player.army = hero_unit.AddToArmy(self.GameData.Player)
                self.hero_unit_created = True

            # draw border last to cover anything up
            self.ut.create_border(self.pgu)

            # event handling, gets all event from the event queue.  These events are only fired once so good for menus or single movement but not for continuous
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.events.mouse_left_single_event(event, self.GameData.Player, self.ut, self.tiles, self.GameData)
                    if event.button == 2:
                        self.events.mouse_middle_single_event(event)
                    if event.button == 3:
                        self.events.mouse_right_single_event(event)
                if event.type == pygame.MOUSEBUTTONUP:
                    self.logutils.log.debug(f"mouse up: {event}")
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
        self.logutils.log.debug(f"Inside main: {inspect.currentframe().f_code.co_name}")      
        first_opened = True
        while self.running:
            if first_opened:
                first_opened = self.title_loop()
            elif self.GameData.Player.selected_race is None:
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

