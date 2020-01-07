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
            (X + 955, y_down_border, X + 1075, y_down_border),  # third room

            (X + 1000, y_top_border, X + 1080, y_top_border),
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
