## Among Myth and Wonder
## common_hero_funs

import random

from Resources import game_stats
from Resources import game_classes
from Resources import skill_classes
from Resources import game_basic
from Resources import update_gf_game_board
from Resources import common_transactions

from Content import hero_names


def create_hero(hero_class, hero_pick, realm, settlement,
                first_skill_name, second_skill_name, first_skill, second_skill):
    game_stats.hero_id_counter += 1
    new_hero = game_classes.Hero(int(game_stats.hero_id_counter),  # hero_id
                                 str(random.choice(hero_names.hero_classes_cat[hero_class])),
                                 str(hero_pick[0]),  # hero_class
                                 int(hero_pick[3]),  # level
                                 0,  # experience
                                 int(hero_pick[1]),  # magic_power
                                 int(hero_pick[2]),  # knowledge
                                 list(hero_pick[8]),  # attributes_list
                                 str(hero_pick[4]),  # img
                                 str(hero_pick[5]),  # img_source
                                 int(hero_pick[6]),  # x_offset
                                 int(hero_pick[7]),  # y_offset
                                 [skill_classes.Hero_Skill(str(first_skill_name),
                                                           str(first_skill[0]),
                                                           str(first_skill[1]),
                                                           str(first_skill[2]),
                                                           str(first_skill[3]),
                                                           str(first_skill[4]),
                                                           list(first_skill[5]),
                                                           list(first_skill[6]),
                                                           first_skill[7],
                                                           [0, 0]),
                                  skill_classes.Hero_Skill(str(second_skill_name),
                                                           str(second_skill[0]),
                                                           str(second_skill[1]),
                                                           str(second_skill[2]),
                                                           str(second_skill[3]),
                                                           str(second_skill[4]),
                                                           list(second_skill[5]),
                                                           list(second_skill[6]),
                                                           second_skill[7],
                                                           [0, 1])],  # skills
                                 int(hero_pick[2]) * 10,  # maximum mana reserve
                                 int(hero_pick[2]) * 10)  # mana reserve

    new_hero.abilities.append("Direct order")
    game_basic.learn_new_abilities(first_skill_name, new_hero)
    game_basic.learn_new_abilities(second_skill_name, new_hero)

    new_experience, bonus_level = game_basic.increase_level_for_new_heroes(settlement)
    game_basic.hero_next_level(new_hero, new_experience)

    common_transactions.payment([["Florins", 2000 + (hero_pick[3] + bonus_level - 1) * 250]], realm)

    # Update visuals
    update_gf_game_board.update_regiment_sprites()

    return new_hero
