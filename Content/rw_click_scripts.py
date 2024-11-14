## Among Myth and Wonder
## rw_click_scripts

import math
import random

from Resources import game_stats
from Resources import game_basic
from Resources import game_classes
from Resources import skill_classes
from Resources import artifact_classes
from Resources import game_obj
from Resources import update_gf_game_board

from Content import battle_attributes_catalog
from Content import hero_skill_catalog
from Content import skill_weights
from Content import artifact_assortment
from Content import artifact_catalog
from Content import skills_curriculum


def hero_skills(position):
    yVar = game_stats.game_window_height - 800
    zone = [864, 271, 1278, 540]
    print("hero_skills")

    if 864 < position[0] < 1040 and 271 < position[1] < 540:
        if position[0] <= 1040:
            x_axis, y_axis = position[0], position[1]
            x_axis -= 863
            y_axis -= 270
            print(str(x_axis) + ", " + str(y_axis))
            # print(str(x_axis % 45) + ", " + str(y_axis % 45))
            # Click on existing skill or perk to show information about it
            if (x_axis % 45) <= 42 and (y_axis % 45) <= 42:
                x_axis = math.ceil(x_axis / 45)
                y_axis = math.ceil(y_axis / 45)
                print(str(x_axis) + ", " + str(y_axis))

                # game_stats.selected_skill_info = game_stats.rw_object.skills[y_axis - 1]
                for skill in game_stats.rw_object.skills:
                    if skill.screen_position == [x_axis - 1, y_axis - 1]:
                        game_stats.selected_skill_info = skill
                        break

    elif 1041 < position[0] < 1130 and 515 < position[1] < 535:
        print("new skills")
        # New skills button
        if game_stats.rw_object.new_skill_points > 0:
            if len(game_stats.rw_object.new_skills) == 0:
                # Prepare new skills and perks
                upgrade_skill_list = []
                for skill in game_stats.rw_object.skills:
                    if skill.skill_type == "Skill" and skill.skill_level != "Expert":
                        upgrade_skill_list.append(str(skill.next_level))

                if len(upgrade_skill_list) > 0:
                    game_stats.rw_object.new_skills.append(random.choice(upgrade_skill_list))

                print("guaranteed_perk_list")
                guaranteed_perk_list = []
                for skill in hero_skill_catalog.hero_skill_data:
                    # print("Checking " + str(skill))
                    if hero_skill_catalog.hero_skill_data[skill][1] == "Perk":
                        # print("Found perk - " + str(skill))
                        all_there = True
                        for requisite in hero_skill_catalog.hero_skill_data[skill][6]:
                            found = False
                            for available in game_stats.rw_object.skills:
                                if requisite in available.tags:
                                    found = True

                            if not found:
                                all_there = False

                        if all_there:
                            perk_capacity = 0
                            learned_perks = 0
                            for skill2 in game_stats.rw_object.skills:
                                if skill2.skill_type == "Skill" and skill2.theme == hero_skill_catalog.hero_skill_data[skill][4]:
                                    if skill2.skill_level == "Basic":
                                        perk_capacity = 1
                                    elif skill2.skill_level == "Advanced":
                                        perk_capacity = 2
                                    else:
                                        perk_capacity = 3

                                elif skill2.skill_type == "Perk" and skill2.theme == hero_skill_catalog.hero_skill_data[skill][4]:
                                    learned_perks += 1

                            if learned_perks < perk_capacity:
                                guaranteed_perk_list.append(str(skill))

                if len(guaranteed_perk_list) > 0:
                    print(str(guaranteed_perk_list))
                    game_stats.rw_object.new_skills.append(random.choice(guaranteed_perk_list))

                print("third_skill_list")
                third_skill_list = []
                for skill in game_stats.rw_object.skills:
                    if skill.skill_type == "Skill" and skill.skill_level != "Expert":
                        if skill.next_level not in game_stats.rw_object.new_skills:
                            third_skill_list.append(str(skill.next_level))

                for skill in hero_skill_catalog.hero_skill_data:
                    n_skill = hero_skill_catalog.hero_skill_data[skill]
                    if n_skill[1] == "Skill" and n_skill[3] == "Basic":
                        not_in_skills = True
                        for old_skill in game_stats.rw_object.skills:
                            if skill in old_skill.tags:
                                not_in_skills = False

                        if skill not in game_stats.rw_object.new_skills and not_in_skills:
                            third_skill_list.append(str(skill))

                    elif n_skill[1] == "Perk":
                        not_in_skills = True
                        complete_requisites = True
                        for old_perk in game_stats.rw_object.skills:
                            if skill == old_perk.name:
                                not_in_skills = False

                        for requisite in n_skill[6]:
                            found = False
                            for old_skill in game_stats.rw_object.skills:
                                if requisite in old_skill.tags:
                                    found = True

                            if not found:
                                complete_requisites = False

                        if skill not in game_stats.rw_object.new_skills and not_in_skills and complete_requisites:
                            perk_capacity = 0
                            learned_perks = 0
                            for skill2 in game_stats.rw_object.skills:
                                if skill2.skill_type == "Skill" and skill2.theme == \
                                        hero_skill_catalog.hero_skill_data[skill][4]:
                                    if skill2.skill_level == "Basic":
                                        perk_capacity = 1
                                    elif skill2.skill_level == "Advanced":
                                        perk_capacity = 2
                                    else:
                                        perk_capacity = 3

                                elif skill2.skill_type == "Perk" and skill2.theme == \
                                        hero_skill_catalog.hero_skill_data[skill][4]:
                                    learned_perks += 1

                            if learned_perks < perk_capacity:
                                third_skill_list.append(str(skill))

                if len(third_skill_list) > 0:
                    print(str(third_skill_list))
                    weights_list = []
                    for skill in third_skill_list:
                        weights_list.append(int(skill_weights.class_cat[game_stats.rw_object.hero_class][skill]))
                    print(str(weights_list))
                    third_skill = random.choices(third_skill_list, weights=weights_list)
                    print(str(third_skill))
                    game_stats.rw_object.new_skills.append(str(third_skill[0]))
                    print(str(game_stats.rw_object.new_skills))

                print("fourth_skill_list")
                fourth_skill_list = []
                for skill in game_stats.rw_object.skills:
                    if skill.skill_type == "Skill" and skill.skill_level != "Expert":
                        if skill.next_level not in game_stats.rw_object.new_skills:
                            fourth_skill_list.append(str(skill.next_level))

                for skill in hero_skill_catalog.hero_skill_data:
                    n_skill = hero_skill_catalog.hero_skill_data[skill]
                    if n_skill[1] == "Skill" and n_skill[3] == "Basic":
                        not_in_skills = True
                        for old_skill in game_stats.rw_object.skills:
                            if skill in old_skill.tags:
                                not_in_skills = False

                        if skill not in game_stats.rw_object.new_skills and not_in_skills:
                            fourth_skill_list.append(str(skill))

                    elif n_skill[1] == "Perk":
                        not_in_skills = True
                        complete_requisites = True
                        for old_perk in game_stats.rw_object.skills:
                            if skill == old_perk.name:
                                not_in_skills = False

                        for requisite in n_skill[6]:
                            found = False
                            for old_skill in game_stats.rw_object.skills:
                                if requisite in old_skill.tags:
                                    found = True

                            if not found:
                                complete_requisites = False

                        if skill not in game_stats.rw_object.new_skills and not_in_skills and complete_requisites:
                            perk_capacity = 0
                            learned_perks = 0
                            for skill2 in game_stats.rw_object.skills:
                                if skill2.skill_type == "Skill" and skill2.theme == \
                                        hero_skill_catalog.hero_skill_data[skill][4]:
                                    if skill2.skill_level == "Basic":
                                        perk_capacity = 1
                                    elif skill2.skill_level == "Advanced":
                                        perk_capacity = 2
                                    else:
                                        perk_capacity = 3

                                elif skill2.skill_type == "Perk" and skill2.theme == \
                                        hero_skill_catalog.hero_skill_data[skill][4]:
                                    learned_perks += 1

                            if learned_perks < perk_capacity:
                                fourth_skill_list.append(str(skill))

                if len(fourth_skill_list) > 0:
                    print(str(fourth_skill_list))
                    weights_list = []
                    for skill in fourth_skill_list:
                        weights_list.append(int(skill_weights.class_cat[game_stats.rw_object.hero_class][skill]))
                    print(str(weights_list))
                    fourth_skill = random.choices(fourth_skill_list, weights=weights_list)
                    print(str(fourth_skill))
                    game_stats.rw_object.new_skills.append(str(fourth_skill[0]))
                    print(str(game_stats.rw_object.new_skills))

            game_stats.hero_information_option = "New skills"
            game_stats.rw_panel_det = game_classes.Object_Surface({},
                                                                  [],
                                                                  None,
                                                                  hero_new_skills)

            # Update visuals
            update_gf_game_board.update_skills_sprites()


