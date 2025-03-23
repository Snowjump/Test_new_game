## Among Myth and Wonder
## execute_order_funs

from Resources import game_stats
from Resources import game_battle
from Resources import battle_skills
from Resources import effect_classes
from Resources import common_selects
from Resources import algo_b_movement_range
from Resources import game_classes
from Resources.Game_Battle import defence_action_funs


def primary_move(b, unit, acting_army, enemy_army):
    if b.primary == "Move":
        print("execute_order - Move")
        x1 = int(b.queue[0].position[0])
        y1 = int(b.queue[0].position[1])
        TileNum1 = (y1 - 1) * game_stats.battle_width + x1 - 1

        # open_or_close_the_gate(b, TileNum1)  # develop more later

        print("game_battle .. execute_order() .. b.tile_trail:")
        print(str(b.tile_trail))
        print("")
        b.queue[0].position = b.tile_trail.pop(0)

        update_true = True
        if b.secondary == "Route":
            if b.queue[0].position[0] < 1 or b.queue[0].position[0] > game_stats.battle_width:
                update_true = False

        x2 = int(b.queue[0].position[0])
        y2 = int(b.queue[0].position[1])
        TileNum2 = (y2 - 1) * game_stats.battle_width + x2 - 1

        if update_true:
            if b.secondary == "Hit and fly":
                # This flying regiment is striking enemy from above
                # Therefore it is staying in the air
                b.battle_map[TileNum2].passing_unit_index = int(b.queue[0].number)
                b.battle_map[TileNum2].passing_army_id = int(b.queue[0].army_id)

            elif len(b.tile_trail) != 0:
                # Regular rules
                b.battle_map[TileNum2].passing_unit_index = int(b.queue[0].number)
                b.battle_map[TileNum2].passing_army_id = int(b.queue[0].army_id)

        if b.battle_map[TileNum1].army_id == b.queue[0].army_id \
                and b.battle_map[TileNum1].unit_index == b.queue[0].number:
            b.battle_map[TileNum1].army_id = None
            b.battle_map[TileNum1].unit_index = None

        b.battle_map[TileNum1].passing_army_id = None
        b.battle_map[TileNum1].passing_unit_index = None

        unit.position = [int(x2), int(y2)]
        unit.direction = game_battle.change_direction([x1, y1], [x2, y2])

        for skill in unit.skills:
            if skill.application == "Movement":
                if skill.quality == "Can fly":
                    unit.in_air = True
                    print("1) move_figure - " + str(b.move_figure))
                    if len(b.tile_trail) > 1:
                        if b.move_figure == "takeoff":
                            b.move_figure = "flying"
                    else:
                        if b.secondary == "Hit and fly":
                            # Not landing yet, but striking enemy from above
                            b.move_figure = "flying"
                        else:
                            b.move_figure = "landing"
                    print("2) move_figure - " + str(b.move_figure))
                    break

        if len(b.tile_trail) == 0:
            if b.secondary == "Hit and fly":
                # This flying regiment is striking enemy from above
                b.move_figure = "nosedive"
                print("b.secondary - " + str(b.secondary) + "; b.move_figure - " + str(b.move_figure))
            else:
                if update_true:
                    b.battle_map[TileNum2].unit_index = int(b.queue[0].number)
                    b.battle_map[TileNum2].army_id = int(b.queue[0].army_id)

                if unit.in_air:
                    unit.in_air = False
                    b.move_figure = None
            game_battle.apply_aura(unit, b, b.queue[0].army_id)
            b.tile_trail = None
            b.primary = None
            if b.secondary is None:
                battle_skills.passive_charge_track(unit)
                b.move_destination = None
                game_battle.complete_turn(b, 1.0)
            elif b.secondary == "Break the gates":
                b.primary = "Rotate"
            elif b.secondary == "Dock the wall":
                b.primary = "Rotate"
            elif b.secondary == "Melee attack":
                b.primary = "Rotate"
                print("end of movement: b.primary == Rotate; b.secondary == Melee attack")
                # print("b.enemy_army_id - " + str(b.enemy_army_id))
                game_battle.rotation_direction(b, acting_army, enemy_army)
            elif b.secondary == "Hit and fly":
                b.primary = "Hit from above"
                print("b.primary == Hit from above; b.secondary == Hit and fly")
                print("b.enemy_army_id - " + str(b.enemy_army_id))
            elif b.secondary == "Fly back":
                b.move_back_destination = None
                b.primary = "Damage message"
                # b.anim_message = "Damage and kills"
            elif b.secondary == "Route":
                battle_skills.passive_charge_track(unit)
                game_battle.battle_ending(b)

                if b.battle_stop:
                    # Unit has routed and battle is over
                    print("Unit has routed and battle is over")

                else:
                    b.secondary = None
                    if not update_true:
                        b.path = None
                        b.movement_grid = None
                        unit.deserted = True
                        b.queue.pop(0)
                        game_battle.advance_queue(b)
                    else:
                        game_battle.complete_turn(b, 1.0)


