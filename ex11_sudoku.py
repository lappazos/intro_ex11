##################################################################
# FILE : ex11_sudoku.py
# WRITERS : Lior Paz,lioraryepaz,206240996
# EXERCISE : intro2cs ex11 2017-2018
# DESCRIPTION : solves sudoku board game with general backtracking
##################################################################

from math import floor
from ex11_backtrack import general_backtracking


def print_board(board, board_size=9):
    """ prints a sudoku board to the screen

    ---  board should be implemented as a dictionary
         that points from a location to a number {(row,col):num}
    """
    for row in range(board_size):
        if row % 3 == 0:
            print('-------------')
        toPrint = ''
        for col in range(board_size):
            if col % 3 == 0:
                toPrint += '|'
            toPrint += str(board[(row, col)])
        toPrint += '|'
        print(toPrint)
    print('-------------')


def load_game(sudoku_file):
    """
    parsing input file into sudoku dict
    :param sudoku_file: input file location
    :return: dict {board coordinate: current value}
    """
    with open(sudoku_file, 'r') as sudoku:
        sudoku_dict = {}
        sudoku = sudoku.readlines()
        for line in range(len(sudoku)):
            for index in range(0, 18, 2):
                sudoku_dict[(line, index / 2)] = int(sudoku[line][index])
    return sudoku_dict


def check_board(board, x, *args):
    """
    legal_assignment_func
    :param board: dict {board coordinate: current value}
    :param x: item to check
    :param args: unused - needed for fitting other general backtracking
    functions
    :return: True if assignment is legal, False otherwise
    """
    # row & column check
    for i in range(0, 9):
        if (board[(x[0], i)] == board[x]) and (i != x[1]):
            return False
        if (board[(i, x[1])] == board[x]) and (i != x[0]):
            return False
        # square check
    factor = (floor(x[0] / 3), floor(x[1] / 3))
    for i in range(3):
        for j in range(3):
            index = (factor[0] * 3 + i, factor[1] * 3 + j)
            if (board[index] == board[x]) and (index != x):
                return False
    else:
        return True


def run_game(sudoku_file, print_mode=False):
    """

    :param sudoku_file: input file location
    :param print_mode: should we print in case of solution
    :return: True if there is a solution, False otherwise
    """
    board = load_game(sudoku_file)
    list_of_items = []
    for key in board.keys():
        if board[key] == 0:
            list_of_items.append(key)
    set_of_assignments = range(1, 10)
    legal_assignment_func = check_board
    if general_backtracking(list_of_items, board, 0,
                            set_of_assignments, legal_assignment_func):
        if print_mode:
            print_board(board)
        return True
    else:
        return False
