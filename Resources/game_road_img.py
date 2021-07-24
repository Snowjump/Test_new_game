## Miracle battles!

from Resources import game_stats
from Resources import game_classes

def add_road(TileNumOrig, x2, y2):
    if game_stats.brush in ["Earthen"]:
        # Creating new road with central piece
        game_stats.level_map[TileNumOrig].road = game_classes.Roadway("Earthen", 1)

        # Creating connection with nearby tiles
        x3 = int(x2) - 1
        if x3 > 0:
            TileNum = (y2 - 1) * game_stats.new_level_width + x3 - 1
            if game_stats.level_map[TileNum].road is not None:
                game_stats.level_map[TileNum].road.r_m = True
                game_stats.level_map[TileNumOrig].road.l_m = True

        x3 = int(x2) + 1
        if x3 <= game_stats.new_level_width:
            TileNum = (y2 - 1) * game_stats.new_level_width + x3 - 1
            if game_stats.level_map[TileNum].road is not None:
                game_stats.level_map[TileNum].road.l_m = True
                game_stats.level_map[TileNumOrig].road.r_m = True

        y3 = int(y2) - 1
        if y3 > 0:
            TileNum = (y3 - 1) * game_stats.new_level_width + x2 - 1
            if game_stats.level_map[TileNum].road is not None:
                game_stats.level_map[TileNum].road.m_b = True
                game_stats.level_map[TileNumOrig].road.m_t = True

        y3 = int(y2) + 1
        if y3 <= game_stats.new_level_height:
            TileNum = (y3 - 1) * game_stats.new_level_width + x2 - 1
            if game_stats.level_map[TileNum].road is not None:
                game_stats.level_map[TileNum].road.m_t = True
                game_stats.level_map[TileNumOrig].road.m_b = True

        x3 = int(x2) + 1
        y3 = int(y2) - 1
        if y3 > 0 and x3 <= game_stats.new_level_width:
            TileNum = (y3 - 1) * game_stats.new_level_width + x3 - 1
            if game_stats.level_map[TileNum].road is not None:
                game_stats.level_map[TileNum].road.l_b = True
                game_stats.level_map[TileNumOrig].road.r_t = True

                x4 = int(x2)
                y4 = int(y2) - 1
                x5 = int(x2) + 1
                y5 = int(y2)

                TileNum2 = (y4 - 1) * game_stats.new_level_width + x4 - 1
                if game_stats.level_map[TileNum2].road is not None:
                    game_stats.level_map[TileNum].road.l_b = False
                    game_stats.level_map[TileNumOrig].road.r_t = False
                    game_stats.level_map[TileNum2].road.r_b = False

                TileNum3 = (y5 - 1) * game_stats.new_level_width + x5 - 1
                if game_stats.level_map[TileNum3].road is not None:
                    game_stats.level_map[TileNum].road.l_b = False
                    game_stats.level_map[TileNumOrig].road.r_t = False
                    game_stats.level_map[TileNum3].road.l_t = False

                # if game_stats.level_map[TileNum2].road is not None and game_stats.level_map[TileNum3].road is not None:

        x3 = int(x2) - 1
        y3 = int(y2) - 1
        if y3 > 0 and x3 > 0:
            TileNum = (y3 - 1) * game_stats.new_level_width + x3 - 1
            if game_stats.level_map[TileNum].road is not None:
                game_stats.level_map[TileNum].road.r_b = True
                game_stats.level_map[TileNumOrig].road.l_t = True

                x4 = int(x2) - 1
                y4 = int(y2)
                x5 = int(x2)
                y5 = int(y2) - 1

                TileNum2 = (y4 - 1) * game_stats.new_level_width + x4 - 1
                if game_stats.level_map[TileNum2].road is not None:
                    game_stats.level_map[TileNum].road.r_b = False
                    game_stats.level_map[TileNumOrig].road.l_t = False
                    game_stats.level_map[TileNum2].road.r_t = False

                TileNum3 = (y5 - 1) * game_stats.new_level_width + x5 - 1
                if game_stats.level_map[TileNum3].road is not None:
                    game_stats.level_map[TileNum].road.r_b = False
                    game_stats.level_map[TileNumOrig].road.l_t = False
                    game_stats.level_map[TileNum3].road.l_b = False

        x3 = int(x2) - 1
        y3 = int(y2) + 1
        if y3 <= game_stats.new_level_height and x3 > 0:
            TileNum = (y3 - 1) * game_stats.new_level_width + x3 - 1
            if game_stats.level_map[TileNum].road is not None:
                game_stats.level_map[TileNum].road.r_t = True
                game_stats.level_map[TileNumOrig].road.l_b = True

                x4 = int(x2) - 1
                y4 = int(y2)
                x5 = int(x2)
                y5 = int(y2) + 1

                TileNum2 = (y4 - 1) * game_stats.new_level_width + x4 - 1
                if game_stats.level_map[TileNum2].road is not None:
                    game_stats.level_map[TileNum].road.r_t = False
                    game_stats.level_map[TileNumOrig].road.l_b = False
                    game_stats.level_map[TileNum2].road.r_b = False

                TileNum3 = (y5 - 1) * game_stats.new_level_width + x5 - 1
                if game_stats.level_map[TileNum3].road is not None:
                    game_stats.level_map[TileNum].road.r_t = False
                    game_stats.level_map[TileNumOrig].road.l_b = False
                    game_stats.level_map[TileNum3].road.l_t = False

        x3 = int(x2) + 1
        y3 = int(y2) + 1
        if y3 <= game_stats.new_level_height and x3 <= game_stats.new_level_width:
            TileNum = (y3 - 1) * game_stats.new_level_width + x3 - 1
            if game_stats.level_map[TileNum].road is not None:
                game_stats.level_map[TileNum].road.l_t = True
                game_stats.level_map[TileNumOrig].road.r_b = True

                x4 = int(x2) + 1
                y4 = int(y2)
                x5 = int(x2)
                y5 = int(y2) + 1

                TileNum2 = (y4 - 1) * game_stats.new_level_width + x4 - 1
                if game_stats.level_map[TileNum2].road is not None:
                    game_stats.level_map[TileNum].road.l_t = False
                    game_stats.level_map[TileNumOrig].road.r_b = False
                    game_stats.level_map[TileNum2].road.l_b = False

                TileNum3 = (y5 - 1) * game_stats.new_level_width + x5 - 1
                if game_stats.level_map[TileNum3].road is not None:
                    game_stats.level_map[TileNum].road.l_t = False
                    game_stats.level_map[TileNumOrig].road.r_b = False
                    game_stats.level_map[TileNum3].road.r_t = False