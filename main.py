# import the pygame module, so you can use it
import random
import pygame, sys

# our stuff
from utility import Utility
from player import Player
from elf import Elf
from goblin import Goblin
from human import Human
from fae import Fae
from dwarf import Dwarf
from gamebutton import GameButton
from colors import Colors
from constants import Constants

class rts:
    # initialize the pygame module
    pygame.init()
    
    # main window title
    main_caption = f"{Constants.GAME_NAME} - GLHF!"

    # screen border
    border_rects = []
    top_border_rect = pygame.Rect(0, 0, Constants.SCREEN_WIDTH, Constants.BORDER_SIZE)
    border_rects.append(top_border_rect)

    bottom_border_rect = pygame.Rect(0, Constants.SCREEN_HEIGHT-Constants.BORDER_SIZE, Constants.SCREEN_WIDTH, Constants.BORDER_SIZE)
    border_rects.append(bottom_border_rect)

    left_border_rect = pygame.Rect(0, 0, Constants.BORDER_SIZE, Constants.SCREEN_WIDTH)
    border_rects.append(left_border_rect)

    right_border_rect = pygame.Rect(Constants.SCREEN_WIDTH - Constants.BORDER_SIZE, 0, Constants.BORDER_SIZE, Constants.SCREEN_HEIGHT)
    border_rects.append(right_border_rect)

    # mouse
    mouse_pointer = pygame.Surface((Constants.MOUSE_POINTER_SIZE, Constants.MOUSE_POINTER_SIZE))
    mouse_pointer.fill(Colors.MOUSE_POINTER_COLOR)
    mouse_pointer_mask = pygame.mask.from_surface(mouse_pointer)
    pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

    #logo
    logo = pygame.image.load("logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption(Constants.GAME_NAME)    
    font = pygame.font.SysFont("arialblack", Constants.FONT_SIZE)
    surface = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
    running = True # kill everything

    # game data
    player = Player()

    def first_open_loop(self):
        first_open_running = True 
        pygame.display.set_caption("Welcome!")

        while first_open_running:
            self.surface.fill(Colors.BACKGROUND_COLOR) # blank out screen to allow refresh

            # create yellow border
            for screen_border in self.border_rects:
                pygame.draw.rect(self.surface, Colors.YELLOW, screen_border)

            race_mouse_position = pygame.mouse.get_pos()
            self.surface.blit(self.mouse_pointer, race_mouse_position)

            Utility.draw_center_text(self, f"Welcome to {Constants.GAME_NAME}!", Colors.TEXT_COLOR, Constants.SCREEN_HEIGHT / 2 - Constants.FONT_SIZE)        
            Utility.draw_center_text(self, "press SPACE or CLICK to begin!", Colors.TEXT_COLOR, Constants.SCREEN_HEIGHT - Constants.FONT_SIZE - 50)

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
            self.surface.fill(Colors.BACKGROUND_COLOR) # blank out screen to allow refresh

            # create ALICE_BLUE border
            for screen_border in self.border_rects:
                pygame.draw.rect(self.surface, Colors.ALICE_BLUE, screen_border)

            # get mouse info
            race_mouse_position = pygame.mouse.get_pos()
            self.surface.blit(self.mouse_pointer, race_mouse_position)

            # buttons!
            Utility.draw_center_text(self, "Select your race", Colors.TEXT_COLOR, text_height)
            goblin_button_rect = Utility.get_rect_with_center_text(self, "Goblin", self.font, Constants.MENU_FIRST_BUTTON, Constants.SCREEN_WIDTH)
            goblin_button = GameButton(goblin_button_rect, "Goblin", self.font, base_color="White", hovering_color="Green")      
            goblin_button.change_color(race_mouse_position)
            goblin_button.update(self.surface)

            elf_button_rect = Utility.get_rect_with_center_text(self, "Elf", self.font, Constants.MENU_FIRST_BUTTON + (Constants.MENU_SPACING * 1), Constants.SCREEN_WIDTH)
            elf_button = GameButton(elf_button_rect, text_input="Elf", font=self.font, base_color="White", hovering_color="Green")
            elf_button.change_color(race_mouse_position)
            elf_button.update(self.surface)

            human_button_rect = Utility.get_rect_with_center_text(self, "Human", self.font, Constants.MENU_FIRST_BUTTON + (Constants.MENU_SPACING * 2), Constants.SCREEN_WIDTH)
            human_button = GameButton(human_button_rect, text_input="Human", font=self.font, base_color="White", hovering_color="Green")
            human_button.change_color(race_mouse_position)
            human_button.update(self.surface)

            fae_button_rect = Utility.get_rect_with_center_text(self, "Fae", self.font, Constants.MENU_FIRST_BUTTON + (Constants.MENU_SPACING * 3), Constants.SCREEN_WIDTH)
            fae_button = GameButton(fae_button_rect, text_input="Fae", font=self.font, base_color="White", hovering_color="Green")
            fae_button.change_color(race_mouse_position)
            fae_button.update(self.surface)

            dwarf_button_rect = Utility.get_rect_with_center_text(self, "Dwarf", self.font, Constants.MENU_FIRST_BUTTON + (Constants.MENU_SPACING * 4), Constants.SCREEN_WIDTH)
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
            self.surface.fill(Colors.BACKGROUND_COLOR) # blank out screen to allow refresh

            # create ALICE_BLUE border
            for screen_border in self.border_rects:
                pygame.draw.rect(self.surface, Colors.PLUM, screen_border)

            race_mouse_position = pygame.mouse.get_pos()
            self.surface.blit(self.mouse_pointer, race_mouse_position)

            race_button_rect = Utility.get_rect_with_center_text(self, "Choose Race", self.font, Constants.MENU_FIRST_BUTTON, Constants.SCREEN_WIDTH)
            race_button = GameButton(race_button_rect, text_input="Choose Race", font=self.font, base_color="White", hovering_color="Green")
            race_button.change_color(race_mouse_position)
            race_button.update(self.surface)

            quit_button_rect = Utility.get_rect_with_center_text(self, "Quit", self.font, Constants.MENU_FIRST_BUTTON + (Constants.MENU_SPACING * 1), Constants.SCREEN_WIDTH)
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
        main_game_running = True 
        pygame.display.set_caption(self.main_caption)

        clock = pygame.time.Clock()
        print(f"Started clock: {clock}")

        # water
        water_rects = []
        for _ in range(260):
            water_rect = pygame.Rect(random.randint(0, Constants.SCREEN_WIDTH), random.randint(0, Constants.SCREEN_HEIGHT), random.randint(0, 50), random.randint(0, 50))
            water_rects.append(water_rect)

        # force initialiation of side panel
        initial_unit_created = False
        while main_game_running:
            # slow things down
            clock.tick(60)

            # blank out screen so we can redraw it
            self.surface.fill(Colors.BACKGROUND_COLOR) 

            # create initial unit
            unit = Utility.create_unit(self, "super", self.player.selected_race.hero_character)

            # create random obstacles
            for water_tile in water_rects:
                pygame.draw.rect(self.surface, Colors.AQUA, water_tile)

            # mouse position
            pos = pygame.mouse.get_pos()
            print(pos)

            #  side panel
            side_panel_list, unit_list = Utility.create_side_panel(self, Constants.SIDE_PANEL_TEXT_SIZE)

            # add pointer
            self.surface.blit(self.mouse_pointer, pos)

            # check for highlighting unit buttons
            for unit in unit_list:
                if unit["unit_rect"].collidepoint(pos):
                    Utility.unit_button_highlighted(self, unit, Constants.SIDE_PANEL_TEXT_SIZE)    

            # create border last to cover anything up
            for screen_border in self.border_rects:
                pygame.draw.rect(self.surface, Colors.SALMON, screen_border)

            # continuous key movement (fast)
            key = pygame.key.get_pressed()            
            if key[pygame.K_a] or key[pygame.K_LEFT] == True:
                for army_unit in self.player.army:
                    Utility.move_unit(self, army_unit['unit_rect'], -5, 0, self.player.selected_race.main_color)
                    if army_unit['unit_rect'].collidelist(water_rects) != -1:
                        Utility.move_unit(self, army_unit['unit_rect'], 5, 0, self.player.selected_race.main_color)
            elif key[pygame.K_d] or key[pygame.K_RIGHT] == True:
                for army_unit in self.player.army:
                    Utility.move_unit(self, army_unit['unit_rect'], 5, 0, self.player.selected_race.main_color)
                    if army_unit['unit_rect'].collidelist(water_rects) != -1:
                        Utility.move_unit(self, army_unit['unit_rect'], -5, 0, self.player.selected_race.main_color)
            elif key[pygame.K_w] or key[pygame.K_UP] == True:
                for army_unit in self.player.army:
                    Utility.move_unit(self, army_unit['unit_rect'], 0, -5, self.player.selected_race.main_color)
                    if army_unit['unit_rect'].collidelist(water_rects) != -1:
                        Utility.move_unit(self, army_unit['unit_rect'], 0, 5, self.player.selected_race.main_color)
            elif key[pygame.K_s] or key[pygame.K_DOWN] == True:
                for army_unit in self.player.army:          
                    Utility.move_unit(self, army_unit['unit_rect'], 0, 5, self.player.selected_race.main_color)
                    if army_unit['unit_rect'].collidelist(water_rects) != -1:
                        Utility.move_unit(self, army_unit['unit_rect'], 0, -5, self.player.selected_race.main_color)
            
            # continuous mouse movement (fast)
            mouse = pygame.mouse.get_pressed()            
            if mouse[0] == True:
                # print(f"left mouse: {pos}")
                # scan troops for select      
                for unit in self.player.army:
                    for newrect in unit["unit_rect"]:
                        if newrect.collidepoint(pos):
                            Utility.select_unit(self, unit)

            elif mouse[1] == True:
                pass
                # print(f"middle mouse: {pos}")
            elif mouse[2] == True:
                pass
                # print(f"right mouse: {pos}")

            # event handling, gets all event from the event queue.  These events are only fired once so good for menus or single movement but not for continuous
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(f"mouse down: {event}")
                    any_mouse_clicked = False
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
            pygame.display.flip()

    def main(self):     
        first_opened = True
        while self.running:
            self.surface.fill(Colors.BACKGROUND_COLOR) # blank out screen to allow refresh
            if first_opened:
                first_opened = self.first_open_loop()
            elif (self.player.selected_race is None):
                self.race_select_loop()
            else:   
                self.main_game_loop()
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    rts().main()
