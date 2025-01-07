import pygame
import sys

# Import function from other .py files
from keys import *
from map_display import *
from object_class_map_ressources import *
from animation_managment import *
from moving import *
from game_manager import *

# Initialize Pygame
pygame.init()

# create and init the game_manager which contains every important aspect of the game current informations
game_manager = init_game_manager()


# Main loop

while game_manager.running:
    
    game_manager.clock.tick(60) #FPS
    
    game_manager.events = pygame.event.get()
    # get keys input from player
    manage_keys_input(game_manager)
    print_map(game_manager)
    moving_managment(game_manager)
    animation_managment(game_manager)
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()