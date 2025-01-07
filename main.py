import pygame
import sys

# Import function from other .py files
from keys import *
from map_display import *
from object_class_map_ressources import *
from player import *
from animation_managment import *
from moving import *
from user_interactions import *

# Initialize Pygame
pygame.init()


# Set up the display
screen = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0])
pygame.display.set_caption("My Pygame Window")


# Set up clock
clock = pygame.time.Clock()

# setup fonts
font = pygame.font.SysFont("Comic Sans MS", 30, bold=False, italic=False)

# set up images in a list
map_png_list = []
#grass fill 0
map_png_list.append(load_sprites(r"C:\Users\simon\Desktop\personal_project\RPG_basics\sprites\map_village\theme1\1 Tiles\grass", 10, 10))
#grass details 1
map_png_list.append(load_sprites(r"C:\Users\simon\Desktop\personal_project\RPG_basics\sprites\map_village\theme1\2 Objects\5 Grass", 1, 1))
# shadow and tree 2
map_png_list.append(load_sprites(r"C:\Users\simon\Desktop\personal_project\RPG_basics\sprites\map_village\theme1\2 Objects\tree_shadow", 1.3, 1.3))
# bushes 3
map_png_list.append(load_sprites(r"C:\Users\simon\Desktop\personal_project\RPG_basics\sprites\map_village\theme1\2 Objects\9 Bush", 1.3, 1.3))
# stones 4
map_png_list.append(load_sprites(r"C:\Users\simon\Desktop\personal_project\RPG_basics\sprites\map_village\theme1\2 Objects\4 Stone", 2, 2))
# logs 5
map_png_list.append(load_sprites(r"C:\Users\simon\Desktop\personal_project\RPG_basics\sprites\map_village\theme1\2 Objects\logs", 1, 1))
# interface loading
interface = load_sprites(r"C:\Users\simon\Desktop\personal_project\RPG_basics\sprites\UI\interface", 1, 1)

# Calculate the number of flowers based on the screen size
screen_area = screen.get_width() * screen.get_height()
flower_count = screen_area // 5000  # Adjust the divisor to control density

# Generate object positions once and store them in a list
generated_map_obj = []
generated_map_bg = []
generated_map_bg.append(generate_grass_positions(screen, map_png_list[0])) # grass fill
generated_map_bg.append(generate_flower_positions(screen, map_png_list[1], flower_count)) # grass details flowers
generated_map_obj.append(generate_bush_positions(screen, map_png_list[3], flower_count // 2)) # bushes
generated_map_obj.append(generate_tree_positions(screen, map_png_list[2], flower_count // 6)) # tree in map
generated_map_obj.append(generate_stones_positions(screen, map_png_list[4], flower_count // 10)) # stones in map
generated_map_obj.append(generate_logs_positions(screen, map_png_list[5], flower_count // 50)) # logs in map


# List of animations
animations_list = []

# List of events
events = []

#init player
player = init_warrior(screen)

#init user_interaction
user_interactions = user_interaction()
user_interactions.selected_obj.append(player)

# Main loop
running = [True]
while running[0]:
    
    clock.tick(60) #FPS
    
    events = pygame.event.get()
    # get keys input from player
    manage_keys_input(clock, running, player, animations_list, user_interactions, events, generated_map_obj)
    print_map(screen, generated_map_bg, generated_map_obj, player, animations_list, user_interactions, interface, clock, font)
    moving_managment(clock, player, generated_map_obj)
    animation_managment(clock, player, animations_list)
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()