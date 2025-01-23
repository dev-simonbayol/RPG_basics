import pygame
from player import *
from animation_managment import *
from chunk_map import *

pygame.init()

cd_mouse0 = 0
cd_mouse3 = 0

def right_click_actions (player, view, mobs):
    global cd_mouse3
    
    if cd_mouse3 > 75:
        if player.is_selected and player.has_died != True:
            player.dx = pygame.mouse.get_pos()[0] + view.x
            player.dy = pygame.mouse.get_pos()[1] + view.y
            player.check_facing()
            player.init_movement()
            player.target = None
        cd_mouse3 = 0


def delete_animation_right_click(animations_list, player):

    for animation in animations_list: # delete existent click animation
        if animation.type == "rclick":
            animations_list.remove(animation)
    if player.attack_move:
        player.attack_move = False
        player.is_attacking = False


def trigger_attack(entitie1, entiti2):

    entitie1.dx = entiti2.x
    entitie1.dy = entiti2.y
    entitie1.check_facing()
    entitie1.init_movement()
    entitie1.target = entiti2
    

def right_click_released(game_manager, mouse_pos):
    
    global cd_mouse3
    if game_manager.player.is_selected == False or game_manager.player.has_died == True:
        return
    
    mob_n = 0
    for mob in game_manager.mobs:
        if mob.hitbox.collidepoint(mouse_pos):
            if mob.hp > 0:
                trigger_attack(game_manager.player, mob)
                cd_mouse3 = -25
            return
        mob_n += 1
    
    game_manager.player.target = None
    new_sprite= load_sprites(r"C:\Users\simon\Desktop\personal_project\RPG_basics\sprites\UI\mouse", 1, 1) #create a new animation for right click on map
    new_rclick = Map_Animation(new_sprite[0], mouse_pos[0] + game_manager.map_view.x, mouse_pos[1] + game_manager.map_view.y, 436/14, 15, 5, "rclick")

    delete_animation_right_click(game_manager.animations_list, game_manager.player)

    new_rclick.offsety = new_rclick.sprite.get_height()
    new_rclick.delay = 0
    game_manager.animations_list.append(new_rclick)

def left_click_pressed (game_manager):
    
    mouse_pos = pygame.mouse.get_pos()
    
    if game_manager.minimap.collidepoint(mouse_pos):
        game_manager.minimap_clicked = True
        game_manager.user_interactions.saved_x = mouse_pos[0]
        game_manager.user_interactions.saved_y = mouse_pos[1]
        return
    
    if game_manager.player.set_cursor_atk:
        return
    
    new_area = pygame.Rect(mouse_pos[0], mouse_pos[1], 5, 5)
    new_drawable_area = pygame.surface.Surface((5, 5))

    new_drawable_area.set_alpha(35)
    new_drawable_area.fill((0, 255, 0))
    game_manager.user_interactions.click = True
    game_manager.user_interactions.area = new_area
    game_manager.user_interactions.drawable_area = new_drawable_area
    game_manager.user_interactions.saved_x = mouse_pos[0]
    game_manager.user_interactions.saved_y = mouse_pos[1]


def left_click_actions (user_interactions, minimap_clicked):
    mouse_pos = pygame.mouse.get_pos()
    
    if minimap_clicked:
        return "minimap_clicked"
    elif user_interactions.click:
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
        return "drawing_selection"


def update_cd(clock):
    global cd_mouse3
    global cd_mouse0
    d_time = clock.get_time()
    
    cd_mouse3 += d_time

def get_selected_obj_in_area(game_manager):
    
    if game_manager.minimap_clicked == True:
        game_manager.minimap_clicked = False
        return
    
    for selected_obj in game_manager.user_interactions.selected_obj: # remove all selected objects
        selected_obj.is_selected = False
        game_manager.user_interactions.selected_obj.remove(selected_obj)
    
    if game_manager.user_interactions.area.height == 0 or game_manager.user_interactions.area.width == 0:
        game_manager.user_interactions.area.height = 1
        game_manager.user_interactions.area.width = 1
    if game_manager.user_interactions.area.colliderect(game_manager.player.get_hitbox(game_manager.map_view)): # check if the player is in the area
        if game_manager.player.is_selected == False:
            game_manager.user_interactions.selected_obj.append(game_manager.player)
            game_manager.player.is_selected = True
    else :
        game_manager.player.is_selected = False
    
    for mob in game_manager.mobs:
        if game_manager.user_interactions.area.colliderect(mob.get_hitbox(game_manager.map_view)): # check if the mob is in the area
            if mob.is_selected == False:
                game_manager.user_interactions.selected_obj.append(mob)
                mob.is_selected = True
        else :
            mob.is_selected = False

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
    if game_manager.map_decay >= game_manager.chunk_size_x / 5:
        game_manager.map_decay = 0
        game_manager.disp_chunks = get_chunk_to_display(game_manager)
    

def move_view_from_minimap(gm):
    mouse_pos = pygame.mouse.get_pos()
    decay_x = (mouse_pos[0] - gm.minimap.x)
    decay_y = (mouse_pos[1] - gm.minimap.y)

    gm.map_view.x = (decay_x * gm.map_size_x / 290) - 1920 / 2
    gm.map_view.y = (decay_y * gm.map_size_y / 230) - 1080 / 2
    if gm.map_view.x >= gm.map_size_x - 1920:
        gm.map_view.x = gm.map_size_x - 1920
    if gm.map_view.y >= gm.map_size_y - 1080:
        gm.map_view.y = gm.map_size_y - 1080
    if gm.map_view.x <= 0:
        gm.map_view.x = 0
    if gm.map_view.y <= 0:
        gm.map_view.y = 0
    gm.larger_map_view.x = gm.map_view.x - 400
    gm.larger_map_view.y = gm.map_view.y - 400
    gm.disp_chunks = get_chunk_to_display(gm)


def move_and_attack(gm):
    if gm.player.has_died:
        return

    gm.player.dx = pygame.mouse.get_pos()[0] + gm.map_view.x
    gm.player.dy = pygame.mouse.get_pos()[1] + gm.map_view.y
    gm.player.check_facing()
    gm.player.init_movement()
    gm.player.target = None
    gm.player.attack_move = True


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
                left_click_pressed(game_manager)
        if event.type == pygame.MOUSEBUTTONUP: # mouse release handling
            if event.button == pygame.BUTTON_RIGHT:
                right_click_released(game_manager, pygame.mouse.get_pos())
            if event.button == pygame.BUTTON_LEFT:
                if game_manager.player.is_selected and game_manager.player.set_cursor_atk:
                    move_and_attack(game_manager)
                    game_manager.player.set_cursor_atk = False
                else :
                    get_selected_obj_in_area(game_manager)
                    game_manager.user_interactions.click = False
                    game_manager.user_interactions.area = None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                game_manager.user_interactions.draw_invisible_area = not game_manager.user_interactions.draw_invisible_area
            if event.key == pygame.K_a:
                if game_manager.player.is_selected and game_manager.user_interactions.click != True:
                    game_manager.player.set_cursor_atk = True
    
    # keys input handling (repeated pressed events)
    move_view(game_manager, keys)
    if keys[pygame.K_ESCAPE]:
        game_manager.running = False
    if mouse[pygame.BUTTON_RIGHT - 1]:
        right_click_actions(game_manager.player, game_manager.map_view, game_manager.mobs)
    if mouse[pygame.BUTTON_LEFT - 1]:
        if (left_click_actions(game_manager.user_interactions, game_manager.minimap_clicked)) == "minimap_clicked" and game_manager.player.attack_move == False:
            move_view_from_minimap(game_manager)