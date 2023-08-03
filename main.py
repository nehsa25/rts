# import the pygame module, so you can use it
from pprint import pprint
import pygame
from elf import Elf
from goblin import Goblin
from human import Human

# define a main function
def main():     
    # initialize the pygame module
    pygame.init()
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    # load and set the logo
    logo = pygame.image.load("logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Super duper awesome RTS game")
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
     
    # create some objects
    human = Human()
    human_archer = human.Archer()

    elf = Elf()
    elf_archer = elf.Archer()

    goblin = Goblin()
    goblin_pillager = goblin.Pillager()

    # main loop
    running = True
    while running:
        screen.fill((43.5, 57.3, 44)) # blank out screen to allow refresh
        selected_rect = human_archer.rect

        # draw some guys
        pygame.draw.rect(screen, human_archer.color, human_archer.rect)
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
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

        pygame.display.update()
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
