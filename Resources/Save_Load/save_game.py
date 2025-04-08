## Among Myth and Wonder
## save_game

import pickle

from Resources.Save_Load import save_classes

from Resources import game_stats
from Resources import game_obj
from Resources import game_start
from Resources import common_selects


def save_current_game(filename):
    print("save_current_game() " + str(filename))
    data = save_classes.Save_File()
    data.fill_in_the_information()
    with open(filename + '.svfl', 'wb') as file:  # Savefile = svfl
        pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)


def get_save_info(filename):
    with open(filename, 'rb') as file:
        game_stats.level_info = pickle.load(file)


def load_game(file):
    # Level parameters
    game_stats.level_type = file.level_type
    game_stats.current_level_name = file.level_name
    game_stats.game_year = file.game_year
    game_stats.game_month = file.game_month
    game_stats.cur_level_width = file.cur_level_width
    game_stats.cur_level_height = file.cur_level_height
    # ID counters
    game_stats.cities_id_counter = file.cities_id_counter
    game_stats.army_id_counter = file.army_id_counter
    game_stats.population_id_counter = file.population_id_counter
    game_stats.hero_id_counter = file.hero_id_counter
    game_stats.reward_id_counter = file.reward_id_counter

    game_stats.player_power = file.player_power
    game_stats.pov_pos = file.pov_pos

    # Objects
    game_obj.game_powers = file.game_powers
    game_obj.bin_realms = file.bin_realms
    game_obj.game_map = file.game_map
    game_obj.borders_map = file.borders_map
    game_obj.game_cities = file.game_cities
    game_obj.game_armies = file.game_armies
    game_obj.game_wars = file.game_wars
    game_stats.ongoing_wars = file.ongoing_wars

    game_start.nullify_level_editor_variables()

    game_stats.turn_hourglass = False
    player_realm = common_selects.select_realm_by_name(game_stats.player_power)
    game_stats.map_to_display = player_realm.known_map
    game_stats.strategy_mode = True


