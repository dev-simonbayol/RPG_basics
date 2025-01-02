import pygame

class MapObject:
    def __init__(self, sprite, x, y, hp, resource_type):
        self.sprite = sprite
        self.x = x
        self.y = y
        self.hp = hp
        self.type = resource_type
        self.shadow = None
        self.shadow_x = x
        self.shadow_y = y
        self.display_priority = 0

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.disappear()

    def disappear(self):
        # Logic to make the object disappear
        print(f"{self.resource_type} at {self.position} has disappeared.")

    def get_resources(self):
        if self.hp == 0:
            return self.resource_type
        else:
            return None