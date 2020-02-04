def get_node_pos_by_mouse_pos(mouse_pos, grid_size, max_nodes_on_edge):
    box_coord = tuple()

    for x in range(1, max_nodes_on_edge + 1):
        if x * grid_size > mouse_pos[0]:
            box_coord += (x - 1,)
            break

    for y in range(1, max_nodes_on_edge + 1):
        if y * grid_size > mouse_pos[1]:
            box_coord += (y - 1,)
            break

    return box_coord
