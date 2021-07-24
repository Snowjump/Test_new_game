## Miracle battles!

import math
import random

from Content import building_drafts
from Resources import game_classes
from Resources import game_obj
from Resources import game_pathfinding
from Resources import game_stats
from Resources import algo_circle_range
from Resources import game_battle


def establish_leader(focus):
    for army in game_stats.editor_armies:
        if army.army_id == focus:
            # Check if army has a hero
            if army.hero_id is None:
                # Check if army has any units
                if len(army.units) == 0:
                    army.leader = None
                else:
                    # List all units and their ranks
                    ledger = []
                    index = 0
                    for unit in army.units:
                        ledger.append([index, unit.rank])
                        index += 1

                    # Find unit with highest rank
                    leader = None
                    for item in ledger:
                        if leader == None:
                            leader = list(item)
                        elif item[1] > leader[1]:
                            leader = list(item)

                    # Set army's leader unit
                    army.leader = int(leader[0])


def prepare_known_map(player_power):
    for power in game_obj.game_powers:
        if power.name == player_power:
            power.known_map = []

            for city in game_obj.game_cities:
                print("Settlement " + str(city.name) + " location is " + str(city.location))
                if city.owner == player_power:

                    x = int((city.location + 1) % game_stats.cur_level_width)
                    y = int(math.ceil((city.location + 1) / game_stats.cur_level_width))
                    print("X is " + str(x) + " and Y is " + str(y))
                    if [x, y] not in power.known_map:
                        power.known_map.append([x, y])
                    if x - 1 > 0:
                        if [x - 1, y] not in power.known_map:
                            power.known_map.append([x - 1, y])
                    if x + 1 <= game_stats.cur_level_width:
                        if [x + 1, y] not in power.known_map:
                            game_stats.known_map.append([x + 1, y])
                    if y - 1 > 0:
                        if [x, y - 1] not in power.known_map:
                            power.known_map.append([x, y - 1])
                    if y + 1 <= game_stats.cur_level_height:
                        if [x, y + 1] not in power.known_map:
                            power.known_map.append([x, y + 1])

                    if x - 1 > 0 and y - 1 > 0:
                        if [x - 1, y - 1] not in power.known_map:
                            power.known_map.append([x - 1, y - 1])
                    if x - 1 > 0 and y + 1 <= game_stats.cur_level_height:
                        if [x - 1, y + 1] not in power.known_map:
                            power.known_map.append([x - 1, y + 1])
                    if x + 1 <= game_stats.cur_level_width and y - 1 > 0:
                        if [x + 1, y - 1] not in power.known_map:
                            power.known_map.append([x + 1, y - 1])
                    if x + 1 <= game_stats.cur_level_width and y + 1 <= game_stats.cur_level_height:
                        if [x + 1, y + 1] not in power.known_map:
                            power.known_map.append([x + 1, y + 1])

            for army in game_obj.game_armies:
                print("Army location is " + str(army.location))
                print("Army owner is " + str(army.owner))
                if army.owner == player_power:
                    print("Army location is " + str(army.location))
                    x = int((army.location + 1) % game_stats.cur_level_width)
                    y = int(math.ceil((army.location + 1) / game_stats.cur_level_width))
                    print("X is " + str(x) + " and Y is " + str(y))
                    for tile in algo_circle_range.within_circle_range([x, y], 5):
                        if tile not in power.known_map:
                            power.known_map.append(tile)
                    # if [x, y] not in power.known_map:
                    #     power.known_map.append([x, y])
                    # if x - 1 > 0:
                    #     if [x - 1, y] not in power.known_map:
                    #         power.known_map.append([x - 1, y])
                    # if x + 1 <= game_stats.cur_level_width:
                    #     if [x + 1, y] not in power.known_map:
                    #         power.known_map.append([x + 1, y])
                    # if y - 1 > 0:
                    #     if [x , y - 1] not in power.known_map:
                    #         power.known_map.append([x, y - 1])
                    # if y + 1 <= game_stats.cur_level_height:
                    #     if [x, y + 1] not in power.known_map:
                    #         power.known_map.append([x, y + 1])
                    #
                    # if x - 1 > 0 and y - 1 > 0:
                    #     if [x - 1, y - 1] not in power.known_map:
                    #         power.known_map.append([x - 1, y - 1])
                    # if x - 1 > 0 and y + 1 <= game_stats.cur_level_height:
                    #     if [x - 1, y + 1] not in power.known_map:
                    #         power.known_map.append([x - 1, y + 1])
                    # if x + 1 <= game_stats.cur_level_width and y - 1 > 0:
                    #     if [x + 1, y - 1] not in power.known_map:
                    #         power.known_map.append([x + 1, y - 1])
                    # if x + 1 <= game_stats.cur_level_width and y + 1 <= game_stats.cur_level_height:
                    #     if [x + 1, y + 1] not in power.known_map:
                    #         power.known_map.append([x + 1, y + 1])


