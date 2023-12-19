## Among Myth and Wonder

import math

from Resources import game_obj
from Resources import game_stats
from Resources import game_basic
from Resources import diplomacy_classes

from Surfaces import sf_game_board


def prepare_summary():
    war_status = False
    for war in game_obj.game_wars:
        if war.initiator == game_stats.realm_inspection.name \
                or war.respondent == game_stats.realm_inspection.name:
            if war.initiator == game_stats.contact_inspection.name \
                    or war.respondent == game_stats.contact_inspection.name:
                war_status = True
                break
    game_stats.dip_summary = diplomacy_classes.Relations_Summary(war_status)


def prepare_war_summary():
    the_war = None
    for war in game_obj.game_wars:
        if war.initiator == game_stats.realm_inspection.name or war.respondent == game_stats.realm_inspection.name:
            if war.initiator == game_stats.contact_inspection.name \
                    or war.respondent == game_stats.contact_inspection.name:
                the_war = war
                break

    game_stats.war_summary = create_war_summary(game_stats.realm_inspection.name,
                                                game_stats.contact_inspection.name,
                                                the_war)


def create_war_summary(own_realm, enemy, war):
    summary_war_goals = []
    own_realm_war_enthusiasm = 0
    opponent_war_enthusiasm = 0
    own_realm_battle_victories = 0
    opponent_battle_victories = 0
    own_realm_captured_provinces = 0
    opponent_captured_provinces = 0
    list_of_objective_settlements = []
    is_initiator = True

    opponent_name = None
    opponent_f_color = None
    opponent_s_color = None

    if war.initiator == own_realm:
        own_realm_battle_victories = int(war.initiator_battle_victories)
        opponent_battle_victories = int(war.respondent_battle_victories)
        opponent_name = str(war.respondent)
        opponent_f_color = str(war.respondent_f_color)
        opponent_s_color = str(war.respondent_s_color)
    else:
        own_realm_battle_victories = int(war.respondent_battle_victories)
        opponent_battle_victories = int(war.initiator_battle_victories)
        opponent_name = str(war.initiator)
        opponent_f_color = str(war.initiator_f_color)
        opponent_s_color = str(war.initiator_s_color)
        is_initiator = False

    print("War goals: " + str(war.war_goals))
    for goal in war.war_goals:
        if goal[2] == "Conquest":
            list_of_objective_settlements.append(int(goal[1]))
            print("list_of_objective_settlements: " + str(list_of_objective_settlements))
            holder = None
            f_color = None
            s_color = None
            for settlement in game_obj.game_cities:
                if settlement.city_id == goal[1]:
                    if settlement.military_occupation:
                        if settlement.military_occupation[2] in [war.initiator, war.respondent]:
                            holder = str(settlement.military_occupation[2])
                            if settlement.military_occupation[2] == own_realm:
                                own_realm_war_enthusiasm += 20
                            else:
                                opponent_war_enthusiasm += 20
                    else:
                        holder = str(settlement.owner)
                        if settlement.owner == own_realm:
                            own_realm_war_enthusiasm += 20
                        else:
                            opponent_war_enthusiasm += 20
                    break
            if holder is not None:
                for realm in game_obj.game_powers:
                    if realm.name == holder:
                        f_color = str(realm.f_color)
                        s_color = str(realm.s_color)
                        break
            summary_war_goals.append([str(goal[2]),
                                      str(war_goal_icon_dict[goal[2]]),
                                      str(holder),
                                      str(f_color),
                                      str(s_color),
                                      int(war_goal_war_enthusiasm_dict[goal[2]]),
                                      str(goal[0])])

        elif goal[2] == "Tribute":
            # Battle victories
            battle_success_rate = 0.0
            print("initiator_battle_victories " + str(war.initiator_battle_victories))
            print("respondent_battle_victories " + str(war.respondent_battle_victories))
            if war.initiator_battle_victories + war.respondent_battle_victories > 0:
                battle_success_rate = war.initiator_battle_victories / \
                                      (war.initiator_battle_victories +
                                       war.respondent_battle_victories)

            print("battle_success_rate " + str(battle_success_rate))

            winner = str(war.respondent)
            f_color = str(war.respondent_f_color)
            s_color = str(war.respondent_s_color)
            if battle_success_rate >= tribute_success_rate_dict[goal[0]]:
                winner = str(war.initiator)
                f_color = str(war.initiator_f_color)
                s_color = str(war.initiator_s_color)
                if war.initiator == own_realm:
                    own_realm_war_enthusiasm += int(war_goal_war_enthusiasm_dict[goal[0]])
                else:
                    opponent_war_enthusiasm += int(war_goal_war_enthusiasm_dict[goal[0]])

            else:
                if war.respondent == own_realm:
                    own_realm_war_enthusiasm += int(war_goal_war_enthusiasm_dict[goal[0]])
                else:
                    opponent_war_enthusiasm += int(war_goal_war_enthusiasm_dict[goal[0]])

            summary_war_goals.append([str(goal[2]),
                                      str(war_goal_icon_dict[goal[2]]),
                                      winner,
                                      f_color,
                                      s_color,
                                      int(war_goal_war_enthusiasm_dict[goal[0]]),
                                      str(goal[0])])

    # print("1. own_realm_war_enthusiasm " + str(own_realm_war_enthusiasm))
    if war.initiator_battle_victories > war.respondent_battle_victories:
        if war.initiator == own_realm:
            own_realm_war_enthusiasm += int(war.initiator_battle_victories -
                                            war.respondent_battle_victories)
        else:
            opponent_war_enthusiasm += int(war.initiator_battle_victories -
                                           war.respondent_battle_victories)
    else:
        if war.respondent == own_realm:
            own_realm_war_enthusiasm += int(war.initiator_battle_victories -
                                            war.respondent_battle_victories)
        else:
            opponent_war_enthusiasm += int(war.initiator_battle_victories -
                                           war.respondent_battle_victories)

    initiator_settlements = 0
    respondent_settlements = 0
    captured_initiator_settlements = 0
    captured_respondent_settlements = 0
    for settlement in game_obj.game_cities:
        if settlement.city_id not in list_of_objective_settlements:
            if settlement.military_occupation:
                print(settlement.name + " - " + str(settlement.city_id) + " - "
                      + settlement.military_occupation[2])
                if settlement.military_occupation[2] in [war.initiator, war.respondent]:
                    if settlement.military_occupation[2] == own_realm:
                        own_realm_captured_provinces += 1
                        own_realm_war_enthusiasm += 10
                    else:
                        opponent_captured_provinces += 1
                        opponent_war_enthusiasm += 10

        if settlement.owner == war.initiator:
            initiator_settlements += 1
            if settlement.military_occupation:
                if settlement.military_occupation[2] == war.respondent:
                    captured_initiator_settlements += 1
        elif settlement.owner == war.respondent:
            respondent_settlements += 1
            if settlement.military_occupation:
                if settlement.military_occupation[2] == war.initiator:
                    captured_respondent_settlements += 1

    # print("2. own_realm_war_enthusiasm " + str(own_realm_war_enthusiasm))

    if initiator_settlements == captured_initiator_settlements:
        # All war initiator settlements have been captured
        # Enemy should receive bonus WE equal to the half of max WE in order to speed up war completion
        if war.initiator == own_realm:
            opponent_war_enthusiasm += int(math.ceil(war.max_war_enthusiasm / 2))
        else:
            own_realm_war_enthusiasm += int(math.ceil(war.max_war_enthusiasm / 2))

    # print("3. own_realm_war_enthusiasm " + str(own_realm_war_enthusiasm))

    if respondent_settlements == captured_respondent_settlements:
        # All war initiator settlements have been captured
        # Enemy should receive bonus WE equal to the half of max WE in order to speed up war completion
        if war.respondent == own_realm:
            opponent_war_enthusiasm += int(math.ceil(war.max_war_enthusiasm / 2))
        else:
            own_realm_war_enthusiasm += int(math.ceil(war.max_war_enthusiasm / 2))

    # print("4. own_realm_war_enthusiasm " + str(own_realm_war_enthusiasm))

    return diplomacy_classes.War_Summary(list(summary_war_goals),
                                         int(war.max_war_enthusiasm),
                                         int(own_realm_war_enthusiasm),
                                         int(opponent_war_enthusiasm),
                                         int(own_realm_battle_victories),
                                         int(opponent_battle_victories),
                                         int(own_realm_captured_provinces),
                                         int(opponent_captured_provinces),
                                         int(war.war_duration),
                                         bool(is_initiator))