def primary_wait(b, unit):
    if b.queue[0].obj_type != "Hero":
        battle_skills.passive_charge_track(unit)
        b.anim_message.append(game_classes.Battle_Message(["Wait"], str(b.queue[0].obj_type),
                                                          (b.queue[0].position[0], b.queue[0].position[1])))
    else:
        b.anim_message.append(game_classes.Battle_Message(["Wait"], str(b.queue[0].obj_type)))
    b.primary = "Wait message"


def primary_wait_message(b):
    b.primary = "Wait message1"


def primary_wait_message1(b):
    b.primary = None
    b.anim_message = []
    game_battle.complete_turn(b, 0.5)


def primary_defend(b, unit, acting_hero):
    defence_value = defence_action_funs.defence_action_effect(int(unit.defence), acting_hero)
    base_missile_defence = 1
    missile_defence_value = defence_action_funs.defence_action_effect(int(base_missile_defence), acting_hero)
    defence_action_funs.defence_morale_restoration(unit, acting_hero)
    unit.effects.append(effect_classes.Battle_Effect("Defend action", True,
                                                     float(b.queue[0].time_act), float(b.queue[0].time_act + 1.0),
                                                     [effect_classes.Buff("Missile defence", missile_defence_value,
                                                                          "addition", None),
                                                      effect_classes.Buff("Defence", defence_value,
                                                                          "addition", None)]))

    battle_skills.passive_charge_track(unit)

    b.primary = "Defend message"
    if b.queue[0].obj_type != "Hero":
        b.anim_message.append(game_classes.Battle_Message(["Defend"], str(b.queue[0].obj_type),
                                                          (b.queue[0].position[0], b.queue[0].position[1])))
    else:
        b.anim_message.append(game_classes.Battle_Message(["Defend"], str(b.queue[0].obj_type)))


def primary_defend_message(b):
    b.primary = "Defend message1"


def primary_defend_message1(b):
    b.primary = None
    b.anim_message = []
    game_battle.complete_turn(b, 1.0)


def primary_pass(b):
    print(str(b.primary) + ", b.selected_ability - " + str(b.selected_ability))
    b.primary = "Pass1"
    # b.anim_message = str(b.selected_ability)


def primary_pass1(b, acting_army, acting_hero):
    print(str(b.primary) + ", b.queue[0].obj_type - " + str(b.queue[0].obj_type))
    b.primary = None
    b.anim_message = []

    b.list_of_schools = []
    b.list_of_abilities = []
    b.ability_index = 0
    b.school_index = 0
    b.selected_school = None
    b.selected_ability = None
    if b.queue[0].obj_type == "Hero":
        game_battle.complete_turn(b, acting_hero.initiative)
    elif b.queue[0].obj_type == "Regiment":
        unit = acting_army.units[b.queue[0].number]
        game_battle.complete_turn(b, unit.initiative)


def primary_rotate(b, acting_army, acting_unit, enemy_army):
    # print("b.primary == Rotate")
    # print("b.enemy_army_id - " + str(b.enemy_army_id))
    if b.secondary == "Break the gates":
        b.primary = "Break the gates"
        b.secondary = None
        acting_unit.direction = game_battle.change_direction(acting_unit.position, b.target_destination)

    elif b.secondary == "Dock the wall":
        b.primary = "Dock the wall"
        b.secondary = None
        acting_unit.direction = game_battle.change_direction(acting_unit.position, b.target_destination)

    elif b.secondary == "Melee attack":
        b.primary = "Melee attack"
        b.secondary = None
        acting_unit.direction = game_battle.change_direction(acting_unit.position, b.target_destination)
        TileNum2 = (b.target_destination[1] - 1) * game_stats.battle_width + b.target_destination[0] - 1
        primary_target = enemy_army.units[b.battle_map[TileNum2].unit_index]
        if primary_target.counterattack:
            primary_target.direction = game_battle.change_direction(primary_target.position, acting_unit.position)

        b.damage_dealt_positions.append(tuple(primary_target.position))
        print("b.damage_dealt_positions: " + str(b.damage_dealt_positions))

        game_battle.print_rotating_units(b)
        print("")

    elif b.secondary == "Counterattack":
        b.primary = "Counterattack"
        b.secondary = None

        b.damage_dealt_positions.append(tuple(b.queue[0].position))
        print("b.damage_dealt_positions: " + str(b.damage_dealt_positions))

        game_battle.print_rotating_units(b)
        print("")

    elif b.secondary == "Ranged attack":
        acting_unit.direction = str(b.changed_direction)

        b.primary = "Ranged attack"
        b.secondary = None

        b.damage_dealt_positions.append(tuple(b.target_destination))
        print("b.damage_dealt_positions: " + str(b.damage_dealt_positions))

        print("")


