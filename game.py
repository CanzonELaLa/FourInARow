from board import *


class Game:
    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2
    EMPTY = 3

    def __init__(self):
        self.__board = Board()
        # TODO:: figure out who goes first
        # Changes immediatly if this is the client side
        self.__current_player = self.PLAYER_ONE
        self.__player = self.PLAYER_ONE
        self.__canvas = None
        self.__gui = None

    def set_canvas(self, canvas):
        self.__canvas = canvas

    def make_move(self, column):
        # if self.__current_player == 0:
        #     print("server side")
        # else:
        #     print("client side")
        if self.get_winner() is not None:
            raise Exception("Illegal move")
        if not self.__board.add_chip(column,
                              self.PLAYER_ONE if not
                              self.__current_player else self.PLAYER_TWO,
                              self):
            raise Exception("Illegal move")
        self.__toggle_player()

    def __toggle_player(self):
        if self.__current_player == self.PLAYER_ONE:
            self.__current_player = self.PLAYER_TWO
            flag = True
        else:
            self.__current_player = self.PLAYER_ONE
            flag = False

        self.__gui.toggle_column_buttons(flag)

    def get_winner(self):
        return None

    def get_player_at(self, row, col):
        return self.__board.get_columns()[col][row].get_chip().get_player()

    def get_current_player(self):
        # return self.PLAYER_ONE if self.__player_one_turn else self.PLAYER_TWO
        return self.__current_player

    def get_board(self):
        return self.__board

    def set_current_player(self, player):
        self.__current_player = player

    def set_player(self, player):
        self.__player = player

    def get_player(self):
        return self.__player

    def get_canvas(self):
        return self.__canvas

    def set_gui(self, gui):
        self.__gui = gui