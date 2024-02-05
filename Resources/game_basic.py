## Among Myth and Wonder
## game_basic

import math
import random

from Storage import create_unit

from Content import starting_skills
from Content import exploration_catalog
from Content import exploration_scripts
from Content import study_abilities_catalog
from Content import exploration_objs_replenishment
from Content import buy_resources
from Content import recruitment_structures
from Content import terrain_catalog
from Content import siege_warfare_catalog
from Content import unit_alignment_catalog
from Content import enlist_regiment_prices

from Resources import game_classes
from Resources import game_obj
from Resources import game_stats
from Resources import graphics_basic
from Resources import game_diplomacy
from Resources import algo_circle_range
from Resources import economy
from Resources import algo_building
from Resources import update_gf_game_board
from Resources import algo_path_arrows
from Resources import siege_warfare
from Resources import game_autobattle
from Resources import common_selects

from Content.Quests import knight_lords_cond
from Content.Quests import knight_lords_quest_result_scripts

from Strategy_AI import strategy_logic
from Strategy_AI import AI_exploration_scripts
from Strategy_AI import AI_learn_skills
from Strategy_AI import AI_learn_attributes

from Strategy_AI.Logic_Solutions import power_ranking
from Strategy_AI.Logic_Solutions import exploration_targets


def establish_leader(focus, mode):
    obj_list = None
    if mode == "Game":
        obj_list = game_obj.game_armies
    else:
        obj_list = game_stats.editor_armies
    for army in obj_list:
        if army.army_id == focus:
            # Check if army has a hero
            if army.hero is None:
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
                        if leader is None:
                            leader = list(item)
                        elif item[1] > leader[1]:
                            leader = list(item)

                    # Set army's leader unit
                    army.leader = int(leader[0])
                    print("Army ID - " + str(focus) + ", leader - " + str(leader))

            break


def open_tiles(condition, the_army, location, next_point, own_realm):
    explored_cities = []  # IDs
    explored_armies = []  # IDs

    the_role = None
    for role in own_realm.AI_cogs.army_roles:
        if role.army_id == the_army.army_id:
            the_role = role.army_role
            break

    if condition == "Army":
        targets = []
        for tile in algo_circle_range.within_circle_range(next_point, 5):
            if tile not in own_realm.known_map:
                # print("Discovered new tile - " + str(tile))
                own_realm.known_map.append(tile)

                if own_realm.AI_player:
                    targets.append(tile)

                if the_role == "Adventure":
                    if len(the_army.route) > 0:
                        if the_army.route[-1] == tile:
                            the_army.route = []
                            the_army.path_arrows = []
                            the_army.action = "Stand"
                            print("Discovered target - " + str(tile))

            TileNum = (tile[1] - 1) * game_stats.cur_level_width + tile[0] - 1
            TileObj = game_obj.game_map[TileNum]

            if TileObj.city_id is not None:
                if TileObj.city_id not in explored_cities:
                    explored_cities.append(TileObj.city_id)

            if TileObj.army_id is not None:
                if TileObj.army_id not in explored_cities:
                    explored_armies.append(TileObj.army_id)

        if targets:
            for tile in targets:
                if tile in own_realm.AI_cogs.exploration_targets:
                    own_realm.AI_cogs.exploration_targets.remove(tile)

            exploration_targets.collect_new_exploration_targets(own_realm, own_realm.known_map,
                                                                own_realm.AI_cogs.exploration_targets)

    # Update contacts if met new realms
    for settlement in game_obj.game_cities:
        if settlement.city_id in explored_cities:
            if settlement.owner != own_realm.name:
                if settlement.owner not in own_realm.contacts:
                    own_realm.contacts.append(str(settlement.owner))
                    for contacted_realm in game_obj.game_powers:
                        if contacted_realm.name == settlement.owner:
                            if own_realm.name not in contacted_realm.contacts:
                                contacted_realm.contacts.append(str(own_realm.name))
                            break

    for army in game_obj.game_armies:
        if army.army_id in explored_armies:
            if army.owner != own_realm.name:
                if army.owner not in own_realm.contacts:
                    own_realm.contacts.append(str(army.owner))
                    for contacted_realm in game_obj.game_powers:
                        if contacted_realm.name == army.owner:
                            if own_realm.name not in contacted_realm.contacts:
                                contacted_realm.contacts.append(str(own_realm.name))
                            break


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

            strategy_logic.manage_realm()
            perform_actions()  # Characters complete actions from their tasks
            # Change directions
            for army in game_obj.game_armies:
                if len(army.route) > 0:
                    change_side_direction(army)
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
                additional_points = 0
                if army.hero is not None:
                    bonus_mana_increase = 0
                    total_knowledge = int(army.hero.knowledge)
                    # print("army.hero is not None")
                    for skill in army.hero.skills:
                        # print("Skill - " + str(skill.name))
                        for effect in skill.effects:
                            if effect.application == "Movement points":
                                if effect.method == "addition":
                                    # print("Additional movement " + str(effect.quantity))
                                    additional_points += int(effect.quantity)

                    if len(army.hero.inventory) > 0:
                        for artifact in army.hero.inventory:
                            if artifact.blocked == 0:
                                for effect in artifact.effects:
                                    if effect.application == "Knowledge":
                                        if effect.method == "addition":
                                            total_knowledge += int(effect.quantity)
                                    elif effect.application == "Mana replenishment":
                                        if effect.method == "addition":
                                            bonus_mana_increase += int(effect.quantity)
                                    elif effect.application == "Movement points":
                                        if effect.method == "addition":
                                            additional_points += int(effect.quantity)
                            else:
                                artifact.blocked -= 1

                    # Mana reserve
                    army.hero.max_mana_reserve = 10 * total_knowledge
                    mana_increase = 2 + math.ceil(army.hero.level / 5) + bonus_mana_increase

                    if army.hero.mana_reserve + mana_increase > army.hero.max_mana_reserve:
                        army.hero.mana_reserve = int(army.hero.max_mana_reserve)
                    else:
                        army.hero.mana_reserve += int(mana_increase)

                # Movement
                for unit in army.units:
                    unit.movement_points = int(unit.max_movement_points) + int(additional_points)
                    # print(unit.name + " has " + str(unit.movement_points) + " movement points")

                # Update arrow visuals
                if army.army_id == game_stats.selected_army:
                    if army.owner == game_stats.player_power:
                        if len(army.route) > 0:
                            route = list(army.route)
                            route.insert(0, list(army.posxy))
                            algo_path_arrows.construct_path(army.army_id, route)
                        break

                # Refresh shattered status
                if army.shattered == "Recovering":
                    army.shattered = "Stable"
                elif army.shattered == "Shattered":
                    army.shattered = "Recovering"

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

        # Change terrain conditions
        for Tile in game_obj.game_map:
            Tile.conditions = terrain_catalog.terrain_calendar[Tile.terrain][game_stats.game_month]
        # Set players to not ready to end turn
        for realm in game_obj.game_powers:
            realm.turn_completed = False
            if realm.AI_player:
                realm.AI_cogs.economy_cogs.new_round = True
                realm.AI_cogs.cognition_stage = "Diplomacy"

                # Refresh armies roles
                for role in realm.AI_cogs.army_roles:
                    role.status = "Start"
                    if role.army_role == "Nothing to do":
                        role.army_role = "Idle"

        # Post turn computing
        # Economy
        print("")
        print("~~~ economy.snapshot_turnover()")
        economy.snapshot_turnover()
        print("")
        print("~~~ economy.nullify_inner_market()")
        economy.nullify_inner_market()
        print("~~~ economy.nullify_market_demand()")
        economy.nullify_market_demand()
        print("~~~ economy.nullify_records()")
        economy.nullify_records()
        print("")
        print("~~~ economy.production()")
        economy.production()
        print("")
        print("~~~ economy.sell_to_inner_market()")
        economy.sell_to_inner_market()
        print("")
        print("~~~ economy.buy_from_inner_market()")
        economy.buy_from_inner_market()
        print("~~~ economy.consume_goods()")
        economy.consume_goods()
        print("")
        print("~~~ economy.nullify_turnover()")
        economy.nullify_turnover()

        # Consume military upkeep
        military_upkeep()

        #
        # Update control effects
        base_update_control()

        # Buildings
        print("replenish_buildings")
        replenish_buildings()
        print("algo_building.perform_construction()")
        algo_building.perform_construction()

        # Exploration objects
        print("exploration_objs_replenishment.replenish_objects()")
        exploration_objs_replenishment.replenish_objects()

        # Update settlement effects
        base_update_settlement_effects()

        # Close windows
        game_stats.right_window = ""
        # game_stats.rw_object = None

        # Update settlement information
        if game_stats.settlement_area == "Building":
            algo_building.check_requirements()
        elif game_stats.settlement_area == "Economy":
            if game_stats.settlement_subsection == "Overview":
                gather_province_records()
            elif game_stats.settlement_subsection == "Local market":
                snapshot_local_market()

        # Quests
        for settlement in game_obj.game_cities:
            settlement.new_quest_message_countdown -= 1
            if settlement.new_quest_message_countdown == 0:
                settlement.new_quest_message_countdown = random.randint(5, 11)
                create_new_quest_message(settlement)

        for realm in game_obj.game_powers:
            remove_list = []
            quest_num = 0
            for quest in realm.quests_messages:
                if quest.message_type == "Quest":
                    if quest.remaining_time is not None:
                        quest.remaining_time -= 1
                        if quest.remaining_time == 0:
                            remove_list.append(int(quest_num))
                            knight_lords_quest_result_scripts.result_scripts[quest.name](None, quest)
                            game_stats.quest_message_index = None
                quest_num += 1

            for remove_num in remove_list:
                del realm.quests_messages[remove_num]

        # Advance sieges
        for settlement in game_obj.game_cities:
            if settlement.siege is not None:
                siege_warfare.advance_siege(settlement, settlement.siege)

        if game_stats.game_board_panel == "settlement blockade panel":
            for army in game_obj.game_armies:
                if army.army_id == game_stats.selected_army:
                    settlement, defender = find_siege(army)

                    game_stats.assault_allowed = True
                    for defensive_structure in settlement.defences:
                        if defensive_structure.provide_wall:
                            game_stats.assault_allowed = False
                            for def_object in defensive_structure.def_objects:
                                if def_object.state in ["Broken", "Opened"]:
                                    game_stats.assault_allowed = True
                                    break

                    # Check available siege equipment
                    if not game_stats.assault_allowed:
                        if settlement.siege.siege_towers_ready + settlement.siege.battering_rams_ready > 0:
                            game_stats.assault_allowed = True

                    break

        # Advance war
        for war in game_obj.game_wars:
            war.war_duration += 1

        # Refresh interface
        if game_stats.game_board_panel == "diplomacy panel":
            if game_stats.diplomacy_area == "Draft a peace offer":
                game_diplomacy.prepare_war_summary()
                if game_stats.claimed_demands:
                    game_diplomacy.peace_acceptance()
                else:
                    game_diplomacy.prepare_peace_demands_summary()

        graphics_basic.prepare_resource_ribbon()

        # Update visuals
        update_gf_game_board.update_sprites()
        update_gf_game_board.update_regiment_sprites()


