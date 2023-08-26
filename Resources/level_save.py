## Miracle battles!
## level_save

import shelve
from pathlib import Path

from Resources import game_stats


# Start saving new level
def save_new_level():
    if game_stats.LE_level_type == "Skirmish":
        check_playable_realms()

    folder = str(game_stats.LE_level_type)
    shelfFile = shelve.open(str(Path('levels/' + folder)) + '/' + game_stats.new_level_name)

    shelfFile["new_level_named"] = game_stats.new_level_name

    shelfFile["new_level_type"] = game_stats.LE_level_type

    shelfFile["new_level_year"] = game_stats.LE_year

    shelfFile["new_level_month"] = game_stats.LE_month

    shelfFile["new_level_map"] = game_stats.level_map

    shelfFile["new_level_powers"] = game_stats.editor_powers

    shelfFile["new_level_cities"] = game_stats.editor_cities

    shelfFile["new_level_armies"] = game_stats.editor_armies

    shelfFile["new_level_LE_cities_id_counter"] = game_stats.LE_cities_id_counter

    shelfFile["new_level_LE_army_id_counter"] = game_stats.LE_army_id_counter

    shelfFile["new_level_LE_hero_id_counter"] = game_stats.LE_hero_id_counter

    shelfFile["new_level_LE_population_id_counter"] = game_stats.LE_population_id_counter

    shelfFile.close()


# Save current game
def save_game():
    shelfFile = shelve.open(str(Path('savefiles')) + '/' + game_stats.new_level_name)

    shelfFile["new_level_named"] = game_stats.new_level_name

    shelfFile["new_level_map"] = game_stats.level_map

    shelfFile["new_level_factions"] = game_stats.editor_factions

    shelfFile["new_level_id_counter"] = game_stats.person_id_counter

    shelfFile.close()


def check_playable_realms():
    # In case there is no playable realms for human player in skirmish scenario
    # then all realms should be made to be playable
    no_playable_realms = True
    for realm in game_stats.editor_powers:
        if realm.playable:
            no_playable_realms = False
            break

    if no_playable_realms:
        for realm in game_stats.editor_powers:
            realm.playable = True
