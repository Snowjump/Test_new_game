## Among Myth and Wonder
## objs_selects

from Resources import game_stats
from Resources import graphics_basic
from Resources import algo_building
from Resources import update_gf_game_board


def deselect_army():
    game_stats.selected_object = ""
    game_stats.selected_army = -1
    game_stats.selected_second_army = -1
    game_stats.details_panel_mode = ""
    game_stats.game_board_panel = ""
    game_stats.first_army_exchange_list = []
    game_stats.second_army_exchange_list = []

    graphics_basic.remove_selected_objects()


def select_settlement(settlement):
    game_stats.selected_object = "Settlement"
    game_stats.selected_settlement = int(settlement.city_id)
    game_stats.settlement_area = "Building"
    game_stats.building_row_index = 0
    game_stats.game_board_panel = "settlement panel"
    game_stats.details_panel_mode = "settlement lower panel"

    algo_building.check_requirements()
    graphics_basic.prepare_settlement_info_panel()

    list_of_rows = []
    for plot in settlement.buildings:
        if int(plot.screen_position[1]) not in list_of_rows:
            list_of_rows.append(int(plot.screen_position[1]))

    game_stats.building_rows_amount = max(list_of_rows)

    # Update visuals
    update_gf_game_board.update_settlement_misc_sprites()
    update_gf_game_board.open_settlement_building_sprites()
