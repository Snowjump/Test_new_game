## Among Myth and Wonder
## sf_entrance_menu

from Resources import graphics_obj


def entrance_menu_keys(key_action):
    pass


def entrance_menu_surface_m1(position):
    print("entrance_menu_surface_m1")
    for obj in graphics_obj.menus_objects:
        for button in obj.buttons:
            button.press_button(position)


def entrance_menu_surface_m3(position):
    print("entrance_menu_surface_m3")
