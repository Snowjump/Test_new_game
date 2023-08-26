## Miracle battles

import random

from Resources import game_obj
from Resources import game_stats
from Resources import game_diplomacy
from Resources import diplomacy_classes


def attack_humans_AI(AI):
    # AI = realm of computer player
    # Test module
    names_at_war = []
    targets_for_new_war = []

    for name in AI.relations.at_war:
        names_at_war.append(name[2])

    # Collect new targets
    for realm in game_obj.game_powers:
        if realm.name in AI.contacts:
            if not realm.AI_player:
                if realm.name not in names_at_war:
                    targets_for_new_war.append(realm.name)

    # Declare war
    for target_name in targets_for_new_war:
        # Choose casus belli
        target_settlements = []
        for settlement in game_obj.game_cities:
            if settlement.owner == target_name:
                target_settlements.append([str(settlement.name), int(settlement.city_id), "Conquest"])

        max_we = 10
        if len(target_settlements) > 0:
            war_goals = [random.choice(target_settlements)]
            max_we += 30
            target = None
            for realm in game_obj.game_powers:
                if realm.name == target_name:
                    target = realm
                    break

            AI_declare_war(war_goals, AI, target, max_we)
            print(AI.name + " declare war on " + target_name)

    at_war_status = False
    for war in game_obj.game_wars:
        if war.initiator == AI.name or war.initiator == AI.name:
            at_war_status = True
            break

    if at_war_status:
        AI.AI_cogs.cognition_stage = "Economy"  # "Manage armies"
    else:
        AI.AI_cogs.cognition_stage = "Economy"  # "Finished turn"


def propose_white_peace_to_humans_AI(AI):
    # AI = realm of computer player
    # Test module
    names_at_war = []
    targets_for_white_peace = []

    for name in AI.relations.at_war:
        names_at_war.append(name[2])

    # Collect new targets
    for realm in game_obj.game_powers:
        if realm.name in AI.contacts:
            if not realm.AI_player:
                if realm.name in names_at_war:
                    targets_for_white_peace.append(realm.name)

    # Propose white peace
    for target_name in targets_for_white_peace:
        target = None
        for realm in game_obj.game_powers:
            if realm.name == target_name:
                target = realm
                break

        AI_propose_white_peace(AI, target)
        print(AI.name + " propose white peace to " + target_name)


def propose_peace_agreement_to_humans_AI(AI):
    # AI = realm of computer player
    # Test module
    names_at_war = []
    targets_for_peace = []

    for name in AI.relations.at_war:
        names_at_war.append(name[2])

    # Collect new targets
    for realm in game_obj.game_powers:
        if realm.name in AI.contacts:
            if not realm.AI_player:
                if realm.name in names_at_war:
                    targets_for_peace.append(realm.name)

    # Propose peace offer
    for target_name in targets_for_peace:
        target = None
        for realm in game_obj.game_powers:
            if realm.name == target_name:
                target = realm
                break

        # Evaluate war enthusiasm
        the_war = None
        for war in game_obj.game_wars:
            # print("num - " + str(num) + "; war.initiator - " + str(war.initiator) +
            #       "; war.respondent - " + str(war.respondent))
            if war.initiator == AI.name or war.initiator == target_name:
                if war.respondent == AI.name or war.respondent == target_name:
                    # print("break: num - " + str(num))
                    the_war = war
                    break

        summary = game_diplomacy.create_war_summary(AI.name, target_name, the_war)

        if summary.own_realm_war_enthusiasm >= summary.max_war_enthusiasm:
            print("AI undeniable victory - no action for now WIP")
        elif summary.own_realm_war_enthusiasm > summary.opponent_war_enthusiasm:
            print("AI is leading - no action for now WIP")
        elif summary.own_realm_war_enthusiasm < summary.opponent_war_enthusiasm:
            AI_propose_capitulation(AI, target, the_war, summary)
            # print("AI is losing - no action for now WIP")


def AI_declare_war(war_goals, AI, target, max_we):
    game_obj.game_wars.append(diplomacy_classes.War(str(AI.name),
                                                    str(AI.f_color),
                                                    str(AI.s_color),
                                                    str(target.name),
                                                    str(target.f_color),
                                                    str(target.s_color),
                                                    list(war_goals),
                                                    int(max_we)))

    if target.name == game_stats.player_power:
        game_stats.ongoing_wars.append([str(AI.f_color),
                                        str(AI.s_color),
                                        str(AI.name)])

        game_stats.new_tasks = True
        game_stats.turn_hourglass = False

    target.turn_completed = False

    AI.relations.at_war.append([str(target.f_color),
                                str(target.s_color),
                                str(target.name)])

    target.relations.at_war.append([str(AI.f_color),
                                    str(AI.s_color),
                                    str(AI.name)])

    # Send message
    target.diplomatic_messages.append(diplomacy_classes.Diplomatic_Message(str(AI.name),
                                                                           str(target.name),
                                                                           "Declaration of war",
                                                                           list(war_goals),
                                                                           str(AI.f_color),
                                                                           str(AI.s_color)))


