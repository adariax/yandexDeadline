import sys
from random import choice
from func import *
from coords import *

# launch constructor of PyGame
pygame.init()

# window's characteristics
WIDTH = 800
HEIGHT = 400
X = - WIDTH // 2
Y = - HEIGHT // 2
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Deadline')
screen.fill((0, 0, 0))

GOEVENT = 30  # event for moving enemies
pygame.time.set_timer(GOEVENT, 15)

clock = pygame.time.Clock()  # makes count time possible

FPS = 20  # Frames Per Second

# create all sprite group
all_sprites = pygame.sprite.Group()
tasks = pygame.sprite.Group()
character = pygame.sprite.Group()
enemies = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
computer = pygame.sprite.Group()

# game's constants
POINTS = 3000  # start points
TIME = 1440  # all time

collected_tasks = 0  # var for collected task
millisec = 0  # var for left time

running = True  # main game loop
WIN = False  # flag for win game


def terminate():  # exit game function
    pygame.quit()
    sys.exit()


class InfoScreen:
    def __init__(self, list_of_strings):
        self.fon = pygame.transform.scale(load_image('data\\screen.jpg'), (WIDTH, HEIGHT))
        screen.blit(self.fon, (0, 0))
        self.font = pygame.font.Font(None, 30)
        self.add_text(list_of_strings)

    def add_text(self, list_of_strings):  # add info text
        text_coord = 15
        for line in list_of_strings:
            string_rendered = self.font.render(line, 1, pygame.Color(246, 200, 159))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    def show(self):  # show info while player don't push any button
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return
            pygame.display.flip()
            clock.tick(FPS)


class StartScreen(InfoScreen):  # for showing info before start
    def __init__(self):
        super().__init__(['DEADLINE',
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
                          "ДЛЯ НАЧАЛА НАЖМИТЕ ПРОБЕЛ"])


class FinishScreen(InfoScreen):  # for showing endgame info
    def __init__(self, tasks, time, points):
        global WIN  # if player reached computer
        super().__init__(['ИГРА ОКОНЧЕНА',
                          '',
                          "Вы набрали:",
                          f"{get_points(tasks, time, points) + (1000 if WIN else 0)} очков",
                          "",
                          f"1000 бонусных очков за сдачу" if WIN
                          else 'В следующий раз дойдите до компьютера',
                          '',
                          '',
                          "Поздравляю! Новый рекорд"
                          # update highscore and check it
                          if save_results(get_points(tasks, time, points) + (1000 if WIN else 0))
                          else "Попробуйте установить новый рекорд",
                          "",
                          '',
                          "ЧТОБЫ НАЧАТЬ СНАЧАЛА НАЖМИТЕ ПРОБЕЛ"])


def show_time(time):  # show time on game screen
    minutes, hours = time_left(time, TIME)
    line = f'{hours}:{str(minutes) if minutes >= 10 else str(0) + str(minutes)}'
    font1 = pygame.font.Font(None, 33)
    font2 = pygame.font.Font(None, 30)

    string_rendered1 = font1.render(line, True, pygame.Color(63, 40, 60))
    string_rendered2 = font2.render(line, True, pygame.Color(255, 0, 68))
    screen.blit(string_rendered1, (698, 350))
    screen.blit(string_rendered2, (700, 350))


def show_points(tasks, time):  # show current points on main game screen
    line = f'points: {get_points(tasks, time, POINTS)}'
    font = pygame.font.Font(None, 33)

    string_rendered = font.render(line, True, pygame.Color(18, 78, 137))
    screen.blit(string_rendered, (60, 350))


def show_highscore():  # show highscore from file data\\highscore.sc
    line = f'HIGHSCORE: {get_highscore()}'  # get highscore from file
    font = pygame.font.Font(None, 33)

    string_rendered = font.render(line, True, pygame.Color(38, 43, 68))
    screen.blit(string_rendered, (200, 350))


def furniture_generation():  # furniture placement by static coords
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

    for coord_x in [504, 834, 974, 1398, 2444]:
        Walllamp(coord_x, 228)

    for coord_x in [1310, 150, 2474]:
        Pictures(coord_x, 50)

    Carpet(2554, 160, 'orangecarpet.png')
    for coord_x in [700, 870]:
        Carpet(coord_x, 200, 'bluecarpet.png')

    Wash(532, 100)
    Bath(700, 50)
    Toilet(890, 96)

    Computer(2760, 100)
    Kitchen()

    for coords in [(30, 280, 320), (2870, 280, 320), (1100, 120)]:
        Chest(*coords)


def tasks_mobs_generation(X, Y):  # tasks placement and mobs generation; coords from file coords.py
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


