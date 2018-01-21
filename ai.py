from board_analyzer import *
from sys import argv
from time import time
from board import Board
from copy import deepcopy


class AI:
    def __init__(self):
        self.__board_state = BoardAnalyzer()
        self.__turn = 0 if len(argv) == 3 else 1
        self.__player = self.__turn % 2
        self.__fictive_board = Board(self.get_current_player, self.get_player)
        self.__current_player = None

    def get_current_player(self):
        return self.__current_player

    def get_player(self):
        return self.__player

    def find_legal_move(self, g, func, timeout=None):
        start_time = time()

        def helper(ranking_dict, depth, path):
            if timeout is not None:
                if time() - start_time >= timeout:
                    return optimal_column(ranking_dict)

            if len(path) >= depth:
                return optimal_column(ranking_dict)

            self.__current_player = len(path) % 2

            for i in range(Board.BOARD_WIDTH):
                org_columns = deepcopy(
                    self.__fictive_board.get_columns_as_str())
                org_ranking_dict = dict(ranking_dict)
                if self.__make_possible_ai_move(i, len(path) % 2):
                    for key in get_path_to_remove_from_dict(ranking_dict,
                                                            path):
                        del ranking_dict[key]
                    ranking_dict[tuple(path)] = self.__board_state.rank_board(
                        len(path) % 2,
                        self.__fictive_board.get_columns_as_str())
                    path.append(i)
                    return helper(ranking_dict, depth, path)
                ranking_dict = dict(org_ranking_dict)
                self.__fictive_board.set_columns(org_columns)
                path.remove(len(path) - 1)

            raise Exception("sdjf")

        def optimal_column(ranking_dict):
            return max(ranking_dict, key=ranking_dict.get)[self.__turn]

        def get_path_to_remove_from_dict(ranking_dict, path):
            for key in ranking_dict.keys():
                if len(path) >= len(key):
                    if key == tuple(path[0:len(key)]):
                        yield key

        start_path = []
        if len(argv) == 4:
            start_path.append(g.get_last_inserted_chip()[0])
        columns = g.get_board().get_columns_as_str()
        self.__fictive_board.set_columns(columns)
        column = helper(dict(), 4, start_path)
        func(column)
        self.__turn += 2

    def __make_possible_ai_move(self, column, player):
        return self.__fictive_board.check_add_chip(column, player)[0]
        # taken_cells = [cell
        #                for cell in columns[column]
        #                if cell.get_chip_owner() != 3]
        # designated_row = Board.BOARD_HEIGHT - len(taken_cells) - 1 \
        #     if len(taken_cells) < Board.BOARD_HEIGHT else -1
        #
        # if designated_row == -1:
        #     return False, -1