def replenish_buildings():
    for city in game_obj.game_cities:
        for plot in city.buildings:
            if plot.structure is not None:
                # print("Replenishing " + str(plot.structure.name))
                if len(plot.structure.recruitment) > 0:
                    if plot.status == "Built":
                        # print("Replenishing " + str(plot.structure.name))
                        for lodge in plot.structure.recruitment:
                            # print(str(lodge))
                            if lodge.ready_units != lodge.hiring_capacity:
                                replenish = True
                                # Check replenishment effects
                                for local_effect in city.local_effects:
                                    for effect in local_effect.content:
                                        if effect.application == "Replenishment and ready":
                                            for effect_tag in effect.tags:
                                                print(effect_tag)
                                                if effect_tag in recruitment_structures.unit_tags[lodge.unit_name]:
                                                    if effect.operator == "Banned":
                                                        replenish = False

                                if replenish:
                                    lodge.time_passed += 1
                                    if lodge.time_passed >= lodge.replenishment_rate:
                                        lodge.time_passed = 0
                                        lodge.ready_units += 1
                                else:
                                    lodge.time_passed = 0


def movement_action(army):
    next_point = list(army.route[0])
    TileNum = (next_point[1] - 1) * game_stats.cur_level_width + next_point[0] - 1
    TileObj = game_obj.game_map[TileNum]

    at_war_list = []
    own_realm = None

    for realm in game_obj.game_powers:
        if realm.name == army.owner:
            own_realm = realm
            for enemy in realm.relations.at_war:
                at_war_list.append(enemy[2])
            break

    if army.action == "Ready to move":
        army.action = "Move"
    elif army.action == "Move":
        # Check if route hasn't been blocked since last moment
        # or newly discovered tiles turned out to be unreachable
        print("army.route[:-1] - " + str(army.route[:-1]))
        cancel_movement = False
        for tile in army.route[:-1]:
            xTileNum = (tile[1] - 1) * game_stats.cur_level_width + tile[0] - 1
            xTileObj = game_obj.game_map[xTileNum]
            # print("xTileNum - " + str(xTileNum))
            if tile in own_realm.known_map:
                if xTileObj.army_id is not None:
                    cancel_movement = True
                    print("Army " + str(army.army_id) + " canceled movement, path is blocked by army " +
                          str(xTileObj.army_id))
                elif xTileObj.lot is not None:
                    if xTileObj.lot == "City":
                        cancel_movement = True
                    elif xTileObj.lot.obj_typ == "Obstacle":
                        if not xTileObj.travel:
                            print("Obstacle - cancel movement: xTileNum - " + str(xTileNum) + "; tile - " + str(tile))
                            cancel_movement = True
                    elif xTileObj.lot.obj_typ == "Facility":
                        print("Facility - cancel movement: xTileNum - " + str(xTileNum) + "; tile - " + str(tile))
                        cancel_movement = True
                    elif xTileObj.lot.obj_typ in exploration_catalog.exploration_objects_groups_cat:
                        print("Exploration - cancel movement: xTileNum - " + str(xTileNum) + "; tile - " + str(tile))
                        cancel_movement = True

        tile = army.route[-1]
        yTileNum = (tile[1] - 1) * game_stats.cur_level_width + tile[0] - 1
        yTileObj = game_obj.game_map[yTileNum]
        if tile in own_realm.known_map:
            if yTileObj.lot is not None:
                if yTileObj.lot == "City":
                    pass
                elif yTileObj.lot.obj_typ == "Obstacle":
                    if not yTileObj.travel:
                        print("Untravelable - cancel movement: yTileNum - " + str(yTileNum) + "; tile - " + str(tile))
                        cancel_movement = True

        if cancel_movement:
            print("Movement has been canceled")
            army.action = "Stand"
            army.route = []
            army.path_arrows = []
            reset_cognition_stage(realm)
            return

        # change_direction(army)
        # print("Army is moving to " + str(next_point))
        if TileObj.army_id is not None and TileObj.lot is None:
            if len(army.route) == 1:
                for found_army in game_obj.game_armies:
                    if found_army.army_id == TileObj.army_id:
                        print("")
                        if army.owner == found_army.owner:
                            print("Meeting ally army")
                            exchange_armies(army, found_army)

                        elif found_army.owner == "Neutral":
                            print("Engage neutral enemy army")
                            engage_army(army, found_army, TileObj.terrain, TileObj.conditions, "Attack")
                        elif found_army.owner in at_war_list:
                            print("Engaging " + str(found_army.owner) + "'s army")
                            # print("TileObj.conditions " + str(TileObj.conditions))
                            engage_army(army, found_army, TileObj.terrain, TileObj.conditions, "Attack")

                        break

        elif TileObj.lot is not None:
            # print("TileObj.lot - " + str(TileObj.lot))
            # if TileObj.lot == "Settlement":
            #     print("Moving to settlement - " + str(TileObj.lot.name))
            #     route = algo_astar.astar(selected_army, start, tile_position, "Settlement")

            if TileObj.lot == "City":
                # print("TileObj.city_id - " + str(TileObj.city_id))
                if TileObj.travel:
                    settlement = None
                    for city in game_obj.game_cities:
                        if city.city_id == TileObj.city_id:
                            settlement = city
                            break

                    # print("Settlement " + str(settlement.name))

                    if settlement.owner == army.owner:
                        if settlement.military_occupation:
                            if TileObj.army_id is None:
                                print("Moving to capture empty own settlement")
                                settlement.military_occupation = None

                                change_position(army, own_realm)
                                # If player has had selected an army, then it get deselected
                                if game_stats.selected_object == "Army" and army.owner == game_stats.player_power:
                                    game_stats.selected_object = ""
                                    game_stats.selected_army = -1
                                    game_stats.selected_second_army = -1
                                    game_stats.details_panel_mode = ""
                                    game_stats.game_board_panel = ""
                                    game_stats.first_army_exchange_list = []
                                    game_stats.second_army_exchange_list = []

                                    # Select settlement
                                    print("Moved to neutral settlement")
                                    game_stats.selected_object = "Settlement"
                                    game_stats.selected_settlement = int(game_obj.game_map[TileNum].city_id)
                                    game_stats.settlement_area = "Building"
                                    game_stats.building_row_index = 0
                                    game_stats.game_board_panel = "settlement panel"
                                    game_stats.details_panel_mode = "settlement lower panel"
                                    algo_building.check_requirements()

                                    # Update visuals
                                    update_gf_game_board.update_settlement_misc_sprites()
                                    update_gf_game_board.open_settlement_building_sprites()

                            else:
                                enemy_army = None
                                for found_army in game_obj.game_armies:
                                    if found_army.army_id == TileObj.army_id:
                                        enemy_army = found_army
                                        break
                                print("Blockade own settlement captured by enemy")
                                blockade_settlement(army, enemy_army, settlement, own_realm)

                        else:
                            if TileObj.army_id is None:
                                print("Moving to own empty settlement")
                                change_position(army, own_realm)
                                # If player has had selected an army, then it get deselected
                                if game_stats.selected_object == "Army" and army.owner == game_stats.player_power:
                                    game_stats.selected_object = ""
                                    game_stats.selected_army = -1
                                    game_stats.selected_second_army = -1
                                    game_stats.details_panel_mode = ""
                                    game_stats.game_board_panel = ""
                                    game_stats.first_army_exchange_list = []
                                    game_stats.second_army_exchange_list = []

                                    # Select settlement
                                    print("Moved to settlement")
                                    game_stats.selected_object = "Settlement"
                                    game_stats.selected_settlement = int(game_obj.game_map[TileNum].city_id)
                                    game_stats.settlement_area = "Building"
                                    game_stats.building_row_index = 0
                                    game_stats.game_board_panel = "settlement panel"
                                    game_stats.details_panel_mode = "settlement lower panel"
                                    algo_building.check_requirements()

                                    list_of_rows = []
                                    for plot in settlement.buildings:
                                        if int(plot.screen_position[1]) not in list_of_rows:
                                            list_of_rows.append(int(plot.screen_position[1]))

                                    game_stats.building_rows_amount = max(list_of_rows)

                                    # Update visuals
                                    update_gf_game_board.update_settlement_misc_sprites()
                                    update_gf_game_board.open_settlement_building_sprites()

                            else:
                                for found_army in game_obj.game_armies:
                                    if found_army.army_id == TileObj.army_id:
                                        print("Meeting ally army stationed in your settlement")
                                        exchange_armies(army, found_army)
                                        break

                    elif settlement.owner == "Neutral":
                        if TileObj.army_id is None:
                            print("Moving to capture empty neutral settlement")
                            settlement.owner = str(army.owner)

                            change_position(army, own_realm)
                            # If player has had selected an army, then it get deselected
                            if game_stats.selected_object == "Army" and army.owner == game_stats.player_power:
                                game_stats.selected_object = ""
                                game_stats.selected_army = -1
                                game_stats.selected_second_army = -1
                                game_stats.details_panel_mode = ""
                                game_stats.game_board_panel = ""
                                game_stats.first_army_exchange_list = []
                                game_stats.second_army_exchange_list = []

                                # Select settlement
                                print("Moved to neutral settlement")
                                game_stats.selected_object = "Settlement"
                                game_stats.selected_settlement = int(game_obj.game_map[TileNum].city_id)
                                game_stats.settlement_area = "Building"
                                game_stats.building_row_index = 0
                                game_stats.game_board_panel = "settlement panel"
                                game_stats.details_panel_mode = "settlement lower panel"
                                algo_building.check_requirements()

                                # Update visuals
                                update_gf_game_board.update_settlement_misc_sprites()
                                update_gf_game_board.open_settlement_building_sprites()

                        else:
                            enemy_army = None
                            for found_army in game_obj.game_armies:
                                if found_army.army_id == TileObj.army_id:
                                    enemy_army = found_army
                                    break
                            print("Blockade neutral settlement")
                            blockade_settlement(army, enemy_army, settlement, own_realm)

                    elif settlement.owner in at_war_list:
                        if settlement.military_occupation:
                            if settlement.military_occupation[2] != own_realm.name:
                                print("Settlement occupied by someone else")
                                pass
                            else:
                                if TileObj.army_id is None:
                                    change_position(army, own_realm)
                                    # If player has had selected an army, then it get deselected
                                    if game_stats.selected_object == "Army" and army.owner == game_stats.player_power:
                                        game_stats.selected_object = ""
                                        game_stats.selected_army = -1
                                        game_stats.selected_second_army = -1
                                        game_stats.details_panel_mode = ""
                                        game_stats.game_board_panel = ""
                                        game_stats.first_army_exchange_list = []
                                        game_stats.second_army_exchange_list = []

                                        # Select settlement
                                        print("Moved to settlement")
                                        game_stats.selected_object = "Settlement"
                                        game_stats.selected_settlement = int(game_obj.game_map[TileNum].city_id)
                                        game_stats.settlement_area = "Building"
                                        game_stats.building_row_index = 0
                                        game_stats.game_board_panel = "settlement panel"
                                        game_stats.details_panel_mode = "settlement lower panel"
                                        algo_building.check_requirements()

                                        # Update visuals
                                        update_gf_game_board.update_settlement_misc_sprites()
                                        update_gf_game_board.open_settlement_building_sprites()

                                else:
                                    for found_army in game_obj.game_armies:
                                        if found_army.army_id == TileObj.army_id:
                                            print("Meeting ally army stationed in occupied settlement")
                                            exchange_armies(army, found_army)
                                            break

                        else:
                            if TileObj.army_id is None:
                                print("Moving to capture empty enemy settlement")
                                settlement.military_occupation = [str(own_realm.f_color), str(own_realm.s_color),
                                                                  str(own_realm.name)]

                                change_position(army, own_realm)
                                # If player has had selected an army, then it get deselected
                                if game_stats.selected_object == "Army" and army.owner == game_stats.player_power:
                                    game_stats.selected_object = ""
                                    game_stats.selected_army = -1
                                    game_stats.selected_second_army = -1
                                    game_stats.details_panel_mode = ""
                                    game_stats.game_board_panel = ""
                                    game_stats.first_army_exchange_list = []
                                    game_stats.second_army_exchange_list = []

                                    # Select settlement
                                    print("Moved to neutral settlement")
                                    game_stats.selected_object = "Settlement"
                                    game_stats.selected_settlement = int(game_obj.game_map[TileNum].city_id)
                                    game_stats.settlement_area = "Building"
                                    game_stats.building_row_index = 0
                                    game_stats.game_board_panel = "settlement panel"
                                    game_stats.details_panel_mode = "settlement lower panel"
                                    algo_building.check_requirements()

                                    # Update visuals
                                    update_gf_game_board.update_settlement_misc_sprites()
                                    update_gf_game_board.open_settlement_building_sprites()

                            else:
                                enemy_army = None
                                for found_army in game_obj.game_armies:
                                    if found_army.army_id == TileObj.army_id:
                                        enemy_army = found_army
                                        break
                                print("Blockade enemy settlement")
                                blockade_settlement(army, enemy_army, settlement, own_realm)

            elif TileObj.army_id is not None:
                # Army standing on object
                if len(army.route) == 1:
                    for found_army in game_obj.game_armies:
                        if found_army.army_id == TileObj.army_id:
                            if army.owner == found_army.owner:
                                print("Meeting ally army")
                                exchange_armies(army, found_army)

                            else:
                                if found_army.owner == "Neutral":
                                    print("Engage neutral enemy army")
                                else:
                                    print("Engaging " + str(found_army.owner) + "'s army")
                                # print("TileObj.conditions " + str(TileObj.conditions))
                                engage_army(army, found_army, TileObj.terrain, TileObj.conditions, "Attack")

                            break

            elif TileObj.lot.obj_typ == "Obstacle":
                if TileObj.travel:
                    print("Moving to cross-country")
                    change_position(army, own_realm)

            elif TileObj.lot.obj_typ == "Facility":
                print("Moving to " + str(TileObj.lot.obj_name))
                change_position(army, own_realm)

            elif TileObj.lot.obj_typ in exploration_catalog.exploration_objects_groups_cat:
                print("Moving to " + str(TileObj.lot.obj_name))
                change_position(army, own_realm)
                if army.hero is not None:
                    if own_realm.AI_player:
                        AI_exploration_scripts.event_scripts[TileObj.lot.properties.obj_script](TileObj.lot, army)
                    else:
                        exploration_scripts.event_scripts[TileObj.lot.properties.obj_script](TileObj.lot, army)

        else:
            print("Moving to empty location")
            change_position(army, own_realm)


