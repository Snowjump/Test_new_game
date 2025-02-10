## Among Myth and Wonder
## game_board_navigation

from Resources import game_stats
from Resources import update_gf_game_board


def move_pov_up():
    print("w: key_action == 119")
    if game_stats.pov_pos[1] > - 6:
        game_stats.pov_pos[1] -= 1
        update_gf_game_board.update_sprites()
        print("new pov_pos - " + str(game_stats.pov_pos))


def move_pov_down():
    print("s: key_action == 115")
    if game_stats.pov_pos[1] < game_stats.cur_level_height - 9:
        game_stats.pov_pos[1] += 1
        update_gf_game_board.update_sprites()
        print("new pov_pos - " + str(game_stats.pov_pos))


def move_pov_left():
    print("a: key_action == 97")
    if game_stats.pov_pos[0] > - 6:
        game_stats.pov_pos[0] -= 1
        update_gf_game_board.update_sprites()
        print("new pov_pos - " + str(game_stats.pov_pos))


def move_pov_right():
    print("d: key_action == 100")
    if game_stats.pov_pos[0] < game_stats.cur_level_width - 21:
        game_stats.pov_pos[0] += 1
        update_gf_game_board.update_sprites()
        print("new pov_pos - " + str(game_stats.pov_pos))
