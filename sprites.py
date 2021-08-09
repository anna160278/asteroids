import random as rnd
import pygame as p
from settings import *


class Spaceship:
    def __init__(self, pos, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def draw(self, target_surf):
        target_surf.blit(self.image, self.rect)

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

