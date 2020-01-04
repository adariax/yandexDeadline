import pygame
import os
from random import choice


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
MOVEEVENT = 30

all_sprites = pygame.sprite.Group()
pygame.time.set_timer(MOVEEVENT, 100)


class Tasks(pygame.sprite.Sprite):
    image = load_image(f"data\\tasks\\ + {choice(['task_1.png', 'task_2.png', 'task_3.png'])}",
                       (0, 0, 0))

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = Tasks.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.save_y = self.rect.y
        self.upd = 0

    def update(self):
        self.upd += 1
        if self.upd % 4 == 1:
            self.rect.y += 1
        elif self.upd % 4 == 2:
            self.rect.y += 1
        elif self.upd % 4 == 3:
            self.rect.y += 1
        else:
            self.rect.y = self.save_y


# create all possible coord
tasks_places = [(50, 40)]
for _ in range(1):
    Tasks(all_sprites, *choice(tasks_places))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == MOVEEVENT:
            all_sprites.update()

        screen.fill((100, 100, 100))
        all_sprites.draw(screen)

    pygame.display.flip()
