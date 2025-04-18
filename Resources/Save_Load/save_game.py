## Among Myth and Wonder
## save_game

import pickle
import site
import os
import glob

from pathlib import Path

from platformdirs import PlatformDirs

from Resources.Save_Load import save_classes

from Resources import game_stats
from Resources import game_obj
from Resources import game_start
from Resources import common_selects


def prepare_save_files_list():
    # print("levels_list: " + str(game_stats.levels_list))
    dirs = PlatformDirs(game_stats.app_name, game_stats.author)
    folder_path = str(dirs.user_data_dir) + '\\saves\\' + game_stats.level_type
    # print("folder_path: " + folder_path)
    # print("Directory exist - " + str(os.path.isdir(folder_path)))
    if os.path.isdir(folder_path):
        game_stats.levels_list = glob.glob(folder_path + "\\*.svfl")
        for i, s in enumerate(game_stats.levels_list):
            pos = s.find(game_stats.level_type)
            game_stats.levels_list[i] = s[pos + len(game_stats.level_type) + 1:]
    else:
        game_stats.levels_list = []
    # print("levels_list: " + str(game_stats.levels_list))


def save_current_game(filename):
    print("save_current_game() " + str(filename))
    data = save_classes.Save_File()
    data.fill_in_the_information()
    dirs = PlatformDirs(game_stats.app_name, game_stats.author)
    print(str(dirs.user_data_dir) + "; type - " + str(type(dirs.user_data_dir)))
    folder_path = str(dirs.user_data_dir) + '\\saves\\' + game_stats.level_type
    check_dir(folder_path)
    path = folder_path + '\\' + filename + '.svfl'
    print(path)
    with open(path, 'wb') as file:  # Savefile = svfl
        pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)


def get_save_info(filename):
    # print(site.getsitepackages())
    # print(dir(pygame))
    dirs = PlatformDirs(game_stats.app_name, game_stats.author)
    folder_path = str(dirs.user_data_dir) + '\\saves\\' + game_stats.level_type
    path = folder_path + '\\' + filename
    with open(path, 'rb') as file:
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
    player_realm.turn_completed = False
    game_stats.map_to_display = player_realm.known_map
    game_stats.strategy_mode = True


def check_dir(folder_path):
    folder_exist = os.path.isdir(folder_path)
    print("Directory exist - " + str(folder_exist))
    if not folder_exist:
        Path(folder_path).mkdir(parents=True, exist_ok=True)


def autosave_current_game():
    print("autosave_current_game()")
    prepare_save_files_list()
    print("levels_list: " + str(game_stats.levels_list))
    if game_stats.levels_list:
        dirs = PlatformDirs(game_stats.app_name, game_stats.author)
        folder_path = str(dirs.user_data_dir) + '\\saves\\' + game_stats.level_type
        for i in reversed(range(1, 5)):
            old_save = 'autosave_' + str(i) + '.svfl'
            print("old_save - " + str(old_save))

            if old_save in game_stats.levels_list:
                print("Replace autosave_" + str(i + 1) + '.svfl')
                if i == 4:
                    print("Delete last autosave: autosave_" + str(i + 1) + '.svfl')
                    if 'autosave_' + str(i + 1) + '.svfl' in game_stats.levels_list:
                        file_to_rem = Path(folder_path + '\\' + 'autosave_' + str(i + 1) + '.svfl')
                        print(str(file_to_rem) + "; type - " + str(type(file_to_rem)))
                        file_to_rem.unlink()

                old_filename = folder_path + '\\' + 'autosave_' + str(i) + '.svfl'
                new_filename = folder_path + '\\' + 'autosave_' + str(i + 1) + '.svfl'
                os.rename(old_filename, new_filename)

    save_current_game('autosave_1')
