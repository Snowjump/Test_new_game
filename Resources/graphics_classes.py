## Among Myth and Wonder
## graphics_classes

from Screens.Interface_Elements import buttons

from Resources import game_stats


class Resource_Ribbon_Item:
    def __init__(self, name, quantity, delta):
        self.name = name
        self.quantity = quantity
        self.delta = delta  # Change in quantity since last turn


class Panel:
    def __init__(self, name):
        self.name = name
        self.buttons = []  # List of interactable buttons objects


class Text_Button:
    def __init__(self, name, function, text, text_font, text_color, field_color, border_color, x, y, x_p, y_p,
                 x_w, y_w, border_thickness):
        self.name = name
        self.function = function
        self.text = text
        self.text_font = text_font
        self.text_color = text_color
        self.field_color = field_color
        self.border_color = border_color
        self.x = x
        self.y = y
        self.x_p = x_p
        self.y_p = y_p
        self.x_w = x_w
        self.y_w = y_w
        self.border_thickness = border_thickness

    def draw_text_button(self, screen):
        buttons.element_button(screen, self.text, self.text_font, self.text_color, self.field_color, self.border_color,
                               self.x, self.y, self.x_p, self.y_p, self.x_w, self.y_w, self.border_thickness)

    def press_text_button(self, position):
        if self.x < position[0] < self.x + self.x_p and self.y < position[1] < self.y + self.y_p:
            self.function()
            b = game_stats.present_battle
            b.button_pressed = True
            print("b.button_pressed is " + str(b.button_pressed))

