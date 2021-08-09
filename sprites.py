import pygame as p


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


