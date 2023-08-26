## Miracle battles!

def provide_resources(resources_list):
    treasury = []
    # print("0. Treasury - " + str(treasury))
    for res in resources_list:
        treasury.append([str(res[0]), int(res[1])])
        # print("1. Treasury - " + str(treasury))

    print("Final. Treasury - " + str(treasury))
    return list(treasury)


def LE_provide_resources_KL():
    # print("LE_provide_resources_KL")
    return provide_resources([["Florins", 10000], ["Food", 1000], ["Wood", 1400], ["Stone", 1000], ["Armament", 5000]])
# [["Florins", 4000], ["Food", 1000], ["Wood", 800], ["Armament", 500]]


def LE_provide_resources_NK():
    # print("LE_provide_resources_NK")
    return provide_resources([["Florins", 4000], ["Food", 1000], ["Wood", 1000], ["Armament", 500]])


alignment_resources = {"Knight Lords": LE_provide_resources_KL,
                       "Nature Keepers": LE_provide_resources_NK}
