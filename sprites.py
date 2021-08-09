import random as rnd
import pygame as p
from settings import *


class Spaceship:
    def __init__(self, pos, images):
        self.image = images[0]
        self.images = images
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.hp = 4

    def draw(self, target_surf):
        if self.hp > 0:
            target_surf.blit(self.image, self.rect)
            if self.hp < 4:
                target_surf.blit(self.images[-self.hp], self.rect)

    def update(self):
        self.move()
        self.restrain()

    def move(self):
        keys = p.key.get_pressed()
        if keys[p.K_a]:
            self.rect.x -= 5
        if keys[p.K_d]:
            self.rect.x += 5
        if keys[p.K_w]:
            self.rect.y -= 5
        if keys[p.K_s]:
            self.rect.y += 5

    def restrain(self):
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def get_damage(self, damage):
        if self.hp > 0:
            self.hp -= damage


class Meteor(p.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.speed_x = rnd.randint(-3, 3)
        self.speed_y = rnd.randint(3, 9)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()


class Laser(p.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

