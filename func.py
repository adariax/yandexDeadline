import os
import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def get_highscore():
    with open('data\\highscore.sc', 'r') as f:
        read_data = f.read()
    return int(read_data)


def save_results(points, highscore):
    if points > highscore:
        with open('data\\highscore.sc', 'w') as f:
            f.write(str(points))


def time_check(current_time, all_time):
    return True if current_time < all_time else False


def time_left(current_time, all_time):
    left_millisec = all_time - current_time
    return (left_millisec % 60, left_millisec // 60)


def get_points(tasks, time, points):
    return points + tasks * 300 - time * 5
