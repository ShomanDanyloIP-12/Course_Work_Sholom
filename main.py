import pygame
from pygame.math import Vector2 as vector
from settings import *
from support import *

from pygame.image import load

from ui import UI
from editor import Editor
from level import Level

from main_menu import Main_menu
from save_menu import Save_menu
from level_menu import Level_menu

from os import walk, getcwd, path

class Main:
	def __init__(self):
		pygame.init()
		script_directory = path.dirname(path.realpath(__file__))
		print("Current working directory:", getcwd())
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.clock = pygame.time.Clock()
		self.imports()

		self.main_menu = Main_menu(self.switch)
		self.level_menu = Level_menu(self.switch)
		self.save_menu = Save_menu(self.switch)

		# game attributes
		self.max_health = 100
		self.cur_health = 100
		self.coins = 0
		self.diamonds = 0
		self.player_dead = False

		# ui
		self.ui = UI(self.display_surface)

		self.replacement = {}
		self.editor_active = False
		self.level_active = False
		self.main_menu_active = True
		self.level_menu_active = False
		self.save_menu_active = False
		self.transition = Transition(self.toggle)
		self.editor = Editor(self.land_tiles, self.switch, self.editor_sounds)

		# cursor 
		surf = load(path.join(script_directory, 'graphics', 'cursors', 'mouse.png')).convert_alpha()
		cursor = pygame.cursors.Cursor((0,0), surf)
		pygame.mouse.set_cursor(cursor)



	def imports(self):
		script_directory = path.dirname(path.realpath(__file__))
		# terrain
		self.land_tiles = import_folder_dict(path.join(script_directory, 'graphics', 'terrain', 'land'))
		self.water_bottom = load(path.join(script_directory, 'graphics', 'terrain', 'water', 'water_bottom.png')).convert_alpha()
		self.water_top_animation = import_folder(path.join(script_directory, 'graphics', 'terrain', 'water', 'animation'))

		# coins
		self.gold = import_folder(path.join(script_directory, 'graphics', 'items', 'gold'))
		self.silver = import_folder(path.join(script_directory, 'graphics', 'items', 'silver'))
		self.diamond = import_folder(path.join(script_directory, 'graphics', 'items', 'diamond'))
		self.particle = import_folder(path.join(script_directory, 'graphics', 'items', 'particle'))

		# palm trees
		self.palms = {folder: import_folder(path.join(script_directory, 'graphics', 'terrain', 'palm', f'{folder}')) for folder in list(walk(path.join(script_directory, 'graphics', 'terrain', 'palm')))[0][1]}

		# enemies
		self.spikes = load(path.join(script_directory, 'graphics', 'enemies', 'spikes', 'spikes.png')).convert_alpha()
		self.tooth = {folder: import_folder(path.join(script_directory, 'graphics', 'enemies', 'tooth', f'{folder}')) for folder in list(walk(path.join(script_directory, 'graphics', 'enemies', 'tooth')))[0][1]}
		self.shell = {folder: import_folder(path.join(script_directory, 'graphics', 'enemies', 'shell_left', f'{folder}')) for folder in list(walk(path.join(script_directory, 'graphics', 'enemies', 'shell_left')))[0][1]}
		self.pearl = load(path.join(script_directory, 'graphics', 'enemies', 'pearl', 'pearl.png')).convert_alpha()

		# player
		self.player_graphics = {folder: import_folder(path.join(script_directory, 'graphics', 'player', f'{folder}')) for folder in list(walk(path.join(script_directory, 'graphics', 'player')))[0][1]}

		# clouds
		self.clouds = import_folder(path.join(script_directory, 'graphics', 'clouds'))

		# editor_sounds
		self.editor_sounds = {
			'music': pygame.mixer.Sound(path.join(script_directory, 'audio', 'Explorer.ogg'))
		}

		# level_sounds
		self.level_sounds = {
			'coin': pygame.mixer.Sound(path.join(script_directory, 'audio', 'coin.wav')),
			'hit': pygame.mixer.Sound(path.join(script_directory, 'audio', 'hit.wav')),
			'jump': pygame.mixer.Sound(path.join(script_directory, 'audio', 'jump.wav')),
			'music': pygame.mixer.Sound(path.join(script_directory, 'audio', 'SuperHero.ogg')),
		}


	def change_coins(self, amount):
		self.coins += amount

	def change_health(self, amount):
		self.cur_health -= amount

	def death(self):
		if self.cur_health <= 0:
			self.player_dead = True
			self.switch_locker = False
			self.switch({'from': 'level', 'to': 'main_menu'})
			self.level.bg_music.stop()

	def player_dead_get(self):
		return self.player_dead

	def change_toggle(self, toggle_replacement):
		self.replacement = toggle_replacement

	def toggle(self):
		if self.replacement['from'] == 'editor':
			self.editor_active = False
		elif self.replacement['from'] == 'level':
			self.level_active = False
		elif self.replacement['from'] == 'main_menu':
			self.main_menu_active = False
		elif self.replacement['from'] == 'level_menu':
			self.level_menu_active = False
		elif self.replacement['from'] == 'save_menu':
			self.save_menu_active = False

		if self.replacement['to'] == 'editor':
			self.editor_active = True
		elif self.replacement['to'] == 'level':
			self.level_active = True
		elif self.replacement['to'] == 'main_menu':
			self.main_menu_active = True
		elif self.replacement['to'] == 'level_menu':
			self.level_menu_active = True
		elif self.replacement['to'] == 'save_menu':
			self.save_menu_active = True

		if self.editor_active:
			self.editor.editor_music.play()
			self.editor.switch_locker = True
		if self.level_active:
			self.level.switch_locker = True
		if self.main_menu_active:
			self.main_menu.switch_locker = True
		if self.level_menu_active:
			self.level_menu.switch_locker = True
		if self.save_menu_active:
			self.save_menu.switch_locker = True

		if not self.level_active:
			self.coins = 0
			self.cur_health = 100
			self.player_dead = False



	def switch(self, toggle_replacement, grid = None):
		self.change_toggle(toggle_replacement)
		self.transition.active = True
		if grid:
			self.level = Level(
				grid,
				self.switch, {
					'land': self.land_tiles,
					'water bottom': self.water_bottom,
					'water top': self.water_top_animation,
					'gold': self.gold,
					'silver': self.silver,
					'diamond': self.diamond,
					'particle': self.particle,
					'palms': self.palms,
					'spikes': self.spikes,
					'tooth': self.tooth,
					'shell': self.shell,
					'player': self.player_graphics,
					'pearl': self.pearl,
					'clouds': self.clouds},
				self.level_sounds,
				self.change_coins,
				self.change_health,
				self.player_dead_get
			)

	def run(self):
		while True:
			dt = self.clock.tick() / 1000
			
			if self.editor_active:
				self.editor.run(dt)
			elif self.level_active:
				self.level.run(dt)
				self.ui.show_health(self.cur_health, self.max_health)
				self.ui.show_coins(self.coins)
				self.death()
			elif self.main_menu_active:
				self.main_menu.run(dt)
			elif self.level_menu_active:
				self.level_menu.run(dt)
			elif self.save_menu_active:
				self.save_menu.run(dt)

			self.transition.display(dt)
			pygame.display.update()


class Transition:
	def __init__(self, toggle):
		self.display_surface = pygame.display.get_surface()
		self.toggle = toggle
		self.active = False


		self.border_width = 0
		self.direction = 1
		self.center = (WINDOW_WIDTH /2, WINDOW_HEIGHT / 2)
		self.radius = vector(self.center).magnitude()
		self.threshold = self.radius + 100

	def display(self, dt):
		if self.active:
			self.border_width += 1000 * dt * self.direction
			if self.border_width >= self.threshold:
				self.direction = -1
				self.border_width += -10
				self.toggle()

			if self.border_width < 0:
				self.active = False
				self.border_width = 0
				self.direction = 1
			pygame.draw.circle(self.display_surface, 'black',self.center, self.radius, int(self.border_width))


if __name__ == '__main__':
	main = Main()
	main.run() 