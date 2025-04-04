## Among Myth and Wonder
## graphics_funs

from Resources import game_stats


def draw_panel_objects(screen, graphics_objects_list):
    for obj in graphics_objects_list:
        if hasattr(obj, 'draw_panel'):
            obj.draw_panel(screen)
        for button in obj.buttons:
            button.draw_button(screen)
        for obj_list in obj.lists:
            obj_list.draw_list(screen)
        for text_box in obj.text_boxes:
            text_box.draw_box(screen)


def find_graphics_object(obj_name, obj_list):
    for obj in obj_list:
        if obj.name == obj_name:
            return obj


def key_action_panel(graphics_objects_list, key_action):
    for obj in graphics_objects_list:
        for text_box in obj.text_boxes:
            if text_box.type_text:
                if key_action == 27:  # Escape
                    text_box.deselect_box()
                elif key_action == 8:  # Backspace
                    if text_box.text:  # Remove last character from text line
                        text_box.text = text_box.text[:-1]
                else:  # Add a character to text line
                    if game_stats.input_text.isalnum() or game_stats.input_text.isspace():
                        print(str(game_stats.input_text))
                        text_box.text += game_stats.input_text


def m1_single_click(graphics_objects_list, position):
    for obj in graphics_objects_list:
        for button in obj.buttons:
            button.press_button(position)
        for obj_list in obj.lists:
            obj_list.select_element(position)
        for text_box in obj.text_boxes:
            text_box.press_box(position)
