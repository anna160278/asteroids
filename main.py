import os
import random as rnd

import pygame as p

import sprites
from settings import *


# Loading images
ship_img = p.image.load('res/PNG/playerShip1_orange.png')
background_img = p.image.load('res/Backgrounds/darkPurple.png')
background_img = p.transform.scale(background_img,
                                   (SCREEN_WIDTH, SCREEN_HEIGHT))

meteor_name_list = os.listdir('res/PNG/Meteors')

# Initializing the game window
p.init()
clock = p.time.Clock()
screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
p.display.set_caption('Asteroids')

ship = sprites.Spaceship((SCREEN_WIDTH/2, SCREEN_HEIGHT-50),
                         ship_img)
meteor_group = p.sprite.Group()

SPAWN_METEOR = p.USEREVENT
p.time.set_timer(SPAWN_METEOR, 300)

running = True
while running:
    for event in p.event.get():
        if event.type == p.QUIT or (event.type == p.KEYDOWN
                                    and event.key == p.K_ESCAPE):
            running = False

        if event.type == SPAWN_METEOR:
            # Not the best approach. It'll be improved
            # in the next lesson.
            meteor_image = p.image.load(
                'res/PNG/Meteors/'+rnd.choice(meteor_name_list))
            meteor = sprites.Meteor(
                (rnd.randint(0,SCREEN_WIDTH), -20), meteor_image)
            meteor_group.add(meteor)

    # Drawing
    screen.blit(background_img, (0, 0))
    ship.draw(screen)
    meteor_group.draw(screen)

    # Updating
    ship.move()
    meteor_group.update()

    clock.tick(60)
    p.display.flip()

