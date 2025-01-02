import pygame

from player import *

def moving_managment(clock, player) :
    if player.state == "run":
        player.moving(clock.get_time())