def AI_propose_white_peace(AI, target):
    no_messages = True
    for message in AI.diplomatic_messages:
        if message.dm_from == target.name:
            if message.subject in ["White peace", "Surrender request"]:
                no_messages = False

    for message in target.diplomatic_messages:
        if message.dm_from == AI.name:
            if message.subject in ["White peace", "Surrender request"]:
                no_messages = False

    if no_messages:
        if target.name == game_stats.player_power:
            game_stats.new_tasks = True
            game_stats.turn_hourglass = False

        target.turn_completed = False
        target.diplomatic_messages.append(diplomacy_classes.Diplomatic_Message(str(AI.name),
                                                                               str(target.name),
                                                                               "White peace",
                                                                               [],
                                                                               str(AI.f_color),
                                                                               str(AI.s_color)))


def AI_propose_capitulation(AI, target, war, summary):
    concessions = []
    list_of_conquest_settlements = []

    for goal in summary.war_goals:
        if goal[0] == "Conquest":
            print("goal - " + str(goal))
            list_of_conquest_settlements.append(str(goal[6]))

    for settlement in game_obj.game_cities:
        if settlement.owner == AI.name:
            # if settlement.posxy in AI.known_map:
            if settlement.military_occupation:
                if settlement.military_occupation[2] == target.name:
                    war_goal = "Conquest"
                    icon = None
                    if settlement.name in list_of_conquest_settlements:
                        # This settlement was declared a war goal at the start of war
                        icon = str(game_diplomacy.war_goal_icon_dict["Conquest"])
                    concessions.append([war_goal, icon, str(settlement.name),
                                       int(settlement.city_id)])

    # Battle victories
    battle_success_rate = 0.0
    print("initiator_battle_victories " + str(war.initiator_battle_victories))
    print("respondent_battle_victories " + str(war.respondent_battle_victories))
    if war.initiator_battle_victories + war.respondent_battle_victories > 0:
        if war.initiator == target.name:
            battle_success_rate = war.initiator_battle_victories / \
                                  (war.initiator_battle_victories + war.respondent_battle_victories)
        else:
            battle_success_rate = war.respondent_battle_victories / \
                                  (war.initiator_battle_victories + war.respondent_battle_victories)

    print("battle_success_rate " + str(battle_success_rate))

    goal_tribute = ""
    for goal in summary.war_goals:
        print(str(goal))
        if goal[0] == "Tribute":
            goal_tribute = str(goal[6])
            break

    if war.initiator_battle_victories + war.respondent_battle_victories > 0:
        icon = None
        if goal_tribute == "Low tribute":
            icon = str(game_diplomacy.war_goal_icon_dict["Tribute"])
        concessions.append(["Tribute", icon, "Low tribute", int(0.1)])

        if battle_success_rate >= game_diplomacy.tribute_success_rate_dict["Moderate tribute"]:
            icon = None
            if goal_tribute == "Moderate tribute":
                icon = str(game_diplomacy.war_goal_icon_dict["Tribute"])
            concessions.append(["Tribute", icon, "Moderate tribute", int(0.25)])

            if battle_success_rate >= game_diplomacy.tribute_success_rate_dict["Severe tribute"]:
                icon = None
                if goal_tribute == "Severe tribute":
                    icon = str(game_diplomacy.war_goal_icon_dict["Tribute"])
                concessions.append(["Tribute", icon, "Severe tribute", int(0.5)])

                if battle_success_rate >= game_diplomacy.tribute_success_rate_dict["Harsh tribute"]:
                    icon = None
                    if goal_tribute == "Harsh tribute":
                        icon = str(game_diplomacy.war_goal_icon_dict["Tribute"])
                    concessions.append(["Tribute", icon, "Harsh tribute", int(0.8)])

    if len(concessions) > 0:
        concessions = [random.choice(concessions)]

        if target.name == game_stats.player_power:
            game_stats.new_tasks = True
            game_stats.turn_hourglass = False

        target.turn_completed = False
        target.diplomatic_messages.append(diplomacy_classes.Diplomatic_Message(str(AI.name),
                                                                               str(target.name),
                                                                               "Capitulation offer",
                                                                               concessions,
                                                                               str(AI.f_color),
                                                                               str(AI.s_color)))