def prepare_casus_bellis():
    ## Conquest casus belli
    # War goal is to conquer a province by taking its settlement
    permissible_settlements = []
    for settlement in game_obj.game_cities:
        if settlement.owner == game_stats.contact_inspection.name:
            if settlement.posxy in game_stats.realm_inspection.known_map:
                permissible_settlements.append(int(settlement.city_id))

    if len(permissible_settlements) > 0:
        game_stats.casus_bellis.append("Conquest")

    # War goal is to collect tribute
    game_stats.casus_bellis.append("Tribute")


def add_war_goal(cb_item):
    print("add_war_goal - " + str(cb_item))
    num = 0
    found = False
    for goal in game_stats.war_goals:
        if goal[2] == cb_item[2]:
            if cb_item[2] == "Tribute":
                game_stats.cb_details.append(game_stats.war_goals.pop(num))
            game_stats.war_goals.insert(num, cb_item)
            found = True
            break
        num += 1

    if not found:
        game_stats.war_goals.append(cb_item)


def remove_war_goal(wg_num):
    if game_stats.cb_details:
        if game_stats.war_goals[wg_num][2] == game_stats.cb_details[0][2]:
            game_stats.cb_details.append(game_stats.war_goals.pop(wg_num))
        else:
            del game_stats.war_goals[wg_num]
    else:
        del game_stats.war_goals[wg_num]


def cb_details_conquest():
    avoid_list = []
    if game_stats.war_goals:
        for goal in game_stats.war_goals:
            if goal[2] == "Conquest":
                avoid_list.append(str(goal[0]))

    for settlement in game_obj.game_cities:
        if settlement.owner == game_stats.contact_inspection.name:
            if settlement.posxy in game_stats.realm_inspection.known_map:
                if settlement.name not in avoid_list:
                    game_stats.cb_details.append([str(settlement.name), int(settlement.city_id), "Conquest"])


def cb_details_tribute():
    avoid = None
    if game_stats.war_goals:
        for goal in game_stats.war_goals:
            if goal[2] == "Tribute":
                avoid = str(goal[0])

    if avoid != "Low tribute":
        # Low tribute - 10%
        game_stats.cb_details.append(["Low tribute", int(0.1), "Tribute"])
    if avoid != "Moderate tribute":
        # Moderate tribute - 25%
        game_stats.cb_details.append(["Moderate tribute", int(0.25), "Tribute"])
    if avoid != "Severe tribute":
        # Severe tribute - 50%
        game_stats.cb_details.append(["Severe tribute", int(0.50), "Tribute"])
    if avoid != "Harsh tribute":
        # Harsh tribute - 80%
        game_stats.cb_details.append(["Harsh tribute", int(0.80), "Tribute"])


def declare_war():
    max_we = 10  # Base 10 points of war enthusiasm for all wars

    for goal in game_stats.war_goals:
        if goal[2] == "Conquest":
            max_we += 30

        elif goal[2] == "Tribute":
            max_we += 10  # For Tribute war goal
            if goal[0] == "Low tribute":
                max_we += 10
            elif goal[0] == "Moderate tribute":
                max_we += 15
            elif goal[0] == "Severe tribute":
                max_we += 20
            elif goal[0] == "Harsh tribute":
                max_we += 30

    game_obj.game_wars.append(diplomacy_classes.War(str(game_stats.realm_inspection.name),
                                                    str(game_stats.realm_inspection.f_color),
                                                    str(game_stats.realm_inspection.s_color),
                                                    str(game_stats.contact_inspection.name),
                                                    str(game_stats.contact_inspection.f_color),
                                                    str(game_stats.contact_inspection.s_color),
                                                    list(game_stats.war_goals),
                                                    int(max_we)))

    game_stats.ongoing_wars.append([str(game_stats.contact_inspection.f_color),
                                    str(game_stats.contact_inspection.s_color),
                                    str(game_stats.contact_inspection.name)])

    # for war in game_obj.game_wars:
    #     if war.initiator == game_stats.realm_inspection.name:
    #         if war.respondent == game_stats.contact_inspection.name:
    #             game_stats.ongoing_wars.append([str(war.respondent_f_color),
    #                                             str(war.respondent_s_color),
    #                                             str(war.respondent)])
    #             break

    # print("declare_war_but - " + str(game_stats.contact_inspection.f_color) +
    #       " " + str(game_stats.contact_inspection.s_color) +
    #       " " + str(game_stats.contact_inspection.name))
    game_stats.realm_inspection.relations.at_war.append([str(game_stats.contact_inspection.f_color),
                                                         str(game_stats.contact_inspection.s_color),
                                                         str(game_stats.contact_inspection.name)])

    # print("declare_war_but - " + str(game_stats.realm_inspection.f_color) +
    #       " " + str(game_stats.realm_inspection.s_color) +
    #       " " + str(game_stats.realm_inspection.name))
    game_stats.contact_inspection.relations.at_war.append([str(game_stats.realm_inspection.f_color),
                                                           str(game_stats.realm_inspection.s_color),
                                                           str(game_stats.realm_inspection.name)])

    # for realm in game_stats.realm_inspection.relations.at_war:
    #     print("At war with " + str(realm[2]) + " " + str(realm[0]) + " " + str(realm[1]))

    sf_game_board.return_to_diplomatic_actions_area_but()


