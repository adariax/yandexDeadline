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
GOEVENT = 30

all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
pygame.time.set_timer(GOEVENT, 15)


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class CompilationError(pygame.sprite.Sprite):
    image = load_image("data\\mobs\\mob_1.png", (0, 0, 0))

    def __init__(self, group, width, height):
        super().__init__(group)
        self.image = CompilationError.image
        self.rect = self.image.get_rect()
        self.rect.x = width
        self.rect.y = height
        self.vx = 3

    def update(self):
        self.rect = self.rect.move(self.vx, 0)
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


class RuntimeError(pygame.sprite.Sprite):
    image = load_image("data\\mobs\\mob_3.png", (0, 0, 0))

    def __init__(self, group, width, height):
        super().__init__(group)
        self.image = RuntimeError.image
        self.rect = self.image.get_rect()
        self.rect.x = width
        self.rect.y = height
        self.vy = 3

    def update(self):
        self.rect = self.rect.move(0, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy


class WrongAnswer(pygame.sprite.Sprite):
    image = load_image("data\\mobs\\mob_2.png", (0, 0, 0))

    def __init__(self, group, width, height):
        super().__init__(group)
        self.image = WrongAnswer.image
        self.rect = self.image.get_rect()
        self.rect.x = width
        self.rect.y = height
        self.vx = 2
        self.vy = 2

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx

Border(5, 5, 300 - 5, 5)
Border(5, 300 - 5, 300 - 5, 300 - 5)
Border(5, 5, 5, 300 - 5)
Border(300 - 5, 5, 300 - 5, 300 - 5)
CompilationError(all_sprites, 200, 200)
RuntimeError(all_sprites, 200, 200)
WrongAnswer(all_sprites, 200, 200)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == GOEVENT:
            all_sprites.update()

        screen.fill((100, 100, 100))
        all_sprites.draw(screen)
        vertical_borders.draw(screen)
        horizontal_borders.draw(screen)

    pygame.display.flip()