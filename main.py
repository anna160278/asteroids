import pygame as p
import sprites


SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

# Loading images
ship_img = p.image.load('res/PNG/playerShip1_orange.png')

# Initializing the game window
p.init()
clock = p.time.Clock()
screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
p.display.set_caption('Asteroids')

ship = sprites.Spaceship((SCREEN_WIDTH/2, SCREEN_HEIGHT-50),
                         ship_img)

running = True
while running:
    for event in p.event.get():
        if event.type == p.QUIT or (event.type == p.KEYDOWN
                                    and event.key == p.K_ESCAPE):
            running = False

    ship.draw(screen)
    ship.move()

    clock.tick(60)
    p.display.flip()

