import pygame as pg
import os

#screen settings 
TITLE = "Doodle Jump"
ICON = pg.image.load(os.path.join('img', 'lik-left@2x.png'))
WIDTH = 480
HEIGHT = 550
FPS = 700 #70
FONT_NAME = "arial"
HS_FILE = "highscore.txt"
PLAYER_SPRITE_PATHS_LEFT = ['blue-lik-left@2x.png', 'bunny-left@2x.png', 'doodlestein-left@2x.png', 'frozen-left@2x.png', 'ghost-left@2x.png', 'ice-left@2x.png', 'jungle-left@2x.png', 'lik-left@2x.png', 'soccer-left@2x.png', 'space-left@2x.png', 'underwater-left@2x.png']
PLAYER_SPRITE_PATHS_RIGHT = ['blue-lik-right@2x.png', 'bunny-right@2x.png', 'doodlestein-right@2x.png', 'frozen-right@2x.png', 'ghost-right@2x.png', 'ice-right@2x.png', 'jungle-right@2x.png', 'lik-right@2x.png', 'soccer-right@2x.png', 'space-right@2x.png', 'underwater-right@2x.png']
for i in range(11):
	pass


#player character properties
PLAYER_ACC = .35  #acceleration was .35
PLAYER_FRICTION = -0.05
PLAYER_GRAVITY = 0.3
PLAYER_JUMP = 12


# PLATFORM PROPERTIES
MIDDLE_TOLERANCE = 20  # increases size of 'middle' of platform
MIDDLE_JUMP_FACTOR = 1.4
PLATFORM_HEIGHT = 20
PLATFORM_WIDTH = 80
NUMBER_OF_PLATFORMS = 14
INITIAL_PLATFORM = ((WIDTH - PLATFORM_WIDTH)/2 + MIDDLE_TOLERANCE + 1,
					HEIGHT * 3/4)

                                   
#colors
WHITE = (255,255,255)
BLACK = (0, 0, 0)
RED = (255, 0 , 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE   # background color
DARK_BLUE = (0, 0, 150)