def prepare_peace_demands_summary():
    the_war = None
    the_player = game_stats.realm_inspection.name
    the_opponent = game_stats.contact_inspection.name
    for war in game_obj.game_wars:
        if war.initiator == game_stats.realm_inspection.name \
                or war.respondent == game_stats.realm_inspection.name:
            if war.initiator == game_stats.contact_inspection.name \
                    or war.respondent == game_stats.contact_inspection.name:
                the_war = war
                break

    game_stats.peace_demands = []
    game_stats.demand_details = []

    # Prepare conditions for surrender request
    if game_stats.make_demands:
        # print("Make demands")
        for settlement in game_obj.game_cities:
            if settlement.owner == the_opponent:
                # print(settlement.name)
                if settlement.posxy in game_stats.realm_inspection.known_map:
                    # print("settlement.posxy in")
                    if settlement.military_occupation:
                        # print(settlement.name + " is occupied")
                        # print(str(settlement.military_occupation))
                        if settlement.military_occupation[2] == the_player:
                            # print("Take territory")
                            game_stats.peace_demands.append("Take territory")
                            break

        # Battle victories
        battle_success_rate = 0.0
        print("initiator_battle_victories " + str(the_war.initiator_battle_victories))
        print("respondent_battle_victories " + str(the_war.respondent_battle_victories))
        if the_war.initiator_battle_victories + the_war.respondent_battle_victories > 0:
            if the_war.initiator == game_stats.realm_inspection.name:
                battle_success_rate = the_war.initiator_battle_victories / \
                    (the_war.initiator_battle_victories + the_war.respondent_battle_victories)
            else:
                battle_success_rate = the_war.respondent_battle_victories / \
                    (the_war.initiator_battle_victories + the_war.respondent_battle_victories)

        print("battle_success_rate " + str(battle_success_rate))

        if battle_success_rate >= 0.5:
            game_stats.peace_demands.append("Impose tribute")

    # Prepare conditions for capitulation
    else:
        for settlement in game_obj.game_cities:
            if settlement.owner == the_player:
                if settlement.posxy in game_stats.realm_inspection.known_map:
                    if settlement.military_occupation:
                        if settlement.military_occupation[2] == the_opponent:
                            game_stats.peace_demands.append("Take territory")
                            break

        # Battle victories
        battle_success_rate = 0.0
        print("initiator_battle_victories " + str(the_war.initiator_battle_victories))
        print("respondent_battle_victories " + str(the_war.respondent_battle_victories))
        if the_war.initiator_battle_victories + the_war.respondent_battle_victories > 0:
            if the_war.initiator == game_stats.realm_inspection.name:
                battle_success_rate = the_war.initiator_battle_victories / \
                                      (the_war.initiator_battle_victories + the_war.respondent_battle_victories)
            else:
                battle_success_rate = the_war.respondent_battle_victories / \
                                      (the_war.initiator_battle_victories + the_war.respondent_battle_victories)

        print("battle_success_rate " + str(battle_success_rate))

        if the_war.initiator_battle_victories + the_war.respondent_battle_victories > 0:
            if battle_success_rate < 0.5:
                game_stats.peace_demands.append("Impose tribute")

        print("Make concessions - peace_demands: " + str(game_stats.peace_demands))

    # Generate white peace text
    game_stats.will_accept_white_peace = False
    opponent = game_stats.contact_inspection.leader
    game_stats.peace_offer_text = []
    score = 0
    summary = game_stats.war_summary

    no_messages = True
    for message in game_stats.realm_inspection.diplomatic_messages:
        if message.dm_from == game_stats.contact_inspection.name:
            if message.subject in ["White peace", "Surrender request", "Capitulation offer"]:
                no_messages = False

    for message in game_stats.contact_inspection.diplomatic_messages:
        if message.dm_from == game_stats.realm_inspection.name:
            if message.subject in ["White peace", "Surrender request", "Capitulation offer"]:
                no_messages = False

    if not no_messages:
        game_stats.peace_offer_text.append("Peace agreement has been already proposed")

    if not game_stats.contact_inspection.AI_player and no_messages:
        game_stats.peace_offer_text.append("Human player")
        game_stats.will_accept_white_peace = True

    elif summary.own_realm_war_enthusiasm >= summary.max_war_enthusiasm and no_messages:
        game_stats.peace_offer_text.append("Enemy is defeated")
        game_stats.peace_offer_text.append("Will accept white peace")
        game_stats.will_accept_white_peace = True

    if not game_stats.will_accept_white_peace and no_messages:
        sufficient_time = 5
        for trait in opponent.behavior_traits:
            if trait in white_peace_war_duration_trait_dict:
                sufficient_time += white_peace_war_duration_trait_dict[trait]

        too_soon = False
        if not summary.player_is_initiator:
            if sufficient_time > summary.war_duration:
                for trait in opponent.behavior_traits:
                    if trait in white_peace_war_duration_trait_dict:
                        game_stats.peace_offer_text.append("Enemy started the war:")
                        game_stats.peace_offer_text.append("+5 months fighting")
                        game_stats.peace_offer_text.append(str(trait) + ": +" +
                                                           str(white_peace_war_duration_trait_dict[trait])
                                                           + " months fighting")
                game_stats.peace_offer_text.append("Enemy desires to keep fighting")
                game_stats.peace_offer_text.append(str(sufficient_time - summary.war_duration) + " months left")
                too_soon = True

        if not too_soon:
            number = summary.own_realm_war_enthusiasm - summary.opponent_war_enthusiasm
            if number >= 0:
                game_stats.peace_offer_text.append("War enthusiasm: " + str(number))
            else:
                game_stats.peace_offer_text.append("War enthusiasm: " + str(number))
            score += int(number)

            for trait in opponent.behavior_traits:
                if trait in white_peace_score_trait_dict:
                    game_stats.peace_offer_text.append(str(trait) + ": " +
                                                       str(white_peace_score_trait_dict[trait]))
                    score += int(white_peace_score_trait_dict[trait])

            if score > 0:
                game_stats.will_accept_white_peace = True
                game_stats.peace_offer_text.append("Total: " + str(score))
                game_stats.peace_offer_text.append("Will accept white peace")
            else:
                game_stats.peace_offer_text.append("Total: " + str(score))
                game_stats.peace_offer_text.append("Won't accept white peace")

    if game_stats.claimed_demands:
        peace_acceptance()


