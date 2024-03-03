from lib2to3.pgen2 import token
from xml.dom.pulldom import parseString
import pygame
from pygame.locals import *
from Buttons import Button
from gacha import gacha
from weapon import Weapon
import time

pygame.init()
# ----- CLASSES -----#
class Scene:
    def __init__(self, width, height, image):
        self.width, self.height = width, height
        self.bg = image
        self.surface = pygame.Surface((width, height))
        self.active = True

    def add(self, value):
        # add some key and value to a determined dictionary inside the scene(game or menu)
        pass

    def handle_keyboard(self, text_box, keys, shift_keys, bar):
        # handles the keyboard, in this case, the quit button and the mouse clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.active = False
                
            if event.type == pygame.KEYDOWN:
                keys_state = pygame.key.get_pressed()
                if event.key == pygame.K_RETURN:
                    try:
                        chars = return_words(text_box.text)
                        text_box.text = ""
                        bar.add(chars)
                    except FileNotFoundError:
                        pass
                if event.key == pygame.K_BACKSPACE:
                    text_box.text = text_box.text[:-1]
                try:
                    if keys_state[event.key] and (keys_state[pygame.K_RSHIFT] or keys_state[pygame.K_LSHIFT]):
                        text_box.add(shift_keys[event.key])
                    else:
                        text_box.add(keys[event.key])
                except KeyError:
                    pass

    def draw(self):
        # draws things onto the scene's surface, which is later drawn on the actual window
        pass


class Game_Scene(Scene):
    def __init__(self, width, height, image):
        super().__init__(width, height, image)
        self.active = True
        self.text_list = []
        self.text_box = None
        self.bar = None

    def add_text(self, value):
        self.text_list.append(value)

    def set_progress_bar(self, bar):
        self.bar = bar

    def set_text_box(self, val):
        self.text_box = val

    def draw(self):
        self.surface.blit(self.bg, (0, 0))
        self.text_box.draw(self.surface)
        self.bar.draw(self.surface)
        for text in self.text_list:
            text.draw(self.surface)

class Progress_Bar:
    def __init__(self, w, h, sx, sy):
        self.progress = 0
        self.max_bar_width = w

        self.max_bar_height = h
        self.max_chars = 1000
        self.current_chars = 0
        self.scale = self.progress / self.max_chars
        self.surface = pygame.Surface((self.max_bar_width, self.max_bar_height))
        self.rect = pygame.Rect(0, 0, w * self.scale, self.max_bar_height)
        self.bg_color = (0, 0, 0)
        self.color = (0, 255, 0)
        self.multiplier = 0
        self.surface_x = sx
        self.surface_y = sy

        # this draws the greenbar

    def draw(self, surface):
        self.surface.fill(self.bg_color)
        pygame.draw.rect(self.surface, self.color, self.rect)
        surface.blit(self.surface, (self.surface_x, self.surface_y))

    # this reads the charcount from notes and adds to the progress bar
    def add(self, char_count):
        self.progress += char_count
        self.scale = self.progress / self.max_chars
        while self.progress > self.max_chars:
            self.rect.width -= self.max_bar_width
            self.progress = 0
            self.multiplier += 1
        self.rect.width = self.max_bar_width * self.scale

