import pygame
import math

from map_display import load_sprites

class PlayerClass:
    def __init__(self, x, y):
        
        # Player base attribute
        self.x = x
        self.y = y
        self.hitbox = 0
        self.colhitbox = None
        self.hp = 100

        # Player movement attributes
        self.dx = x
        self.dy = y
        self.x_speed = 5
        self.y_speed = 5
        self.a = 0
        self.b = 0
        self.speed = 5
        self.running_time = 0
        self.old_x = x
        self.old_y = y
    
        # Player sprite attributes
        self.current_sprite = None
        self.idle = None
        self.idle2 = None
        self.jump = None
        self.walk = self.idle = None
        self.run = self.idle = None
        self.attack = None
        self.attack2 = None
        self.attack3 = None
        self.hurt = None
        self.die = None
        self.state = "idle"
    
        # Player sprite animation attributes
        self.offsety = 128
        self.offsetx = 128
        self.animation_x = 0
        self.animation_y = 0
        self.animation_time = 0
        self.animation_speed = 100
        self.facing = "right"

        # Player display attributes
        self.display_priority = 0
        
        # Selection attributes
        self.is_selected = True
        self.selected_sprite = None
        self.selected_sprite_offsetx = 0
        self.selected_sprite_offsety = 0
        self.selected_sprite_x = 0
        self.selected_sprite_y = 0
        self.selected_sprite_animation_time = 0
        self.selected_sprite_animation_speed = 0


    def update_hitbox(self):
        self.hitbox = pygame.Rect(self.x - self.offsetx / 4.3, self.y - self.current_sprite.get_height() / 1.7, self.offsetx / 2, self.offsety / 1.6)
        self.colhitbox = pygame.Rect(self.x - self.offsetx / 14, self.y - self.current_sprite.get_height() / 14, self.offsetx / 5, self.offsety / 12)

    # Function to manage the player's movement
    def moving(self, time):
        if self.running_time > 5: # speed (time) of the player movement action
            self.old_x = self.x
            self.old_y = self.y
            if self.x < self.dx: # if the player is on the left side of the destination
                if self.x + self.x_speed > self.dx:
                    self.x = self.dx
                else:
                    self.x += self.x_speed
            else: # if the player is on the right side of the destination
                if self.x - self.x_speed < self.dx:
                    self.x = self.dx
                else:
                    self.x -= self.x_speed
            if abs(self.y - self.dy) < 0.3 : # if the player is close enough to the destination, he will directly go to it preventing weird movement
                    self.y = self.dy
            else :
                if self.y_speed == 0 : # no y speed means y is calculated with a*x + b equation
                    self.y = self.a * self.x + self.b
                else : # if the player moves only on y axis
                    if self.y < self.dy: # if the player is on the top side of the destination
                        if self.y + self.speed > self.dy:
                            self.y = self.dy
                        else:
                            self.y += self.speed
                    else: # if the player is on the bottom side of the destination
                        if self.y - self.speed < self.dy:
                            self.y = self.dy
                        else:
                            self.y -= self.speed
            self.running_time = 0 #reset timer of the movement
            self.update_hitbox()
        else:
            self.running_time += time # increment the timer of the movement
        if self.x == self.dx and self.y == self.dy: # if the player has reached the destination
            self.state = "idle"
            self.current_sprite = self.idle
            self.animation_speed = 200
            self.x_speed = 0
    
    
    # Function to define the x speed of the player, in order to have a constant speed
    def define_x_speed(self):
            distance = ((self.dx - self.x) ** 2 + (self.dy - self.y) ** 2) ** 0.5 # calculate the distance between the player and the destination
            total_time = distance / self.speed # calculate the total time to reach the destination with constant speed
            self.x_speed = abs(self.dx - self.x) / total_time # calculate the x speed to have a constant speed while moving on x and y axis
    
    
    # Function to initialize the player's movement, calculate y = a*x + b to have a linear movement
    def init_movement(self):
        if abs(self.x - self.dx) < 1 :
            self.x = self.dx
            self.x_speed = self.speed
            self.y_speed = self.speed
            return 0    # to stop the function to prevent division by 0, only y movement will be done
        else :
            self.y_speed = 0    # having no speed at y will allow to have a linear movement with y = a*x + b equation
        if abs(self.y - self.dy) < 0.5 : # if the player is close enough to the destination, he will directly go to it preventing weird movement
            self.y = self.dy
        if self.x != self.dx and self.y != self.dy:
            if self.x < self.dx:
                self.a = (self.dy - self.y) / (self.dx - self.x) # calculate a for the linear movement
            else :
                self.a = (self.y - self.dy) / (self.x - self.dx) # calculate a for the linear movement
            self.b = self.y - self.a * self.x # calculate b for the linear movement
            self.define_x_speed()
        else :
            if self.x != self.dx: # if the player only moves on x axis
                self.x_speed = self.speed
                self.y_speed = 0
            elif self.y != self.dy: # if the player only moves on y axis
                self.y_speed = self.speed
                self.x_speed = 0
    
    # Function to check the player's facing direction, flip the sprite if necessary
    def check_facing(self):
        if abs(self.x - self.dx) > 10 or abs(self.y - self.dy) > 10: # prevent changing direction if the player is close to the destination, to avoid weird sprites flipping
            if self.x < self.dx:
                self.facing = "right"
                self.current_sprite = self.run
            else:
                self.facing = "left"
                self.current_sprite = pygame.transform.flip(self.run, True, False)
            self.animation_speed = 50
            self.state = "run"
        
    # Function to manage the player's animation
    def animation (self, time):
        self.animation_time += time
        self.selected_sprite_animation_time += time

        if self.animation_time > self.animation_speed: # timer of character animation
            if self.animation_x + self.offsetx < self.current_sprite.get_width():
                self.animation_x += self.offsetx
            else:
                self.animation_x = 0
            self.animation_time = 0

        if self.selected_sprite_animation_time > self.selected_sprite_animation_speed and self.is_selected: # timer of the selection animation
            if self.selected_sprite_x + self.selected_sprite_offsetx + 5 < self.selected_sprite.get_width():
                self.selected_sprite_x += self.selected_sprite_offsetx
            else:
                self.selected_sprite_x = 0
            self.selected_sprite_animation_time = 0
    
    # Function to display the player
    def display(self, screen):
        
        if self.is_selected: # display the selection sprite if the player is selected
            x = self.x - self.selected_sprite_offsetx / 2
            y = self.y - self.selected_sprite_offsety / 2
            x2 = self.selected_sprite_x
            y2 = self.selected_sprite_y
            width = self.selected_sprite_offsetx
            height = self.selected_sprite_offsety
            screen.blit(self.selected_sprite, (x, y), (x2, y2, width, height))
        screen.blit(self.current_sprite, (self.x - self.offsetx / 2, self.y - self.current_sprite.get_height()), (self.animation_x, self.animation_y, self.offsetx, self.offsety))

    # Function to take damage
    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.disappear()


    def disappear(self):
        # Logic to make the player disappear
        print("Player has disappeared.")


