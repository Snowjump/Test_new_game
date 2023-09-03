## Miracle battles

import random, pygame, math

from Resources import game_stats
from Resources import game_classes
from Content import terrain_catalog


def new_game():
    game_stats.map_operations = True
    game_stats.active_name_field = False
    game_stats.pov_pos = [0, 0]
    game_stats.edit_instrument = "select"
    game_stats.selected_tile = []
    game_stats.faction_num = 0
    game_stats.cities_id_counter = 0
    game_stats.lv_year = 0
    game_stats.lv_month = 5

    # Create level map
    nullify_level_editor_variables()
    tile_cells = game_stats.new_level_width * game_stats.new_level_height
    print("Number of tile cells - " + str(tile_cells) + " with width "
          + str(game_stats.new_level_width) + " and height " + str(game_stats.new_level_height))
    tile_number = 1
    # print("Test: 1) game_stats.level_map - " + str(len(game_stats.level_map)))

    while tile_number <= tile_cells:
        x = int(tile_number % game_stats.new_level_width)
        if x == 0:
            x = int(game_stats.new_level_width)
        y = int(math.ceil(tile_number / game_stats.new_level_width))
        game_stats.level_map.append(game_classes.Tile((x, y), "Plain",
                                                      terrain_catalog.terrain_calendar["Plain"][game_stats.LE_month]))
        # print("x, y - " + str(x) + " " + str(y))
        tile_number += 1

    # print("Test: 2) game_stats.level_map - " + str(len(game_stats.level_map)))


def nullify_level_editor_variables():
    game_stats.level_map = []
    game_stats.editor_powers = []
    game_stats.editor_cities = []
    game_stats.editor_armies = []
    game_stats.LE_cities_id_counter = 0
    game_stats.LE_army_id_counter = 0
    game_stats.LE_hero_id_counter = 0
    game_stats.LE_population_id_counter = 0
    game_stats.LE_faction_id_counter = 0
