import os
import random as rnd

import pygame as p

import sprites
from settings import *


# Loading images
background_img = p.image.load('res/Backgrounds/darkPurple.png')
background_img = p.transform.scale(background_img,
                                   (SCREEN_WIDTH, SCREEN_HEIGHT))
laser_img = p.image.load("res/PNG/Lasers/laserRed01.png")
meteor_images = [p.image.load('res/PNG/Meteors/'+name)
                 for name in os.listdir('res/PNG/Meteors')]
ship_images = [p.image.load(f'res/PNG/Damage/playerShip1_damage{i}.png')
               for i in range(1, 4)]
ship_images.insert(0, p.image.load('res/PNG/playerShip1_orange.png'))

# Initializing the game window
p.init()
clock = p.time.Clock()
screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
p.display.set_caption('Asteroids')

ship = sprites.Spaceship((SCREEN_WIDTH/2, SCREEN_HEIGHT-50),
                         ship_images)
# Making groups
meteor_group = p.sprite.Group()
laser_group = p.sprite.GroupSingle()

# Making a timer for meteors
SPAWN_METEOR = p.USEREVENT
p.time.set_timer(SPAWN_METEOR, 300)

running = True
while running:
    for event in p.event.get():
        if event.type == p.QUIT or (event.type == p.KEYDOWN
                                    and event.key == p.K_ESCAPE):
            running = False

        if event.type == SPAWN_METEOR:
            meteor_image = rnd.choice(meteor_images)
            meteor = sprites.Meteor(
                (rnd.randint(0, SCREEN_WIDTH), -20), meteor_image)
            meteor_group.add(meteor)
        if event.type == p.MOUSEBUTTONDOWN:
            if len(laser_group) == 0:
                laser_group.add(sprites.Laser(ship.rect.center,
                                              laser_img))

    # If the returned list is empty, it evaluates to False.
    # Otherwise - to True.
    if p.sprite.spritecollide(ship, meteor_group, True):
        ship.get_damage(1)

    for laser in laser_group:
        if p.sprite.spritecollide(laser, meteor_group, True):
            laser.kill()

    # Drawing
    screen.blit(background_img, (0, 0))
    laser_group.draw(screen)
    ship.draw(screen)
    meteor_group.draw(screen)

    # Updating
    ship.update()
    meteor_group.update()
    laser_group.update()

    clock.tick(60)
    p.display.flip()

