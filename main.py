import pygame
import sys
from random import choice
from func import load_image
from coords import create_borders_coords

pygame.init()
pygame.font.init()

WIDTH = 800
HEIGHT = 400
X = - WIDTH // 2
Y = - HEIGHT // 2
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Deadline')
screen.fill((0, 0, 0))

running = True
MOVEEVENT = 30
GOEVENT = 31

pygame.time.set_timer(GOEVENT, 15)
pygame.time.set_timer(MOVEEVENT, 100)
clock = pygame.time.Clock()
millisec = 0

FPS = 20
all_sprites = pygame.sprite.Group()
tasks = pygame.sprite.Group()
character = pygame.sprite.Group()
enemies = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()

collected_tasks = 0
points = 3000


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('data\\screen.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    intro_text = ['DEADLINE',
                  '',
                  "Соберите все задачи до того, как закончится время",
                  "Но будьте осоторжны! Не наткнитесь на ошибки:",
                  "они отнимают ваши драгоценные секунды",
                  "Не забудьте сдать все задачи, дойдя до компьютера",
                  '',
                  "Упрвление стрелками;",
                  "чтобы собрать задачу, достаточно подойти к ней.",
                  '',
                  "ДЛЯ НАЧАЛА НАЖМИТЕ ЛЮБУЮ КНОПКУ"]
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 30
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(246, 200, 159))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def endgame_screen():  # ДОПИСАТЬ
    fon = pygame.transform.scale(load_image('data\\screen.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    line = 'GAME OVER'
    font1 = pygame.font.Font(None, 50)
    string_rendered1 = font1.render(line, True, pygame.Color(63, 40, 60))
    screen.blit(string_rendered1, (698, 350))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()


def time_check(time):
    return True if time < 1440 else False


def time_left(time):
    left_millisec = 1440 - time
    return (left_millisec % 60, left_millisec // 60)


def show_time(time):
    minutes, hours = time_left(time)
    line = f'{hours}:{str(minutes) if minutes >= 10 else str(0) + str(minutes)}'
    font1 = pygame.font.Font(None, 33)
    font2 = pygame.font.Font(None, 30)

    string_rendered1 = font1.render(line, True, pygame.Color(63, 40, 60))
    string_rendered2 = font2.render(line, True, pygame.Color(255, 0, 68))
    screen.blit(string_rendered1, (698, 350))
    screen.blit(string_rendered2, (700, 350))


def get_points(tasks, time):
    global points
    return points + tasks * 100 - time * 5


def show_points(tasks, time):
    line = f'points: {get_points(tasks, time)}'
    font = pygame.font.Font(None, 33)

    string_rendered = font.render(line, True, pygame.Color(38, 43, 68))
    screen.blit(string_rendered, (60, 350))


class Map(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)

        self.image = pygame.Surface([0, 0])
        self.image = load_image('data\\map\\map.png')
        self.image = pygame.transform.scale(load_image('data\\map\\map.png'), (3000, 506))

        self.rect = self.image.get_rect()
        self.rect.x = - WIDTH // 2
        self.rect.y = - HEIGHT // 2 - 20


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
        # forward - 0, left - 1, back - 2, right - 3
        for status in ('standing', 'walking'):
            for direction in range(4):
                for number_file in range(11):
                    path = f'data\\character\\{status}\\{str(direction)}\\{number_file + 1}.png'
                    image = load_image(path)
                    image = pygame.transform.scale(image,
                                                   (image.get_rect().w * 2, image.get_rect().h * 2))
                    eval(f'self.images_{status}[direction].append(image)')

        self.image = self.images_standing[0][self.cur_frame]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.Mask((self.rect.w, self.rect.h), False)
        for x in range(self.rect.w // 4, self.rect.w // 4 * 3):
            for y in range(self.rect.h // 9 * 8, self.rect.h):
                self.mask.set_at((x, y), 1)

    def update(self):
        keys = pygame.key.get_pressed()
        moving = False

        global millisec
        if pygame.sprite.spritecollideany(self, enemies, collided=pygame.sprite.collide_mask):
            millisec += 20

        if keys[pygame.K_LEFT] ^ keys[pygame.K_RIGHT]:
            self.direction = 1 if keys[pygame.K_LEFT] else 3
            self.vx = -10 if keys[pygame.K_LEFT] else 10
            self.rect.x += self.vx \
                if not pygame.sprite.spritecollideany(self, vertical_borders,
                                                      collided=pygame.sprite.collide_mask) else 0
            moving = True
        elif keys[pygame.K_UP] ^ keys[pygame.K_DOWN]:
            self.direction = 2 if keys[pygame.K_UP] else 0
            self.vy = 10 if keys[pygame.K_DOWN] else -10
            self.rect.y += self.vy \
                if not pygame.sprite.spritecollideany(self, horizontal_borders,
                                                      collided=pygame.sprite.collide_mask) else 0
            moving = True

        while pygame.sprite.spritecollideany(self, vertical_borders,
                                             collided=pygame.sprite.collide_mask):
            self.rect.x += 1 if self.vx <= 0 else -1
        while pygame.sprite.spritecollideany(self, horizontal_borders,
                                             collided=pygame.sprite.collide_mask):
            self.rect.y += 1 if self.vy <= 0 else -1

        self.image = self.images_standing[self.direction][self.cur_frame % self.frames] \
            if not moving else self.images_walking[self.direction][self.cur_frame % self.frames]
        self.cur_frame += 1


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
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global collected_tasks
        global millisec

        if pygame.sprite.spritecollideany(self, character, collided=pygame.sprite.collide_mask):
            collected_tasks += 1
            millisec += 30
            self.kill()


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
            self.mask = pygame.mask.Mask((1, y2 - y1), True)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
            self.mask = pygame.mask.Mask((x2 - x1, 1), True)
        self.image.set_alpha(0)


class InteriorItems(pygame.sprite.Sprite):
    def __init__(self, x, y, name, bottom_top_y=150, borders=True):
        super().__init__(all_sprites)
        image = load_image('data\\furniture\\' + name)
        self.image = pygame.transform.scale(image, (image.get_rect().w * 2, image.get_rect().h * 2))
        self.rect = self.image.get_rect()
        self.rect.x = X + x
        self.rect.y = Y + y
        self.bottom_top_y = Y + bottom_top_y

        if borders:
            Border(self.rect.x, self.bottom_top_y,
                   self.rect.x, self.rect.y + self.rect.h)
            Border(self.rect.x, self.bottom_top_y,
                   self.rect.x + self.rect.w, self.bottom_top_y)
            Border(self.rect.x, self.rect.y + self.rect.h,
                   self.rect.x + self.rect.w, self.rect.y + self.rect.h)
            Border(self.rect.x + self.rect.w, self.bottom_top_y,
                   self.rect.x + self.rect.w, self.rect.y + self.rect.h)


class Bath(InteriorItems):
    def __init__(self, x, y):
        super().__init__(x, y, 'bath.png')


class Bed(InteriorItems):
    def __init__(self, x, y, name='bed.png'):
        super().__init__(x, y, name)


class BigBed(Bed):
    def __init__(self, x, y):
        super().__init__(x, y, 'bigbed.png')


class Carpet(InteriorItems):
    def __init__(self, x, y):
        super().__init__(x, y, 'carpet.png', False)


class Chair(InteriorItems):
    def __init__(self, x, y, y_coord=150):
        super().__init__(x, y, 'chair.png', y_coord)


class Chest(InteriorItems):
    def __init__(self, x, y, y_coord=150):
        super().__init__(x, y, 'chest.png', y_coord)
        self.bottom_top_y = self.rect.h // 4 * 3


class Computer(InteriorItems):
    def __init__(self, x, y):
        super().__init__(x, y, 'computer.png')

    def update(self, *args):
        pass


class Table(InteriorItems):
    def __init__(self, x, y, y_coord=150):
        super().__init__(x, y, 'table.png')
        self.bottom_top_y = self.rect.h // 3 * 2


class Toilet(InteriorItems):
    def __init__(self, x, y):
        super().__init__(x, y, 'toilet.png')
        self.bottom_top_y = self.rect.h // 6 * 5


class Wallchest(InteriorItems):
    def __init__(self, x, y):
        super().__init__(x, y, 'wallchest.png', 0, False)


class Walllamp(InteriorItems):
    def __init__(self, x, y):
        super().__init__(x, y, 'walllamp.png', 0, False)


class Wardrobe(InteriorItems):
    def __init__(self, x, y):
        super().__init__(x, y, 'wardrobe.png')


class Washingmachine(InteriorItems):
    def __init__(self, x, y):
        super().__init__(x, y, 'washingmachine.png')


class Window(InteriorItems):
    def __init__(self, x, y):
        super().__init__(x, y, 'window.png', borders=False)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__(all_sprites)
        self.add(enemies)
        self.image = load_image('data\\mobs\\' + name)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 2
        self.vy = 3

        self.mask = pygame.mask.Mask((self.rect.w, self.rect.h), False)
        for x in range(self.rect.w):
            for y in range(self.rect.h // 9 * 8, self.rect.h):
                self.mask.set_at((x, y), 1)


class CompilationError(Enemy):
    def __init__(self, width, height):
        super().__init__(width, height, "mob_1.png")
        self.vy = 0

    def update(self):
        self.rect = self.rect.move(self.vx, 0)
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


class RuntimeError(Enemy):
    def __init__(self, width, height):
        super().__init__(width, height, "mob_3.png")

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        elif pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


class WrongAnswer(Enemy):
    def __init__(self, width, height):
        super().__init__(width, height, "mob_2.png")
        self.vx = 0

    def update(self):
        self.rect = self.rect.move(0, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy


start_screen()

camera = Camera()
map_level = Map()

borders_coords = create_borders_coords(map_level.rect.x, map_level.rect.y)
for b in borders_coords:
    Border(*b)

for coords in [(324, 50), (2548, 50),]:
    Window(*coords)

for coords in [(145, 105), (2473, 105)]:
    Bed(*coords)
BigBed(1225, 105)

for coords in [(224, 56), (1003, 56)]:
    Wardrobe(*coords)

for coords in [(224, 56), (1003, 56)]:
    Wardrobe(*coords)

for coords in [(322, 95), (2342, 95), (2388, 95), (2712, 95)]:
    Chair(*coords)

for coords in [(380, 110)]:
    Table(*coords)

for coord in [504, 834, 974, 1398, 2444]:
    Walllamp(coord, 228)

Carpet(2554, 160)

Washingmachine(532, 100)
Bath(700, 50)
Toilet(890, 96)

Computer(2760, 100)

for coords in [(30, 280, 320), (2870, 280, 320), (1100, 120)]:
    Chest(*coords)

tasks_coords = [(X + 200, Y + 200), (X + 1000, Y + 250), (X + 700, Y + 400), (X + 2500, Y + 350),
                (X + 1500, Y + 300), (X + 1200, Y + 250)]
for t in tasks_coords:
    Tasks(*t)

CompilationError(200, 200)
RuntimeError(200, 100)
WrongAnswer(200, 100)

player = Character(388, 268)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == MOVEEVENT:
            tasks.update()
        if event.type == GOEVENT:
            enemies.update()

    character.update()

    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)

    screen.fill((93, 44, 40))

    all_sprites.draw(screen)

    clock.tick(FPS)
    millisec += 1
    show_time(millisec)
    show_points(collected_tasks, millisec)

    pygame.display.flip()

    running = time_check(millisec)
