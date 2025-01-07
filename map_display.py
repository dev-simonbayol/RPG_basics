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

# generating grass to fill background
def generate_grass_positions(sprites, map_size_x = 1920, map_size_y = 1080):
    grass_tiles = []
    x, y = 0, 0
    while y < map_size_y:
        while x < map_size_x:
            sprite = random.choice(sprites)
            grass_tiles.append((sprite, x, y, "grass"))
            x += sprite.get_width()
        x = 0
        y += sprite.get_height()
    return grass_tiles

# generating flowers to fill background randomly
def generate_flower_positions(sprites, count, map_size_x = 1920, map_size_y = 1080):
    flowers = []
    for _ in range(count):
        sprite = random.choice(sprites)
        x = random.randint(0, map_size_x - sprite.get_width())
        y = random.randint(sprite.get_height(), map_size_y - sprite.get_height())
        flowers.append((sprite, x, y, "flower"))
    return flowers


# generating trees and there shadow from y = 0 to screen_height by a ratio, return a list of trees
def generate_tree_positions(sprites, ratio, map_size_x = 1920, map_size_y = 1080):
    trees = []
    sprtie_tree = sprites[1]
    y = sprtie_tree.get_height()
    n = 0
    while y < map_size_y - sprites[1].get_height() * 2:
        sprite = sprites[0]
        x = random.randint(0, map_size_x - sprite.get_width())
        y += random.randint(0, int (ratio / 2))
        new_tree = MapObject(sprites[1], x, y , 100, "tree")
        new_tree.shadow = sprites[0] #attribute shadow to the tree
        new_tree.shadow_x = x - sprite.get_width() / 6
        new_tree.shadow_y = y - sprite.get_height() / 2
        new_tree.col_hitbox = pygame.Rect(x + sprite.get_width() / 5, y - new_tree.sprite.get_height() / 4, sprite.get_width() / 3, sprite.get_height() / 3)
        new_tree.hitbox = pygame.Rect(x + 10, y - new_tree.sprite.get_height(), new_tree.sprite.get_width() - 20, new_tree.sprite.get_height())
        trees.append(new_tree)
    return trees


#generating bushes randomly
def generate_bush_positions(sprites, count, map_size_x = 1920, map_size_y = 1080):
    bushes = []
    new_bush = None
    for _ in range(count):
        sprite = random.choice(sprites)
        x = random.randint(0, map_size_x - sprite.get_width())
        y = random.randint(sprite.get_height(), map_size_y)
        new_bush = MapObject(sprite, x, y, 50, "bush")
        new_bush.hitbox = pygame.Rect(x, y - sprite.get_height(), sprite.get_width(), sprite.get_height())
        bushes.append(new_bush)
    return bushes


# generating stones randomly
def generate_stones_positions(sprites, count, map_size_x = 1920, map_size_y = 1080):
    stones = []
    for _ in range(count):
        sprite = random.choice(sprites)
        x = random.randint(0, map_size_x - sprite.get_width())
        y = random.randint(sprite.get_height(), map_size_y)
        new_stone = MapObject(sprite, x, y, 250, "stone")
        new_stone.col_hitbox = pygame.Rect(x, y - new_stone.sprite.get_height() /2.2, sprite.get_width(), sprite.get_height() / 3)
        new_stone.hitbox = pygame.Rect(x, y - new_stone.sprite.get_height(), sprite.get_width(), sprite.get_height())
        stones.append(new_stone)
    return stones


# generating logs randomly
def generate_logs_positions(sprites, count, map_size_x = 1920, map_size_y = 1080):
    logs = []
    for _ in range(count):
        sprite = random.choice(sprites)
        x = random.randint(0, map_size_x - sprite.get_width())
        y = random.randint(sprite.get_height(), map_size_y)
        new_log = MapObject(sprite, x, y, 50, "log")
        logs.append(new_log)
    return logs

# printing grass on the screen
def print_grass(game_manager):
    for sprite, x, y, type in game_manager.generated_map_bg[0]:
        if game_manager.larger_map_view.collidepoint(x, y):
            game_manager.screen.blit(sprite, (x - game_manager.map_view.x, y - game_manager.map_view.y))
  
# printing detailed grass on the screen
def print_detailed_grass(game_manager):
    for sprite, x, y, type in game_manager.generated_map_bg[1]:
        if game_manager.larger_map_view.collidepoint(x, y):
            game_manager.screen.blit(sprite, (x - game_manager.map_view.x, y - game_manager.map_view.y))


# printing shadows if the object have one on the screen
def print_shadows(game_manager):
    for object_list in game_manager.generated_map_obj:
      for object in object_list:
        if object.shadow != None:
            if game_manager.larger_map_view.collidepoint(object.shadow_x , object.shadow_y):
                game_manager.screen.blit(object.shadow, (object.shadow_x - game_manager.map_view.x, object.shadow_y - game_manager.map_view.y))


# displaying objects on the screen, from the top to the bottom
def display_obj(game_manager):
    n_y = 0
    delta = 5 # precision of the display
    while n_y <= game_manager.map_size_y:
        for objects in game_manager.generated_map_obj:
            for object in objects:
                if object.y >= n_y - object.display_priority and object.y < n_y + delta:
                    if game_manager.larger_map_view.collidepoint(object.x, object.y):
                        object.display(game_manager.screen, game_manager.user_interactions, game_manager.map_view)
        if game_manager.player.y >= n_y and game_manager.player.y < n_y + delta:
            if game_manager.larger_map_view.collidepoint(game_manager.player.x, game_manager.player.y):
                game_manager.player.display(game_manager.screen, game_manager.map_view)
        n_y += delta


def display_animations(game_manager):
    for animation in game_manager.animations_list:
        if animation.delay_n >= animation.delay:
            if game_manager.larger_map_view.collidepoint(animation.x, animation.y):
                animation.display(game_manager.screen, game_manager.player.is_selected, game_manager.map_view)

def display_selection_area(game_manager, view):
    
    if game_manager.user_interactions.click:
        game_manager.screen.blit(game_manager.user_interactions.drawable_area, (game_manager.user_interactions.area.x, game_manager.user_interactions.area.y))
        pygame.draw.rect(game_manager.screen, (0, 195, 0), game_manager.user_interactions.area, 2)
    if game_manager.user_interactions.draw_invisible_area:
        fps = float("{:.2f}".format(game_manager.clock.get_fps()))
        text = game_manager.font.render(f'fps: {fps}', True, (0,0,0))
        game_manager.screen.blit(text, (game_manager.screen.get_width() - text.get_width(), 0))
        if (game_manager.larger_map_view.collidepoint(game_manager.player.x, game_manager.player.y)):
            pygame.draw.rect(game_manager.screen, (255, 0, 0), game_manager.player.get_hitbox(game_manager.map_view), 1)
            pygame.draw.rect(game_manager.screen, (0, 0, 255), game_manager.player.get_colhitbox(game_manager.map_view), 1)

def display_interface(game_manager):
    
    game_manager.screen.blit(game_manager.interface[0], (0, 0))
    if game_manager.player.is_selected:
        if game_manager.map_view.collidepoint(game_manager.player.x, game_manager.player.y):
            game_manager.player.draw_selection_interface(game_manager.screen, game_manager.map_view)

# main function to print the map on the screen
def print_map(game_manager):
    fullmap = False
    x, y = 0, 0
    print_grass(game_manager)
    print_detailed_grass(game_manager)
    print_shadows(game_manager)
    display_obj(game_manager)
    display_animations(game_manager)
    display_selection_area(game_manager, game_manager.map_view)
    display_interface(game_manager)