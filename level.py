import pygame, sys 
from pygame.math import Vector2 as vector
from settings import *
from support import *
from pygame.mouse import get_pos as mouse_pos
from pygame.image import load

from sprites import Generic, Block, Animated, Particle, Coin, Player, Spikes, Tooth, Shell, Cloud
from timer import Timer

from random import choice, randint


class Level:
	def __init__(self, grid, switch, asset_dict, audio, change_coins, change_health, player_dead, change_diamonds, get_score, get_diamonds, player_alive):
		self.display_surface = pygame.display.get_surface()
		self.switch = switch
		self.switch_locker = True
		self.player_dead = player_dead
		self.player_alive = player_alive


		# groups 
		self.all_sprites = CameraGroup()
		self.coin_sprites = pygame.sprite.Group()
		self.damage_sprites = pygame.sprite.Group()
		self.collision_sprites = pygame.sprite.Group()
		self.shell_sprites = pygame.sprite.Group()
		self.mortal_enemy_collisions = pygame.sprite.Group()
		self.water_damage = pygame.sprite.Group()
		self.damage_sprites_pearl = pygame.sprite.Group()
		self.pearl_destroy = pygame.sprite.Group()

		self.build_level(grid, asset_dict, audio['jump'])

		# ui
		self.change_coins = change_coins
		self.change_health = change_health
		self.change_diamonds = change_diamonds
		self.buttons = Buttons()
		self.get_score = get_score
		self.get_diamonds = get_diamonds
		self.additional_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.additional_surf.fill('green')
		self.additional_surf.set_colorkey('green')
		self.alpha = 0
		self.additional_surf.set_alpha(self.alpha)
		self.score_menu = Score_menu(self.get_score, self.additional_surf)
		self.paused = False
		self.after_pause_timer = Timer(500)

		# level limits
		self.level_limits = {
		'left': -WINDOW_WIDTH,
		'right': sorted(list(grid['terrain'].keys()), key = lambda pos: pos[0])[-1][0] + 500
		}

		# red_line
		self.red_line = sorted(list(grid['terrain'].keys()), key=lambda pos: pos[1])[-1][1] + 100

		# additional stuff
		self.particle_surfs = asset_dict['particle']
		self.cloud_surfs = asset_dict['clouds']
		self.cloud_timer = pygame.USEREVENT + 2
		pygame.time.set_timer(self.cloud_timer, 2000)
		self.startup_clouds()
		self.complete = False
		self.grid = grid

		# sounds 
		self.bg_music = audio['music']
		self.bg_music.set_volume(0.1)

		self.coin_sound = audio['coin']
		self.coin_sound.set_volume(0.1)

		self.hit_sound = audio['hit']
		self.hit_sound.set_volume(0.1)

	def build_level(self, grid, asset_dict, jump_sound):
		for layer_name, layer in grid.items():
			for pos, data in layer.items():
				if layer_name == 'terrain':
					Generic(pos, asset_dict['land'][data], [self.all_sprites, self.collision_sprites, self.pearl_destroy])
				if layer_name == 'water':
					if data == 'top':
						Animated(asset_dict['water top'], pos, [self.all_sprites, self.water_damage], LEVEL_LAYERS['water'])
					else:
						Generic(pos, asset_dict['water bottom'], [self.all_sprites, self.water_damage], LEVEL_LAYERS['water'])

				match data:
					case 0: self.player = Player(pos, asset_dict['player'], self.all_sprites, self.collision_sprites, jump_sound, self.player_dead)
					case 1: 
						self.horizon_y = pos[1]
						self.all_sprites.horizon_y = pos[1]
					# coins
					case 4: Coin('gold', asset_dict['gold'], pos, [self.all_sprites, self.coin_sprites])
					case 5: Coin('silver', asset_dict['silver'], pos, [self.all_sprites, self.coin_sprites])
					case 6: Coin('diamond', asset_dict['diamond'], pos, [self.all_sprites, self.coin_sprites])

					# enemies
					case 7: Spikes(asset_dict['spikes'], pos, [self.all_sprites, self.damage_sprites])
					case 8: 
						Tooth(asset_dict['tooth'], pos, [self.all_sprites, self.mortal_enemy_collisions], self.collision_sprites)
					case 9: 
						Shell(
							orientation = 'left', 
							assets = asset_dict['shell'], 
							pos =  pos, 
							group =  [self.all_sprites, self.collision_sprites, self.shell_sprites],
							pearl_surf = asset_dict['pearl'],
							damage_sprites = self.damage_sprites_pearl
							)
					case 10:
						Shell(
							orientation = 'right',
							assets = asset_dict['shell'],
							pos =  pos,
							group =  [self.all_sprites, self.collision_sprites, self.shell_sprites],
							pearl_surf = asset_dict['pearl'],
							damage_sprites = self.damage_sprites_pearl
							)

					# palm trees
					case 11: 
						Animated(asset_dict['palms']['small_fg'], pos, self.all_sprites)
						Block(pos, (76,50), self.collision_sprites)
					case 12: 
						Animated(asset_dict['palms']['large_fg'], pos, self.all_sprites)
						Block(pos, (76,50), self.collision_sprites)
					case 13: 
						Animated(asset_dict['palms']['left_fg'], pos, self.all_sprites)
						Block(pos, (76,50), self.collision_sprites)
					case 14: 
						Animated(asset_dict['palms']['right_fg'], pos, self.all_sprites)
						Block(pos + vector(50,0), (76,50), self.collision_sprites)
					
					case 15: Animated(asset_dict['palms']['small_bg'], pos, self.all_sprites, LEVEL_LAYERS['bg'])
					case 16: Animated(asset_dict['palms']['large_bg'], pos, self.all_sprites, LEVEL_LAYERS['bg'])
					case 17: Animated(asset_dict['palms']['left_bg'], pos, self.all_sprites, LEVEL_LAYERS['bg'])
					case 18: Animated(asset_dict['palms']['right_bg'], pos, self.all_sprites, LEVEL_LAYERS['bg'])
		for sprite in self.shell_sprites:
			sprite.player = self.player



	def get_coins(self):
		collided_coins = pygame.sprite.spritecollide(self.player, self.coin_sprites, True)
		for sprite in collided_coins:
			self.coin_sound.play()
			Particle(self.particle_surfs, sprite.rect.center, self.all_sprites)
			if sprite.coin_type == "gold":
				self.change_coins(50)
			elif sprite.coin_type == "silver":
				self.change_coins(10)
			elif sprite.coin_type == "diamond":
				self.change_diamonds(1)

	def player_under_red_line(self):
		if self.player.pos[1] >= self.red_line and not self.player.invul_timer.active and self.player.player_dead() == False:
			self.hit_sound.play()
			self.player.damage()
			self.change_health(100)


	def get_damage(self):
		collision_sprites = pygame.sprite.spritecollide(self.player, self.damage_sprites, False, pygame.sprite.collide_mask)
		if collision_sprites and not self.player.invul_timer.active and self.player.player_dead() == False:
			self.hit_sound.play()
			self.player.damage()
			self.change_health(20)


	def get_damage_pearl(self):
		collision_sprites = pygame.sprite.spritecollide(self.player, self.damage_sprites_pearl, True, pygame.sprite.collide_mask)
		pygame.sprite.groupcollide(self.pearl_destroy, self.damage_sprites_pearl, False, True)
		if collision_sprites and not self.player.invul_timer.active and self.player.player_dead() == False:
			self.hit_sound.play()
			self.player.damage()
			self.change_health(20)


	def get_water_damage(self):
		collision_sprites = pygame.sprite.spritecollide(self.player, self.water_damage, False, pygame.sprite.collide_mask)
		if collision_sprites and not self.player.invul_timer.active and self.player.player_dead() == False:
			self.hit_sound.play()
			self.player.set_drowning(True)
			self.change_health(20)
			self.player.invul_timer.activate()
		elif collision_sprites and self.player.player_dead() == False:
			self.player.set_drowning(True)
		else:
			self.player.set_drowning(False)

	def menu_click(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN and self.buttons.mm_rect.collidepoint(mouse_pos()) and self.switch_locker == True:
			self.switch_locker = False
			self.switch({'from':  'level', 'to': 'main_menu'})
		if event.type == pygame.MOUSEBUTTONDOWN and self.buttons.pause_rect.collidepoint(mouse_pos()) and self.switch_locker == True and self.paused:
			self.paused = False
			self.after_pause_timer.activate()
		elif event.type == pygame.MOUSEBUTTONDOWN and self.buttons.pause_rect.collidepoint(mouse_pos()) and self.switch_locker == True and self.paused == False:
			self.paused = True


	def score_menu_click(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN and self.score_menu.restart_rect.collidepoint(mouse_pos()) and self.switch_locker == True:
			self.switch_locker = False
			self.switch({'from':  'level', 'to': 'level'}, self.grid)
		if event.type == pygame.MOUSEBUTTONDOWN and self.score_menu.levels_rect.collidepoint(mouse_pos()) and self.switch_locker == True and self.paused == False:
			self.switch_locker = False
			self.switch({'from':  'level', 'to': 'level_menu'})
		if event.type == pygame.MOUSEBUTTONDOWN and self.score_menu.levels_rect.collidepoint(mouse_pos()) and self.switch_locker == True and self.paused:
			self.paused = False
			self.after_pause_timer.activate()



	def mortal_enemy_collision(self):
		mortal_collided = pygame.sprite.spritecollide(self.player, self.mortal_enemy_collisions, False, pygame.sprite.collide_mask)
		if mortal_collided:
			for enemy in mortal_collided:
				enemy_center = enemy.rect.centery
				enemy_top = enemy.rect.top
				player_bottom = self.player.rect.bottom
				if enemy_top < player_bottom < enemy_center and self.player.status == 'fall' :
					self.player.direction.y -= 3.5
					enemy.death_timer.activate()
					enemy.dead = True
				elif not enemy_top < player_bottom < enemy_center and not self.player.invul_timer.active:
					self.hit_sound.play()
					self.player.damage()
					self.change_health(20)

	def event_loop(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and self.switch_locker == True:
				self.switch_locker = False
				self.switch({'from':  'level', 'to': 'editor'})
			if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
				if self.paused:
					self.paused = not self.paused
					self.after_pause_timer.activate()
				else:
					self.paused = not self.paused
			if event.type == self.cloud_timer:
				surf = choice(self.cloud_surfs)
				surf = pygame.transform.scale2x(surf) if randint(0,5) > 3 else surf
				x = self.level_limits['right'] + randint(100,300)
				y = self.horizon_y - randint(-50,600)
				Cloud((x,y), surf, self.all_sprites, self.level_limits['left'])

			self.menu_click(event)
			if self.complete or self.player_dead() or self.paused:
				self.score_menu_click(event)

	def startup_clouds(self):
		for i in range(40):
			surf = choice(self.cloud_surfs)
			surf = pygame.transform.scale2x(surf) if randint(0,5) > 3 else surf
			x = randint(self.level_limits['left'], self.level_limits['right'])
			y = self.horizon_y - randint(-50,600)
			Cloud((x,y), surf, self.all_sprites, self.level_limits['left'])

	def transition(self):
		self.alpha = max(0, min(self.alpha, 255))
		self.alpha += 5
		self.additional_surf.set_alpha(self.alpha)

	def transition_out(self):
		self.alpha = max(0, min(self.alpha, 255))
		self.alpha -= 5
		self.additional_surf.set_alpha(self.alpha)

	def run(self, dt):
		# update

		self.event_loop()
		if self.paused:
			self.transition()
			self.score_menu.display(False, self.get_diamonds, True)
		else:
			self.all_sprites.update(dt)
			self.get_damage()
			self.get_damage_pearl()
			self.get_water_damage()
		if self.after_pause_timer.active:
			self.transition_out()
		self.get_coins()
		self.mortal_enemy_collision()
		self.player_under_red_line()

		# drawing
		self.display_surface.fill(SKY_COLOR)
		self.all_sprites.custom_draw(self.player)
		if self.paused:
			self.buttons.display(True)
		else:
			self.buttons.display(False)
		self.display_surface.blit(self.additional_surf, (0, 0))
		self.after_pause_timer.update()
		if self.player_dead():
			self.transition()
			self.score_menu.display(False, self.get_diamonds)
		if self.complete:
			self.transition()
			self.score_menu.display(True)
			self.player.speed = 0

class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = vector()

	def draw_horizon(self):
		horizon_pos = self.horizon_y - self.offset.y	

		if horizon_pos < WINDOW_HEIGHT:
			sea_rect = pygame.Rect(0,horizon_pos,WINDOW_WIDTH,WINDOW_HEIGHT - horizon_pos)
			pygame.draw.rect(self.display_surface, SEA_COLOR, sea_rect)

			# horizon line 
			# 3 extra rectangles 
			horizon_rect1 = pygame.Rect(0,horizon_pos - 10,WINDOW_WIDTH,10)
			horizon_rect2 = pygame.Rect(0,horizon_pos - 16,WINDOW_WIDTH,4)
			horizon_rect3 = pygame.Rect(0,horizon_pos - 20,WINDOW_WIDTH,2)
			pygame.draw.rect(self.display_surface, HORIZON_TOP_COLOR, horizon_rect1)
			pygame.draw.rect(self.display_surface, HORIZON_TOP_COLOR, horizon_rect2)
			pygame.draw.rect(self.display_surface, HORIZON_TOP_COLOR, horizon_rect3)
			pygame.draw.line(self.display_surface, HORIZON_COLOR, (0,horizon_pos), (WINDOW_WIDTH,horizon_pos), 3)

		if horizon_pos < 0:
			self.display_surface.fill(SEA_COLOR)

	def custom_draw(self, player):
		self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
		self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

		for sprite in self:
			if sprite.z == LEVEL_LAYERS['clouds']:
				offset_rect = sprite.rect.copy()
				offset_rect.center -= self.offset
				self.display_surface.blit(sprite.image, offset_rect)

		self.draw_horizon()
		for sprite in self:
			for layer in LEVEL_LAYERS.values():
				if sprite.z == layer and sprite.z != LEVEL_LAYERS['clouds']:
					offset_rect = sprite.rect.copy()
					offset_rect.center -= self.offset
					self.display_surface.blit(sprite.image, offset_rect)

class Buttons:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.create_buttons()


	def create_buttons(self):
		# main_menu area
		mm_size = 45
		mm_margin = 6
		mm_topleft = (WINDOW_WIDTH - mm_size - mm_margin, mm_margin)
		self.mm_rect = pygame.Rect(mm_topleft, (mm_size, mm_size))
		self.image = load(path.join(script_directory, 'graphics', 'menus', 'main_menu_button.png')).convert_alpha()
		self.image = pygame.transform.scale(self.image, (mm_size, mm_size))
		self.pause_rect = pygame.Rect(vector(mm_topleft) - (mm_size + mm_margin, 0), (mm_size, mm_size))
		self.p_image = load(path.join(script_directory, 'graphics', 'menus', 'score_menu', 'pause_button.png')).convert_alpha()
		self.p_image = pygame.transform.scale(self.p_image, (mm_size, mm_size))
		self.r_image = load(path.join(script_directory, 'graphics', 'menus', 'score_menu', 'release_pause_button.png')).convert_alpha()
		self.r_image = pygame.transform.scale(self.r_image, (mm_size, mm_size))


	def display(self, paused = False):
		self.display_surface.blit(self.image, self.mm_rect.topleft)
		if paused:
			self.display_surface.blit(self.r_image, self.pause_rect.topleft)
		else:
			self.display_surface.blit(self.p_image, self.pause_rect.topleft)

class Score_menu:
	def __init__(self, get_score, surf):
		self.display_surface = surf
		self.get_score = get_score
		self.create_buttons()



	def create_buttons(self):
		# main_menu area
		topleft = (WINDOW_WIDTH / 2 - 360 / 2, 120)
		self.tittle_rect = pygame.Rect(topleft, (360, 100))
		self.image = load(path.join(script_directory, 'graphics', 'menus', 'score_menu', 'win.png')).convert_alpha()
		self.image = pygame.transform.scale(self.image, (360, 100))
		self.image_go = load(path.join(script_directory, 'graphics', 'menus', 'score_menu', 'game_over.png')).convert_alpha()
		self.image_go = pygame.transform.scale(self.image_go, (360, 100))
		self.image_paused = load(path.join(script_directory, 'graphics', 'menus', 'score_menu', 'paused.png')).convert_alpha()
		self.image_paused = pygame.transform.scale(self.image_paused, (360, 100))
		self.score_rect = pygame.Rect(vector(topleft) + (0, 110), (360, 240))
		self.score_rect_image = load(path.join(script_directory, 'graphics', 'menus', 'score_menu', 'score_back.png')).convert_alpha()
		self.score_rect_image = pygame.transform.scale(self.score_rect_image, (360, 240))
		self.diamonds0_image = load(path.join(script_directory, 'graphics', 'menus', 'score_menu', '0diamond_score.png')).convert_alpha()
		self.diamonds0_image = pygame.transform.scale(self.diamonds0_image, (360, 240))
		self.diamonds1_image = load(path.join(script_directory, 'graphics', 'menus', 'score_menu', '1diamond_score.png')).convert_alpha()
		self.diamonds1_image = pygame.transform.scale(self.diamonds1_image, (360, 240))
		self.diamonds2_image = load(path.join(script_directory, 'graphics', 'menus', 'score_menu', '2diamond_score.png')).convert_alpha()
		self.diamonds2_image = pygame.transform.scale(self.diamonds2_image, (360, 240))
		self.buttons_rect = pygame.Rect(vector(topleft) + (0, 360), (360, 120))
		self.buttons_rect_image = load(path.join(script_directory, 'graphics', 'menus', 'score_menu', 'buttons_back.png')).convert_alpha()
		self.buttons_rect_image = pygame.transform.scale(self.buttons_rect_image, (360, 120))
		self.restart_rect = pygame.Rect(vector(topleft) + (50, 396), (120, 46))
		self.restart_rect_image = load(path.join(script_directory, 'graphics', 'menus', 'score_menu', 'restart.png')).convert_alpha()
		self.restart_rect_image = pygame.transform.scale(self.restart_rect_image, (120, 46))
		self.levels_rect = pygame.Rect(vector(topleft) + (190, 396), (120, 46))
		self.levels_rect_image = load(path.join(script_directory, 'graphics', 'menus', 'score_menu', 'levels.png')).convert_alpha()
		self.levels_rect_image = pygame.transform.scale(self.levels_rect_image, (120, 46))
		self.resume_rect_image = load(path.join(script_directory, 'graphics', 'menus', 'score_menu', 'resume.png')).convert_alpha()
		self.resume_rect_image = pygame.transform.scale(self.resume_rect_image, (120, 46))
		self.font = pygame.font.Font(path.join(script_directory, 'graphics', 'ui', 'ARCADEPI.ttf'), 18)



	def display(self, level_complete, get_diamonds = None, paused = False):
		self.score_surf = self.font.render(f"Score: {self.get_score()}", False, '#33323d')
		self.score_surf_rect = self.score_surf.get_rect(topleft=(vector(WINDOW_WIDTH / 2 - 360 / 2, 120) + (120, 255)))
		self.display_surface.blit(self.buttons_rect_image, self.buttons_rect.topleft)
		if level_complete:
			self.display_surface.blit(self.image, self.tittle_rect.topleft)
			self.display_surface.blit(self.score_rect_image, self.score_rect.topleft)
		else:
			if paused:
				self.display_surface.blit(self.image_paused, self.tittle_rect.topleft)
			else:
				self.display_surface.blit(self.image_go, self.tittle_rect.topleft)
			if get_diamonds() == 0:
				self.display_surface.blit(self.diamonds0_image, self.score_rect.topleft)
			elif get_diamonds() == 1:
				self.display_surface.blit(self.diamonds1_image, self.score_rect.topleft)
			if get_diamonds() == 2:
				self.display_surface.blit(self.diamonds2_image, self.score_rect.topleft)
		self.display_surface.blit(self.restart_rect_image, self.restart_rect.topleft)
		if paused:
			self.display_surface.blit(self.resume_rect_image, self.levels_rect.topleft)
		else:
			self.display_surface.blit(self.levels_rect_image, self.levels_rect.topleft)
		self.display_surface.blit(self.score_surf, self.score_surf_rect)
