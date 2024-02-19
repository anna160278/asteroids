import os
import random as rnd

import pygame as pg
import pygame.freetype

import sprites
from settings import *


def draw_game():
    screen.blit(background_img, (0, 0))
    laser_group.draw(screen)
    ship.draw(screen)
    meteor_group.draw(screen)
    powerup_group.draw(screen)

    screen.blit(hp_img, (20, 20))
    screen.blit(x_img, (60, 28))
    score_font.render_to(screen, (85, 23), str(ship.hp), WHITE)
    score_font.render_to(screen, (SCREEN_WIDTH - 180, 23), str(ship.score).zfill(5), WHITE)


def draw_menu():
    screen.fill(VIOLET)
    screen.blit(game_over_surf, game_over_rect)
    button.draw(screen)
    quit_button.draw(screen)
    screen.blit(hp_img, (20, 20))
    screen.blit(x_img, (60, 28))
    score_font.render_to(screen, (80, 23), str(ship.hp), WHITE)
    score_font.render_to(screen, (SCREEN_WIDTH - 180, 23), str(ship.score).zfill(3), WHITE)


def update_game():
    laser_group.update()
    ship.update()
    meteor_group.update()
    powerup_group.update()
    check_laser_collision()
    check_ship_collision()
    check_powerup_collision()


def check_laser_collision():
    for laser in laser_group:
        if pg.sprite.spritecollide(laser, meteor_group, True):
            hit_meteor_sound.play()
            laser.kill()
            ship.score += 1


def check_ship_collision():
    # If the returned list is empty, it evaluates to False.
    # Otherwise - to True.
    if pg.sprite.spritecollide(ship, meteor_group, True):
        hit_ship_sound.play()
        ship.get_damage(1)


def check_powerup_collision():
    powerup = pg.sprite.spritecollideany(ship, powerup_group)
    if powerup == None:
        return
    if powerup.type == 'shield':
        ship.apply_shield()
        powerup.kill()
    # Placeholder for the next homework
    elif powerup.type == 'bolt':
        ship.apply_laserx2()
        powerup.kill()


def make_laser():
    fire_laser_sound.play()
    for i in range(ship.laser_count):
        x, y = ship.rect.center
        laser_group.add(sprites.Laser((x, y + i * 100), laser_images))
    fire_laser_sound.play()


def make_meteor():
    meteor_image = rnd.choice(meteor_images)
    meteor = sprites.Meteor((rnd.randint(0, SCREEN_WIDTH), -20), meteor_image)
    meteor_group.add(meteor)


def make_powerup():
    random_number = rnd.randint(0, 100)
    pos = (rnd.randint(0, SCREEN_WIDTH), -20)
    if random_number % 2 == 0:
        powerup = sprites.PowerUp(pos, power_ups['shield'], 'shield')
        powerup_group.add(powerup)
    else:
        powerup = sprites.PowerUp(pos, power_ups['bolt'], 'bolt')
        powerup_group.add(powerup)


def stop_game():
    pg.mouse.set_visible(True)
    # Either fadeout or game_over_sound
    bg_music.fadeout(5000)
    meteor_group.empty()
    laser_group.empty()


def restart_game():
    pg.mouse.set_visible(False)
    new_game_sound.play()
    bg_music.play(-1)
    ship.rebuild()
    ship.laserx1()


pg.init()
# Loading images
background_img = pg.image.load('res/Backgrounds/darkPurple.png')
background_img = pg.transform.scale(background_img,
                                    (SCREEN_WIDTH, SCREEN_HEIGHT))
laser_img = pg.image.load("res/PNG/Lasers/laserRed01.png")
meteor_images = [pg.image.load('res/PNG/Meteors/' + name)
                 for name in os.listdir('res/PNG/Meteors')]
ship_images = [pg.image.load(f'res/PNG/Damage/playerShip1_damage{i}.png')
               for i in range(1, 4)]
ship_images.insert(0, pg.image.load('res/PNG/playerShip1_orange.png'))
hp_img = pg.image.load('res/PNG/UI/playerLife1_orange.png')
x_img = pg.image.load('res/PNG/UI/numeralX.png')

laser_images = [pg.image.load(f'res/PNG/Lasers/laserBlue{i}.png')
                for i in range(12, 17)]
thruster_images = [pg.image.load(f'res/PNG/Effects/fire{i}.png')
                   for i in range(11, 18)]
power_ups = {'shield': pg.image.load('res/PNG/Power-ups/shield_gold.png'),
             'bolt': pg.image.load('res/PNG/Power-ups/bolt_gold.png'), }
shield_images = [pg.image.load(f'res/PNG/Effects/shield{i}.png')
                 for i in range(1, 4)]

# Loading sounds
fire_laser_sound = pg.mixer.Sound('res/Bonus/sfx_laser1.ogg')
hit_meteor_sound = pg.mixer.Sound('res/Bonus/meteor_hit.wav')
hit_ship_sound = pg.mixer.Sound('res/Bonus/hit.wav')
game_over_sound = pg.mixer.Sound('res/Bonus/sfx_lose.ogg')
new_game_sound = pg.mixer.Sound('res/Bonus/sfx_twoTone.ogg')
# bg_music = pg.mixer.Sound('res/Bonus/space_ambiance.wav')
bg_music = pg.mixer.Sound('res/Bonus/background_music.mp3')

# Initializing the game window
clock = pg.time.Clock()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Asteroids')
game_state = 'MAIN GAME'  # MAIN GAME or MENU

ship = sprites.Spaceship((SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50),
                         ship_images, thruster_images, shield_images)
# Fonts
score_font = pg.freetype.Font('res/Bonus/kenvector_future.ttf', 32)
text_font = pg.freetype.Font('res/Bonus/kenvector_future.ttf', 52)

# Text and buttons
button = sprites.Button((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), 'restart', text_font)
quit_button = sprites.Button((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100), 'quit', text_font)
game_over_surf, game_over_rect = text_font.render("game over")
game_over_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)

# Making groups
meteor_group = pg.sprite.Group()
laser_group = pg.sprite.Group()
powerup_group = pg.sprite.Group()

# Making a timer for meteors
SPAWN_METEOR = pg.USEREVENT
pg.time.set_timer(SPAWN_METEOR, 300)
# Making a timer for buffs
SPAWN_POWERUP = pg.USEREVENT + 2
pg.time.set_timer(SPAWN_POWERUP, 3000)

pg.mouse.set_visible(False)
bg_music.play(-1)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN
                                     and event.key == pg.K_ESCAPE):
            running = False

        if game_state == 'MAIN GAME':
            if event.type == SPAWN_METEOR:
                make_meteor()
            elif event.type == SPAWN_POWERUP:
                make_powerup()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if len(laser_group) == 0:
                    make_laser()
            elif event.type == ship.DESTROY_EVENT:
                game_state = 'MENU'
                stop_game()
        else:
            if event.type == pg.MOUSEBUTTONDOWN:
                if button.rect.collidepoint(event.pos):
                    game_state = 'MAIN GAME'
                    restart_game()
                if quit_button.rect.collidepoint(event.pos):
                    running = False

    if game_state == 'MAIN GAME':
        draw_game()
        update_game()
    else:
        draw_menu()

    clock.tick(60)
    pg.display.flip()
