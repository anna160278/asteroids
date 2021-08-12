import random as rnd
import pygame as p
from settings import *


class Spaceship:
    def __init__(self, pos, images, thruster_images,
                 shield_images):
        self.start_pos = pos
        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.frame = 0
        self.thruster_images = thruster_images
        self.thruster_animation_len = len(thruster_images)

        self.shield_power = 0
        self.shield_images = shield_images
        self.shield_rect = shield_images[0].get_rect()

        self.hp = 4
        self.score = 0
        self.DESTROY_EVENT = p.USEREVENT + 1

    def draw(self, target_surf):
        if self.hp > 0:
            target_surf.blit(self.image, self.rect)
            if self.hp < 4:
                target_surf.blit(self.images[-self.hp], self.rect)
        self.draw_thurster(target_surf)
        self.draw_shield(target_surf)

    def draw_thurster(self, target_surf):
        self.frame += 0.5
        if int(self.frame) == self.thruster_animation_len:
            self.frame = 0
        img = self.thruster_images[int(self.frame)]

        # x positions are different because we are placing
        # the top left corner of the image
        l_thruster_pos = (self.rect.centerx-35, self.rect.bottom-18)
        r_thruster_pos = (self.rect.centerx+21, self.rect.bottom-18)
        target_surf.blit(img, l_thruster_pos)
        target_surf.blit(img, r_thruster_pos)

    def draw_shield(self, target_surf):
        if self.shield_power > 0:
            self.shield_rect.center = self.rect.center
            if self.shield_power != 1:
                # Compensating for the thicker border
                # of the second and third shield image
                self.shield_rect.move_ip((-5, -5))
            target_surf.blit(self.shield_images[self.shield_power-1],
                             self.shield_rect)

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
        if self.shield_power > 0:
            self.shield_power -= damage
        else:
            self.hp -= damage
            if self.hp == 0:
                p.event.post(p.event.Event(self.DESTROY_EVENT))

    def rebuild(self):
        self.hp = 4
        self.score = 0
        self.is_alive = True
        self.rect.center = self.start_pos
        
    def apply_shield(self):
        self.shield_power = 3

    def apply_laserx2(self):
        pass


class Meteor(p.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.speed_x = rnd.randint(-3, 3)
        self.speed_y = rnd.randint(3, 9)

        self.original_image = image
        self.angle = 0
        self.rotation_speed = rnd.randint(-3, 3)

    def update(self):
        self.rotate()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()

    def rotate(self):
        self.angle += self.rotation_speed
        self.image = p.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)


class Laser(p.sprite.Sprite):
    def __init__(self, pos, images):
        super().__init__()
        self.images = images
        self.image = self.images[0]
        self.animation_len = len(self.images)
        self.frame = 0
        self.rect = self.image.get_rect(center=pos)
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

        # Animating
        self.frame += 0.25
        if int(self.frame) == self.animation_len:
            self.frame = 0
        self.image = self.images[int(self.frame)]
        
        # More concise way
        # self.frame = (self.frame + 1) % self.animation_len
        # self.image = self.images[self.frame]


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


class PowerUp(p.sprite.Sprite):
    def __init__(self, pos, image, _type):
        super().__init__()
        self.image = image
        self.type = _type
        self.rect = self.image.get_rect(center=pos)
        self.speed_y = rnd.randint(1, 6)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()
