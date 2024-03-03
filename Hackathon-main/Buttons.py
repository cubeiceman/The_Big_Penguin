import pygame


class Button:
    def __init__(self, x, y, w, h, base_color, hover_color, pressed_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.colors_list = [base_color, hover_color, pressed_color]
        self.color_pick = 0  # pick a color based on what's happening
        # 0: mouse is not touching color box
        # 1: mouse is hovering over color box
        # 2: mouse is holding down over color box

    def change_color(self, button_status):
        if button_status == "off":
            self.color_pick = 0
        elif button_status == "hover":
            self.color_pick = 1
        elif button_status == "holding":
            self.color_pick = 2

    def draw(self, win):
        pygame.draw.rect(win, self.colors_list[self.color_pick], self.rect)


class Generate_Button(Button):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, (34, 139, 34), (0, 128, 0), (0, 100, 0))
