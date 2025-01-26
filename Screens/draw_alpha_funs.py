## Among Myth and Wonder
## draw_alpha_funs

import pygame.draw


# Function to draw a transparent rectangle
def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


# Function to draw a transparent line
def draw_line_alpha(surface, color, start, end, thickness, position):
    draw_surf3 = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.line(draw_surf3, color, start, end, thickness)
    surface.blit(draw_surf3, position)
