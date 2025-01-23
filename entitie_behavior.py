import pygame

from werewolf import *
from player import *

def entities_behavior(gm):

    for mob in gm.mobs:
        mob.look_for_targets(gm.player)
    if gm.player.attack_move:
        gm.player.look_for_targets(gm.mobs)