def peace_acceptance():
    print("peace_acceptance")
    game_stats.peace_offer_text = []
    opponent = game_stats.contact_inspection.leader
    game_stats.will_accept_peace_agreement = False
    summary = game_stats.war_summary
    score = 0
    excessive_demands = False

    if game_stats.make_demands:
        ## Make demands
        no_messages = True
        for message in game_stats.realm_inspection.diplomatic_messages:
            if message.dm_from == game_stats.contact_inspection.name:
                if message.subject in ["White peace", "Surrender request", "Capitulation offer"]:
                    no_messages = False

        for message in game_stats.contact_inspection.diplomatic_messages:
            if message.dm_from == game_stats.realm_inspection.name:
                if message.subject in ["White peace", "Surrender request", "Capitulation offer"]:
                    no_messages = False

        if not no_messages:
            game_stats.peace_offer_text.append("Peace agreement has been")
            game_stats.peace_offer_text.append("already proposed")

        if not game_stats.contact_inspection.AI_player and no_messages:
            game_stats.peace_offer_text.append("Human player")
            game_stats.will_accept_peace_agreement = True

        elif summary.own_realm_war_enthusiasm >= summary.max_war_enthusiasm and no_messages:
            game_stats.peace_offer_text.append("Demands cost: " + str(game_stats.calculated_pa_cost)
                                               + "/" + str(summary.max_war_enthusiasm))
            if game_stats.calculated_pa_cost > summary.max_war_enthusiasm:
                game_stats.peace_offer_text.append("Your demands are too harsh")
                excessive_demands = True
            else:
                game_stats.peace_offer_text.append("Enemy is defeated")
                game_stats.peace_offer_text.append("Will accept peace agreement")
                game_stats.will_accept_peace_agreement = True

        if not game_stats.will_accept_peace_agreement and no_messages and not excessive_demands:
            # Expected war time length increase with each war goal
            sufficient_time = 4 + len(summary.war_goals) * 3
            score_per_time = -math.ceil(summary.max_war_enthusiasm/sufficient_time)
            time_effect = score_per_time * (sufficient_time - summary.war_duration)
            print("sufficient_time: " + str(sufficient_time))
            print("score_per_time: " + str(score_per_time))
            print("time_effect: " + str(time_effect))

            number = summary.own_realm_war_enthusiasm - summary.opponent_war_enthusiasm
            if number >= 0:
                game_stats.peace_offer_text.append("War enthusiasm: " + str(number))
            else:
                game_stats.peace_offer_text.append("War enthusiasm: " + str(number))
            score += int(number)

            if time_effect < 0:
                game_stats.peace_offer_text.append("Duration of the war: " + str(time_effect))
                score += int(time_effect)

            for trait in opponent.behavior_traits:
                if trait in peace_score_trait_dict:
                    game_stats.peace_offer_text.append(str(trait) + ": " +
                                                       str(peace_score_trait_dict[trait]))
                    score += int(peace_score_trait_dict[trait])

            if score > 0:
                game_stats.will_accept_peace_agreement = True
                game_stats.peace_offer_text.append("Total: " + str(score))
                game_stats.peace_offer_text.append("Will accept peace agreement")
            else:
                game_stats.peace_offer_text.append("Total: " + str(score))
                game_stats.peace_offer_text.append("Won't accept peace agreement")

    else:
        ## Make concessions
        no_messages = True
        for message in game_stats.realm_inspection.diplomatic_messages:
            if message.dm_from == game_stats.contact_inspection.name:
                if message.subject in ["White peace", "Surrender request", "Capitulation offer"]:
                    no_messages = False

        for message in game_stats.contact_inspection.diplomatic_messages:
            if message.dm_from == game_stats.realm_inspection.name:
                if message.subject in ["White peace", "Surrender request", "Capitulation offer"]:
                    no_messages = False

        if not no_messages:
            game_stats.peace_offer_text.append("Peace agreement has been")
            game_stats.peace_offer_text.append("already proposed")

        if not game_stats.contact_inspection.AI_player and no_messages:
            game_stats.peace_offer_text.append("Human player")
            game_stats.will_accept_peace_agreement = True

        elif summary.opponent_war_enthusiasm >= summary.max_war_enthusiasm and no_messages:
            game_stats.peace_offer_text.append("Demands cost: " + str(game_stats.calculated_pa_cost)
                                               + "/" + str(summary.max_war_enthusiasm))
            if game_stats.calculated_pa_cost > summary.max_war_enthusiasm:
                game_stats.peace_offer_text.append("Excessive concessions")
                excessive_demands = True
            else:
                game_stats.peace_offer_text.append("You are defeated")
                game_stats.will_accept_peace_agreement = True

        if not game_stats.will_accept_peace_agreement and no_messages and not excessive_demands:
            game_stats.will_accept_peace_agreement = True
            game_stats.peace_offer_text.append("Your capitulation")
            game_stats.peace_offer_text.append("would be considered")


def add_demand(demand_item):
    print("add_demand - " + str(demand_item))
    num = 0
    found = False
    for demand in game_stats.claimed_demands:
        if demand[0] == demand_item[0]:
            if demand[0] == "Tribute":
                game_stats.calculated_pa_cost -= war_goal_war_enthusiasm_dict[demand[2]]
                game_stats.demand_details.append(game_stats.claimed_demands.pop(num))
            game_stats.claimed_demands.insert(num, demand_item)
            found = True
            break
        num += 1

    if not found:
        game_stats.claimed_demands.append(demand_item)

    if demand_item[0] == "Conquest":
        game_stats.calculated_pa_cost += 20
    elif demand_item[0] == "Tribute":
        game_stats.calculated_pa_cost += war_goal_war_enthusiasm_dict[demand_item[2]]

    peace_acceptance()


def remove_pressed_demand(wg_num):
    if game_stats.claimed_demands[wg_num][0] == "Conquest":
        game_stats.calculated_pa_cost -= 20
    elif game_stats.claimed_demands[wg_num][0] == "Tribute":
        game_stats.calculated_pa_cost -= war_goal_war_enthusiasm_dict[game_stats.claimed_demands[wg_num][2]]

    if game_stats.demand_details:
        if game_stats.claimed_demands[wg_num][0] == game_stats.demand_details[0][0]:
            game_stats.demand_details.append(game_stats.claimed_demands.pop(wg_num))
        else:
            del game_stats.claimed_demands[wg_num]
    else:
        del game_stats.claimed_demands[wg_num]

    peace_acceptance()


