import pygame, sys
from pygame.mouse import get_pos as mouse_pos
from pygame.image import load

from settings import *
from support import *

class Save_menu:
    def __init__(self, switch):
        self.display_surface = pygame.display.get_surface()
        self.image_background = load(path.join(script_directory, 'graphics', 'menus', 'save_menu', 'background.png')).convert_alpha()
        self.image_background = pygame.transform.scale(self.image_background, (1280, 720))
        self.switch = switch
        self.buttons = Buttons()
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

    def menu_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.buttons.mm_rect.collidepoint(
                mouse_pos()) and self.switch_locker == True:
            self.switch_locker = False
            self.switch({'from': 'save_menu', 'to': 'main_menu'})
            # self.bg_music.stop()


class Buttons:
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
        width = 300
        height = 200
        self.level1_save_button_rect = pygame.Rect((150, 135), (width, height))
        self.level2_save_button_rect = pygame.Rect((width + 190, 135), (width, height))
        self.level3_save_button_rect = pygame.Rect((width * 2 + 230, 135), (width, height))

        self.level4_save_button_rect = pygame.Rect((150, height + 175), (width, height))
        self.level5_save_button_rect = pygame.Rect((width + 190, height + 175), (width, height))
        self.level6_save_button_rect = pygame.Rect((width * 2 + 230, height + 175), (width, height))

        self.image_save_button = load(path.join(script_directory, 'graphics', 'menus', 'save_menu', 'save_button.png')).convert_alpha()
        self.image_save_button = pygame.transform.scale(self.image_save_button, (300, 200))


    def display(self):
        self.display_surface.blit(self.image, self.mm_rect.topleft)
        self.display_surface.blit(self.image_save_button, self.level1_save_button_rect.topleft)
        self.display_surface.blit(self.image_save_button, self.level2_save_button_rect.topleft)
        self.display_surface.blit(self.image_save_button, self.level3_save_button_rect.topleft)
        self.display_surface.blit(self.image_save_button, self.level4_save_button_rect.topleft)
        self.display_surface.blit(self.image_save_button, self.level5_save_button_rect.topleft)
        self.display_surface.blit(self.image_save_button, self.level6_save_button_rect.topleft)

        # pygame.draw.rect(self.display_surface, 'red', self.level1_save_button_rect)
        # pygame.draw.rect(self.display_surface, 'red', self.level2_save_button_rect)
        # pygame.draw.rect(self.display_surface, 'red', self.level3_save_button_rect)
        # pygame.draw.rect(self.display_surface, 'red', self.level4_save_button_rect)
        # pygame.draw.rect(self.display_surface, 'red', self.level5_save_button_rect)
        # pygame.draw.rect(self.display_surface, 'red', self.level6_save_button_rect)