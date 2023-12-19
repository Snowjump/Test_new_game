## Among Myth and Wonder
## start_new_level

import shelve
from pathlib import Path

from Resources import game_stats
from Resources import game_obj
from Resources import update_gf_game_board
from Resources import prepare_level
from Resources import game_start


# This function needed to load level, when player is starting new game or proceed to next level

def begin_new_level(folder, level_to_load):
    shelfFile = shelve.open(str(Path('levels/' + folder)) + '/' + level_to_load)

    game_stats.current_level_name = shelfFile["new_level_named"]

    game_stats.game_year = shelfFile["new_level_year"]

    game_stats.game_month = shelfFile["new_level_month"]

    game_obj.game_map = shelfFile["new_level_map"]

    game_obj.game_powers = shelfFile["new_level_powers"]

    game_obj.game_cities = shelfFile["new_level_cities"]

    game_obj.game_armies = shelfFile["new_level_armies"]

    game_stats.cities_id_counter = shelfFile["new_level_LE_cities_id_counter"]

    game_stats.army_id_counter = shelfFile["new_level_LE_army_id_counter"]

    game_stats.hero_id_counter = shelfFile["new_level_LE_hero_id_counter"]

    game_stats.population_id_counter = shelfFile["new_level_LE_population_id_counter"]

    level_type = shelfFile["new_level_type"]

    shelfFile.close()

    game_start.nullify_level_editor_variables()

    pov_pos = [0, 0]
    # print("Level name is " + game_stats.current_level_name)
    # print(str(game_stats.game_month) + " month " + str(game_stats.game_year) + " year")
    # print("Playable faction is " + assign_parameters[game_stats.current_level_name])
    # game_stats.player_power = assign_parameters[game_stats.current_level_name]
    # print("Playable faction is " + game_stats.start_level_selected_realm.name)
    game_stats.player_power = str(game_stats.start_level_selected_realm.name)
    # print("game_stats.player_power - " + str(game_stats.player_power))
    game_stats.perspective = str(game_stats.player_power)
    game_stats.turn_hourglass = False

    # Human player
    for realm in game_obj.game_powers:
        if realm.name == game_stats.player_power:
            realm.AI_player = False
            break

    count_x = 0
    count_y = 0
    for xy_tile in game_obj.game_map:
        if xy_tile.posxy[0] > count_x:
            count_x = xy_tile.posxy[0]
        if xy_tile.posxy[1] > count_y:
            count_y = xy_tile.posxy[1]
    # print("count_x = " + str(count_x) + " and count_y = " + str(count_y))
    game_stats.cur_level_width = int(count_x)
    game_stats.cur_level_height = int(count_y)
    game_stats.selected_object = ""

    game_stats.map_positions = list(prepare_level.map_all_tiles())
    prepare_level.prepare_known_map(game_stats.player_power)
    prepare_level.set_pov_pos(game_stats.player_power, level_type)
    prepare_level.prepare_AI_class_AI_cogs()
    prepare_level.prepare_regiments()
    prepare_level.prepare_leader_traits(game_stats.player_power)
    prepare_level.prepare_leader_nicknames()
    prepare_level.prepare_AI_army_roles()
    prepare_level.prepare_population_reserves()

    game_stats.pause_status = True
    game_stats.day = 0
    game_stats.hours = 0
    game_stats.minutes = 0
    game_stats.count_started = False

    game_stats.game_board_panel = ""

    game_stats.ongoing_wars = []

    game_obj.game_battles = []
    game_obj.game_rewards = []
    game_obj.game_wars = []

    # Update visuals
    update_gf_game_board.update_misc_sprites()
    update_gf_game_board.update_sprites()


def gather_level_information(folder, level_to_load):
    shelfFile = shelve.open(str(Path('levels/' + folder)) + '/' + level_to_load)

    realms = shelfFile["new_level_powers"]
    game_stats.start_level_total_realms = int(len(realms))
    game_stats.start_level_playable_realms = 0
    for realm in realms:
        # print(realm.name + "; playable is " + str(realm.playable))
        if realm.playable:
            # print(realm.name)
            game_stats.start_level_playable_realms += 1
            if game_stats.start_level_playable_realms == 1:
                # print(realm.name)
                game_stats.start_level_selected_realm = realm


def skirmish_previous_realm():
    if game_stats.start_level_playable_realms > 0:
        shelfFile = shelve.open(str(Path('levels/Skirmish')) + '/' + game_stats.levels_list[game_stats.level_index])

        realms = shelfFile["new_level_powers"]

        num = 0
        for realm in realms:
            if realm.name == game_stats.start_level_selected_realm.name:
                break
            num += 1

        searching = True
        while searching:
            if num - 1 < 0:
                num = game_stats.start_level_total_realms - 1
            else:
                num -= 1

            if realms[num].playable:
                searching = False
                game_stats.start_level_selected_realm = realms[num]


def skirmish_next_realm():
    if game_stats.start_level_playable_realms > 0:
        shelfFile = shelve.open(str(Path('levels/Skirmish')) + '/' + game_stats.levels_list[game_stats.level_index])

        realms = shelfFile["new_level_powers"]

        num = 0
        for realm in realms:
            if realm.name == game_stats.start_level_selected_realm.name:
                break
            num += 1

        searching = True
        while searching:
            if num + 1 == game_stats.start_level_total_realms:
                num = 0
            else:
                num += 1

            if realms[num].playable:
                searching = False
                game_stats.start_level_selected_realm = realms[num]


# assign_parameters = {"Test level": "First",
#                      "New name": "First",
#                      "Derete": None}