def demands_details_take_territory():
    the_player = game_stats.realm_inspection.name
    the_opponent = game_stats.contact_inspection.name

    avoid_list = []
    if game_stats.claimed_demands:
        for demand in game_stats.claimed_demands:
            if demand[0] == "Conquest":
                avoid_list.append(str(demand[2]))

    list_of_conquest_settlements = []

    for goal in game_stats.war_summary.war_goals:
        if goal[0] == "Conquest":
            print("goal - " + str(goal))
            list_of_conquest_settlements.append(str(goal[6]))

    if game_stats.make_demands:
        for settlement in game_obj.game_cities:
            if settlement.owner == the_opponent:
                if settlement.posxy in game_stats.realm_inspection.known_map:
                    if settlement.military_occupation:
                        if settlement.military_occupation[2] == the_player:
                            if settlement.name not in avoid_list:
                                war_goal = "Conquest"
                                icon = None
                                if settlement.name in list_of_conquest_settlements:
                                    # This settlement was declared a war goal at the start of war
                                    icon = str(war_goal_icon_dict["Conquest"])
                                game_stats.demand_details.append([war_goal, icon, str(settlement.name),
                                                                  int(settlement.city_id)])
                                # print(str(game_stats.demand_details))


def demands_details_impose_tribute():
    print("demands_details_impose_tribute")
    goal_tribute = ""
    for goal in game_stats.war_summary.war_goals:
        print(str(goal))
        if goal[0] == "Tribute":
            goal_tribute = str(goal[6])
            break

    the_war = None
    for war in game_obj.game_wars:
        if war.initiator == game_stats.realm_inspection.name \
                or war.respondent == game_stats.realm_inspection.name:
            if war.initiator == game_stats.contact_inspection.name \
                    or war.respondent == game_stats.contact_inspection.name:
                the_war = war
                break

    if game_stats.make_demands:
        # Make demands from enemy
        # Battle victories
        battle_success_rate = 0.0
        print("initiator_battle_victories " + str(the_war.initiator_battle_victories))
        print("respondent_battle_victories " + str(the_war.respondent_battle_victories))
        if the_war.initiator_battle_victories + the_war.respondent_battle_victories > 0:
            if the_war.initiator == game_stats.realm_inspection.name:
                battle_success_rate = the_war.initiator_battle_victories / \
                                      (the_war.initiator_battle_victories + the_war.respondent_battle_victories)
            else:
                battle_success_rate = the_war.respondent_battle_victories / \
                                      (the_war.initiator_battle_victories + the_war.respondent_battle_victories)

        print("battle_success_rate " + str(battle_success_rate))
        avoid = None
        if game_stats.claimed_demands:
            for demand in game_stats.claimed_demands:
                if demand[0] == "Tribute":
                    avoid = str(demand[2])

        if avoid != "Low tribute":
            icon = None
            if goal_tribute == "Low tribute":
                icon = str(war_goal_icon_dict["Tribute"])
            game_stats.demand_details.append(["Tribute", icon, "Low tribute", int(0.1)])

        if battle_success_rate >= tribute_success_rate_dict["Moderate tribute"]:
            if avoid != "Moderate tribute":
                icon = None
                if goal_tribute == "Moderate tribute":
                    icon = str(war_goal_icon_dict["Tribute"])
                game_stats.demand_details.append(["Tribute", icon, "Moderate tribute", int(0.25)])

            if battle_success_rate >= tribute_success_rate_dict["Severe tribute"]:
                if avoid != "Severe tribute":
                    icon = None
                    if goal_tribute == "Severe tribute":
                        icon = str(war_goal_icon_dict["Tribute"])
                    game_stats.demand_details.append(["Tribute", icon, "Severe tribute", int(0.5)])

                if battle_success_rate >= tribute_success_rate_dict["Harsh tribute"]:
                    if avoid != "Harsh tribute":
                        icon = None
                        if goal_tribute == "Harsh tribute":
                            icon = str(war_goal_icon_dict["Tribute"])
                        game_stats.demand_details.append(["Tribute", icon, "Harsh tribute", int(0.8)])

    else:
        # Make concessions for enemy
        # Battle victories
        battle_success_rate = 0.0
        print("initiator_battle_victories " + str(the_war.initiator_battle_victories))
        print("respondent_battle_victories " + str(the_war.respondent_battle_victories))
        if the_war.initiator_battle_victories + the_war.respondent_battle_victories > 0:
            if the_war.initiator == game_stats.contact_inspection.name:
                battle_success_rate = the_war.initiator_battle_victories / \
                                      (the_war.initiator_battle_victories + the_war.respondent_battle_victories)
            else:
                battle_success_rate = the_war.respondent_battle_victories / \
                                      (the_war.initiator_battle_victories + the_war.respondent_battle_victories)

        print("battle_success_rate " + str(battle_success_rate))
        avoid = None
        if game_stats.claimed_demands:
            for demand in game_stats.claimed_demands:
                if demand[0] == "Tribute":
                    avoid = str(demand[2])

        if avoid != "Low tribute":
            icon = None
            if goal_tribute == "Low tribute":
                icon = str(war_goal_icon_dict["Tribute"])
            game_stats.demand_details.append(["Tribute", icon, "Low tribute", int(0.1)])

        if battle_success_rate >= tribute_success_rate_dict["Moderate tribute"]:
            if avoid != "Moderate tribute":
                icon = None
                if goal_tribute == "Moderate tribute":
                    icon = str(war_goal_icon_dict["Tribute"])
                game_stats.demand_details.append(["Tribute", icon, "Moderate tribute", int(0.25)])

            if battle_success_rate >= tribute_success_rate_dict["Severe tribute"]:
                if avoid != "Severe tribute":
                    icon = None
                    if goal_tribute == "Severe tribute":
                        icon = str(war_goal_icon_dict["Tribute"])
                    game_stats.demand_details.append(["Tribute", icon, "Severe tribute", int(0.5)])

                if battle_success_rate >= tribute_success_rate_dict["Harsh tribute"]:
                    if avoid != "Harsh tribute":
                        icon = None
                        if goal_tribute == "Harsh tribute":
                            icon = str(war_goal_icon_dict["Tribute"])
                        game_stats.demand_details.append(["Tribute", icon, "Harsh tribute", int(0.8)])

        print("demand_details " + str(game_stats.demand_details))


def propose_white_peace():
    the_player = game_stats.realm_inspection
    opponent = game_stats.contact_inspection
    no_messages = True
    for message in the_player.diplomatic_messages:
        if message.dm_from == opponent.name:
            if message.subject in ["White peace", "Surrender request", "Capitulation offer"]:
                no_messages = False

    for message in opponent.diplomatic_messages:
        if message.dm_from == the_player.name:
            if message.subject in ["White peace", "Surrender request", "Capitulation offer"]:
                no_messages = False

    if no_messages:
        opponent.turn_completed = False
        opponent.diplomatic_messages.append(diplomacy_classes.Diplomatic_Message(str(the_player.name),
                                                                                 str(opponent.name),
                                                                                 "White peace",
                                                                                 []))


