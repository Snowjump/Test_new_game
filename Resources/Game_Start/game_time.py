## Among Myth and Wonder
## game_time

import pygame

from Resources import game_stats
from Resources import game_basic
from Resources import game_battle


def time_update():
    if not game_stats.pause_status:
        game_stats.time_counted = pygame.time.get_ticks()
        game_stats.temp_time_passed = game_stats.time_counted - game_stats.last_start
        game_stats.display_time = int(game_stats.passed_time + game_stats.temp_time_passed)
        # print("game_stats.display_time - " + str(game_stats.display_time))
        # print("math.floor(game_stats.display_time/1000) - " + str(math.floor(game_stats.display_time/1000)))

        # if game_stats.strategy_mode:
        #     game_basic.advance_time()  # Increase time - also characters complete actions from their tasks

        game_basic.advance_time()
        if not game_stats.strategy_mode:
            game_battle.advance_battle_time(game_stats.time_counted)

        # print("Passed time - " + str(game_stats.passed_time) + " get_ticks - " + str(game_stats.time_counted)
        #       + " start time - " + str(game_stats.start_time))
    else:
        game_stats.display_time = int(game_stats.passed_time)
