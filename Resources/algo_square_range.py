## Among Myth and Wonder
## algo_square_range

from Resources import game_stats
import math


def within_square_range(start, distance):
    level_width = 0
    level_height = 0
    if game_stats.current_screen == "Level Editor":
        level_width = int(game_stats.new_level_width)
        level_height = int(game_stats.new_level_height)
    elif game_stats.current_screen in ["New Game", "Game Board"]:
        level_width = int(game_stats.cur_level_width)
        level_height = int(game_stats.cur_level_height)

    # print("Start - " + str(start) + " and distance - " + str(distance))
    reach = []
    for x_pos in range(start[0] - distance, start[0] + distance + 1):
        if 0 < x_pos <= level_width:
            for y_pos in range(start[1] - distance, start[1] + distance + 1):
                if 0 < y_pos <= level_height:
                    reach.append([x_pos, y_pos])

    return reach