def propose_peace_agreement():
    the_player = game_stats.realm_inspection
    opponent = game_stats.contact_inspection
    no_messages = True
    for message in the_player.diplomatic_messages:
        if message.dm_from == opponent.name:
            if message.subject in ["White peace", "Surrender request", "Capitulation offer"]:
                no_messages = False

    for message in opponent.diplomatic_messages:
        if message.dm_from == the_player.name:
            if message.subject in ["White peace", "Surrender request", "Capitulation offer"]:
                no_messages = False

    if no_messages:
        if game_stats.make_demands:
            ## Make demands
            opponent.turn_completed = False
            opponent.diplomatic_messages.append(diplomacy_classes.Diplomatic_Message(str(the_player.name),
                                                                                     str(opponent.name),
                                                                                     "Surrender request",
                                                                                     list(game_stats.claimed_demands)))
        else:
            ## Make concessions
            opponent.turn_completed = False
            opponent.diplomatic_messages.append(diplomacy_classes.Diplomatic_Message(str(the_player.name),
                                                                                     str(opponent.name),
                                                                                     "Capitulation offer",
                                                                                     list(game_stats.claimed_demands)))


def accept_white_peace(diplomatic_messages, message):
    # Remove war
    # print("message.dm_from - " + str(message.dm_from) + "; message.dm_to - " + str(message.dm_to))
    num = 0
    for war in game_obj.game_wars:
        # print("num - " + str(num) + "; war.initiator - " + str(war.initiator) +
        #       "; war.respondent - " + str(war.respondent))
        if war.initiator == message.dm_from \
                or war.initiator == message.dm_to:
            if war.respondent == message.dm_from \
                    or war.respondent == message.dm_to:
                # print("break: num - " + str(num))
                break
        num += 1

    # print("num - " + str(num))
    del game_obj.game_wars[num]

    # Remove occupation
    for settlement in game_obj.game_cities:
        if settlement.owner == message.dm_to:
            if settlement.military_occupation:
                if settlement.military_occupation[2] == message.dm_from:
                    settlement.military_occupation = None

    # Remove war notification
    num = 0
    for notification in game_stats.ongoing_wars:
        if notification[2] in [message.dm_from, message.dm_to]:
            break
        num += 1

    del game_stats.ongoing_wars[num]

    if game_stats.war_notifications_index > 0:
        game_stats.war_notifications_index -= 1

    # Remove from lists of ongoing wars
    for realm in game_obj.game_powers:
        if realm.name == message.dm_from:
            num = 0
            for opponent in realm.relations.at_war:
                if opponent[2] == message.dm_to:
                    break
                num += 1
            if num < len(realm.relations.at_war):
                del realm.relations.at_war[num]
            break

    for realm in game_obj.game_powers:
        if realm.name == message.dm_to:
            num = 0
            for opponent in realm.relations.at_war:
                if opponent[2] == message.dm_from:
                    break
                num += 1
            if num < len(realm.relations.at_war):
                del realm.relations.at_war[num]
            break

    # Move out all armies from foreign settlements and finish sieges
    for army in game_obj.game_armies:
        if army.owner == message.dm_from:
            if army.action in ["Stand", "Ready to move", "Moving", "Routing"]:
                if game_obj.game_map[army.location].lot:
                    if game_obj.game_map[army.location].lot == "City":
                        for settlement in game_obj.game_cities:
                            if settlement.owner == message.dm_to:
                                game_basic.move_out_army_from_settlement(army)
                                break
            elif army.action == "Besieging":
                settlement, defender = game_basic.find_siege(army)
                if defender.owner == message.dm_to:
                    game_basic.finish_settlement_blockade(settlement, army, defender)

        elif army.owner == message.dm_to:
            if army.action in ["Stand", "Ready to move", "Moving", "Routing"]:
                if game_obj.game_map[army.location].lot:
                    if game_obj.game_map[army.location].lot == "City":
                        for settlement in game_obj.game_cities:
                            if settlement.owner == message.dm_from:
                                game_basic.move_out_army_from_settlement(army)
                                break
            elif army.action == "Besieging":
                settlement, defender = game_basic.find_siege(army)
                if defender.owner == message.dm_from:
                    game_basic.finish_settlement_blockade(settlement, army, defender)

    # Remove message
    num = 0
    for mes in diplomatic_messages:
        if mes == message:
            break
        num += 1

    del diplomatic_messages[num]

    if game_stats.diplomacy_area in ["Diplomatic actions", "Sue for peace", "Draft a peace offer"]:
        sf_game_board.return_to_diplomatic_actions_area_but()


