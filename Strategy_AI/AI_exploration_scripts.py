## Miracle battles
## AI_exploration_scripts

import random

from Resources import game_obj
from Resources import game_basic
from Resources import game_autobattle

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

        mana_value = 0
        if mana_reserve + (max_mana / 2) > max_mana:
            mana_value = int(max_mana - mana_reserve)
        else:
            mana_value = int(max_mana / 2)

        army.hero.mana_reserve += int(mana_value)


def burial_mound_event(obj, army):
    if not obj.properties.need_replenishment:
        # AI player always takes an artifact
        artefact = [random.choice(["Bone wand", "Old dwarven chieftan's axe", "Grimcloud horde's staff",
                                   "Ancient elven sceptre", "Broken javelin"])]
        script_rewards = [artefact]

        the_realm = None
        for realm in game_obj.game_powers:
            if realm.name == army.owner:
                the_realm = realm
                break

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
            for realm in game_obj.game_powers:
                if realm.name == army.owner:
                    for res in realm.coffers:
                        if res[0] == "Florins":
                            # print("Florins - " + str(res[1]) + "; " + str(artifact_name) + " - " +
                            #       str(artifact_catalog.artifact_data[artifact_name][2]))
                            if res[1] <= 3000:
                                res[1] -= 3000

                                exploration_scripts.spread_reward(army, realm, obj.properties.storage)

                                obj.properties.storage = []
                                obj.properties.need_replenishment = True
                                obj.properties.time_left_before_replenishment = int(
                                    obj.properties.waiting_time_for_replenishment)

                                break

                    break


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
    # Lair
    "runaway serfs refuge script": runaway_serfs_refuge_event,
    "treasure tower script": treasure_tower_event,
    "lair of grey dragons script": lair_of_grey_dragons_event}
