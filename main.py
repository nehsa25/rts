# import the pygame module, so you can use it
import random
import pygame, sys

# our stuff
from race import Race
from elf import Elf
from goblin import Goblin
from human import Human
from gamebutton import GameButton

class rts:
    # initialize the pygame module
    pygame.init()

    # constants
    BLACK = (0, 0, 0)
    BLUE = (43.5, 57.3, 44)
    WHITE = (255, 255, 255)
    MAROON = (128, 0, 0)
    YELLOW = (98, 67, 41)
    ALICE_BLUE = (240,248,255)
    AQUA = (0,255,255)
    MOUSE_POINTER_COLOR = WHITE
    MOUSE_POINTER_SIZE = 5
    BACKGROUND_COLOR = BLUE
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    TEXT_COLOR = WHITE
    GAME_NAME = "Super duper awesome RTS game"
    FONT_SIZE = 20
    BORDER_SIZE = 10

    # screen border
    border_rects = []
    top_border_rect = pygame.Rect(0, 0, SCREEN_WIDTH, BORDER_SIZE)
    border_rects.append(top_border_rect)

    bottom_border_rect = pygame.Rect(0, SCREEN_HEIGHT-BORDER_SIZE, SCREEN_WIDTH, BORDER_SIZE)
    border_rects.append(bottom_border_rect)

    left_border_rect = pygame.Rect(0, 0, BORDER_SIZE, SCREEN_WIDTH)
    border_rects.append(left_border_rect)

    right_border_rect = pygame.Rect(SCREEN_WIDTH - BORDER_SIZE, 0, BORDER_SIZE, SCREEN_HEIGHT)
    border_rects.append(right_border_rect)

    # mouse
    mouse_pointer = pygame.Surface((MOUSE_POINTER_SIZE, MOUSE_POINTER_SIZE))
    mouse_pointer.fill(MOUSE_POINTER_COLOR)
    mouse_pointer_mask = pygame.mask.from_surface(mouse_pointer)
    pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

    #logo
    logo = pygame.image.load("logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption(GAME_NAME)    
    font = pygame.font.SysFont("arialblack", FONT_SIZE)
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    running = True # kill everything

    # game data
    main_unit = None
    any_mouse_clicked = False

    def draw_center_text(self, text, font, text_color, y):
        text = font.render(text, True, text_color)
        text_rect = text.get_rect(center=(self.SCREEN_WIDTH / 2, y))
        self.surface.blit(text, text_rect)    

    def get_center_text(self, text, font, y, total_width):
        text = font.render(text, True, 'black')
        return text.get_rect(center=(total_width / 2, y))
        
    def first_open_loop(self):
        first_open_running = True 
        pygame.display.set_caption("Welcome!")

        while first_open_running:
            self.surface.fill(self.BACKGROUND_COLOR) # blank out screen to allow refresh

            # create yellow border
            for screen_border in self.border_rects:
                pygame.draw.rect(self.surface, self.YELLOW, screen_border)

            race_mouse_position = pygame.mouse.get_pos()
            self.surface.blit(self.mouse_pointer, race_mouse_position)

            self.draw_center_text(f"Welcome to {self.GAME_NAME}!", self.font, self.TEXT_COLOR, self.SCREEN_HEIGHT / 2 - self.FONT_SIZE)        
            self.draw_center_text("press SPACE to begin!", self.font, self.TEXT_COLOR, self.SCREEN_HEIGHT - self.FONT_SIZE - 50)

            # pygame.draw.rect(screen, elf_archer.color, elf_archer.rect)
            # pygame.draw.rect(screen, goblin_pillager.color, goblin_pillager.rect)

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
        base_height = self.SCREEN_HEIGHT / 2 - self.FONT_SIZE # true center height
        text_height = base_height / 2

        while race_select_running:
            self.surface.fill(self.BACKGROUND_COLOR) # blank out screen to allow refresh

            # create teal border
            for screen_border in self.border_rects:
                pygame.draw.rect(self.surface, self.ALICE_BLUE, screen_border)

            # get mouse info
            race_mouse_position = pygame.mouse.get_pos()
            self.surface.blit(self.mouse_pointer, race_mouse_position)

            self.draw_center_text("Select your race", self.font, self.TEXT_COLOR, text_height)
            goblin_button_rect = self.get_center_text("Goblin", self.font, 260, self.SCREEN_WIDTH)
            goblin_button = GameButton(goblin_button_rect, "Goblin", self.font, base_color="White", hovering_color="Green")      
            goblin_button.change_color(race_mouse_position)
            goblin_button.update(self.surface)

            elf_button_rect = self.get_center_text("Elf", self.font, 300, self.SCREEN_WIDTH)
            elf_button = GameButton(elf_button_rect, text_input="Elf", font=self.font, base_color="White", hovering_color="Green")
            elf_button.change_color(race_mouse_position)
            elf_button.update(self.surface)

            human_button_rect = self.get_center_text("Human", self.font, 340, self.SCREEN_WIDTH)
            human_button = GameButton(human_button_rect, text_input="Human", font=self.font, base_color="White", hovering_color="Green")
            human_button.change_color(race_mouse_position)
            human_button.update(self.surface)

            # event loop for option selection screen
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if goblin_button.check_position(race_mouse_position):
                        print("Goblin selected")
                        self.main_unit = Goblin()
                        race_select_running = False
                    if elf_button.check_position(race_mouse_position):
                        print("Elf selected")
                        self.main_unit = Elf()
                        race_select_running = False
                    if human_button.check_position(race_mouse_position):
                        print("Human selected")
                        self.main_unit = Human()
                        race_select_running = False               
                if event.type == pygame.QUIT:
                    race_select_running = False
                    self.running = False
            
            # print("Updating options loop")
            pygame.display.flip()

    def create_unit_with_border(self, rect, main_color):
        unit = []
        unit.append(rect)
        
        border_width = 2
        pygame.draw.rect(self.surface, main_color, rect) # this is what actually causes the rect to show up on screen

        # left
        left_border_color = (random.choice(range(256)), random.choice(range(256)), random.choice(range(256)))
        left_border_rect = pygame.Rect((rect.x-border_width, rect.y, border_width, rect.height))
        pygame.draw.rect(self.surface, left_border_color, left_border_rect) # this is what actually causes the rect to show up on screen
        unit.append(left_border_rect)

        # bottom
        bottom_border_color = (random.choice(range(256)), random.choice(range(256)), random.choice(range(256)))
        bottom_border_rect = pygame.Rect((rect.x, rect.y + rect.height, rect.width, border_width))
        pygame.draw.rect(self.surface, bottom_border_color, bottom_border_rect) # this is what actually causes the rect to show up on screen
        unit.append(bottom_border_rect)

        # right
        right_border_color = (random.choice(range(256)), random.choice(range(256)), random.choice(range(256)))
        right_border_rect = pygame.Rect((rect.x + rect.width, rect.y, border_width, rect.height))
        pygame.draw.rect(self.surface, right_border_color, right_border_rect) # this is what actually causes the rect to show up on screen
        unit.append(right_border_rect)

        # top
        top_border_color = (random.choice(range(256)), random.choice(range(256)), random.choice(range(256)))
        top_border_rect = pygame.Rect((rect.x, rect.y - border_width, rect.width, border_width))
        pygame.draw.rect(self.surface, top_border_color, top_border_rect) # this is what actually causes the rect to show up on screen
        unit.append(top_border_rect)

        # print(unit)
        return unit
        pass
    
    def create_unit(self, rect, main_color):
        return self.create_unit_with_border(rect, main_color)   

    def move_unit(self, rect, x, y, main_color):
        rects = self.create_unit_with_border(rect, main_color)        
        for edge in rects:
            edge.move_ip(x, y)

    def main_game_loop(self):
        main_game_running = True 
        pygame.display.set_caption("")

        # water
        water_rects = []
        for _ in range(260):
            water_rect = pygame.Rect(random.randint(0, self.SCREEN_WIDTH), random.randint(0, self.SCREEN_HEIGHT), random.randint(0, 50), random.randint(0, 50))
            water_rects.append(water_rect)

        clock = pygame.time.Clock()
        print(f"Started: {clock}")
        while main_game_running:
            # slow things down
            clock.tick(60)

            # blank out screen so we can redraw it
            self.surface.fill(self.BACKGROUND_COLOR) 

            # mouse position
            pos = pygame.mouse.get_pos()
            self.surface.blit(self.mouse_pointer, pos)

            # create initial unit
            unit = self.create_unit(self.main_unit.rect, self.main_unit.color)

            # create random obstacles
            for water_tile in water_rects:
                pygame.draw.rect(self.surface, self.AQUA, water_tile)

            # create border last to cover anything up
            for screen_border in self.border_rects:
                pygame.draw.rect(self.surface, self.BLACK, screen_border)

            # continuous key movement (fast)
            key = pygame.key.get_pressed()
            if key[pygame.K_a] == True:
                print(self.main_unit.rect.collidelist(water_rects)) 
                self.move_unit(self.main_unit.rect, -5, 0, self.main_unit.color)
                if self.main_unit.rect.collidelist(water_rects) != -1:
                    self.move_unit(self.main_unit.rect, 5, 0, self.main_unit.color)
            elif key[pygame.K_d] == True:
                print(self.main_unit.rect.collidelist(water_rects)) 
                self.move_unit(self.main_unit.rect, 5, 0, self.main_unit.color)
                if self.main_unit.rect.collidelist(water_rects) != -1:
                    self.move_unit(self.main_unit.rect, -5, 0, self.main_unit.color)
            elif key[pygame.K_w] == True:
                print(self.main_unit.rect.collidelist(water_rects))
                self.move_unit(self.main_unit.rect, 0, -5, self.main_unit.color)
                if self.main_unit.rect.collidelist(water_rects) != -1:
                    self.move_unit(self.main_unit.rect, 0, 5, self.main_unit.color)
            elif key[pygame.K_s] == True:
                print(self.main_unit.rect.collidelist(water_rects))                
                self.move_unit(self.main_unit.rect, 0, 5, self.main_unit.color)
                if self.main_unit.rect.collidelist(water_rects) != -1:
                    self.move_unit(self.main_unit.rect, 0, -5, self.main_unit.color)
            
            # continuous mouse movement (fast)
            mouse = pygame.mouse.get_pressed()            
            if mouse[0] == True:
                print(f"left mouse: {pos}")
            elif mouse[1] == True:
                print(f"middle mouse: {pos}")
            elif mouse[2] == True:
                print(f"right mouse: {pos}")

            # event handling, gets all event from the event queue.  These events are only fired once so good for menus or single movement but not for continuous
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(f"mouse down: {event}")
                    any_mouse_clicked = False
                if event.type == pygame.MOUSEBUTTONUP:
                    print(f"mouse up: {event}")
                # 
                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_a:
                #         self.move_unit(self.selected_race.rect, -1, 0, self.selected_race.color)
                #     elif event.key == pygame.K_d:
                #         self.move_unit(self.selected_race.rect, 1, 0, self.selected_race.color)
                #     elif event.key == pygame.K_w:
                #         self.move_unit(self.selected_race.rect, 0, -1, self.selected_race.color)
                #     elif event.key == pygame.K_s:
                #         self.move_unit(self.selected_race.rect, 0, 1, self.selected_race.color)
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    main_game_running = False
                    self.running = False

            # print("Main game loop...")
            pygame.display.flip()

    def main(self):     
        first_opened = True
        while self.running:
            self.surface.fill(self.BACKGROUND_COLOR) # blank out screen to allow refresh
            if first_opened:
                first_opened = self.first_open_loop()
            elif (self.main_unit is None):
                self.race_select_loop()
            else:   
                self.main_game_loop()
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    rts().main()
