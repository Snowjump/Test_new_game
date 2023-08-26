## Miracle battles
## battle_result_scripts

import math
import copy

from Resources import game_stats
from Resources import game_classes
from Resources import artifact_classes
from Resources import game_obj
from Resources import game_basic

from Content import artifact_imgs_cat
from Content import artifact_catalog

from Storage import create_unit


resource_names = ["Florins",
                  "Food",
                  "Wood"]


def runaway_serfs_refuge_result_close():
    the_army, the_realm = give_army_and_realm()

    # prize = [["Food", 500], ["Wood", 300]]
    # for new_res in prize:
    #     found = False
    #     if len(the_realm.coffers) > 0:
    #         for res in the_realm.coffers:
    #             if res[0] == new_res[0]:
    #                 res[1] += new_res[1]
    #                 found = True
    #                 break
    #
    #     if not found:
    #         the_realm.coffers.append([str(new_res[0]), int(new_res[1])])

    spread_reward(the_army, the_realm)

    game_stats.reward_for_demonstration = None
    game_stats.game_board_panel = ""
    game_stats.event_panel_det = None
    game_stats.battle_result_script = None


def treasure_tower_result_close():
    the_army, the_realm = give_army_and_realm()

    # prize = [["Florins", 1200]]
    # for new_res in prize:
    #     found = False
    #     if len(the_realm.coffers) > 0:
    #         for res in the_realm.coffers:
    #             if res[0] == new_res[0]:
    #                 res[1] += new_res[1]
    #                 found = True
    #                 break
    #
    #     if not found:
    #         the_realm.coffers.append([str(new_res[0]), int(new_res[1])])

    spread_reward(the_army, the_realm)

    game_stats.reward_for_demonstration = None
    game_stats.game_board_panel = ""
    game_stats.event_panel_det = None
    game_stats.battle_result_script = None


def lair_of_grey_dragons_result_close():
    the_army, the_realm = give_army_and_realm()

    for number in game_stats.second_army_exchange_list:
        unit_info = game_stats.reward_for_demonstration[number]
        units_list = list(create_unit.LE_units_dict_by_alignment[unit_info[2]])
        for new_unit in units_list:
            if new_unit.name == unit_info[1]:
                the_army.units.append(copy.deepcopy(new_unit))
                print("Added to army new unit - " + new_unit.name)
                print("Img - " + new_unit.img)
                break

    game_stats.second_army_exchange_list = []

    game_basic.establish_leader(the_army.army_id, "Game")

    game_stats.reward_for_demonstration = None
    game_stats.game_board_panel = ""
    game_stats.event_panel_det = None
    game_stats.battle_result_script = None


def lair_of_grey_dragons_result_acquire_regiments(position):
    square = [493, 238, 753, 468]
    if square[0] < position[0] < square[2] and square[1] < position[1] < square[3]:
        game_stats.button_pressed = True
        x_axis, y_axis = position[0], position[1]
        x_axis -= 493
        y_axis -= 233
        x_axis = math.ceil(x_axis / 52)
        y_axis = math.ceil(y_axis / 57)
        # Add new units to exchange list
        number = int(y_axis - 1) * 5 + int(x_axis) - 1
        print("number - " + str(number))
        approaching_army = None
        for army in game_obj.game_armies:
            if army.army_id == game_stats.selected_army:
                approaching_army = army
                break
        if number not in game_stats.second_army_exchange_list:
            if number + 1 <= len(game_stats.reward_for_demonstration):
                if len(approaching_army.units) + len(game_stats.second_army_exchange_list) < 20:
                    game_stats.second_army_exchange_list.append(number)
        else:
            game_stats.second_army_exchange_list.remove(number)


def give_army_and_realm():
    the_army = None
    for army in game_obj.game_armies:
        if army.army_id == game_stats.selected_army:
            the_army = army
            break

    the_realm = None
    for realm in game_obj.game_powers:
        if realm.name == the_army.owner:
            the_realm = realm
            break

    return the_army, the_realm


