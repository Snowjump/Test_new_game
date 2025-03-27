## Among Myth and Wonder
## ability_menu_funs

import math

from Resources import game_stats
from Resources import common_selects
from Resources import update_gf_battle
from Resources import graphics_basic
from Resources import graphics_obj

from Resources.Abilities import game_ability

from Content.Abilities import ability_catalog
from Content.Abilities import ability_desc_cat_hero
from Content.Abilities import ability_targets


def prepare_opening_ability_menu():
    print("prepare_opening_ability_menu()")
    b = game_stats.present_battle
    b.total_targets = 0
    graphics_basic.remove_specific_objects(["Selected targets counter panel"], graphics_obj.battle_objects)
    if b.queue[0].obj_type == "Hero":
        open_hero_ability_menu_but(b)
    elif b.queue[0].obj_type == "Regiment":
        open_regiment_ability_menu_but(b)


def open_hero_ability_menu_but(b):
    print("open_hero_ability_menu_but")

    b.battle_window = "Abilities menu"
    b.cursor_function = None
    b.ability_index = 0
    b.school_index = 0
    b.list_of_abilities = []
    b.list_of_schools = []

    army = common_selects.select_army_by_id(b.queue[0].army_id)
    b.available_mana_reserve = int(army.hero.mana_reserve)
    b.list_of_schools.append("Overall")
    b.selected_school = "Overall"
    # Update visuals
    update_gf_battle.add_school_misc_sprites("Overall")
    for ability in army.hero.abilities:
        b.list_of_abilities.append(str(ability))

        school = ability_catalog.ability_cat[ability].school

        if school not in b.list_of_schools:
            b.list_of_schools.append(str(school))

        # Update visuals
        update_gf_battle.add_school_misc_sprites(school)
        update_gf_battle.add_ability_misc_sprites(ability)

    # Abilities from artifacts
    for artifact in army.hero.inventory:
        for effect in artifact.effects:
            if effect.application == "Cast spells":
                for ability in effect.application_tags:
                    b.list_of_abilities.append(str(ability))

                    school = ability_catalog.ability_cat[ability].school

                    if school not in b.list_of_schools:
                        b.list_of_schools.append(str(school))

                    # Update visuals
                    update_gf_battle.add_school_misc_sprites(school)
                    update_gf_battle.add_ability_misc_sprites(ability)

    b.selected_ability = str(army.hero.abilities[0])
    select_hero_ability(b, army)


def open_regiment_ability_menu_but(b):
    print("open_regiment_ability_menu_but")

    army = common_selects.select_army_by_id(b.queue[0].army_id)
    the_unit = army.units[b.queue[0].number]

    if b.attack_name == "Abilities":
        b.battle_window = "Abilities menu"
        b.cursor_function = None
        b.ability_index = 0
        b.school_index = 0
        b.list_of_abilities = []
        b.list_of_schools = []

        b.available_mana_reserve = int(the_unit.mana_reserve)
        b.list_of_schools.append("Overall")
        b.selected_school = "Overall"
        # Update visuals
        update_gf_battle.add_school_misc_sprites("Overall")

        for ability in the_unit.abilities:
            b.list_of_abilities.append(str(ability))

            school = ability_catalog.ability_cat[ability].school

            if school not in b.list_of_schools:
                b.list_of_schools.append(str(school))

            # Update visuals
            update_gf_battle.add_school_misc_sprites(school)
            update_gf_battle.add_ability_misc_sprites(ability)

        b.selected_ability = str(the_unit.abilities[0])
        select_regiment_ability(b, army)


def prepare_selecting_ability(b, position):
    y_axis = position[1]
    y_axis -= 127
    # print("y_axis - " + str(y_axis))
    if y_axis % 44 <= 40:
        y_axis = math.ceil(y_axis / 44)
        # print("index - " + str(y_axis))
        if y_axis <= len(b.list_of_abilities):
            b.selected_ability = str(b.list_of_abilities[y_axis - 1])
            army = common_selects.select_army_by_id(b.queue[0].army_id)
            if b.queue[0].obj_type == "Hero":
                select_hero_ability(b, army)
            elif b.queue[0].obj_type == "Regiment":
                select_regiment_ability(b, army)


def select_hero_ability(b, army):
    print("select_hero_ability")
    ability = ability_catalog.ability_cat[b.selected_ability]
    MP_bonus, initiative, mana_bonus = game_ability.calculate_bonus(ability.name, ability.school, army.hero,
                                                                    ability.base_initiative)
    # print("mana_bonus - " + str(mana_bonus))
    b.ability_mana_cost = int(ability_catalog.ability_cat[b.selected_ability].mana_cost + mana_bonus)
    b.initiative_cost = initiative
    print("b.initiative_cost - " + str(b.initiative_cost))
    b.bonus_magic_power = int(MP_bonus)
    b.ability_description = ability_desc_cat_hero.script_cat[b.selected_ability](b, army.hero.magic_power, MP_bonus)


