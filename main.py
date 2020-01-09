import pygame
import sys
from random import choice
from func import load_image
from coords import create_borders_coords, create_tasks_coords, create_mobs_coords

pygame.init()

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
                  "Для включения/выключения музыки нажмите пробел",
                  '',
                  "ДЛЯ НАЧАЛА НАЖМИТЕ ЛЮБУЮ КНОПКУ"]
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 25
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
    return points + tasks * 300 - time * 5


def show_points(tasks, time):
    line = f'points: {get_points(tasks, time)}'
    font = pygame.font.Font(None, 33)

    string_rendered = font.render(line, True, pygame.Color(38, 43, 68))
    screen.blit(string_rendered, (60, 350))


def furniture_generation():
    for coord_x in [324, 2548, 1760, 2076]:
        Window(coord_x, 50)

    for coords in [(145, 105), (2473, 105)]:
        Bed(*coords)
    BigBed(1225, 105)

    for coords in [(224, 56), (1003, 56)]:
        Wardrobe(*coords)

    for coords in [(224, 56), (1003, 56)]:
        Wardrobe(*coords)

    for coord_x in [322, 1930, 1985, 2040, 2712]:
        Chair(coord_x, 110)

    Table(380, 125)
    BigTable(1910, 140)
    Sofa(2280, 130)

    for coord in [504, 834, 974, 1398, 2444]:
        Walllamp(coord, 228)

    for coord_x in [1310, 150, 2474]:
        Pictures(coord_x, 50)

    Carpet(2554, 160, 'orangecarpet.png')
    Carpet(700, 200, 'bluecarpet.png')
    Carpet(870, 200, 'bluecarpet.png')

    Wash(532, 100)
    Bath(700, 50)
    Toilet(890, 96)

    Computer(2760, 100)
    Kitchen()

    for coords in [(30, 280, 320), (2870, 280, 320), (1100, 120)]:
        Chest(*coords)


def tasks_mobs_generation(X, Y):
    borders_coords = create_borders_coords(X, Y)
    for b in borders_coords:
        Border(*b)

    tasks_coords = create_tasks_coords(X, Y)
    for t in tasks_coords:
        Tasks(*t)

    mob1_coords, mob2_coords, mob3_coords = create_mobs_coords(X, Y)
    for m1 in mob1_coords:
        CompilationError(*m1)
    for m2 in mob2_coords:
        WrongAnswer(*m2)
    for m3 in mob3_coords:
        RuntimeError(*m3)