def hero_attributes(position):
    zone = [864, 271, 1278, 540]
    print("hero_attributes")

    if 863 < position[0] < 1066 and 292 < position[1] < 515:
        x_axis, y_axis = position[0], position[1]
        x_axis -= 863
        y_axis -= 292
        print(str(x_axis) + ", " + str(y_axis))

        starting = 1
        ending = 19
        y = 0
        for pack in battle_attributes_catalog.basic_heroes_attributes[game_stats.rw_object.hero_class][
            game_stats.skill_tree_level_index - 1]:
            length = len(pack.attribute_list) - 1
            starting = 1 + y * 20 + length * 20
            ending = 19 + y * 20 + length * 20
            if starting <= y_axis <= ending:
                result = y
                print("result - " + str(result))
                game_stats.selected_new_attribute = int(result)
                break

            y += 1

    elif 1001 < position[0] < 1130 and 515 < position[1] < 535:
        print("confirm selection")
        pack = battle_attributes_catalog.basic_heroes_attributes[game_stats.rw_object.hero_class][
            game_stats.skill_tree_level_index - 1][game_stats.selected_new_attribute]

        # Increase knowledge and magic power of hero if needed
        for attribute in pack.attribute_list:
            if attribute.tag == "hero":
                if attribute.stat == "magic power":
                    game_stats.rw_object.magic_power += int(attribute.value)
                elif attribute.stat == "knowledge":
                    game_stats.rw_object.knowledge += int(attribute.value)
                    game_stats.rw_object.max_mana_reserve += int(attribute.value * 10)
                    game_stats.rw_object.mana_reserve += int(attribute.value * 10)

        game_stats.rw_object.attributes_list.append(pack)
        game_stats.rw_object.attribute_points_used += 1
        game_stats.rw_object.new_attribute_points -= 1
        game_stats.selected_new_attribute = None
        if game_stats.skill_tree_level_index == 5:
            pass
        else:
            game_stats.skill_tree_level_index += 1


