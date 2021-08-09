import os
import random as rnd

import pygame as p
import pygame.freetype

import sprites
from settings import *


def draw():
    screen.blit(background_img, (0, 0))
    laser_group.draw(screen)
    ship.draw(screen)
    meteor_group.draw(screen)

    screen.blit(hp_img, (20, 20))
    screen.blit(x_img, (60, 28))
    score_font.render_to(screen, (85, 23), str(ship.hp), WHITE)
    score_font.render_to(screen, (SCREEN_WIDTH-180, 23), 
                         str(ship.score).zfill(5), WHITE)


def update():
    laser_group.update()
    ship.update()
    meteor_group.update()
    check_laser_collision()
    check_ship_collision()


def check_laser_collision():
    for laser in laser_group:
        if p.sprite.spritecollide(laser, meteor_group, True):
            hit_meteor_sound.play()
            laser.kill()
            ship.score += 1


def check_ship_collision():
    # If the returned list is empty, it evaluates to False.
    # Otherwise - to True.
    if p.sprite.spritecollide(ship, meteor_group, True):
        hit_ship_sound.play()
        ship.get_damage(1)


def make_laser():
    fire_laser_sound.play()
    laser_group.add(sprites.Laser(ship.rect.center, laser_img))
    fire_laser_sound.play()


def make_meteor():
    meteor_image = rnd.choice(meteor_images)
    meteor = sprites.Meteor((rnd.randint(0, SCREEN_WIDTH), -20),
                            meteor_image)
    meteor_group.add(meteor)


p.init()
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
hp_img = p.image.load('res/PNG/UI/playerLife1_orange.png')
x_img = p.image.load('res/PNG/UI/numeralX.png')

# Loading sounds
fire_laser_sound = p.mixer.Sound('res/Bonus/sfx_laser1.ogg')
hit_meteor_sound = p.mixer.Sound('res/Bonus/meteor_hit.wav')
hit_ship_sound = p.mixer.Sound('res/Bonus/hit.wav')
game_over_sound = p.mixer.Sound('res/Bonus/sfx_lose.ogg')
new_game_sound = p.mixer.Sound('res/Bonus/sfx_twoTone.ogg')
bg_music = p.mixer.Sound('res/Bonus/space_ambiance.wav')

# Initializing the game window
clock = p.time.Clock()
screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
p.display.set_caption('Asteroids')

ship = sprites.Spaceship((SCREEN_WIDTH/2, SCREEN_HEIGHT-50),
                         ship_images)
score_font = p.freetype.Font('res/Bonus/kenvector_future.ttf', 32)

# Making groups
meteor_group = p.sprite.Group()
laser_group = p.sprite.GroupSingle()

# Making a timer for meteors
SPAWN_METEOR = p.USEREVENT
p.time.set_timer(SPAWN_METEOR, 300)

bg_music.play(-1)
running = True
while running:
    for event in p.event.get():
        if event.type == p.QUIT or (event.type == p.KEYDOWN
                                    and event.key == p.K_ESCAPE):
            running = False

        if event.type == SPAWN_METEOR:
            make_meteor()
        if event.type == p.MOUSEBUTTONDOWN:
            if len(laser_group) == 0:
                make_laser()

    draw()
    update()

    clock.tick(60)
    p.display.flip()

