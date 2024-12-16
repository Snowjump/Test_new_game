## Among Myth and Wonder
## AI_exploration_scripts

import random
import math

from Resources import game_obj
from Resources import game_basic
from Resources import game_classes
from Resources import game_autobattle
from Resources import common_selects
from Resources import common_transactions

from Content import exploration_scripts


# Bonus
def mythic_monolith_event(obj, army):
    if army.hero.hero_id not in obj.properties.hero_list:
        obj.properties.hero_list.append(int(army.hero.hero_id))
        game_basic.hero_next_level(army.hero, 1000)


def stone_circle_event(obj, army):
    if army.hero.hero_id not in obj.properties.hero_list:
        obj.properties.hero_list.append(int(army.hero.hero_id))
        army.hero.magic_power += 1


def scholars_tower_event(obj, army):
    if army.hero.hero_id not in obj.properties.hero_list:
        obj.properties.hero_list.append(int(army.hero.hero_id))
        army.hero.knowledge += 1
        army.hero.max_mana_reserve += 10
        army.hero.mana_reserve += 10


def stone_well_event(obj, army):
    if army.hero.hero_id not in obj.properties.hero_list:
        obj.properties.hero_list.append(int(army.hero.hero_id))
        max_mana = int(10 * army.hero.knowledge)
        mana_reserve = int(army.hero.mana_reserve)

        mana_value = int(max_mana / 2)
        if mana_reserve + (max_mana / 2) > max_mana:
            mana_value = int(max_mana - mana_reserve)

        army.hero.mana_reserve += int(mana_value)


def burial_mound_event(obj, army):
    if not obj.properties.need_replenishment:
        # AI player always takes an artifact
        artefact = [random.choice(["Bone wand", "Old dwarven chieftan's axe", "Grimcloud horde's staff",
                                   "Ancient elven sceptre", "Broken javelin"])]
        script_rewards = [artefact]

        the_realm = common_selects.select_realm_by_name(army.owner)

        exploration_scripts.spread_reward(army, the_realm, script_rewards)

        obj.properties.need_replenishment = True
        obj.properties.time_left_before_replenishment = int(obj.properties.waiting_time_for_replenishment)


def anglers_cabin_event(obj, army):
    if not obj.properties.need_replenishment:
        # AI player has 25% chance to buy an artifact
        if len(obj.properties.storage) == 0:
            # ["Composite bow", "Elven crown", "Forgotten mask", "Hat of grand wizard", "Champion's sword"]
            obj.properties.storage.append([random.choice(["Composite bow", "Elven crown", "Forgotten mask",
                                                          "Hat of grand wizard", "Champion's sword"])])

        buy_artifact = False
        # Inventory not full
        if len(army.hero.inventory) < 4:
            if random.randint(0, 100) <= 25:
                buy_artifact = True

        print("buy_artifact = " + str(buy_artifact))
        if buy_artifact:
            for artifact in army.hero.inventory:
                if artifact.name == obj.properties.storage[0]:
                    buy_artifact = False
                    break

        if buy_artifact:
            realm = common_selects.select_realm_by_name(army.owner)
            price = [["Florins", 3000]]
            if common_transactions.sufficient_funds(price, realm):
                common_transactions.payment(price, realm)

                exploration_scripts.spread_reward(army, realm, obj.properties.storage)

                obj.properties.storage = []
                obj.properties.need_replenishment = True
                obj.properties.time_left_before_replenishment = int(obj.properties.waiting_time_for_replenishment)


def champions_tent_event(obj, army):
    if army.hero.hero_id not in obj.properties.hero_list:
        obj.properties.hero_list.append(int(army.hero.hero_id))
        pack = game_classes.Attribute_Package([game_classes.Battle_Attribute(
            "melee cavalry",
            "defence",
            1)])
        army.hero.attributes_list.append(pack)

        if army.hero.hero_class == "Knight":
            game_basic.hero_next_level(army.hero, 500)


def leshys_hut_event(obj, army):
    result = int(random.randint(1, 6))

    if result == 6:
        # Magic power
        army.hero.magic_power += 1
    elif result == 5:
        # Food and wood
        # print("leshys_hut_close() - Food and wood reward number 5")
        reward = [["Food", 500], ["Wood", 1000]]
        realm = common_selects.select_realm_by_name(army.owner)
        exploration_scripts.spread_reward(army, realm, reward)
    elif result == 4:
        # Additional movement points
        for unit in army.units:
            unit.movement_points += 800
    elif result == 3:
        # Drain mana
        army.hero.mana_reserve = 0
    elif result == 2:
        # Lose money
        price = [["Florins", 1500]]
        realm = common_selects.select_realm_by_name(army.owner)
        common_transactions.payment(price, realm)
    elif result == 1:
        # Lose regiments
        units_to_destroy = math.ceil(len(army.units)/8)
        index_list = []
        units_numbered_list = []
        for i in range(0, len(army.units)):
            units_numbered_list.append(i)
        for i in range(1, units_to_destroy + 1):
            index_list.append(units_numbered_list.pop(random.choice(units_numbered_list)))
        game_basic.disband_unit(army, index_list)

    obj.properties.need_replenishment = True
    obj.properties.time_left_before_replenishment = int(random.randint(15, 25))


# Lair
def runaway_serfs_refuge_event(obj, army):
    if not obj.properties.need_replenishment:
        obj.properties.need_replenishment = True
        obj.properties.time_left_before_replenishment = int(obj.properties.waiting_time_for_replenishment)

    defender = None
    # print("len(game_obj.game_armies) - " + str(len(game_obj.game_armies)))
    for other_army in game_obj.game_armies:
        # print("army_id - " + str(other_army.army_id) + "; owner - " + str(other_army.owner))
        if other_army.army_id == obj.properties.army_id:
            defender = other_army
            break

    game_autobattle.begin_battle(army, defender, "special", "Runaway serfs refuge reward")


def treasure_tower_event(obj, army):
    if not obj.properties.need_replenishment:
        obj.properties.need_replenishment = True
        obj.properties.time_left_before_replenishment = int(obj.properties.waiting_time_for_replenishment)

    defender = None
    # print("len(game_obj.game_armies) - " + str(len(game_obj.game_armies)))
    for other_army in game_obj.game_armies:
        # print("army_id - " + str(other_army.army_id) + "; owner - " + str(other_army.owner))
        if other_army.army_id == obj.properties.army_id:
            defender = other_army
            break

    game_autobattle.begin_battle(army, defender, "special", "Treasure tower reward")


def lair_of_grey_dragons_event(obj, army):
    if not obj.properties.need_replenishment:
        obj.properties.need_replenishment = True
        obj.properties.time_left_before_replenishment = int(obj.properties.waiting_time_for_replenishment)

    defender = None
    # print("len(game_obj.game_armies) - " + str(len(game_obj.game_armies)))
    for other_army in game_obj.game_armies:
        # print("army_id - " + str(other_army.army_id) + "; owner - " + str(other_army.owner))
        if other_army.army_id == obj.properties.army_id:
            defender = other_army
            break

    game_autobattle.begin_battle(army, defender, "special", "Lair of grey dragons reward")


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