def accept_peace_agreement(diplomatic_messages, message):
    # print("message.subject == Surrender request")
    print("message.subject - " + str(message.subject))
    # Remove war
    num = 0
    for war in game_obj.game_wars:
        if war.initiator == message.dm_from \
                or war.initiator == message.dm_to:
            if war.respondent == message.dm_from \
                    or war.respondent == message.dm_to:
                print("War: " + str(war.initiator) + " vs " + str(war.respondent))
                break
        num += 1

    print("num - " + str(num) + "; len(game_obj.game_wars) - " + str(len(game_obj.game_wars)))
    del game_obj.game_wars[num]

    # Remove war notification
    num = 0
    for notification in game_stats.ongoing_wars:
        if notification[2] in [message.dm_from, message.dm_to]:
            break
        num += 1

    del game_stats.ongoing_wars[num]

    if game_stats.war_notifications_index > 0:
        game_stats.war_notifications_index -= 1

    # Remove from lists of ongoing wars
    for realm in game_obj.game_powers:
        if realm.name == message.dm_from:
            num = 0
            for opponent in realm.relations.at_war:
                if opponent[2] == message.dm_to:
                    break
                num += 1
            if num < len(realm.relations.at_war):
                del realm.relations.at_war[num]
            break

    for realm in game_obj.game_powers:
        if realm.name == message.dm_to:
            num = 0
            for opponent in realm.relations.at_war:
                if opponent[2] == message.dm_from:
                    break
                num += 1
            if num < len(realm.relations.at_war):
                del realm.relations.at_war[num]
            break

    if message.subject == "Surrender request":
        ## Enforcing demands
        # Transfer province ownership
        for demand in message.contents:
            if demand[0] == "Conquest":
                for settlement in game_obj.game_cities:
                    if settlement.city_id == demand[3]:
                        settlement.military_occupation = None
                        settlement.owner = str(message.dm_from)

    elif message.subject == "Capitulation offer":
        ## Enforcing concessions
        # Transfer province ownership
        for demand in message.contents:
            if demand[0] == "Conquest":
                for settlement in game_obj.game_cities:
                    if settlement.city_id == demand[3]:
                        # settlement.military_occupation = None
                        settlement.owner = str(message.dm_to)

    # Remove occupation
    for settlement in game_obj.game_cities:
        if settlement.owner == message.dm_to:
            if settlement.military_occupation:
                if settlement.military_occupation[2] == message.dm_from:
                    settlement.military_occupation = None
        elif settlement.owner == message.dm_from:
            if settlement.military_occupation:
                if settlement.military_occupation[2] == message.dm_to:
                    settlement.military_occupation = None

    # Move out all armies from foreign settlements
    for army in game_obj.game_armies:
        if army.owner == message.dm_from:
            if army.action in ["Stand", "Ready to move", "Moving", "Routing"]:
                print("posxy - " + str(army.posxy) + "; location - " + str(army.location))
                if game_obj.game_map[army.location].lot:
                    if game_obj.game_map[army.location].lot == "City":
                        for settlement in game_obj.game_cities:
                            if settlement.city_id == game_obj.game_map[army.location].city_id:
                                if settlement.owner == message.dm_to:
                                    print("Settlement - " + str(settlement.name) + ", " + str(settlement.owner) +
                                          "; realm - " + str(message.dm_to))
                                    game_basic.move_out_army_from_settlement(army)
                                break
            elif army.action == "Besieging":
                settlement, defender = game_basic.find_siege(army)
                if defender.owner == message.dm_to:
                    game_basic.finish_settlement_blockade(settlement, army, defender)

        elif army.owner == message.dm_to:
            if army.action in ["Stand", "Ready to move", "Moving", "Routing"]:
                if game_obj.game_map[army.location].lot:
                    if game_obj.game_map[army.location].lot == "City":
                        for settlement in game_obj.game_cities:
                            if settlement.city_id == game_obj.game_map[army.location].city_id:
                                if settlement.owner == message.dm_from:
                                    game_basic.move_out_army_from_settlement(army)
                                break
            elif army.action == "Besieging":
                settlement, defender = game_basic.find_siege(army)
                if defender.owner == message.dm_from:
                    game_basic.finish_settlement_blockade(settlement, army, defender)

    realm_name = None
    count_left_settlements = 0
    if message.subject == "Surrender request":
        realm_name = str(message.dm_to)
        for settlement in game_obj.game_cities:
            if settlement.owner == message.dm_to:
                print("Counting (" + str(count_left_settlements) + "): settlement - " + str(settlement.name) + ", " +
                      str(settlement.owner) + "; realm - " + str(message.dm_to))
                count_left_settlements += 1

    elif message.subject == "Capitulation offer":
        realm_name = str(message.dm_from)
        for settlement in game_obj.game_cities:
            if settlement.owner == message.dm_from:
                print("Counting (" + str(count_left_settlements) + "): settlement - " + str(settlement.name) + ", " +
                      str(settlement.owner) + "; realm - " + str(message.dm_from))
                count_left_settlements += 1

    # Remove message
    num = 0
    for mes in diplomatic_messages:
        if mes == message:
            break
        num += 1

    del diplomatic_messages[num]

    if count_left_settlements == 0:
        # Realm doesn't have any provinces left
        # It should be transferred to the bin
        # And removed from contact lists
        for realm in game_obj.game_powers:
            if realm.name == realm_name:
                realm.contacts = []
            if realm_name in realm.contacts:
                realm.contacts.remove(realm_name)

        num = 0
        for contact in game_stats.explored_contacts:
            if contact[2] == realm_name:
                break
            num += 1

        if num < len(game_stats.explored_contacts):
            del game_stats.explored_contacts[num]
            if game_stats.contact_index > 0:
                game_stats.contact_index -= 1

        num = 0
        for realm in game_obj.game_powers:
            if realm.name == realm_name:
                break
            else:
                num += 1

        if num < len(game_obj.game_powers):
            game_obj.bin_realms.append(game_obj.game_powers.pop(num))
            print("bin_realms: " + str(len(game_obj.bin_realms)))
            former_realm = game_obj.bin_realms[-1]
            print(former_realm.name + " // messages: " + str(len(former_realm.diplomatic_messages)))
            print(former_realm.name + " // contacts: " + str(len(former_realm.contacts)))

        if game_stats.contact_inspection.name == realm_name:
            print("game_stats.contact_inspection = None")
            game_stats.contact_inspection = None

    # if game_stats.contact_inspection.name == realm_name:
    if game_stats.diplomacy_area in ["Diplomatic actions", "Sue for peace", "Draft a peace offer"]:
        sf_game_board.return_to_diplomatic_actions_area_but()


def prepare_threats():
    ## Conquest casus belli
    # War goal is to conquer a province by taking its settlement
    permissible_settlements = []
    for settlement in game_obj.game_cities:
        if settlement.owner == game_stats.contact_inspection.name:
            if settlement.posxy in game_stats.realm_inspection.known_map:
                permissible_settlements.append(int(settlement.city_id))

    if len(permissible_settlements) > 0:
        game_stats.casus_bellis.append("Give up territory")

    # War goal is to collect tribute
    game_stats.casus_bellis.append("Tribute")


def threats_details_give_up_territory():
    avoid_list = []
    if game_stats.war_goals:
        for threat_item in game_stats.war_goals:
            if threat_item[2] == "Territory concession":
                avoid_list.append(str(threat_item[0]))

    for settlement in game_obj.game_cities:
        if settlement.owner == game_stats.contact_inspection.name:
            if settlement.posxy in game_stats.realm_inspection.known_map:
                if not settlement.military_occupation:
                    if settlement.name not in avoid_list:
                        game_stats.cb_details.append([str(settlement.name), int(settlement.city_id),
                                                      "Territory concession"])


def threats_details_tribute():
    avoid = None
    if game_stats.war_goals:
        for threat_item in game_stats.war_goals:
            if threat_item[2] == "Tribute":
                avoid = str(threat_item[0])
                print(threat_item[2] + " - " + threat_item[0])

    if avoid != "Low tribute":
        # Low tribute - 10%
        game_stats.cb_details.append(["Low tribute", int(0.1), "Tribute"])
    if avoid != "Moderate tribute":
        # Moderate tribute - 25%
        game_stats.cb_details.append(["Moderate tribute", int(0.25), "Tribute"])
    if avoid != "Severe tribute":
        # Severe tribute - 50%
        game_stats.cb_details.append(["Severe tribute", int(0.50), "Tribute"])
    if avoid != "Harsh tribute":
        # Harsh tribute - 80%
        game_stats.cb_details.append(["Harsh tribute", int(0.80), "Tribute"])


def add_threat_demand(threat_item):
    print("select_threat_item - " + str(threat_item))
    num = 0
    found = False
    for demand in game_stats.war_goals:
        if demand[2] == threat_item[2]:
            if threat_item[2] == "Tribute":
                game_stats.cb_details.append(game_stats.war_goals.pop(num))
            game_stats.war_goals.insert(num, threat_item)
            found = True
            break
        num += 1

    if not found:
        game_stats.war_goals.append(threat_item)

    threat_acceptance()


def remove_threat_demand(wg_num):
    if game_stats.cb_details:
        if game_stats.war_goals[wg_num][2] == game_stats.cb_details[0][2]:
            game_stats.cb_details.append(game_stats.war_goals.pop(wg_num))
        else:
            del game_stats.war_goals[wg_num]
    else:
        del game_stats.war_goals[wg_num]

    threat_acceptance()