def primary_melee_attack(b, acting_hero, acting_unit, enemy_hero, enemy_army):
    # print("b.primary == Melee attack")
    # print("b.enemy_army_id - " + str(b.enemy_army_id))
    TileNum2 = (b.target_destination[1] - 1) * game_stats.battle_width + b.target_destination[0] - 1

    unit_at = acting_unit.direction
    primary_target = enemy_army.units[b.battle_map[TileNum2].unit_index]
    unit_df = primary_target.direction

    angle = game_battle.attack_angle(unit_at, unit_df)

    # Let AI player choose a melee attack
    # print("b.realm_in_control - " + str(b.realm_in_control))
    if b.realm_in_control == "Neutral":  # If enemy doesn't have a realm
        game_battle.choose_melee_attack_by_type(b, acting_unit, primary_target)
    else:
        realm = common_selects.select_realm_by_name(b.realm_in_control)
        if realm.AI_player:
            game_battle.choose_melee_attack_by_type(b, acting_unit, primary_target)

    b.perform_attack = game_battle.form_list_of_attackers(b, acting_unit)
    game_battle.complete_melee_attack(b, acting_unit, primary_target, angle, acting_hero, enemy_hero)

    if b.battle_stop:
        # Enemy is killed and battle is over
        print("Enemy is killed in melee and battle is over")
    else:
        b.primary = "Damage message"
        # b.anim_message = "Damage and kills"


def primary_hit_from_above(b, acting_hero, acting_unit, enemy_army, enemy_hero):
    print("b.primary == Hit from above")
    print("b.enemy_army_id - " + str(b.enemy_army_id))
    TileNum = (b.target_destination[1] - 1) * game_stats.battle_width + b.target_destination[0] - 1
    primary_target = enemy_army.units[b.battle_map[TileNum].unit_index]

    angle = "Above"
    b.perform_attack = game_battle.form_list_of_attackers(b, acting_unit)
    game_battle.complete_melee_attack(b, acting_unit, primary_target, angle, acting_hero, enemy_hero)

    if b.battle_stop:
        # Enemy is killed and battle is over
        print("Enemy is killed in melee and battle is over")
    else:
        b.primary = "Move"
        b.secondary = "Fly back"
        b.move_destination = [int(b.move_back_destination[0]), int(b.move_back_destination[1])]
        start = b.queue[0].position
        MP = acting_unit.attacks[b.attack_type_index].range_limit

        b.path, b.movement_grid = algo_b_movement_range.pseudo_astar(None, start, MP, b, "Flight")
        game_battle.action_order(b, "Move", "Fly back")


def primary_break_the_gates(b):
    TileNum = (b.target_destination[1] - 1) * game_stats.battle_width + b.target_destination[0] - 1
    game_battle.gates_destruction(b, TileNum)
    # b.anim_message either "The gate has been destroyed" or "The gate withstood the attack"
    b.primary = "Damage message"


def primary_dock_the_wall(b):
    game_battle.dock_the_wall(b)
    # b.anim_message either "The gate has been destroyed" or "The gate withstood the attack"
    b.primary = "Damage message"


def primary_damage_message(b):
    print("b.primary == Damage message")
    print("b.dealt_damage - " + str(b.dealt_damage) + "; b.killed_creatures - " + str(b.killed_creatures))
    print("")
    b.primary = "Damage message1"
    # if b.anim_message == "Damage and kills":
    #     b.anim_message = "Damage and kills"
    # elif b.anim_message == "Gate busting result":
    #     b.anim_message = "Gate busting result"
    # elif b.anim_message == "Docking the wall":
    #     b.anim_message = "Docking the wall"