def generation_game():
    character.empty()
    computer.empty()
    enemies.empty()
    vertical_borders.empty()
    horizontal_borders.empty()
    tasks.empty()
    all_sprites.empty()

    map_level = Map()
    furniture_generation()  # load all furniture

    tasks_mobs_generation(map_level.rect.x, map_level.rect.y)  # load tasks adn mobs

    player = Character(0, 0)

    # create sound
    sound = pygame.mixer.Sound('data\\music.wav')
    sound.play()
    music = True
    return (map_level, player, sound, music)


class Map(pygame.sprite.Sprite):  # create map for level
    def __init__(self):
        super().__init__(all_sprites)

        self.image = pygame.Surface([0, 0])
        self.image = pygame.transform.scale(load_image('data\\map\\map.png'), (3000, 506))

        self.rect = self.image.get_rect()
        self.rect.x = - WIDTH // 2
        self.rect.y = - HEIGHT // 2


class Camera:  # creates camera for game, which move all obj in apply except for target in update
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


class Character(pygame.sprite.Sprite):  # class for player
    def __init__(self, x, y):  # create sprite on screen in x, y coords
        super().__init__(all_sprites)
        self.add(character)
        self.x = x
        self.y = y
        self.frames = 11  # animation len animation
        # start speed
        self.vx = 0
        self.vy = 0

        self.direction = 0  # start direction
        # forward - 0, left - 1, back - 2, right - 3
        self.cur_frame = 0  # current frame of animation
        self.images_standing = [[], [], [], []]  # list of images for standing with 4 direction
        self.images_walking = [[], [], [], []]  # list of images for walking with 4 direction

        for status in ('standing', 'walking'):  # makes list of images full
            for direction in range(4):
                for number_file in range(11):
                    path = f'data\\character\\{status}\\{str(direction)}\\{number_file + 1}.png'
                    image = load_image(path)
                    image = pygame.transform.scale(image,
                                                   (image.get_rect().w * 2, image.get_rect().h * 2))
                    eval(f'self.images_{status}[direction].append(image)')

        self.image = self.images_standing[0][self.cur_frame]  # image for start game
        self.rect = self.image.get_rect()  # permanent rect
        self.mask = pygame.mask.Mask((self.rect.w, self.rect.h), False)  # create mask on player's
        for x in range(self.rect.w // 7, self.rect.w // 7 * 6):  # feet only
            for y in range(self.rect.h // 9 * 8, self.rect.h):
                self.mask.set_at((x, y), 1)

    def update(self):
        self.vx = 0
        self.vy = 0

        keys = pygame.key.get_pressed()  # get all pressed keys
        moving = False  # flag for change standing sprite to walking

        global millisec
        if pygame.sprite.spritecollideany(self, enemies, collided=pygame.sprite.collide_mask):
            millisec += 10

        if keys[pygame.K_LEFT] ^ keys[pygame.K_RIGHT]:  # ^ = xor
            self.direction = 1 if keys[pygame.K_LEFT] else 3  # change direction
            self.vx = -10 if self.direction == 1 else 10  # change speed by direction
            self.rect.x += self.vx  # change x coord
            moving = True

            while pygame.sprite.spritecollideany(self, vertical_borders,  # remove collide
                                                 collided=pygame.sprite.collide_mask):
                self.rect.x += 1 if self.vx <= 0 else -1

        elif keys[pygame.K_UP] ^ keys[pygame.K_DOWN]:  # ^ = xor
            self.direction = 2 if keys[pygame.K_UP] else 0  # change direction
            self.vy = 10 if self.direction == 0 else -10  # change speed by direction
            self.rect.y += self.vy  # change y coord
            moving = True

            while pygame.sprite.spritecollideany(self, horizontal_borders,  # remove collide
                                                 collided=pygame.sprite.collide_mask):
                self.rect.y += 1 if self.vy <= 0 else -1

        # change image (animation)
        self.image = self.images_standing[self.direction][self.cur_frame % self.frames] \
            if not moving else self.images_walking[self.direction][self.cur_frame % self.frames]
        self.cur_frame += 1  # change count frame for animation


class Tasks(pygame.sprite.Sprite):

    def __init__(self, x, y):  # create task sprite on screen on x, y coords
        super().__init__(all_sprites)
        self.add(tasks)
        self.image = load_image(f"data\\tasks\\"  # random image of task
                                f"{choice(['task_1.png', 'task_2.png', 'task_3.png'])}", (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global collected_tasks
        global millisec
        # after collide with player, collected tasks increase of 1 and task disappear
        if pygame.sprite.spritecollideany(self, character, collided=pygame.sprite.collide_mask):
            collected_tasks += 1
            self.kill()


class Border(pygame.sprite.Sprite):
    # create only horizontal or vertical border
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # vertical border
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
            self.mask = pygame.mask.Mask((1, y2 - y1), True)
        else:  # horizontal border
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
            self.mask = pygame.mask.Mask((x2 - x1, 1), True)
        self.image.set_alpha(0)  # makes border invisible


class InteriorItems(pygame.sprite.Sprite):
    # parent class for all furniture
    def __init__(self, x, y, name, bottom_top_y=150, borders=True):
        super().__init__(all_sprites)
        image = load_image('data\\furniture\\' + name)  # load picture
        # and increases it in 2 times
        self.image = pygame.transform.scale(image, (image.get_rect().w * 2, image.get_rect().h * 2))
        self.rect = self.image.get_rect()
        self.rect.x = X + x
        self.rect.y = Y + y
        self.bottom_top_y = Y + bottom_top_y  # top y coord of borders for collide

        if borders:  # create borders for collide events
            Border(self.rect.x, self.bottom_top_y,
                   self.rect.x, self.rect.y + self.rect.h)
            Border(self.rect.x, self.bottom_top_y,
                   self.rect.x + self.rect.w, self.bottom_top_y)
            Border(self.rect.x, self.rect.y + self.rect.h,
                   self.rect.x + self.rect.w, self.rect.y + self.rect.h)
            Border(self.rect.x + self.rect.w, self.bottom_top_y,
                   self.rect.x + self.rect.w, self.rect.y + self.rect.h)


# furniture classes


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
        self.add(computer)
        self.mask = pygame.mask.Mask((self.rect.w, self.rect.h + 5), False)  # create mask
        for x in range(self.rect.w):
            for y in range(self.rect.h // 3 * 2, self.rect.h + 5):
                self.mask.set_at((x, y), 1)

    def update(self):  # makes closing deadline possible
        global WIN
        if pygame.sprite.spritecollideany(self, character, collided=pygame.sprite.collide_mask):
            WIN = True


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
    # parent class for all furniture
    def __init__(self, x, y, name):
        super().__init__(all_sprites)
        self.add(enemies)  # add to enemies sprite group
        image = load_image('data\\mobs\\' + name)  # load image
        self.image = pygame.transform.scale(image, (image.get_rect().w * 2, image.get_rect().h * 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # start speed
        self.vx = 2
        self.vy = 3

        # make mask for 1/7 of height
        self.mask = pygame.mask.Mask((self.rect.w, self.rect.h), False)
        for x in range(self.rect.w):
            for y in range(self.rect.h // 7 * 6, self.rect.h):
                self.mask.set_at((x, y), 1)


class CompilationError(Enemy):
    def __init__(self, width, height):
        super().__init__(width, height, "mob_1.png")
        self.vy = 0

    def update(self):  # walk right-left
        self.rect = self.rect.move(self.vx, 0)
        if pygame.sprite.spritecollideany(self, vertical_borders,
                                          collided=pygame.sprite.collide_mask):
            self.vx = -self.vx


class RuntimeError(Enemy):
    def __init__(self, width, height):
        super().__init__(width, height, "mob_3.png")

    def update(self):  # start walk to top-right corner, when bounce off borders
        change = False  # flag to change vector of speed
        self.rect.y += self.vy
        while pygame.sprite.spritecollideany(self, horizontal_borders,  # remove collide
                                             collided=pygame.sprite.collide_mask):
            self.rect.y += 3 if self.vy <= 0 else -3
            change = True
        self.vy = -self.vy if change else self.vy

        change = False
        self.rect.x += self.vx
        while pygame.sprite.spritecollideany(self, vertical_borders,  # remove collide
                                             collided=pygame.sprite.collide_mask):
            self.rect.x += 2 if self.vx <= 0 else -2
            change = True
        self.vx = -self.vx if change else self.vx


class WrongAnswer(Enemy):
    def __init__(self, width, height):
        super().__init__(width, height, "mob_2.png")
        self.vx = 0

    def update(self):  # walk up-down
        self.rect = self.rect.move(0, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders,
                                          collided=pygame.sprite.collide_mask):
            self.vy = -self.vy


start = StartScreen()  # load start screen
start.show()

camera = Camera()

map_level, player, sound, music = generation_game()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == GOEVENT:
            enemies.update()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            sound.stop() if music else sound.play()
            music = not music

    tasks.update()
    character.update()
    computer.update()

    camera.update(player)  # move all sprites with respect to a player
    for sprite in all_sprites:
        camera.apply(sprite)

    screen.fill((93, 44, 40))

    all_sprites.draw(screen)

    clock.tick(FPS)
    millisec += 1

    # show information on screen
    show_time(millisec)
    show_points(collected_tasks, millisec)
    show_highscore()

    pygame.display.flip()

    running = time_check(millisec, TIME)  # end game if time ended
    if not running or WIN:  # if the player reached the computer or time ended
        sound.stop()
        finish = FinishScreen(collected_tasks, millisec, POINTS)
        finish.show()  # endgame screen

        map_level, player, sound, music = generation_game()  # regenerate level

        millisec = 0
        collected_tasks = 0
        running = True
        WIN = False
