## Among Myth and Wonder
# algo_circle_range

from Resources import game_stats
import math


def within_circle_range(start, distance):
    level_width = 0
    level_height = 0
    if game_stats.current_screen == "Level Editor":
        level_width = int(game_stats.new_level_width)
        level_height = int(game_stats.new_level_height)
    elif game_stats.current_screen in ["Skirmish", "Game Board"]:
        level_width = int(game_stats.cur_level_width)
        level_height = int(game_stats.cur_level_height)

    # print("Start - " + str(start) + " and distance - " + str(distance))
    reach = []
    for x_pos in range(start[0] - distance, start[0] + distance + 1):
        if 0 < x_pos <= level_width:
            for y_pos in range(start[1] - distance, start[1] + distance + 1):
                if 0 < y_pos <= level_height:
                    # print("Tile - [" + str(x_pos) + ", " + str(y_pos) + "]")
                    # print("Distance^2 - {0}, x^2 - {1} y^2 - {2}".format(str(distance ** 2), str(x_pos ** 2),
                    #                                                      str(y_pos ** 2)))
                    if distance ** 2 >= ((x_pos - start[0]) ** 2) + ((y_pos - start[1]) ** 2):
                        reach.append([x_pos, y_pos])

    return reach


def simple_square_range(xy):
    # print("xy - " + str(xy))
    # print("current_screen - " + str(game_stats.current_screen))
    level_width = 0
    level_height = 0
    if game_stats.current_screen == "Level Editor":
        level_width = int(game_stats.new_level_width)
        level_height = int(game_stats.new_level_height)
    elif game_stats.current_screen in ["Skirmish", "Game Board"]:
        level_width = int(game_stats.cur_level_width)
        level_height = int(game_stats.cur_level_height)

    # print("level_width - " + str(level_width))
    # print("level_height - " + str(level_height))
    reach = []
    for position in [[-1, -1], [0, -1], [1, -1],
                     [-1, 0], [0, 0], [1, 0],
                     [-1, 1], [0, 1], [1, 1]]:
        if 0 < xy[0] + position[0] <= level_width:
            if 0 < xy[1] + position[1] <= level_height:
                reach.append([int(xy[0] + position[0]), int(xy[1] + position[1])])

    return reach