def primary_damage_message1(b, acting_army, acting_unit, enemy_army):
    print("b.primary == Damage message1")
    b.primary = None
    b.anim_message = []
    b.damage_dealt_positions = []
    b.dealt_damage = 0
    b.killed_creatures = 0

    TileNum2 = (b.target_destination[1] - 1) * game_stats.battle_width + b.target_destination[0] - 1
    if b.battle_map[TileNum2].army_id:
        enemy_unit = enemy_army.units[b.battle_map[TileNum2].unit_index]

        # Check if enemy unit is routing or should start routing
        if enemy_unit.morale <= 0.0 or b.attack_name == "Hit and fly":
            b.secondary = None
            game_battle.complete_turn(b, 1.0)
        else:
            # Check if attacked unit can counterattack back
            if enemy_unit.counterattack > 0 and len(enemy_unit.crew) > 0 and b.secondary != "Ranged attack":
                print(str(enemy_army.owner) + " - " + enemy_unit.name + " will counterattack")
                b.primary = "Rotate"
                b.secondary = "Counterattack"
                # Decrease available counterattacks
                decrease = True
                # Check for skills with cat reflex
                for skill in enemy_unit.skills:
                    if skill.application == "Counterattack":
                        if skill.quality == "Unlimited counterattacks":
                            decrease = False
                            break
                if decrease:
                    enemy_unit.counterattack -= 1

                if not enemy_unit.engaged:
                    enemy_unit.engaged = True

                print(enemy_unit.name + " position - " + str(enemy_unit.position))
                b.defending_rotate.append(game_classes.Rotation_Data(tuple(enemy_unit.position),
                                                                     b.battle_map[TileNum2].unit_index,
                                                                     b.battle_map[TileNum2].army_id))

                game_battle.rotation_direction(b, acting_army, enemy_army)
                # print_rotating_units(b)

            else:
                b.secondary = None
                game_battle.complete_turn(b, acting_unit.initiative)
    else:
        # Defending unit has been killed before it could counterattack
        game_battle.complete_turn(b, acting_unit.initiative)


def primary_counterattack(b, acting_army, acting_hero, enemy_army, enemy_hero):
    print("b.primary == Counterattack")

    TileNum2 = (b.target_destination[1] - 1) * game_stats.battle_width + b.target_destination[0] - 1
    primary_target = acting_army.units[b.queue[0].number]
    unit_df = primary_target.direction
    print(str(TileNum2) + " - " + str(b.target_destination))

    unit = enemy_army.units[b.battle_map[TileNum2].unit_index]
    unit_at = unit.direction

    angle = game_battle.attack_angle(unit_at, unit_df)

    game_battle.choose_melee_attack_by_type(b, unit, primary_target)

    b.perform_attack = game_battle.form_list_of_attackers(b, unit)
    game_battle.complete_melee_attack(b, unit, primary_target, angle, enemy_hero, acting_hero)

    if b.battle_stop:
        # Enemy is killed and battle is over
        print("Enemy is killed in counterattack and battle is over")

    else:
        b.primary = "Counterattack damage message"
        # b.anim_message = "Damage and kills"


def primary_counterattack_damage_message(b):
    b.primary = "Counterattack damage message1"
    # b.anim_message = "Damage and kills"
    print("")


def primary_counterattack_damage_message1(b):
    b.primary = None
    b.anim_message = []
    b.damage_dealt_positions = []
    b.dealt_damage = 0
    b.killed_creatures = 0
    game_battle.complete_turn(b, 1.0)


def primary_ranged_attack(b, acting_hero, acting_unit, enemy_army, enemy_hero):
    TileNum2 = (b.target_destination[1] - 1) * game_stats.battle_width + b.target_destination[0] - 1
    # print("b.target_destination - " + str(b.target_destination) + " TileNum2 - " + str(TileNum2))
    # print("b.enemy_army_id - " + str(b.enemy_army_id) + " b.queue[0].army_id - " + str(b.queue[0].army_id))
    # print("b.queue[0].army_id - " + str(b.queue[0].army_id) + " owner - " + str(b.queue[0].owner))
    # print("b.queue[0].army_id - " + str(b.enemy_army_id) + " owner - " + str(army.owner))
    primary_target = enemy_army.units[b.battle_map[TileNum2].unit_index]

    # print("Again, unit object - " + str(unit) + " len(unit.crew) - " + str(len(unit.crew)))
    game_battle.complete_ranged_attack(b, acting_unit, primary_target, acting_hero, enemy_hero)

    if b.battle_stop:
        # Enemy is killed and battle is over
        print("Enemy is killed in ranged attack and battle is over")

    else:
        b.primary = "Damage message"
        # b.anim_message = "Damage and kills"
        b.secondary = "Ranged attack"
