from utils import Graph

neighbour_displacements = [
    (-1, -1),  # Top Left
    (0, -1),  # Top
    (1, -1),  # Top Right
    (1, 0),  # Right
    (1, 1),  # Bottom Right
    (0, 1),  # Bottom
    (-1, 1),  # Bottom Left
    (-1, 0),  # Left
]


def add_vector(v1, v2, dim):
    v = tuple()
    for i in range(dim):
        v += (v1[i] + v2[i],)

    return v


def get_distance_from_neighbour_vector(vec):
    if sum(vec) % 2 == 1:
        return 1
    else:
        return 1.4142135624


def create_boxed_graph(size):
    g = Graph()

    for y in range(size):
        for x in range(size):
            current_node = (x, y)
            for displacement_vector in neighbour_displacements:
                neighbour_node = add_vector(displacement_vector, current_node, 2)
                if -1 not in neighbour_node:
                    g.add_edge(current_node, neighbour_node, get_distance_from_neighbour_vector(displacement_vector))

    return g


if __name__ == '__main__':
    from pprint import pformat

    data = create_boxed_graph(5).data
    print(pformat(data))
