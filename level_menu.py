import pygame, sys
from pygame.mouse import get_pos as mouse_pos
from pygame.image import load
import pickle

from settings import *
from support import *

class Level_menu:
    def __init__(self, switch):
        self.display_surface = pygame.display.get_surface()
        self.image_background = load(path.join(script_directory, 'graphics', 'menus', 'level_menu', 'background.png')).convert_alpha()
        self.image_background = pygame.transform.scale(self.image_background, (1280, 720))
        self.switch = switch
        self.buttons = Buttons_lm()
        self.switch_locker = True

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.menu_click(event)

    def run(self, dt):
        self.event_loop()
        self.display_surface.blit(self.image_background, (0, 0))
        self.buttons.display()

    def read_level(self, name):
        file_path = path.join(script_directory, 'levels', f'{name}.json')
        with open(file_path, 'rb') as file:
            grid = pickle.load(file)
        return grid

    def menu_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.buttons.mm_rect.collidepoint(
                mouse_pos()) and self.switch_locker == True:
            self.switch_locker = False
            self.switch({'from': 'level_menu', 'to': 'main_menu'})
        if event.type == pygame.MOUSEBUTTONDOWN and self.buttons.level1_button_rect.collidepoint(
                mouse_pos()) and self.switch_locker == True:
            self.switch_locker = False
            self.switch({'from': 'level_menu', 'to': 'level'}, self.read_level('level1'))
        elif event.type == pygame.MOUSEBUTTONDOWN and self.buttons.level2_button_rect.collidepoint(
                mouse_pos()) and self.switch_locker == True:
            self.switch_locker = False
            self.switch({'from': 'level_menu', 'to': 'level'}, self.read_level('level2'))
        elif event.type == pygame.MOUSEBUTTONDOWN and self.buttons.level3_button_rect.collidepoint(
                mouse_pos()) and self.switch_locker == True:
            self.switch_locker = False
            self.switch({'from': 'level_menu', 'to': 'level'}, self.read_level('level3'))
        elif event.type == pygame.MOUSEBUTTONDOWN and self.buttons.level4_button_rect.collidepoint(
                mouse_pos()) and self.switch_locker == True:
            self.switch_locker = False
            self.switch({'from': 'level_menu', 'to': 'level'}, self.read_level('level4'))


class Buttons_lm:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.create_buttons()


    def create_buttons(self):
        self.display_surface = pygame.display.get_surface()
        # back to main menu
        mm_size = 45
        mm_margin = 6
        mm_topleft = (WINDOW_WIDTH - mm_size - mm_margin, mm_margin)
        self.mm_rect = pygame.Rect(mm_topleft, (mm_size, mm_size))
        self.image = load(path.join(script_directory, 'graphics', 'menus', 'main_menu_button.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (mm_size, mm_size))

        # button areas
        size = 240
        self.level1_button_rect = pygame.Rect((64, 320), (size, size))
        self.image_level1_button = load(path.join(script_directory, 'graphics', 'menus', 'level_menu', 'level1_button.png')).convert_alpha()
        self.image_level1_button = pygame.transform.scale(self.image_level1_button, (240, 240))
        self.level2_button_rect = pygame.Rect((size + 64 * 2, 160), (size, size))
        self.image_level2_button = load(path.join(script_directory, 'graphics', 'menus', 'level_menu', 'level2_button.png')).convert_alpha()
        self.image_level2_button = pygame.transform.scale(self.image_level2_button, (240, 240))
        self.level3_button_rect = pygame.Rect((size * 2 + 64 * 3, 320), (size, size))
        self.image_level3_button = load( path.join(script_directory, 'graphics', 'menus', 'level_menu', 'level3_button.png')).convert_alpha()
        self.image_level3_button = pygame.transform.scale(self.image_level3_button, (240, 240))
        self.level4_button_rect = pygame.Rect((size * 3 + 64 * 4, 160), (size, size))
        self.image_level4_button = load(path.join(script_directory, 'graphics', 'menus', 'level_menu', 'level4_button.png')).convert_alpha()
        self.image_level4_button = pygame.transform.scale(self.image_level4_button, (240, 240))


    def display(self):
        self.display_surface.blit(self.image, self.mm_rect.topleft)
        self.display_surface.blit(self.image_level1_button, self.level1_button_rect.topleft)
        self.display_surface.blit(self.image_level2_button, self.level2_button_rect.topleft)
        self.display_surface.blit(self.image_level3_button, self.level3_button_rect.topleft)
        self.display_surface.blit(self.image_level4_button, self.level4_button_rect.topleft)
        # pygame.draw.rect(self.display_surface, 'red', self.level1_button_rect)
        # pygame.draw.rect(self.display_surface, 'red', self.level2_button_rect)
        # pygame.draw.rect(self.display_surface, 'red', self.level3_button_rect)
        # pygame.draw.rect(self.display_surface, 'red', self.level4_button_rect)