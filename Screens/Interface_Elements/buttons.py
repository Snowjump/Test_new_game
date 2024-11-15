## Among Myth and Wonder
## buttons

from Screens.colors_catalog import *
from Screens.fonts_catalog import *

font_dic = {"arial_font14" : arial_font14}

color_dic = {"LineMainMenuColor1" : LineMainMenuColor1,
             "DarkText" : DarkText,
             "FillButton" : FillButton}


def element_button(screen, text, text_font, text_color, field_color, border_color, x, y, x_p, y_p, x_w, y_w,
                   border_thickness):
    # Simple basic button with border and single textbox

    # x - x-axis coordinate
    # y - y-axis coordinate
    # x_p - button width
    # y_p - button length
    # x_w - x-axis distance between border of a button and a text
    # y_w - y-axis distance between border of a button and a text

    # Button's field
    pygame.draw.polygon(screen, color_dic[field_color],
                        [[x, y], [x + x_p, y], [x + x_p, y + y_p], [x, y + y_p]])

    # Button's border
    pygame.draw.polygon(screen, color_dic[border_color], [[x, y], [x + x_p, y], [x + x_p, y + y_p], [x, y + y_p]],
                        border_thickness)

    # Single textbox inside button
    text_panel1 = font_dic[text_font].render(text, True, color_dic[text_color])
    screen.blit(text_panel1, [x + x_w, y + y_w])