def select_regiment_ability(b, army):
    unit = army.units[b.queue[0].number]
    ability = ability_catalog.ability_cat[b.selected_ability]
    MP_bonus, initiative, mana_bonus = game_ability.calculate_bonus_regiment(ability.name, ability.school, army.hero,
                                                                             unit, ability.base_initiative)
    b.ability_mana_cost = int(ability_catalog.ability_cat[b.selected_ability].mana_cost + mana_bonus)
    b.initiative_cost = initiative
    b.bonus_magic_power = int(MP_bonus)
    regiment_strength = len(unit.crew)/(unit.number * unit.rows)
    magic_power = int(regiment_strength * unit.magic_power + 0.5)
    b.ability_description = ability_desc_cat_hero.script_cat[b.selected_ability](b, magic_power, MP_bonus)


def prepare_selecting_ability_school(b, position):
    y_axis = position[1]
    y_axis -= 127
    # print("y_axis - " + str(y_axis))
    if y_axis % 44 <= 40:
        y_axis = math.ceil(y_axis / 44)
        # print("index - " + str(y_axis))
        army = common_selects.select_army_by_id(b.queue[0].army_id)
        b.list_of_abilities = []
        if y_axis <= len(b.list_of_schools):
            b.selected_school = str(b.list_of_schools[y_axis - 1])
            if b.queue[0].obj_type == "Hero":
                select_hero_ability_school(b, army)

            elif b.queue[0].obj_type == "Regiment":
                select_regiment_ability_school(b, army)


def select_hero_ability_school(b, army):
    hero = army.hero
    for ability in hero.abilities:
        if b.selected_school == "Overall":
            b.list_of_abilities.append(str(ability))
            # Update visuals
            update_gf_battle.add_ability_misc_sprites(ability)
        elif ability_catalog.ability_cat[ability].school == b.selected_school:
            b.list_of_abilities.append(str(ability))
            # Update visuals
            update_gf_battle.add_school_misc_sprites(b.selected_school)
            update_gf_battle.add_ability_misc_sprites(ability)

    # Abilities from artifacts
    if len(hero.inventory) > 0:
        for artifact in hero.inventory:
            for effect in artifact.effects:
                if effect.application == "Cast spells":
                    if b.selected_school == "Overall":
                        for ability in effect.application_tags:
                            b.list_of_abilities.append(str(ability))
                            # Update visuals
                            update_gf_battle.add_ability_misc_sprites(ability)
                    else:
                        for ability in effect.application_tags:
                            if ability_catalog.ability_cat[ability].school == b.selected_school:
                                b.list_of_abilities.append(str(ability))
                                # Update visuals
                                update_gf_battle.add_school_misc_sprites(b.selected_school)
                                update_gf_battle.add_ability_misc_sprites(ability)

    b.selected_ability = str(b.list_of_abilities[0])
    select_hero_ability(b, army)


def select_regiment_ability_school(b, army):
    unit = army.units[b.queue[0].number]
    for ability in unit.abilities:
        if b.selected_school == "Overall":
            b.list_of_abilities.append(str(ability))
        elif ability_catalog.ability_cat[ability].school == b.selected_school:
            b.list_of_abilities.append(str(ability))

    b.selected_ability = str(b.list_of_abilities[0])
    select_regiment_ability(b, army)


def close_ability_menu_window():
    b = game_stats.present_battle

    b.list_of_schools = []
    b.list_of_abilities = []
    b.ability_index = 0
    b.school_index = 0
    b.selected_school = None
    b.selected_ability = None
    b.battle_window = None
    b.available_mana_reserve = None
    b.ability_description = None


def execute_ability_but():
    b = game_stats.present_battle
    ability = ability_catalog.ability_cat[b.selected_ability]
    if b.available_mana_reserve >= ability.mana_cost:
        player_army = common_selects.select_army_by_id(b.queue[0].army_id)
        b.ability_targets = []
        if ability.target == "all_allies":
            # Ability is executing instantly
            game_ability.select_all_targets(b, player_army)
            game_ability.execute_ability(b, ability)
            b.battle_window = None
        else:
            # Player has to select suitable regiment as a target for ability
            b.cursor_function = "Execute ability"
            magic_power = 0
            if b.queue[0].obj_type == "Regiment":
                unit = player_army.units[b.queue[0].number]
                regiment_strength = len(unit.crew) / (unit.number * unit.rows)
                magic_power = int(regiment_strength * unit.magic_power + 0.5)
            else:
                print("bless_targets(): magic_power - " + str(player_army.hero.magic_power + b.bonus_magic_power) +
                      "; hero.magic_power - " + str(player_army.hero.magic_power) +
                      "; b.bonus_magic_power - " + str(b.bonus_magic_power))
                magic_power = player_army.hero.magic_power
            b.total_targets = ability_targets.ability_cat[b.selected_ability](magic_power +
                                                                              b.bonus_magic_power)
            b.battle_window = None
            graphics_basic.prepare_selected_targets_counter()


def confirm_ability_targets(b, TileNum, player_army, opponent_army):
    print("confirm_ability_targets()")
    print(b.selected_ability)
    correct_target = False
    ability = ability_catalog.ability_cat[b.selected_ability]
    for action in ability.action:
        correct_target = game_ability.confirm_target(b, TileNum, player_army, opponent_army, ability)
        if not correct_target:
            break  # Selected wrong regiment for ability

    if correct_target:
        game_ability.manage_ability_targets(b)
        # b.ready_to_act = False
        # game_battle.action_order(b, "Pass", None)
