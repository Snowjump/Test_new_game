## Among Myth and Wonder
## anim_battle_message

from Screens.colors_catalog import *
from Screens.fonts_catalog import *

from Resources import game_stats


def manage_messages(screen, b):
    spread = (b.battle_display_time / 1000 - b.battle_last_change) / 1
    k = (spread * 1000) / 50
    k1 = 0
    if b.primary in ["Wait message1", "Defend message1", "Damage message1", "Counterattack damage message1", "Pass1"]:
        k1 = 20

    for message in b.anim_message:
        if message.position:  # Regiment or Structure
            x = message.position[0] - b.battle_pov[0]
            y = message.position[1] - b.battle_pov[1]
            x_pos = x * 96 + 10
            y_pos = (y - 1) * 96 - k - k1
        else:  # Hero
            yVar = game_stats.game_window_height - 800
            x = 400
            y = 724 + yVar
            x_pos = x
            y_pos = y - k - k1
        line = 0
        for text_line in message.text:
            text_NewGame1 = arial_font16.render(text_line, True, DarkText)
            screen.blit(text_NewGame1, [x_pos, y_pos + (20 * line)])
            line += 1
