## Among Myth and Wonder
## exploration_scripts

import pygame
import random
import math

from Resources import game_stats
from Resources import game_classes
from Resources import artifact_classes
from Resources import game_obj
from Resources import game_basic
from Resources import common_selects
from Resources import common_transactions
from Resources import graphics_basic

from Content import artifact_imgs_cat
from Content import artifact_catalog


resource_names = ["Florins",
                  "Food",
                  "Wood"]


def mythic_monolith_close():
    army = common_selects.select_army_by_id(game_stats.selected_army)
    # army.hero.experience += 1000
    game_basic.hero_next_level(army.hero, 1000)

    game_stats.game_board_panel = ""
    game_stats.event_panel_det = None


def stone_circle_close():
    army = common_selects.select_army_by_id(game_stats.selected_army)
    army.hero.magic_power += 1

    game_stats.game_board_panel = ""
    game_stats.event_panel_det = None


def scholars_tower_close():
    army = common_selects.select_army_by_id(game_stats.selected_army)
    army.hero.knowledge += 1
    army.hero.max_mana_reserve += 10
    army.hero.mana_reserve += 10

    game_stats.game_board_panel = ""
    game_stats.event_panel_det = None


def stone_well_close():
    army = common_selects.select_army_by_id(game_stats.selected_army)
    max_mana = int(10 * army.hero.knowledge)
    mana_reserve = int(army.hero.mana_reserve)

    mana_value = 0
    if mana_reserve + (max_mana / 2) > max_mana:
        mana_value = int(max_mana - mana_reserve)
    else:
        mana_value = int(max_mana / 2)

    army.hero.mana_reserve += int(mana_value)

    game_stats.game_board_panel = ""
    game_stats.event_panel_det = None


def burial_mound_excavate():
    # ["Bone wand", "Old dwarven chieftan's axe", "Grimcloud horde's staff", "Ancient elven sceptre", "Broken javelin"]
    artefact = [random.choice(["Bone wand", "Old dwarven chieftan's axe", "Grimcloud horde's staff",
                               "Ancient elven sceptre", "Broken javelin"])]
    script_rewards = [artefact]

    the_army, the_realm = give_army_and_realm()
    spread_reward(the_army, the_realm, script_rewards)
    
    lot = game_obj.game_map[the_army.location].lot
    lot.properties.need_replenishment = True
    lot.properties.time_left_before_replenishment = int(lot.properties.waiting_time_for_replenishment)

    game_stats.game_board_panel = ""
    game_stats.event_panel_det = None


def burial_mound_close():
    game_stats.game_board_panel = ""
    game_stats.event_panel_det = None


def anglers_cabin_obtain_artifact():
    print("anglers_cabin_obtain_artifact")
    the_army, the_realm = give_army_and_realm()
    lot = game_obj.game_map[the_army.location].lot

    # enough_money = False
    # if len(the_realm.coffers) > 0:
    #     for res in the_realm.coffers:
    #         if res[0] == "Florins":
    #             if res[1] >= 3000:
    #                 res[1] -= 3000
    #                 enough_money = True
    #             break
    price = [["Florins", 3000]]

    if common_transactions.sufficient_funds(price, the_realm):
        common_transactions.payment(price, the_realm)
        spread_reward(the_army, the_realm, lot.properties.storage)

        lot.properties.storage = []
        lot.properties.need_replenishment = True
        lot.properties.time_left_before_replenishment = int(lot.properties.waiting_time_for_replenishment)

        game_stats.game_board_panel = ""
        game_stats.event_panel_det = None


def anglers_cabin_close():
    game_stats.game_board_panel = ""
    game_stats.event_panel_det = None


def champions_tent_close():
    army = common_selects.select_army_by_id(game_stats.selected_army)
    pack = game_classes.Attribute_Package([game_classes.Battle_Attribute(
        "melee cavalry",
        "defence",
        1)])
    army.hero.attributes_list.append(pack)
    if army.hero.hero_class == "Knight":
        game_basic.hero_next_level(army.hero, 500)

    game_stats.game_board_panel = ""
    game_stats.event_panel_det = None


