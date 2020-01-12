import pygame


def load_image(name, colorkey=None):  # load image by name
    image = pygame.image.load(name)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def get_highscore():  # read and return highscore from file
    with open('data\\highscore.sc', 'r') as f:
        read_data = f.read()
    return int(read_data)


def save_results(points, highscore):  # check score and write new highscore
    if points > highscore:
        with open('data\\highscore.sc', 'w') as f:
            f.write(str(points))
        return True


def time_check(current_time, all_time):  # retuurn False if time left
    return True if current_time < all_time else False


def time_left(current_time, all_time):  # return left 'hours' and 'minutes'
    left_millisec = all_time - current_time
    return (left_millisec % 60, left_millisec // 60)


def get_points(tasks, time, points):  # return current points
    ret_points = points + tasks * 300 - time * 5
    return 0 if ret_points < 0 else ret_points
