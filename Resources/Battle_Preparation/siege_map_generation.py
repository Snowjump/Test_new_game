## Among Myth and Wonder
## siege_map_generation

import math
import random

from Resources import game_stats
from Resources import game_obj
from Resources import game_classes
from Resources import effect_classes
from Resources import update_gf_battle
from Resources import common_selects

from Content import objects_img_catalog
from Content import terrain_seasons


def generate_map(attacker, defender):
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
        for x in range(3, game_stats.battle_width - 3):
            grid_for_obstacle.append([x, y])
    number_of_obstacles = random.randrange(3, 6)
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

    settlement = None
    for city in game_obj.game_cities:
        if city.city_id == game_stats.selected_settlement:
            settlement = city
            break

    # Add settlements defensive structures to battle map
    add_defences(new_battle_map, settlement)

    starting_pov = [0, 0]
    cover_map = [3, 1, 16, 12]
    if game_stats.defender_realm == game_stats.player_power:
        starting_pov = [6, 0]
        cover_map = [1, 1, 13, 12]

    starting_attacking_positions = []
    starting_defending_positions = []
    attacking_positions = []
    defending_positions = []

    for x in range(1, 3):
        for y in range(1, game_stats.battle_height + 1):
            attacking_positions.append([x, y])
            starting_attacking_positions = list(attacking_positions)
    for x in range(game_stats.battle_width - 2, game_stats.battle_width + 1):
        for y in range(1, game_stats.battle_height + 1):
            defending_positions.append([x, y])
            starting_defending_positions = list(defending_positions)

    unit_num = 0
    for unit in attacker.units:
        spot = list(random.choice(attacking_positions))
        attacking_positions.remove(spot)
        unit.position = list(spot)
        unit.direction = "E"  # E
        unit.right_side = True
        x2 = int(spot[0])
        y2 = int(spot[1])
        TileNum = (y2 - 1) * game_stats.battle_width + x2 - 1
        new_battle_map[TileNum].unit_index = int(unit_num)
        new_battle_map[TileNum].army_id = int(game_stats.attacker_army_id)
        print("spot - " + str(spot) + " regiment - " + unit.name + " TileNum - " + str(TileNum))
        print(unit.img_source + "/" + unit.img)
        # Ground flying regiments
        unit.in_air = False
        unit_num += 1

    unit_num = 0
    for unit in defender.units:
        spot = list(random.choice(defending_positions))
        defending_positions.remove(spot)
        unit.position = list(spot)
        unit.direction = "W"  # W
        unit.right_side = False
        x2 = int(spot[0])
        y2 = int(spot[1])
        TileNum = (y2 - 1) * game_stats.battle_width + x2 - 1
        new_battle_map[TileNum].unit_index = int(unit_num)
        new_battle_map[TileNum].army_id = int(game_stats.defender_army_id)
        print("spot - " + str(spot) + " regiment - " + unit.name + " TileNum - " + str(TileNum))
        print(unit.img_source + "/" + unit.img)
        # Ground flying regiments
        unit.in_air = False
        unit_num += 1

    game_obj.game_battles.append(game_classes.Land_Battle(game_stats.battle_id_counter,
                                                          game_stats.attacker_army_id,
                                                          game_stats.attacker_realm,
                                                          game_stats.defender_army_id,
                                                          game_stats.defender_realm,
                                                          game_stats.battle_terrain,
                                                          game_stats.battle_conditions,
                                                          "Siege",
                                                          new_battle_map,
                                                          starting_pov,
                                                          cover_map,
                                                          starting_attacking_positions,
                                                          starting_defending_positions,
                                                          game_stats.battle_result_script,
                                                          settlement.siege.siege_towers_ready,
                                                          settlement.siege.battering_rams_ready))

    game_stats.present_battle = common_selects.select_battle_by_realm_name(game_stats.player_power)

    game_stats.attacker_realm = ""
    game_stats.defender_realm = ""
    game_stats.blockaded_settlement_name = ""
    game_stats.selected_settlement = -1
    game_stats.selected_object = ""
    game_stats.selected_army = -1
    game_stats.selected_second_army = -1
    game_stats.details_panel_mode = ""
    game_stats.first_army_exchange_list = []
    game_stats.second_army_exchange_list = []

    # New visuals
    game_stats.gf_settlement_dict = {}
    game_stats.gf_facility_dict = {}
    game_stats.gf_exploration_dict = {}
    game_stats.gf_misc_img_dict = {}

    # Update visuals for battle
    update_gf_battle.battle_update_sprites()
    update_gf_battle.update_misc_sprites()
    game_stats.gf_battle_effects_dict = {}