def leshys_hut_play_dice():
    game_stats.game_board_panel = "leshy's hut dice results event panel"
    game_stats.event_panel_det = game_classes.Object_Surface({1: leshys_hut_close},
                                                             [[611, 421, 670, 441]],
                                                             [481, 101, 800, 445],
                                                             None)

    result = int(random.randint(1, 6))
    # result = 1
    army = common_selects.select_army_by_id(game_stats.selected_army)
    lot = game_obj.game_map[army.location].lot
    lot.properties.storage.append(result)


def leshys_hut_leave():
    # If player rejects to play dice with Leshy
    game_stats.game_board_panel = ""
    game_stats.event_panel_det = None


def leshys_hut_close():
    # After the game of dice, player could leave Leshy's hut
    the_army, the_realm = give_army_and_realm()

    lot = game_obj.game_map[the_army.location].lot

    if lot.properties.storage[0] == 6:
        # Magic power
        the_army.hero.magic_power += 1
    elif lot.properties.storage[0] == 5:
        # Food and wood
        print("leshys_hut_close() - Food and wood reward number 5")
        reward = [["Food", 500], ["Wood", 1000]]
        spread_reward(the_army, the_realm, reward)
    elif lot.properties.storage[0] == 4:
        # Additional movement points
        for unit in the_army.units:
            unit.movement_points += 800
    elif lot.properties.storage[0] == 3:
        # Drain mana
        the_army.hero.mana_reserve = 0
    elif lot.properties.storage[0] == 2:
        # Lose money
        price = [["Florins", 1500]]
        common_transactions.payment(price, the_realm)
    elif lot.properties.storage[0] == 1:
        # Lose regiments
        units_to_destroy = math.ceil(len(the_army.units)/8)
        index_list = []
        units_numbered_list = []
        for i in range(0, len(the_army.units)):
            units_numbered_list.append(i)
        for i in range(1, units_to_destroy + 1):
            index_list.append(units_numbered_list.pop(random.choice(units_numbered_list)))
        game_basic.disband_unit(the_army, index_list)

    lot.properties.need_replenishment = True
    lot.properties.time_left_before_replenishment = int(random.randint(15, 25))
    lot.properties.storage = []

    game_stats.game_board_panel = ""
    game_stats.event_panel_det = None


# Lair
def runaway_serfs_refuge_retreat():
    game_stats.game_board_panel = ""
    game_stats.event_panel_det = None


def treasure_tower_retreat():
    game_stats.game_board_panel = ""
    game_stats.event_panel_det = None


def lair_of_grey_dragons_retreat():
    game_stats.game_board_panel = ""
    game_stats.event_panel_det = None


def runaway_serfs_refuge_fight():
    at_army, df_army, TileObj = battle_information()

    if not TileObj.lot.properties.need_replenishment:
        TileObj.lot.properties.need_replenishment = True
        TileObj.lot.properties.time_left_before_replenishment = int(
            TileObj.lot.properties.waiting_time_for_replenishment)

    game_stats.game_board_panel = ""
    game_stats.event_panel_det = None

    game_stats.battle_result_script = "Runaway serfs refuge reward"
    game_basic.engage_army(at_army, df_army, TileObj.terrain, TileObj.conditions, "Lair")


def treasure_tower_fight():
    at_army, df_army, TileObj = battle_information()

    if not TileObj.lot.properties.need_replenishment:
        TileObj.lot.properties.need_replenishment = True
        TileObj.lot.properties.time_left_before_replenishment = int(
            TileObj.lot.properties.waiting_time_for_replenishment)

    game_stats.game_board_panel = ""
    game_stats.event_panel_det = None

    game_stats.battle_result_script = "Treasure tower reward"
    game_basic.engage_army(at_army, df_army, TileObj.terrain, TileObj.conditions, "Lair")


