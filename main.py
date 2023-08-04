# import the pygame module, so you can use it
import pygame, sys

# our stuff
from race import Race
from elf import Elf
from goblin import Goblin
from human import Human
from gamebutton import GameButton

class rts:
    # constants
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    TEXT_COLOR = (255, 255, 255)
    GAME_NAME = "Super duper awesome RTS game"
    FONT_SIZE = 20
    BACKGROUND_COLOR = (43.5, 57.3, 44)

    # initialize the pygame module
    pygame.init()
    logo = pygame.image.load("logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption(GAME_NAME)
    font = pygame.font.SysFont("arialblack", FONT_SIZE)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    running = True # kill everything

    # game data
    selected_race = None

    def draw_center_text(self, text, font, text_color, y):
        text = font.render(text, True, text_color)
        text_rect = text.get_rect(center=(self.SCREEN_WIDTH / 2, y))
        self.screen.blit(text, text_rect)    

    def get_center_text(self, text, font, y, total_width):
        text = font.render(text, True, 'black')
        return text.get_rect(center=(total_width / 2, y))
        
    def first_open(self):
        first_open_running = True 
        pygame.display.set_caption("Welcome!")

        while first_open_running:
            self.screen.fill(self.BACKGROUND_COLOR) # blank out screen to allow refresh

            self.draw_center_text(f"Welcome to {self.GAME_NAME}!", self.font, self.TEXT_COLOR, self.SCREEN_HEIGHT / 2 - self.FONT_SIZE)        
            self.draw_center_text("press SPACE to begin!", self.font, self.TEXT_COLOR, self.SCREEN_HEIGHT - self.FONT_SIZE - 50)

            # pygame.draw.rect(screen, elf_archer.color, elf_archer.rect)
            # pygame.draw.rect(screen, goblin_pillager.color, goblin_pillager.rect)

            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        first_open_running = False
                        break
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    first_open_running = False
                    self.running = False
                    break

            print("first_open loop...")
            pygame.display.update()

        return False

    def race_select(self):
        race_select_running = True 
        pygame.display.set_caption("Select your race")
        base_height = self.SCREEN_HEIGHT / 2 - self.FONT_SIZE # true center height
        text_height = base_height / 2

        while race_select_running:
            self.screen.fill(self.BACKGROUND_COLOR) # blank out screen to allow refresh
            race_mouse_position = pygame.mouse.get_pos()

            self.draw_center_text("Select your race", self.font, self.TEXT_COLOR, text_height)
            goblin_button_rect = self.get_center_text("Goblin", self.font, 260, self.SCREEN_WIDTH)
            goblin_button = GameButton(goblin_button_rect, "Goblin", self.font, base_color="White", hovering_color="Green")      
            goblin_button.change_color(race_mouse_position)
            goblin_button.update(self.screen)

            elf_button_rect = self.get_center_text("Elf", self.font, 300, self.SCREEN_WIDTH)
            elf_button = GameButton(elf_button_rect, text_input="Elf", font=self.font, base_color="White", hovering_color="Green")
            elf_button.change_color(race_mouse_position)
            elf_button.update(self.screen)

            human_button_rect = self.get_center_text("Human", self.font, 340, self.SCREEN_WIDTH)
            human_button = GameButton(human_button_rect, text_input="Human", font=self.font, base_color="White", hovering_color="Green")
            human_button.change_color(race_mouse_position)
            human_button.update(self.screen)

            # event loop for option selection screen
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if goblin_button.check_position(race_mouse_position):
                        print("Goblin selected")
                        self.selected_race = Goblin()
                        race_select_running = False
                    if elf_button.check_position(race_mouse_position):
                        print("Elf selected")
                        self.selected_race = Elf()
                        race_select_running = False
                    if human_button.check_position(race_mouse_position):
                        print("Human selected")
                        self.selected_race = Human()
                        race_select_running = False               
                if event.type == pygame.QUIT:
                    race_select_running = False
                    self.running = False
            
            print("Updating options loop")
            pygame.display.update()

    def move_unit(self, rect, x, y):
        # create a "screen same size and move it"
        rect.move_ip(x, y)

    def main_game(self):
        main_game_running = True 
        pygame.display.set_caption("")
        while main_game_running:
            self.screen.fill(self.BACKGROUND_COLOR) # blank out screen to allow refresh
            pygame.draw.rect(self.screen, self.selected_race.color, self.selected_race.rect)
            # pygame.draw.rect(screen, elf_archer.color, elf_archer.rect)
            # pygame.draw.rect(screen, goblin_pillager.color, goblin_pillager.rect)

            key = pygame.key.get_pressed()
            if key[pygame.K_a] == True:
                self.move_unit(self.selected_race.rect, -1, 0)
            elif key[pygame.K_d] == True:
                self.move_unit(self.selected_race.rect, 1, 0)
            elif key[pygame.K_w] == True:
                self.move_unit(self.selected_race.rect, 0, -1)
            elif key[pygame.K_s] == True:
                self.move_unit(self.selected_race.rect, 0, 1)

            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    main_game_running = False
                    self.running = False

            print("Main game loop...")
            pygame.display.update()

    def main(self):     
        first_opened = True
        while self.running:
            self.screen.fill(self.BACKGROUND_COLOR) # blank out screen to allow refresh
            if first_opened:
                first_opened = self.first_open()
            elif (self.selected_race is None):
                self.race_select()
            else:   
                self.main_game()
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    rts().main()
