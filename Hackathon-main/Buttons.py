import pygame

class Button:
    def __init__(self, x, y, w, h, image):
        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (w, h))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def draw_loc(self, surface, loc):
        surface.blit(self.image, self.image.get_rect(center=loc))
    
    def check_hover(self, mouse_pos):
        if self.rect.collidepoint(*mouse_pos):
            return True
        return False

    def check_click(self, mouse_pos, mouse_click):
        if self.check_hover(mouse_pos) and mouse_click:
            return True
        return False