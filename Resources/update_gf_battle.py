## Among Myth and Wonder
## update_gf_battle

import pygame.draw

from Resources import game_stats
from Resources import game_obj

from Content import objects_img_catalog
from Content import terrain_seasons
from Content import ability_catalog

WhiteColor = (255, 255, 255)


def battle_update_sprites():
    game_stats.gf_terrain_dict = {}
    game_stats.gf_obstacle_dict = {}
    game_stats.gf_regiment_dict = {}
    game_stats.gf_hero_dict = {}

    # Terrain border 96x96
    misc_img = pygame.image.load('img/Terrains/border_96_96_170.png').convert_alpha()
    # misc_img.set_colorkey(WhiteColor)
    game_stats.gf_terrain_dict["Terrains/border_96_96_170"] = misc_img

    for battle in game_obj.game_battles:
        if battle.attacker_realm == game_stats.player_power or \
                battle.defender_realm == game_stats.player_power:

            for TileObj in battle.battle_map:
                # Terrain
                if battle.conditions not in game_stats.gf_terrain_dict:
                    terrain_img = pygame.image.load('img/Terrains/' + TileObj.conditions + '.png').convert()
                    game_stats.gf_terrain_dict[str(TileObj.conditions)] = terrain_img

                # Objects
                # -------
                if TileObj.map_object is not None:
                    # Obstacles
                    if TileObj.map_object.obj_type == "Obstacle":
                        obj_cal = objects_img_catalog.object_calendar[TileObj.map_object.obj_name]
                        season = terrain_seasons.terrain_calendar[TileObj.terrain][game_stats.game_month]
                        number_variations = objects_img_catalog.object_variations[TileObj.map_object.obj_name]
                        for var in range(1, number_variations + 1):
                            if obj_cal[season] + "_0" + str(var) not in game_stats.gf_obstacle_dict:
                                obj_img = pygame.image.load('img/' +
                                                            TileObj.map_object.img_path + obj_cal[season] + "_0" +
                                                            str(var) + '.png').convert_alpha()
                                obj_img.set_colorkey(WhiteColor)
                                game_stats.gf_obstacle_dict[str(obj_cal[season]) + "_0" + str(var)] = obj_img

                    # Battle map structures
                    elif TileObj.map_object.obj_type == "Structure":
                        if TileObj.map_object.obj_name not in game_stats.gf_obstacle_dict:
                            obj_img = pygame.image.load('img/' +
                                                        TileObj.map_object.img_path +
                                                        '.png').convert_alpha()
                            obj_img.set_colorkey(WhiteColor)
                            game_stats.gf_obstacle_dict[str(TileObj.map_object.obj_name)] = obj_img

            for army in game_obj.game_armies:
                if army.army_id == game_stats.attacker_army_id or army.army_id == game_stats.defender_army_id:
                    print("army.army_id - " + str(army.army_id))
                    # Creatures
                    for unit in army.units:
                        for creature in unit.crew:
                            if creature.img_source + "/" + creature.img + "_r" not in game_stats.gf_regiment_dict:
                                army_img = pygame.image.load(
                                    'img/Creatures/' + str(creature.img_source) + "/" + str(creature.img) + '_r.png')
                                army_img.set_colorkey(WhiteColor)
                                game_stats.gf_regiment_dict[str(creature.img_source + "/" + creature.img
                                                                + "_r")] = army_img

                            if creature.img_source + "/" + creature.img + "_l" not in game_stats.gf_regiment_dict:
                                army_img = pygame.image.load(
                                    'img/Creatures/' + str(creature.img_source) + "/" + str(creature.img) + '_l.png')
                                army_img.set_colorkey(WhiteColor)
                                game_stats.gf_regiment_dict[str(creature.img_source + "/" + creature.img
                                                                + "_l")] = army_img

                    # Heroes
                    if army.hero is not None:
                        if army.hero.img + "/" + army.hero.img_source + "_r" not in game_stats.gf_hero_dict:
                            army_img = pygame.image.load('img/Heroes/' + str(army.hero.img_source) + "/" +
                                                         str(army.hero.img) + '_r.png')
                            army_img.set_colorkey(WhiteColor)
                            game_stats.gf_hero_dict[str(army.hero.img_source + "/" + army.hero.img + "_r")] = army_img

                        if army.hero.img + "/" + army.hero.img_source + "_l" not in game_stats.gf_hero_dict:
                            army_img = pygame.image.load('img/Heroes/' + str(army.hero.img_source) + "/" +
                                                         str(army.hero.img) + '_l.png')
                            army_img.set_colorkey(WhiteColor)
                            game_stats.gf_hero_dict[str(army.hero.img_source + "/" + army.hero.img + "_l")] = army_img

            if battle.battle_type == "Siege":
                # Add siege machines
                machine_img = pygame.image.load('img/Creatures/siege_machines/battering_ram' + '_l.png')
                machine_img.set_colorkey(WhiteColor)
                game_stats.gf_regiment_dict[str('img/Creatures/siege_machines/battering_ram' + "_l")] = machine_img

                machine_img = pygame.image.load('img/Creatures/siege_machines/battering_ram' + '_r.png')
                machine_img.set_colorkey(WhiteColor)
                game_stats.gf_regiment_dict[str('img/Creatures/siege_machines/battering_ram' + "_r")] = machine_img

                machine_img = pygame.image.load('img/Creatures/siege_machines/siege_tower' + '_l.png')
                machine_img.set_colorkey(WhiteColor)
                game_stats.gf_regiment_dict[str('img/Creatures/siege_machines/siege_tower' + "_l")] = machine_img

                machine_img = pygame.image.load('img/Creatures/siege_machines/siege_tower' + '_r.png')
                machine_img.set_colorkey(WhiteColor)
                game_stats.gf_regiment_dict[str('img/Creatures/siege_machines/siege_tower' + "_r")] = machine_img

                # Icon - pick up siege machine
                misc_img = pygame.image.load('img/Icons/pick_up_siege_machine.png').convert_alpha()
                misc_img.set_colorkey(WhiteColor)
                game_stats.gf_misc_img_dict["Icons/pick_up_siege_machine"] = misc_img

                # Icon - drop siege machine
                misc_img = pygame.image.load('img/Icons/drop_siege_machine.png').convert_alpha()
                misc_img.set_colorkey(WhiteColor)
                game_stats.gf_misc_img_dict["Icons/drop_siege_machine"] = misc_img

            print("gf_regiment_dict: " + str(game_stats.gf_regiment_dict))
            break


