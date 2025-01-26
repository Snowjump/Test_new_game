## Among Myth and Wonder
## algo_square_range

from Resources import game_stats
import math


def within_square_range(start, distance, location=False):
    level_width = 0
    level_height = 0
    if game_stats.current_screen in ["Level Editor", "Load Level Into Editor"]:
        level_width = int(game_stats.new_level_width)
        level_height = int(game_stats.new_level_height)
    elif game_stats.current_screen in ["New Game", "Game Board", "Skirmish", "Battle"]:
        level_width = int(game_stats.cur_level_width)
        level_height = int(game_stats.cur_level_height)

    # print("Start - " + str(start) + " and distance - " + str(distance))
    reach = []
    for x_pos in range(start[0] - distance, start[0] + distance + 1):
        if 0 < x_pos <= level_width:
            for y_pos in range(start[1] - distance, start[1] + distance + 1):
                if 0 < y_pos <= level_height:
                    if location:
                        reach.append(int((y_pos - 1) * level_width + x_pos - 1))
                    else:
                        reach.append([x_pos, y_pos])

    return reach
