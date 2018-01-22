from board_analyzer import *
from sys import argv
from time import time
from board import Board
from copy import deepcopy


class AI:
    def __init__(self):
        self.board_state = BoardAnalyzer()
        self.turn = 0 if len(argv) == 3 else 1
        self.player = self.turn % 2
        self.fictive_board = Board(self.get_current_player)
        self.current_player = None

    def get_current_player(self):
        return self.current_player

    def find_legal_move(self, g, func, timeout=None):
        if timeout is not None:
            start_time = time()

        def helper(ranking_dict, depth, path, optimal_col):
            if timeout is not None:
                if time() - start_time >= timeout - 0.002:
                    return optimal_col

            if len(path) >= depth:
                return optimal_col

            self.current_player = len(path) % 2

            for i in range(Board.BOARD_WIDTH):
                original_columns = deepcopy(
                    self.fictive_board.get_columns_as_str())
                if self.__make_possible_ai_move(i, self.current_player):
                    path.append(i)
                    keys_to_delete = list(get_path_to_remove_from_dict(
                        ranking_dict, path))
                    for key in keys_to_delete:
                        del ranking_dict[key]
                    ranking_dict[tuple(path)] = self.board_state.rank_board(
                        self.player,
                        self.fictive_board.get_columns_as_str())
                    optimal_col = helper(ranking_dict, depth, path,
                           optimal_column(ranking_dict))
                    path.pop()
                    self.current_player = len(path) % 2
                    print(self.current_player, len(path) % 2, path)
                self.fictive_board.set_columns(original_columns)

            if optimal_col == -1:
                raise Exception("sdjf")
            else:
                return optimal_col

        def optimal_column(ranking_dict):
            return max(ranking_dict, key=ranking_dict.get)[self.turn]

        def get_path_to_remove_from_dict(ranking_dict, path):
            for key in ranking_dict.keys():
                if len(path) >= len(key):
                    if key == tuple(path[0:len(key)]):
                        yield key

        start_path = []
        if len(argv) == 4:
            start_path.append(g.get_last_inserted_chip()[0])

        columns = g.get_board().get_columns_as_str()

        self.fictive_board.set_columns(columns)

        ranking_dict = {}
        col = helper(ranking_dict, 4, start_path, -1)
        # print(col)
        func(col)
        # self.turn += 2

    def __make_possible_ai_move(self, column, player):
        return self.fictive_board.check_legal_move_get_row(column, player)[0]
