## Miracle battles!

# Set of scripts for all kinds of population to define how they sell produced resources to inner market

import math

from Resources import game_obj


def put_to_sell(pops, resource_name, settlement, selling_price):
    # print(str(resource_name) + " for selling")
    if len(pops.reserve) != 0:
        for resource in pops.reserve:
            if resource[0] in resource_name:
                # print("population_id - " + str(pops.population_id) + " pops.reserve - " + str(pops.reserve))
                # [Pop id, product name, quantity for sale, price]
                settlement.inner_market.append([int(pops.population_id), str(resource[0]),
                                                int(resource[1]), float(selling_price)])
                print("population_id - " + str(pops.population_id) + " " + str(resource[0]) + " "
                      + str(int(resource[1])) + " price " + str(float(selling_price)))


def buy_up_from_inner_market(buyer, settlement, buyer_name, realm_treasury):
    budget = 0
    for res in buyer.reserve:
        if res[0] == "Florins":
            budget = int(res[1])

    primary_offer = []
    contenders = []
    the_rest = []
    queue = []
    keep_trading = True
    lowest_price = None
    first_assessment = True

    while keep_trading:
        if first_assessment:
            queue = list(sorted(settlement.inner_market, key=lambda offers: offers[3]))
            first_assessment = False
        else:
            queue = list(the_rest)
            lowest_price = float(queue[0][3])
            the_rest = []

        print("queue: " + str(queue))

        for product in queue:
            if lowest_price is None:
                lowest_price = float(product[3])
                contenders.append([int(product[0]), str(product[1]), int(product[2]), float(product[3])])
                print("contenders: " + str(contenders))
            elif product[3] > lowest_price:
                the_rest.append([int(product[0]), str(product[1]), int(product[2]), float(product[3])])
                print("the_rest: " + str(the_rest))
            else:
                contenders.append([int(product[0]), str(product[1]), int(product[2]), float(product[3])])
                print("contenders: " + str(contenders))

        print("contenders: " + str(contenders))
        total_offer_sum = 0
        for product in contenders:
            total_offer_sum += int(math.floor(int(product[2]) * float(product[3])))

        print("total_offer_sum - " + str(total_offer_sum) + ", budget - " + str(budget))
        if total_offer_sum <= budget:
            # Can continue trading
            print(str(budget - total_offer_sum) + " further trading budget ")
            budget -= int(total_offer_sum)
            for product in contenders:
                quantity = int(product[2])  # * float(product[3])
                income = int(math.floor(int(product[2]) * float(product[3])))
                # [Pop id, product name, sold quantity, price, total income for seller]
                primary_offer.append([int(product[0]), str(product[1]), int(quantity), float(product[3]), int(income)])

            # print("primary_offer: " + str(primary_offer))
            contenders = []
            # print("po - the_rest: " + str(the_rest))
            if not the_rest:
                keep_trading = False
        else:
            print("Not enough money, reduce quantity")
            for product in contenders:
                quantity = math.floor( (int(product[2]) * float(product[3])) * (budget/total_offer_sum) )
                income = math.floor(int(quantity) * float(product[3]))
                # [Pop id, product name, sold quantity, price, total income for seller]
                primary_offer.append([int(product[0]), str(product[1]), int(quantity), float(product[3]), int(income)])

            print("primary_offer: " + str(primary_offer))
            keep_trading = False

        # keep_trading = False

    if len(primary_offer) > 0:
        # Time to transfer sold product and paid money
        # 1 stage: facilities
        # print("transferring resources (facilities) - " + str(settlement.name))
        for TileNum in settlement.property:
            TileObj = game_obj.game_map[TileNum]

            for pops in TileObj.lot.residency:
                for contract in primary_offer:
                    if pops.population_id == contract[0]:
                        for product in pops.reserve:
                            ended_product = False
                            if product[0] == contract[1]:
                                payment = int(contract[4])
                                product_quantity = int(contract[2])
                                for record in buyer.records_turnover:
                                    if record[0] == contract[1]:
                                        if record[1] < 1.0:
                                            product_quantity = int(math.floor(product_quantity * record[1]))
                                            payment = math.floor(int(product_quantity) * float(contract[3]))
                                        break

                                if product_quantity > 0:  # Buyer actually ready to buy product
                                    tax_sum = math.ceil(int(payment) * 0.02)
                                    money_transfer = int(payment) - tax_sum
                                    # print(settlement.name + " - records_turnover_tax: " + str(settlement.records_turnover_tax))
                                    turnover_tax(tax_sum, realm_treasury, settlement)

                                    print("Contract: pop ID - " + str(contract[0]) + " " + str(product_quantity) + " " +
                                          str(contract[1]) + " for " + str(payment) + " florins")
                                    print("Found contract for pops " + str(pops.population_id)
                                          + " - " + str([product[0], product[1]]))
                                    product[1] -= int(product_quantity)
                                    print("pops.reserve - " + str(pops.reserve))
                                    pops.records_sold.append([str(contract[1]), int(product_quantity)])
                                    if product[1] == 0:
                                        ended_product = True

                                    # Check money
                                    no_money = True
                                    for product1 in pops.reserve:
                                        if product1[0] == "Florins":
                                            # print("1) Florins - " + str(product1))
                                            product1[1] += int(money_transfer)
                                            # print("2) Florins - " + str(product1))
                                            no_money = False
                                            break

                                    if no_money:
                                        pops.reserve.append(["Florins", int(money_transfer)])

                                    if ended_product:
                                        for product2 in pops.reserve:
                                            if product2[0] == contract[1]:
                                                pops.reserve.remove(product2)

                                    # Buyer's accounting
                                    no_product = True
                                    for b_product in buyer.reserve:  # Buyer's product = b_product
                                        if b_product[0] == "Florins":
                                            b_product[1] -= int(money_transfer)

                                            # Records - money payment
                                            no_record = True
                                            for br_product in buyer.records_sold:  # Buyer's record product = br_product
                                                if br_product[0] == "Florins":
                                                    br_product[1] += -1 * int(money_transfer)
                                                    no_record = False
                                                    break
                                            if no_record:
                                                buyer.records_sold.append(["Florins", -1 * int(money_transfer)])

                                        elif b_product[0] == contract[1]:
                                            no_product = False
                                            b_product[1] += int(product_quantity)

                                    if no_product:
                                        buyer.reserve.append([str(contract[1]), int(product_quantity)])

                                    # Records - shipment of goods
                                    no_record = True
                                    for br_product in buyer.records_sold:  # Buyer's record product = br_product
                                        if br_product[0] == contract[1]:
                                            br_product[1] += int(product_quantity)
                                            no_record = False
                                            break
                                    if no_record:
                                        buyer.records_sold.append([str(contract[1]), int(product_quantity)])

        # 2 stage: settlements
        print("transferring resources (settlement) - " + str(settlement.name))
        for pops in settlement.residency:
            if pops.name != buyer_name:
                for contract in primary_offer:
                    if pops.population_id == contract[0]:
                        for product in pops.reserve:
                            ended_product = False
                            if product[0] == contract[1]:
                                payment = int(contract[4])
                                product_quantity = int(contract[2])
                                for record in buyer.records_turnover:
                                    if record[0] == contract[1]:
                                        if record[1] < 1.0:
                                            product_quantity = int(math.floor(product_quantity * record[1]))
                                            payment = math.floor(int(product_quantity) * float(contract[3]))
                                        break

                                if product_quantity > 0:  # Buyer actually ready to buy product
                                    tax_sum = math.ceil(int(payment) * 0.02)
                                    money_transfer = int(payment) - tax_sum
                                    turnover_tax(tax_sum, realm_treasury, settlement)

                                    print("contract[1] - " + str(contract[1]) + " for " + str(payment) + " florins")
                                    print("Found contract for pops " + str(pops.population_id)
                                          + " - " + str([product[0], product[1]]))
                                    product[1] -= int(product_quantity)
                                    print("pops.reserve - " + str(pops.reserve))
                                    pops.records_sold.append([str(contract[1]), int(product_quantity)])
                                    if product[1] == 0:
                                        ended_product = True
                                        # pops.reserve.remove(product)

                                    # Check money
                                    no_money = True
                                    for product1 in pops.reserve:
                                        if product1[0] == "Florins":
                                            # print("Increase money for pops " + str(pops.population_id))
                                            # print("1) Florins - " + str(product1))
                                            product1[1] += int(money_transfer)
                                            # print("2) Florins - " + str(product1))
                                            no_money = False
                                            break

                                    if no_money:
                                        # print("Pops " + str(pops.population_id) + " had no money beforehand")
                                        pops.reserve.append(["Florins", int(money_transfer)])

                                    if ended_product:
                                        for product2 in pops.reserve:
                                            if product2[0] == contract[1]:
                                                pops.reserve.remove(product2)

                                    # Buyer's accounting
                                    no_product = True
                                    for b_product in buyer.reserve:  # Buyer's product = b_product
                                        if b_product[0] == "Florins":
                                            b_product[1] -= int(money_transfer)

                                            # Records - money payment
                                            no_record = True
                                            for br_product in buyer.records_sold:  # Buyer's record product = br_product
                                                if br_product[0] == "Florins":
                                                    br_product[1] += -1 * int(money_transfer)
                                                    no_record = False
                                                    break
                                            if no_record:
                                                buyer.records_sold.append(["Florins", -1 * int(money_transfer)])

                                        elif b_product[0] == contract[1]:
                                            no_product = False
                                            b_product[1] += int(product_quantity)

                                    if no_product:
                                        buyer.reserve.append([str(contract[1]), int(product_quantity)])

                                    # Records - shipment of goods
                                    no_record = True
                                    for br_product in buyer.records_sold:  # Buyer's record product = br_product
                                        if br_product[0] == contract[1]:
                                            br_product[1] += int(product_quantity)
                                            no_record = False
                                            break
                                    if no_record:
                                        buyer.records_sold.append([str(contract[1]), int(product_quantity)])

            # else:
            #     # Buyer's payments for product
            #     for contract in primary_offer:
            #         no_product = True
            #         for product in pops.reserve:
            #             # Buyer pays money to seller
            #             tax_sum = math.ceil(int(contract[4]) * 0.02)
            #             money_transfer = int(contract[4]) - tax_sum
            #             # turnover_tax(tax_sum, realm_treasury)
            #
            #             if product[0] == "Florins":
            #                 product[1] -= money_transfer
            #
            #                 # Records
            #                 if len(pops.records_sold) == 0:
            #                     pops.records_sold.append(["Florins", -1 * money_transfer])
            #                 else:
            #                     pops.records_sold[0][1] -= money_transfer
            #
            #             # Check if buyer already has same product
            #             if product[0] == contract[1]:
            #                 no_product = False
            #                 product[1] += int(contract[2])
            #
            #                 # Records
            #                 for record in pops.records_sold:
            #                     if record[0] == contract[1]:
            #                         record[1] += int(contract[2])
            #
            #         if no_product:
            #             pops.reserve.append([str(contract[1]), int(contract[2])])
            #             # Records
            #             pops.records_sold.append([str(contract[1]), int(contract[2])])


