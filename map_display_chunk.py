import pygame
import os
import random

from object_class_map_ressources import *


# loading sprites from a folder, precising size of the sprite
def load_sprites(folder, size_x, size_y):
    sprites = []
    for filename in os.listdir(folder):
        if filename.endswith('.png'):
            if size_x != 1 or size_y != 1:
                image = pygame.Surface.convert_alpha(pygame.transform.scale_by(pygame.image.load(os.path.join(folder, filename)), (size_x, size_y)))
            else :
                image = pygame.Surface.convert_alpha(pygame.image.load(os.path.join(folder, filename)))
            sprites.append(image)
    return sprites

def load_sprites_size(folder, size_x, size_y):
    sprites = []
    for filename in os.listdir(folder):
        if filename.endswith('.png'):
            image = pygame.Surface.convert_alpha(pygame.transform.scale(pygame.image.load(os.path.join(folder, filename)), (size_x, size_y)))
            sprites.append(image)
    return sprites

# generating grass to fill background
def generate_grass_positions_chunk(sprites, nb_x, nb_y, chunk_size_x = 500, chunk_size_y = 500):
    grass_tiles = []
    x = nb_x * chunk_size_x
    y = nb_y * chunk_size_y
    while y < (nb_y + 1) * chunk_size_y:
        while x < (nb_x + 1) * chunk_size_x:
            sprite = random.choice(sprites)
            grass_tiles.append((sprite, "grass"))
            x += sprite.get_width()
        x = nb_x * chunk_size_x
        y += sprite.get_height()
    return grass_tiles

# generating flowers to fill background randomly
def generate_flower_positions_chunk(sprites, ratio_details, n_x, n_y, chunk_size_x = 500, chunk_size_y = 500):
    flowers = []

    for _ in range(ratio_details):
        sprite = random.choice(sprites)
        x = random.randint(n_x * chunk_size_x, (n_x + 1) * chunk_size_x - sprite.get_width())
        y = random.randint(sprite.get_height() + n_y * chunk_size_y, (n_y + 1) * chunk_size_y - sprite.get_height())
        flower = MapObject(sprite, x, y, 2, "flower")
        flowers.append(flower)
    return flowers


# generating trees and there shadow from y = 0 to screen_height by a ratio, return a list of trees
def generate_tree_positions_chunk(sprites, ratio, n_x, n_y, chunk_size_x = 500, chunk_size_y = 500):
    trees = []
    sprtie_tree = sprites[1]
    y = n_y * chunk_size_y

    while y < chunk_size_y * (n_y + 1) - sprites[1].get_height() * 2:
        sprite = sprites[0]
        x = random.randint(n_x * chunk_size_x, (n_x + 1) * chunk_size_x - sprite.get_width())
        y += random.randint(0, ratio * 2)
        new_tree = MapObject(sprites[1], x, y , 100, "tree")
        new_tree.shadow = sprites[0] #attribute shadow to the tree
        new_tree.shadow_x = x - sprite.get_width() / 6
        new_tree.shadow_y = y - sprite.get_height() / 2
        new_tree.col_hitbox = pygame.Rect(x + sprite.get_width() / 5, y - new_tree.sprite.get_height() / 4, sprite.get_width() / 3, sprite.get_height() / 3)
        new_tree.hitbox = pygame.Rect(x + 10, y - new_tree.sprite.get_height(), new_tree.sprite.get_width() - 20, new_tree.sprite.get_height())
        trees.append(new_tree)
    return trees


#generating bushes randomly
def generate_bush_positions_chunk(sprites, count, n_x, n_y, chunk_size_x = 500, chunk_size_y = 500):
    bushes = []

    for _ in range(count):
        sprite = random.choice(sprites)
        x = random.randint((n_x) * chunk_size_x, (n_x + 1) * chunk_size_x - sprite.get_width())
        y = random.randint(sprite.get_height() + (n_y) * chunk_size_y, (n_y + 1) * chunk_size_y - sprite.get_height())
        new_bush = MapObject(sprite, x, y, 50, "bush")
        new_bush.hitbox = pygame.Rect(x, y - sprite.get_height(), sprite.get_width(), sprite.get_height())
        bushes.append(new_bush)
    return bushes