def routing_action(army):
    # Routed army must lose all its movement points
    for unit in army.units:
        unit.movement_points = 0

    next_point = list(army.route[0])
    TileNum = (next_point[1] - 1) * game_stats.cur_level_width + next_point[0] - 1
    TileObj = game_obj.game_map[TileNum]

    own_realm = None

    for realm in game_obj.game_powers:
        if realm.name == army.owner:
            own_realm = realm
            break

    if TileObj.army_id is not None:
        # Someone stays in the way
        army.action = "Stand"
        army.route = []
        army.path_arrows = []

    else:
        print("Army is routing")
        change_position(army, own_realm)


def change_position(army, own_realm):
    # print("army.action - " + str(army.action))
    # if army.action == "Ready to move":
    #     army.action = "Move"
    # elif army.action == "Move":
    role = common_selects.select_army_role_by_id(own_realm, army.army_id)

    if army.action == "Move":
        if enough_movement_points(army):
            spent_movement_points(army)
            next_point = list(army.route[0])
            TileNum = (next_point[1] - 1) * game_stats.cur_level_width + next_point[0] - 1

            game_obj.game_map[army.location].army_id = None
            game_obj.game_map[TileNum].army_id = army.army_id
            army.location = int(TileNum)
            army.posxy = list(next_point)
            print("Army " + str(army.army_id) + ": new position - " + str(army.posxy) + "; " + str(army.location))
            # print("Army arrows path is " + str(army.path_arrows))

            del army.route[0]
            del army.path_arrows[0]

            open_tiles("Army", army, TileNum, next_point, own_realm)

            if len(army.route) == 0:
                army.action = "Stand"
                if own_realm.AI_player:
                    if role.army_role in ["Adventure", "Exploration"]:
                        reset_cognition_stage(own_realm)

            else:
                if not enough_movement_points(army):
                    # Not enough movement points for army to make next move
                    army.action = "Stand"
                    if own_realm.AI_player:
                        role.status = "Finished"

        else:
            # Not enough movement points for army to move
            army.action = "Stand"
            if own_realm.AI_player:
                role.status = "Finished"

    elif army.action == "Routing":
        next_point = list(army.route[0])
        TileNum = (next_point[1] - 1) * game_stats.cur_level_width + next_point[0] - 1

        game_obj.game_map[army.location].army_id = None
        game_obj.game_map[TileNum].army_id = army.army_id
        army.location = int(TileNum)
        army.posxy = list(next_point)
        print("Army: new position - " + str(army.posxy) + "; " + str(army.location))

        del army.route[0]

        open_tiles("Army", army, TileNum, next_point, own_realm)

        if len(army.route) == 0:
            army.action = "Stand"
            print("army.action = Stand")

        # Won't be able to move anywhere after routing anyway
        if own_realm.AI_player:
            if role.status != "Finished":
                role.status = "Finished"


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
    # print("Next step - " + str(child) + "; army.posxy - " + str(army.posxy))
    for unit in army.units:
        # print(unit.name + " MP - " + str(unit.movement_points))
        if unit.movement_points - distance < 0:
            enough = False
            continue
    return enough


