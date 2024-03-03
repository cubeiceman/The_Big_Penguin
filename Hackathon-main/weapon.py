import pygame

class Weapon:
    def __init__(self, name:str, strength:int, image_loc:str):
        self.name = name
        self.strength = strength
        self.image = pygame.image.load(image_loc)
    
    def __str__(self):
        return f"{self.name}, Strength: {self.strength}"

    def return_name(self):
        return self.name
    
    def return_strength(self):
        return self.strength
    
    def draw(self, surface:pygame.Surface, loc:tuple):
        surface.blit(self.image, loc)