## Miracle battles!

# After turn end these scripts compute economy actions

import math
import random

from Content import production_methods
from Content import sell_resources
from Content import buy_resources
from Content import basic_needs
from Resources import game_obj


def snapshot_turnover():
    # Record ratio of sold to bought quantity of products last round
    # In order to adjust purchases in new round

    # 1 step - look for merchants
    for city in game_obj.game_cities:
        for pop in city.residency:
            if pop.name in ["Merchants"]:
                # 2 step - look over products sold by population to merchants
                for sold_product in pop.records_sold:
                    if sold_product[0] != "Florins":
                        no_sale = True
                        # 3 step - look over products bought by population from merchants
                        for bought_product in pop.records_bought:
                            if bought_product[0] == sold_product[0]:
                                # 3 step - add ratio to records
                                no_sale = False
                                ratio = float(-1 * int(bought_product[1]) / int(sold_product[1]))
                                ratio = math.floor(ratio * 100) / 100
                                pop.records_turnover.append([str(sold_product[0]),
                                                             float(ratio)])
                                print("Added ratio: " + str(sold_product[0]) + " - " +
                                      str(ratio))

                        if no_sale:
                            # 4 step - add ratio to records with value 0
                            pop.records_turnover.append([str(sold_product[0]),
                                                         float(0)])
                            print("Added ratio: " + str(sold_product[0]) + " - " +
                                  str(float(0)))

                # Check for products in reserve that hadn't been sold in previous round
                # 5 step - look through reserves
                for reserved_product in pop.reserve:
                    if reserved_product[0] != "Florins":
                        calculate_ratio = True
                        for record in pop.records_turnover:
                            if reserved_product[0] == record[0]:
                                # 6 stop - ignore products with calculated ratio
                                calculate_ratio = False
                                break

                        if calculate_ratio:
                            # 7 step - add ratio to records with value 0
                            pop.records_turnover.append([str(reserved_product[0]),
                                                         float(0)])
                            print("Added ratio: " + str(reserved_product[0]) + " - " +
                                  str(float(0)))



def nullify_inner_market():
    for city in game_obj.game_cities:
        print("nullify_inner_market - " + str(city.name))
        # print("1 city.previous_inner_market - " + str(city.previous_inner_market))
        # print("city.inner_market - " + str(city.inner_market))
        city.previous_inner_market = []
        # print("2 city.previous_inner_market - " + str(city.previous_inner_market))
        city.inner_market = []
        # print("3 city.previous_inner_market - " + str(city.previous_inner_market))


def nullify_market_demand():
    for city in game_obj.game_cities:
        print("nullify_market_demand - " + str(city.name))
        city.market_demand = []


def nullify_records():
    for city in game_obj.game_cities:
        # 1 stage: facilities
        print("nullify_records (facilities) - " + str(city.name))
        for TileNum in city.property:
            TileObj = game_obj.game_map[TileNum]
            # print("nullify_records - " + str(TileObj.lot.obj_name))
            for pops in TileObj.lot.residency:
                # print("1) nullify_records - " + str(pops.name) + " records are "
                #       + str(pops.records_gained) + " " + str(pops))
                pops.records_gained = list(pops.records_additional_gains)  # Remove old gains and record resources
                # that have been gained during the turn
                pops.records_additional_gains = []
                pops.records_sold = []
                pops.records_bought = []
                pops.records_consumed = []
                # print("2) nullify_records - " + str(pops.name) + " records are "
                #       + str(pops.records_gained) + " " + str(pops))

        # 2 stage: settlements
        print("nullify_records (settlements) - " + str(city.name))
        for pops in city.residency:
            # print("1) nullify_records - " + str(pops.name) + " records are "
            #       + str(pops.records_gained) + " " + str(pops))
            pops.records_gained = list(pops.records_additional_gains)  # Remove old gains and record resources
            # that have been gained during the turn
            pops.records_additional_gains = []
            pops.records_sold = []
            pops.records_bought = []
            pops.records_consumed = []
            # print("2) nullify_records - " + str(pops.name) + " records are "
            #       + str(pops.records_gained) + " " + str(pops))

        # 3 stage: fees and taxes
        city.records_turnover_tax = 0
        city.records_local_fees = []


def production():
    for city in game_obj.game_cities:

        # Temporary solution
        if city.owner != "Neutral":

            realm_treasury = None
            for realm in game_obj.game_powers:
                if realm.name == city.owner:
                    realm_treasury = realm.coffers

            # 1 stage: facilities

            print("production (facilities) - " + str(city.name))
            for TileNum in city.property:

                TileObj = game_obj.game_map[TileNum]
                # print("")
                # print("Facility - " + str(TileNum) + " - " + str(TileObj.lot.obj_name) + " - " + str(TileObj))
                # print(TileObj.lot.obj_name)

                for pops in TileObj.lot.residency:
                    # if TileNum > 50:
                    # print("Population - " + str(pops.name) + ", id - " + str(pops.population_id)
                    #       + ", tilenum - " + str(TileNum) + " - " + str(pops))
                    production_methods.pops_to_facility_cat[pops.name][TileObj.lot.obj_name](pops, realm_treasury,
                                                                                             city.buildings,
                                                                                             city.records_local_fees,
                                                                                             TileObj.lot.obj_name)

            # 2 stage: settlements
            # print("")
            # print("production (settlements) - " + str(city.name))
            for pops in city.residency:
                # print("Population - " + str(pops.name) + ", id - " + str(pops.population_id)
                #       + ", tilenum - " + str(city.location) + " - " + str(pops))
                production_methods.pops_to_facility_cat[pops.name]["Settlement"](pops, realm_treasury, city.buildings,
                                                                                 city.records_local_fees,
                                                                                 "Settlement")