def engage_army(attacker, defender, terrain, conditions, encounter_type):
    print("")
    print("Engaging army " + str(attacker.army_id) + " vs army " + str(defender.army_id))

    # print("Found defending army " + str(defender.army_id))
    defender.action = "Fighting"

    # print("Found attacking army " + str(attacker.army_id))
    attacker.action = "Fighting"

    if encounter_type == "Attack":
        if enough_movement_points(attacker):
            spent_movement_points(attacker)

            del attacker.route[0]
            del attacker.path_arrows[0]

            if attacker.owner == game_stats.player_power or defender.owner == game_stats.player_power:
                game_stats.attacker_army_id = int(attacker.army_id)
                game_stats.attacker_realm = str(attacker.owner)
                game_stats.defender_army_id = int(defender.army_id)
                game_stats.defender_realm = str(defender.owner)
                game_stats.battle_type = "Battle"
                game_stats.battle_terrain = str(terrain)
                game_stats.battle_conditions = str(conditions)

                # print("game_stats.attacker_army_id - " + str(game_stats.attacker_army_id))
                # print("game_stats.defender_army_id - " + str(game_stats.defender_army_id))

                # print('game_stats.game_board_panel = "begin battle panel"')
                game_stats.game_board_panel = "begin battle panel"

                # Update visuals
                update_gf_game_board.update_regiment_sprites()

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

            else:
                # AI battle
                print("AI field battle")
                game_autobattle.begin_battle(attacker, defender, "Battle", None)

    elif encounter_type == "Lair":
        # for unit in attacker.units:
        #     unit.right_side = True
        #     print("regiment - " + unit.name + " side - " + str(unit.right_side))
        # for unit in defender.units:
        #     unit.right_side = False
        #     print("regiment - " + unit.name + " side - " + str(unit.right_side))
        if attacker.owner == game_stats.player_power:
            print("Position - " + str(attacker.posxy) + ", and location - " + str(attacker.location))
            game_stats.attacker_army_id = int(attacker.army_id)
            game_stats.attacker_realm = str(attacker.owner)
            game_stats.defender_army_id = int(defender.army_id)
            game_stats.defender_realm = str(defender.owner)
            game_stats.battle_type = "special"
            game_stats.battle_terrain = str(terrain)
            game_stats.battle_conditions = str(conditions)

            # print('game_stats.game_board_panel = "begin battle panel"')
            game_stats.game_board_panel = "begin battle panel"

            # Update visuals
            update_gf_game_board.update_regiment_sprites()


def blockade_settlement(attacker, defender, settlement, attacker_realm):
    if enough_movement_points(attacker):
        spent_movement_points(attacker)

        del attacker.route[0]
        del attacker.path_arrows[0]
        attacker.action = "Besieging"
        # print("attacker.route - " + str(attacker.route))
        # print("attacker.path_arrows - " + str(attacker.path_arrows))
        game_stats.attacker_army_id = int(attacker.army_id)
        game_stats.attacker_realm = str(attacker.owner)

        trebuchets_max_quantity = 0
        siege_towers_max_quantity = 0
        battering_rams_max_quantity = 0

        if defender is not None:
            defender.route = []
            defender.path_arrows = []
            defender.action = "Besieged"
            game_stats.defender_army_id = int(defender.army_id)
            game_stats.defender_realm = str(defender.owner)

        game_stats.assault_allowed = True
        gate_exist = False
        walls_exist = False
        for defensive_structure in settlement.defences:
            if defensive_structure.provide_wall:
                game_stats.assault_allowed = False
                for def_object in defensive_structure.def_objects:
                    if def_object.state in ["Broken", "Opened"]:
                        game_stats.assault_allowed = True

                    if def_object.section_type == "Gate":
                        if def_object.state in ["Unbroken"]:
                            gate_exist = True
                    elif def_object.section_type == "Wall":
                        if def_object.state in ["Unbroken"]:
                            walls_exist = True

        # Siege engines data preparation
        for unit in attacker.units:
            alignment = unit_alignment_catalog.alignment_dict[unit.name]
            capacity_list = siege_warfare_catalog.units_siege_dict_by_alignment[alignment][unit.name]
            if walls_exist:
                trebuchets_max_quantity += capacity_list[0]
                siege_towers_max_quantity += capacity_list[1]
            if gate_exist:
                battering_rams_max_quantity += capacity_list[1]

        settlement.siege = game_classes.Blockade(int(attacker.army_id),
                                                 str(attacker.owner),
                                                 3,
                                                 0,
                                                 trebuchets_max_quantity,
                                                 siege_towers_max_quantity,
                                                 battering_rams_max_quantity)

        human_attacker = True
        for realm in game_obj.game_powers:
            if realm.name == attacker.owner:
                if realm.AI_player:
                    human_attacker = False
                break

        if human_attacker:
            game_stats.blockaded_settlement_name = str(settlement.name)
            game_stats.selected_settlement = settlement.city_id
            game_stats.besieged_by_human = True

            game_stats.game_board_panel = "settlement blockade panel"

            # Update visuals
            update_gf_game_board.update_misc_sprites()
            update_gf_game_board.update_regiment_sprites()
            update_gf_game_board.open_settlement_building_sprites()

        else:
            AI_blockade_settlement(settlement, attacker, defender, attacker_realm)


