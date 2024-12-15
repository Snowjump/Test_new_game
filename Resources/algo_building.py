## Among Myth and Wonder
## settlement_structures

from Resources import game_obj
from Resources import game_stats
from Resources import update_gf_game_board

from Content import settlement_structures
from Content import ef_structures
from Content import recruitment_structures
from Content import settlement_defences


def check_available_resources(treasury, construction_cost):
    enough = True

    if len(treasury) > 0:
        for res1 in construction_cost:
            available = False
            for res2 in treasury:
                if res1[0] == res2[0]:
                    if res1[1] <= res2[1]:
                        pass
                    else:
                        enough = False
                    available = True

            if not available:
                enough = False
    else:
        enough = False

    if enough:
        return True
    else:
        return False


def consume_constructions_materials(treasury, construction_cost, settlement):
    for needed in construction_cost:
        if needed[0] == "Florins":
            # Pay wages to builders
            builders = builders_cat[settlement.alignment]
            for pops in settlement.residency:
                if pops.name == builders:
                    # Give money
                    no_money = True
                    if len(pops.reserve) > 0:
                        for res in pops.reserve:
                            if res[0] == "Florins":
                                res[1] += int(needed[1])
                                no_money = False

                    if no_money:
                        pops.reserve.append(["Florins", int(needed[1])])

                    # Record payment
                    no_money = True
                    if len(pops.records_additional_gains) > 0:
                        for res in pops.records_additional_gains:
                            if res[0] == "Florins":
                                res[1] += int(needed[1])
                                no_money = False

                    if no_money:
                        pops.records_additional_gains.append(["Florins", int(needed[1])])

        # Remove consumed resources
        for stock in treasury:
            if needed[0] == stock[0]:
                if needed[1] == stock[1]:
                    treasury.remove(stock)
                else:
                    stock[1] -= int(needed[1])


def start_construction(plot):
    plot.status = "Building"
    plot.structure = plot.upgrade
    plot.upgrade = None

    # Update visuals
    update_gf_game_board.add_settlement_building_sprites(plot.structure.name, plot.structure.img)


def perform_construction():
    for city in game_obj.game_cities:
        for plot in city.buildings:
            if plot.status == "Building":
                plot.structure.time_passed += 1

                if plot.structure.time_passed == plot.structure.construction_time:
                    # Construction is completed
                    plot.status = "Built"
                    print("Structure - " + str(plot.structure.name) + ", upgrade - "
                          + str(settlement_structures.new_upgrades_cat[city.alignment][plot.structure.name]))
                    next_upgrade = settlement_structures.new_upgrades_cat[city.alignment][plot.structure.name]
                    if plot.structure.defensive_structure is not None:
                        print("name - " + str(plot.structure.name))
                        print("title_name - " + str(plot.structure.title_name))
                        print("img - " + str(plot.structure.img))
                        print("construction_cost - " + str(plot.structure.construction_cost))
                        print("construction_time - " + str(plot.structure.construction_time))
                        print("provided_effects - " + str(plot.structure.provided_effects))
                        print("recruitment - " + str(plot.structure.recruitment))
                        print("structure_tags - " + str(plot.structure.structure_tags))
                        print("required_buildings - " + str(plot.structure.required_buildings))
                        print("defensive_structure - " + str(plot.structure.defensive_structure))
                        settlement_defences.defence_scripts[plot.structure.name](city)
                    if next_upgrade is not None:
                        parameters = settlement_structures.structures_groups[city.alignment][next_upgrade]
                        print(str(parameters))
                        ef_list = []
                        if plot.structure.name in ef_structures.ef_structures_cat:
                            ef_list = ef_structures.ef_structures_cat[city.alignment][plot.structure.name]
                        recruitment = None
                        if parameters[0] in recruitment_structures.structures_groups[city.alignment]:
                            print("New recruitment - " + str(recruitment_structures.structures_groups[city.alignment]
                                                             [parameters[0]]))
                            recruitment = recruitment_structures.prepare_recruitment(
                                recruitment_structures.structures_groups[city.alignment]
                                [parameters[0]])
                        defences = None
                        if parameters[8] is not None:
                            defences = str(parameters[8])
                        plot.upgrade = settlement_structures.Structure(str(parameters[0]),
                                                                       list(parameters[1]),
                                                                       str(parameters[2]),
                                                                       list(parameters[3]),
                                                                       int(parameters[4]),
                                                                       list(ef_list),
                                                                       recruitment,
                                                                       list(parameters[6]),
                                                                       list(parameters[7]),
                                                                       defences)

                    update_control(plot.structure, city)


def check_requirements():
    for settlement in game_obj.game_cities:
        if settlement.city_id == game_stats.selected_settlement:
            for plot in settlement.buildings:
                if plot.upgrade is not None:
                    lost_something = False
                    if len(plot.upgrade.required_buildings) > 0:
                        for requirement in plot.upgrade.required_buildings:
                            requirement_ready = False
                            for building in settlement.buildings:
                                if building.status == "Built":
                                    if requirement in building.structure.structure_tags:
                                        requirement_ready = True

                            if not requirement_ready:
                                lost_something = True

                    if lost_something:
                        plot.upgrade.fulfilled_conditions = False
                    else:
                        plot.upgrade.fulfilled_conditions = True
            break


def update_control(structure, settlement):
    print("update_control")
    if structure.provided_effects:
        for effect in structure.provided_effects:
            print(effect.name)
            if effect.ef_type == "Control":
                for control_eff in effect.content:
                    add_new_culture = True
                    if len(settlement.control) > 0:
                        for culture in settlement.control:
                            if culture[0] == control_eff.realm_type:
                                add_new_culture = False
                                if control_eff.operator == "Addition":
                                    culture[1] += int(control_eff.bonus)

                    if add_new_culture:
                        settlement.control.append([str(control_eff.realm_type), int(control_eff.bonus)])


# Catalogs
builders_cat = {"Knight Lords": "Artisans",
                "Nature Keepers": None}
