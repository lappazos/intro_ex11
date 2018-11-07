##################################################################
# FILE : ex11_improve_backtrack.py
# WRITERS : Lior Paz,lioraryepaz,206240996
# EXERCISE : intro2cs ex11 2017-2018
# DESCRIPTION : 4 improved versions of map coloring backtracking -
# degree_heruistic, MRV, FC & LCV
##################################################################

import ex11_map_coloring as mc
from ex11_backtrack import general_backtracking

MRV_FACTOR = 'MRV'
LCV_FACTOR = 'LCV'


def back_track_degree_heuristic(adj_dict, colors):
    """
    use general backtracking in order to solve map coloring problem with an
    improvement of list_of_items sorted by countries with  maximal to minimal
    num of neighbours
    :param adj_dict: dict contains countries in the map & their neighbours
    :param colors: list containing all legal colors
    :return: dict with the solution of {country : color}, or None if no
    solution
    """
    neighbour_num = {}  # dict with {countries : number of neighbours
    for country in adj_dict: neighbour_num[country] = len(adj_dict[country])
    list_of_items = sorted(neighbour_num, key=neighbour_num.get, reverse=True)
    color_map = adj_dict.fromkeys(adj_dict, None)
    # naming the check func
    legal_assignment_func = mc.check_map
    if general_backtracking(list_of_items, color_map, mc.START_INDEX, colors,
                            legal_assignment_func, adj_dict):
        return color_map
    else:
        return None


def back_track_MRV(adj_dict, colors):
    """
    solves map coloring problem with an improvement of choosing
    our next item in the recursion by the min legal assignments left
    :param adj_dict: dict contains countries in the map & their neighbours
    :param colors: list containing all legal colors
    :return: dict with the solution of {country : color}, or None if no
    solution
    """
    color_map = adj_dict.fromkeys(adj_dict, None)
    # dict with {country : legal assignments}
    allowed_colors_dict = {country: colors[:] for country in adj_dict}
    # helper func
    if back_track_MRV_helper(color_map, allowed_colors_dict, adj_dict):
        return color_map
    else:
        return None


def back_track_MRV_helper(color_map, allowed_colors_dict, adj_dict):
    """
    MRV helper func
    :param color_map: dict with the solution of {country : color}
    :param allowed_colors_dict: dict with {country : legal assignments}
    :param adj_dict: dict contains countries in the map & their neighbours
    :return: True if backtracking succeeded, False otherwise
    """
    # recursion base case
    if all(value is not None for value in color_map.values()):
        return True
    else:
        # choosing which item is with minimal assignments
        current_country = \
            min(allowed_colors_dict.items(), key=lambda x: len(x[1]))[0]
        # defining legal countries to that item
        set_of_assignments = allowed_colors_dict[current_country]
        # helper func
        return helper_MRV_LCV(current_country, set_of_assignments, color_map,
                              allowed_colors_dict, adj_dict, MRV_FACTOR)


def back_track_FC(adj_dict, colors):
    """
    use general backtracking in order to solve map coloring problem with an
    improvement of neighbours legality forward checking per recursion stage
    :param adj_dict: dict contains countries in the map & their neighbours
    :param colors: list containing all legal colors
    :return: dict with the solution of {country : color}, or None if no
    solution
    """
    list_of_items = list(adj_dict.keys())
    color_map = adj_dict.fromkeys(adj_dict, None)
    # naming the check func
    legal_assignment_func = FC_check
    if general_backtracking(list_of_items, color_map, mc.START_INDEX, colors,
                            legal_assignment_func, adj_dict, colors):
        return color_map
    else:
        return None


def FC_check(color_map, country, *args):
    """
    FC legal_assignment_func
    :param color_map: dict with the solution of {country : color}
    :param country: current country in recursion
    :param args: add-on to inner funcs
    :return: True if assignment is legal, False otherwise
    """
    # helper func - 'normal' check
    if mc.check_map(color_map, country, args[0]):
        # helper func - FC check
        return check_neighbour(color_map, country, args[0])
    else:
        return False


def check_neighbour(color_map, country, *args):
    """
    legal_assignment_func helper
    :param color_map: dict with the solution of {country : color}
    :param country: current country in recursion
    :param args: extra arguments - adj_dict & colors
    :return: True if assignment is legal, False otherwise
    """
    adj_dict = args[0][0]
    # we use set in order to perform '-' operation in end
    colors = set(args[0][1])
    if adj_dict[country] == mc.NO_NEIGHBOUR:
        return True
    # FC check process
    for neighbour in adj_dict[country]:
        neighbour_color = set()
        if adj_dict[neighbour] == mc.NO_NEIGHBOUR:
            return True
        for neighbour_2nd_degree in adj_dict[neighbour]:
            neighbour_color.add(color_map[neighbour_2nd_degree])
        if colors - neighbour_color == set():
            return False
    return True


