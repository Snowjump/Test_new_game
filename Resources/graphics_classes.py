## Among Myth and Wonder
## graphics_classes

import pygame.draw

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
        self.lists = []  # List of interactable list objects


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

    def draw_button(self, screen):
        buttons.element_button(screen, self.text, self.text_font, self.text_color, self.field_color, self.border_color,
                               self.x, self.y, self.x_p, self.y_p, self.x_w, self.y_w, self.border_thickness)

    def press_button(self, position):
        if self.x < position[0] < self.x + self.x_p and self.y < position[1] < self.y + self.y_p:
            self.function()


class Battle_Text_Button(Text_Button):
    def press_button(self, position):
        if self.x < position[0] < self.x + self.x_p and self.y < position[1] < self.y + self.y_p:
            self.function()
            b = game_stats.present_battle
            b.button_pressed = True
            print("b.button_pressed is " + str(b.button_pressed))


class Arrow_Button:
    def __init__(self, name, function, direction, field_color, border_color, line_color, x, y, x_p, y_p,
                 border_thickness, line_thickness, x_s=0, y_s=0):
        self.name = name
        self.function = function
        self.direction = direction
        self.field_color = field_color
        self.border_color = border_color
        self.line_color = line_color
        self.x = x
        self.y = y
        self.x_p = x_p
        self.y_p = y_p
        self.border_thickness = border_thickness
        self.line_thickness = line_thickness
        self.x_s = x_s
        self.y_s = y_s

    def draw_button(self, screen):
        buttons.element_arrow_button(screen, self.direction, self.field_color, self.border_color, self.line_color,
                                     self.x, self.y, self.x_p, self.y_p, self.border_thickness, self.line_thickness,
                                     self.x_s, self.y_s)

    def press_button(self, position):
        if self.x < position[0] < self.x + self.x_p and self.y < position[1] < self.y + self.y_p:
            self.function()


class Text_List:
    def __init__(self, name, function, obj_list, square, text_font, text_color, underline_color, underline_thickness,
                 accent_color, accent_index, x, y, x_p, y_p, line_indent):
        self.name = name
        self.function = function
        self.obj_list = obj_list
        self.square = square  # List of 4 (int) values [100, 30, 200, 40]
        self.text_font = text_font
        self.text_color = text_color
        self.underline_color = underline_color
        self.underline_thickness = underline_thickness
        self.accent_color = accent_color
        self.accent_index = accent_index
        self.x = x
        self.y = y
        self.x_p = x_p
        self.y_p = y_p
        self.line_indent = line_indent

    def draw_list(self, screen):
        x = self.x
        y = self.y
        underline_number = 0
        for line in self.obj_list:
            text_line = self.text_font.render(line, True, self.text_color)
            screen.blit(text_line, [x, y])

            # Grey underlines
            pygame.draw.lines(screen, self.underline_color, False,
                              [(self.x, self.y + underline_number * self.y_p + self.line_indent),
                               (self.x + self.x_p, self.y + underline_number * self.y_p + self.line_indent)],
                              self.underline_thickness)
            underline_number += 1
            y += self.y_p

        pygame.draw.lines(screen, self.accent_color, False,
                          [(self.x, self.y + game_stats.level_index * self.y_p + self.line_indent),
                           (self.x + self.x_p, self.y + game_stats.level_index * self.y_p + self.line_indent)],
                          self.underline_thickness)

    def select_element(self, position):
        if self.square[0] < position[0] < self.square[2] and self.square[1] < position[1] < self.square[3]:
            self.function(position)
