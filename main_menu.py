import pygame, sys
from pygame.mouse import get_pos as mouse_pos
from pygame.math import Vector2 as vector

from settings import *
from support import *

class Main_menu:
    def __init__(self, switch):
        self.display_surface = pygame.display.get_surface()
        self.switch = switch
        self.buttons = Buttons()
        self.switch_locker = True
        self.tittle = pygame.Rect((WINDOW_WIDTH / 2 - 540 / 2, 80), (540, 180))

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.menu_click(event)

    def run(self, dt):
        self.event_loop()
        self.display_surface.fill(SKY_COLOR)
        self.buttons.display()
        pygame.draw.rect(self.display_surface, 'red', self.tittle)

    def menu_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.buttons.editor_button_rect.collidepoint(
                mouse_pos()) and self.switch_locker == True:
            self.switch_locker = False
            self.switch({'from': 'main_menu', 'to': 'editor'})
            print("to editor")
        if event.type == pygame.MOUSEBUTTONDOWN and self.buttons.play_button_rect.collidepoint(
                mouse_pos()) and self.switch_locker == True:
            self.switch_locker = False
            self.switch({'from': 'main_menu', 'to': 'level_menu'})
        if event.type == pygame.MOUSEBUTTONDOWN and self.buttons.saved_button_rect.collidepoint(
                mouse_pos()) and self.switch_locker == True:
            self.switch_locker = False
            self.switch({'from': 'main_menu', 'to': 'save_menu'})


class Buttons:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.create_buttons()


    def create_buttons(self):
        # menu area
        width = 360
        height = 360
        topleft = (WINDOW_WIDTH / 2 - width / 2, WINDOW_HEIGHT / 2 - height / 2 + 100)
        self.rect = pygame.Rect(topleft, (width, height))

        # button areas
        self.play_button_rect = pygame.Rect(vector(self.rect.topleft) + (25, 25), (self.rect.width - 50, self.rect.height / 4 - 20))
        self.editor_button_rect = pygame.Rect(vector(self.rect.topleft) + (25, 105), (self.rect.width - 50, self.rect.height / 4 - 20))
        self.saved_button_rect = pygame.Rect(vector(self.rect.topleft) + (25, 185), (self.rect.width - 50, self.rect.height / 4 - 20))
        self.exit_button_rect = pygame.Rect(vector(self.rect.topleft) + (25, 265), (self.rect.width - 50, self.rect.height / 4 - 20))

    def display(self):
        pygame.draw.rect(self.display_surface, 'white', self.rect)
        pygame.draw.rect(self.display_surface, 'red', self.play_button_rect)
        pygame.draw.rect(self.display_surface, 'red', self.editor_button_rect)
        pygame.draw.rect(self.display_surface, 'red', self.saved_button_rect)
        pygame.draw.rect(self.display_surface, 'red', self.exit_button_rect)