class Text_Box:
    def __init__(self, x, y, w, h, f, c, bgc, text=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = f
        self.color = c
        self.bg_color = bgc
        self.can_add = True

    def draw(self, surface):
        text_show = self.font.render(self.text, False, self.color)
        pygame.draw.rect(surface, self.bg_color, self.rect)
        surface.blit(text_show, (self.rect.x, self.rect.y))


class File_Box(Text_Box):
    def add(self, letter):
        if self.can_add:
            self.text += letter
        if len(self.text) > 200:
            self.can_add = False
        else:
            self.can_add = True

    def draw(self, surface):
        text_show = self.font.render(self.text, False, self.color)
        cursor_rect = pygame.Rect(self.rect.x + text_show.get_width(), self.rect.y, 5, text_show.get_height())

        pygame.draw.rect(surface, self.bg_color, self.rect)
        if time.time() % 1 > 0.5:
            pygame.draw.rect(surface, self.color, cursor_rect)
        surface.blit(text_show, (self.rect.x, self.rect.y))

# ----- FUNCTIONS ----- #
def return_words(file_name):
    with open("notes/"+file_name, "r") as file:
        content = file.read()
        len = 0
        for character in content:
            if character != " ":
                len += 1
        return len


def check_user_input(scene, text_box, keys, shift_keys, bar):
    scene.handle_keyboard(text_box, keys, shift_keys, bar)


def draw_scene(scene, win):
    scene.draw()
    win.blit(scene.surface, (0, 0))
    pygame.display.flip()

# ----- VARIABLES ----- #

keys = {pygame.K_a: "a", pygame.K_b: "b", pygame.K_c: "c", pygame.K_d: "d", pygame.K_e: "e", pygame.K_f: "f",
        pygame.K_g: "g", pygame.K_h: "h", pygame.K_i: "i", pygame.K_j: "j", pygame.K_k: "k", pygame.K_l: "l", pygame.K_m: "m",
        pygame.K_n: "n", pygame.K_o: "o", pygame.K_p: "p", pygame.K_q: "q", pygame.K_r: "r", pygame.K_s: "s", pygame.K_t: "t",
        pygame.K_u: "u", pygame.K_v: "v", pygame.K_w: "w", pygame.K_x: "x", pygame.K_y: "y", pygame.K_z: "z", pygame.K_SLASH: "/",
        pygame.K_BACKSLASH: "\\", pygame.K_SPACE: " ", pygame.K_SEMICOLON: "; ", pygame.K_KP_MINUS: "-",
        pygame.K_0: "0", pygame.K_1: "1", pygame.K_2: "2", pygame.K_3: "3", pygame.K_4: "4", pygame.K_5: "5", pygame.K_6: "6",
        pygame.K_7: "7", pygame.K_8: "8", pygame.K_9: "9", pygame.K_LEFTBRACKET: "[", pygame.K_RIGHTBRACKET: "]", pygame.K_PERIOD: "."}

keys_shift = {pygame.K_a: "A", pygame.K_b: "B", pygame.K_c: "C", pygame.K_d: "D", pygame.K_e: "E", pygame.K_f: "F",
              pygame.K_g: "G", pygame.K_h: "H", pygame.K_i: "I", pygame.K_j: "J", pygame.K_k: "K", pygame.K_l: "L",
              pygame.K_m: "M", pygame.K_n: "N", pygame.K_o: "O", pygame.K_p: "P", pygame.K_q: "Q", pygame.K_r: "R",
              pygame.K_s: "S", pygame.K_t: "T", pygame.K_u: "U", pygame.K_v: "V", pygame.K_w: "W", pygame.K_x: "X",
              pygame.K_y: "Y", pygame.K_z: "Z", pygame.K_SEMICOLON: ":", pygame.K_UNDERSCORE: "_", pygame.K_SPACE: " ",
              pygame.K_0: ")", pygame.K_1: "!", pygame.K_2: "@", pygame.K_3: "#", pygame.K_4: "$", pygame.K_5: "%",
              pygame.K_6: "^", pygame.K_7: "&", pygame.K_8: "*", pygame.K_9: "("}


total_words = 0
num_tokens = 0
scene_name = "home"
owned_weapons = []
equipped_weapons = []
level = 1

background_dir = "images/background/"
buttons_dir = "images/buttons/"
weapons_dir = "images/weapons/"
other_dir = "images/other/"

# items dictionary with Weapon a_weapon : integer probability
items = {
    Weapon("Normal Sword", 5, weapons_dir+"normal_sword.png"):30,
    Weapon("Banana Duckler", 10, weapons_dir+"banana_duckler.png"):30,
    Weapon("Big Penguin's Beak", 50, weapons_dir+"big_penguins_beak.png"):2,
    Weapon("Bloodthirtser", 25, weapons_dir+"bloodthirster.png"):5,
    Weapon("Emerald Spear", 20, weapons_dir+"emerald_spear.png"):5,
    Weapon("Ghostblade", 30, weapons_dir+"ghostblade.png"):5,
    Weapon("Penguin Slayer", 55, weapons_dir+"penguin_slayer.png"):1,
    Weapon("Rageblade", 40, weapons_dir+"rageblade.png"):5,
    Weapon("Ruby", 15, weapons_dir+"ruby.png"):20,
    Weapon("Tanghulu", 30, weapons_dir+"tanghulu.png"):3,
    Weapon("Throngler", 60, weapons_dir+"throngler.png"):1,
}

pygame.font.init()
default_font = pygame.font.Font("MadimiOne-Regular.ttf", 50)
big_font = pygame.font.Font("MadimiOne-Regular.ttf", 200)
med_font = pygame.font.Font("MadimiOne-Regular.ttf", 100)
small_font = pygame.font.Font("MadimiOne-Regular.ttf", 25)
text_font = pygame.font.Font("MadimiOne-Regular.ttf", 25)

equipped_text = default_font.render("EQUIPPED WEAPONS", True, (250, 250, 250))
owned_text = default_font.render("OWNED WEAPONS", True, (250, 250, 250))

title_the = med_font.render("The", True, (0, 0, 0))
title_big = big_font.render("BIG", True, (59, 144, 209))
title_penguin = med_font.render("PENGUIN", True, (200, 200, 255))

# ----- MAIN ----- #


WIDTH, HEIGHT = (1600, 900)
HEIGHT -= 80
window = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("The Big Penguin")
c = pygame.time.Clock()
WHITE = (255, 255, 255)
GREY = (75, 75, 75)

home_bg = pygame.image.load(background_dir+"bg placeholder.png")
home_bg = pygame.transform.scale(home_bg, (WIDTH, HEIGHT))

fight_bg = pygame.image.load(background_dir+"fight_bg.png")
fight_bg = pygame.transform.scale(fight_bg, (WIDTH, HEIGHT))

inventory_bg = pygame.image.load(background_dir+"bg placeholder.png")
inventory_bg = pygame.transform.scale(inventory_bg, (WIDTH, HEIGHT))

notes_bg = pygame.image.load(background_dir+"bg placeholder.png")
notes_bg = pygame.transform.scale(notes_bg, (WIDTH, HEIGHT))

gacha_bg = pygame.image.load(background_dir+"bg placeholder.png")
gacha_bg = pygame.transform.scale(gacha_bg, (WIDTH, HEIGHT))

chest_img = pygame.image.load(other_dir+"chest.png")
chest_img = pygame.transform.scale(chest_img, (400, 500))


fight_button = Button(100, 650, 100, 100, buttons_dir+"fight.png")
inventory_button = Button(300, 650, 100, 100, buttons_dir+"inventory.png")
notes_button = Button(500, 650, 100, 100, buttons_dir+"notes.png")
gacha_button = Button(700, 650, 100, 100, buttons_dir+"gacha.png")
home_button = Button(20, 20, 100, 100, buttons_dir+"home.png")

fight_button2 = Button(*(WIDTH//2-50, 675), 100, 100, buttons_dir+"fight.png")

penguin_img = pygame.image.load(other_dir+"penguin.png").convert_alpha()
penguin_img = pygame.transform.scale(penguin_img, (500, 500))

user_img = pygame.image.load(other_dir+"user.png").convert_alpha()
user_img = pygame.transform.scale(user_img, (300, 300))

boss_img = pygame.image.load(other_dir+"boss.png").convert_alpha()
boss_img = pygame.transform.scale(boss_img, (300, 300))

token_img = pygame.image.load(buttons_dir+"token.png")
token_img = pygame.transform.scale(token_img, (100, 100))

import_text_box = File_Box(WIDTH * (1 / 20), HEIGHT * (8 / 20), WIDTH * (8 / 20), HEIGHT * (1 / 20), text_font,
                           (0, 0, 0),
                           (255, 255, 255))
progress_bar = Progress_Bar(WIDTH * (17 / 20), HEIGHT * (2 / 20), WIDTH * (2 / 20), HEIGHT * (1 / 20))
progress_text = Text_Box(WIDTH * (1 / 20), HEIGHT * (15 / 20), WIDTH * (18 / 20), HEIGHT * (1 / 20), text_font,
                         (0, 0, 0),
                         (255, 255, 255), text="Fill this bar full to get tokens! You can input a file directory "
                                               "for this program to grade your notes.")
progress_text2 = Text_Box(WIDTH * (1 / 20), (HEIGHT * (15 / 20)) + 40, WIDTH * (18 / 20), HEIGHT * (1 / 20),
                          text_font, (0, 0, 0), (255, 255, 255), text="Then you will fill the progress bar and "
                                                                      "earn tokens based on how well you did!")
progress_text3 = Text_Box(WIDTH * (1/20), (HEIGHT * (15/20))+80, WIDTH * (18/20), HEIGHT * (1/20), text_font, (0, 0, 0),
                          (255, 255, 255), text="Press enter to submit your file.")

game_scene = Game_Scene(WIDTH, HEIGHT, notes_bg)
game_scene.text_box = import_text_box
game_scene.bar = progress_bar
game_scene.add_text(progress_text)
game_scene.add_text(progress_text2)
game_scene.add_text(progress_text3)

def game_loop(scene, win, keys, shift_keys, bar):
    check_user_input(scene, import_text_box, keys, shift_keys, bar)
    draw_scene(scene, win)
    mouse_pos1 = pygame.mouse.get_pos()
    mouse_click = False
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = True
    home_button.draw(window)
    if home_button.check_click(mouse_pos1, mouse_click):
        # game scene = false
        game_scene.active = False


run = True
frame_num = 0

while run:
    clicked = False
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
    
    match scene_name:
        case "home":
            window.blit(home_bg, (0, 0))

            # draw title
            pygame.draw.rect(window, (255, 255, 255), (100, 150, 650, 450), border_radius=20)
            window.blit(title_the, (200, 200))
            window.blit(title_big, (225, 225))
            window.blit(title_penguin, (270, 400))

            window.blit(penguin_img, penguin_img.get_rect(center=(1200,HEIGHT//2)))
            # display progress bar

            gacha_button.draw(window)
            if gacha_button.check_click(mouse_pos, clicked):
                scene_name = "gacha"
                frame_num = 0

            fight_button.draw(window)
            if fight_button.check_click(mouse_pos, clicked):
                scene_name = "fight"
                frame_num = 0
            
            notes_button.draw(window)
            if notes_button.check_click(mouse_pos, clicked):
                scene_name = "notes"
                frame_num = 0
            
            inventory_button.draw(window)
            if inventory_button.check_click(mouse_pos, clicked):
                scene_name = "inventory"
                frame_num = 0

        case "fight":
            if frame_num == 1:
                user_pos = (100, 400)
                boss_pos = (1200, 400)
                level_disp = big_font.render(f"LEVEL {level}", True, (255, 255, 255))
            
            window.blit(fight_bg, (0, 0))
            window.blit(level_disp, level_disp.get_rect(center=(WIDTH//2, 100)))
            fight_button2.draw(window)

            if fight_button2.check_click(mouse_pos, clicked):
                # compare fighting powers
                user_power = 0
                for weapon in equipped_weapons:
                    user_power += weapon.return_strength()
                boss_power = 5 + 10 * level

                if user_power >= boss_power:
                    win = True
                else:
                    win = False
                # if winnable -> win animation
                # if lose -> lose animation
                scene_name = "animation"
                frame_num = 0
            window.blit(user_img, user_pos)
            window.blit(boss_img, boss_pos)
            home_button.draw(window)
            if home_button.check_click(mouse_pos, clicked):
                scene_name = "home"
                frame_num = 0

        case "animation":
            if frame_num == 1:
                a_frame = 0
                user_pos = (100, 400)
                boss_pos = (1200, 400)
            
            window.blit(fight_bg, (0, 0))
            window.blit(user_img, user_pos)
            window.blit(boss_img, boss_pos)
            
            if a_frame < 24:
                user_pos = (user_pos[0]+20, 400)
                boss_pos = (boss_pos[0]-20, 400)
            else:
                if win:
                    user_pos = (user_pos[0]-10*((150-a_frame)/150), 400)
                    boss_pos = (boss_pos[0]+30, 400)
                else:
                    user_pos = (user_pos[0]-30, 400)
                    boss_pos = (boss_pos[0]+10*((150-a_frame)/150), 400)
            a_frame += 1

            if a_frame == 180:
                if win:
                    level += 1
                scene_name = "home"
                frame_num = 0
        
        case "inventory":
            if frame_num == 1:
                if len(owned_weapons) <= 5:
                    equipped_weapons = owned_weapons.copy()
                
                print(owned_weapons)
                print(equipped_weapons)

            # equip weapons
            #window.blit(inventory_bg, (0, 0))
            window.fill((209, 117, 100))

            window.blit(equipped_text, equipped_text.get_rect(center=(WIDTH//2, 100)))
            window.blit(owned_text, owned_text.get_rect(center=(WIDTH//2, 475)))

            # equipped item display
            for i in range(5):
                location_x = 75 + 300*i + 125
                location_y = 275
                pygame.draw.rect(window, (128, 128, 128), (location_x-125, location_y-125, 250, 250))
                if i<len(equipped_weapons):
                    equipped_weapons[i].inventory_disp(window, (location_x, location_y), small_font)

            # owned item display
            for i in range(10):
                location_x = 75 + 300 * i + 125
                location_y = 650
                pygame.draw.rect(window, (128, 128, 128), (location_x-125, location_y-125, 250, 250))
                if i<len(owned_weapons):
                    owned_weapons[i].inventory_disp(window, (location_x, location_y), small_font)
            pygame.draw.rect(window, (209, 117, 100), (0, 525, 75, 375))
            pygame.draw.rect(window, (209, 117, 100), (1525, 525, 75, 375))
            
            home_button.draw(window)
            if home_button.check_click(mouse_pos, clicked):
                scene_name = "home"
                frame_num = 0

        case "notes":
            game_scene.active = True
            
            window.blit(notes_bg, (0, 0))
            # take notes, get points
            while game_scene.active:
                game_loop(game_scene, window, keys, keys_shift, progress_bar)

                pygame.display.flip()
                c.tick(60)
            scene_name = "home"
            frame_num = 0

        case "gacha":
            if frame_num == 1:
                if num_tokens > 0:
                    can_roll = True
                else:
                    can_roll = False
                display_item = False
                rolled_item = None
                display_frame = 0
                token_disp = default_font.render(str(num_tokens), True, (255, 255, 255))
            
            window.blit(gacha_bg, (0, 0))

            window.blit(token_img, (650, 100))
            window.blit(token_disp, (800, 110))

            if can_roll:
                window.blit(chest_img, chest_img.get_rect(center = (WIDTH//2, HEIGHT//2)))

                if clicked and chest_img.get_rect(center = (WIDTH//2, HEIGHT//2)).collidepoint(*mouse_pos):
                    rolled_item = gacha(items)
                    if rolled_item not in owned_weapons:
                        owned_weapons.append(rolled_item)
                    num_tokens -= 1
                    display_item = True

                    if num_tokens > 0:
                        can_roll = True
                    else:
                        can_roll = False
                    token_disp = default_font.render(str(num_tokens), True, (255, 255, 255))

            else:
                pass
                
            if display_item and rolled_item is not None:
                rolled_item.draw(window, (WIDTH//2, HEIGHT//2-50), default_font)
                display_frame += 1
                if display_frame == 100:
                    display_item = False
                    display_frame = 0
            
            home_button.draw(window)
            if home_button.check_click(mouse_pos, clicked):
                scene_name = "home"
                frame_num = 0

    frame_num+=1
    pygame.display.flip()

    c.tick(60)

