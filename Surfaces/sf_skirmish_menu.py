## Among Myth and Wonder
## sf_skirmish_menu

from Resources import graphics_obj


def skirmish_menu_keys(key_action):
    pass


def skirmish_menu_surface_m1(position):
    # print("skirmish_menu_surface_m1")
    for obj in graphics_obj.menus_objects:
        for button in obj.buttons:
            button.press_button(position)
        for obj_list in obj.lists:
            obj_list.select_element(position)


def skirmish_menu_surface_m3(position):
    print("skirmish_menu_surface_m3")