class Map(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)

        self.image = pygame.Surface([0, 0])
        self.image = load_image('data\\map\\map.png')
        self.image = pygame.transform.scale(load_image('data\\map\\map.png'), (3000, 506))

        self.rect = self.image.get_rect()
        self.rect.x = - WIDTH // 2
        self.rect.y = - HEIGHT // 2


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
        for x in range(self.rect.w // 5, self.rect.w // 5 * 4):
            for y in range(self.rect.h // 9 * 8, self.rect.h):
                self.mask.set_at((x, y), 1)

    def update(self):
        self.vx = 0
        self.vy = 0

        keys = pygame.key.get_pressed()
        moving = False

        global millisec
        if pygame.sprite.spritecollideany(self, enemies, collided=pygame.sprite.collide_mask):
            millisec += 3

        if keys[pygame.K_LEFT] ^ keys[pygame.K_RIGHT]:
            self.direction = 1 if keys[pygame.K_LEFT] else 3
            self.vx = -10 if keys[pygame.K_LEFT] else 10
            self.rect.x += self.vx \
                if not pygame.sprite.spritecollideany(self, vertical_borders,
                                                      collided=pygame.sprite.collide_mask) else 0
            moving = True

            while pygame.sprite.spritecollideany(self, vertical_borders,
                                                 collided=pygame.sprite.collide_mask):
                self.rect.x += 1 if self.vx <= 0 else -1

        elif keys[pygame.K_UP] ^ keys[pygame.K_DOWN]:
            self.direction = 2 if keys[pygame.K_UP] else 0
            self.vy = 10 if keys[pygame.K_DOWN] else -10
            self.rect.y += self.vy \
                if not pygame.sprite.spritecollideany(self, horizontal_borders,
                                                      collided=pygame.sprite.collide_mask) else 0
            moving = True

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
            millisec += 2
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
    def __init__(self, x, y, name):
        super().__init__(x, y, name, borders=False)


class Chair(InteriorItems):
    def __init__(self, x, y, y_coord=150):
        super().__init__(x, y, 'chair.png', y_coord)


class Chest(InteriorItems):
    def __init__(self, x, y, y_coord=150):
        super().__init__(x, y, 'chest.png', y_coord)


class Computer(InteriorItems):
    def __init__(self, x, y):
        super().__init__(x, y, 'computer.png')

    def update(self, *args):
        pass


class Sofa(InteriorItems):
    def __init__(self, x, y):
        super().__init__(x, y, 'sofa.png')


class Kitchen:
    def __init__(self):
        InteriorItems(1424, 28, 'kitchen2.png')
        InteriorItems(1424, 174, 'kitchen1.png')


class Table(InteriorItems):
    def __init__(self, x, y, name='table.png', y_coord=150):
        super().__init__(x, y, name, y_coord)


class BigTable(Table):
    def __init__(self, x, y, y_coord=150):
        super().__init__(x, y, 'bigtable.png', y_coord)


class Toilet(InteriorItems):
    def __init__(self, x, y):
        super().__init__(x, y, 'toilet.png')


class Wallchest(InteriorItems):
    def __init__(self, x, y):
        super().__init__(x, y, 'wallchest.png', 0, False)


class Walllamp(InteriorItems):
    def __init__(self, x, y):
        super().__init__(x, y, 'walllamp.png', 0, False)


class Wardrobe(InteriorItems):
    def __init__(self, x, y):
        super().__init__(x, y, 'wardrobe.png')


class Wash(InteriorItems):
    def __init__(self, x, y):
        super().__init__(x, y, 'wash.png')


class Window(InteriorItems):
    def __init__(self, x, y):
        super().__init__(x, y, 'window.png', borders=False)


class Pictures(InteriorItems):
    def __init__(self, x, y):
        super().__init__(x, y, 'pictures.png', borders=False)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__(all_sprites)
        self.add(enemies)
        image = load_image('data\\mobs\\' + name)
        self.image = pygame.transform.scale(image, (image.get_rect().w * 2, image.get_rect().h * 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 2
        self.vy = 3

        self.mask = pygame.mask.Mask((self.rect.w, self.rect.h), False)
        for x in range(self.rect.w):
            for y in range(self.rect.h // 7 * 6, self.rect.h):
                self.mask.set_at((x, y), 1)


class CompilationError(Enemy):
    def __init__(self, width, height):
        super().__init__(width, height, "mob_1.png")
        self.vy = 0

    def update(self):
        self.rect = self.rect.move(self.vx, 0)
        if pygame.sprite.spritecollideany(self, vertical_borders,
                                          collided=pygame.sprite.collide_mask):
            self.vx = -self.vx


class RuntimeError(Enemy):
    def __init__(self, width, height):
        super().__init__(width, height, "mob_3.png")

    def update(self):
        change = False
        self.rect.y += self.vy
        while pygame.sprite.spritecollideany(self, horizontal_borders,
                                          collided=pygame.sprite.collide_mask):
            self.rect.y += 3 if self.vy <= 0 else -3
            change = True
        self.vy = -self.vy if change else self.vy

        change = False
        self.rect.x += self.vx
        while pygame.sprite.spritecollideany(self, vertical_borders,
                                          collided=pygame.sprite.collide_mask):
            self.rect.x += 2 if self.vx <= 0 else -2
            change = True
        self.vx = -self.vx if change else self.vx


class WrongAnswer(Enemy):
    def __init__(self, width, height):
        super().__init__(width, height, "mob_2.png")
        self.vx = 0

    def update(self):
        self.rect = self.rect.move(0, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders,
                                          collided=pygame.sprite.collide_mask):
            self.vy = -self.vy


start_screen()

camera = Camera()
map_level = Map()

furniture_generation()

tasks_mobs_generation(map_level.rect.x, map_level.rect.y)

player = Character(388, 268)

sound = pygame.mixer.Sound('data\\music.wav')
sound.play()
music = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == MOVEEVENT:
            tasks.update()
        if event.type == GOEVENT:
            enemies.update()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            sound.stop() if music else sound.play()
            music = not music

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
