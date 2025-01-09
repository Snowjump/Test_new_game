## Among Myth and Wonder
## anim_army_move

from Resources import game_stats
import math


def army_march(child, parent):
    x = (child[0] - parent[0]) * 48
    y = (child[1] - parent[1]) * 48
    spread = (game_stats.display_time/1000 - game_stats.last_change) / 1
    # print(str(abs((spread * 1000) % 500 - 250)))
    # print(str(((250 - abs((spread * 1000) % 500 - 250)) / 250) * -12))
    # 0 - 500
    # -250 - 250
    # 250 - 0 - 250
    # 0 - 250 - 0
    # 0 - 1 - 0
    # 0 - -12 - 0
    k = ((250 - abs((spread * 1000) % 500 - 250)) / 250) * -12
    return [x * spread, y * spread + k]
