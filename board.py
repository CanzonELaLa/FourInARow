import game
from board_analyzer import *

DEFAULT_STATE = "EMPTY"


class Cell:
    def __init__(self, location, player=None):
        self.__chip_owner = game.Game.EMPTY if player is None else player
        self.__location = location

    def get_location(self):
        return self.__location

    def set_chip_owner(self, player):
        self.__chip_owner = player

    def get_chip_owner(self):
        return self.__chip_owner

    def __str__(self):
        return str(self.__chip_owner)

    def __int__(self):
        return self.__chip_owner


class Board:
    # Class constants
    DELTA_HEIGHT = 130
    DELTA_WIDTH = 180
    DELTA_CELL = 109
    CELL_PADDING = 13
    NW_ANCHOR = "nw"
    BOARD_WIDTH = 7
    BOARD_HEIGHT = 6

    WINNING_SEQ_LENGTH = 4

    # TODO:: Make size constants
    def __init__(self, get_current_player, get_player):
        self.__columns = []
        self.__get_current_player = get_current_player
        self.__get_player = get_player

        for i in range(Board.BOARD_WIDTH):
            column = []
            for j in range(Board.BOARD_HEIGHT):
                column.append(Cell((self.DELTA_WIDTH + self.CELL_PADDING +
                                    (self.CELL_PADDING - 2) * i +
                                    self.DELTA_CELL * i,
                                    self.DELTA_HEIGHT + self.CELL_PADDING +
                                    (self.CELL_PADDING - 2) * j +
                                    self.DELTA_CELL * j)))
            # column.reverse()
            self.__columns.append(column)

    def check_add_chip(self, column, player):

        # TODO:: User assert on the output of this function
        # why would this ever happen?
        if self.__columns is None:
            return False, -1
        # designated_row = -1

        # loop to find row to insert chip in selected column (index of first
        # empty cell in column counting down)
        # for row in range(Board.BOARD_HEIGHT - 1, -1, -1):
        #     if self.__columns[column][row].get_chip_owner() == game.Game.EMPTY:
        #         designated_row = row
        #         break
        #
        # # if no empty cell was found in column
        # if designated_row == -1:
        #     return False, -1

        taken_cells = [cell
                       for cell in self.__columns[column]
                       if cell.get_chip_owner() != game.Game.EMPTY]

        designated_row = Board.BOARD_HEIGHT - len(taken_cells) - 1 \
            if len(taken_cells) < Board.BOARD_HEIGHT else -1

        if designated_row == -1:
            return False, -1

        # puts chip in correct row in column if found
        self.__set_cell(player, column, designated_row)
        # self.__create_chip(cell.get_location()[0],
        #                    cell.get_location()[1], player)
        #
        # if player == game.get_player():
        #     chip = self.red_piece
        # else:
        #     chip = self.blue_piece
        #
        # self._canvas.create_image(cell.get_location()[0],
        #                     cell.get_location()[1], image=chip,
        #                     anchor=self.NW_ANCHOR)

        return True, designated_row

    def get_chip_location(self, column, row):
        cell = self.__columns[column][row]

        # self.__set_cell(player, column, row)
        return cell.get_location()[0], cell.get_location()[1]
        # self.__create_chip(cell.get_location()[0],
        #                    cell.get_location()[1], player)

    def __set_cell(self, player, column, row):
        self.__columns[column][row].set_chip_owner(player)

    def get_columns(self):
        columns = [[int(self.__columns[col][cell]) for cell in
                    range(len(self.__columns[col]))] for
                   col in range(len(
                self.__columns))]
        return columns

    def get_columns_as_str(self):
        columns = [[str(self.__columns[col][cell])
                    for cell in range(len(self.__columns[col]))]
                   for col in range(len(self.__columns))]

        return columns

    def get_cell_at(self, col, row):
        return self.__columns[col][row]

    def __repr__(self):
        return self.__columns

    def find_connected_and_winner(self, column, row):
        columns = self.__columns
        # Check column
        lst = []
        for j in range(row, min(row + self.WINNING_SEQ_LENGTH,
                                len(columns[column]))):
            if columns[column][j].get_chip_owner() == \
                    self.__get_current_player():
                lst.append((column, j))

        if len(lst) == self.WINNING_SEQ_LENGTH:
            return self.__get_current_player(), lst

        # Check row
        rows = BoardAnalyzer.transpose_matrix(self.__columns)

        for j in range(len(rows[row]) - 3):
            flag = True
            for i in range(self.WINNING_SEQ_LENGTH):
                if rows[row][j + i].get_chip_owner() != \
                        self.__get_current_player():
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
                        if columns[j][i].get_chip_owner() == \
                                self.__get_current_player():
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
                        if columns[j][i].get_chip_owner() == \
                                self.__get_current_player():
                            lst.append((j, i))
                        else:
                            lst.clear()

                if len(lst) == self.WINNING_SEQ_LENGTH:
                    return self.__get_current_player(), lst

        if self.check_draw():
            return game.Game.DRAW, None

        return None, None

    def check_draw(self):
        draw_flag = True
        for col in range(len(self.__columns)):
            for row in range(len(self.__columns[col])):
                if self.__columns[col][row].get_chip_owner() == 3:
                    draw_flag = False

        return draw_flag

    def set_columns(self, str_columns):
        # For backtracking in AI
        self.__columns = [[Cell(None, int(str_columns[col][cell]))
                           for cell in range(len(str_columns[col]))]
                          for col in range(len(str_columns))]
