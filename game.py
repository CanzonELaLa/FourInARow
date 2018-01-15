from board import *


class Game:
    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2
    EMPTY = 3

    def __init__(self):
        self.__board = Board()
        # TODO:: figure out who goes first
        self.__current_player = self.PLAYER_ONE
        self.__canvas = None

    def set_canvas(self, canvas):
        self.__canvas = canvas

    def make_move(self, column):
        self.__board.add_chip(column,
                              self.PLAYER_ONE if not
                              self.__current_player else self.PLAYER_TWO,
                              self.__canvas)

    def get_winner(self):
        pass

    def get_player_at(self, row, col):
        pass

    def get_current_player(self):
        # return self.PLAYER_ONE if self.__player_one_turn else self.PLAYER_TWO
        return self.__current_player

    def get_board(self):
        return self.__board

    def set_current_player(self, player):
        self.__current_player = player