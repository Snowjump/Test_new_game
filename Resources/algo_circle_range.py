## Miracle battles

from Resources import game_stats
import math


def within_circle_range(start, distance):
    print("Start - " + str(start) + " and distance - " + str(distance))
    reach = []
    for x_pos in range(start[0] - distance, start[0] + distance + 1):
        if 0 < x_pos <= game_stats.cur_level_width:
            for y_pos in range(start[1] - distance, start[1] + distance + 1):
                if 0 < y_pos <= game_stats.cur_level_height:
                    # print("Tile - [" + str(x_pos) + ", " + str(y_pos) + "]")
                    # print("Distance^2 - {0}, x^2 - {1} y^2 - {2}".format(str(distance ** 2), str(x_pos ** 2),
                    #                                                      str(y_pos ** 2)))
                    if distance ** 2 >= ((x_pos - start[0]) ** 2) + ((y_pos - start[1]) ** 2):
                        reach.append([x_pos, y_pos])

    return reach
