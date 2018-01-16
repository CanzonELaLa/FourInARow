import tkinter as t
import game

DEFAULT_STATE = "EMPTY"


class Cell:
    def __init__(self, location, board):
        self.__chip_owner = game.Game.EMPTY
        self.__location = location
        self.__board = board

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

    # TODO:: Make size constants
    def __init__(self, canvas, create_chip):
        self.__columns = []
        self._canvas = canvas
        self.__create_chip = create_chip

        for i in range(7):
            column = []
            for j in range(6):
                column.append(Cell((self.DELTA_WIDTH + self.CELL_PADDING +
                                    (self.CELL_PADDING - 2) * i +
                                    self.DELTA_CELL * i,
                                    self.DELTA_HEIGHT + self.CELL_PADDING +
                                    (self.CELL_PADDING - 2) * j +
                                    self.DELTA_CELL * j), self))
            # column.reverse()
            self.__columns.append(column)

    def add_chip(self, column, player):
        # TODO:: User assert on the output of this function
        if self.__columns is None:
            return False, -1
        designated_row = -1

        for row in range(Board.BOARD_HEIGHT - 1, -1, -1):
            if self.__columns[column][row].get_chip_owner() == game.Game.EMPTY:
                designated_row = row
                break

        if designated_row == -1:
            return False, -1

        cell = self.__columns[column][designated_row]

        self.__set_cell(player, column, designated_row)
        self.__create_chip(cell.get_location()[0],
                           cell.get_location()[1], player)
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

    def __set_cell(self, player, column, row):
        self.__columns[column][row].set_chip_owner(player)

    def get_columns(self):
        columns = [[int(self.__columns[col][cell]) for cell in
                    range(len(self.__columns[col]))] for
                   col in range(len(
                self.__columns))]
        return columns

    def get_columns_as_str(self):
        columns = [[str(self.__columns[col][cell]) for cell in range(len(
            self.__columns[col]))] for col in range(len(self.__columns))]

        return columns

    def get_cell_at(self, col, row):
        return self.__columns[col][row]

    def __repr__(self):
        return self.__columns

#
#
# class Chip:
#     def __init__(self, player):
#         self.__player = player
#
#     def get_player(self):
#         return self.__player
#
#     def set_player(self, player):
#         self.__player = player
#
#     def __repr__(self):
#         return str(self.__player)
