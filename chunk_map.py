import pygame

from map_display_chunk import *


class Chunk:
    
    def __init__(self):
        # chunk position arguments
        self.nb_x = 0
        self.nb_y = 0
        self.size_x = 0
        self.size_y = 0
        
        # chunk fill arguments
        self.bg_fill = None
        self.details = None
        self.obj = None
        self.animations = None
        


def generate_chunks(max_x, max_y, game_manager, size_x_chunk = 500, size_y_chunk = 500):
    
    n_y = 0
    n_x = 0
    chunk_area = size_x_chunk * size_y_chunk
    ratio_details = chunk_area // 10000
    chunk_list = []
    
    while n_y != max_y:
        new_chunk = Chunk()
        new_chunk.size_x = size_x_chunk
        new_chunk.size_y = size_y_chunk

        new_chunk.bg_fill = []
        new_chunk.details = []
        new_chunk.obj = []

        new_chunk.bg_fill.append(generate_grass_positions_chunk(game_manager.map_png_list[0], n_x, n_y, size_x_chunk, size_y_chunk)) # grass fill chunk
        new_chunk.details.append(generate_flower_positions_chunk(game_manager.map_png_list[1], ratio_details, n_x, n_y, size_x_chunk, size_y_chunk)) # chunk details flowers
        new_chunk.obj.append(generate_logs_positions_chunk(game_manager.map_png_list[5], ratio_details // 50, n_x, n_y, size_x_chunk, size_y_chunk)) # logs in chunk
        new_chunk.obj.append(generate_bush_positions_chunk(game_manager.map_png_list[3], ratio_details // 2, n_x, n_y, size_x_chunk, size_y_chunk)) # chunk bushes
        new_chunk.obj.append(generate_tree_positions_chunk(game_manager.map_png_list[2], ratio_details * 3, n_x, n_y, size_x_chunk, size_y_chunk)) # tree in chunk
        new_chunk.obj.append(generate_stones_positions_chunk(game_manager.map_png_list[4], ratio_details // 10, n_x, n_y, size_x_chunk, size_y_chunk)) # stones in chunk

        
        new_chunk.nb_x = n_x
        new_chunk.nb_y = n_y
        n_x += 1
        if n_x >= max_x:
            n_x = 0
            n_y += 1
        chunk_list.append(new_chunk)

    return chunk_list