def add_defences(new_battle_map, settlement):

    for defensive_structure in settlement.defences:
        if defensive_structure.name == "Earth rampart":
            add_earth_rampart(new_battle_map)
        if defensive_structure.name == "Palisade":
            add_palisade(new_battle_map, defensive_structure.def_objects)


def add_earth_rampart(new_battle_map):
    x = game_stats.battle_width - 2
    for y in range(1, game_stats.battle_height + 1):
        TileNum = (y - 1) * game_stats.battle_width + x - 1
        effect1 = effect_classes.Battle_Structure_Effect(["NW", "W", "SW"],
                                                         "Incoming attack", 2,
                                                         "division", None)
        effect2 = effect_classes.Battle_Structure_Effect(["NW", "W", "SW"],
                                                         "Crush denied", None,
                                                         "ignored", None)
        properties = effect_classes.Battle_Structure_Properties([effect1, effect2])
        new_battle_map[TileNum].map_object = game_classes.Battle_Map_Object("Earth rampart",
                                                                            "Battle_objects/earthen_stakes",
                                                                            "Structure",
                                                                            [-10, -8],
                                                                            True, properties)


def add_palisade(new_battle_map, def_objects):
    x = game_stats.battle_width - 2

    y = 1
    for def_object in def_objects:
        TileNum = (y - 1) * game_stats.battle_width + x - 1
        name = None
        path = None
        position = None
        print("Name - " + str(def_object.section_name) + "; State - " + str(def_object.state))
        cover = "Medium fortification cover"
        if def_object.section_name == "Palisade wall section":
            # print("y - " + str(y) + "; height - " + str(game_stats.battle_height))
            if y != game_stats.battle_height:
                if def_object.state == "Unbroken":
                    name = "Palisade"
                    path = "Battle_objects/palisade"
                    position = [-5, -40]
                    properties = effect_classes.Battle_Structure_Properties([])
                    new_battle_map[TileNum].map_object = game_classes.Battle_Map_Object(name,
                                                                                        path,
                                                                                        "Structure",
                                                                                        position,
                                                                                        True, properties)
                else:  # "Broken"
                    cover = "Light fortification cover"
                    name = "Palisade_ruins"
                    path = "Battle_objects/palisade_destroyed"
                    position = [-5, -40]
                    properties = effect_classes.Battle_Structure_Properties([])
                    new_battle_map[TileNum].map_object = game_classes.Battle_Map_Object(name,
                                                                                        path,
                                                                                        "Structure",
                                                                                        position,
                                                                                        True, properties)
            else:
                if def_object.state == "Unbroken":
                    name = "Palisade_bottom"
                    path = "Battle_objects/palisade_bottom"
                    position = [-5, -40]
                    properties = effect_classes.Battle_Structure_Properties([])
                    new_battle_map[TileNum].map_object = game_classes.Battle_Map_Object(name,
                                                                                        path,
                                                                                        "Structure",
                                                                                        position,
                                                                                        True, properties)
                else:  # "Broken"
                    cover = "Light fortification cover"
                    name = "Palisade_bottom_ruins"
                    path = "Battle_objects/palisade_bottom_destroyed"
                    position = [-5, -40]
                    properties = effect_classes.Battle_Structure_Properties([])
                    new_battle_map[TileNum].map_object = game_classes.Battle_Map_Object(name,
                                                                                        path,
                                                                                        "Structure",
                                                                                        position,
                                                                                        True, properties)

        elif def_object.section_name == "Palisade gate":
            if def_object.state == "Unbroken":
                name = "Palisade_gates"
                path = "Battle_objects/palisade_gates"
                position = [-11, -40]
                properties = effect_classes.Battle_Structure_Properties([])
                new_battle_map[TileNum].map_object = game_classes.Battle_Map_Object(name,
                                                                                    path,
                                                                                    "Structure",
                                                                                    position,
                                                                                    True, properties)
            elif def_object.state == "Broken":
                cover = "Light fortification cover"
                name = "Palisade_gates_ruins"
                path = "Battle_objects/palisade_gates_destroyed"
                position = [-11, -40]
                properties = effect_classes.Battle_Structure_Properties([])
                new_battle_map[TileNum].map_object = game_classes.Battle_Map_Object(name,
                                                                                    path,
                                                                                    "Structure",
                                                                                    position,
                                                                                    True, properties)

        # Apply fortification cover
        CoverTileNum = (y - 1) * game_stats.battle_width + x - 1
        new_battle_map[CoverTileNum].aura_effects.append([-1,
                                                          [-1, -1],
                                                          cover])

        CoverTileNum = (y - 1) * game_stats.battle_width + x - 1 + 1
        new_battle_map[CoverTileNum].aura_effects.append([-1,
                                                          [-1, -1],
                                                          cover])

        CoverTileNum = (y - 1) * game_stats.battle_width + x - 1 + 2
        new_battle_map[CoverTileNum].aura_effects.append([-1,
                                                          [-1, -1],
                                                          cover])

        y += 1

    # # upper walls
    # for y in range(1, int(game_stats.battle_height / 2)):
    #     TileNum = (y - 1) * game_stats.battle_width + x - 1
    #
    #     properties = effect_classes.Battle_Structure_Properties([], ["NW", "W", "SW"], [])
    #     new_battle_map[TileNum].map_object = game_classes.Battle_Map_Object("Palisade",
    #                                                                         "Battle_objects/palisade",
    #                                                                         "Structure",
    #                                                                         [-5, -40],
    #                                                                         True, properties)
    #
    # # gates
    # TileNum = (int(game_stats.battle_height / 2) - 1) * game_stats.battle_width + x - 1
    #
    # properties = effect_classes.Battle_Structure_Properties([], ["NW", "W", "SW"], [])
    # new_battle_map[TileNum].map_object = game_classes.Battle_Map_Object("Palisade_gates",
    #                                                                     "Battle_objects/palisade_gates",
    #                                                                     "Structure",
    #                                                                     [-11, -40],
    #                                                                     True, properties)
    #
    # # lower walls
    # for y in range(int(game_stats.battle_height / 2 + 1), game_stats.battle_height):
    #     TileNum = (y - 1) * game_stats.battle_width + x - 1
    #
    #     properties = effect_classes.Battle_Structure_Properties([], ["NW", "W", "SW"], [])
    #     new_battle_map[TileNum].map_object = game_classes.Battle_Map_Object("Palisade",
    #                                                                         "Battle_objects/palisade",
    #                                                                         "Structure",
    #                                                                         [-5, -40],
    #                                                                         True, properties)
    #
    # # bottom block
    # TileNum = (int(game_stats.battle_height) - 1) * game_stats.battle_width + x - 1
    #
    # properties = effect_classes.Battle_Structure_Properties([], ["NW", "W", "SW"], [])
    # new_battle_map[TileNum].map_object = game_classes.Battle_Map_Object("Palisade_bottom",
    #                                                                     "Battle_objects/palisade_bottom",
    #                                                                     "Structure",
    #                                                                     [-5, -40],
    #                                                                     True, properties)
