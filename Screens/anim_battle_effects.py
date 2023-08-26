## Miracle battles

from Resources import game_stats
import math
import pygame.draw
import pygame.font

WhiteColor = [255, 255, 255]

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


def white_buff_effect(screen, b, current_position):
    spread = (b.battle_display_time / 1000 - b.battle_last_change) / 1
    alpha = (abs((spread * 1000) % 1000 - 500)) / 5 * 2
    color = [220, 220, 220, 20 + alpha]

    x = int(current_position[0]) - int(b.battle_pov[0])
    y = int(current_position[1]) - int(b.battle_pov[1])

    draw_rect_alpha(screen, color, ((x - 1) * 96 + 1, (y - 1) * 96 + 1, 96, 96))


def message_float(screen, b):
    msg1 = ""
    k2 = 0
    if b.queue[0].obj_type == "Regiment":
        x = b.queue[0].position[0]
        y = b.queue[0].position[1]

    if b.primary in ["Wait message1", "Defend message1", "Damage message1", "Counterattack damage message1"]:
        k2 = 20

    # print("message_float")
    if b.anim_message == "Wait":
        msg = "Wait"
    elif b.anim_message == "Defend":
        msg = "Defend"
    else:  # Spell message
        msg = str(b.anim_message)

    if b.anim_message == "Damage and kills":
        x = b.damage_msg_position[0]
        y = b.damage_msg_position[1]
        msg = "Damage " + str(b.dealt_damage)
        msg1 = "Killed " + str(b.killed_creatures)

    spread = (b.battle_display_time / 1000 - b.battle_last_change) / 1
    k = (spread * 1000)/50
    # print("k - " + str(k))

    if b.queue[0].obj_type == "Regiment":
        x -= int(b.battle_pov[0])
        y -= int(b.battle_pov[1])

        text_NewGame1 = ArialFont16.render(msg, True, DarkText)
        screen.blit(text_NewGame1, [x * 96 + 10, (y - 1) * 96 - k - k2])

        if msg1 != "":
            text_NewGame2 = ArialFont16.render(msg1, True, DarkText)
            screen.blit(text_NewGame2, [x * 96 + 10, (y - 1) * 96 - k - k2 + 20])

    elif b.queue[0].obj_type == "Hero":
        if b.selected_ability is not None:  # Spell message
            x = int(b.selected_tile[0]) - int(b.battle_pov[0])
            y = int(b.selected_tile[1]) - int(b.battle_pov[1])
            text_NewGame1 = ArialFont16.render(msg, True, DarkText)
            screen.blit(text_NewGame1, [x * 96 + 10, (y - 1) * 96 - k - k2])

            # Damage and kills
            if b.dealt_damage > 0:
                msg1 = "Damage " + str(b.dealt_damage)
                msg2 = "Killed " + str(b.killed_creatures)

                text_NewGame1 = ArialFont16.render(msg1, True, DarkText)
                screen.blit(text_NewGame1, [x * 96 + 10, (y - 1) * 96 - k - k2 + 20])
                text_NewGame1 = ArialFont16.render(msg2, True, DarkText)
                screen.blit(text_NewGame1, [x * 96 + 10, (y - 1) * 96 - k - k2 + 40])
        else:
            yVar = game_stats.game_window_height - 800
            x = 400
            y = 724 + yVar
            text_NewGame1 = ArialFont16.render(msg, True, DarkText)
            screen.blit(text_NewGame1, [x, y - k - k2])


def spell_effect(screen, b, current_position):
    spell_effect_dictionary[b.selected_ability](screen, b, current_position)


def fire_arrows_effect(screen, b, current_position):
    spread = (b.battle_display_time / 1000 - b.battle_last_change) / 1
    # print("Spread " + str(spread))

    number = math.ceil(spread * 10 / 2.5)
    # print("Number " + str(number))
    if number == 0:
        number = 1

    x = int(current_position[0]) - int(b.battle_pov[0])
    y = int(current_position[1]) - int(b.battle_pov[1])

    x_centre = 48
    y_centre = 48

    img = game_stats.gf_battle_effects_dict["Battle_effects/flame_a_0" + str(number)]

    for element in b.positions_list:
        # screen.blit(img,
        #             [(x - 1) * 96 + 1 + x_centre,
        #              (y - 1) * 96 + 1 + y_centre])

        screen.blit(img,
                    [(x - 1) * 96 + 1 + element[0] + x_centre,
                     (y - 1) * 96 + 1 + element[1] + y_centre])


def lightning_bolts_effect(screen, b, current_position):
    spread = (b.battle_display_time / 1000 - b.battle_last_change) / 1
    # print("Spread " + str(spread))

    number = math.ceil(spread * 10 / 2.5)
    # print("Number " + str(number))
    if number == 0:
        number = 1

    x = int(current_position[0]) - int(b.battle_pov[0])
    y = int(current_position[1]) - int(b.battle_pov[1])

    x_centre = 48
    y_centre = 48

    img = game_stats.gf_battle_effects_dict["Battle_effects/lightning_bolt_a_0" + str(number)]

    for element in b.positions_list:
        # screen.blit(img,
        #             [(x - 1) * 96 + 1 + x_centre,
        #              (y - 1) * 96 + 1 + y_centre])

        screen.blit(img,
                    [(x - 1) * 96 + 1 + element[0] + x_centre,
                     (y - 1) * 96 + 1 + element[1] + y_centre])


def hail_effect(screen, b, current_position):
    spread = (b.battle_display_time / 1000 - b.battle_last_change) / 1
    # print("Spread " + str(spread))

    # number = math.ceil(spread * 10 / 2.5)

    x = int(current_position[0]) - int(b.battle_pov[0])
    y = int(current_position[1]) - int(b.battle_pov[1])

    x_centre = 48
    y_centre = 48

    img = game_stats.gf_battle_effects_dict["Battle_effects/icicle_a"]

    for element in b.positions_list:
        # screen.blit(img,
        #             [(x - 1) * 96 + 1 + x_centre,
        #              (y - 1) * 96 + 1 + y_centre])

        y_b = 30 - math.floor(math.fabs(element[0]) / 49 * 30)
        # print("element - " + str(element) + ", y_b - " + str(y_b))
        screen.blit(img,
                    [(x - 1) * 96 + 1 + element[0] + x_centre,
                     (y - 1) * 96 + 1 + element[1] + y_centre - math.ceil((20 + y_b) * (1 - spread))])


spell_effect_dictionary = {"Fire arrows" : fire_arrows_effect,
                           "Lightning bolts" : lightning_bolts_effect,
                           "Hail" : hail_effect}
