##################################################################
# FILE : ex11_backtrack.py
# WRITERS : Lior Paz,lioraryepaz,206240996
# EXERCISE : intro2cs ex11 2017-2018
# DESCRIPTION : general backtracking function
##################################################################

def general_backtracking(list_of_items, dict_items_to_vals, index,
                         set_of_assignments, legal_assignment_func, *args):
    """
    in naive way solves any backtracking problem
    :param list_of_items: list of items we would like to assign
    :param dict_items_to_vals: dict contains keys from list_of_items &
    values from set_of_assignments
    :param index: integer specifying a given location of item in list at the
    current position of recursion
    :param set_of_assignments: a sequence containing all legal assignments
    :param legal_assignment_func: specific function which check  the
    legality of one assignment
    :param args: other objects could be given to func as an add-on to
    legal_assignment_func
    :return: True if found solution, False otherwise
    """
    # recursion base case
    if all(value in set_of_assignments for value in
           dict_items_to_vals.values()):
        return True
    else:
        # going over every possible value
        for val in set_of_assignments:
            item_check = list_of_items[index]
            temp = dict_items_to_vals[item_check]
            # assigning the value
            dict_items_to_vals[item_check] = val
            if legal_assignment_func(dict_items_to_vals, item_check, args):
                # recursion in case action s legal
                if general_backtracking(list_of_items, dict_items_to_vals,
                                        index + 1, set_of_assignments,
                                        legal_assignment_func, *args):
                    return True
            # going one step back in case we have reached a dead-end
            dict_items_to_vals[item_check] = temp
        return False