def AI_blockade_settlement(settlement, attacker, defender, attacker_realm):
    print("AI_blockade_settlement()")
    print("the_siege.siege_towers_max_quantity " + str(settlement.siege.siege_towers_max_quantity))
    print("the_siege.trebuchets_max_quantity " + str(settlement.siege.trebuchets_max_quantity))
    print("the_siege.battering_rams_max_quantity " + str(settlement.siege.battering_rams_max_quantity))
    assault_allowed = True
    for defensive_structure in settlement.defences:
        if defensive_structure.provide_wall:
            assault_allowed = False
            for def_object in defensive_structure.def_objects:
                if def_object.state in ["Broken", "Opened"]:
                    assault_allowed = True
                    break

    # Check available siege equipment
    if not assault_allowed:
        if settlement.siege.siege_towers_ready + settlement.siege.battering_rams_ready > 0:
            assault_allowed = True

    continue_blockade = True

    if assault_allowed:
        own_army_sum_rank = 0
        for unit in attacker.units:
            own_army_sum_rank += unit.rank
        print("Siege - own army: len(army.units) - " + str(len(attacker.units)) + "; own_army_sum_rank - "
              + str(own_army_sum_rank))

        # Standard border is 120
        power_border = 120
        # But for human player factions increase to 135, since humans are better at battling
        for realm in game_obj.game_powers:
            if realm.name == defender.owner:
                if not realm.AI_player:
                    power_border = 135
                break

        if power_ranking.rank_ratio_calculation(own_army_sum_rank, defender, power_border):
            print("Assault")
            continue_blockade = False

            game_stats.blockaded_settlement_name = str(settlement.name)
            game_stats.selected_settlement = settlement.city_id
            game_stats.besieged_by_human = False
            game_stats.siege_assault = True

            game_stats.selected_object = ""
            game_stats.game_board_panel = "settlement blockade panel"
            game_stats.details_panel_mode = ""
            game_stats.right_window = ""
            game_stats.settlement_area = ""

            # Update visuals
            update_gf_game_board.update_misc_sprites()
            update_gf_game_board.update_regiment_sprites()
            update_gf_game_board.open_settlement_building_sprites()

    if continue_blockade:
        print("Setting blockade")
        for role in attacker_realm.AI_cogs.army_roles:
            if role.army_id == attacker.army_id:
                role.status = "Finished"
                break

        the_siege = settlement.siege
        gate_exist = False
        walls_exist = False
        for defensive_structure in settlement.defences:
            if defensive_structure.provide_wall:
                game_stats.assault_allowed = False
                for def_object in defensive_structure.def_objects:
                    if def_object.state in ["Broken", "Opened"]:
                        game_stats.assault_allowed = True

                    if def_object.section_type == "Gate":
                        if def_object.state in ["Unbroken"]:
                            gate_exist = True
                    elif def_object.section_type == "Wall":
                        if def_object.state in ["Unbroken"]:
                            walls_exist = True

        if gate_exist:
            if the_siege.battering_rams_ordered + the_siege.battering_rams_ready < 1:
                the_siege.battering_rams_ordered += 1
                the_siege.siege_towers_max_quantity -= 1
                the_siege.construction_orders.append(["Battering ram", 0])

        if walls_exist:
            while (the_siege.trebuchets_ordered + the_siege.trebuchets_ready <
                   the_siege.trebuchets_max_quantity) and \
                    (the_siege.siege_towers_ordered + the_siege.siege_towers_ready <
                     the_siege.siege_towers_max_quantity):

                if the_siege.trebuchets_ordered + the_siege.trebuchets_ready < the_siege.trebuchets_max_quantity:
                    the_siege.trebuchets_ordered += 1
                    the_siege.construction_orders.append(["Trebuchet", 0])

                if the_siege.siege_towers_ordered + the_siege.siege_towers_ready < the_siege.siege_towers_max_quantity:
                    the_siege.siege_towers_ordered += 1
                    the_siege.battering_rams_max_quantity -= 1
                    the_siege.construction_orders.append(["Siege tower", 0])

        if game_stats.game_board_panel == "settlement panel" and settlement.city_id == game_stats.selected_settlement:
            game_stats.assault_allowed = True
            game_stats.blockaded_settlement_name = str(settlement.name)
            game_stats.selected_settlement = settlement.city_id
            game_stats.besieged_by_human = False
            game_stats.siege_assault = False

            game_stats.selected_object = ""
            game_stats.game_board_panel = "settlement blockade panel"
            game_stats.details_panel_mode = ""
            game_stats.right_window = ""
            game_stats.settlement_area = ""

            # Update visuals
            update_gf_game_board.update_misc_sprites()
            update_gf_game_board.update_regiment_sprites()
            update_gf_game_board.open_settlement_building_sprites()

    print("")
    print("the_siege.siege_towers_max_quantity " + str(settlement.siege.siege_towers_max_quantity))
    print("the_siege.trebuchets_max_quantity " + str(settlement.siege.trebuchets_max_quantity))
    print("the_siege.battering_rams_max_quantity " + str(settlement.siege.battering_rams_max_quantity))


def find_siege(army):
    the_settlement = None
    defender_id = None
    for xy in [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]:
        if 0 < army.posxy[0] + xy[0] <= game_stats.cur_level_width:
            if 0 < army.posxy[1] + xy[1] <= game_stats.cur_level_height:
                x = int(army.posxy[0] + xy[0])
                y = int(army.posxy[1] + xy[1])
                TileNum = (y - 1) * game_stats.cur_level_width + x - 1
                TileObj = game_obj.game_map[TileNum]
                if TileObj.lot is not None:
                    if TileObj.lot == "City":
                        for settlement in game_obj.game_cities:
                            if settlement.city_id == TileObj.city_id:
                                if settlement.siege is not None:
                                    if settlement.siege.attacker_id == army.army_id:
                                        the_settlement = settlement
                                        defender_id = TileObj.army_id
                                        break
                if the_settlement is not None:
                    break

    defender_army = None
    if defender_id is not None:
        for army in game_obj.game_armies:
            if army.army_id == defender_id:
                defender_army = army
                break

    return the_settlement, defender_army


def perform_actions():
    for army in game_obj.game_armies:
        if army.action in ["Move", "Ready to move"]:
            movement_action(army)
        elif army.action in ["Routing"]:
            routing_action(army)

    # Next set of checks exist to prevent armies from performing unnecessary animations
    for army in game_obj.game_armies:
        if len(army.route) > 1 and army.owner != "Neutral":
            own_realm = None
            for realm in game_obj.game_powers:
                if realm.name == army.owner:
                    own_realm = realm
                    break

            # print("The rest of the route: " + str(army.route))
            for role in own_realm.AI_cogs.army_roles:
                if role.army_id == army.army_id:
                    next_point = list(army.route[0])
                    TileNum = (next_point[1] - 1) * game_stats.cur_level_width + next_point[0] - 1
                    TileObj = game_obj.game_map[TileNum]
                    if TileObj.army_id is not None:
                        army.action = "Stand"
                        army.route = []
                        army.path_arrows = []
                        role.army_role = "Idle"
                        print("change_position: Path to adventure is blocked by army " + str(TileObj.army_id))
                    break


def exchange_armies(approaching_army, standing_army):
    game_stats.game_board_panel = "army exchange panel"
    game_stats.selected_second_army = int(standing_army.army_id)

    # print("Found defending army " + str(defender.army_id))
    standing_army.action = "Exchanging"

    # print("Found attacking army " + str(attacker.army_id))
    approaching_army.action = "Exchanging"

    if enough_movement_points(approaching_army):
        spent_movement_points(approaching_army)

        del approaching_army.route[0]
        del approaching_army.path_arrows[0]

    # Update visuals
    update_gf_game_board.update_regiment_sprites()


def enough_resources_to_hire(unit_name, settlement):
    # settlement = None
    # for city in game_obj.game_cities:
    #     if city.city_id == game_stats.selected_settlement:
    #         settlement = city
    #         break

    treasury = None
    for realm in game_obj.game_powers:
        if realm.name == settlement.owner:
            treasury = realm.coffers
            break

    # Check available resources to pay a cost of regiment
    enough_resources = True
    alignment = unit_alignment_catalog.alignment_dict[unit_name]
    total_costs = enlist_regiment_prices.units_dict_by_alignment[alignment][unit_name]
    for cost in total_costs:
        no_res = True
        for res in treasury:
            if cost[0] == res[0]:
                no_res = False
                if cost[1] > res[1]:
                    enough_resources = False
                    break
        if no_res:
            enough_resources = False

    # print("enough_resources - " + str(enough_resources))
    if not enough_resources:
        return False
    else:
        return True


