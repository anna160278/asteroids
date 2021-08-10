import pygame as p


class Frog(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.is_animating = False
        self.sprites = [p.image.load(f'attack_{i}.png')
                        for i in range(1, 11)]
        self.frame = 0
        self.image = self.sprites[self.frame]
        self.rect = self.image.get_rect(center=(140, 140))

    def animate(self):
        self.is_animating = True

    def draw(self, target_surf):
        target_surf.blit(self.image, self.rect)

    def update(self, speed):
        if self.is_animating:
            self.frame += speed
            if int(self.frame) == len(self.sprites):
                self.frame = 0
                self.is_animating = False
        self.image = self.sprites[int(self.frame)]


SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300

p.init()
clock = p.time.Clock()
screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
p.display.set_caption('Frog')

frog = Frog()

running = True
while running:
    for event in p.event.get():
        if event.type == p.QUIT or (event.type == p.KEYDOWN
                                    and event.key == p.K_ESCAPE):
            running = False

        if event.type == p.KEYDOWN and event.key == p.K_SPACE:
            frog.animate()

    screen.fill((255, 255, 255))

    frog.update(0.25)
    frog.draw(screen)

    clock.tick(60)
    p.display.flip()

