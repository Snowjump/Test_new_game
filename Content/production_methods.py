## Among Myth and Wonder
## production_methods

# Set of scripts for all kinds of population to define how they produce new resources and goods
# PM - stands for production method

import math

from Content.production_catalog import *

from Resources import common_selects


def add_resource(r_pops, goods, raw_material, extra_material, additional_amount, tax,
                 realm_treasury, records_local_fees):
    # (r_pops, resource_name, add_quantity, raw_material, extra_material, additional_amount, tax,
    #                  realm_treasury):
    # Check if any of required raw materials are not available at all
    lacking_resources = []
    if raw_material is not None:
        for mat in raw_material:
            lacking_resources.append(str(mat[0]))
            for resource in r_pops.reserve:
                if resource[0] == str(mat[0]):
                    lacking_resources.remove(mat[0])

    # print("lacking_resources - " + str(lacking_resources))
    if len(lacking_resources) == 0:

        # Check if there enough raw materials
        materials = 1
        lowest_material = None
        if raw_material is not None:

            # print("raw_material is not None")
            for mat in raw_material:

                for resource in r_pops.reserve:
                    # print(str(resource[0]) + " and " + str(mat[0]))
                    if resource[0] == str(mat[0]):
                        # print("Required raw mat " + str(mat))

                        current_material = 0.0
                        if resource[1] >= int(mat[1]):
                            current_material = 1.0
                        else:
                            current_material = float(int(resource[1])/int(mat[1]))

                        if lowest_material is None:
                            lowest_material = float(current_material)
                        else:
                            if current_material < lowest_material:
                                lowest_material = float(current_material)

        else:
            # If production doesn't required consumption of any raw materials, then production is free
            lowest_material = 1.0
        # Check if no raw materials have been found in possession of working population
        if lowest_material is None:
            lowest_material = 0.0

        # Consume raw materials required for production
        if raw_material is not None:
            for mat in raw_material:
                for resource in r_pops.reserve:
                    if resource[0] == str(mat[0]):
                        resource[1] -= math.floor(int(mat[1]) * float(lowest_material))
                        if resource[1] == 0:
                            r_pops.reserve.remove(resource)

                # Record consumption of raw materials
                no_record = True
                for resource in r_pops.records_consumed:
                    if resource[0] == str(mat[0]):
                        no_record = False
                        resource[1] += -1 * math.floor(int(mat[1]) * float(lowest_material))

                if no_record:
                    r_pops.records_consumed.append([str(mat[0]), -1 * math.floor(int(mat[1]) * float(lowest_material))])

        # Extra output
        extra_output = 0
        if extra_material is not None:
            available_resource = 0
            run_out_of_resource = False
            for resource in r_pops.reserve:
                if resource[0] == extra_material[0]:
                    if extra_material[1] > resource[1]:
                        available_resource = resource[1]/extra_material[1]
                        run_out_of_resource = True
                    elif extra_material[1] == resource[1]:
                        available_resource = 1
                        run_out_of_resource = True
                    else:
                        available_resource = 1
                        resource[1] -= int(extra_material[1])

            extra_output = int(math.floor(int(additional_amount[1]) * available_resource))
            print("Produced extra output: " + str(additional_amount[0]) + " - " + str(extra_output))

            # Remove used extra material
            if run_out_of_resource:
                for resource in r_pops.reserve:
                    if resource[0] == extra_material[0]:
                        r_pops.reserve.remove(resource)

            # Record consumption of extra material
            if available_resource > 0:
                no_record = True
                for resource in r_pops.records_consumed:
                    if resource[0] == str(extra_material[0]):
                        no_record = False
                        resource[1] += -1 * math.floor(int(extra_material[1]) * float(available_resource))

                if no_record:
                    r_pops.records_consumed.append([str(extra_material[0]),
                                                    -1 * math.floor(int(extra_material[1])
                                                                    * float(available_resource))])

        # Production

        # if add_quantity > 0:
        # print(str(r_pops.reserve) + " - " + str(r_pops.name) + "; goods: " + str(goods))
        for res in goods:
            print(str(res[0]) + " add " + str(res[1]) + " + " + str(extra_output))
            # print(str(goods) + " + " + str(extra_output))
            if len(r_pops.reserve) == 0:
                r_pops.reserve.append([str(res[0]), math.ceil(int(res[1]) * float(lowest_material))
                                       + extra_output])
            else:
                added_true = False
                for abc in r_pops.reserve:
                    # print(str(abc[0]) + " - " + str(abc[1]))
                    if abc[0] == str(res[0]) :
                        print(str(abc[0]) + " - " + str(abc[1]))
                        abc[1] += math.ceil(int(res[1]) * float(lowest_material)) + extra_output
                        added_true = True
                        print(str(abc[0]) + " has became " + str(abc[1]))
                # for resource in r_pops.reserve:
                #     print(str(resource[0]) + " - " + str(resource[1]))
                #     if resource[0] == resource_name:
                #         resource[1] += int(add_quantity)
                #         added_true = True
                #         print(str(resource[0]) + " become " + str(resource[1]))

                if not added_true:
                    r_pops.reserve.append([str(res[0]),
                                           math.ceil(int(res[1]) * float(lowest_material)) + extra_output])
                    print("After creating new resource " + str(r_pops.reserve))

            # print("Total " + str(r_pops.reserve) + " - " + str(r_pops.name) + " " + str(r_pops.population_id))

            # Record production gains
            # print("Gains - " + str(r_pops.records_gained))
            if len(r_pops.records_gained) == 0:
                r_pops.records_gained.append([str(res[0]), math.ceil(int(res[1]) * float(lowest_material))
                                              + extra_output])
                print(str(res[0]) + " gained " + str(math.ceil(int(res[1]) * float(lowest_material)) + extra_output))
            else:
                added_true = False
                for resource in r_pops.records_gained:
                    if resource[0] == res[0]:
                        resource[1] += math.ceil(int(res[1]) * float(lowest_material)) + extra_output
                        added_true = True
                        # print(str(resource[0]) + " - " + str(resource[1]))

                if not added_true:
                    r_pops.records_gained.append([str(res[0]),
                                                  math.ceil(int(res[1]) * float(lowest_material)) + extra_output])
            print("Gains - " + str(r_pops.records_gained))

        # Taxes
        # print(str(tax) + " to put into treasury " + str(realm_treasury))
        for res in tax:
            # Treasury
            if len(realm_treasury) == 0:
                realm_treasury.append([str(res[0]), math.ceil(int(res[1]) * float(lowest_material))])
            else:
                added_true = False
                for abc in realm_treasury:
                    # print(str(abc[0]) + " - " + str(abc[1]))
                    if abc[0] == str(res[0]) :
                        abc[1] += math.ceil(int(res[1]) * float(lowest_material))
                        added_true = True
                        # print(str(abc[0]) + " become " + str(abc[1]))

                if not added_true:
                    realm_treasury.append([str(res[0]), math.ceil(int(res[1]) * float(lowest_material))])
                    # print("After taxing new resource " + str(realm_treasury))

            # Fees records
            if len(records_local_fees) == 0:
                records_local_fees.append([str(res[0]), math.ceil(int(res[1]) * float(lowest_material))])
            else:
                added_true = False
                for abc in records_local_fees:
                    # print(str(abc[0]) + " - " + str(abc[1]))
                    if abc[0] == str(res[0]) :
                        abc[1] += math.ceil(int(res[1]) * float(lowest_material))
                        added_true = True
                        # print(str(abc[0]) + " become " + str(abc[1]))

                if not added_true:
                    records_local_fees.append([str(res[0]), math.ceil(int(res[1]) * float(lowest_material))])
                    # print("After taxing new resource " + str(records_local_fees))


