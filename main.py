import pygame

from settings import *
from utils import dijkstra
from utils.draw import draw_square, reset_cell
from utils.geometry_2d import get_node_pos_by_mouse_pos
from utils.graph_creator import create_boxed_graph, add_vector, get_distance_from_neighbour_vector
from utils.graph_creator import neighbour_displacements

# CALCULATED CONSTANTS (NO MESSING HERE)
N_NODES_ON_EDGE = WINDOW_SIZE // GRID_SIZE
GRAPH = None
#

# WORKING_VARIABLES (USED BY THIS PROGRAM)
source_coord = None
backup_source_coord = None
destination_coord = None
prev_path = None
#

pygame.init()
pygame.display.set_caption("Dijkstra's Algorithm Visualizer")

screen = pygame.display.set_mode([WINDOW_SIZE, WINDOW_SIZE])
clock = pygame.time.Clock()


def prepare_background():
    global GRAPH

    screen.fill(BACKGROUND_COLOR)  # Setting Background Color

    # Drawing Grid
    # - # Drawing Horizontal Lines
    for y in range(WINDOW_SIZE // GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y * GRID_SIZE), (WINDOW_SIZE, y * GRID_SIZE))

    # - # Drawing Vertical Lines
    for x in range(WINDOW_SIZE // GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x * GRID_SIZE, 0), (x * GRID_SIZE, WINDOW_SIZE))

    # Updating changes on screen
    pygame.display.flip()
    GRAPH = create_boxed_graph(N_NODES_ON_EDGE)


prepare_background()


def mainloop():
    global source_coord, backup_source_coord, destination_coord, prev_path, GRAPH

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.quit()
                return 0
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                prepare_background()
                pygame.display.flip()
                mouse_pos = pygame.mouse.get_pos()

                box_coord = get_node_pos_by_mouse_pos(mouse_pos, GRID_SIZE, N_NODES_ON_EDGE)

                draw_square(screen, box_coord, START_END_CELL_COLOR)
                source_coord = backup_source_coord = box_coord
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                mouse_pos = pygame.mouse.get_pos()

                box_coord = get_node_pos_by_mouse_pos(mouse_pos, GRID_SIZE, N_NODES_ON_EDGE)

                draw_square(screen, box_coord, START_END_CELL_COLOR)
                if source_coord is None:
                    source_coord = backup_source_coord
                    for coord in prev_path[1:]:
                        reset_cell(screen, coord)

                destination_coord = box_coord
            elif event.type == pygame.MOUSEBUTTONDOWN:
                box_coord = get_node_pos_by_mouse_pos(event.pos, GRID_SIZE, N_NODES_ON_EDGE)
                if event.button == 1:
                    draw_square(screen, box_coord, OBSTACLE_COLOR)
                    GRAPH.kill_node(box_coord)
                elif event.button == 3:
                    reset_cell(screen, box_coord)

                    for displacement_vector in neighbour_displacements:
                        neighbour_node = add_vector(displacement_vector, box_coord, 2)
                        if -1 not in neighbour_node and neighbour_node in GRAPH.data.keys():
                            GRAPH.add_edge(box_coord, neighbour_node,
                                           get_distance_from_neighbour_vector(displacement_vector))

        if source_coord and destination_coord:
            path, distance = dijkstra(GRAPH, source_coord, destination_coord, screen)
            prev_path = path.copy()
            source_coord = destination_coord = None

            for coord in path[1:-1]:
                draw_square(screen, coord, PATH_COLOR)


if __name__ == '__main__':
    mainloop()