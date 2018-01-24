import game
from board_analyzer import *

DEFAULT_STATE = "EMPTY"


class Cell:
    """
    Cell class
    """
    def __init__(self, location, player=None):
        """ Initializes the cell class
            :param location: Tuple of pixel position
            :param player: Pre_load cell with this player """
        self.__chip_owner = game.Game.EMPTY if player is None else player
        self.__location = location

    def get_location(self):
        """ Getter for location """
        return self.__location

    def set_chip_owner(self, player):
        """ Setter for chip owner """
        self.__chip_owner = player

    def __str__(self):
        return str(self.__chip_owner)

    def __int__(self):
        return self.__chip_owner


class Board:
    """
    Board class
    """
    # Class constants
    DELTA_HEIGHT = 130
    DELTA_WIDTH = 180
    DELTA_CELL = 109
    CELL_PADDING = 13
    NW_ANCHOR = "nw"
    BOARD_WIDTH = 7
    BOARD_HEIGHT = 6

    WINNING_SEQ_LENGTH = 4

    def __init__(self, get_current_player):
        """ Initializes the class
            :param get_current_player: Func from game, gets current playing
                                       player """
        self.__columns = []
        self.__get_current_player = get_current_player

        for i in range(Board.BOARD_WIDTH):
            column = []
            for j in range(Board.BOARD_HEIGHT):
                # Calculations based on board image size
                column.append(Cell((self.DELTA_WIDTH + self.CELL_PADDING +
                                    (self.CELL_PADDING - 2) * i +
                                    self.DELTA_CELL * i,
                                    self.DELTA_HEIGHT + self.CELL_PADDING +
                                    (self.CELL_PADDING - 2) * j +
                                    self.DELTA_CELL * j)))

            self.__columns.append(column)

    def check_legal_move_get_row(self, column, player, set_chip_flag=True):
        """ :param column: Column to place chip in
            :param player: Owner of the chip
            :param set_chip_flag: if True, sets cell on successful check
            :return: Success, row """
        # TODO:: User assert on the output of this function

        # Cells already occupied
        taken_cells = [cell
                       for cell in self.__columns[column]
                       if int(cell) != game.Game.EMPTY]

        # Get designated row for chip, -1 if no row available
        designated_row = Board.BOARD_HEIGHT - len(taken_cells) - 1 \
            if len(taken_cells) < Board.BOARD_HEIGHT else -1

        if designated_row == -1:
            return False, -1

        if set_chip_flag:

            # Update board columns
            self.__set_cell(player, column, designated_row)

        return True, designated_row

    def get_chip_location(self, column, row):
        """ :param column: Column of requested chip
            :param row: Row of requested chip
            :return: x, y pixels
        """
        return self.__columns[column][row].get_location()

    def __set_cell(self, player, column, row):
        """ :param player: Owner of chip
            :param column: Column of chip
            :param row: Row of chip """
        self.__columns[column][row].set_chip_owner(player)

    def get_columns(self):
        """ Gets columns list as ints instead of cells """
        columns = [[int(self.__columns[col][cell])
                    for cell in range(len(self.__columns[col]))]
                   for col in range(len(self.__columns))]
        return columns

    def get_columns_as_str(self):
        """ Gets columns list as strings instead of cells, used by AI """
        columns = [[str(self.__columns[col][cell])
                    for cell in range(len(self.__columns[col]))]
                   for col in range(len(self.__columns))]
        return columns

    def get_cell_at(self, col, row):
        """ Getter for specific cell """
        return self.__columns[col][row]

    def __repr__(self):
        return self.__columns

    def find_connected_and_winner(self, column, row):
        """ :param column: Column of last placed chip
            :param row: Row of last placed chip
            :return: Winning __player, List of winning chips
        """
        columns = self.__columns  # For readability

        # Check column
        lst = []
        for j in range(row, min(row + self.WINNING_SEQ_LENGTH,
                                len(columns[column]))):
            if int(columns[column][j]) == self.__get_current_player():
                lst.append((column, j))

        if len(lst) == self.WINNING_SEQ_LENGTH:
            return self.__get_current_player(), lst

        # Check row
        rows = BoardAnalyzer.transpose_matrix(self.__columns)

        for j in range(len(rows[row]) - 3):
            flag = True
            for i in range(self.WINNING_SEQ_LENGTH):
                if int(rows[row][j + i]) != self.__get_current_player():
                    flag = False
                    break

            if flag:
                return self.__get_current_player(), \
                       [(k, row) for k in range(j, j +
                                                self.WINNING_SEQ_LENGTH)]

        # Check diagonal
        for indices_diff in range(len(rows) - 1, -len(columns), -1):
            lst = []
            for i in range(len(rows)):
                for j in range(len(columns)):
                    if indices_diff == i - j:
                        if int(columns[j][i]) == self.__get_current_player():
                            lst.append((j, i))
                        else:
                            lst.clear()

                if len(lst) == self.WINNING_SEQ_LENGTH:
                    return self.__get_current_player(), lst

        # Check anti-diagonal
        for indices_sum in range(len(rows) + len(columns) - 1):
            lst = []
            for i in range(len(rows)):
                for j in range(len(columns)):
                    if indices_sum == i + j:
                        if int(columns[j][i]) == self.__get_current_player():
                            lst.append((j, i))
                        else:
                            lst.clear()

                if len(lst) == self.WINNING_SEQ_LENGTH:
                    return self.__get_current_player(), lst

        if self.check_draw():
            return game.Game.DRAW, None

        # If no winning chips were found
        return None, None

    def check_draw(self):
        """ Check if all the board is full, if so, it is a draw, as this
            function is called AFTER every other possibility has been """
        draw_flag = True
        for col in range(len(self.__columns)):
            for row in range(len(self.__columns[col])):
                if int(self.__columns[col][row]) == game.Game.EMPTY:
                    draw_flag = False

        return draw_flag

    def set_columns(self, str_columns):
        """ Setter for columns for usage in AI class """
        # For backtracking in AI
        self.__columns = [[Cell(None, int(str_columns[col][cell]))
                           for cell in range(len(str_columns[col]))]
                          for col in range(len(str_columns))]
