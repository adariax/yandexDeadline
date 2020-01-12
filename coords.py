def create_borders_coords(X, Y):
    y_top_room = Y + 168
    y_top_border = Y + 328
    y_down_border = Y + 340
    return [(X, Y, X, Y + 506), (X, Y + 506, X + 3000, Y + 506),
            (X + 3000, Y, X + 3000, Y + 506),
            (X, Y, X + 3000, Y),  # frame of map
            (X, Y + 340, X + 200, Y + 340),
            (X + 143, y_top_border, X + 220, y_top_border),
            (X + 390, y_top_border, X + 495, y_top_border),
            (X + 144, y_top_room, X + 495, y_top_room),
            (X + 144, y_top_room, X + 144, y_top_border),
            (X + 495, y_top_room, X + 495, y_top_border),
            (X + 390, y_down_border, X + 600, y_down_border),  # first room

            (X + 528, y_top_border, X + 600, y_top_border),
            (X + 528, y_top_room, X + 823, y_top_room),
            (X + 528, y_top_room, X + 528, y_top_border),
            (X + 823, y_top_room, X + 823, y_top_border),
            (X + 705, y_top_border, X + 823, y_top_border),
            (X + 705, y_down_border, X + 865, y_down_border),  # second room

            (X + 860, y_top_border, X + 865, y_top_border),
            (X + 860, y_top_room, X + 963, y_top_room),
            (X + 860, y_top_room, X + 860, y_top_border),
            (X + 963, y_top_room, X + 963, y_top_border),
            (X + 955, y_top_border, X + 963, y_top_border),
            (X + 955, y_down_border, X + 1070, y_down_border),  # third room

            (X + 1000, y_top_border, X + 1070, y_top_border),
            (X + 1000, y_top_room, X + 1390, y_top_room),
            (X + 1000, y_top_room, X + 1000, y_top_border),
            (X + 1390, y_top_room, X + 1390, y_top_border),
            (X + 1220, y_top_border, X + 1390, y_top_border),
            (X + 1220, y_down_border, X + 1545, y_down_border),  # fourth room

            (X + 1422, y_top_border, X + 1546, y_top_border),
            (X + 1422, y_top_room, X + 2435, y_top_room),
            (X + 1422, y_top_room, X + 1422, y_top_border),
            (X + 2435, y_top_room, X + 2435, y_top_border),
            (X + 2348, y_top_border, X + 2435, y_top_border),
            (X + 1628, y_top_border, X + 2265, y_top_border),
            (X + 1628, y_down_border, X + 2265, y_down_border),
            (X + 2350, y_down_border, X + 2545, y_down_border),  # fifth room

            (X + 2468, y_top_border, X + 2545, y_top_border),
            (X + 2468, y_top_room, X + 2858, y_top_room),
            (X + 2468, y_top_room, X + 2468, y_top_border),
            (X + 2858, y_top_room, X + 2858, y_top_border),
            (X + 2635, y_top_border, X + 2858, y_top_border),
            (X + 2635, y_down_border, X + 3000, y_down_border)  # last room
            ]


def create_tasks_coords(X, Y):
    return map(lambda x: (x[0] + X, x[1] + Y),
               [(200, 230), (400, 360), (444, 220), (220, 370), (280, 290), (1020, 290),
                (470, 442), (620, 180), (760, 260), (590, 360), (710, 430), (920, 200),
                (830, 350), (1050, 460), (9800, 300), (1500, 250), (100, 406), (1114, 209),
                (1284, 280), (960, 4000), (1375, 400), (1590, 365), (1690, 280), (1732, 400),
                (1774, 184), (1874, 455), (1980, 364), (2026, 262), (2112, 440), (2170, 180),
                (2208, 280), (2370, 370), (2400, 450), (2470, 380), (2524, 272), (2580, 436),
                (2614, 180), (2662, 280), (2730, 390), (2806, 236), (2860, 460), (2942, 365),
                (1150, 360)])


def create_mobs_coords(X, Y):
    mob1 = map(lambda x: (x[0] + X, x[1] + Y),
               [(226, 200), (1010, 220), (1478, 210), (2110, 220)])
    mob2 = map(lambda x: (x[0] + X, x[1] + Y),
               [(270, 350), (550, 350), (1210, 350), (2090, 350)])
    mob3 = map(lambda x: (x[0] + X, x[1] + Y),
               [(890, 380), (1150, 400), (2655, 220), (586, 280)])
    return (mob1, mob2, mob3)
