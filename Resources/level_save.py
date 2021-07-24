## Miracle battles!

import shelve
from pathlib import Path

from Resources import game_stats

# Start saving new level
def save_new_level():
    shelfFile = shelve.open(str(Path('levels')) + '/' + game_stats.new_level_name)

    shelfFile["new_level_named"] = game_stats.new_level_name

    shelfFile["new_level_year"] = game_stats.LE_year

    shelfFile["new_level_month"] = game_stats.LE_month

    shelfFile["new_level_map"] = game_stats.level_map

    shelfFile["new_level_powers"] = game_stats.editor_powers

    shelfFile["new_level_cities"] = game_stats.editor_cities

    shelfFile["new_level_armies"] = game_stats.editor_armies

    shelfFile["new_level_LE_cities_id_counter"] = game_stats.LE_cities_id_counter

    shelfFile["new_level_LE_army_id_counter"] = game_stats.LE_army_id_counter

    shelfFile.close()

# Save current game
def save_game():
    shelfFile = shelve.open(str(Path('savefiles')) + '/' + game_stats.new_level_name)

    shelfFile["new_level_named"] = game_stats.new_level_name

    shelfFile["new_level_map"] = game_stats.level_map

    shelfFile["new_level_factions"] = game_stats.editor_factions

    shelfFile["new_level_id_counter"] = game_stats.person_id_counter

    shelfFile.close()