# generating stones randomly
def generate_stones_positions_chunk(sprites, count, n_x, n_y, chunk_size_x = 500, chunk_size_y = 500):
    stones = []
    for _ in range(count):
        sprite = random.choice(sprites)
        x = random.randint((n_x) * chunk_size_x, (n_x + 1) * chunk_size_x - sprite.get_width())
        y = random.randint(sprite.get_height() + (n_y) * chunk_size_y, (n_y + 1) * chunk_size_y - sprite.get_height())
        new_stone = MapObject(sprite, x, y, 250, "stone")
        new_stone.col_hitbox = pygame.Rect(x, y - new_stone.sprite.get_height() /2.2, sprite.get_width(), sprite.get_height() / 3)
        new_stone.hitbox = pygame.Rect(x, y - new_stone.sprite.get_height(), sprite.get_width(), sprite.get_height())
        stones.append(new_stone)
    return stones


# generating logs randomly
def generate_logs_positions_chunk(sprites, count, n_x, n_y, chunk_size_x = 500, chunk_size_y = 500):
    logs = []
    for _ in range(count):
        sprite = random.choice(sprites)
        x = random.randint((n_x) * chunk_size_x, (n_x + 1) * chunk_size_x - sprite.get_width())
        y = random.randint(sprite.get_height() + (n_y) * chunk_size_y, (n_y + 1) * chunk_size_y - sprite.get_height())
        new_log = MapObject(sprite, x, y, 50, "log")
        logs.append(new_log)
    return logs

# printing grass on the screen
def print_grass_chunk(game_manager, chunk):
    x = chunk.nb_x * chunk.size_x
    y = chunk.nb_y * chunk.size_y
    for sprite, type in chunk.bg_fill[0]:
        game_manager.screen.blit(sprite, (x - game_manager.map_view.x, y - game_manager.map_view.y))
  
# printing detailed grass on the screen
def print_detailed_chunk(game_manager, chunk):
    for sprite_list in chunk.details:
        for sprite in sprite_list:
            game_manager.screen.blit(sprite.sprite, (sprite.x - game_manager.map_view.x, sprite.y - game_manager.map_view.y))


# printing shadows if the object have one on the screen
def print_shadows_chunk(game_manager, chunk):
    for object_list in chunk.obj:
      for object in object_list:
        if object.shadow != None:
            game_manager.screen.blit(object.shadow, (object.shadow_x - game_manager.map_view.x, object.shadow_y - game_manager.map_view.y))


def print_obj(chunk, n_y, delta, game_manager):
    for objects in chunk.obj:
            for object in objects:
                if object.y >= n_y - object.display_priority and object.y < n_y + delta:
                    object.display(game_manager.screen, game_manager.user_interactions, game_manager.map_view)


def print_player(game_manager, n_y, delta, x, n_x, chunk):
    if game_manager.player.y >= n_y and game_manager.player.y < n_y + delta and x >= n_x and x <= n_x + chunk.size_x:
            if game_manager.larger_map_view.collidepoint(game_manager.player.x, game_manager.player.y):
                game_manager.player.display(game_manager.screen, game_manager.map_view)


def print_mobs(game_manager, n_y, delta, n_x, chunk):
    for mob in game_manager.mobs:
        if mob.y >= n_y and mob.y < n_y + delta and mob.x >= n_x and mob.x <= n_x + chunk.size_x:
            if game_manager.larger_map_view.collidepoint(mob.x, mob.y):
                mob.display(game_manager.screen, game_manager.map_view)

# displaying objects on the screen, from the top to the bottom
def display_entities_chunk(game_manager, chunk):
    n_y = chunk.nb_y * chunk.size_y
    n_x = chunk.nb_x * chunk.size_x
    x = game_manager.player.x
    delta = 5 # precision of the display
    while n_y <= (chunk.nb_y + 1) * chunk.size_y:
        print_obj(chunk, n_y, delta, game_manager)
        print_player(game_manager, n_y, delta, x, n_x, chunk)
        print_mobs(game_manager, n_y, delta, n_x, chunk)
        n_y += delta

def display_invisible_entities(game_manager):
    if game_manager.user_interactions.draw_invisible_area:
        fps = float("{:.2f}".format(game_manager.clock.get_fps()))
        text = game_manager.font.render(f'fps: {fps}', True, (0,0,0))
        game_manager.screen.blit(text, (game_manager.screen.get_width() - text.get_width(), 0))

        if (game_manager.larger_map_view.collidepoint(game_manager.player.x, game_manager.player.y)):
            pygame.draw.rect(game_manager.screen, (255, 0, 0), game_manager.player.get_hitbox(game_manager.map_view), 1)
            pygame.draw.rect(game_manager.screen, (0, 0, 255), game_manager.player.get_colhitbox(game_manager.map_view), 1)
            pygame.draw.rect(game_manager.screen, (255, 0, 255), game_manager.player.get_watchzone(game_manager.map_view), 1)
        
        for mob in game_manager.mobs:
            pygame.draw.rect(game_manager.screen, (255, 0, 0), mob.get_hitbox(game_manager.map_view), 1)
            pygame.draw.rect(game_manager.screen, (0, 0, 255), mob.get_colhitbox(game_manager.map_view), 1)
            pygame.draw.rect(game_manager.screen, (255, 0, 255), mob.get_watchzone(game_manager.map_view), 1)