def turnover_tax(tax_sum, realm_treasury, settlement):
    # Pay taxes on trade to realm
    settlement.records_turnover_tax += int(tax_sum)
    # print("sell_resources - turnover tax: " + str(settlement.records_turnover_tax) + ", tax_sum: " + str(tax_sum))
    if len(realm_treasury) > 0:
        no_money = True
        for res in realm_treasury:
            if res[0] == "Florins":
                res[1] += int(tax_sum)
                # print("Florins in treasury: " + str(res[1]))
                no_money = False
                break

        if no_money:
            realm_treasury.append(["Florins", int(tax_sum)])
            # print("Florins in treasury: " + str(tax_sum))


# Selling methods
def nobles_sell_resources_gold_deposit(selling_pops, settlement):
    pass


def nobles_sell_resources_arable_land(selling_pops, settlement):
    pass


def nobles_sell_resources_logging_camp(selling_pops, settlement):
    pass


def nobles_sell_resources_stone_quarry(selling_pops, settlement):
    pass


def nobles_sell_resources_metal_mine(selling_pops, settlement):
    pass


def serfs_sell_resources_gold_deposit(selling_pops, settlement):
    pass


def serfs_sell_resources_arable_land(selling_pops, settlement):
    # print("serfs_sell_resources_arable_land")
    put_to_sell(selling_pops, ["Food"], settlement, 1.0)


