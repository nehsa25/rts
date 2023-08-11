# import the pygame module, so you can use it
import random
import time
#from threading import Thread
import concurrent.futures
import pygame

# our stuff
from utility import Utility
from player import Player
from elf import Elf
from goblin import Goblin
from human import Human
from fae import Fae
from dwarf import Dwarf
from gamebutton import GameButton
from constants import Constants
from pygameutility import PygameUtilities

class rts:
    pgu = PygameUtilities()
    ut = Utility()
    
    # main window title
    main_caption = f"{Constants.GAME_NAME} - GLHF!"

    # screen border
    border_rects = []
    top_border_rect = pygame.Rect(0, 0, Constants.SCREEN_WIDTH, Constants.GAME_MAIN_BORDER_SIZE)
    border_rects.append(top_border_rect)

    bottom_border_rect = pygame.Rect(0, Constants.SCREEN_HEIGHT-Constants.GAME_MAIN_BORDER_SIZE, Constants.SCREEN_WIDTH, Constants.GAME_MAIN_BORDER_SIZE)
    border_rects.append(bottom_border_rect)

    left_border_rect = pygame.Rect(0, 0, Constants.GAME_MAIN_BORDER_SIZE, Constants.SCREEN_WIDTH)
    border_rects.append(left_border_rect)

    right_border_rect = pygame.Rect(Constants.SCREEN_WIDTH - Constants.GAME_MAIN_BORDER_SIZE, 0, Constants.GAME_MAIN_BORDER_SIZE, Constants.SCREEN_HEIGHT)
    border_rects.append(right_border_rect)

    #logo
    logo = pygame.image.load("logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption(Constants.GAME_NAME)    

    running = True # kill everything if this gets set to false

    # game data
    player = Player()
    matrix = None
    grid = None
    side_panel_rects = None
    obstacles = None    
    selected_units = [] # units on the screen that have been clicked on
    loading_msg = ""
    hero_unit_created = False

    # title screen
    def title_loop(self):
        first_open_running = True 
        pygame.display.set_caption("Welcome!")

        while first_open_running:
            self.pgu.surface.fill(Constants.Colors.GAME_MAIN_COLOR) # blank out screen to allow refresh

            # create border
            for screen_border in self.border_rects:
                pygame.draw.rect(self.pgu.surface, Constants.Colors.ROYAL_PURPLE, screen_border)

            self.ut.update_mouse(self.pgu)

            # title screen text
            self.pgu.draw_center_text(
                f"{Constants.GAME_NAME} RTS", 
                Constants.Colors.GAME_TEXT_COLOR, 
                Constants.SCREEN_HEIGHT / 2 - Constants.FONT_SIZE, 
                font_name = Constants.TITLE_FONT, 
                font_size = Constants.TITLE_SCREEN_FONT_SIZE
            )        

            self.pgu.draw_center_text(
                "press SPACE or CLICK to begin!", 
                Constants.Colors.GAME_TEXT_COLOR,
                Constants.SCREEN_HEIGHT - Constants.FONT_SIZE - 50,
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

            # print("first_open loop...")
            pygame.display.flip()

        return False
    
    # race select screen
    def race_select_loop(self):
        race_select_running = True 
        pygame.display.set_caption("Select your Race")
        font_size = 60
        base_height = Constants.SCREEN_HEIGHT / 2 - font_size # true center height # .5 of 1024 = 512
        text_height = base_height / 2 # .5 of 512 = 256

        while race_select_running:
            self.pgu.surface.fill(Constants.Colors.GAME_MAIN_COLOR) # blank out screen to allow refresh

            for screen_border in self.border_rects:
                pygame.draw.rect(self.pgu.surface, Constants.Colors.ROYAL_PURPLE, screen_border)

            # get mouse info
            mouse_pos = pygame.mouse.get_pos()          
            self.ut.update_mouse(self.pgu, mouse_pos)

            # buttons!
            self.pgu.draw_center_text("Select your Race", Constants.Colors.GAME_TEXT_COLOR, text_height, Constants.DEFAULT_FONT_NAME, font_size)

            # goblin
            race_name = "Goblins"
            goblin_button_rect = self.pgu.create_rect_with_center_text(race_name, 
                                                                      pygame.font.SysFont(Goblin.font, Goblin.font_size),
                                                                      text_height + (Constants.MENU_SPACING * 2), 
                                                                      Constants.SCREEN_WIDTH)            
            goblin_button = GameButton(goblin_button_rect, race_name, font=pygame.font.SysFont(Goblin.font, Goblin.font_size), base_color="White", hovering_color=Goblin.hover_text_color)      
            goblin_button.change_color(mouse_pos)
            goblin_button.update(self.pgu.surface)

            race_name = "Wood Elves"
            elf_button_rect = self.pgu.create_rect_with_center_text(race_name, 
                                                                   pygame.font.SysFont(Elf.font, Elf.font_size), 
                                                                   text_height + (Constants.MENU_SPACING * 3),
                                                                   Constants.SCREEN_WIDTH)
            elf_button = GameButton(elf_button_rect, text_input=race_name, font=pygame.font.SysFont(Elf.font, Elf.font_size), base_color="White", hovering_color=Elf.hover_text_color)
            elf_button.change_color(mouse_pos)
            elf_button.update(self.pgu.surface)

            race_name = "Humans"
            human_button_rect = self.pgu.create_rect_with_center_text(race_name, 
                                                                     pygame.font.SysFont(Human.font, Human.font_size), 
                                                                     text_height + (Constants.MENU_SPACING * 4), 
                                                                     Constants.SCREEN_WIDTH)
            human_button = GameButton(human_button_rect, text_input=race_name, font=pygame.font.SysFont(Human.font, Human.font_size), base_color="White", hovering_color=Human.hover_text_color)
            human_button.change_color(mouse_pos)
            human_button.update(self.pgu.surface)

            race_name = "Fae"
            fae_button_rect = self.pgu.create_rect_with_center_text(race_name, 
                                                                   pygame.font.SysFont(Fae.font, Fae.font_size), 
                                                                   text_height + (Constants.MENU_SPACING * 5),
                                                                   Constants.SCREEN_WIDTH)
            fae_button = GameButton(fae_button_rect, text_input=race_name, font=pygame.font.SysFont(Fae.font, Fae.font_size), base_color="White", hovering_color=Fae.hover_text_color)
            fae_button.change_color(mouse_pos)
            fae_button.update(self.pgu.surface)

            race_name = "Dwarve"
            dwarf_button_rect = self.pgu.create_rect_with_center_text(race_name.upper(), 
                                                                     pygame.font.SysFont(Dwarf.font, Dwarf.font_size), 
                                                                     text_height + (Constants.MENU_SPACING * 6), 
                                                                     Constants.SCREEN_WIDTH)
            dwarf_button = GameButton(dwarf_button_rect, text_input=race_name.upper(), font=pygame.font.SysFont(Dwarf.font, Dwarf.font_size), base_color="White", hovering_color=Dwarf.hover_text_color)
            dwarf_button.change_color(mouse_pos)
            dwarf_button.update(self.pgu.surface)

            # event loop for option selection screen
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if goblin_button.check_position(mouse_pos):
                        self.player.selected_race = Goblin()
                        race_select_running = False
                    if elf_button.check_position(mouse_pos):
                        self.player.selected_race = Elf()
                        race_select_running = False
                    if human_button.check_position(mouse_pos):
                        self.player.selected_race = Human()
                        race_select_running = False    
                    if fae_button.check_position(mouse_pos):
                        self.player.selected_race = Fae()
                        race_select_running = False  
                    if dwarf_button.check_position(mouse_pos):
                        self.player.selected_race = Dwarf()
                        race_select_running = False            
                if event.type == pygame.QUIT:
                    race_select_running = False
                    self.running = False
            
            # print("Updating options loop")
            pygame.display.flip()

    # pause screen (when you press esc)
    def pause_game_menu_loop(self):
        pause_game_menu_loop_running = True 
        pygame.display.set_caption(f"Paused!")

        while pause_game_menu_loop_running:
            self.pgu.surface.fill(Constants.Colors.GAME_MAIN_COLOR) # blank out screen to allow refresh

            # border
            for screen_border in self.border_rects:
                pygame.draw.rect(self.pgu.surface, Constants.Colors.PLUM, screen_border)

            race_mouse_position = pygame.mouse.get_pos()
            self.pgu.surface.blit(self.mouse_pointer, race_mouse_position)

            pause_y = Constants.SCREEN_HEIGHT / 2 - Constants.FONT_SIZE
            race_button_rect = self.pgu.create_rect_with_center_text("Choose Race", self.font, pause_y, Constants.SCREEN_WIDTH)
            race_button = GameButton(race_button_rect, text_input="Choose Race", font=self.font, base_color="White", hovering_color="Green")
            race_button.change_color(race_mouse_position)
            race_button.update(self.pgu.surface)

            quit_button_rect = self.pgu.create_rect_with_center_text("Quit", self.font, pause_y + (Constants.MENU_SPACING * 1), Constants.SCREEN_WIDTH)
            quit_button = GameButton(quit_button_rect, text_input="Quit", font=self.font, base_color="White", hovering_color="Green")
            quit_button.change_color(race_mouse_position)
            quit_button.update(self.pgu.surface)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(f"mouse down: {event}")
                    if race_button.check_position(race_mouse_position):
                        pause_game_menu_loop_running = False
                        self.hero_unit_created = False
                        self.race_select_loop()
                    if quit_button.check_position(race_mouse_position):
                        pause_game_menu_loop_running = False
                        self.running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    print(f"mouse up: {event}")
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
        loading_screen_loop_running = True 
        pygame.display.set_caption(f"Loading!")

        clock = pygame.time.Clock()
        print(f"Started clock: {clock}")

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

            # mouse
            self.ut.update_mouse(self.pgu)

            # border
            for screen_border in self.border_rects:
                pygame.draw.rect(self.pgu.surface, Constants.Colors.PLUM, screen_border)
            
            # main font
            font_size = 72
            loading_rect_y = Constants.SCREEN_HEIGHT / 2 - font_size
            text = Constants.LOADING_MSG
            rect = self.pgu.draw_center_text(text, Constants.Colors.ROYAL_GOLD, loading_rect_y, font_name = Constants.DEFAULT_FONT_NAME, font_size = font_size)

            font_size = 36
            loading_rect_y = (Constants.SCREEN_HEIGHT / 4 - font_size) * 3
            text = ""
            if state != "":
                if self.loading_msg !=  "":
                    text = self.loading_msg               
                self.pgu.draw_center_text(text, Constants.Colors.CRIMSON, loading_rect_y, font_name = Constants.DEFAULT_FONT_NAME, font_size = font_size)

            # update entire display
            pygame.display.flip()

            # the work..
            if not loading:
                load_env = True # load obstacles or not
                loading_threads.append(executor.submit(self.ut.load_grid, self.pgu, self.grid, load_env))
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
                    self.grid = result[0]  
                    self.obstacles = result[1]      
                    loading_screen_loop_running = False

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(f"mouse down: {event}")
            if event.type == pygame.MOUSEBUTTONUP:
                print(f"mouse up: {event}")
            if event.type == pygame.KEYDOWN:
                print(f"key down: {event}")
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                loading_screen_loop_running = False
                self.running = False

    # the game..
    def main_game_loop(self):        
        game_init_start = time.perf_counter()
        main_game_running = True 

        clock = pygame.time.Clock()
        print(f"main_game_loop: Started clock: {clock}")

        self.loading_screen_loop()

        pygame.display.set_caption(self.main_caption)

        # similate army
        for i in range(0, 3):
            troop = random.choice(self.player.selected_race.units)
            self.ut.create_unit(self.pgu, self.player, troop["Type"])
            pass

        # be hit 60 times every seconds        
        game_init_end = time.perf_counter()
        print(f"Game initialization ended in {round(game_init_end - game_init_start, 2)} second(s)")

        unit_moving_threads = []
        while main_game_running:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                game_start = time.perf_counter()

                # slow things down
                # print(f"Setting clock to 60 FPS")
                clock.tick(60)

                # blank out screen so we can redraw it
                self.pgu.surface.fill(Constants.Colors.GAME_MAP_COLOR) 

                # mouse position
                mouse_pos = pygame.mouse.get_pos()

                # create terrain environment
                self.ut.draw_terrain(self.pgu, self.obstacles)

                # # check for fire damage
                # for army_unit in self.player.army:
                #     if obstacles.colliderect(army_unit.Rect_Settings.Rect):
                #         print("YOU BURNT! - this should be move to somewhere else and slowed down to something like once hurt per .5 second")

                # add mouse pointer
                self.ut.update_mouse(self.pgu, mouse_pos, self.ut.mouse_pointer)
                
                # continuous key movement (fast)
                key = pygame.key.get_pressed()            
                if key[pygame.K_a] or key[pygame.K_LEFT] == True:
                    pass
                elif key[pygame.K_d] or key[pygame.K_RIGHT] == True:
                    pass
                elif key[pygame.K_w] or key[pygame.K_UP] == True:
                    pass
                elif key[pygame.K_s] or key[pygame.K_DOWN] == True:
                    pass

                # scan for selected units on each redraw
                for selected_unit in self.selected_units:
                    self.ut.select_unit(self.pgu, selected_unit)
                    # if we have a unit selected, show it in the bottom window
                    if len(self.selected_units) > 0:
                        self.ut.create_bottom_panel(self.pgu, self.player)
                
                #  refresh side panel / highlight a unit that's hovered over
                self.ut.draw_side_panel(self.pgu, rect_settings=self.side_panel_rects, player=self.player)

                # refresh spawn point
                self.ut.draw_spawn_points(self.pgu)

                # create initial unit
                if self.hero_unit_created:
                    # draw units on field
                    for army_unit in self.player.army:
                        self.ut.create_unit(self.pgu, self.player, army_unit, army_unit)
                else:
                    self.ut.create_unit(self.pgu, self.player, self.player.selected_race.hero_character)
                    self.hero_unit_created = True
                    
                # create border last to cover anything up
                for screen_border in self.border_rects:
                    pygame.draw.rect(self.pgu.surface, Constants.Colors.GAME_MAIN_BORDER_COLOR, screen_border)

                # continuous mouse movement (fast)
                mouse = pygame.mouse.get_pressed()            
                if mouse[0] == True:
                    # print(f"left mouse: {pos}")

                    # scan unit for select      
                    selected_new_unit = False
                    for unit in self.player.army:
                        if unit.Rect_Settings.Rect.collidepoint(mouse_pos):                        
                            self.selected_units = [] # if we clicked a different troop unit and only used left mouse (not CTRL for example), start over                
                            self.selected_units.append(unit)
                            selected_new_unit = True

                            # if we any unit selected, show it in the bottom window and indicate it's selected with border
                            if len(self.selected_units) > 0:
                                self.ut.select_unit(self.pgu, unit)
                                self.ut.create_bottom_panel(self.pgu, self.player)

                    # if we selected something new cool, if not, then the order it to move..
                    if not selected_new_unit and len(self.selected_units) > 0:
                        for army_unit in self.selected_units:
                            if army_unit.Moving_Thread is None:                        
                                # submit - execute once, returns future
                                unit_moving_threads.append(executor.submit(self.ut.move_unit_over_time, self.pgu, self.grid, army_unit, mouse_pos[0], mouse_pos[1]))
                elif mouse[1] == True:
                    self.pgu.show_grid(self.grid, mouse_pos)
                elif mouse[2] == True:
                    pass
                    # print(f"right mouse: {pos}")

                # reset army 
                for f in concurrent.futures.as_completed(unit_moving_threads):
                    print(f"f: {f.result()}")
                    army_unit.Moving_Thread = None
                    self.grid.cleanup()
                    unit_moving_threads.remove(f)

                # event handling, gets all event from the event queue.  These events are only fired once so good for menus or single movement but not for continuous
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        print(f"mouse down: {event}")
                    if event.type == pygame.MOUSEBUTTONUP:
                        print(f"mouse up: {event}")
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.pause_game_menu_loop()
                            if self.running == False:
                                main_game_running = False
                    if event.type == pygame.QUIT:
                        # change the value to False, to exit the main loop
                        main_game_running = False
                        self.running = False

                # print("Main game loop...")
                game_end = time.perf_counter()
                # print(f"FPS: {round(60 - (game_end - game_start), 2)} second(s)")
                pygame.display.flip()

    def main(self):     
        first_opened = True
        while self.running:
            if first_opened:
                first_opened = self.title_loop()
            elif (self.player.selected_race is None):
                self.race_select_loop()
            else:   
                # i = 0
                # for f in pygame.font.get_fonts():                    
                #     print(f)
                #     ut.loop_fonts(f, i)
                #     i += 48
                #     pygame.display.flip()
                #     if i > 990:
                #         i = 0
                #         self.pgu.surface.fill(Constants.Colors.HUNTER_GREEN) 
                #         time.sleep(5)

                self.main_game_loop()
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    main_start = time.perf_counter()
    rts().main()
    main_end = time.perf_counter()
    print(f"Finished in {round(main_end - main_start, 2)} second(s)")