def open_tiles(condition, realm, location, next_point):
    for power in game_obj.game_powers:
        if power.name == realm:
            if condition == "Army":
                for tile in algo_circle_range.within_circle_range(next_point, 5):
                    if tile not in power.known_map:
                        power.known_map.append(tile)


def advance_time():
    # print("It works - " + str(math.floor(game_stats.display_time/1000) % 5))
    if math.floor(game_stats.display_time / 1000) % 1 == 0:
        # print("math.floor(game_stats.display_time/1000) % 5 == 0")
        # print("game_stats.last_change - " + str(game_stats.last_change))
        # print("math.floor(game_stats.display_time/1000) - " + str(math.floor(game_stats.display_time/1000)))
        if math.floor(game_stats.display_time / 1000) != game_stats.last_change:
            # print("math.floor(game_stats.display_time/1000) != game_stats.last_change")
            game_stats.last_change = math.floor(game_stats.display_time / 1000)
            # print(str(game_stats.last_change))
            if game_stats.minutes + 15 != 60:
                game_stats.minutes += 15
            else:
                game_stats.minutes = 0
                if game_stats.hours + 1 != 24:
                    game_stats.hours += 1
                else:
                    game_stats.hours = 0
                    game_stats.day += 1

            perform_actions()  # Characters complete actions from their tasks
            # if game_stats.current_screen == "Battle":
                # print("game_stats.current_screen - " + str(game_stats.current_screen))
                # game_battle.perform_battle_actions()
            turn_end()


def turn_end():
    everyone_is_ready = True
    for realm in game_obj.game_powers:
        if not realm.turn_completed:
            everyone_is_ready = False

    # Every player has ended his turn
    if everyone_is_ready:
        # Replenish movement points
        if len(game_obj.game_armies) > 0:
            for army in game_obj.game_armies:
                for unit in army.units:
                    unit.movement_points = int(unit.max_movement_points)

        # Refresh hourglass icon
        game_stats.turn_hourglass = False

        # Next month
        if game_stats.game_month + 1 > 12:
            game_stats.game_month = 1
            game_stats.game_year += 1
        else:
            game_stats.game_month += 1
        print("game_stats.game_month - " + str(game_stats.game_month)
              + " game_stats.game_year - " + str(game_stats.game_year))

        # Set players to not ready to end turn
        for realm in game_obj.game_powers:
            realm.turn_completed = False


def generate_resources(throws, material, TileNum, level=None):
    resource = {"Rock": "Rock chunk",
                "Red cap": "Red cap",
                "White leg": "White leg"}

    print("Generating resources")
    target = 75
    if level is not None:
        target = level

    for throw in range(1, int(throws) + 1):
        print("Throw number " + str(throw))
        result = random.randrange(1, 101)
        print("result is " + str(result))
        if result <= target:
            game_obj.game_map[TileNum - 1].output.append(resource[material])
            print("Tile " + str(TileNum) + " got new " + str(resource[material]))


