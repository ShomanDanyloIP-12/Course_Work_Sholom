import pygame
from settings import *
from pygame.image import load
from pygame.math import Vector2 as vector

class Menu:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.create_data()
		self.create_buttons()

	def create_data(self):
		self.menu_surfs = {}
		for key, value in EDITOR_DATA.items():
			if value['menu']:
				if not value['menu'] in self.menu_surfs:
					self.menu_surfs[value['menu']] = [(key,load(value['menu_surf']))]
				else:
					self.menu_surfs[value['menu']].append((key,load(value['menu_surf'])))

	def create_buttons(self):
		# main_menu area
		mm_size = 45
		mm_margin = 6
		mm_topleft = (WINDOW_WIDTH - mm_size - mm_margin, mm_margin)
		self.mm_rect = pygame.Rect(mm_topleft, (mm_size, mm_size))
		self.image = load(path.join(script_directory, 'graphics', 'menus', 'main_menu_button.png')).convert_alpha()
		self.image = pygame.transform.scale(self.image, (mm_size, mm_size))
		self.sv_rect = pygame.Rect(vector(mm_topleft) - (mm_size + mm_margin, 0), (mm_size, mm_size))
		self.sv_image = load(path.join(script_directory, 'graphics', 'menus', 'save_button.png')).convert_alpha()
		self.sv_image = pygame.transform.scale(self.sv_image, (mm_size, mm_size))

		# menu area
		size = 180
		margin = 6
		topleft = (WINDOW_WIDTH - size - margin,WINDOW_HEIGHT - size - margin)
		self.rect = pygame.Rect(topleft,(size,size))

		# button areas
		generic_button_rect = pygame.Rect(self.rect.topleft, (self.rect.width / 2, self.rect.height / 2))
		button_margin = 5
		self.tile_button_rect = generic_button_rect.copy().inflate(-button_margin,-button_margin)
		self.coin_button_rect = generic_button_rect.move(self.rect.height / 2,0).inflate(-button_margin,-button_margin)
		self.enemy_button_rect = generic_button_rect.move(self.rect.height / 2,self.rect.width / 2).inflate(-button_margin,-button_margin)
		self.palm_button_rect = generic_button_rect.move(0,self.rect.width / 2).inflate(-button_margin,-button_margin)

		# create the buttons
		self.buttons = pygame.sprite.Group()
		Button_edtr(self.tile_button_rect, self.buttons, self.menu_surfs['terrain'])
		Button_edtr(self.coin_button_rect, self.buttons, self.menu_surfs['coin'])
		Button_edtr(self.enemy_button_rect, self.buttons, self.menu_surfs['enemy'])
		Button_edtr(self.palm_button_rect, self.buttons, self.menu_surfs['palm fg'], self.menu_surfs['palm bg'])

	def click(self, mouse_pos, mouse_button):
		for sprite in self.buttons:
			if sprite.rect.collidepoint(mouse_pos):
				if mouse_button[1]: # middle mouse click
					if sprite.items['alt']:
						sprite.main_active = not sprite.main_active 
				if mouse_button[2]: # right click
					sprite.switch()
				return sprite.get_id()
		if self.mm_rect.collidepoint(mouse_pos):
			if mouse_button[0]:
				pass

	def highlight_indicator(self, index):
		if EDITOR_DATA[index]['menu'] == 'terrain':
			pygame.draw.rect(self.display_surface, BUTTON_LINE_COLOR, self.tile_button_rect.inflate(4,4),5,4)
		if EDITOR_DATA[index]['menu'] == 'coin':
			pygame.draw.rect(self.display_surface, BUTTON_LINE_COLOR, self.coin_button_rect.inflate(4,4),5,4)
		if EDITOR_DATA[index]['menu'] == 'enemy':
			pygame.draw.rect(self.display_surface, BUTTON_LINE_COLOR, self.enemy_button_rect.inflate(4,4),5,4)
		if EDITOR_DATA[index]['menu'] in ('palm bg', 'palm fg'):
			pygame.draw.rect(self.display_surface, BUTTON_LINE_COLOR, self.palm_button_rect.inflate(4,4),5,4)

	def display(self, index):
		self.buttons.update()
		self.buttons.draw(self.display_surface)
		self.display_surface.blit(self.image, self.mm_rect.topleft)
		self.display_surface.blit(self.sv_image, self.sv_rect.topleft)
		self.highlight_indicator(index)

class Button_edtr(pygame.sprite.Sprite):
	def __init__(self, rect, group, items, items_alt = None):
		super().__init__(group)
		self.image = pygame.Surface(rect.size)
		self.rect = rect

		# items 
		self.items = {'main': items, 'alt': items_alt}
		self.index = 0
		self.main_active = True

	def get_id(self):
		return self.items['main' if self.main_active else 'alt'][self.index][0]

	def switch(self):
		self.index += 1
		self.index = 0 if self.index >= len(self.items['main' if self.main_active else 'alt']) else self.index

	def update(self):
		self.image.fill(BUTTON_BG_COLOR)
		surf = self.items['main' if self.main_active else 'alt'][self.index][1]
		rect = surf.get_rect(center = (self.rect.width / 2, self.rect.height / 2))
		self.image.blit(surf, rect)