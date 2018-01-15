import tkinter as t
import game

DEFAULT_STATE = "EMPTY"


class Cell:
    def __init__(self, location, board):
        self.__chip = Chip(DEFAULT_STATE)
        self.__location = location
        self.__board = board

    def get_location(self):
        return self.__location

    def set_chip(self, player):
        self.__chip.set_player(player)

    def get_chip(self):
        return self.__chip


class Board:
    # Class constants
    DELTA_HEIGHT = 130
    DELTA_WIDTH = 180
    DELTA_CELL = 109
    CELL_PADDING = 13
    FIRST_PLAYER = "Images/Red.gif"
    SECOND_PLAYER = "Images/Blue.gif"
    NW_ANCHOR = "nw"
    BOARD_WIDTH = 7
    BOARD_HEIGHT = 6

    # TODO:: Make size constants
    def __init__(self):
        self.__columns = []
        self.red_piece = t.PhotoImage(file=self.FIRST_PLAYER)
        self.blue_piece = t.PhotoImage(file=self.SECOND_PLAYER)

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

    def add_chip(self, column, player, canvas):
        # TODO:: User assert on the output of this function
        if self.__columns is None:
            return False
        row = -1

        for i in range(Board.BOARD_HEIGHT - 1, 0, -1):
            if self.__columns[column][i].get_chip().get_player() == \
                    DEFAULT_STATE:
                row = i

                break
        if row == -1:
            return False

        cell = self.__columns[column][row]

        if player == game.Game.PLAYER_ONE:
            chip = self.red_piece
        elif player == game.Game.PLAYER_TWO:
            chip = self.blue_piece
        else:
            chip = None
            assert False

        self.__set_cell(player, column, row)
        canvas.create_image(cell.get_location()[0],
                            cell.get_location()[1], image=chip,
                            anchor=self.NW_ANCHOR)

        return True

    def __set_cell(self, player, column, row):
        self.__columns[column][row].get_chip().set_player(player)

    def get_columns(self):
        return self.__columns


class Chip:
    def __init__(self, player):
        self.__player = player

    def get_player(self):
        return self.__player

    def set_player(self, player):
        self.__player = player