# Function to initialize the warrior class as character
def init_warrior(screen):
    size_ratio = 1
    aninmated_sprites_list = load_sprites(r"C:\Users\simon\Desktop\personal_project\RPG_basics\sprites\characters\Swordsman", size_ratio, size_ratio)
    selection_sprite = load_sprites(r"C:\Users\simon\Desktop\personal_project\RPG_basics\sprites\UI\selection_character", 1, 1)

    warrior = PlayerClass(screen.get_width() / 2, screen.get_height() / 2)
    warrior.idle = aninmated_sprites_list[5]
    warrior.idle2 = aninmated_sprites_list[6]
    warrior.jump = aninmated_sprites_list[7]
    warrior.walk = aninmated_sprites_list[9]
    warrior.run = aninmated_sprites_list[8]
    warrior.attack = aninmated_sprites_list[0]
    warrior.attack2 = aninmated_sprites_list[1]
    warrior.attack3 = aninmated_sprites_list[2]
    warrior.hurt = aninmated_sprites_list[4]
    warrior.die = aninmated_sprites_list[3]
    warrior.current_sprite = warrior.idle
    warrior.offsetx = 128 * size_ratio
    warrior.offsety = 128 * size_ratio
    warrior.hitbox = pygame.Rect(warrior.x - warrior.offsetx / 4.3, warrior.y - warrior.current_sprite.get_height() / 1.7, warrior.offsetx / 2, warrior.offsety / 1.6)
    warrior.colhitbox = pygame.Rect(warrior.x - warrior.offsetx / 14, warrior.y - warrior.current_sprite.get_height() / 14, warrior.offsetx / 5, warrior.offsety / 12)
    warrior.selected_sprite = selection_sprite[0]
    warrior.selected_sprite_offsetx = 2644/21
    warrior.selected_sprite_offsety = 60
    warrior.selected_sprite_animation_speed = 35
    return warrior