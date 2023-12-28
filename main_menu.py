import pygame, sys
from pygame.mouse import get_pos as mouse_pos
from pygame.math import Vector2 as vector
from pygame.image import load

from settings import *
from support import *

class Main_menu:
    def __init__(self, switch):
        self.display_surface = pygame.display.get_surface()
        self.image_background = load(path.join(script_directory, 'graphics', 'menus', 'main_menu', 'background.png')).convert_alpha()
        self.image_background = pygame.transform.scale(self.image_background, (1280, 720))
        self.switch = switch
        self.buttons = Buttons()
        self.switch_locker = True
        self.image_tittle = load(path.join(script_directory, 'graphics', 'menus', 'main_menu', 'tittle.png')).convert_alpha()
        self.image_tittle = pygame.transform.scale(self.image_tittle, (540, 180))
        self.tittle = pygame.Rect((WINDOW_WIDTH / 2 - 540 / 2, 80), (540, 180))

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
        self.display_surface.blit(self.image_tittle, self.tittle)

    def menu_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.buttons.editor_button_rect.collidepoint(
                mouse_pos()) and self.switch_locker == True:
            self.switch_locker = False
            self.switch({'from': 'main_menu', 'to': 'editor'})
        if event.type == pygame.MOUSEBUTTONDOWN and self.buttons.play_button_rect.collidepoint(
                mouse_pos()) and self.switch_locker == True:
            self.switch_locker = False
            self.switch({'from': 'main_menu', 'to': 'level_menu'})
        if event.type == pygame.MOUSEBUTTONDOWN and self.buttons.saved_button_rect.collidepoint(
                mouse_pos()) and self.switch_locker == True:
            self.switch_locker = False
            self.switch({'from': 'main_menu', 'to': 'save_menu'})
        if event.type == pygame.MOUSEBUTTONDOWN and self.buttons.exit_button_rect.collidepoint(
                mouse_pos()) and self.switch_locker == True:
            pygame.quit()
            sys.exit()

class Buttons:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.create_buttons()


    def create_buttons(self):
        script_directory = path.dirname(path.realpath(__file__))
        # menu area
        width = 360
        height = 360
        topleft = (WINDOW_WIDTH / 2 - width / 2, WINDOW_HEIGHT / 2 - height / 2 + 100)
        self.image = load(path.join(script_directory, 'graphics', 'menus', 'main_menu', 'buttons_back.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        # self.rect = self.image.get_rect(topleft = topleft)
        self.rect = pygame.Rect(topleft, (width, height))



        # button areas
        self.play_button_rect = pygame.Rect(vector(self.rect.topleft) + (25, 25), (self.rect.width - 50, self.rect.height / 4 - 20))
        self.image_play_button = load(path.join(script_directory, 'graphics', 'menus', 'main_menu', 'play_button.png')).convert_alpha()
        self.image_play_button = pygame.transform.scale(self.image_play_button, (310, 70))
        self.editor_button_rect = pygame.Rect(vector(self.rect.topleft) + (25, 105), (self.rect.width - 50, self.rect.height / 4 - 20))
        self.image_editor_button = load(path.join(script_directory, 'graphics', 'menus', 'main_menu', 'editor_button.png')).convert_alpha()
        self.image_editor_button = pygame.transform.scale(self.image_editor_button, (310, 70))
        self.saved_button_rect = pygame.Rect(vector(self.rect.topleft) + (25, 185), (self.rect.width - 50, self.rect.height / 4 - 20))
        self.image_saved_button = load(path.join(script_directory, 'graphics', 'menus', 'main_menu', 'load_button.png')).convert_alpha()
        self.image_saved_button = pygame.transform.scale(self.image_saved_button, (310, 70))
        self.exit_button_rect = pygame.Rect(vector(self.rect.topleft) + (25, 265), (self.rect.width - 50, self.rect.height / 4 - 20))
        self.image_exit_button = load(path.join(script_directory, 'graphics', 'menus', 'main_menu', 'quit_button.png')).convert_alpha()
        self.image_exit_button = pygame.transform.scale(self.image_exit_button, (310, 70))

    def display(self):
        self.display_surface.blit(self.image, self.rect.topleft)
        self.display_surface.blit(self.image_play_button, self.play_button_rect.topleft)
        self.display_surface.blit(self.image_editor_button, self.editor_button_rect.topleft)
        self.display_surface.blit(self.image_saved_button, self.saved_button_rect.topleft)
        self.display_surface.blit(self.image_exit_button, self.exit_button_rect.topleft)
        # pygame.draw.rect(self.display_surface, 'red', self.play_button_rect)
        # pygame.draw.rect(self.display_surface, 'red', self.editor_button_rect)
        # pygame.draw.rect(self.display_surface, 'red', self.saved_button_rect)
        # pygame.draw.rect(self.display_surface, 'red', self.exit_button_rect)