def lair_of_grey_dragons_fight():
    at_army, df_army, TileObj = battle_information()

    if not TileObj.lot.properties.need_replenishment:
        TileObj.lot.properties.need_replenishment = True
        TileObj.lot.properties.time_left_before_replenishment = int(
            TileObj.lot.properties.waiting_time_for_replenishment)

    game_stats.game_board_panel = ""
    game_stats.event_panel_det = None

    game_stats.battle_result_script = "Lair of grey dragons reward"
    game_basic.engage_army(at_army, df_army, TileObj.terrain, TileObj.conditions, "Lair")


# Bonus
def mythic_monolith_event(obj, army):
    if army.hero.hero_id not in obj.properties.hero_list:
        obj.properties.hero_list.append(int(army.hero.hero_id))
        game_stats.game_board_panel = "mythic monolith event panel"
        game_stats.event_panel_det = game_classes.Object_Surface({1: mythic_monolith_close},
                                                                 [[611, 376, 670, 396]],
                                                                 [481, 101, 800, 400],
                                                                 None)


def stone_circle_event(obj, army):
    if army.hero.hero_id not in obj.properties.hero_list:
        obj.properties.hero_list.append(int(army.hero.hero_id))
        game_stats.game_board_panel = "stone circle event panel"
        game_stats.event_panel_det = game_classes.Object_Surface({1: stone_circle_close},
                                                                 [[611, 406, 670, 426]],
                                                                 [481, 101, 800, 430],
                                                                 None)


def scholars_tower_event(obj, army):
    if army.hero.hero_id not in obj.properties.hero_list:
        obj.properties.hero_list.append(int(army.hero.hero_id))
        game_stats.game_board_panel = "scholar's tower event panel"
        game_stats.event_panel_det = game_classes.Object_Surface({1: scholars_tower_close},
                                                                 [[611, 406, 670, 426]],
                                                                 [481, 101, 800, 430],
                                                                 None)


def stone_well_event(obj, army):
    if army.hero.hero_id not in obj.properties.hero_list:
        obj.properties.hero_list.append(int(army.hero.hero_id))
        game_stats.game_board_panel = "stone well event panel"
        game_stats.event_panel_det = game_classes.Object_Surface({1: stone_well_close},
                                                                 [[611, 376, 670, 396]],
                                                                 [481, 101, 800, 400],
                                                                 None)


def burial_mound_event(obj, army):
    game_stats.game_board_panel = "burial mound event panel"
    # game_stats.selected_object = obj
    if not obj.properties.need_replenishment:
        game_stats.event_panel_det = game_classes.Object_Surface({1: burial_mound_excavate,
                                                                  2: burial_mound_close},
                                                                 [[561, 406, 620, 426],
                                                                  [661, 406, 720, 426]],
                                                                 [481, 101, 800, 400],
                                                                 None)
    else:
        game_stats.event_panel_det = game_classes.Object_Surface({1: burial_mound_close},
                                                                 [[611, 376, 670, 396]],
                                                                 [481, 101, 800, 400],
                                                                 None)

    click_sound = pygame.mixer.Sound("Sound/Exploration/Just_Transitions_Creepy-259.wav")
    click_sound.play()


def anglers_cabin_event(obj, army):
    if not obj.properties.need_replenishment:
        if len(obj.properties.storage) == 0:
            # ["Composite bow", "Elven crown", "Forgotten mask", "Hat of grand wizard", "Champion's sword"]
            obj.properties.storage.append([random.choice(["Composite bow", "Elven crown", "Forgotten mask",
                                                          "Hat of grand wizard", "Champion's sword"])])
        game_stats.game_board_panel = "angler's cabin event panel"
        game_stats.event_panel_det = game_classes.Object_Surface({1: anglers_cabin_obtain_artifact,
                                                                  2: anglers_cabin_close},
                                                                 [[561, 436, 620, 456],
                                                                  [661, 436, 720, 456]],
                                                                 [481, 101, 800, 400],
                                                                 None)


