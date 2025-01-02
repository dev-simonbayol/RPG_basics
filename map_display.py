import pygame
import os
import random

from object_class_map_ressources import *

# loading sprites from a folder, precising size of the sprite
def load_sprites(folder, size_x, size_y):
    sprites = []
    for filename in os.listdir(folder):
        if filename.endswith('.png'):
            image = pygame.transform.scale_by(pygame.image.load(os.path.join(folder, filename)), (size_x, size_y))
            sprites.append(image)
    return sprites

# generating grass to fill background
def generate_grass_positions(screen, sprites):
    grass_tiles = []
    x, y = 0, 0
    while y < screen.get_height():
        while x < screen.get_width():
            sprite = random.choice(sprites)
            grass_tiles.append((sprite, x, y, "grass"))
            x += sprite.get_width()
        x = 0
        y += sprite.get_height()
    return grass_tiles

# generating flowers to fill background randomly
def generate_flower_positions(screen, sprites, count):
    flowers = []
    for _ in range(count):
        sprite = random.choice(sprites)
        x = random.randint(0, screen.get_width() - sprite.get_width())
        y = random.randint(0, screen.get_height() - sprite.get_height())
        flowers.append((sprite, x, y, "flower"))
    return flowers


# generating trees and there shadow from y = 0 to screen_height by a ratio, return a list of trees
def generate_tree_positions(screen, sprites, ratio):
    trees = []
    y = 0
    n = 0
    while y < screen.get_height() - sprites[1].get_height() * 2:
        sprite = sprites[0]
        x = random.randint(0, screen.get_width() - sprite.get_width())
        y += random.randint(0, ratio)
        new_tree = MapObject(sprites[1], x, y , 100, "tree")
        new_tree.shadow = sprites[0] #attribute shadow to the tree
        new_tree.shadow_x = x - sprite.get_width() / 6
        new_tree.shadow_y = y - sprite.get_height() / 2
        new_tree.col_hitbox = pygame.Rect(x + sprite.get_width() / 5, y - new_tree.sprite.get_height() / 4, sprite.get_width() / 3, sprite.get_height() / 3)
        new_tree.hitbox = pygame.Rect(x + 10, y - new_tree.sprite.get_height(), new_tree.sprite.get_width() - 20, new_tree.sprite.get_height())
        trees.append(new_tree)
    return trees


#generating bushes randomly
def generate_bush_positions(screen, sprites, count):
    bushes = []
    new_bush = None
    for _ in range(count):
        sprite = random.choice(sprites)
        x = random.randint(0, screen.get_width() - sprite.get_width())
        y = random.randint(0, screen.get_height() - sprite.get_height())
        new_bush = MapObject(sprite, x, y, 50, "bush")
        new_bush.hitbox = pygame.Rect(x, y - sprite.get_height(), sprite.get_width(), sprite.get_height())
        bushes.append(new_bush)
    return bushes


# generating stones randomly
def generate_stones_positions(screen, sprites, count):
    stones = []
    for _ in range(count):
        sprite = random.choice(sprites)
        x = random.randint(0, screen.get_width() - sprite.get_width())
        y = random.randint(0, screen.get_height() - sprite.get_height())
        new_stone = MapObject(sprite, x, y, 250, "stone")
        new_stone.col_hitbox = pygame.Rect(x, y - new_stone.sprite.get_height() /2.2, sprite.get_width(), sprite.get_height() / 3)
        new_stone.hitbox = pygame.Rect(x, y - new_stone.sprite.get_height(), sprite.get_width(), sprite.get_height())
        stones.append(new_stone)
    return stones


# generating logs randomly
def generate_logs_positions(screen, sprites, count):
    logs = []
    for _ in range(count):
        sprite = random.choice(sprites)
        x = random.randint(0, screen.get_width() - sprite.get_width())
        y = random.randint(0, screen.get_height() - sprite.get_height())
        new_log = MapObject(sprite, x, y, 50, "log")
        logs.append(new_log)
    return logs

# printing grass on the screen
def print_grass(screen, positions):
    for sprite, x, y, type in positions:
        screen.blit(sprite, (x, y))
  
# printing detailed grass on the screen
def print_detailed_grass(screen, positions):
    for sprite, x, y, type in positions:
        screen.blit(sprite, (x, y))


# printing shadows if the object have one on the screen
def print_shadows(screen, objects_lists):
    for object_list in objects_lists:
      for object in object_list:
        if object.shadow != None:
            screen.blit(object.shadow, (object.shadow_x , object.shadow_y))


# displaying objects on the screen, from the top to the bottom
def display_obj(screen, objects_lists, player, user_interactions):
    n_y = 0
    delta = 5 # precision of the display
    while n_y <= screen.get_height():
        for objects in objects_lists:
            for object in objects:
                if object.y >= n_y - object.display_priority and object.y < n_y + delta:
                    object.display(screen, user_interactions)
        if player.y >= n_y and player.y < n_y + delta:
            player.display(screen)
        n_y += delta


def display_animations(screen, animations_list, player):
    for animation in animations_list:
        if animation.delay_n >= animation.delay:
            animation.display(screen, player.is_selected)

def display_selection_area(screen, user_interactions, player):
    
    if user_interactions.click:
        screen.blit(user_interactions.drawable_area, (user_interactions.area.x, user_interactions.area.y))
        pygame.draw.rect(screen, (0, 195, 0), user_interactions.area, 2)
    if user_interactions.draw_invisible_area:
        pygame.draw.rect(screen, (255, 0, 0), player.hitbox, 1)
        pygame.draw.rect(screen, (0, 0, 255), player.colhitbox, 1)

# main function to print the map on the screen
def print_map(screen, generatted_map_bg, generated_map_obj, player, animations_list, user_interactions):
    fullmap = False
    x, y = 0, 0
    print_grass(screen, generatted_map_bg[0])
    print_detailed_grass(screen, generatted_map_bg[1])
    print_shadows(screen, generated_map_obj)
    display_obj(screen, generated_map_obj, player, user_interactions)
    display_animations(screen, animations_list, player)
    display_selection_area(screen, user_interactions, player)