def hero_new_skills(position):
    if 864 < position[0] < 1040 and 291 < position[1] < 515:
        if position[0] <= 1040:
            x_axis, y_axis = position[0], position[1]
            x_axis -= 863
            y_axis -= 290
            print(str(x_axis) + ", " + str(y_axis))
            # print(str(x_axis % 45) + ", " + str(y_axis % 45))
            if (x_axis % 45) <= 42 and (y_axis % 45) <= 42:
                x_axis = math.ceil(x_axis / 45)
                y_axis = math.ceil(y_axis / 45)
                print(str(x_axis) + ", " + str(y_axis))

                game_stats.selected_new_skill = game_stats.rw_object.new_skills[y_axis - 1]

    elif 1001 < position[0] < 1130 and 515 < position[1] < 535:
        print("confirm selection")

        new_skill = hero_skill_catalog.hero_skill_data[game_stats.selected_new_skill]

        replace_with = None
        if new_skill[3] == "Advanced" or new_skill[3] == "Expert":
            num = 0
            for old_skill in game_stats.rw_object.skills:
                if old_skill.next_level == game_stats.selected_new_skill:
                    replace_with = int(num)
                    break
                num += 1

        if replace_with is not None:
            position = list(game_stats.rw_object.skills[replace_with].screen_position)
            game_stats.rw_object.skills[replace_with] = (skill_classes.Hero_Skill(str(game_stats.selected_new_skill),
                                                                                  str(new_skill[0]),
                                                                                  str(new_skill[1]),
                                                                                  str(new_skill[2]),
                                                                                  str(new_skill[3]),
                                                                                  str(new_skill[4]),
                                                                                  list(new_skill[5]),
                                                                                  list(new_skill[6]),
                                                                                  new_skill[7],
                                                                                  position))

            game_basic.learn_new_abilities(game_stats.selected_new_skill, game_stats.rw_object)

        else:
            position = []
            if new_skill[1] == "Skill":
                counting = 0
                for skill in game_stats.rw_object.skills:
                    if skill.skill_type == "Skill":
                        counting += 1

                position = [0, int(counting)]

            else:
                counting = 0
                still_counting = True
                perks = 1
                for skill in game_stats.rw_object.skills:
                    if skill.skill_type == "Skill":
                        if skill.theme == new_skill[4]:
                            still_counting = False
                        else:
                            if still_counting:
                                counting += 1

                    else:
                        if skill.theme == new_skill[4]:
                            perks += 1

                position = [int(perks), int(counting)]

            game_stats.rw_object.skills.append(skill_classes.Hero_Skill(str(game_stats.selected_new_skill),
                                                                        str(new_skill[0]),
                                                                        str(new_skill[1]),
                                                                        str(new_skill[2]),
                                                                        str(new_skill[3]),
                                                                        str(new_skill[4]),
                                                                        list(new_skill[5]),
                                                                        list(new_skill[6]),
                                                                        new_skill[7],
                                                                        position))

            game_basic.learn_new_abilities(game_stats.selected_new_skill, game_stats.rw_object)

        game_stats.selected_new_skill = None
        game_stats.rw_object.new_skills = []
        game_stats.rw_object.new_skill_points -= 1
        game_stats.hero_information_option = "Skills"
        game_stats.selected_skill_info = None
        game_stats.rw_panel_det = game_classes.Object_Surface({},
                                                              [],
                                                              None,
                                                              hero_skills)


