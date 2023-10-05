## Miracle battles
## battle_map_generation

import random

from Resources import game_stats
from Resources import game_classes
from Resources import game_obj
from Resources import update_gf_battle

from Content import objects_img_catalog
from Content import terrain_seasons


def create_battle_map():
    game_stats.game_board_panel = ""

    if game_stats.game_type == "singleplayer":
        game_stats.strategy_mode = False

    game_stats.current_screen = "Battle"
    print(game_stats.current_screen)
    game_stats.screen_to_draw = "battle_screen"

    # Create battle
    game_stats.battle_id_counter += 1

    # Preparing battle map
    new_battle_map = []
    for y in range(1, game_stats.battle_height + 1):
        for x in range(1, game_stats.battle_width + 1):
            new_battle_map.append(game_classes.Battle_Tile((x, y),
                                                           game_stats.battle_terrain,
                                                           game_stats.battle_conditions))
    # Adding obstacles on map
    grid_for_obstacle = []
    for y in range(1, game_stats.battle_height + 1):
        for x in range(3, game_stats.battle_width - 1):
            grid_for_obstacle.append([x, y])
    number_of_obstacles = 5
    while number_of_obstacles > 0:
        xy = grid_for_obstacle.pop(random.choice(range(0, len(grid_for_obstacle))))
        TileNum = (xy[1] - 1) * game_stats.battle_width + xy[0] - 1
        tile_object = new_battle_map[TileNum]

        trees_list = []
        positioning = [[1, 1], [2, 1], [3, 1], [4, 1], [5, 1],
                       [1, 2], [2, 2], [3, 2], [4, 1], [5, 2],
                       [1, 3], [2, 3], [3, 3], [4, 1], [5, 3],
                       [1, 4], [2, 4], [3, 4], [4, 4], [5, 4],
                       [1, 5], [2, 5], [3, 5], [4, 5], [5, 5]]
        number_of_objects = random.randint(12, 18)
        obstacle_name = str(random.choice(list(objects_img_catalog.object_variations)))
        number_variations = objects_img_catalog.object_variations[obstacle_name]
        update_gf_battle.add_obstacle_sprites(tile_object, game_stats.game_month, obstacle_name, "Nature/Trees/")
        for num in range(number_of_objects):
            pos = random.choice(positioning)
            positioning.remove(pos)
            variant = str(random.randint(1, number_variations))

            obj_cal = objects_img_catalog.object_calendar[obstacle_name]
            season = terrain_seasons.terrain_calendar[tile_object.terrain][game_stats.game_month]
            obj_img = game_stats.gf_obstacle_dict[obj_cal[season] + "_0" + variant]

            x_pos = int((96 / 5) * pos[0] + random.randint(-4, 4) - 8)
            y_pos = int((96 / 5) * pos[1] + random.randint(-4, 4) - obj_img.get_height()/2)
            trees_list.append(list([x_pos, y_pos, variant]))

        sorted_list = sorted(trees_list, key=lambda x: (x[1], x[0]))

        new_battle_map[TileNum].map_object = game_classes.Battle_Map_Object(str(obstacle_name),
                                                                            "Nature/Trees/",
                                                                            "Obstacle",
                                                                            list(sorted_list),
                                                                            False, None)
        number_of_obstacles -= 1

    starting_pov = [0, 0]
    cover_map = [3, 1, 16, 12]
    if game_stats.defender_realm == game_stats.player_power:
        starting_pov = [6, 0]
        cover_map = [1, 1, 14, 12]

    attacking_positions = []
    for x in range(1, 3):
        for y in range(1, game_stats.battle_height + 1):
            attacking_positions.append([x, y])
            starting_attacking_positions = list(attacking_positions)
    defending_positions = []
    for x in range(game_stats.battle_width - 1, game_stats.battle_width + 1):
        for y in range(1, game_stats.battle_height + 1):
            defending_positions.append([x, y])
            starting_defending_positions = list(defending_positions)

    for army in game_obj.game_armies:
        if army.army_id == game_stats.attacker_army_id:
            unit_num = 0
            for unit in army.units:
                unit.right_side = True
                spot = list(random.choice(attacking_positions))
                attacking_positions.remove(spot)
                unit.position = list(spot)
                unit.direction = "E"  # E
                x2 = int(spot[0])
                y2 = int(spot[1])
                TileNum = (y2 - 1) * game_stats.battle_width + x2 - 1
                new_battle_map[TileNum].unit_index = int(unit_num)
                new_battle_map[TileNum].army_id = int(game_stats.attacker_army_id)
                print("spot - " + str(spot) + " regiment - " + unit.name + " TileNum - " + str(TileNum) +
                      " side - " + str(unit.right_side))
                # Ground flying regiments
                unit.in_air = False
                unit_num += 1
        elif army.army_id == game_stats.defender_army_id:
            unit_num = 0
            for unit in army.units:
                unit.right_side = False
                spot = list(random.choice(defending_positions))
                defending_positions.remove(spot)
                unit.position = list(spot)
                unit.direction = "W"  # W
                x2 = int(spot[0])
                y2 = int(spot[1])
                TileNum = (y2 - 1) * game_stats.battle_width + x2 - 1
                new_battle_map[TileNum].unit_index = int(unit_num)
                new_battle_map[TileNum].army_id = int(game_stats.defender_army_id)
                print("spot - " + str(spot) + " regiment - " + unit.name + " TileNum - " + str(TileNum) +
                      " side - " + str(unit.right_side))
                # Ground flying regiments
                unit.in_air = False
                unit_num += 1

    print("game_stats.battle_conditions " + game_stats.battle_conditions)
    game_obj.game_battles.append(game_classes.Land_Battle(game_stats.battle_id_counter,
                                                          game_stats.attacker_army_id,
                                                          game_stats.attacker_realm,
                                                          game_stats.defender_army_id,
                                                          game_stats.defender_realm,
                                                          game_stats.battle_terrain,
                                                          game_stats.battle_conditions,
                                                          "Land battle",
                                                          new_battle_map,
                                                          starting_pov,
                                                          cover_map,
                                                          starting_attacking_positions,
                                                          starting_defending_positions,
                                                          game_stats.battle_result_script,
                                                          0, 0))

    # New visuals
    game_stats.gf_settlement_dict = {}
    game_stats.gf_facility_dict = {}
    game_stats.gf_exploration_dict = {}
    game_stats.gf_misc_img_dict = {}

    # Update visuals for battle
    update_gf_battle.battle_update_sprites()
    update_gf_battle.update_misc_sprites()
    game_stats.gf_battle_effects_dict = {}
