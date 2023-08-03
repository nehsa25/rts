# import the pygame module, so you can use it
from pprint import pprint
import pygame

# our stuff
from race import Race
from elf import Elf
from goblin import Goblin
from human import Human

# constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TEXT_COLOR = (255, 255, 255)
GAME_NAME = "Super duper awesome RTS game"
FONT_SIZE = 20

# initialize the pygame module
pygame.init()
logo = pygame.image.load("logo.png")
pygame.display.set_icon(logo)
pygame.display.set_caption(GAME_NAME)
font = pygame.font.SysFont("arialblack", FONT_SIZE)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_center_text(text, font, text_color, y):
    text = font.render(text, True, text_color)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, y))
    screen.blit(text, text_rect)

def main():     
    races = Race._member_names_
    selected_race = "goblin"

    # main loop
    running = True
    game_paused = True
    while running:
        screen.fill((43.5, 57.3, 44)) # blank out screen to allow refresh
        if (game_paused):
            draw_center_text(f"Welcome to {GAME_NAME}!", font, TEXT_COLOR, SCREEN_HEIGHT / 2 - FONT_SIZE)        
            draw_center_text("press SPACE to continue", font, TEXT_COLOR, SCREEN_HEIGHT / 2 + FONT_SIZE)
        else:
            base_height = SCREEN_HEIGHT / 2 - FONT_SIZE # true center height
            text_height = base_height / 2
            draw_center_text("Who do you wish to play as?", font, TEXT_COLOR, text_height)  
            for race in races:
                text_height += FONT_SIZE * 2
                if race.lower() == selected_race:
                    draw_center_text(race.upper(), font, TEXT_COLOR, text_height)  
                else:
                   draw_center_text(race.lower(), font, TEXT_COLOR, text_height)   
   
        if selected_race.lower() == "human":
            selected_race_obj = Human()
        elif selected_race.lower() == "goblin":
            selected_race_obj = Goblin()
        elif selected_race.lower() == "elf":
            selected_race_obj = Elf()

        # draw some guys
        pygame.draw.rect(screen, selected_race_obj.color, selected_race_obj.rect)
        # pygame.draw.rect(screen, elf_archer.color, elf_archer.rect)
        # pygame.draw.rect(screen, goblin_pillager.color, goblin_pillager.rect)

        key = pygame.key.get_pressed()
        if key[pygame.K_a] == True:
            selected_rect = selected_rect.move_ip(-1, 0)
        elif key[pygame.K_d] == True:
            selected_rect = selected_rect.move_ip(1, 0)
        elif key[pygame.K_w] == True:
            selected_rect = selected_rect.move_ip(0, -1)
        elif key[pygame.K_s] == True:
            selected_rect = selected_rect.move_ip(0, 1)

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_paused = False
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

        pygame.display.update()
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
