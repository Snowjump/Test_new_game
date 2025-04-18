## Among Myth and Wonder
## building_rw_det_cat

from Resources import game_stats
from Resources import game_classes
from Resources import skill_classes
from Resources import game_obj
from Resources import artifact_classes
from Resources import update_gf_game_board
from Resources import common_selects
from Resources.Game_Graphics import graphics_basic
from Resources import common_transactions

from Content import rw_click_scripts
from Content import artifact_catalog
from Content import hero_skill_catalog


def artifact_market_details():
    game_stats.rw_panel_det = game_classes.Object_Surface({1 : buy_artifact_for_hero,
                                                           2 : buy_artifact_for_realm},
                                                          [[651, 217, 790, 237],
                                                           [651, 247, 790, 267]],
                                                          None,
                                                          rw_click_scripts.artifact_market)

    game_stats.enough_resources_to_pay = False

    # Index of settlement's tile in map list
    x = int(game_stats.selected_tile[0])
    y = int(game_stats.selected_tile[1])
    TileNum = (y - 1) * game_stats.cur_level_width + x - 1

    if game_obj.game_map[TileNum].army_id is not None:
        army = common_selects.select_army_by_id(game_obj.game_map[TileNum].army_id)
        if army.hero is not None:
            game_stats.hero_inventory = army.hero.inventory

    the_settlement = common_selects.select_settlement_by_id(game_stats.selected_settlement)

    realm = common_selects.select_realm_by_name(the_settlement.owner)
    game_stats.realm_artifact_collection = realm.artifact_collection

    # Update visuals
    # print("Update visuals")
    update_gf_game_board.update_artifact_sprites()
    img_list = ['Icons/paper_square_40']
    update_gf_game_board.add_misc_sprites(img_list)


def buy_artifact_for_hero():
    print("buy_artifact_for_hero")
    if game_stats.enough_resources_to_pay and game_stats.hero_in_settlement and not game_stats.inventory_is_full:
        if not game_stats.already_has_an_artifact:
            game_stats.already_has_an_artifact = True
            # Index of settlement's tile in map list
            x = int(game_stats.selected_tile[0])
            y = int(game_stats.selected_tile[1])
            TileNum = (y - 1) * game_stats.cur_level_width + x - 1

            the_army = common_selects.select_army_by_id(game_obj.game_map[TileNum].army_id)

            the_settlement = common_selects.select_settlement_by_id(game_stats.selected_settlement)

            treasury = common_selects.select_treasury_by_realm_name(the_settlement.owner)

            # Spent money
            for res in treasury:
                if "Florins" == res[0]:
                    res[1] -= int(game_stats.selected_artifact_info.price)
                    break

            # Transfer money to traders
            for pops in the_settlement.residency:
                if pops.name == "Merchants":
                    no_money = True
                    for product in pops.reserve:
                        # Pay money to seller
                        if product[0] == "Florins":
                            no_money = False
                            product[1] += int(game_stats.selected_artifact_info.price)

                    if no_money:
                        pops.reserve.append(["Florins", int(game_stats.selected_artifact_info.price)])
                    break

            # Give artifact to hero
            artifact_name = game_stats.selected_artifact_info.name
            details = artifact_catalog.artifact_data[artifact_name]
            the_army.hero.inventory.append(artifact_classes.Artifact(details[0],
                                                                     details[1],
                                                                     details[2],
                                                                     details[3],
                                                                     details[4]))

            graphics_basic.prepare_resource_ribbon()


def buy_artifact_for_realm():
    print("buy_artifact_for_realm")
    if game_stats.enough_resources_to_pay:
        the_settlement = common_selects.select_settlement_by_id(game_stats.selected_settlement)

        the_realm = common_selects.select_realm_by_name(the_settlement.owner)
        treasury = common_selects.select_treasury_by_realm_name(the_settlement.owner)

        # Spent money
        for res in treasury:
            if "Florins" == res[0]:
                res[1] -= int(game_stats.selected_artifact_info.price)
                break

        # Transfer money to traders
        for pops in the_settlement.residency:
            if pops.name == "Merchants":
                no_money = True
                for product in pops.reserve:
                    # Pay money to seller
                    if product[0] == "Florins":
                        no_money = False
                        product[1] += int(game_stats.selected_artifact_info.price)

                if no_money:
                    pops.reserve.append(["Florins", int(game_stats.selected_artifact_info.price)])
                break

        # Give artifact to hero
        artifact_name = game_stats.selected_artifact_info.name
        details = artifact_catalog.artifact_data[artifact_name]
        the_realm.artifact_collection.append(artifact_classes.Artifact(details[0],
                                                                       details[1],
                                                                       details[2],
                                                                       details[3],
                                                                       details[4]))

        graphics_basic.prepare_resource_ribbon()