def champions_tent_event(obj, army):
    if army.hero.hero_id not in obj.properties.hero_list:
        obj.properties.hero_list.append(int(army.hero.hero_id))
        game_stats.game_board_panel = "champion's tent event panel"
        game_stats.event_panel_det = game_classes.Object_Surface({1: champions_tent_close},
                                                                 [[611, 421, 670, 441]],
                                                                 [481, 101, 800, 445],
                                                                 None)


def leshys_hut_event(obj, army):
    if not obj.properties.need_replenishment:
        game_stats.game_board_panel = "leshy's hut event panel"
        game_stats.event_panel_det = game_classes.Object_Surface({1: leshys_hut_play_dice,
                                                                  2: leshys_hut_leave},
                                                                 [[561, 321, 620, 341],
                                                                  [661, 321, 720, 341]],
                                                                 [481, 101, 800, 345],
                                                                 None)


# Lair
def runaway_serfs_refuge_event(obj, army):
    print("army_id - " + str(obj.properties.army_id))
    if obj.properties.army_id is not None:
        game_stats.game_board_panel = "runaway serfs refuge event panel"
        game_stats.event_panel_det = game_classes.Object_Surface({1: runaway_serfs_refuge_fight,
                                                                  2: runaway_serfs_refuge_retreat},
                                                                 [[561, 406, 620, 426],
                                                                  [661, 406, 720, 426]],
                                                                 [481, 101, 800, 430],
                                                                 None)


def treasure_tower_event(obj, army):
    print("army_id - " + str(obj.properties.army_id))
    if obj.properties.army_id is not None:
        game_stats.game_board_panel = "treasure tower event panel"
        game_stats.event_panel_det = game_classes.Object_Surface({1: treasure_tower_fight,
                                                                  2: treasure_tower_retreat},
                                                                 [[561, 406, 620, 426],
                                                                  [661, 406, 720, 426]],
                                                                 [481, 101, 800, 430],
                                                                 None)


def lair_of_grey_dragons_event(obj, army):
    print("army_id - " + str(obj.properties.army_id))
    if obj.properties.army_id is not None:
        game_stats.game_board_panel = "lair of grey dragons event panel"
        game_stats.event_panel_det = game_classes.Object_Surface({1: lair_of_grey_dragons_fight,
                                                                  2: lair_of_grey_dragons_retreat},
                                                                 [[561, 406, 620, 426],
                                                                  [661, 406, 720, 426]],
                                                                 [481, 101, 800, 430],
                                                                 None)


# Support functions

def battle_information():
    at_army = None  # Attacking army
    for army in game_obj.game_armies:
        if army.army_id == game_stats.selected_army:
            at_army = army
            break

    TileObj = game_obj.game_map[at_army.location]

    df_army = None  # Defending army
    for army in game_obj.game_armies:
        if army.army_id == TileObj.lot.properties.army_id:
            df_army = army
            break

    return at_army, df_army, TileObj


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


def spread_reward(army, realm, script_rewards):
    for reward in script_rewards:
        print(str(reward[0]))
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
                    # print("Coffers: " + str(res))
                    if res[0] == reward[0]:
                        res[1] += reward[1] + int(bonus_quantity)
                        found = True
                        break

            if not found:
                realm.coffers.append([str(reward[0]), int(reward[1]) + int(bonus_quantity)])

            if realm.name == game_stats.player_power:
                graphics_basic.prepare_resource_ribbon()

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


event_scripts = {  # Bonus
    "mythic monolith script": mythic_monolith_event,
    "stone circle script": stone_circle_event,
    "scholar's tower script": scholars_tower_event,
    "stone well script": stone_well_event,
    "burial mound script" : burial_mound_event,
    "angler's cabin script" : anglers_cabin_event,
    "champion's tent script" : champions_tent_event,
    "leshy's hut script" : leshys_hut_event,
    # Lair
    "runaway serfs refuge script": runaway_serfs_refuge_event,
    "treasure tower script": treasure_tower_event,
    "lair of grey dragons script": lair_of_grey_dragons_event}
