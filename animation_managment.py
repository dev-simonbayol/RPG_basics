import pygame
import time

class Map_Animation:
    def __init__(self, sprite, x, y, offsetx, speed, rep, type):
        self.sprite = sprite
        self.animation_speed = speed
        self.animation_time = 0
        self.x = x
        self.y = y
        self.animation_x = 0
        self.animation_y = 0
        self.offsetx = offsetx
        self.offsety = 0
        self.nb_repetition = rep
        self.rep_count = 0
        self.type = type
        self.delay = 0
        self.delay_n = 0


    def disappear(self):
        self.x = -10000
        self.y = -10000

    def animation(self, time, indicator):
        self.animation_time += time
        if self.animation_time > self.animation_speed:
            if self.animation_x + self.offsetx < self.sprite.get_width():
                self.animation_x += self.offsetx
            else:
                self.animation_x = 0
                self.rep_count += 1
            self.animation_time = 0
        if indicator == "idle":
            self.rep_count = self.nb_repetition + 1
    
    def display(self, screen, indicator = True, view = None):
        if not indicator and self.type == "rclick":
            return
        if view == None:
            screen.blit(self.sprite, (self.x - self.offsetx / 2, self.y - self.sprite.get_height()), (self.animation_x, self.animation_y, self.offsetx, self.offsety))
        else:
            screen.blit(self.sprite, (self.x - self.offsetx / 2 - view.x, self.y - self.sprite.get_height() - view.y), (self.animation_x, self.animation_y, self.offsetx, self.offsety))


def animation_managment(game_manager):
    d_time = game_manager.clock.get_time()
    
    game_manager.player.animation(d_time) # launch player animation
    for mob in game_manager.mobs:
        mob.animation(d_time)

    for animation in game_manager.animations_list: # launch all animations
        if animation.delay != 0 and animation.delay_n <= animation.delay: # manage the delay of new animation
            animation.delay_n += d_time
        animation.animation(d_time, indicator = game_manager.player.state)
        if animation.rep_count > animation.nb_repetition:
            game_manager.animations_list.remove(animation)