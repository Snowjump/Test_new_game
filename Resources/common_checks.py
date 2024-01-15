## Among Myth and Wonder
## common_checks

from Resources import game_stats


def within_map_limits(tile):
    # tile - list [int x, int y]
    verdict = False
    if game_stats.current_screen == "Level Editor":
        if 0 < tile[0] <= game_stats.new_level_width:
            if 0 < tile[1] <= game_stats.new_level_height:
                verdict = True

    elif game_stats.current_screen in ["Skirmish", "Game Board"]:
        if 0 < tile[0] <= game_stats.cur_level_width:
            if 0 < tile[1] <= game_stats.cur_level_height:
                verdict = True

    return verdict
