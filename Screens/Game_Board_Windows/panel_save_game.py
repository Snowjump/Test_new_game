## Among Myth and Wonder
## panel_save_game

from Resources.Game_Graphics import graphics_classes
from Resources import game_stats


class Save_Game_Panel(graphics_classes.Panel):
    def draw_panel(self, screen):
        self.draw_parchment_icon(screen)

    def draw_parchment_icon(self, screen):
        parchment_img = game_stats.gf_misc_img_dict["Icons/parchment_save"]
        screen.blit(parchment_img, (1205, 5))
