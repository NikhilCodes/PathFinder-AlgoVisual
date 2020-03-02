import pygame

from settings import *


def draw_square(screen_, cell_coord, color):
    pygame.draw.rect(screen_,
                     color,
                     [
                         cell_coord[0] * GRID_SIZE,
                         cell_coord[1] * GRID_SIZE,
                         GRID_SIZE,
                         GRID_SIZE
                     ]
                     )

    pygame.display.flip()


def reset_cell(screen_, box_coord):
    pygame.draw.rect(screen_,
                     BACKGROUND_COLOR,
                     [
                         box_coord[0] * GRID_SIZE + 1,
                         box_coord[1] * GRID_SIZE + 1,
                         GRID_SIZE - 1,
                         GRID_SIZE - 1
                     ]
                     )

    start_pos = (box_coord[0] * GRID_SIZE, box_coord[1] * GRID_SIZE)
    pygame.draw.line(screen_, GRID_COLOR, start_pos, (start_pos[0], start_pos[1] + GRID_SIZE))
    pygame.draw.line(screen_, GRID_COLOR, start_pos, (start_pos[0] + GRID_SIZE, start_pos[1]))
    pygame.display.flip()
