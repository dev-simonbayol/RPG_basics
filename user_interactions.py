import pygame

class user_interaction:
    def __init__(self):
        self.selected_obj = []
        self.area = None
        self.click = False
        self.drawable_area = None
        self.save_x = 0
        self.save_y = 0
        self.draw_invisible_area = False
        
    def get_area(self, view):
        area = pygame.Rect(self.area.x - view.x, self.area.y - view.y, self.area.width, self.area.height)
        return area
        