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

class rts:
    # initialize the pygame module
    pygame.init()
    
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

    # units on the screen that have been clicked on
    selected_units = []

    # mouse
    mouse_pointer = pygame.Surface((Constants.MOUSE_POINTER_SIZE, Constants.MOUSE_POINTER_SIZE))
    mouse_pointer.fill(Constants.Colors.MOUSE_POINTER_COLOR)
    mouse_pointer_mask = pygame.mask.from_surface(mouse_pointer)
    pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

    #logo
    logo = pygame.image.load("logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption(Constants.GAME_NAME)    
    font = pygame.font.SysFont(Constants.DEFAULT_FONT_NAME, Constants.FONT_SIZE)
    surface = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
    running = True # kill everything

    # game data
    player = Player()
    matrix = None

    # title screen
    def title_loop(self):
        first_open_running = True 
        pygame.display.set_caption("Welcome!")

        while first_open_running:
            self.surface.fill(Constants.Colors.GAME_MAIN_COLOR) # blank out screen to allow refresh

            # create border
            for screen_border in self.border_rects:
                pygame.draw.rect(self.surface, Constants.Colors.ROYAL_PURPLE, screen_border)

            race_mouse_position = pygame.mouse.get_pos()
            self.surface.blit(self.mouse_pointer, race_mouse_position)

            # title screen text
            Utility.draw_center_text(
                self, 
                f"{Constants.GAME_NAME} RTS", 
                Constants.Colors.GAME_TEXT_COLOR, 
                Constants.SCREEN_HEIGHT / 2 - Constants.FONT_SIZE, 
                font_name = Constants.TITLE_FONT, 
                font_size = Constants.TITLE_SCREEN_FONT_SIZE
            )        

            Utility.draw_center_text(                
                self, 
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
            self.surface.fill(Constants.Colors.GAME_MAIN_COLOR) # blank out screen to allow refresh

            for screen_border in self.border_rects:
                pygame.draw.rect(self.surface, Constants.Colors.ROYAL_PURPLE, screen_border)

            # get mouse info
            race_mouse_position = pygame.mouse.get_pos()
            self.surface.blit(self.mouse_pointer, race_mouse_position)

            # buttons!
            Utility.draw_center_text(self, "Select your Race", Constants.Colors.GAME_TEXT_COLOR, text_height, Constants.DEFAULT_FONT_NAME, font_size)

            # goblin
            race_name = "Goblins"
            goblin_button_rect = Utility.create_rect_with_center_text(self, 
                                                                      race_name, 
                                                                      pygame.font.SysFont(Goblin.font, Goblin.font_size),
                                                                      text_height + (Constants.MENU_SPACING * 2), 
                                                                      Constants.SCREEN_WIDTH)            
            goblin_button = GameButton(goblin_button_rect, race_name, font=pygame.font.SysFont(Goblin.font, Goblin.font_size), base_color="White", hovering_color=Goblin.hover_text_color)      
            goblin_button.change_color(race_mouse_position)
            goblin_button.update(self.surface)

            race_name = "Wood Elves"
            elf_button_rect = Utility.create_rect_with_center_text(self, 
                                                                   race_name, 
                                                                   pygame.font.SysFont(Elf.font, Elf.font_size), 
                                                                   text_height + (Constants.MENU_SPACING * 3),
                                                                   Constants.SCREEN_WIDTH)
            elf_button = GameButton(elf_button_rect, text_input=race_name, font=pygame.font.SysFont(Elf.font, Elf.font_size), base_color="White", hovering_color=Elf.hover_text_color)
            elf_button.change_color(race_mouse_position)
            elf_button.update(self.surface)

            race_name = "Humans"
            human_button_rect = Utility.create_rect_with_center_text(self, 
                                                                     race_name, 
                                                                     pygame.font.SysFont(Human.font, Human.font_size), 
                                                                     text_height + (Constants.MENU_SPACING * 4), 
                                                                     Constants.SCREEN_WIDTH)
            human_button = GameButton(human_button_rect, text_input=race_name, font=pygame.font.SysFont(Human.font, Human.font_size), base_color="White", hovering_color=Human.hover_text_color)
            human_button.change_color(race_mouse_position)
            human_button.update(self.surface)

            race_name = "Fae"
            fae_button_rect = Utility.create_rect_with_center_text(self, 
                                                                   race_name, 
                                                                   pygame.font.SysFont(Fae.font, Fae.font_size), 
                                                                   text_height + (Constants.MENU_SPACING * 5),
                                                                   Constants.SCREEN_WIDTH)
            fae_button = GameButton(fae_button_rect, text_input=race_name, font=pygame.font.SysFont(Fae.font, Fae.font_size), base_color="White", hovering_color=Fae.hover_text_color)
            fae_button.change_color(race_mouse_position)
            fae_button.update(self.surface)

            race_name = "Dwarve"
            dwarf_button_rect = Utility.create_rect_with_center_text(self, 
                                                                     race_name.upper(), 
                                                                     pygame.font.SysFont(Dwarf.font, Dwarf.font_size), 
                                                                     text_height + (Constants.MENU_SPACING * 6), 
                                                                     Constants.SCREEN_WIDTH)
            dwarf_button = GameButton(dwarf_button_rect, text_input=race_name.upper(), font=pygame.font.SysFont(Dwarf.font, Dwarf.font_size), base_color="White", hovering_color=Dwarf.hover_text_color)
            dwarf_button.change_color(race_mouse_position)
            dwarf_button.update(self.surface)

            # event loop for option selection screen
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if goblin_button.check_position(race_mouse_position):
                        self.player.selected_race = Goblin()
                        race_select_running = False
                    if elf_button.check_position(race_mouse_position):
                        self.player.selected_race = Elf()
                        race_select_running = False
                    if human_button.check_position(race_mouse_position):
                        self.player.selected_race = Human()
                        race_select_running = False    
                    if fae_button.check_position(race_mouse_position):
                        self.player.selected_race = Fae()
                        race_select_running = False  
                    if dwarf_button.check_position(race_mouse_position):
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
            self.surface.fill(Constants.Colors.GAME_MAIN_COLOR) # blank out screen to allow refresh

            # create ALICE_BLUE border
            for screen_border in self.border_rects:
                pygame.draw.rect(self.surface, Constants.Colors.PLUM, screen_border)

            race_mouse_position = pygame.mouse.get_pos()
            self.surface.blit(self.mouse_pointer, race_mouse_position)

            race_button_rect = Utility.create_rect_with_center_text(self, "Choose Race", self.font, Constants.MENU_FIRST_BUTTON, Constants.SCREEN_WIDTH)
            race_button = GameButton(race_button_rect, text_input="Choose Race", font=self.font, base_color="White", hovering_color="Green")
            race_button.change_color(race_mouse_position)
            race_button.update(self.surface)

            quit_button_rect = Utility.create_rect_with_center_text(self, "Quit", self.font, Constants.MENU_FIRST_BUTTON + (Constants.MENU_SPACING * 1), Constants.SCREEN_WIDTH)
            quit_button = GameButton(quit_button_rect, text_input="Quit", font=self.font, base_color="White", hovering_color="Green")
            quit_button.change_color(race_mouse_position)
            quit_button.update(self.surface)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(f"mouse down: {event}")
                    if race_button.check_position(race_mouse_position):
                        pause_game_menu_loop_running = False
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

    # the game..
    def main_game_loop(self):        
        game_init_start = time.perf_counter()
        main_game_running = True 
        pygame.display.set_caption(self.main_caption)

        clock = pygame.time.Clock()
        print(f"Started clock: {clock}")

        # get grid of screen based on unit size
        grid = Utility.get_empty_grid(self)
        
        #  refresh side panel / highlight a unit that's hovered over
        side_panel_rects = Utility.draw_side_panel(self)

        # update grid with nodes we cannot walk on
        obstacles = Utility.create_terrain(self, grid, side_panel_rects)

        grid = Utility.update_grid_with_terrain(self, grid, obstacles)

        # be hit 60 times every seconds
        hero_unit_created = False
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
                self.surface.fill(Constants.Colors.HUNTER_GREEN) 

                # mouse position
                mouse_pos = pygame.mouse.get_pos()

                # create terrain environment
                Utility.draw_terrain(self, obstacles)

                # create initial unit
                if hero_unit_created:
                    # draw units on field
                    for army_unit in self.player.army:
                        Utility.create_unit(self, army_unit, army_unit)
                else:
                    Utility.create_unit(self, self.player.selected_race.hero_character)
                    hero_unit_created = True

                # # check for fire damage
                # for army_unit in self.player.army:
                #     if obstacles.colliderect(army_unit.Rect_Settings.Rect):
                #         print("YOU BURNT! - this should be move to somewhere else and slowed down to something like once hurt per .5 second")

                # add mouse pointer
                self.surface.blit(self.mouse_pointer, mouse_pos)

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
                    self, Utility.select_unit(self, selected_unit)
                    # if we have a unit selected, show it in the bottom window
                    if len(self.selected_units) > 0:
                        Utility.create_bottom_panel(self)
                
                #  refresh side panel / highlight a unit that's hovered over
                Utility.draw_side_panel(self, mouse_pos, side_panel_rects)

                # create border last to cover anything up
                for screen_border in self.border_rects:
                    pygame.draw.rect(self.surface, Constants.Colors.GAME_MAIN_BORDER_COLOR, screen_border)

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
                                self, Utility.select_unit(self, unit)
                                Utility.create_bottom_panel(self)

                    # if we selected something new cool, if not, then the order it to move..
                    if not selected_new_unit and len(self.selected_units) > 0:
                        for army_unit in self.selected_units:
                            if army_unit.Moving_Thread is None:                        
                                # submit - execute once, returns future
                                unit_moving_threads.append(executor.submit(Utility.move_unit_over_time, self, grid, army_unit, mouse_pos[0], mouse_pos[1]))
                elif mouse[1] == True:
                    Utility.show_grid(self, grid, mouse_pos)
                elif mouse[2] == True:
                    pass
                    # print(f"right mouse: {pos}")

                # reset army 
                for f in concurrent.futures.as_completed(unit_moving_threads):
                    print(f"f: {f.result()}")
                    army_unit.Moving_Thread = None
                    grid.cleanup()
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
            self.surface.fill(Constants.Colors.GAME_MAIN_COLOR) # blank out screen to allow refresh
            if first_opened:
                first_opened = self.title_loop()
            elif (self.player.selected_race is None):
                self.race_select_loop()
            else:   
                # i = 0
                # for f in pygame.font.get_fonts():                    
                #     print(f)
                #     Utility.loop_fonts(self, f, i)
                #     i += 48
                #     pygame.display.flip()
                #     if i > 990:
                #         i = 0
                #         self.surface.fill(Constants.Colors.HUNTER_GREEN) 
                #         time.sleep(5)

                self.main_game_loop()
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    main_start = time.perf_counter()
    rts().main()
    main_end = time.perf_counter()
    print(f"Finished in {round(main_end - main_start, 2)} second(s)")

