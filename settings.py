# general setup
from os import path
TILE_SIZE = 64
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
ANIMATION_SPEED = 8

# editor graphics
script_directory = path.dirname(path.realpath(__file__))
graphics_directory = path.join(script_directory, 'graphics')
EDITOR_DATA = {
	0: {'style': 'player', 'type': 'object', 'menu': None, 'menu_surf': None, 'preview': None, 'graphics': path.join(graphics_directory, 'player', 'idle_right')},
	1: {'style': 'sky',    'type': 'object', 'menu': None, 'menu_surf': None, 'preview': None, 'graphics': None},

	2: {'style': 'terrain', 'type': 'tile', 'menu': 'terrain', 'menu_surf': path.join(graphics_directory, 'menu', 'land.png'),  'preview': path.join(graphics_directory, 'preview', 'land.png'),  'graphics': None},
	3: {'style': 'water',   'type': 'tile', 'menu': 'terrain', 'menu_surf': path.join(graphics_directory, 'menu', 'water.png'), 'preview': path.join(graphics_directory, 'preview', 'water.png'), 'graphics': path.join(graphics_directory, 'terrain', 'water', 'animation')},

	4: {'style': 'coin', 'type': 'tile', 'menu': 'coin', 'menu_surf': path.join(graphics_directory, 'menu', 'gold.png'),    'preview': path.join(graphics_directory, 'preview', 'gold.png'),    'graphics': path.join(graphics_directory, 'items', 'gold')},
	5: {'style': 'coin', 'type': 'tile', 'menu': 'coin', 'menu_surf': path.join(graphics_directory, 'menu', 'silver.png'),  'preview': path.join(graphics_directory, 'preview', 'silver.png'),  'graphics': path.join(graphics_directory, 'items', 'silver')},
	6: {'style': 'coin', 'type': 'tile', 'menu': 'coin', 'menu_surf': path.join(graphics_directory, 'menu', 'diamond.png'), 'preview': path.join(graphics_directory, 'preview', 'diamond.png'), 'graphics': path.join(graphics_directory, 'items', 'diamond')},

	7:  {'style': 'enemy', 'type': 'tile', 'menu': 'enemy', 'menu_surf': path.join(graphics_directory, 'menu', 'spikes.png'),      'preview': path.join(graphics_directory, 'preview', 'spikes.png'),      'graphics': path.join(graphics_directory, 'enemies', 'spikes')},
	8:  {'style': 'enemy', 'type': 'tile', 'menu': 'enemy', 'menu_surf': path.join(graphics_directory, 'menu', 'tooth.png'),       'preview': path.join(graphics_directory, 'preview', 'tooth.png'),       'graphics': path.join(graphics_directory, 'enemies', 'tooth', 'idle')},
	9:  {'style': 'enemy', 'type': 'tile', 'menu': 'enemy', 'menu_surf': path.join(graphics_directory, 'menu', 'shell_left.png'),  'preview': path.join(graphics_directory, 'preview', 'shell_left.png'),  'graphics': path.join(graphics_directory, 'enemies', 'shell_left', 'idle')},
	10: {'style': 'enemy', 'type': 'tile', 'menu': 'enemy', 'menu_surf': path.join(graphics_directory, 'menu', 'shell_right.png'), 'preview': path.join(graphics_directory, 'preview', 'shell_right.png'), 'graphics': path.join(graphics_directory, 'enemies', 'shell_right', 'idle')},

	11: {'style': 'palm_fg', 'type': 'object', 'menu': 'palm fg', 'menu_surf': path.join(graphics_directory, 'menu', 'small_fg.png'), 'preview': path.join(graphics_directory, 'preview', 'small_fg.png'), 'graphics': path.join(graphics_directory, 'terrain', 'palm', 'small_fg')},
	12: {'style': 'palm_fg', 'type': 'object', 'menu': 'palm fg', 'menu_surf': path.join(graphics_directory, 'menu', 'large_fg.png'), 'preview': path.join(graphics_directory, 'preview', 'large_fg.png'), 'graphics': path.join(graphics_directory, 'terrain', 'palm', 'large_fg')},
	13: {'style': 'palm_fg', 'type': 'object', 'menu': 'palm fg', 'menu_surf': path.join(graphics_directory, 'menu', 'left_fg.png'),  'preview': path.join(graphics_directory, 'preview', 'left_fg.png'),  'graphics': path.join(graphics_directory, 'terrain', 'palm', 'left_fg')},
	14: {'style': 'palm_fg', 'type': 'object', 'menu': 'palm fg', 'menu_surf': path.join(graphics_directory, 'menu', 'right_fg.png'), 'preview': path.join(graphics_directory, 'preview', 'right_fg.png'), 'graphics': path.join(graphics_directory, 'terrain', 'palm', 'right_fg')},

	15: {'style': 'palm_bg', 'type': 'object', 'menu': 'palm bg', 'menu_surf': path.join(graphics_directory, 'menu', 'small_bg.png'), 'preview': path.join(graphics_directory, 'preview', 'small_bg.png'), 'graphics': path.join(graphics_directory, 'terrain', 'palm', 'small_bg')},
	16: {'style': 'palm_bg', 'type': 'object', 'menu': 'palm bg', 'menu_surf': path.join(graphics_directory, 'menu', 'large_bg.png'), 'preview': path.join(graphics_directory, 'preview', 'large_bg.png'), 'graphics': path.join(graphics_directory, 'terrain', 'palm', 'large_bg')},
	17: {'style': 'palm_bg', 'type': 'object', 'menu': 'palm bg', 'menu_surf': path.join(graphics_directory, 'menu', 'left_bg.png'),  'preview': path.join(graphics_directory, 'preview', 'left_bg.png'),  'graphics': path.join(graphics_directory, 'terrain', 'palm', 'left_bg')},
	18: {'style': 'palm_bg', 'type': 'object', 'menu': 'palm bg', 'menu_surf': path.join(graphics_directory, 'menu', 'right_bg.png'), 'preview': path.join(graphics_directory, 'preview', 'right_bg.png'), 'graphics': path.join(graphics_directory, 'terrain', 'palm', 'left_bg')},
}

NEIGHBOR_DIRECTIONS = {
	'A': (0,-1),
	'B': (1,-1),
	'C': (1,0),
	'D': (1,1),
	'E': (0,1),
	'F': (-1,1),
	'G': (-1,0),
	'H': (-1,-1)
}

LEVEL_LAYERS = {
	'clouds': 1,
	'ocean': 2,
	'bg': 3,
	'water': 4,
	'main': 5
}

# colors 
SKY_COLOR = '#ddc6a1'
SEA_COLOR = '#92a9ce'
HORIZON_COLOR = '#f5f1de'
HORIZON_TOP_COLOR = '#d1aa9d'
LINE_COLOR = 'black'
BUTTON_BG_COLOR = '#33323d'
BUTTON_LINE_COLOR = '#f5f1de'