def enough_resources_to_hire_hero(hero_for_hire, realm_treasury=None):
    treasury = realm_treasury
    if treasury is None:
        for realm in game_obj.game_powers:
            if realm.name == game_stats.player_power:
                treasury = realm.coffers
                break

    # Check available resources to pay a cost of hero
    enough_resources = True
    for res in treasury:
        if "Florins" == res[0]:
            if 2000 + (hero_for_hire[3] - 1) * 250 > res[1]:
                enough_resources = False
                break

    # print("enough_resources_to_hire_hero: enough_resources - " + str(enough_resources))
    if not enough_resources:
        return False
    else:
        return True


def enough_resources_to_pay(cost_list, realm_treasury=None):
    treasury = realm_treasury
    if treasury is None:
        treasury = common_selects.select_treasury_by_realm_name(game_stats.player_power)

    # Check available resources to pay a cost
    enough_resources = True
    for cost in cost_list:
        no_res = True
        for res in treasury:
            # print(str(cost) + " --- " + str(res))
            if cost[0] == res[0]:
                no_res = False
                if cost[1] > res[1]:
                    enough_resources = False
                    break
        if no_res:
            enough_resources = False
            break

    # print("enough_resources - " + str(enough_resources))
    if not enough_resources:
        return False
    else:
        return True


def realm_payment_for_object(unit_name, settlement):
    # For regiment
    # settlement = None
    # for city in game_obj.game_cities:
    #     if city.city_id == game_stats.selected_settlement:
    #         settlement = city
    #         break

    treasury = common_selects.select_treasury_by_realm_name(settlement.owner)

    # Deduct resources
    alignment = unit_alignment_catalog.alignment_dict[unit_name]
    total_costs = enlist_regiment_prices.units_dict_by_alignment[alignment][unit_name]
    for cost in total_costs:
        for res in treasury:
            depleted = False
            if cost[0] == res[0]:
                # res[1] -= int(cost[1] * game_stats.rw_object.rows * game_stats.rw_object.number * 3)
                res[1] -= int(cost[1])
                if res[1] == 0:
                    depleted = True

            if depleted:
                for delete_res in treasury:
                    if res[0] == delete_res[0]:
                        treasury.remove(delete_res)


def realm_payment(realm_source, cost_list):
    # realm_source - either "settlement" or name of realm
    treasury = None
    if realm_source == "settlement":
        settlement = None
        for city in game_obj.game_cities:
            if city.city_id == game_stats.selected_settlement:
                settlement = city
                break

        for realm in game_obj.game_powers:
            if realm.name == settlement.owner:
                treasury = realm.coffers
                break

    else:  # "player"
        for realm in game_obj.game_powers:
            if realm.name == realm_source:
                treasury = realm.coffers
                break

    # Deduct resources
    for cost in cost_list:
        depleted = False
        for res in treasury:

            if cost[0] == res[0]:
                res[1] -= cost[1]
                if res[1] == 0:
                    depleted = True
                break

        if depleted:
            for delete_res in treasury:
                if cost[0] == delete_res[0]:
                    treasury.remove(delete_res)
                    break

    if realm_source == game_stats.player_power:
        graphics_basic.prepare_resource_ribbon()


def realm_income(realm_source, earnings_list):
    # When realm earn som resources
    # realm_source - either "settlement" or name of realm

    treasury = None
    if realm_source == "settlement":
        settlement = None
        for city in game_obj.game_cities:
            if city.city_id == game_stats.selected_settlement:
                settlement = city
                break

        for realm in game_obj.game_powers:
            if realm.name == settlement.owner:
                treasury = realm.coffers
                break

    else:  # "player"
        for realm in game_obj.game_powers:
            if realm.name == realm_source:
                treasury = realm.coffers
                break

    # Accumulate resources
    print("1) treasury: " + str(treasury))
    for earning in earnings_list:
        no_resource = True
        for res in treasury:
            print("res - " + str(res))

            if earning[0] == res[0]:
                res[1] += earning[1]
                no_resource = False
                break

        if no_resource:
            treasury.append([str(earning[0]), int(earning[1])])
    print("2) treasury: " + str(treasury))

    if realm_source == game_stats.player_power:
        graphics_basic.prepare_resource_ribbon()


def simple_add_resources(reserves, resources_list):
    # print("1) reserves: " + str(reserves))
    for resource in resources_list:
        no_resource = True
        for res in reserves:
            # print("res - " + str(res))

            if res[0] == resource[0]:
                res[1] += int(resource[1])
                no_resource = False
                break

        if no_resource:
            reserves.append([str(resource[0]), int(resource[1])])
    # print("2) reserves: " + str(reserves))


def form_starting_skills_pool(hero_class, mode):
    # Mode: 1) Player - human player; 2) AI - computer player
    if mode == "Player":
        if not starting_skills.locked_first_skill_check[hero_class]:
            game_stats.first_starting_skill = 0
            game_stats.second_starting_skill = 1
        else:
            game_stats.first_starting_skill = None
            game_stats.second_starting_skill = 0

    else:
        if not starting_skills.locked_first_skill_check[hero_class]:
            return 0, 1
        else:
            return None, 0


def hero_next_level(hero, new_exp):
    # After receiving new experience check if hero could advance to next level
    needed_exp = 0
    current_level = int(hero.level)
    for l in range(current_level + 1):
        needed_exp += l * 1000

    if hero.experience + new_exp < needed_exp:
        hero.experience += int(new_exp)
    else:
        # Advance level
        more_exp = int(new_exp)
        while more_exp > 0:
            if hero.experience + more_exp < needed_exp:
                hero.experience += int(more_exp)
                more_exp -= more_exp
            else:
                hero.level += 1
                hero.new_attribute_points += 1
                hero.new_skill_points += 1
                exp = int(needed_exp) - int(hero.experience)
                more_exp -= int(exp)
                hero.experience += int(exp)

                current_level = int(hero.level)
                needed_exp = 0
                for l in range(current_level + 1):
                    needed_exp += l * 1000

    print("Hero's level - " + str(hero.level) + ", experience - " + str(hero.experience))
    print("hero.archetype - " + str(hero.archetype))
    if hero.archetype is not None:
        AI_learn_skills.manage_skill_points(hero)
        AI_learn_attributes.manage_attributes_points(hero)


def learn_new_abilities(skill_name, hero):
    if skill_name in study_abilities_catalog.abilities_cat:
        for ability in study_abilities_catalog.abilities_cat[skill_name]:
            if ability not in hero.abilities:
                hero.abilities.append(ability)


def increase_level_for_new_heroes(settlement):
    new_experience = 0
    bonus_level = 0
    for local_effect in settlement.local_effects:
        if local_effect.ef_type == "New heroes":
            for effect in local_effect.content:
                # print("effect.application = " + str(effect.application))
                if effect.application == "Level":
                    if effect.operator == "Addition":
                        bonus_level += effect.bonus

    if bonus_level > 0:
        for l in range(1 + bonus_level):
            new_experience += l * 1000

    return new_experience, bonus_level