def update_misc_sprites():
    game_stats.gf_misc_img_dict = {}

    # Icon - card effect
    misc_img = pygame.image.load('img/Icons/eff.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/eff"] = misc_img

    # Icon - battle hourglass
    misc_img = pygame.image.load('img/Icons/battle_hourglass.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/battle_hourglass"] = misc_img

    # Icon - battle shield
    misc_img = pygame.image.load('img/Icons/battle_shield.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/battle_shield"] = misc_img

    # Paper background
    misc_img = pygame.image.load('img/Icons/paper_3_square_560_x_60.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/paper_3_square_560_x_60"] = misc_img

    # Attack types
    # ------------
    # Icon - Melee attack
    misc_img = pygame.image.load('img/Icons/Melee.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/Melee assault"] = misc_img

    # Icon - Ranged attack
    misc_img = pygame.image.load('img/Icons/Ranged.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/Shooting"] = misc_img

    # Icon - Hit and fly attack
    misc_img = pygame.image.load('img/Icons/hit_and_fly.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/Hit and fly"] = misc_img

    # Icon - Hit and run attack
    misc_img = pygame.image.load('img/Icons/hit_and_run.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/Hit and run"] = misc_img

    # Icon - Abilities
    misc_img = pygame.image.load('img/Icons/Abilities.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/Abilities"] = misc_img

    # Icon - Flame attack (for dragons and drakes)
    misc_img = pygame.image.load('img/Icons/flame_attack.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/Dragon breath"] = misc_img
    game_stats.gf_misc_img_dict["Icons/Drake breath"] = misc_img

    # --------------------

    # Icon - Arrow next
    misc_img = pygame.image.load('img/Icons/arrow_next_full.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/arrow_next_full"] = misc_img

    # Icon - Abilities
    misc_img = pygame.image.load('img/Icons/abilities_icon.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/abilities_icon"] = misc_img

    # Icon - Broken ranged attack
    misc_img = pygame.image.load('img/Icons/broken_ranged_attack.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/broken_ranged_attack"] = misc_img

    # Icon - Full ranged attack
    misc_img = pygame.image.load('img/Icons/ranged_attack.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/ranged_attack"] = misc_img

    # Melee attack icons
    # ------------------
    # Icon - 1 melee attack north-west
    misc_img = pygame.image.load('img/Icons/melee_attack_nw.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/melee_attack_nw"] = misc_img

    # Icon - 2 melee attack west
    misc_img = pygame.image.load('img/Icons/melee_attack_w.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/melee_attack_w"] = misc_img

    # Icon - 3 melee attack south-west
    misc_img = pygame.image.load('img/Icons/melee_attack_sw.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/melee_attack_sw"] = misc_img

    # Icon - 4 melee attack north
    misc_img = pygame.image.load('img/Icons/melee_attack_n.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/melee_attack_n"] = misc_img

    # Icon - 5 melee attack south
    misc_img = pygame.image.load('img/Icons/melee_attack_s.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/melee_attack_s"] = misc_img

    # Icon - 6 melee attack north-east
    misc_img = pygame.image.load('img/Icons/melee_attack_ne.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/melee_attack_ne"] = misc_img

    # Icon - 7 melee attack east
    misc_img = pygame.image.load('img/Icons/melee_attack_e.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/melee_attack_e"] = misc_img

    # Icon - 8 melee attack south-east
    misc_img = pygame.image.load('img/Icons/melee_attack_se.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/melee_attack_se"] = misc_img

    # --------------------------------

    # Icon - break gates (for battering rams)
    misc_img = pygame.image.load('img/Icons/break_gates.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/break_gates"] = misc_img

    # Icon - wall contact (for siege towers)
    misc_img = pygame.image.load('img/Icons/wall_contact.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/wall_contact"] = misc_img

    # --------------------------------

    # Icon - Mana icon
    misc_img = pygame.image.load('img/Icons/mana_icon.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/mana_icon"] = misc_img

    # Icon - paper 3 square 40
    misc_img = pygame.image.load('img/Icons/paper_3_square_40.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/paper_3_square_40"] = misc_img

    # if battle.battle_type == "Siege":
    # Icon - pick up siege machine
    misc_img = pygame.image.load('img/Icons/pick_up_siege_machine.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/pick_up_siege_machine"] = misc_img

    # Icon - drop siege machine
    misc_img = pygame.image.load('img/Icons/drop_siege_machine.png').convert_alpha()
    misc_img.set_colorkey(WhiteColor)
    game_stats.gf_misc_img_dict["Icons/drop_siege_machine"] = misc_img


def add_structure_obstacle_sprites(list_of_structures):
    for structure in list_of_structures:
        if structure[0] not in game_stats.gf_obstacle_dict:
            obj_img = pygame.image.load('img/' +
                                        structure[1] +
                                        '.png').convert_alpha()
            obj_img.set_colorkey(WhiteColor)
            game_stats.gf_obstacle_dict[str(structure[0])] = obj_img


def add_obstacle_sprites(tile_object, month, obstacle_name, img_path):
    obj_cal = objects_img_catalog.object_calendar[obstacle_name]
    season = terrain_seasons.terrain_calendar[tile_object.terrain][month]
    number_variations = objects_img_catalog.object_variations[obstacle_name]
    for var in range(1, number_variations + 1):
        if obj_cal[season] + "_0" + str(var) not in game_stats.gf_obstacle_dict:
            obj_img = pygame.image.load('img/' +
                                        img_path + obj_cal[season] + "_0" +
                                        str(var) + '.png').convert_alpha()
            obj_img.set_colorkey(WhiteColor)
            game_stats.gf_obstacle_dict[str(obj_cal[season]) + "_0" + str(var)] = obj_img


def add_school_misc_sprites(school):
    if "Schools/" + school not in game_stats.gf_misc_img_dict:
        misc_img = pygame.image.load('Img/Abilities/Schools/' + school_imgs[school] + '.png').convert_alpha()
        misc_img.set_colorkey(WhiteColor)
        game_stats.gf_misc_img_dict["Schools/" + school_imgs[school]] = misc_img


def add_ability_misc_sprites(ability):
    img = ability_catalog.ability_cat[ability].img
    img_source = ability_catalog.ability_cat[ability].img_source
    if img_source + img not in game_stats.gf_misc_img_dict:
        misc_img = pygame.image.load('Img/' + img_source + img + '.png').convert_alpha()
        misc_img.set_colorkey(WhiteColor)
        game_stats.gf_misc_img_dict[str(img_source + img)] = misc_img


def add_battle_effects_sprites(effects):
    for effect in effects:
        if effect not in game_stats.gf_battle_effects_dict:
            battle_effect_img = pygame.image.load('Img/' + effect + '.png').convert_alpha()
            battle_effect_img.set_colorkey(WhiteColor)
            game_stats.gf_battle_effects_dict[str(effect)] = battle_effect_img


school_imgs = {"Overall" : "everything",
               "Tactics" : "tactics",
               "Devine" : "devine",
               "Elemental" : "elemental"}
