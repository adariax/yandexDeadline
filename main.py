import pygame
import os


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    print(fullname)
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
FPS = 15

clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()


class Character(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.x = x
        self.y = y
        self.frames = 11
        self.vx = 0
        self.vy = 0

        self.direction = 0
        self.cur_frame = 0
        self.status = 'standing'

        # forward - 0, left - 1, back - 2, right - 3

        self.images = {}
        for status in ['standing']:  # , 'walking'
            for direction in range(4):
                self.images[status] = [[0] * 11] * 4
                for number_file in range(11):
                    if direction != 2:  # DELETE THIS
                        name = ['data', 'character', status, str(direction), f'{number_file + 1}.png']
                        print(name)
                        self.images[status][direction][number_file] = load_image('\\'.join(name),
                                                                                 (0, 0, 0))
        self.image = self.images[self.status][self.direction][self.cur_frame]
        self.rect = self.image.get_rect()

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] ^ keys[pygame.K_RIGHT]:
            # self.status = 'walking'
            self.direction = 1 if keys[pygame.K_LEFT] else 3
            self.vx = -10 if keys[pygame.K_LEFT] else 10
            self.x += self.vx
        elif keys[pygame.K_UP] ^ keys[pygame.K_DOWN]:
            # self.status = 'walking'
            self.direction = 0
            self.vy = -10 if keys[pygame.K_UP] else 10
            self.y += self.vy
        else:
            self.vx = 0
            self.vy = 0
            self.status = 'standing'

        self.image = self.images[self.status][self.direction][self.cur_frame % self.frames]
        self.cur_frame += 1
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y


Character(all_sprites, 250, 200)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((100, 100, 100))
    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.flip()

    clock.tick(FPS)
