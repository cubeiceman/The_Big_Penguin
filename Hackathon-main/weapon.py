import pygame

class Weapon:
    def __init__(self, name:str, strength:int, image_loc:str):
        self.name = name
        self.strength = strength
        self.image = pygame.image.load(image_loc)
        self.image = pygame.transform.scale(self.image, (500, 500))
        self.small_img = pygame.transform.scale(self.image, (200, 200))
    
    def __str__(self):
        return f"{self.name}, Strength: {self.strength}"

    def return_name(self):
        return self.name
    
    def return_strength(self):
        return self.strength
    
    def draw(self, surface:pygame.Surface, loc:tuple, font:pygame.font.FontType):
        image_rect = self.image.get_rect(center=loc)
        pygame.draw.rect(surface, (255, 255, 255), (image_rect.left-25, image_rect.top-25, image_rect.width+50, image_rect.height+200), border_radius = 7)
        surface.blit(self.image, self.image.get_rect(center=loc))
        name = font.render(self.name, True,(200, 200, 200))
        surface.blit(name, name.get_rect(center=(loc[0], loc[1]-200)))
        strength = font.render(f"Strength: {self.strength}", True, (200, 200, 200))
        surface.blit(strength, strength.get_rect(center=(loc[0], loc[1]+300)))
    
    def inventory_disp(self, surface, loc, font):
        image_rect = self.small_img.get_rect(center=loc)
        strength = font.render(str(self.strength), True, (200, 200, 200))
        pygame.draw.rect(surface, (255, 255, 255), self.small_img.get_rect(center=loc), border_radius = 5)
        surface.blit(self.small_img, self.small_img.get_rect(center=loc))
        surface.blit(strength, strength.get_rect(bottomright=image_rect.bottomright))