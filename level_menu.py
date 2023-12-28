import pygame, sys
from pygame.mouse import get_pos as mouse_pos

from settings import *
from support import *

class Level_menu:
    def __init__(self, switch):
        self.display_surface = pygame.display.get_surface()
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
        self.display_surface.fill(SKY_COLOR)
        self.buttons.display()

    def menu_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.buttons.mm_rect.collidepoint(
                mouse_pos()) and self.switch_locker == True:
            self.switch_locker = False
            self.switch({'from': 'level_menu', 'to': 'main_menu'})
            # self.bg_music.stop()


class Buttons:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.create_buttons()


    def create_buttons(self):
        # back to main menu
        mm_size = 45
        mm_margin = 6
        mm_topleft = (WINDOW_WIDTH - mm_size - mm_margin, mm_margin)
        self.mm_rect = pygame.Rect(mm_topleft, (mm_size, mm_size))

        # button areas
        size = 240
        self.level1_button_rect = pygame.Rect((64, 320), (size, size))
        self.level2_button_rect = pygame.Rect((size + 64 * 2, 160), (size, size))
        self.level3_button_rect = pygame.Rect((size * 2 + 64 * 3, 320), (size, size))
        self.level4_button_rect = pygame.Rect((size * 3 + 64 * 4, 160), (size, size))


    def display(self):
        pygame.draw.rect(self.display_surface, 'red', self.mm_rect)
        pygame.draw.rect(self.display_surface, 'red', self.level1_button_rect)
        pygame.draw.rect(self.display_surface, 'red', self.level2_button_rect)
        pygame.draw.rect(self.display_surface, 'red', self.level3_button_rect)
        pygame.draw.rect(self.display_surface, 'red', self.level4_button_rect)