def gather_province_records():
    game_stats.province_records = []
    game_stats.allocated_gains_records = []
    game_stats.allocated_sold_records = []
    game_stats.allocated_bought_records = []
    settlement = common_selects.select_settlement_by_id(game_stats.selected_settlement)

    game_stats.province_records.append(["Turnover tax", int(settlement.records_turnover_tax)])
    for res in settlement.records_local_fees:
        game_stats.province_records.append([str(res[0]), int(res[1])])

    for pops in settlement.residency:
        # game_stats.allocated_gains_records
        # print(pops.name + " - records_gained: " + str(pops.records_gained))
        for res_rec in pops.records_gained:
            # print(pops.name + ": " + str(res_rec))
            add_new_res_rec = True
            for res_all in game_stats.allocated_gains_records:
                if res_all[0] == res_rec[0]:
                    res_all[1] += int(res_rec[1])
                    add_new_res_rec = False

            if add_new_res_rec:
                game_stats.allocated_gains_records.append([res_rec[0], res_rec[1]])

        # game_stats.allocated_sold_records
        for res_rec in pops.records_sold:
            add_new_res_rec = True
            for res_all in game_stats.allocated_sold_records:
                if res_all[0] == res_rec[0]:
                    res_all[1] += int(res_rec[1])
                    add_new_res_rec = False

            if add_new_res_rec:
                game_stats.allocated_sold_records.append([res_rec[0], res_rec[1]])

        # game_stats.allocated_bought_records
        for res_rec in pops.records_bought:
            add_new_res_rec = True
            for res_all in game_stats.allocated_bought_records:
                if res_all[0] == res_rec[0]:
                    res_all[1] += int(res_rec[1])
                    add_new_res_rec = False

            if add_new_res_rec:
                game_stats.allocated_bought_records.append([res_rec[0], res_rec[1]])

    for TileNum in settlement.property:
        TileObj = game_obj.game_map[TileNum]
        for pops in TileObj.lot.residency:
            # game_stats.allocated_gains_records
            for res_rec in pops.records_gained:
                add_new_res_rec = True
                for res_all in game_stats.allocated_gains_records:
                    if res_all[0] == res_rec[0]:
                        res_all[1] += int(res_rec[1])
                        add_new_res_rec = False

                if add_new_res_rec:
                    game_stats.allocated_gains_records.append([res_rec[0], res_rec[1]])

            # game_stats.allocated_sold_records
            for res_rec in pops.records_sold:
                add_new_res_rec = True
                for res_all in game_stats.allocated_sold_records:
                    if res_all[0] == res_rec[0]:
                        res_all[1] += int(res_rec[1])
                        add_new_res_rec = False

                if add_new_res_rec:
                    game_stats.allocated_sold_records.append([res_rec[0], res_rec[1]])

            # game_stats.allocated_bought_records
            for res_rec in pops.records_bought:
                add_new_res_rec = True
                for res_all in game_stats.allocated_bought_records:
                    if res_all[0] == res_rec[0]:
                        res_all[1] += int(res_rec[1])
                        add_new_res_rec = False

                if add_new_res_rec:
                    game_stats.allocated_bought_records.append([res_rec[0], res_rec[1]])

    # print("allocated_gains_records - " + str(game_stats.allocated_gains_records))


def snapshot_local_market():
    print("snapshot_local_market")
    game_stats.allocated_sold_records = []
    game_stats.allocated_requested_goods_records = []
    game_stats.allocated_bought_records = []
    settlement = common_selects.select_settlement_by_id(game_stats.selected_settlement)

    for pops in settlement.residency:
        for res_rec in pops.records_sold:
            # game_stats.allocated_sold_records
            add_new_res_rec = True
            for res_all in game_stats.allocated_sold_records:
                if res_all[0] == res_rec[0]:
                    res_all[1] += int(res_rec[1])
                    add_new_res_rec = False

            if add_new_res_rec:
                game_stats.allocated_sold_records.append([res_rec[0], res_rec[1]])

        # game_stats.allocated_requested_goods_records
        # print(pops.name + " test")
        basket = buy_resources.pops_to_facility_cat[pops.name]["Settlement"](pops, settlement, False)
        # print(basket)
        for res_rec in basket:
            add_new_res_rec = True
            # print(str(res_rec))
            for res_all in game_stats.allocated_requested_goods_records:
                if res_all[0] == res_rec[0]:
                    res_all[1] += int(res_rec[1])
                    add_new_res_rec = False

            if add_new_res_rec:
                game_stats.allocated_requested_goods_records.append([res_rec[0], res_rec[1]])

        # game_stats.allocated_bought_records
        for res_rec in pops.records_bought:
            add_new_res_rec = True
            for res_all in game_stats.allocated_bought_records:
                if res_all[0] == res_rec[0]:
                    res_all[1] += int(res_rec[1])
                    add_new_res_rec = False

            if add_new_res_rec:
                game_stats.allocated_bought_records.append([res_rec[0], res_rec[1]])

    for TileNum in settlement.property:
        TileObj = game_obj.game_map[TileNum]
        for pops in TileObj.lot.residency:
            for res_rec in pops.records_sold:
                # game_stats.allocated_sold_records
                add_new_res_rec = True
                for res_all in game_stats.allocated_sold_records:
                    if res_all[0] == res_rec[0]:
                        res_all[1] += int(res_rec[1])
                        add_new_res_rec = False

                if add_new_res_rec:
                    game_stats.allocated_sold_records.append([res_rec[0], res_rec[1]])

            # game_stats.allocated_requested_goods_records
            basket = buy_resources.pops_to_facility_cat[pops.name][TileObj.lot.obj_name](pops, settlement, False)
            for res_rec in basket:
                add_new_res_rec = True
                for res_all in game_stats.allocated_requested_goods_records:
                    if res_all[0] == res_rec[0]:
                        res_all[1] += int(res_rec[1])
                        add_new_res_rec = False

                if add_new_res_rec:
                    game_stats.allocated_requested_goods_records.append([res_rec[0], res_rec[1]])

            # game_stats.allocated_bought_records
            for res_rec in pops.records_bought:
                add_new_res_rec = True
                for res_all in game_stats.allocated_bought_records:
                    if res_all[0] == res_rec[0]:
                        res_all[1] += int(res_rec[1])
                        add_new_res_rec = False

                if add_new_res_rec:
                    game_stats.allocated_bought_records.append([res_rec[0], res_rec[1]])


def base_update_control():
    # Update control every turn
    # print("base_update_control")
    for settlement in game_obj.game_cities:
        settlement.control = []
        for local_effect in settlement.local_effects:
            if local_effect.ef_type == "Control":
                # print("local_effect.name - " + local_effect.name + ", local_effect.ef_type - " + local_effect.ef_type)
                for control_eff in local_effect.content:
                    add_new_culture = True
                    if len(settlement.control) > 0:
                        for culture in settlement.control:
                            if culture[0] == control_eff.realm_type:
                                add_new_culture = False
                                if control_eff.operator == "Addition":
                                    culture[1] += int(control_eff.bonus)
                                break

                    if add_new_culture:
                        settlement.control.append([str(control_eff.realm_type), int(control_eff.bonus)])

        for plot in settlement.buildings:
            if plot.structure is not None and plot.status == "Built":
                if len(plot.structure.provided_effects) > 0:
                    for effect in plot.structure.provided_effects:
                        # print(effect.name)
                        if effect.ef_type == "Control":
                            for control_eff in effect.content:
                                add_new_culture = True
                                if len(settlement.control) > 0:
                                    for culture in settlement.control:
                                        if culture[0] == control_eff.realm_type:
                                            add_new_culture = False
                                            if control_eff.operator == "Addition":
                                                culture[1] += int(control_eff.bonus)
                                            break

                                if add_new_culture:
                                    settlement.control.append([str(control_eff.realm_type), int(control_eff.bonus)])


def base_update_settlement_effects():
    # Check duration of effects in settlement
    # print("base_update_settlement_effects()")
    for settlement in game_obj.game_cities:
        index_list = []
        num = 0
        for local_effect in settlement.local_effects:
            if local_effect.duration is not True:
                local_effect.duration -= 1
                if local_effect.duration == 0:
                    # Remove this effect
                    index_list.append(int(num))

                    for effect in local_effect.content:
                        # print("effect.application = " + str(effect.application))
                        if effect.application == "Loyalty":
                            for faction in settlement.factions:
                                # print("faction.name = " + str(faction.name))
                                if faction.name == effect.faction:
                                    # print("effect.operator = " + str(effect.operator))
                                    if effect.operator == "Subtraction":
                                        faction.loyalty += int(effect.bonus)
                                    elif effect.operator == "Addition":
                                        faction.loyalty -= int(effect.bonus)
                                    break

            num += 1

        if len(index_list) > 0:
            # Removing effects
            index_list.reverse()
            for ind in index_list:
                del settlement.local_effects[ind]


def create_new_quest_message(settlement):
    quests_conditions_choice = {"Knight Lords": knight_lords_cond.check_conditions}

    if settlement.owner != "Neutral":
        quest_message_name = quests_conditions_choice[settlement.alignment](settlement)
        print(settlement.name + ": new quest message - " + str(quest_message_name))

        for realm in game_obj.game_powers:
            if realm.name == settlement.owner:
                realm.quests_messages.append(game_classes.Quest_Message(str(quest_message_name),
                                                                        int(settlement.location),
                                                                        str(settlement.name),
                                                                        "Dilemma",
                                                                        str(settlement.alignment),
                                                                        None,
                                                                        None,
                                                                        None))

                if game_stats.player_power == realm.name:
                    game_stats.new_tasks = True
                break


