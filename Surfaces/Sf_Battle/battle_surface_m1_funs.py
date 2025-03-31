## Among Myth and Wonder
## battle_surface_m1_funs

from Resources import graphics_obj


def manage_clicks(position, b):
    for obj in graphics_obj.battle_objects:
        for button in obj.buttons:
            button.press_button(position)