def hero_inventory(position):
    if 864 < position[0] < 1040 and 271 < position[1] < 540:
        if position[0] <= 1060:
            # Hero's inventory
            if 290 < position[1] <= 332:
                x_axis, y_axis = position[0], position[1]
                x_axis -= 863
                y_axis -= 290
                print(str(x_axis) + ", " + str(y_axis))

                if (x_axis % 45) <= 42:
                    x_axis = math.ceil(x_axis / 45)
                    print("x_axis - " + str(x_axis))
                    if x_axis <= len(game_stats.rw_object.inventory):
                        game_stats.selected_artifact_info = game_stats.rw_object.inventory[x_axis - 1]
                        game_stats.artifact_focus = "Hero's inventory"

            # Realm's artifact collection
            elif 355 < position[1] <= 397:
                x_axis, y_axis = position[0], position[1]
                x_axis -= 863
                y_axis -= 290
                print(str(x_axis) + ", " + str(y_axis))

                if (x_axis % 45) <= 42:
                    x_axis = math.ceil(x_axis / 45)
                    print("x_axis - " + str(x_axis))
                    if x_axis <= len(game_stats.realm_artifact_collection):
                        game_stats.selected_artifact_info = game_stats.realm_artifact_collection[x_axis - 1]
                        game_stats.artifact_focus = "Realm's artifact collection"


def artifact_market(position):
    if 650 < position[0] < 920 and 148 < position[1] < 190:
        x_axis, y_axis = position[0], position[1]
        x_axis -= 650
        y_axis -= 148
        print(str(x_axis) + ", " + str(y_axis))
        if (x_axis % 45) <= 42:
            x_axis = math.ceil(x_axis / 45)
            print("x_axis - " + str(x_axis))

            # structure = special_structures[game_stats.rw_object.name]
            structure = game_stats.rw_object.name

            if x_axis <= len(artifact_assortment.stock_by_place[structure]):
                game_stats.artifact_focus = None
                artifact_name = artifact_assortment.stock_by_place[structure][x_axis - 1]
                details = artifact_catalog.artifact_data[artifact_name]
                game_stats.selected_artifact_info = artifact_classes.Artifact(details[0],
                                                                              details[1],
                                                                              details[2],
                                                                              details[3],
                                                                              details[4])

                the_settlement = None
                for city in game_obj.game_cities:
                    if city.city_id == game_stats.selected_settlement:
                        the_settlement = city
                        break

                treasury = None
                for realm in game_obj.game_powers:
                    if realm.name == the_settlement.owner:
                        treasury = realm.coffers
                        break

                # Check available resources to pay a cost of regiment
                enough_resources = True
                for res in treasury:
                    if "Florins" == res[0]:
                        if game_stats.selected_artifact_info.price > res[1]:
                            enough_resources = False
                            break

                # Index of settlement's tile in map list
                x = int(game_stats.selected_tile[0])
                y = int(game_stats.selected_tile[1])
                TileNum = (y - 1) * game_stats.cur_level_width + x - 1

                if game_obj.game_map[TileNum].army_id is not None:
                    for army in game_obj.game_armies:
                        if army.army_id == game_obj.game_map[TileNum].army_id:
                            if army.hero is not None:
                                game_stats.hero_in_settlement = True
                                if len(army.hero.inventory) < 4:
                                    game_stats.inventory_is_full = False
                                else:
                                    game_stats.inventory_is_full = True

                                game_stats.already_has_an_artifact = False
                                if len(army.hero.inventory) > 0:
                                    for artifact in army.hero.inventory:
                                        if artifact.name == artifact_name:
                                            game_stats.already_has_an_artifact = True
                            break

                if enough_resources:
                    game_stats.enough_resources_to_pay = True
                else:
                    game_stats.enough_resources_to_pay = False

    elif 650 < position[0] < 920 and 293 < position[1] < 334:
        # Hero's inventory
        x_axis, y_axis = position[0], position[1]
        x_axis -= 650
        y_axis -= 148
        # print(str(x_axis) + ", " + str(y_axis))
        if (x_axis % 45) <= 42:
            x_axis = math.ceil(x_axis / 45)
            # print("x_axis - " + str(x_axis))
            # print(str(game_stats.hero_inventory))
            if game_stats.hero_inventory is not None:
                # print("len " + str(len(game_stats.hero_inventory)))
                if x_axis <= len(game_stats.hero_inventory):
                    game_stats.inventory_is_full = False
                    game_stats.enough_resources_to_pay = False
                    game_stats.already_has_an_artifact = False
                    game_stats.artifact_focus = "Hero's inventory"
                    game_stats.selected_artifact_info = game_stats.hero_inventory[x_axis - 1]

    elif 650 < position[0] < 920 and 360 < position[1] < 401:
        # Realm's artifact collection
        x_axis, y_axis = position[0], position[1]
        x_axis -= 650
        y_axis -= 148
        # print(str(x_axis) + ", " + str(y_axis))
        if (x_axis % 45) <= 42:
            x_axis = math.ceil(x_axis / 45)
            # print("x_axis - " + str(x_axis))
            # print(str(game_stats.hero_inventory))
            if game_stats.realm_artifact_collection is not None:
                # print("len " + str(len(game_stats.hero_inventory)))
                if x_axis <= len(game_stats.realm_artifact_collection):
                    game_stats.inventory_is_full = False
                    game_stats.enough_resources_to_pay = False
                    game_stats.already_has_an_artifact = False
                    game_stats.artifact_focus = "Realm's artifact collection"
                    game_stats.selected_artifact_info = game_stats.realm_artifact_collection[x_axis - 1]


