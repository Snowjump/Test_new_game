## Miracle battles
## AI_battle_result_scripts

import copy

from Resources import artifact_classes
from Resources import game_basic

from Content import reward_catalog
from Content import artifact_catalog
from Content import artifact_imgs_cat

from Storage import create_unit


resource_names = ["Florins",
                  "Food",
                  "Wood"]


def runaway_serfs_refuge_reward(the_army, the_realm):
    reward_list = reward_catalog.reward_scripts["Runaway serfs refuge reward"](the_army)
    spread_reward(the_army, the_realm, list(reward_list[1]))


def treasure_tower_reward(the_army, the_realm):
    reward_list = reward_catalog.reward_scripts["Treasure tower reward"](the_army)
    spread_reward(the_army, the_realm, list(reward_list[1]))


def lair_of_grey_dragons_reward(the_army, the_realm):
    # AI will take new regiments if it has available capacity in its army
    reward_list = reward_catalog.reward_scripts["Lair of grey dragons reward"](the_army)
    recruit_new_regiments(the_army, list(reward_list[1]))


def spread_reward(army, realm, reward_list):
    for reward in reward_list:
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


def update_max_mana_reserve(hero):
    total_knowledge = int(hero.knowledge)
    for artifact in hero.inventory:
        for effect in artifact.effects:
            if effect.application == "Knowledge":
                if effect.method == "addition":
                    total_knowledge += int(effect.quantity)

    hero.max_mana_reserve = 10 * total_knowledge


def recruit_new_regiments(army, reward_list):
    for reward in reward_list:
        if reward[0] == "Regiment":
            if len(army.units) < 20:
                units_list = list(create_unit.LE_units_dict_by_alignment[reward[2]])
                for new_unit in units_list:
                    if new_unit.name == reward[1]:
                        army.units.append(copy.deepcopy(new_unit))
                        print("Added to army new unit - " + new_unit.name)
                        break
            else:
                break

    game_basic.establish_leader(army.army_id, "Game")


result_scripts = {
    # Lair
    "Runaway serfs refuge reward" : runaway_serfs_refuge_reward,
    "Treasure tower reward" : treasure_tower_reward,
    "Lair of grey dragons reward" : lair_of_grey_dragons_reward}
