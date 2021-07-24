## Miracle battles!

import shelve
from pathlib import Path

from Resources import game_stats
from Resources import game_obj
from Resources import game_basic


# This function needed to load level, when player is starting new game or proceed to next level

def begin_new_level(level_to_load):
    shelfFile = shelve.open(str(Path('levels')) + '/' + level_to_load)

    game_stats.current_level_name = shelfFile["new_level_named"]

    game_stats.game_year = shelfFile["new_level_year"]

    game_stats.game_month = shelfFile["new_level_month"]

    game_obj.game_map = shelfFile["new_level_map"]

    game_obj.game_powers = shelfFile["new_level_powers"]

    game_obj.game_cities = shelfFile["new_level_cities"]

    game_obj.game_armies = shelfFile["new_level_armies"]

    game_stats.cities_id_counter = shelfFile["new_level_LE_cities_id_counter"]

    game_stats.army_id_counter = shelfFile["new_level_LE_army_id_counter"]

    shelfFile.close()

    pov_pos = [0, 0]
    print("Level name is " + game_stats.current_level_name)
    print(str(game_stats.game_month) + " month " + str(game_stats.game_year) + " year")
    print("Playable faction is " + assign_parameters[game_stats.current_level_name])
    game_stats.player_power = assign_parameters[game_stats.current_level_name]
    game_stats.perspective = str(game_stats.player_power)
    game_stats.turn_hourglass = False

    count_x = 0
    count_y = 0
    for xy_tile in game_obj.game_map:
        if xy_tile.posxy[0] > count_x:
            count_x = xy_tile.posxy[0]
        if xy_tile.posxy[1] > count_y:
            count_y = xy_tile.posxy[1]
    print("count_x = " + str(count_x) + " and count_y = " + str(count_y))
    game_stats.cur_level_width = int(count_x)
    game_stats.cur_level_height = int(count_y)
    game_stats.selected_object = ""

    game_basic.prepare_known_map(game_stats.player_power)

    game_stats.pause_status = True
    game_stats.day = 0
    game_stats.hours = 0
    game_stats.minutes = 0
    game_stats.count_started = False


assign_parameters = {"Test level": "First",
                     "New name": "First"}
