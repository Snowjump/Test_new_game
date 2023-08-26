## Miracle battles
## AI_learn_skills

import random

from Resources import game_basic
from Resources import skill_classes

from Content import hero_skill_catalog
from Content import skill_weights

from Strategy_AI import archetype_skill_weights


def manage_skill_points(hero):
    print("hero.new_skill_points - " + str(hero.new_skill_points))
    if hero.new_skill_points > 0:
        for skill_point in range(hero.new_skill_points):
            # Prepare new skills and perks
            upgrade_skill_list = []
            for skill in hero.skills:
                if skill.skill_type == "Skill" and skill.skill_level != "Expert":
                    upgrade_skill_list.append(str(skill.next_level))

            if len(upgrade_skill_list) > 0:
                hero.new_skills.append(random.choice(upgrade_skill_list))

            # print("guaranteed_perk_list")
            guaranteed_perk_list = []
            for skill in hero_skill_catalog.hero_skill_data:
                # print("Checking " + str(skill))
                if hero_skill_catalog.hero_skill_data[skill][1] == "Perk":
                    # print("Found perk - " + str(skill))
                    all_there = True
                    for requisite in hero_skill_catalog.hero_skill_data[skill][6]:
                        found = False
                        for available in hero.skills:
                            if requisite in available.tags:
                                found = True

                        if not found:
                            all_there = False

                    if all_there:
                        perk_capacity = 0
                        learned_perks = 0
                        for skill2 in hero.skills:
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
                            guaranteed_perk_list.append(str(skill))

            if len(guaranteed_perk_list) > 0:
                # print(str(guaranteed_perk_list))
                hero.new_skills.append(random.choice(guaranteed_perk_list))

            # print("third_skill_list")
            third_skill_list = []
            for skill in hero.skills:
                if skill.skill_type == "Skill" and skill.skill_level != "Expert":
                    if skill.next_level not in hero.new_skills:
                        third_skill_list.append(str(skill.next_level))

            for skill in hero_skill_catalog.hero_skill_data:
                n_skill = hero_skill_catalog.hero_skill_data[skill]
                if n_skill[1] == "Skill" and n_skill[3] == "Basic":
                    not_in_skills = True
                    for old_skill in hero.skills:
                        if skill in old_skill.tags:
                            not_in_skills = False

                    if skill not in hero.new_skills and not_in_skills:
                        third_skill_list.append(str(skill))

                elif n_skill[1] == "Perk":
                    not_in_skills = True
                    complete_requisites = True
                    for old_perk in hero.skills:
                        if skill == old_perk.name:
                            not_in_skills = False

                    for requisite in n_skill[6]:
                        found = False
                        for old_skill in hero.skills:
                            if requisite in old_skill.tags:
                                found = True

                        if not found:
                            complete_requisites = False

                    if skill not in hero.new_skills and not_in_skills and complete_requisites:
                        perk_capacity = 0
                        learned_perks = 0
                        for skill2 in hero.skills:
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
                # print(str(third_skill_list))
                weights_list = []
                for skill in third_skill_list:
                    weights_list.append(int(skill_weights.class_cat[hero.hero_class][skill]))
                # print(str(weights_list))
                third_skill = random.choices(third_skill_list, weights=weights_list)
                # print(str(third_skill))
                hero.new_skills.append(str(third_skill[0]))
                # print(str(hero.new_skills))

            # print("fourth_skill_list")
            fourth_skill_list = []
            for skill in hero.skills:
                if skill.skill_type == "Skill" and skill.skill_level != "Expert":
                    if skill.next_level not in hero.new_skills:
                        fourth_skill_list.append(str(skill.next_level))

            for skill in hero_skill_catalog.hero_skill_data:
                n_skill = hero_skill_catalog.hero_skill_data[skill]
                if n_skill[1] == "Skill" and n_skill[3] == "Basic":
                    not_in_skills = True
                    for old_skill in hero.skills:
                        if skill in old_skill.tags:
                            not_in_skills = False

                    if skill not in hero.new_skills and not_in_skills:
                        fourth_skill_list.append(str(skill))

                elif n_skill[1] == "Perk":
                    not_in_skills = True
                    complete_requisites = True
                    for old_perk in hero.skills:
                        if skill == old_perk.name:
                            not_in_skills = False

                    for requisite in n_skill[6]:
                        found = False
                        for old_skill in hero.skills:
                            if requisite in old_skill.tags:
                                found = True

                        if not found:
                            complete_requisites = False

                    if skill not in hero.new_skills and not_in_skills and complete_requisites:
                        perk_capacity = 0
                        learned_perks = 0
                        for skill2 in hero.skills:
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
                # print(str(fourth_skill_list))
                weights_list = []
                for skill in fourth_skill_list:
                    weights_list.append(int(skill_weights.class_cat[hero.hero_class][skill]))
                # print(str(weights_list))
                fourth_skill = random.choices(fourth_skill_list, weights=weights_list)
                # print(str(fourth_skill))
                hero.new_skills.append(str(fourth_skill[0]))
                # print(str(hero.new_skills))

            final_weights_list = []
            for available_skill in hero.new_skills:
                final_weights_list.append(archetype_skill_weights.class_cat[hero.archetype][available_skill])
            new_skill_name = random.choices(hero.new_skills, weights=final_weights_list)[0]
            print("new_skill_name - " + new_skill_name)

            new_skill = hero_skill_catalog.hero_skill_data[new_skill_name]

            replace_with = None
            if new_skill[3] == "Advanced" or new_skill[3] == "Expert":
                num = 0
                for old_skill in hero.skills:
                    if old_skill.next_level == new_skill_name:
                        replace_with = int(num)
                        break
                    num += 1

            if replace_with is not None:
                position = list(hero.skills[replace_with].screen_position)
                hero.skills[replace_with] = (
                    skill_classes.Hero_Skill(str(new_skill_name),
                                             str(new_skill[0]),
                                             str(new_skill[1]),
                                             str(new_skill[2]),
                                             str(new_skill[3]),
                                             str(new_skill[4]),
                                             list(new_skill[5]),
                                             list(new_skill[6]),
                                             new_skill[7],
                                             position))

                game_basic.learn_new_abilities(new_skill_name, hero)

            else:
                position = []
                if new_skill[1] == "Skill":
                    counting = 0
                    for skill in hero.skills:
                        if skill.skill_type == "Skill":
                            counting += 1

                    position = [0, int(counting)]

                else:
                    counting = 0
                    still_counting = True
                    perks = 1
                    for skill in hero.skills:
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

                hero.skills.append(skill_classes.Hero_Skill(str(new_skill_name),
                                                            str(new_skill[0]),
                                                            str(new_skill[1]),
                                                            str(new_skill[2]),
                                                            str(new_skill[3]),
                                                            str(new_skill[4]),
                                                            list(new_skill[5]),
                                                            list(new_skill[6]),
                                                            new_skill[7],
                                                            position))

                game_basic.learn_new_abilities(new_skill_name, hero)

            hero.new_skills = []
            hero.new_skill_points -= 1
