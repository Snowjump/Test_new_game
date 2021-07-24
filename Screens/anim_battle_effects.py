## Miracle battles

from Resources import game_stats
import math
import pygame.draw
import pygame.font

TitleText = [0xFF, 0xFF, 0x99]
DarkText = [0x11, 0x11, 0x11]

ArialFont16 = pygame.font.SysFont('arial', 16)
ArialFont16.set_bold(True)


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def border_blipping(color):
    spread = (game_stats.display_time / 1000 - game_stats.last_change) / 1
    # -500 - 500
    # 500 - 0 - 500
    # 200 - 0 - 200
    alpha = (abs((spread * 1000) % 1000 - 500)) / 5 * 2
    color[3] = 20 + alpha  # 20 - 220
    # print(alpha)
    return color


def damage_dealt_red(screen, b, owner, unit_index, current_position):
    TileNum2 = (b.target_destination[1] - 1) * game_stats.battle_width + b.target_destination[0] - 1
    if ((b.primary == "Melee attack" or b.primary == "Ranged attack") and unit_index == b.battle_map[
        TileNum2].unit_index and owner == b.enemy) or (
            b.primary == "Counterattack" and unit_index in b.attacking_rotate and owner == b.realm_in_control):
        # print("defending_rotate now is - " + str(b.defending_rotate) + " and unit_index is - " + str(unit_index))
        spread = (b.battle_display_time / 1000 - b.battle_last_change) / 1
        alpha = (abs((spread * 1000) % 1000 - 500)) / 5 * 2
        color = [255, 20, 20, 20 + alpha]

        x = int(current_position[0]) - int(b.battle_pov[0])
        y = int(current_position[1]) - int(b.battle_pov[1])

        draw_rect_alpha(screen, color, ((x - 1) * 96 + 1, (y - 1) * 96 + 1, 96, 96))


def message_float(screen, b):
    msg1 = ""
    k2 = 0
    x = b.queue[0].position[0]
    y = b.queue[0].position[1]

    if b.primary in ["Wait message1", "Defend message1", "Damage message1", "Counterattack damage message1"]:
        k2 = 20

    # print("message_float")
    if b.anim_message == "Wait":
        msg = "Wait"
    elif b.anim_message == "Defend":
        msg = "Defend"

    if b.anim_message == "Damage and kills":
        x = b.damage_msg_position[0]
        y = b.damage_msg_position[1]
        msg = "Damage " + str(b.dealt_damage)
        msg1 = "Killed " + str(b.killed_creatures)

    spread = (b.battle_display_time / 1000 - b.battle_last_change) / 1
    k = (spread * 1000)/50
    # print("k - " + str(k))

    x -= int(b.battle_pov[0])
    y -= int(b.battle_pov[1])

    text_NewGame1 = ArialFont16.render(msg, True, DarkText)
    screen.blit(text_NewGame1, [x * 96 + 10, (y - 1) * 96 - k - k2])

    if msg1 != "":
        text_NewGame2 = ArialFont16.render(msg1, True, DarkText)
        screen.blit(text_NewGame2, [x * 96 + 10, (y - 1) * 96 - k - k2 + 20])
