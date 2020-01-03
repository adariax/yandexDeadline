import pygame
import os


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pygame.init()

size = (500, 500)
screen = pygame.display.set_mode(size)
screen.fill((100, 100, 100))

running = True
FPS = 60
TRIG_FRAME = 5

clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()


class Character(pygame.sprite.Sprite):
    images = {}
    for status in ['standing', 'walking']:
        for direction in ['forward', 'left', 'right', 'back']:
            eval(f'images[{status}] = [[] * 11]')
    image = load_image('', (0, 0, 0))

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = Character.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.direction = 'f'
        self.stand_still = True

    def update(self):
        self.image = self.frames[self.cur_frame // TRIG_FRAME]
        self.cur_frame = (self.cur_frame + 1) % (len(self.frames) * TRIG_FRAME)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        screen.fill((100, 100, 100))
        all_sprites.draw(screen)

    pygame.display.flip()

    clock.tick(FPS)
