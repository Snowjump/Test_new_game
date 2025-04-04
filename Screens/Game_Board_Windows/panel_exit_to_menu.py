## Among Myth and Wonder
## panel_exit_to_menu

from Resources.Game_Graphics import graphics_classes
from Resources import game_stats


class Exit_To_Menu_Panel(graphics_classes.Panel):
    def draw_panel(self, screen):
        self.draw_door_icon(screen)

    def draw_door_icon(self, screen):
        door_img = game_stats.gf_misc_img_dict["Icons/exit_to_menu"]
        screen.blit(door_img, (1240, 5))
