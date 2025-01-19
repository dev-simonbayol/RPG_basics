import pygame

from player import *

def change_direction_left_above(Px, Py, Ox, Oy, player, object, speed):
    if Py + player.colhitbox.height <= Oy : # player is stuck above the object
        if player.facing == "right" and player.dy < player.y: # player is facing right and going up
            player.y -= speed
        elif player.facing == "right" and player.dy > player.y: # player is facing right and going down
            player.y += speed
        else : # player is facing left ?
            player.x -= speed
    else : # player is on the left and above the object
        if player.facing == "right" and player.dy < player.y: # player is facing right and going up
            player.y -= speed
        elif player.facing == "right" and player.dy > player.y: # player is facing right and going down
            player.x += speed
        else : # player is facing left ?
            player.x -= speed
        

def change_direction_right_above(Px, Py, Ox, Oy, player, object, speed):
    if Py + player.colhitbox.height <= Oy + player.speed : # player is stuck above the object
        if player.facing == "right" and player.dy < player.y: # player is facing right and going up
            player.x += speed
            player.y += speed
        elif player.facing == "right" and player.dy > player.y: # player is facing right and going down
            player.x += speed
        else : # player is facing left ?
            player.x -= speed
    else : # player is on the right and above the object
        if player.facing == "right" and player.dy < player.y: # player is facing right and going up
            player.x += speed
        elif player.facing == "right" and player.dy > player.y: # player is facing right and going down
            player.x += speed
        else : # player is facing left ?
            player.y -= speed

def change_direction_left_below(Px, Py, Ox, Oy, player, object, speed):
    if Py >= Oy + object.col_hitbox.height : # player is stuck under the object
        if player.facing == "right" and player.dy < player.y: # player is facing right and going up
            player.x += speed
        elif player.facing == "right" and player.dy > player.y: # player is facing right and going down
            player.x += speed
        else : # player is facing left ?
            player.x -= speed
    else : # player is on the left and below the object
        if player.facing == "right" and player.dy < player.y: # player is facing right and going up
            player.y -= speed
        elif player.facing == "right" and player.dy > player.y: # player is facing right and going down
            player.y += speed
        else : # player is facing left ?
            player.x -= speed

def change_direction_right_below(Px, Py, Ox, Oy, player, object, speed):
    if Py >= Oy + object.col_hitbox.height : # player is stuck under the object
        if player.facing == "right" and player.dy < player.y: # player is facing right and going up
            player.x += speed
        elif player.facing == "right" and player.dy > player.y: # player is facing right and going down
            player.x += speed
        else : # player is facing left ?
            player.x -= speed
    else : # player is on the left and below the object
        if player.facing == "right" and player.dy < player.y: # player is facing right and going up
            player.x += speed
        elif player.facing == "right" and player.dy > player.y: # player is facing right and going down
            player.x += speed
        else : # player is facing left ?
            player.y += speed

def change_direction(player, object):
    Px = player.colhitbox.x
    Py = player.colhitbox.y
    Ox = object.col_hitbox.x
    Oy = object.col_hitbox.y
    speed = player.speed

    if object.col_hitbox.collidepoint(player.dx, player.dy):
        player.dx = player.x
        player.dy = player.y
        player.oldx = player.x
        player.oldy = player.y
        player.update_hitbox()
        player.init_movement()
        return
        
    if Px <= Ox and Py <= Oy: # player is on the left and above the object
        change_direction_left_above(Px, Py, Ox, Oy, player, object, speed)
    elif Px >= Ox and Py <= Oy: # player is on the right and above the object
        change_direction_right_above(Px, Py, Ox, Oy, player, object, speed)
    elif Px <= Ox and Py >= Oy: # player is on the left and below the object
        change_direction_left_below(Px, Py, Ox, Oy, player, object, speed)
    elif Px >= Ox and Py >= Oy: # player is on the right and below the object
        change_direction_right_below(Px, Py, Ox, Oy, player, object, speed)                                                        
            
    player.update_hitbox()
    player.init_movement()

def check_collision(entitie, chunks):
    
    for chunk in chunks:
        for obj_list in chunk.obj:
            for obj in obj_list:
                if obj.col_hitbox is not None:
                    if entitie.colhitbox.colliderect(obj.col_hitbox):
                        entitie.x = entitie.old_x
                        entitie.y = entitie.old_y
                        entitie.update_hitbox()
                        change_direction(entitie, obj)
                        break

def moving_managment(game_manager) :
    if game_manager.player.state == "run":
        game_manager.player.moving(game_manager.clock.get_time())
        check_collision(game_manager.player, game_manager.chunks)
    for mob in game_manager.mobs:
        if mob.state == "run":
            mob.moving(game_manager.clock.get_time())
            check_collision(mob, game_manager.chunks)
            