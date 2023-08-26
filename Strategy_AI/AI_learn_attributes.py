## Miracle battles
## AI_learn_attributes

import random
import math

from Content import battle_attributes_catalog

from Strategy_AI import archetype_attributes_weights


def manage_attributes_points(hero):
    print("hero.new_attribute_points - " + str(hero.new_attribute_points))
    if hero.new_attribute_points > 0:
        pack_list = []
        pack_weights_list = []
        for pack in battle_attributes_catalog.basic_heroes_attributes[hero.hero_class][hero.attribute_points_used - 1]:
            pack_list.append(pack)
            weight_sum = 0
            for attribute in pack.attribute_list:
                weight_sum += archetype_attributes_weights.class_tag_cat[hero.archetype][attribute.tag] + \
                    archetype_attributes_weights.class_stat_cat[hero.archetype][attribute.stat]
            weight_sum = int(math.ceil(weight_sum / len(pack.attribute_list)))
            pack_weights_list.append(weight_sum)

        print("pack_weights_list: " + str(pack_weights_list))

        new_attribute_pack = random.choices(pack_list, weights=pack_weights_list)[0]
        print("Battle attributes pack:")
        for attribute in new_attribute_pack.attribute_list:
            print(attribute.tag + " " + attribute.stat + " +" + str(attribute.value))
            if attribute.tag == "hero":
                if attribute.stat == "magic power":
                    hero.magic_power += int(attribute.value)
                elif attribute.stat == "knowledge":
                    hero.knowledge += int(attribute.value)
                    hero.max_mana_reserve += int(attribute.value * 10)
                    hero.mana_reserve += int(attribute.value * 10)

        hero.attributes_list.append(new_attribute_pack)

        hero.attribute_points_used += 1
        hero.new_attribute_points -= 1