def display_animations_chunk(game_manager):
    for animation in game_manager.animations_list:
        if animation.delay_n >= animation.delay:
            animation.display(game_manager.screen, game_manager.player.is_selected, game_manager.map_view)

def display_selection_area_chunk(game_manager):
    
    if game_manager.user_interactions.click:
        game_manager.screen.blit(game_manager.user_interactions.drawable_area, (game_manager.user_interactions.area.x, game_manager.user_interactions.area.y))
        pygame.draw.rect(game_manager.screen, (0, 195, 0), game_manager.user_interactions.area, 2)

def display_mini_map(game_manager):
    screen = game_manager.screen
    x = (game_manager.map_view.x / game_manager.map_size_x) * 290
    y = (game_manager.map_view.y / game_manager.map_size_y) * 230
    ratio_view_x =  1920  * 290 / (game_manager.map_size_x)
    ratio_view_y =  1080 * 230 / (game_manager.map_size_y)
    
    pygame.draw.rect(screen, (166, 176, 79), game_manager.minimap)
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(screen.get_width() - 300 + x, screen.get_height() - 240 + y, ratio_view_x, ratio_view_y), 2)
    
    x_icon = (game_manager.minimap.x + 290 * game_manager.player.x / game_manager.map_size_x) - 15 / 2 # determinate the corect x location of the player to show on the minimap
    y_icon = (game_manager.minimap.y + 230 * game_manager.player.y / game_manager.map_size_y) - 15 / 2 # determinate the corect y location of the player to show on the minimap
    screen.blit(game_manager.player.minimap_icon[0], (x_icon, y_icon))
    for mob in game_manager.mobs:
        x_icon = (game_manager.minimap.x + 290 * mob.x / game_manager.map_size_x) - 10 / 2
        y_icon = (game_manager.minimap.y + 230 * mob.y / game_manager.map_size_y) - 10 / 2
        screen.blit(mob.minimap_icon[0], (x_icon, y_icon))

def display_interface_chunk(game_manager):
    
    game_manager.screen.blit(game_manager.interface[0], (0, 0))
    display_mini_map(game_manager)
    if game_manager.player.is_selected:
        game_manager.player.draw_selection_interface(game_manager.screen, game_manager.map_view)
    else :
        for mob in game_manager.mobs:
            if mob.is_selected:
                mob.draw_selection_interface(game_manager.screen, game_manager.map_view)
                break


def get_chunk_to_display(game_manager):
    chunk_list = []
    x = game_manager.map_view.x
    y = game_manager.map_view.y
    nb_x_view = x // game_manager.chunk_size_x
    nb_y_view = y // game_manager.chunk_size_y
    inc_x = 0
    inc_y = 0

    while inc_y != 4 :
        while inc_x != 6:
            if (nb_y_view + inc_y) * game_manager.nb_chunk_x + (nb_x_view + inc_x) >= len(game_manager.chunks):
                return chunk_list
            if (nb_y_view + inc_y) * game_manager.nb_chunk_x + (nb_x_view + inc_x) < 0:
                return chunk_list
            chunk_list.append(game_manager.chunks[(nb_y_view + inc_y) * game_manager.nb_chunk_x + (nb_x_view + inc_x)])
            inc_x += 1
        inc_y += 1
        inc_x = 0
    return chunk_list


def print_chunks(game_manager):
    for chunk in game_manager.disp_chunks:
        print_grass_chunk(game_manager, chunk)
    for chunk in game_manager.disp_chunks:
        print_shadows_chunk(game_manager, chunk)
    for chunk in game_manager.disp_chunks:
        print_detailed_chunk(game_manager, chunk)
    for chunk in game_manager.disp_chunks:
        display_entities_chunk(game_manager, chunk)

# main function to print the map on the screen
def print_map_chunk(game_manager):
    print_chunks(game_manager)
    display_animations_chunk(game_manager)
    display_selection_area_chunk(game_manager)
    display_invisible_entities(game_manager)
    display_interface_chunk(game_manager)