def serfs_sell_resources_logging_camp(selling_pops, settlement):
    put_to_sell(selling_pops, ["Wood"], settlement, 1.0)


def serfs_sell_resources_stone_quarry(selling_pops, settlement):
    put_to_sell(selling_pops, ["Stone"], settlement, 1.0)


def serfs_sell_resources_metal_mine(selling_pops, settlement):
    put_to_sell(selling_pops, ["Metals"], settlement, 1.0)


def artisans_sell_resources_settlement(selling_pops, settlement):
    put_to_sell(selling_pops, ["Armament", "Tools"], settlement, 1.3)


def merchants_sell_resources_settlement(selling_pops, settlement):
    pass


def clergy_sell_resources_abbey(selling_pops, settlement):
    put_to_sell(selling_pops, ["Ingredients", "Food"], settlement, 1.0)


# Buy up resources from the inner market for later resale
def artisans_buy_up(buying_pops, settlement, realm_treasury):
    pass


def merchants_buy_up(buying_pops, settlement, realm_treasury):
    # Merchants buying up resources in the inner market for Knight Lords
    buy_up_from_inner_market(buying_pops, settlement, "Merchants", realm_treasury)


# Dictionary catalogs
nobles_sell_resources_cat = {"Gold deposit" : nobles_sell_resources_gold_deposit,
                             "Arable land" : nobles_sell_resources_arable_land,
                             "Logging camp" : nobles_sell_resources_logging_camp,
                             "Stone quarry" : nobles_sell_resources_stone_quarry,
                             "Metal mine" : nobles_sell_resources_metal_mine}

serfs_sell_resources_cat = {"Gold deposit" : serfs_sell_resources_gold_deposit,
                            "Arable land" : serfs_sell_resources_arable_land,
                            "Logging camp" : serfs_sell_resources_logging_camp,
                            "Stone quarry" : serfs_sell_resources_stone_quarry,
                            "Metal mine" : serfs_sell_resources_metal_mine}

artisans_sell_resources_cat = {"Settlement" : artisans_sell_resources_settlement}

merchants_sell_resources_cat = {"Settlement" : merchants_sell_resources_settlement}

clergy_sell_resources_cat = {"Magic source" : clergy_sell_resources_abbey}

pops_to_facility_cat = {"Serfs" : serfs_sell_resources_cat,
                        "Nobles" : nobles_sell_resources_cat,
                        "Artisans" : artisans_sell_resources_cat,
                        "Merchants" : merchants_sell_resources_cat,
                        "Clergy" : clergy_sell_resources_cat}

# Buy up
pops_to_buy_up_cat = {"Artisans" : artisans_buy_up,
                      "Merchants" : merchants_buy_up}