def movement_action(army):
    next_point = list(army.route[0])
    TileNum = (next_point[1] - 1) * game_stats.cur_level_width + next_point[0] - 1
    TileObj = game_obj.game_map[TileNum]

    if TileObj.army_id is not None:
        if len(army.route) == 1:
            for found_army in game_obj.game_armies:
                if found_army.owner == "Neutral":
                    print("Engage neutral enemy army")
                    print("TileObj.conditions " + str(TileObj.conditions))
                    engage_army(army, found_army, TileObj.terrain, TileObj.conditions)

    elif TileObj.lot is not None:
        # if TileObj.lot == "Settlement":
        #     print("Moving to settlement - " + str(TileObj.lot.name))
        #     route = algo_astar.astar(selected_army, start, tile_position, "Settlement")

        if TileObj.lot.obj_typ == "Obstacle":
            if TileObj.travel:
                print("Moving to cross-country")
                change_position(army)

        elif TileObj.lot.obj_typ == "Facility":
            print("Moving to " + str(TileObj.lot.obj_name))
            change_position(army)

    else:
        print("Moving to empty location")
        change_position(army)


def change_position(army):
    if army.action == "Ready to move":
        army.action = "Move"
    else:
        if enough_movement_points(army):
            spent_movement_points(army)
            next_point = list(army.route[0])
            TileNum = (next_point[1] - 1) * game_stats.cur_level_width + next_point[0] - 1

            game_obj.game_map[army.location].army_id = None
            game_obj.game_map[TileNum].army_id = army.army_id
            army.location = int(TileNum)
            army.posxy = list(next_point)

            del army.route[0]
            del army.path_arrows[0]

            open_tiles("Army", army.owner, TileNum, next_point)

            if len(army.route) == 0:
                army.action = "Stand"
            else:
                if not enough_movement_points(army):
                    army.action = "Stand"
        else:
            army.action = "Stand"


def spent_movement_points(army):
    child = army.route[0]
    parent = army.posxy
    distance = 100 * (math.sqrt(((child[0] - parent[0]) ** 2) + ((child[1] - parent[1]) ** 2)))
    for unit in army.units:
        unit.movement_points -= distance


def enough_movement_points(army):
    child = army.route[0]
    parent = army.posxy
    distance = 100 * (math.sqrt(((child[0] - parent[0]) ** 2) + ((child[1] - parent[1]) ** 2)))
    enough = True
    for unit in army.units:
        if unit.movement_points - distance < 0:
            enough = False
            continue
    return enough


def engage_army(attacker, defender, terrain, conditions):
    print("Engaging " + str(attacker.army_id) + " vs " + str(defender.army_id))

    # print("Found defending army " + str(defender.army_id))
    defender.action = "Fighting"

    # print("Found attacking army " + str(attacker.army_id))
    attacker.action = "Fighting"

    if attacker.owner == game_stats.player_power:
        game_stats.attacker_army_id = int(attacker.army_id)
        game_stats.attacker_realm = str(attacker.owner)
        game_stats.defender_army_id = int(defender.army_id)
        game_stats.defender_realm = str(defender.owner)
        game_stats.battle_type = "Battle"
        game_stats.battle_terrain = str(terrain)
        game_stats.battle_conditions = str(conditions)

        # print('game_stats.game_board_panel = "begin battle panel"')
        game_stats.game_board_panel = "begin battle panel"

    # for army in game_obj.game_armies:
    #     if army.army_id == defender_id:
    #         print("Found defending army " + str(army.army_id))
    #         army.action = "Fighting"
    #
    # for army in game_obj.game_armies:
    #     if army.army_id == attacker_id:
    #         print("Found attacking army " + str(army.army_id))
    #         army.action = "Fighting"
    #         if army.owner == game_stats.player_power:
    #             print('game_stats.game_board_panel = "begin battle"')
    #             game_stats.game_board_panel = "begin battle"


def perform_actions():
    for army in game_obj.game_armies:
        if army.action == "Move" or army.action == "Ready to move":
            movement_action(army)
