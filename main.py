# import the pygame module, so you can use it
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
    font = pygame.font.SysFont(Constants.DEFAULT_FONT, Constants.FONT_SIZE)
    surface = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
    running = True # kill everything

    # game data
    player = Player()
    matrix = None
    grid = None

    def title_loop(self):
        first_open_running = True 
        pygame.display.set_caption("Welcome!")

        while first_open_running:
            self.surface.fill(Constants.Colors.GAME_MAIN_COLOR) # blank out screen to allow refresh

            # create border
            for screen_border in self.border_rects:
                pygame.draw.rect(self.surface, Constants.Colors.GAME_BORDER, screen_border)

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
                Constants.SCREEN_HEIGHT - Constants.FONT_SIZE - 50
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

    def race_select_loop(self):
        race_select_running = True 
        pygame.display.set_caption("Select your race")
        base_height = Constants.SCREEN_HEIGHT / 2 - Constants.FONT_SIZE # true center height
        text_height = base_height / 2

        while race_select_running:
            self.surface.fill(Constants.Colors.GAME_MAIN_COLOR) # blank out screen to allow refresh

            # create ALICE_BLUE border
            for screen_border in self.border_rects:
                pygame.draw.rect(self.surface, Constants.Colors.ALICE_BLUE, screen_border)

            # get mouse info
            race_mouse_position = pygame.mouse.get_pos()
            self.surface.blit(self.mouse_pointer, race_mouse_position)

            # buttons!
            Utility.draw_center_text(self, "Select your race", Constants.Colors.GAME_TEXT_COLOR, text_height)
            goblin_button_rect = Utility.create_rect_with_center_text(self, "Goblin", self.font, Constants.MENU_FIRST_BUTTON, Constants.SCREEN_WIDTH)
            goblin_button = GameButton(goblin_button_rect, "Goblin", self.font, base_color="White", hovering_color="Green")      
            goblin_button.change_color(race_mouse_position)
            goblin_button.update(self.surface)

            elf_button_rect = Utility.create_rect_with_center_text(self, "Elf", self.font, Constants.MENU_FIRST_BUTTON + (Constants.MENU_SPACING * 1), Constants.SCREEN_WIDTH)
            elf_button = GameButton(elf_button_rect, text_input="Elf", font=self.font, base_color="White", hovering_color="Green")
            elf_button.change_color(race_mouse_position)
            elf_button.update(self.surface)

            human_button_rect = Utility.create_rect_with_center_text(self, "Human", self.font, Constants.MENU_FIRST_BUTTON + (Constants.MENU_SPACING * 2), Constants.SCREEN_WIDTH)
            human_button = GameButton(human_button_rect, text_input="Human", font=self.font, base_color="White", hovering_color="Green")
            human_button.change_color(race_mouse_position)
            human_button.update(self.surface)

            fae_button_rect = Utility.create_rect_with_center_text(self, "Fae", self.font, Constants.MENU_FIRST_BUTTON + (Constants.MENU_SPACING * 3), Constants.SCREEN_WIDTH)
            fae_button = GameButton(fae_button_rect, text_input="Fae", font=self.font, base_color="White", hovering_color="Green")
            fae_button.change_color(race_mouse_position)
            fae_button.update(self.surface)

            dwarf_button_rect = Utility.create_rect_with_center_text(self, "Dwarf", self.font, Constants.MENU_FIRST_BUTTON + (Constants.MENU_SPACING * 4), Constants.SCREEN_WIDTH)
            dwarf_button = GameButton(dwarf_button_rect, text_input="Dwarf", font=self.font, base_color="White", hovering_color="Green")
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

    def main_game_loop(self):        
        game_init_start = time.perf_counter()
        main_game_running = True 
        pygame.display.set_caption(self.main_caption)

        clock = pygame.time.Clock()
        print(f"Started clock: {clock}")

        obstacles = Utility.create_terrain(self)

        self.grid = Utility.get_grid(self, obstacles)

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
                Utility.draw_enviornment(self, obstacles)

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
                                unit_moving_threads.append(executor.submit(Utility.move_unit_over_time, self, army_unit, mouse_pos[0], mouse_pos[1]))
                elif mouse[1] == True:
                    Utility.show_grid(self)
                elif mouse[2] == True:
                    pass
                    # print(f"right mouse: {pos}")

                # reset army 
                for f in concurrent.futures.as_completed(unit_moving_threads):
                    print(f"f: {f.result()}")
                    army_unit.Moving_Thread = None
                    self.grid.cleanup()
                    unit_moving_threads.remove(f)

                #  refresh side panel / highlight a unit that's hovered over
                Utility.draw_side_panel(self, mouse_pos)

                # create border last to cover anything up
                for screen_border in self.border_rects:
                    pygame.draw.rect(self.surface, Constants.Colors.GAME_MAIN_BORDER_COLOR, screen_border)

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
                self.main_game_loop()
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    main_start = time.perf_counter()
    rts().main()
    main_end = time.perf_counter()
    print(f"Finished in {round(main_end - main_start, 2)} second(s)")