def sell_to_inner_market():
    for city in game_obj.game_cities:

        realm_treasury = None
        for realm in game_obj.game_powers:
            if realm.name == city.owner:
                realm_treasury = realm.coffers

        # 1 stage: facilities
        print("sell_to_inner_market (facilities) - " + str(city.name))
        for TileNum in city.property:
            TileObj = game_obj.game_map[TileNum]
            # print("Facility - " + str(TileNum) + " - " + str(TileObj.lot.obj_name) + " - " + str(TileObj))

            for pops in TileObj.lot.residency:
                # print("Population - " + str(pops.name) + ", id - " + str(pops.population_id)
                #       + ", tilenum - " + str(TileNum) + " - " + str(pops))

                # Putting resources from population for selling on the inner market
                sell_resources.pops_to_facility_cat[pops.name][TileObj.lot.obj_name](pops, city)

        # 2 stage: settlements
        # print("sell_to_inner_market (settlements) - " + str(city.name))
        for pops in city.residency:
            # print("Population - " + str(pops.name) + ", id - " + str(pops.population_id)
            #       + ", tilenum - " + str(city.location) + " - " + str(pops))
            sell_resources.pops_to_facility_cat[pops.name]["Settlement"](pops, city)

        print("")
        # Merchants buy up resources from the inner market
        for pops in city.residency:
            sell_resources.pops_to_buy_up_cat[pops.name](pops, city, realm_treasury)


def buy_from_inner_market():
    for city in game_obj.game_cities:
        realm_treasury = None
        for realm in game_obj.game_powers:
            if realm.name == city.owner:
                realm_treasury = realm.coffers

        trader = None

        # Merchants put products to sale in the inner market
        for trader_pops in city.residency:
            buy_resources.pops_sales_cat[trader_pops.name](trader_pops, city)

            if trader_pops.name == "Merchants":
                trader = trader_pops

        city.previous_inner_market = list(city.inner_market)
        print("")
        # 1 stage: facilities
        for TileNum in city.property:
            TileObj = game_obj.game_map[TileNum]

            for pops in TileObj.lot.residency:
                # print("Population - " + str(pops.name) + ", id - " + str(pops.population_id)
                #       + ", tilenum - " + str(TileNum) + " - " + str(pops))
                buy_resources.pops_to_facility_cat[pops.name][TileObj.lot.obj_name](pops, city, True)

        # 2 stage: settlements
        for pops in city.residency:
            # print("Population - " + str(pops.name) + ", id - " + str(pops.population_id)
            #       + ", tilenum - " + str(city.location) + " - " + str(pops))
            buy_resources.pops_to_facility_cat[pops.name]["Settlement"](pops, city, True)

        # Adjust orders quantity on the inner market
        buy_resources.adjust_orders(city)

        print("")
        # Perform purchase on the inner market
        # 1 stage: facilities
        for TileNum in city.property:
            TileObj = game_obj.game_map[TileNum]

            for pops in TileObj.lot.residency:
                # print("")
                # print("Population - " + str(pops.name) + ", id - " + str(pops.population_id)
                #       + ", tilenum - " + str(TileNum) + " - " + str(pops))
                buy_resources.fulfill_orders(pops, city, trader, realm_treasury)

        # 2 stage: settlements
        for pops in city.residency:
            # print("")
            # print("Population - " + str(pops.name) + ", id - " + str(pops.population_id)
            #       + ", tilenum - " + str(city.location) + " - " + str(pops))
            buy_resources.fulfill_orders(pops, city, trader, realm_treasury)


def consume_goods():
    print("")
    for city in game_obj.game_cities:
        # 1 stage: facilities
        print("consumption (facilities) - " + str(city.name))
        for TileNum in city.property:

            TileObj = game_obj.game_map[TileNum]
            # print("")
            # print("Facility - " + str(TileNum) + " - " + str(TileObj.lot.obj_name) + " - " + str(TileObj))
            # print(TileObj.lot.obj_name)

            for pops in TileObj.lot.residency:
                # if TileNum > 50:
                # print("Population - " + str(pops.name) + ", id - " + str(pops.population_id)
                #       + ", tilenum - " + str(TileNum) + " - " + str(pops))
                basic_needs.pops_to_facility_cat[pops.name][TileObj.lot.obj_name](pops)

        # 2 stage: settlements
        print("consumption (settlements) - " + str(city.name))
        for pops in city.residency:
            # print("")
            # print("Population - " + str(pops.name) + ", id - " + str(pops.population_id)
            #       + ", tilenum - " + str(city.location) + " - " + str(pops))
            basic_needs.pops_to_facility_cat[pops.name]["Settlement"](pops)


def nullify_turnover():
    for city in game_obj.game_cities:
        for pops in city.residency:
            pops.records_turnover = []