def back_track_LCV(adj_dict, colors):
    """
    solves map coloring problem with an improvement of choosing
    our color list order by the color that leaves us with the most 'open
    options'
    :param adj_dict: dict contains countries in the map & their neighbours
    :param colors: list containing all legal colors
    :return: dict with the solution of {country : color}, or None if no
    solution
    """
    list_of_items = list(adj_dict.keys())
    color_map = adj_dict.fromkeys(adj_dict, None)
    allowed_colors_dict = {country: colors[:] for country in adj_dict}
    # helper func
    if back_track_LCV_helper(list_of_items, color_map, allowed_colors_dict,
                             mc.START_INDEX, colors, adj_dict):
        return color_map
    else:
        return None


def back_track_LCV_helper(list_of_items, color_map, allowed_colors_dict, index,
                          colors, adj_dict):
    """
    LCV helper func
    :param list_of_items: list of countries we would like to assign
    :param color_map: dict with the solution of {country : color}
    :param allowed_colors_dict: dict with {country : legal assignments}
    :param index: integer specifying a given location of item in list at the
    current position of recursion
    :param colors: list containing all legal colors
    :param adj_dict: dict contains countries in the map & their neighbours
    :return: True if backtracking succeeded, False otherwise
    """
    # recursion base case
    if all(value is not None for value in color_map.values()):
        return True
    else:
        # LCV color propper order choosing process
        current_country = list_of_items[index]
        if not allowed_colors_dict[current_country]:
            return False
        # helper func
        set_of_assignments = build_color_list(allowed_colors_dict,
                                              current_country, adj_dict,
                                              color_map)
        # helper func
        return helper_MRV_LCV(current_country, set_of_assignments, color_map,
                              allowed_colors_dict, adj_dict,
                              LCV_FACTOR, list_of_items, index, colors)


def build_color_list(allowed_colors_dict, current_country, adj_dict,
                     color_map):
    """
    helper func LCV color list per given country & recursion stage
    :param allowed_colors_dict: dict with {country : legal assignments}
    :param current_country: current country in recursion
    :param adj_dict: dict contains countries in the map & their neighbours
    :param color_map: dict with the solution of {country : color}
    :return: LCV sorted list of colors
    """
    color_val_dict = {}  # dict {color: num of open options to use these colors
    for color in allowed_colors_dict[current_country]:
        color_val_dict[color] = 0
        for country in adj_dict[current_country]:
            if color_map[country] is None:
                color_list = allowed_colors_dict[country]
                # add number of options per neighbour (-) the specific current
                #  color if exist in neighbour
                color_val_dict[color] += len(color_list) - (
                    1 if color in color_list else 0)
    set_of_assignments = sorted(color_val_dict, key=color_val_dict.get,
                                reverse=True)
    return set_of_assignments


def helper_MRV_LCV(current_country, set_of_assignments, color_map,
                   allowed_colors_dict, adj_dict, factor, *args):
    """
    # MRV & LCV helper func
    :param current_country: current country in recursion
    :param set_of_assignments: list containing all legal colors
    :param color_map: dict with the solution of {country : color}
    :param allowed_colors_dict: dict with {country : legal assignments}
    :param adj_dict: dict contains countries in the map & their neighbours
    :param factor: MRV or LCV mode
    :param args: other objects needed for LCV recursion process
    :return: True if backtracking succeeded, False otherwise
    """
    # iterating a list of colors
    for val in set_of_assignments:
        # assigning the value
        color_map[current_country] = val
        # saving current_country allowed colors in case of reverse change
        # needed after
        temp = allowed_colors_dict[current_country]
        # deleting the country from allowed_colors_dict - has no longer
        # options, but a chose value
        del allowed_colors_dict[current_country]
        # saving countries we have changed their allowed_colors_dict, in case
        #  of reverse change needed after
        changed_countries = []
        for country in adj_dict[current_country]:
            if country in allowed_colors_dict:
                if val in allowed_colors_dict[country]:
                    # removing val from country neighbours allowed_colors_dict
                    allowed_colors_dict[country].remove(val)
                    changed_countries.append(country)
        if factor == MRV_FACTOR:
            # recursion
            if back_track_MRV_helper(color_map, allowed_colors_dict, adj_dict):
                return True
            else:
                # helper func
                reverse_change(allowed_colors_dict, changed_countries,
                               color_map, current_country, temp, val)
        else:
            # recursion
            if back_track_LCV_helper(args[0], color_map, allowed_colors_dict,
                                     args[1] + 1, args[2], adj_dict):
                return True
            else:
                # helper func
                reverse_change(allowed_colors_dict, changed_countries,
                               color_map, current_country, temp, val)
    return False


def reverse_change(allowed_colors_dict, changed_countries, color_map,
                   current_country, temp, val):
    """
    # helper func - reverse process in case backtracking needs to go back
    :param allowed_colors_dict: dict with {country : legal assignments}
    :param changed_countries: countries we have changed their
    allowed_colors_dict in a iven recursion  stage
    :param color_map: dict with the solution of {country : color}
    :param current_country: current country in recursion
    :param temp: current_country in recursion allowed colors before deleting it
    :param val: value in current recursion stage needed to be reversed in
    changed countries
    """
    color_map[current_country] = None
    allowed_colors_dict[current_country] = temp
    for changed_country in changed_countries:
        allowed_colors_dict[changed_country] += [val]


def fast_back_track(adj_dict, colors):
    pass
