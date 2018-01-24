from board_analyzer import *
from sys import argv
from time import time
from board import Board
from copy import deepcopy

RANK_LOWER_BOUND = -500


class AI:

    FIND_LEGAL_MOVE_FAILED = "CANNOT FIND ANY MOVES"

    def __init__(self):
        """
        Initializes AI class
        """
        # Pre-creating BoardAnalyzer so as not to init it everytime
        self.__board_analyzer = BoardAnalyzer()
        self.__turn = 0 if len(argv) == 3 else 1
        self.__player = self.__turn % 2
        self.__fictive_board = Board(self.get_current_player)
        self.__current_player = None

    def get_current_player(self):
        """ Getter of current player for fictive board """
        return self.__current_player

    def find_legal_move(self, g, func, timeout=None):
        """ :param g: Game object
            :param func: Func for placing chip and updating board from game
            :param timeout: Possible argument that will halt processing """

        # If timeout is set, start timing the function, doing this before
        # declaring functions so as to get the most precise assessment
        if timeout is not None:
            start_time = time()

        def helper(ranking_dict, depth, path, optimal_col):
            """ Recursive backtracking function to analyze board possible
                outcomes
                :param ranking_dict: Current ranking of board given paths
                :param depth: Int of how many moves to simulate
                :param path: Current path taken to get here
                :param optimal_col: Current best column to output
                :return: Optimal_col
            """
            if timeout is not None:  # Edge case, timeout is over
                # Decreasing 0.02 for first algorithm
                if time() - start_time >= timeout - 0.002:
                    return optimal_col

            if len(path) >= depth:  # Regular edge case
                return optimal_col

            # Determine current player and update member
            self.__current_player = len(path) % 2

            # For each column, try placing chip
            for i in range(Board.BOARD_WIDTH):
                # Copy data for backtracking
                original_columns = deepcopy(
                    self.__fictive_board.get_columns_as_str())

                # Check validity of move
                if self.__make_possible_ai_move(i, self.__current_player):
                    unwanted_path = False
                    path.append(i)  # Update path
                    # FIgure out which paths in ranking dict are no longer
                    # relevant
                    keys_to_delete = list(get_path_to_remove_from_dict(
                        ranking_dict, path))
                    # Remove them
                    for dict_path in keys_to_delete:
                        del ranking_dict[dict_path]
                    # Rank current path
                    path_rank = self.__board_analyzer.rank_board(
                        self.__player, self.__fictive_board.get_columns_as_str())
                    if path_rank > RANK_LOWER_BOUND:
                        ranking_dict[tuple(path)] = path_rank
                        optimal_col = helper(ranking_dict, depth, path,
                                             optimal_column(ranking_dict))
                    else:
                        unwanted_path = True
                    path.pop()  # Backtrack
                    self.__current_player = len(path) % 2

                    # Edge case, if enemy has won, dont go with this move
                    if unwanted_path:
                        for dict_path, rank in ranking_dict.items():
                            ranking_dict[dict_path] = \
                                (RANK_LOWER_BOUND
                                 if dict_path [0:depth - 2] == path[0]
                                 else rank)
                        break  # Stop going down this path
                self.__fictive_board.set_columns(original_columns)  # Backtrack

            # Should never happen
            if optimal_col < 0 or optimal_col > 6:
                raise Exception(self.FIND_LEGAL_MOVE_FAILED)
            else:
                return optimal_col

        def optimal_column(ranking_dict):
            """ :param ranking_dict: Current ranking by path
                :return: Returns best column by rank """
            return max(ranking_dict, key=ranking_dict.get)[self.__turn]

        def get_path_to_remove_from_dict(ranking_dict, path):
            """ :param ranking_dict: Current ranking by path
                :param path: List of moves prior
                :return: Keys to delete """
            for key in ranking_dict.keys():
                if len(path) >= len(key):
                    if key == tuple(path[0:len(key)]):
                        yield key

        col = None
        game_board = g.get_board()
        win_locs, block_locs = self.__board_analyzer.get_block_and_win_locs(
            self.__player, game_board.get_columns_as_str())

        for loc in win_locs:
            success, row = game_board.check_legal_move_get_row(
                loc[1], self.__player, False)
            if success and row == loc[0]:
                col = loc[1]
                break

        if col is None:
            for loc in block_locs:
                success, row = game_board.check_legal_move_get_row(
                    loc[1], self.__player, False)
                if success and row == loc[0]:
                    col = loc[1]
                    break

        if col is None:
            # Create initial variables
            start_path = []
            depth = 3
            if len(argv) == g.EXPECTED_AMOUNT_OF_ARGUMENTS_FOR_CLIENT:
                start_path.append(g.get_last_inserted_chip()[0])
                depth = 4

            columns = g.get_board().get_columns_as_str()

            self.__fictive_board.set_columns(columns)

            ranking_dict = {}
            col = helper(ranking_dict, depth, start_path, 3)

        func(col)

    def __make_possible_ai_move(self, column, player):
        """ :param column: Column in which to place chip
        :param player: Owner of chip
        :return: Success or failure """
        return self.__fictive_board.check_legal_move_get_row(column, player)[0]
