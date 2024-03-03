import pygame
from pygame.locals import *
import time
import Buttons
import Functions
from gacha import gacha

pygame.init()

WIDTH, HEIGHT = 500, 500
window = pygame.display.set_mode([WIDTH, HEIGHT], RESIZABLE)
c = pygame.time.Clock()
WHITE = (255, 255, 255)

before_time = time.time()

gen_button = Buttons.Generate_Button(50, 50, 300, 200)

clicked = False
run = True
while run:
    clicked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True

    after_time = time.time()
    delta_time = after_time - before_time
    before_time = after_time

    mx, my = pygame.mouse.get_pos()
    hovering = Functions.in_rect([mx, my], gen_button)
    if hovering and clicked:
        gen_button.change_color("holding")
        print(gacha())
    elif hovering and not clicked:
        gen_button.change_color("hover")
    else:
        gen_button.change_color("off")

    window.fill(WHITE)

    gen_button.draw(window)

    pygame.display.flip()
    c.tick(5)
