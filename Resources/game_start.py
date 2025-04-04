## Among Myth and Wonder
## game_start

import math, shelve
from pathlib import Path

from Resources import game_stats
from Resources import game_classes
from Resources.Game_Graphics import graphics_basic
from Resources import algo_borders
from Content import terrain_catalog

# This function create a new level for level editor
def new_game():
    game_stats.map_operations = True
    game_stats.active_name_field = False
    game_stats.pov_pos = [0, 0]
    game_stats.edit_instrument = "select"
    game_stats.selected_tile = []
    # game_stats.faction_num = 0
    # game_stats.cities_id_counter = 0
    # game_stats.lv_year = 0
    # game_stats.lv_month = 5

    # Create level map
    nullify_level_editor_variables()
    tile_cells = game_stats.new_level_width * game_stats.new_level_height
    print("Number of tile cells - " + str(tile_cells) + " with width "
          + str(game_stats.new_level_width) + " and height " + str(game_stats.new_level_height))
    tile_number = 1
    # print("Test: 1) game_stats.level_map - " + str(len(game_stats.level_map)))

    while tile_number <= tile_cells:
        # Create strategy map
        x = int(tile_number % game_stats.new_level_width)
        if x == 0:
            x = int(game_stats.new_level_width)
        y = int(math.ceil(tile_number / game_stats.new_level_width))
        game_stats.level_map.append(game_classes.Tile((x, y), "Plain",
                                                      terrain_catalog.terrain_calendar["Plain"][game_stats.LE_month]))

        # Create empty realm borders map
        game_stats.LE_borders_map.append(None)

        # print("x, y - " + str(x) + " " + str(y))
        tile_number += 1

    # print("Test: 2) game_stats.level_map - " + str(len(game_stats.level_map)))
    graphics_basic.init_level_editor_graphics()


def nullify_level_editor_variables():
    game_stats.level_map = []
    game_stats.LE_borders_map = []
    game_stats.editor_powers = []
    game_stats.editor_cities = []
    game_stats.editor_armies = []
    game_stats.LE_cities_id_counter = 0
    game_stats.LE_army_id_counter = 0
    game_stats.LE_hero_id_counter = 0
    game_stats.LE_population_id_counter = 0
    game_stats.LE_faction_id_counter = 0


# This function load an existing level for level editor
def load_level_into_editor():
    folder = "Skirmish"
    level_to_load = game_stats.levels_list[game_stats.level_index]
    shelfFile = shelve.open(str(Path('levels/' + folder)) + '/' + level_to_load)

    game_stats.map_operations = True
    game_stats.active_name_field = False
    game_stats.pov_pos = [0, 0]
    game_stats.edit_instrument = "select"
    game_stats.selected_tile = []

    nullify_level_editor_variables()

    game_stats.new_level_name = shelfFile["new_level_named"]
    game_stats.LE_year = shelfFile["new_level_year"]
    game_stats.LE_month = shelfFile["new_level_month"]
    game_stats.level_map = shelfFile["new_level_map"]

    game_stats.editor_powers = shelfFile["new_level_powers"]
    game_stats.editor_cities = shelfFile["new_level_cities"]
    game_stats.editor_armies = shelfFile["new_level_armies"]

    game_stats.LE_cities_id_counter = shelfFile["new_level_LE_cities_id_counter"]
    game_stats.LE_army_id_counter = shelfFile["new_level_LE_army_id_counter"]
    game_stats.LE_hero_id_counter = shelfFile["new_level_LE_hero_id_counter"]
    game_stats.LE_population_id_counter = shelfFile["new_level_LE_population_id_counter"]
    game_stats.LE_faction_id_counter = shelfFile["new_level_LE_faction_id_counter"]

    shelfFile.close()

    max_x = 0
    max_y = 0
    for tile in game_stats.level_map:
        if tile.posxy[0] > max_x:
            max_x = tile.posxy[0]
        if tile.posxy[1] > max_y:
            max_y = tile.posxy[1]
    game_stats.new_level_width = int(max_x)
    game_stats.new_level_height = int(max_y)
    tile_cells = game_stats.new_level_width * game_stats.new_level_height
    print("Number of tile cells - " + str(tile_cells) + " with width "
          + str(game_stats.new_level_width) + " and height " + str(game_stats.new_level_height))

    tile_number = 1
    while tile_number <= tile_cells:
        # Create empty realm borders map
        game_stats.LE_borders_map.append(None)
        tile_number += 1

    algo_borders.refresh_borders(range(0, tile_cells))

    # for i in range(0, tile_cells):
    #     rb = game_stats.LE_borders_map[i]
    #     print("rb type - " + str(type(rb)))

    # print("game_stats.editor_cities - " + str(game_stats.editor_cities))
    graphics_basic.init_level_editor_graphics()