def spread_reward(army, realm):
    for reward in game_stats.reward_for_demonstration:
        # Resources
        if reward[0] in resource_names:
            found = False
            bonus_quantity = 0
            # Check artifacts
            if len(army.hero.inventory) > 0:
                for artifact in army.hero.inventory:
                    for effect in artifact.effects:
                        if effect.application == "Resources bonus":
                            if reward[0] in effect.application_tags:
                                if effect.method == "addition":
                                    bonus_quantity += int(effect.quantity)
            if len(realm.coffers) > 0:
                for res in realm.coffers:
                    if res[0] == reward[0]:

                        res[1] += reward[1] + int(bonus_quantity)
                        found = True
                        break

            if not found:
                realm.coffers.append([str(reward[0]), int(reward[1]) + int(bonus_quantity)])

        # Artifacts
        elif reward[0] in artifact_imgs_cat.imgs_catalog:
            if len(army.hero.inventory) < 4:
                add_true = True
                if len(army.hero.inventory) > 0:
                    for artifact in army.hero.inventory:
                        if artifact.name == reward[0]:
                            add_true = False
                            break

                if add_true:
                    details = artifact_catalog.artifact_data[reward[0]]
                    army.hero.inventory.append(artifact_classes.Artifact(details[0],
                                                                         details[1],
                                                                         details[2],
                                                                         details[3],
                                                                         details[4]))

                    update_max_mana_reserve(army.hero)

                else:
                    details = artifact_catalog.artifact_data[reward[0]]
                    realm.artifact_collection.append(artifact_classes.Artifact(details[0],
                                                                               details[1],
                                                                               details[2],
                                                                               details[3],
                                                                               details[4]))

            else:
                details = artifact_catalog.artifact_data[reward[0]]
                realm.artifact_collection.append(artifact_classes.Artifact(details[0],
                                                                           details[1],
                                                                           details[2],
                                                                           details[3],
                                                                           details[4]))

    # Remove used reward
    for reward in game_obj.game_rewards:
        if reward[0] in realm.reward_IDs:
            realm.reward_IDs.remove(reward[0])
            game_obj.game_rewards.remove(reward)
            break


def update_max_mana_reserve(hero):
    total_knowledge = int(hero.knowledge)
    for artifact in hero.inventory:
        for effect in artifact.effects:
            if effect.application == "Knowledge":
                if effect.method == "addition":
                    total_knowledge += int(effect.quantity)

    hero.max_mana_reserve = 10 * total_knowledge


# Lair
def runaway_serfs_refuge_reward(army):
    game_stats.game_board_panel = "runaway serfs refuge result panel"
    game_stats.event_panel_det = game_classes.Object_Surface({1: runaway_serfs_refuge_result_close},
                                                             [[611, 406, 670, 426]],
                                                             [481, 101, 800, 430],
                                                             None)


def treasure_tower_reward(army):
    game_stats.game_board_panel = "treasure tower result panel"
    game_stats.event_panel_det = game_classes.Object_Surface({1: treasure_tower_result_close},
                                                             [[611, 406, 670, 426]],
                                                             [481, 101, 800, 430],
                                                             None)


def lair_of_grey_dragons_reward(army):
    game_stats.game_board_panel = "lair of grey dragons result panel"
    game_stats.event_panel_det = game_classes.Object_Surface({1: lair_of_grey_dragons_result_close},
                                                             [[611, 481, 670, 501]],
                                                             [481, 101, 800, 430],
                                                             lair_of_grey_dragons_result_acquire_regiments)


result_scripts = {
    # Lair
    "Runaway serfs refuge reward" : runaway_serfs_refuge_reward,
    "Treasure tower reward" : treasure_tower_reward,
    "Lair of grey dragons reward" : lair_of_grey_dragons_reward}
