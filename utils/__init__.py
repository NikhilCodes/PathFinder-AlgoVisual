from settings import *
from utils.draw import draw_square, reset_cell
from time import sleep


def euclidean_dist(c1, c2):
    return ((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2) ** 0.5


class Graph:
    def __init__(self):
        self.data = dict()

    def add_edge(self, start, end, weight):
        # Establishing Bidirectional Path
        if self.data.get(start):
            self.data[start].add((end, weight))
        else:
            self.data[start] = {(end, weight)}

        if self.data.get(end):
            self.data[end].add((start, weight))
        else:
            self.data[end] = {(start, weight)}

    def get_neighbours(self, value):
        return self.data.get(value)

    def exists(self, value):
        if self.data.get(value):
            return True

        return False

    def kill_node(self, value):
        neighbour = self.data.get(value)
        if neighbour:
            del self.data[value]

            for v, d in neighbour:
                self.data[v].discard((value, d))


class PriorityQueue:
    """ Lesser the `priority_lvl` integer greater the priority. """

    class Node:
        def __init__(self, value):
            self.value = value
            self.priority_lvl = None
            self.nextNode = None

        def __repr__(self):
            return "[{}]".format(self.value)

    def __init__(self):
        self.firstNode = None
        self.lastNode = None

    def __repr__(self):
        lines = []
        working_node = self.firstNode
        if working_node is None:
            return "[EmptyQueue]"

        while working_node is not None:
            lines.append(str(working_node))
            working_node = working_node.nextNode

        return "--".join(lines)

    def is_empty(self):
        if self.firstNode is None:
            return True

        return False

    def peek(self):
        return self.firstNode

    def add(self, value, priority):
        new_node = self.Node(value)
        new_node.priority_lvl = priority

        if self.firstNode is None:
            self.firstNode = self.lastNode = new_node
        elif self.firstNode.priority_lvl > priority:
            new_node.nextNode = self.firstNode
            self.firstNode = new_node
        elif self.firstNode.priority_lvl <= priority and self.firstNode.nextNode is None:
            self.firstNode.nextNode = new_node
            self.lastNode = new_node
        else:
            worker_parent_node = self.firstNode
            worker_node = self.firstNode.nextNode

            while priority > worker_node.priority_lvl:
                worker_node = worker_node.nextNode
                worker_parent_node = worker_parent_node.nextNode

                if worker_node is None:
                    worker_parent_node.nextNode = new_node
                    self.lastNode = new_node
                    return

            new_node.nextNode = worker_node
            worker_parent_node.nextNode = new_node

    def pop(self):
        tmp = self.firstNode
        self.firstNode = self.firstNode.nextNode
        if self.firstNode is None:
            self.lastNode = None

        return tmp


##

# Defining Dijkstra Algorithm
def dijkstra(graph: Graph, start, end, screen_):
    if not (graph.exists(start) and graph.exists(end)):
        raise Exception("Start or End does not exist inside the graph.")

    solution = {
        start: [0, None]  # Priority Level, parent
    }

    if start == end:
        return start

    visited_nodes = set()
    nodes_to_visit_ordered_priority_wise = PriorityQueue()
    nodes_to_visit_ordered_priority_wise.add(start, priority=0)

    while True:
        if nodes_to_visit_ordered_priority_wise.peek().value == end:
            break

        _buffer_elem: PriorityQueue.Node = nodes_to_visit_ordered_priority_wise.peek()
        if _buffer_elem.value in visited_nodes:
            nodes_to_visit_ordered_priority_wise.pop()
            continue

        _buffer_set: set = graph.get_neighbours(_buffer_elem.value)
        visited_nodes.add(_buffer_elem.value)
        nodes_to_visit_ordered_priority_wise.pop()

        # Drawing colored boxes for explored nodes
        if _buffer_elem.value != start and _buffer_elem.value != end:
            draw_square(screen_, _buffer_elem.value, VISITED_CELL_COLOR)

        for i in _buffer_set:
            if i[0] not in visited_nodes:
                if solution.get(i[0]) is None or solution[i[0]][0] > i[1] + _buffer_elem.priority_lvl:
                    solution[i[0]] = [i[1] + _buffer_elem.priority_lvl, _buffer_elem.value]

                nodes_to_visit_ordered_priority_wise.add(i[0], i[1] + solution[_buffer_elem.value][0])

    # Backtracking
    parent = end
    dist = solution[end][0]
    path = []
    while parent is not None:
        path.append(parent)
        parent = solution[parent][1]

    path.reverse()

    for coord in visited_nodes:
        if coord == start:
            continue

        reset_cell(screen_, coord)

    return path, dist


# Defining A-Star Algorithm
def a_star(graph: Graph, start, end, screen_):
    if not (graph.exists(start) and graph.exists(end)):
        raise Exception("Start or End does not exist inside the graph.")

    solution = {
        start: [0, None]
    }

    if start == end:
        return start

    visited_nodes = set()
    nodes_to_visit_ordered_priority_wise = PriorityQueue()
    nodes_to_visit_ordered_priority_wise.add(start, priority=0)

    while True:
        if nodes_to_visit_ordered_priority_wise.peek().value == end:
            break

        _buffer_elem: PriorityQueue.Node = nodes_to_visit_ordered_priority_wise.peek()
        if _buffer_elem.value in visited_nodes:
            nodes_to_visit_ordered_priority_wise.pop()
            continue

        _buffer_set: set = graph.get_neighbours(_buffer_elem.value)
        visited_nodes.add(_buffer_elem.value)
        nodes_to_visit_ordered_priority_wise.pop()

        # Drawing colored boxes for explored nodes
        if _buffer_elem.value != start and _buffer_elem.value != end:
            draw_square(screen_, _buffer_elem.value, VISITED_CELL_COLOR)
            # sleep(0.1)

        for i in _buffer_set:
            if i[0] not in visited_nodes:
                print(i)
                if solution.get(i[0]) is None or solution[i[0]][0] > i[1] + _buffer_elem.priority_lvl + euclidean_dist(
                        i[0], end):
                    solution[i[0]] = [i[1] + _buffer_elem.priority_lvl + euclidean_dist(
                        i[0], end), _buffer_elem.value]

                nodes_to_visit_ordered_priority_wise.add(i[0], i[1] + solution[_buffer_elem.value][0] + euclidean_dist(
                        i[0], end))

    # Backtracking
    parent = end
    dist = solution[end][0]
    path = []
    while parent is not None:
        path.append(parent)
        parent = solution[parent][1]

    path.reverse()

    for coord in visited_nodes:
        if coord == start:
            continue

        reset_cell(screen_, coord)

    return path, dist
