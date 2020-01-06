import pygame
from random import choice
from func import load_image

pygame.init()
WIDTH = 600
HEIGHT = 200
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
screen.fill((100, 100, 100))

running = True
MOVEEVENT = 30
GOEVENT = 31

pygame.time.set_timer(GOEVENT, 15)
pygame.time.set_timer(MOVEEVENT, 100)
clock = pygame.time.Clock()

FPS = 20
all_sprites = pygame.sprite.Group()
tasks = pygame.sprite.Group()
character = pygame.sprite.Group()
enemies = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()

collected_tasks = 0


class Map(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)

        self.image = pygame.Surface([0, 0])
        self.image = load_image('data\\map\\map02.png')
        # self.image = pygame.transform.scale(self.image, (1100, 209))

        self.rect = self.image.get_rect()
        self.rect.x = - WIDTH // 2 + 24
        self.rect.y = - HEIGHT // 2 + 32


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(character)
        self.x = x
        self.y = y
        self.frames = 11
        self.vx = 0
        self.vy = 0

        self.direction = 0
        self.cur_frame = 0
        self.images_standing = [[], [], [], []]
        self.images_walking = [[], [], [], []]
        self.image = None
        self.mask = None
        # forward - 0, left - 1, back - 2, right - 3

        for direction in range(4):
            for number_file in range(11):
                name = ['data', 'character', 'standing', str(direction), f'{number_file + 1}.png']
                self.images_standing[direction].append(load_image('\\'.join(name)))
        for direction in range(4):
            for number_file in range(11):
                name = ['data', 'character', 'walking', str(direction), f'{number_file + 1}.png']
                self.images_walking[direction].append(load_image('\\'.join(name)))

        self.image = self.images_standing[0][self.cur_frame]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.Mask((48, 64), True)

    def check_vertical_wall(self, current_direction, new_direction):
        if pygame.sprite.spritecollideany(self, vertical_borders) \
                and current_direction == new_direction:
            return False
        else:
            return True

    def check_horizontal_wall(self, current_direction, new_direction):
        if pygame.sprite.spritecollideany(self, horizontal_borders) \
                and current_direction == new_direction:
            return False
        else:
            return True

    def update(self):
        keys = pygame.key.get_pressed()
        moving = False
        direction = self.direction

        if keys[pygame.K_LEFT] ^ keys[pygame.K_RIGHT]:
            direction = 1 if keys[pygame.K_LEFT] else 3
            self.vx = -10 if keys[pygame.K_LEFT] else 10
            self.rect.x += self.vx if \
                self.check_vertical_wall(self.direction, direction) else -1 if self.vx > 0 else 1
            moving = True
        elif keys[pygame.K_UP] ^ keys[pygame.K_DOWN]:
            direction = 2 if keys[pygame.K_UP] else 0
            self.vy = 10 if keys[pygame.K_DOWN] else -10
            self.rect.y += self.vy \
                if self.check_horizontal_wall(self.direction, direction) \
                else -1 if self.vy > 0 else 1
            moving = True

        self.image = self.images_standing[self.direction][self.cur_frame % self.frames] \
            if not moving else self.images_walking[self.direction][self.cur_frame % self.frames]
        self.cur_frame += 1
        self.direction = direction
        # self.rect = self.image.get_rect()
        # self.rect.x, self.rect.y = self.x, self.y


class Tasks(pygame.sprite.Sprite):
    image = load_image(f"data\\tasks\\{choice(['task_1.png', 'task_2.png', 'task_3.png'])}",
                       (0, 0, 0))

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(tasks)
        self.image = Tasks.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.save_y = self.rect.y
        self.upd = 0

    def update(self):
        global collected_tasks
        if pygame.sprite.spritecollideany(self, character):
            collected_tasks += 1
            self.kill()
        self.upd += 1
        if self.upd % 4 == 1:
            self.rect.y += 1
        elif self.upd % 4 == 2:
            self.rect.y += 1
        elif self.upd % 4 == 3:
            self.rect.y += 1
        else:
            self.rect.y = self.save_y


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

    def __init__(self, width, height):
        super().__init__(all_sprites)
        self.add(enemies)
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

    def __init__(self, width, height):
        super().__init__(all_sprites)
        self.add(enemies)
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

    def __init__(self, width, height):
        super().__init__(all_sprites)
        self.add(enemies)
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

map_level = Map()

Border(5, 5, 450, 5)
Border(5, 5, 5, 300)
Border(5, 300, 150, 300)
Border(150, 300, 150, 450)
Border(150, 450, 450, 450)
Border(450, 5, 450, 450)
CompilationError(200, 200)
RuntimeError(200, 200)
WrongAnswer(200, 200)

player = Character(388, 268)
camera = Camera()

# create all possible coord
tasks_places = [(50, 40)]
for _ in range(1):
    Tasks(*choice(tasks_places))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == MOVEEVENT:
            tasks.update()
        if event.type == GOEVENT:
            enemies.update()

    character.update()
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)

    screen.fill((100, 100, 100))
    screen.blit(map_level.image, (-388, -268))  # выравнить для персонажа
    character.draw(screen)
    all_sprites.draw(screen)
    vertical_borders.draw(screen)
    horizontal_borders.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