def school_of_magic(position):
    if 650 < position[0] < 920 and 148 < position[1] < 190:
        x_axis, y_axis = position[0], position[1]
        x_axis -= 650
        y_axis -= 148
        print(str(x_axis) + ", " + str(y_axis))
        if (x_axis % 45) <= 42:
            x_axis = math.ceil(x_axis / 45)
            print("x_axis - " + str(x_axis))

            # structure = special_structures[game_stats.rw_object.name]
            structure = game_stats.rw_object.name

            if x_axis <= len(skills_curriculum.curriculum_by_school[structure]):
                skill_name = skills_curriculum.curriculum_by_school[structure][x_axis - 1]
                details = hero_skill_catalog.hero_skill_data[skill_name]
                game_stats.selected_new_skill = skill_classes.Hero_Skill(str(skill_name),
                                                                         str(details[0]),
                                                                         str(details[1]),
                                                                         str(details[2]),
                                                                         str(details[3]),
                                                                         str(details[4]),
                                                                         list(details[5]),
                                                                         list(details[6]),
                                                                         details[7],
                                                                         None)

                the_settlement = None
                for city in game_obj.game_cities:
                    if city.city_id == game_stats.selected_settlement:
                        the_settlement = city
                        break

                treasury = None
                for realm in game_obj.game_powers:
                    if realm.name == the_settlement.owner:
                        treasury = realm.coffers
                        break

                # Check available resources to pay a cost of regiment
                enough_resources = True
                for res in treasury:
                    if "Florins" == res[0]:
                        if 2000 > res[1]:
                            enough_resources = False
                            break

                if enough_resources:
                    game_stats.enough_resources_to_pay = True
                else:
                    game_stats.enough_resources_to_pay = False

                # Index of settlement's tile in map list
                x = int(game_stats.selected_tile[0])
                y = int(game_stats.selected_tile[1])
                TileNum = (y - 1) * game_stats.cur_level_width + x - 1

                # Is hero in settlement
                if game_obj.game_map[TileNum].army_id is not None:
                    for army in game_obj.game_armies:
                        if army.army_id == game_obj.game_map[TileNum].army_id:
                            if army.hero is not None:
                                game_stats.hero_in_settlement = True

                                # Does he already has learnt this skill
                                not_learned = True
                                for skill in army.hero.skills:
                                    for tag in skill.tags:
                                        if tag == skill_name:
                                            not_learned = False

                                game_stats.hero_doesnt_know_this_skill = not_learned

                            break


# special_structures = {"KL artifact market" : "KL artifact market",
#                       "KL School of magic" : "KL School of magic"}
