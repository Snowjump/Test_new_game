## Among Myth and Wonder
## buttons

from Screens.colors_catalog import *
from Screens.fonts_catalog import *

font_dic = {"tnr_font16" : tnr_font16,
            "arial_font14" : arial_font14}

color_dic = {"LineMainMenuColor1" : LineMainMenuColor1,
             "DarkText" : DarkText,
             "FillButton" : FillButton,
             "RockTunel" : RockTunel,
             "HighlightOption" : HighlightOption}


def element_button(screen, text, text_font, text_color, field_color, border_color, x, y, x_p, y_p, x_w, y_w,
                   border_thickness):
    # Simple basic button with a border and a single textbox

    # x - x-axis coordinate
    # y - y-axis coordinate
    # x_p - button width
    # y_p - button length
    # x_w - x-axis distance between border of a button and a text
    # y_w - y-axis distance between border of a button and a text
    # print("border_color - " + str(border_color))
    # print("x - " + str(x))
    # print("y - " + str(y))
    # print("x_p - " + str(x_p))
    # print("y_p - " + str(y_p))
    # print("x_w - " + str(x_w))
    # print("y_w - " + str(y_w))
    # print("border_thickness - " + str(border_thickness))

    # Button's field
    if field_color:
        pygame.draw.polygon(screen, color_dic[field_color], [[x, y], [x + x_p, y], [x + x_p, y + y_p], [x, y + y_p]])

    # Button's border
    pygame.draw.polygon(screen, color_dic[border_color], [[x, y], [x + x_p, y], [x + x_p, y + y_p], [x, y + y_p]],
                        border_thickness)

    # Single textbox inside button
    text_panel1 = font_dic[text_font].render(text, True, color_dic[text_color])
    screen.blit(text_panel1, [x + x_w, y + y_w])


def element_arrow_button(screen, direction, field_color, border_color, line_color, x, y, x_p, y_p, border_thickness,
                         line_thickness):
    # Basic button with a border and an arrow consisting of two lines

    # x - x-axis coordinate
    # y - y-axis coordinate
    # x_p - button width
    # y_p - button length

    # Button's field
    pygame.draw.polygon(screen, color_dic[field_color], [[x, y], [x + x_p, y], [x + x_p, y + y_p], [x, y + y_p]])

    # Button's border
    pygame.draw.polygon(screen, color_dic[border_color], [[x, y], [x + x_p, y], [x + x_p, y + y_p], [x, y + y_p]],
                        border_thickness)

    # Arrow lines
    point_1 = None
    point_2 = None
    point_3 = None
    if direction == "Left":
        point_1 = (x + x_p - 3, y + 3)
        point_2 = (x + 4, y + (y_p / 2) + 1)
        point_3 = (x + x_p - 3, y + y_p - 3)
    elif direction == "Right":
        point_1 = (x + 4, y + 3)
        point_2 = (x + x_p - 3, y + (y_p / 2) + 1)
        point_3 = (x + 4, y + y_p - 3)

    pygame.draw.lines(screen, color_dic[line_color], False, [point_1, point_2, point_3],
                      line_thickness)
