import random
import pygame as pg
from settings import *
import os

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.sprite_num = random.randint(1,10)
        self.left_image = pg.image.load(os.path.join('img', PLAYER_SPRITE_PATHS_LEFT[self.sprite_num]))
        self.left_image = pg.transform.scale(self.left_image, (38, 39))
        self.right_image = pg.image.load(os.path.join('img', PLAYER_SPRITE_PATHS_RIGHT[self.sprite_num]))
        self.right_image = pg.transform.scale(self.right_image, (38, 39))
        self.image = self.left_image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT/ 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0) # velocity
        self.acc = vec(0, 0) # acceleration

    def update(self): # part of the sprite class... called every frame and updates the velocity
        self.acc = vec(self.acc.x, PLAYER_GRAVITY)

        self.acc.x += self.vel.x * PLAYER_FRICTION   # slows down player movment when key is let go    
        self.vel += self.acc                         # update velocity
        self.pos += self.vel + 0.5 * self.acc        # update position

        if self.vel.x > 0:
            self.image = self.right_image
        else:
            self.image = self.left_image

        self.rect.midbottom = self.pos  # move player


    # check if the player hits a platform... if so, flip sign of vertical velocity
    def bounce(self):
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)  # collision detection
        for platform in hits:
            # triggers gameover if platform is dangerous 
            if platform.dangerous_chance == 1:
                self.game.death_sound.play()
                self.game.playing = False

            else:
                # check player is above platform and falling
                if self.vel.y > 0 and self.rect.bottom < platform.rect.bottom:
                    self.rect.bottom = platform.rect.top    # prevent player from clipping through platform
                    
                    # bounce higher if in center of platform
                    if platform.rect.midtop[0] - MIDDLE_TOLERANCE < self.rect.midbottom[0] < platform.rect.midtop[0] + MIDDLE_TOLERANCE:
                        self.game.jump_sound.play()
                        self.vel.y = -PLAYER_JUMP * MIDDLE_JUMP_FACTOR
                    
                    # normal platform
                    else:
                        self.game.jump_sound.play()
                        self.vel.y = -PLAYER_JUMP

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w=PLATFORM_WIDTH, h=PLATFORM_HEIGHT): # x and y location, width and height
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join('img', 'green_grass_platform.png'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = random.randrange(1,3) # random velocity for platform
        self.moving_odds = 1   # probability of moving platform
        self.moving_chance = 1
        self.dangerous_odds = 0
        self.dangerous_chance = random.randint(0, self.dangerous_odds)

        # change image if platform is moving
        if self.dangerous_chance == 1:
            self.image = pg.image.load(os.path.join('img', 'red_grass_platform.png'))

    def update(self): # part of the sprite class. Only update for platforms is if they are moving
        if self.moving_chance == 1:
            self.rect.x += self.speed

        # reverse speed if platform hits the side of the screen
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed = -self.speed  