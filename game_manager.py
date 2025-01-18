import pygame

from user_interactions import *
from map_display_chunk import *
from player import *
from chunk_map import *

class class_game_manager:
    def __init__(self):
        
        # pygame environment
        self.screen = None
        self.clock = None
        self.font = None
        self.events = None
        
        # map data
        self.map_size_x = 1920
        self.map_size_y = 1080
        self.map_view = None
        self.larger_map_view = None
        self.map_speed = 6
        self.map_decay = 0
        self.chunks = None
        self.disp_chunks = None
        self.chunk_size_x = 500
        self.chunk_size_y = 500
        self.nb_chunk_x = 1
        self.nb_chunk_y = 1
        self.minimap = None
        self.minimap_view = None
        
        # sprites and object lists
        self.map_png_list = None
        self.generated_map_obj = None
        self.generated_map_bg = None
        self.animations_list = None
        
        # individual sprites
        self.interface = None

        # playable characters
        self.player = None

        #  UI managment
        self.user_interactions = None
        self.minimap_clicked = False
        
        # bools
        self.running = True


# function to be called before main, initializing all game important aspect within

def init_game_manager():
    #set up the game manager to return
    game_manager = class_game_manager()

    # Set up the display
    game_manager.screen = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0])
    pygame.display.set_caption("My Pygame Window")


    # Set up clock
    game_manager.clock = pygame.time.Clock()

    # setup fonts
    game_manager.font = pygame.font.SysFont("Comic Sans MS", 30, bold=False, italic=False)

    # chunk attribute for loading sprites
    game_manager.chunk_size_x = 500
    game_manager.chunk_size_y = 500
    game_manager.nb_chunk_x = 20
    game_manager.nb_chunk_y = 20

    # set up images in a list
    game_manager.map_png_list = []
    #grass fill 0
    game_manager.map_png_list.append(load_sprites_size(r"C:\Users\simon\Desktop\personal_project\RPG_basics\sprites\map_village\theme1\1 Tiles\grass", game_manager.chunk_size_x, game_manager.chunk_size_y))
    #grass details 1
    game_manager.map_png_list.append(load_sprites(r"C:\Users\simon\Desktop\personal_project\RPG_basics\sprites\map_village\theme1\2 Objects\5 Grass", 1, 1))
    # shadow and tree 2
    game_manager.map_png_list.append(load_sprites(r"C:\Users\simon\Desktop\personal_project\RPG_basics\sprites\map_village\theme1\2 Objects\tree_shadow", 1.3, 1.3))
    # bushes 3
    game_manager.map_png_list.append(load_sprites(r"C:\Users\simon\Desktop\personal_project\RPG_basics\sprites\map_village\theme1\2 Objects\9 Bush", 1.3, 1.3))
    # stones 4
    game_manager.map_png_list.append(load_sprites(r"C:\Users\simon\Desktop\personal_project\RPG_basics\sprites\map_village\theme1\2 Objects\4 Stone", 2, 2))
    # logs 5
    game_manager.map_png_list.append(load_sprites(r"C:\Users\simon\Desktop\personal_project\RPG_basics\sprites\map_village\theme1\2 Objects\logs", 1, 1))
    # interface loading
    game_manager.interface = load_sprites(r"C:\Users\simon\Desktop\personal_project\RPG_basics\sprites\UI\interface", 1, 1)

    game_manager.map_size_x = game_manager.chunk_size_x * game_manager.nb_chunk_x
    game_manager.map_size_y = game_manager.chunk_size_y * game_manager.nb_chunk_y
    game_manager.larger_map_view = pygame.Rect(-400, -400, 1920 + 800, 1080 + 800)
    game_manager.map_view = pygame.Rect(0, 0, 1920, 1080)
    game_manager.map_view.width = game_manager.screen.get_width()
    game_manager.map_view.height = game_manager.screen.get_height()

    # Generate object positions once and store them in a list
    game_manager.generated_map_obj = []
    game_manager.generated_map_bg = []
    # game_manager.generated_map_bg.append(generate_grass_positions(game_manager.map_png_list[0], x, y)) # grass fill
    # game_manager.generated_map_bg.append(generate_flower_positions(game_manager.map_png_list[1], flower_count, x, y)) # grass details flowers
    # game_manager.generated_map_obj.append(generate_bush_positions(game_manager.map_png_list[3], flower_count // 2, x, y)) # bushes
    # game_manager.generated_map_obj.append(generate_tree_positions(game_manager.map_png_list[2], flower_count // 6, x, y)) # tree in map
    # game_manager.generated_map_obj.append(generate_stones_positions(game_manager.map_png_list[4], flower_count // 10, x, y)) # stones in map
    # game_manager.generated_map_obj.append(generate_logs_positions(game_manager.map_png_list[5], flower_count // 50, x , y)) # logs in map


    game_manager.chunks = generate_chunks(game_manager.nb_chunk_x, game_manager.nb_chunk_y, game_manager, game_manager.chunk_size_x, game_manager.chunk_size_y)
    game_manager.minimap = pygame.Rect(game_manager.screen.get_width() - 300, game_manager.screen.get_height() - 240, 290, 230)
    
    # List of animations
    game_manager.animations_list = []

    # List of events
    game_manager.events = []

    #init player
    game_manager.player = init_warrior(game_manager.screen)

    #init user_interaction
    game_manager.user_interactions = user_interaction()
    game_manager.user_interactions.selected_obj.append(game_manager.player)
    
    return (game_manager)