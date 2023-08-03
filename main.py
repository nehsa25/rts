# import the pygame module, so you can use it
from pprint import pprint
import pygame
from archer import Archer
from elf import Elf
from goblin import Goblin

# define a main function
def main():
     
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Super duper awesome RTS game")
     
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((640,480))
     
    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:
        
        arch = Archer()

        elf = Elf()
        elf_archer = elf.ElvenArcher()

        goblin = Goblin()
        goblin_pillager = goblin.Pillager()
        
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