def school_of_magic_details():
    game_stats.rw_panel_det = game_classes.Object_Surface({1: learn_skill_from_school},
                                                          [[651, 217, 760, 237]],
                                                          None,
                                                          rw_click_scripts.school_of_magic)

    game_stats.enough_resources_to_pay = False

    # Update visuals
    # print("Update visuals")
    img_list = ['Icons/paper_square_40']
    update_gf_game_board.add_misc_sprites(img_list)
    update_gf_game_board.update_skills_sprites()


def learn_skill_from_school():
    if game_stats.enough_resources_to_pay and game_stats.hero_in_settlement \
            and game_stats.selected_new_skill is not None and game_stats.hero_doesnt_know_this_skill:

        the_settlement = common_selects.select_settlement_by_id(game_stats.selected_settlement)
        realm = common_selects.select_realm_by_name(the_settlement.owner)
        army = common_selects.select_army_by_id(game_obj.game_map[the_settlement.location].army_id)
        hero = army.hero

        # Spent money
        resources = [["Florins", int(2000)]]
        common_transactions.payment(resources, realm)

        # New learned skill
        new_skill = hero_skill_catalog.hero_skill_data[game_stats.selected_new_skill.name]
        counting = 0
        for skill in hero.skills:
            if skill.skill_type == "Skill":
                counting += 1

        position = [0, int(counting)]

        hero.skills.append(skill_classes.Hero_Skill(str(game_stats.selected_new_skill.name),
                                                    str(new_skill[0]),
                                                    str(new_skill[1]),
                                                    str(new_skill[2]),
                                                    str(new_skill[3]),
                                                    str(new_skill[4]),
                                                    list(new_skill[5]),
                                                    list(new_skill[6]),
                                                    new_skill[7],
                                                    position))

        game_stats.enough_resources_to_pay = None
        game_stats.hero_doesnt_know_this_skill = False

        graphics_basic.prepare_resource_ribbon()


def wheelwright_guild_details():
    game_stats.rw_panel_det = game_classes.Object_Surface({1: learn_attribute_from_building},
                                                          [[651, 217, 788, 237]],
                                                          None,
                                                          rw_click_scripts.attribute_store)

    game_stats.enough_resources_to_pay = False

    # Update visuals
    img_list = ['Icons/paper_square_40']
    update_gf_game_board.add_misc_sprites(img_list)
    update_gf_game_board.update_skills_sprites()


def learn_attribute_from_building():
    if game_stats.enough_resources_to_pay and game_stats.hero_in_settlement \
            and game_stats.selected_new_attribute is not None and game_stats.hero_doesnt_know_this_attribute:

        the_settlement = common_selects.select_settlement_by_id(game_stats.selected_settlement)
        realm = common_selects.select_realm_by_name(the_settlement.owner)
        army = common_selects.select_army_by_id(game_obj.game_map[the_settlement.location].army_id)
        hero = army.hero

        # Spent money
        resources = [["Florins", int(game_stats.selected_item_price)]]
        common_transactions.payment(resources, realm)

        pack = game_stats.selected_new_attribute
        # Increase knowledge and magic power of hero if needed
        for attribute in pack.attribute_list:
            if attribute.tag == "hero":
                if attribute.stat == "magic power":
                    hero.magic_power += int(attribute.value)
                elif attribute.stat == "knowledge":
                    hero.knowledge += int(attribute.value)
                    hero.max_mana_reserve += int(attribute.value * 10)
                    hero.mana_reserve += int(attribute.value * 10)

        hero.attributes_list.append(pack)

        game_stats.enough_resources_to_pay = None
        game_stats.hero_doesnt_know_this_attribute = False

        graphics_basic.prepare_resource_ribbon()


building_catalog = {"KL artifact market" : artifact_market_details,
                    "KL School of magic" : school_of_magic_details,
                    "Wheelwright guild" : wheelwright_guild_details}
