import pygame

class MapObject:
    def __init__(self, sprite, x, y, hp, resource_type):
        self.sprite = sprite
        self.x = x
        self.y = y
        self.hp = hp
        self.col_hitbox = None
        self.hitbox = None
        self.type = resource_type
        self.shadow = None
        self.shadow_x = x
        self.shadow_y = y
        self.display_priority = 0

    def display(self, screen, user_interactions, view):
        screen.blit(self.sprite, (self.x - view.x, self.y - self.sprite.get_height() - view.y))
        if user_interactions.draw_invisible_area:
            if self.hitbox is not None:
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.hitbox.x - view.x, self.hitbox.y - view.y, self.hitbox.width, self.hitbox.height), 1)
            if self.col_hitbox is not None:
                pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(self.col_hitbox.x - view.x, self.col_hitbox.y - view.y, self.col_hitbox.width, self.col_hitbox.height), 1)

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.disappear()

    def disappear(self):
        # Logic to make the object disappear
        print(f"{self.resource_type} at {(self.x, " ", self.y)} has disappeared.")

    def get_resources(self):
        if self.hp == 0:
            return self.type
        else:
            return None