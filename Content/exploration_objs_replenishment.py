## Among Myth and Wonder
## exploration_objs_replenishment

from Content import exploration_catalog
from Content import lair_army_catalog

from Resources import game_obj
from Resources import game_stats
from Resources import game_classes
from Resources import common_selects


def replenish_objects():
    for TileObj in game_obj.game_map:
        if TileObj.lot is not None:
            if TileObj.lot != "City":
                if TileObj.lot.obj_typ in exploration_catalog.exploration_objects_groups_cat:
                    fac = groups_cat[TileObj.lot.obj_typ]
                    if TileObj.lot.obj_name in fac:
                        fac[TileObj.lot.obj_name](TileObj.lot)
                    # print(TileObj.lot.obj_name + " at " + str(TileObj.posxy) + " - need_replenishment is " +
                    #       str(TileObj.lot.properties.need_replenishment))

                    else:
                        if TileObj.lot.properties.need_replenishment:
                            TileObj.lot.properties.time_left_before_replenishment -= 1
                            if TileObj.lot.properties.time_left_before_replenishment == 0:
                                TileObj.lot.properties.need_replenishment = False


def replenish_mythic_monolith(lot):
    pass


def replenish_stone_circle(lot):
    pass


def replenish_scholars_tower(lot):
    pass


def replenish_stone_well(lot):
    lot.properties.hero_list = []


def replenish_burial_mound(lot):
    if lot.properties.need_replenishment:
        lot.properties.time_left_before_replenishment -= 1

        if lot.properties.time_left_before_replenishment == 0:
            lot.properties.need_replenishment = False


def replenish_anglers_cabin(lot):
    if lot.properties.need_replenishment:
        lot.properties.time_left_before_replenishment -= 1

        if lot.properties.time_left_before_replenishment == 0:
            lot.properties.need_replenishment = False


# Lair
def replenish_runaway_serfs_refuge(lot):
    replenish_lair_with_army(lot)


def replenish_treasure_tower(lot):
    replenish_lair_with_army(lot)


def replenish_lair_of_grey_dragons(lot):
    replenish_lair_with_army(lot)


def replenish_lair_with_army(lot):
    if lot.properties.need_replenishment:
        lot.properties.time_left_before_replenishment -= 1

        if lot.properties.time_left_before_replenishment == 0:
            lot.properties.need_replenishment = False

            if lot.properties.army_id is None:
                x = int(lot.posxy[0])
                y = int(lot.posxy[1])
                TileNum = int(lot.location)

                game_stats.army_id_counter += 1
                game_obj.game_armies.append(game_classes.Army([x, y], int(TileNum),
                                                              int(game_stats.army_id_counter),
                                                              "Neutral",
                                                              False))

                lot.properties.army_id = int(game_stats.army_id_counter)

                army = common_selects.select_army_by_id(lot.properties.army_id)
                lair_army_catalog.lair_dictionary[lot.obj_name](army.units)

            else:
                army = common_selects.select_army_by_id(lot.properties.army_id)
                army.units = []
                lair_army_catalog.lair_dictionary[lot.obj_name](army.units)


bonus_scripts = {"Mythic monolith" : replenish_mythic_monolith,
                 "Stone circle" : replenish_stone_circle,
                 "Scholar's tower" : replenish_scholars_tower,
                 "Stone well" : replenish_stone_well,
                 "Burial mound" : replenish_burial_mound,
                 "Angler's cabin" : replenish_anglers_cabin,
                 }


lair_scripts = {"Runaway serfs refuge" : replenish_runaway_serfs_refuge,
                "Treasure tower" : replenish_treasure_tower,
                "Lair of grey dragons" : replenish_lair_of_grey_dragons}


groups_cat = {"Bonus" : bonus_scripts,
              "Lair" : lair_scripts}
