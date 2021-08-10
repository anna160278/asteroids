import random as rnd
import pygame as p
from settings import *


class Spaceship:
    def __init__(self, pos, images):
        self.start_pos = pos
        self.image = images[0]
        self.images = images
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.hp = 4
        self.score = 0
        self.DESTROY_EVENT = p.USEREVENT + 1

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
            if self.hp == 0:
                p.event.post(p.event.Event(self.DESTROY_EVENT))

    def rebuild(self):
        self.hp = 4
        self.score = 0
        self.is_alive = True
        self.rect.center = self.start_pos


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


class Button():
    def __init__(self, pos, text, font):
        super().__init__()
        self.image = p.Surface((450, 80))
        self.image.fill('#e09f23')
        self.rect = self.image.get_rect(center=pos)

        self.text_surf, self.text_rect = font.render(text, size=42)
        self.text_rect.center = self.rect.center

    def draw(self, target_surf):
        target_surf.blit(self.image, self.rect)
        target_surf.blit(self.text_surf, self.text_rect)

