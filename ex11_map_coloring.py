##################################################################
# FILE : ex11_map_coloring.py
# WRITERS : Lior Paz,lioraryepaz,206240996
# EXERCISE : intro2cs ex11 2017-2018
# DESCRIPTION : solves map coloring problem with general backtracking
##################################################################

from ex11_backtrack import general_backtracking

COLORS = ['red', 'blue', 'green', 'magenta', 'yellow', 'cyan']
START_INDEX = 0
NO_NEIGHBOUR = ['']


def read_adj_file(adjacency_file):
    """
    parsing input file into countries dict
    :param adjacency_file: input file location
    :return: dict contains countries in the map & their neighbours
    """
    adjacency = open(adjacency_file)
    adjacency_dict = {}
    adjacency = adjacency.readlines()
    for line in adjacency:
        split = line.split(':')
        value = split[1].rstrip().split(',')
        if value == NO_NEIGHBOUR:
            adjacency_dict[split[0]] = []
        else:
            adjacency_dict[split[0]] = value
    return adjacency_dict


def check_map(color_map, country, *args):
    """
    legal_assignment_func
    :param color_map: dict with the solution of {country : color}
    :param country: current country in recursion
    :param args: needed for adjacency_dict
    :return: True if assignment is legal, False otherwise
    """
    adjacency_dict = args[0][0]
    if adjacency_dict[country] == NO_NEIGHBOUR:
        return True
    for neighbour in adjacency_dict[country]:
        if color_map[neighbour] == color_map[country]:
            return False
    return True


def run_map_coloring(adjacency_file, num_colors=4, map_type=None):
    """
    main func - solving map coloring problem using general backtracking
    :param adjacency_file: dict contains countries in the map & their
    neighbours
    :param num_colors: number of wanted colors for solving the problem
    :param map_type:
    :return: dict with the solution of {country : color}, or None if no
    solution
    """
    adjacency = read_adj_file(adjacency_file)
    color_map = dict(adjacency)
    list_of_items = list(adjacency.keys())
    set_of_assignments = COLORS[:num_colors]
    legal_assignment_func = check_map
    if general_backtracking(list_of_items, color_map, START_INDEX,
                            set_of_assignments, legal_assignment_func,
                            adjacency):
        return color_map
    else:
        return None