def apply_effects(PM_pops, building_plots, goods, taxes):
    # Building effects
    for plot in building_plots:
        if plot.status == "Built":
            if len(plot.structure.provided_effects) > 0:
                for building_ef in plot.structure.provided_effects:
                    if building_ef.ef_type == "Population":
                        for base_ef in building_ef.content:
                            if base_ef.pops == PM_pops.name:
                                # print(str(building_ef.name) + " - " + str(base_ef.application))
                                if base_ef.application == "Production":
                                    for res in base_ef.bonus:
                                        for product in goods:
                                            if res[0] == product[0]:
                                                if base_ef.operator == "Addition":
                                                    product[1] += res[1]
                                                break

                                elif base_ef.application == "Tax":
                                    for res in base_ef.bonus:
                                        for product in taxes:
                                            if res[0] == product[0]:
                                                if base_ef.operator == "Addition":
                                                    # print("0) " + res[0] + " " + str(res[1]))
                                                    # print("1) " + product[0] + " " + str(product[1]))
                                                    product[1] += res[1]
                                                    # print("2) " + product[0] + " " + str(product[1]))
                                                break

    return goods, taxes


# Production method
def production_method_by_pop(PM_pops, realm_treasury, building_plots, records_local_fees, facility):
    reference = facility + "_" + PM_pops.name
    # This if statement help determine whether this pop participate in production
    if reference in output_by_place_and_pops_dict:
        goods = common_selects.copy_nested_list(output_by_place_and_pops_dict[reference])  # Output of produced gods

        raw_materials = None
        if reference in raw_materials_by_place_and_pops_dict:
            raw_materials = list(raw_materials_by_place_and_pops_dict[reference])

        extra_materials = None
        if reference in extra_materials_by_place_and_pops_dict:
            extra_materials = list(extra_materials_by_place_and_pops_dict[reference])

        additional_surplus = None
        if reference in additional_surplus_by_place_and_pops_dict:
            additional_surplus = list(additional_surplus_by_place_and_pops_dict[reference])

        taxes = common_selects.copy_nested_list(taxes_by_place_and_pops_dict[reference])  # Taxed product for realm
        # print("Base taxes: " + str(taxes))

        goods, taxes = apply_effects(PM_pops, building_plots, goods, taxes)

        add_resource(PM_pops, goods, raw_materials, extra_materials, additional_surplus, taxes, realm_treasury,
                     records_local_fees)