def update_new_tasks_status(settlement):
    realm = common_selects.select_realm_by_name(settlement.owner)
    new_tasks_exist = False
    for quest in realm.quests_messages:
        if quest.message_type == "Dilemma":
            game_stats.new_tasks = True
            break

    if realm.diplomatic_messages:
        game_stats.new_tasks = True

    if new_tasks_exist:
        game_stats.new_tasks = True
    else:
        game_stats.new_tasks = False


def change_side_direction(army):
    # The location of the army relative to the target tile
    # print("start_pos - " + str(army.posxy) + ", finish_pos - " + str(army.route[0]))
    direction = simple_direction(army.posxy, army.route[0])

    if direction in ["NW", "W", "SW"]:
        if not army.right_side:
            army.right_side = True

    elif direction in ["NE", "E", "SE"]:
        if army.right_side:
            army.right_side = False


def simple_direction(start_pos, finish_pos):
    relative_position = None
    if start_pos[0] < finish_pos[0]:
        if start_pos[1] < finish_pos[1]:
            relative_position = "NW"
        elif start_pos[1] == finish_pos[1]:
            relative_position = "W"
        elif start_pos[1] > finish_pos[1]:
            relative_position = "SW"

    elif start_pos[0] == finish_pos[0]:
        if start_pos[1] < finish_pos[1]:
            relative_position = "N"
        elif start_pos[1] > finish_pos[1]:
            relative_position = "S"

    elif start_pos[0] > finish_pos[0]:
        if start_pos[1] < finish_pos[1]:
            relative_position = "NE"
        elif start_pos[1] == finish_pos[1]:
            relative_position = "E"
        elif start_pos[1] > finish_pos[1]:
            relative_position = "SE"

    return relative_position


def move_out_army_from_settlement(army):
    the_realm = common_selects.select_realm_by_name(army.owner)

    enemy_realms = []
    for opponent in the_realm.relations.at_war:
        enemy_realms.append(str(opponent[2]))

    allowed_city_id = []
    for settlement in game_obj.game_cities:
        if settlement.owner == army.owner:
            allowed_city_id.append(settlement.city_id)
        elif settlement.owner in enemy_realms:
            allowed_city_id.append(settlement.city_id)

    suitable_tiles = []
    rejected_tiles = []
    radius = 1

    rejected_tiles.append([int(army.posxy[0]), int(army.posxy[1])])

    new_tiles = algo_circle_range.within_circle_range(army.posxy, radius)
    search = True

    while search:
        if not new_tiles:
            if suitable_tiles:
                search = False
            else:
                radius += 1
                new_tiles = algo_circle_range.within_circle_range(army.posxy, radius)

        if new_tiles:
            TileNum = (new_tiles[0][1] - 1) * game_stats.cur_level_width + new_tiles[0][0] - 1
            TileObj = game_obj.game_map[TileNum]

            if new_tiles[0] in suitable_tiles:
                del new_tiles[0]
                continue
            elif new_tiles[0] in rejected_tiles:
                del new_tiles[0]
                continue
            elif TileObj.army_id:
                rejected_tiles.append(new_tiles.pop(0))
                continue
            elif TileObj.lot:
                rejected_tiles.append(new_tiles.pop(0))
                continue
            elif not TileObj.travel:
                rejected_tiles.append(new_tiles.pop(0))
                continue
            elif TileObj.city_id is not None:
                if TileObj.city_id not in allowed_city_id:
                    rejected_tiles.append(new_tiles.pop(0))
                    continue
                else:
                    suitable_tiles.append(new_tiles.pop(0))
                    continue
            else:
                suitable_tiles.append(new_tiles.pop(0))

    print("radius - " + str(radius))
    print("suitable_tiles - " + str(suitable_tiles))
    destination = random.choice(suitable_tiles)

    TileNum = (destination[1] - 1) * game_stats.cur_level_width + destination[0] - 1

    game_obj.game_map[army.location].army_id = None
    game_obj.game_map[TileNum].army_id = army.army_id
    army.location = int(TileNum)
    army.posxy = list(destination)
    print("Army: moved to position - " + str(army.posxy) + "; " + str(army.location))

    army.route = []
    army.path_arrows = []

    open_tiles("Army", army, TileNum, destination, the_realm)

    army.action = "Stand"


def finish_settlement_blockade(settlement, attacker, defender):
    attacker.action = "Stand"
    defender.action = "Stand"
    settlement.siege = None


def military_upkeep():
    for realm in game_obj.game_powers:
        total_upkeep = []
        for army in game_obj.game_armies:
            if army.owner == realm.name:
                for unit in army.units:
                    for upkeep in unit.cost:
                        add_new_resource = True
                        for resource in total_upkeep:
                            if resource[0] == upkeep[0]:
                                add_new_resource = False
                                resource[1] += int(upkeep[1] * len(unit.crew))
                                break
                        if add_new_resource:
                            total_upkeep.append([str(upkeep[0]), int(upkeep[1] * len(unit.crew))])

        # Simple way
        upkeep_sum = 0
        reserves = 0
        deficit = 0
        for upkeep_cost in total_upkeep:
            upkeep_sum += upkeep_cost[1]

        for resource in realm.coffers:
            reserves += resource[1]

        print(str(reserves) + " realm.coffers: " + str(realm.coffers))
        print(str(upkeep_sum) + " total_upkeep: " + str(total_upkeep))

        # Deduct
        for upkeep_cost in total_upkeep:
            no_res = True
            for resource in realm.coffers:
                if resource[0] == upkeep_cost[0]:
                    no_res = False
                    resource[1] -= upkeep_cost[1]
                    if resource[1] < 0:
                        deficit += -1 * int(resource[1])
                    break
            if no_res:
                deficit += int(upkeep_cost[1])

        print("deficit " + str(deficit))
        upkeep_ratio = 1.0
        if upkeep_sum != 0 and deficit != 0:
            upkeep_ratio = float((upkeep_sum - deficit) / upkeep_sum)
        print("upkeep_ratio " + str(upkeep_ratio))

        # Cleaning
        num = len(realm.coffers) - 1
        while num >= 0:
            if realm.coffers[num][1] <= 0:
                del realm.coffers[num]
            num -= 1

        if upkeep_ratio < 1.0:
            disband_chance = int(math.floor((1 - upkeep_ratio) * 100))
            for army in game_obj.game_armies:
                if army.owner == realm.name:
                    for unit in army.units:
                        disband_creatures = 0
                        for creature in unit.crew:
                            if random.randint(1, 100) <= disband_chance:
                                disband_creatures += 1

                        if disband_creatures > 0:
                            del unit.crew[0:disband_creatures]

                        num = len(army.units) - 1
                        while num >= 0:
                            if len(army.units[num].crew) == 0:
                                del army.units[num]
                            num -= 1

            # TODO: remove empty army


def remove_army(id_list):
    print("remove_army()")
    print("1. id_list: " + str(id_list))
    while len(id_list) > 0:
        for army in game_obj.game_armies:
            if army.army_id == id_list[0]:

                if army.owner != "Neutral":
                    for realm in game_obj.game_powers:
                        if realm.AI_player:
                            if realm.name == army.owner:
                                for role in realm.AI_cogs.army_roles:
                                    if role.army_id == army.army_id:
                                        realm.AI_cogs.army_roles.remove(role)
                                        break
                                break
                game_obj.game_armies.remove(army)
                del id_list[0]
                break

    # print("2. id_list: " + str(id_list))


def capture_settlement(settlement, attacker_realm, winner_alive, winner):
    print("settlement_captured")
    settlement.siege = None
    if settlement.owner == "Neutral":
        settlement.owner = str(winner.owner)
    elif settlement.owner == attacker_realm:
        settlement.military_occupation = None
    else:
        for realm in game_obj.game_powers:
            if realm.name == attacker_realm:
                settlement.military_occupation = [str(realm.f_color), str(realm.s_color), str(realm.name)]
                break

    print("military_occupation - " + str(settlement.military_occupation))

    if winner_alive:
        # Move victorious army into captured settlement
        game_obj.game_map[winner.location].army_id = None
        game_obj.game_map[settlement.location].army_id = int(winner.army_id)
        winner.location = int(settlement.location)
        winner.posxy = list(settlement.posxy)


def reset_cognition_stage(realm):
    if realm.AI_player:
        if realm.AI_cogs.cognition_stage == "Finished turn":
            realm.AI_cogs.cognition_stage = "Manage armies"

