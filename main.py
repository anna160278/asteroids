import os
import random as rnd

import pygame as p
import pygame.freetype

import sprites
from settings import *


def draw_game():
    screen.blit(background_img, (0, 0))
    laser_group.draw(screen)
    ship.draw(screen)
    meteor_group.draw(screen)

    screen.blit(hp_img, (20, 20))
    screen.blit(x_img, (60, 28))
    score_font.render_to(screen, (85, 23), str(ship.hp), WHITE)
    score_font.render_to(screen, (SCREEN_WIDTH-180, 23), 
                         str(ship.score).zfill(5), WHITE)


def draw_menu():
    screen.fill(VIOLET)
    screen.blit(game_over_surf, game_over_rect)
    button.draw(screen)
    screen.blit(hp_img, (20, 20))
    screen.blit(x_img, (60, 28))
    score_font.render_to(screen, (80, 23), str(ship.hp), WHITE)
    score_font.render_to(screen, (SCREEN_WIDTH-180, 23),
                         str(ship.score).zfill(5), WHITE)


def update_game():
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


def stop_game():
    p.mouse.set_visible(True)
    # Either fadeout or game_over_sound
    bg_music.fadeout(5000)
    meteor_group.empty()
    laser_group.empty()


def restart_game():
    p.mouse.set_visible(False)
    new_game_sound.play()
    bg_music.play(-1)
    ship.rebuild()


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
game_state = 'MAIN GAME'    # MAIN GAME or MENU

ship = sprites.Spaceship((SCREEN_WIDTH/2, SCREEN_HEIGHT-50),
                         ship_images)
# Fonts
score_font = p.freetype.Font('res/Bonus/kenvector_future.ttf', 32)
text_font = p.freetype.Font('res/Bonus/kenvector_future.ttf', 52)

# Text and buttons
button = sprites.Button((SCREEN_WIDTH/2, SCREEN_HEIGHT/2),
                        'restart', text_font)
game_over_surf, game_over_rect = text_font.render("game over")
game_over_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/3)

# Making groups
meteor_group = p.sprite.Group()
laser_group = p.sprite.GroupSingle()

# Making a timer for meteors
SPAWN_METEOR = p.USEREVENT
p.time.set_timer(SPAWN_METEOR, 300)

p.mouse.set_visible(False)
bg_music.play(-1)

running = True
while running:
    for event in p.event.get():
        if event.type == p.QUIT or (event.type == p.KEYDOWN
                                    and event.key == p.K_ESCAPE):
            running = False

        if game_state == 'MAIN GAME':
            if event.type == SPAWN_METEOR:
                make_meteor()
            if event.type == p.MOUSEBUTTONDOWN:
                if len(laser_group) == 0:
                    make_laser()
            if event.type == ship.DESTROY_EVENT:
                game_state = 'MENU'
                stop_game()
        else:
            if (event.type == p.MOUSEBUTTONDOWN
                    and button.rect.collidepoint(event.pos)):
                game_state = 'MAIN GAME'
                restart_game()

    if game_state == 'MAIN GAME':
        draw_game()
        update_game()
    else:
        draw_menu()

    clock.tick(60)
    p.display.flip()

