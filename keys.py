import pygame
from player import *
from animation_managment import *
from chunk_map import *

pygame.init()

cd_mouse0 = 0
cd_mouse3 = 0

def right_click_actions (player, animations_list, view):
    global cd_mouse3
    
    if cd_mouse3 > 75 and player.is_selected:
        player.dx = pygame.mouse.get_pos()[0] + view.x
        player.dy = pygame.mouse.get_pos()[1] + view.y
        player.check_facing()
        player.init_movement()
        cd_mouse3 = 0


def delete_animation_right_click(animations_list, player):

    for animation in animations_list: # delete existent click animation
        if animation.type == "rclick":
            animations_list.remove(animation)


def create_animation_right_click(game_manager, mouse_pos):
    
    if game_manager.player.is_selected == False:
        return
    
    new_sprite= load_sprites(r"C:\Users\simon\Desktop\personal_project\RPG_basics\sprites\UI\mouse", 1, 1) #create a new animation for right click on map
    new_rclick = Map_Animation(new_sprite[0], mouse_pos[0] + game_manager.map_view.x, mouse_pos[1] + game_manager.map_view.y, 436/14, 15, 5, "rclick")

    delete_animation_right_click(game_manager.animations_list, game_manager.player)

    new_rclick.offsety = new_rclick.sprite.get_height()
    new_rclick.delay = 0
    game_manager.animations_list.append(new_rclick)

def left_click_pressed (player, animations_list, user_interactions):
    mouse_pos = pygame.mouse.get_pos()
    new_area = pygame.Rect(mouse_pos[0], mouse_pos[1], 5, 5)
    new_drawable_area = pygame.surface.Surface((5, 5))

    new_drawable_area.set_alpha(35)
    new_drawable_area.fill((0, 255, 0))
    user_interactions.click = True
    user_interactions.area = new_area
    user_interactions.drawable_area = new_drawable_area
    user_interactions.saved_x = mouse_pos[0]
    user_interactions.saved_y = mouse_pos[1]


def left_click_actions (user_interactions):
    mouse_pos = pygame.mouse.get_pos()
    
    if user_interactions.click:
        if mouse_pos[0] - user_interactions.saved_x > 0 and mouse_pos[1] - user_interactions.saved_y > 0:
            user_interactions.area.x = user_interactions.saved_x
            user_interactions.area.y = user_interactions.saved_y
            user_interactions.area.width = mouse_pos[0] - user_interactions.saved_x
            user_interactions.area.height = mouse_pos[1] - user_interactions.saved_y
        elif mouse_pos[0] - user_interactions.saved_x < 0 and mouse_pos[1] - user_interactions.saved_y > 0:
            user_interactions.area.width = abs(mouse_pos[0] - user_interactions.saved_x)
            user_interactions.area.height = mouse_pos[1] - user_interactions.saved_y
            user_interactions.area.x = user_interactions.saved_x - user_interactions.area.width
            user_interactions.area.y = user_interactions.saved_y
        elif mouse_pos[0] - user_interactions.saved_x > 0 and mouse_pos[1] - user_interactions.saved_y < 0:
            user_interactions.area.width = mouse_pos[0] - user_interactions.saved_x
            user_interactions.area.height = abs(mouse_pos[1] - user_interactions.saved_y)
            user_interactions.area.y = user_interactions.saved_y - user_interactions.area.height
            user_interactions.area.x = user_interactions.saved_x
        else:
            user_interactions.area.width = abs(mouse_pos[0] - user_interactions.saved_x)
            user_interactions.area.height = abs(mouse_pos[1] - user_interactions.saved_y)
            user_interactions.area.x = user_interactions.saved_x - user_interactions.area.width
            user_interactions.area.y = user_interactions.saved_y - user_interactions.area.height

        user_interactions.drawable_area = pygame.transform.scale(user_interactions.drawable_area, (user_interactions.area.width, user_interactions.area.height))


def update_cd(clock):
    global cd_mouse3
    global cd_mouse0
    d_time = clock.get_time()
    
    cd_mouse3 += d_time

def get_selected_obj_in_area(user_interactions, player, view):
    
    for selected_obj in user_interactions.selected_obj: # remove all selected objects
        selected_obj.is_selected = False
        user_interactions.selected_obj.remove(selected_obj)
    
    if user_interactions.area.height == 0 or user_interactions.area.width == 0:
        user_interactions.area.height = 1
        user_interactions.area.width = 1
    if user_interactions.area.colliderect(player.get_hitbox(view)): # check if the player is in the area
        if player.is_selected == False:
            user_interactions.selected_obj.append(player)
            player.is_selected = True
    else :
        player.is_selected = False

def move_view(game_manager, keys):
    if keys[pygame.K_d]:
        if game_manager.map_view.x + 1920 + game_manager.map_speed < game_manager.map_size_x:
            game_manager.map_view.x += + game_manager.map_speed
            game_manager.larger_map_view.x += game_manager.map_speed
            game_manager.map_decay += game_manager.map_speed
    if keys[pygame.K_z]:
        if game_manager.map_view.y >= + game_manager.map_speed:
            game_manager.map_view.y -= + game_manager.map_speed
            game_manager.larger_map_view.y -= game_manager.map_speed
            game_manager.map_decay += game_manager.map_speed
    if keys[pygame.K_q]:
        if game_manager.map_view.x >= + game_manager.map_speed:
            game_manager.map_view.x -= + game_manager.map_speed
            game_manager.larger_map_view.x -= game_manager.map_speed
            game_manager.map_decay += game_manager.map_speed
    if keys[pygame.K_s]:
        if game_manager.map_view.y + 1080 + game_manager.map_speed < game_manager.map_size_y:
            game_manager.map_view.y += + game_manager.map_speed
            game_manager.larger_map_view.y += game_manager.map_speed
            game_manager.map_decay += game_manager.map_speed
    if game_manager.map_decay >= game_manager.chunk_size_x / 10:
        game_manager.map_decay = 0
        game_manager.disp_chunks = get_chunk_to_display(game_manager)
    

def manage_keys_input (game_manager):
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    
    update_cd(game_manager.clock) #update global cooldowns
    
    for event in game_manager.events: # events loop handling (single_time pressed events)
        if event.type == pygame.QUIT:
            game_manager.running = False
        if event.type == pygame.MOUSEBUTTONDOWN: # mouse click handling
            if event.button == pygame.BUTTON_RIGHT:
                delete_animation_right_click(game_manager.animations_list, game_manager.player)
            if event.button == pygame.BUTTON_LEFT:
                left_click_pressed(game_manager.player, game_manager.animations_list, game_manager.user_interactions)
        if event.type == pygame.MOUSEBUTTONUP: # mouse release handling
            if event.button == pygame.BUTTON_RIGHT:
                create_animation_right_click(game_manager, pygame.mouse.get_pos())
            if event.button == pygame.BUTTON_LEFT:
                get_selected_obj_in_area(game_manager.user_interactions, game_manager.player, game_manager.map_view)
                game_manager.user_interactions.click = False
                game_manager.user_interactions.area = None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                game_manager.user_interactions.draw_invisible_area = not game_manager.user_interactions.draw_invisible_area
    
    # keys input handling (repeated pressed events)
    move_view(game_manager, keys)
    if keys[pygame.K_ESCAPE]:
        game_manager.running = False
    if mouse[pygame.BUTTON_RIGHT - 1]:
        right_click_actions(game_manager.player, game_manager.animations_list, game_manager.map_view)
    if mouse[pygame.BUTTON_LEFT - 1]:
        left_click_actions(game_manager.user_interactions)