def threat_acceptance():
    print("threat_acceptance")
    the_player = game_stats.realm_inspection
    opponent = game_stats.contact_inspection
    game_stats.will_accept_threat_demands = False
    game_stats.summary_text = []
    unacceptable = False

    no_messages = True
    for message in game_stats.contact_inspection.diplomatic_messages:
        if message.dm_from == game_stats.realm_inspection.name:
            if message.subject == "Threat":
                game_stats.summary_text.append("Target has been")
                game_stats.summary_text.append("already threatened")
                no_messages = False

    opponent_settlements = 0
    for settlement in game_obj.game_cities:
        if settlement.owner == opponent.name:
            opponent_settlements += 1

    demanded_settlements = 0
    for demand in game_stats.war_goals:
        if demand[2] == "Territory concession":
            demanded_settlements += 1

    if demanded_settlements >= opponent_settlements:
        game_stats.summary_text.append("Target won't give up its")
        game_stats.summary_text.append("last territory")
        unacceptable = True

    print("demanded_settlements - " + str(demanded_settlements) + " from " + str(opponent.name))
    print("2. will_accept_threat_demands - " + str(game_stats.will_accept_threat_demands))

    if not game_stats.contact_inspection.AI_player and no_messages and not unacceptable:
        game_stats.summary_text.append("Human player")
        game_stats.will_accept_threat_demands = True

    if not game_stats.will_accept_threat_demands and no_messages and not unacceptable:
        your_power_level = 0.0
        target_power_level = 0.0
        strength_score = 0.0
        target_settlements = 0

        for settlement in game_obj.game_cities:
            if settlement.owner == the_player.name:
                if settlement.military_occupation:
                    your_power_level += 0.5
                else:
                    your_power_level += 1.0
            elif settlement.owner == opponent.name:
                target_settlements += 1
                if settlement.military_occupation:
                    target_power_level += 0.5
                else:
                    target_power_level += 1.0

        abs_advantage = your_power_level - target_power_level
        rel_advantage = your_power_level / (target_power_level + your_power_level)
        print("abs_advantage - " + str(abs_advantage))
        print("rel_advantage - " + str(rel_advantage))

        if abs_advantage <= 0.0:
            game_stats.will_accept_threat_demands = False
            game_stats.summary_text.append("Target is not afraid of you")
        else:
            game_stats.will_accept_threat_demands = True
            strength_score += math.ceil((abs_advantage * 10 * rel_advantage) * 100) / 100
            print("strength_score - " + str(strength_score))

            demands_score = 0.0

            for demand in game_stats.war_goals:
                print(demand)
                if demand[2] == "Territory concession":
                    demands_score += 25.0

                elif demand[2] == "Tribute":
                    demands_score += war_goal_war_enthusiasm_dict[demand[0]]
                    if demand[0] == "Low tribute":
                        demands_score += 1 * target_settlements
                    elif demand[0] == "Moderate tribute":
                        demands_score += 2 * target_settlements
                    elif demand[0] == "Severe tribute":
                        demands_score += 3 * target_settlements
                    elif demand[0] == "Harsh tribute":
                        demands_score += 4 * target_settlements

            print("demands_score - " + str(demands_score))
            print("best result - " + str(strength_score + 20.0 - demands_score))

            if strength_score + 20.0 - demands_score < 0.0:
                game_stats.will_accept_peace_agreement = False
                game_stats.summary_text.append("Won't accept")
            elif strength_score + 20.0 - demands_score < 4.0:
                game_stats.summary_text.append("Very unlikely to accept")
            elif strength_score + 20.0 - demands_score < 8.0:
                game_stats.summary_text.append("Unlikely to accept")
            elif strength_score + 20.0 - demands_score < 12.0:
                game_stats.summary_text.append("Uncertain result")
            elif strength_score + 20.0 - demands_score < 16.0:
                game_stats.summary_text.append("Likely to accept")
            elif strength_score + 20.0 - demands_score < 20.0:
                game_stats.summary_text.append("Very likely to accept")
            else:
                game_stats.summary_text.append("Wouldn't dare to reject")


def send_threat():
    the_player = game_stats.realm_inspection
    opponent = game_stats.contact_inspection

    no_messages = True
    for message in the_player.diplomatic_messages:
        if message.dm_from == opponent.name:
            if message.subject == "Threat":
                no_messages = False

    for message in opponent.diplomatic_messages:
        if message.dm_from == the_player.name:
            if message.subject == "Threat":
                no_messages = False

    if no_messages:
        opponent.turn_completed = False
        opponent.diplomatic_messages.append(diplomacy_classes.Diplomatic_Message(str(the_player.name),
                                                                                 str(opponent.name),
                                                                                 "Threat",
                                                                                 list(game_stats.war_goals)))


def accept_threat_demand(diplomatic_messages, message):
    # Transfer province ownership
    for demand in message.contents:
        print("demand: " + str(demand))
        if demand[2] == "Territory concession":
            for settlement in game_obj.game_cities:
                if settlement.city_id == demand[1]:
                    settlement.owner = str(message.dm_from)

    # Remove message
    num = 0
    for mes in diplomatic_messages:
        if mes == message:
            break
        num += 1

    del diplomatic_messages[num]

    if game_stats.diplomacy_area == "Threaten":
        sf_game_board.return_to_diplomatic_actions_area_but()


cb_details_dict = {"Conquest" : cb_details_conquest,
                   "Tribute" : cb_details_tribute}


war_goal_war_enthusiasm_dict = {"Conquest" : 20,
                                "Low tribute" : 10,
                                "Moderate tribute" : 15,
                                "Severe tribute" : 20,
                                "Harsh tribute" : 30}


war_goal_icon_dict = {"Conquest" : "Icons/captured_province",
                      "Tribute" : "Icons/coins_tribute"}


demands_details_dict = {"Take territory" : demands_details_take_territory,
                        "Impose tribute" : demands_details_impose_tribute}

threats_details_dict = {"Give up territory" : threats_details_give_up_territory,
                        "Tribute" : threats_details_tribute}

white_peace_war_duration_trait_dict = {"Aggressor" : +3,
                                       "Warmonger" : +3}

white_peace_score_trait_dict = {"Pacifist" : + 5,
                                "Aggressor" : -5,
                                "Vindictive" : -5,
                                "Warmonger" : -5}

peace_score_trait_dict = {"Pacifist" : + 5,
                          "Aggressor" : -5,
                          "Vindictive" : -10,
                          "Warmonger" : -5}

tribute_success_rate_dict = {"Low tribute" : 0.5,
                             "Moderate tribute" : 0.6,
                             "Severe tribute" : 0.7,
                             "Harsh tribute" : 0.8}
