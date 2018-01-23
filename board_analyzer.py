from itertools import permutations


class BoardAnalyzer:
    """ Analyzes the board """
    # Re-purposed code from ex5

    EMPTY_STRING = ""

    def __init__(self):
        # Creating scoring dicts, keys being (score for row placement,
        # col placement, diag placement)
        self.__player_one_states = {(2, 1, 1):
                                        set(permutations(["0", "3", "3", "3"],
                                                         4)),
                                    (4, 3, 4):
                                        set(permutations(["0", "0", "3", "3"],
                                                         4)),
                                    (16, 15, 8):
                                        set(permutations(["0", "0", "0", "3"],
                                                         4)),
                                    (1000, 1000, 1000): {("0", "0", "0", "0")}}

        self.__player_two_states = {(2, 1, 1):
                                        set(permutations(["1", "3", "3", "3"],
                                                         4)),
                                    (4, 3, 4):
                                        set(permutations(["1", "1", "3", "3"],
                                                         4)),
                                    (16, 15, 8):
                                        set(permutations(["1", "1", "1", "3"],
                                                         4)),
                                    (1000, 1000, 1000): {("1", "1", "1", "1")}}

        self.__player_one_block_states = self.__player_one_states[(16, 15, 8)]
        self.__player_two_block_states = self.__player_two_states[(16, 15, 8)]

    def get_matrix_cols(self, matrix, reverse=False):
        """ :param matrix: Matrix from which to return the rows
            :param reverse: Default is LTR, True will make it RTL
            :return: List of rows as strings
        """

        # Create the list using comprehension
        return [self.EMPTY_STRING.join(row if not reverse else row[::-1])
                for row in matrix]

    @staticmethod
    def transpose_matrix(matrix):
        """ :param matrix: Matrix to transpose
            :return: Transposed matrix
        """

        # switches places between inner and outer list
        return [[matrix[j][i] for j in range(len(matrix))]
                for i in range(len(matrix[0]))]

    def get_matrix_diagonals(self, matrix, return_as_dict, reverse=False):
        """ :param matrix: Matrix from which to extract diagonals
            :param reverse: determines whether returned list will contain
                            right descending diagonals (if False)
                            or left ascending diagonals (if True)
            :param return_as_dict: if True, returns diagonals as
                                   dictionary where the value of each
                                   diagonal is its starting column.
            :return: List of strings of all characters. All strings will be
                     right descending diagonals or left ascending diagonals
                     based on reverse
        """

        # initializes returned antidiags list to empty list
        diags = []
        diags_dict = dict()

        # saves the matrix row length and matrix column length
        len_cols = len(matrix)
        len_rows = len(matrix[0])

        # The indices of all characters on the same diagonal
        # of a matrix share the same difference
        # (difference < |row_length - column_length|)
        for indices_diff in range(len_rows - 1, -len_cols, -1):

            first_loc_flag = return_as_dict
            diagonal = []

            for i in range(len_cols):
                for j in range(len_rows):
                    if i - j == indices_diff:
                        diagonal.append(matrix[i][j])
                        if first_loc_flag:
                            first_loc = j, i
                            first_loc_flag = False

            # if reverse == true, reverse the list
            if reverse:
                diagonal = diagonal[::-1]

            if return_as_dict:
                diags_dict[first_loc] = self.EMPTY_STRING.join(diagonal)
            else:

                # append the list as a string to diags
                diags.append(self.EMPTY_STRING.join(diagonal))

        if return_as_dict:
            return diags_dict
        return diags

    def get_matrix_antidiagonals(self, matrix, return_as_dict, reverse=False):
        """ :param matrix: Matrix from which to extract diagonals
            :param reverse: determines whether returned list will contain
                            right ascending diagonals (if False)
                            or left descending diagonals (if True)
            :param return_as_dict: if True, returns antidiagonals as
                                         dictionary where the value of each
                                         antidiagonal is its starting column.
            :return: List of strings of all characters. All strings will be
                     right ascending diagonals or left descending diagonals
                     based on reverse
        """

        # initializes returned antidiags list to empty list
        antidiags = []
        antidiags_dict = dict()

        # saves the matrix row length and matrix column length
        len_cols = len(matrix)
        len_rows = len(matrix[0])

        # The indices of all characters on the same antidiagonal
        # of a matrix share the same sum
        # (sums range from 0 to column length + row_length -1)
        for indices_sum in range(len_rows + len_cols - 1):

            first_loc_flag = return_as_dict
            antidiagonal = []

            # creates a list of all characters on the same antidiagonal
            # based on current indices_sum
            for i in range(len_cols):
                for j in range(len_rows):
                    if i + j == indices_sum:
                        antidiagonal.append(matrix[i][j])
                        if first_loc_flag:
                            first_loc = j, i
                            first_loc_flag = False

            # if reverse == true, reverse the list
            if reverse:
                antidiagonal = antidiagonal[::-1]

            if return_as_dict:
                antidiags_dict[first_loc] \
                    = self.EMPTY_STRING.join(antidiagonal)
            else:

                # append the list as a string to antidiags
                antidiags.append(self.EMPTY_STRING.join(antidiagonal))

        if return_as_dict:
            return antidiags_dict
        return antidiags

    def get_directional_strings(self, matrix, return_as_dict=False):
        """ :param matrix: Matrix to search through
            :param return_as_dict:
            :return: List of all possible rows/columns/diagonals as strings to
                     search through
        """

        rows = self.get_matrix_cols(self.transpose_matrix(matrix))
        cols = self.get_matrix_cols(matrix)
        antidiags = self.get_matrix_antidiagonals(matrix, return_as_dict)
        diags = self.get_matrix_diagonals(matrix, return_as_dict)

        if return_as_dict:
            rows_dict = dict()
            cols_dict = dict()

            for i in range(len(rows)):
                rows_dict[(i, 0)] = rows[i]

            for j in range(len(cols)):
                cols_dict[(0, j)] = cols[j]

            return rows_dict, cols_dict, antidiags, diags
        return rows + cols + antidiags + diags

    # def get_winner(self, directional_strings, word_list):
    #     for string in directional_strings:
    #         for i in range(len(string)):
    #             for word in word_list:
    #                 if word == string[i:i + len(word)]:
    #                     return word[0]
    #     return None
    #
    # def get_winner_from_columns(self, columns):
    #     winner = self.get_winner(self.get_directional_strings(columns),
    #                              self.WIN_STATES)
    #     return int(winner) if winner is not None else None
    #
    #     # def get_states(self, columns, ):

    def rank_board(self, player, str_columns):
        rows, cols, antidiags, diags = \
            self.get_directional_strings(str_columns, True)

        player_one_rank = 0
        player_two_rank = 0

        rows_one, rows_two = self.rank_rows_cols(rows)
        cols_one, cols_two = self.rank_rows_cols(cols, True)
        diags_one, diags_two = self.rank_diags({**diags, **antidiags})

        player_one_rank += rows_one + diags_one + cols_one
        player_two_rank += rows_two + diags_two + cols_two

        if player == 0:
            return player_one_rank - player_two_rank
        else:
            return player_two_rank - player_one_rank

    def rank_diags(self, lst):
        player_one_rank = 0
        player_two_rank = 0
        for string in lst:
            for i in range(len(string) - 3):
                for score, sequences in \
                        self.__player_one_states.items():
                    for seq in sequences:
                        if seq == tuple(string[i:i + 4]):
                            player_one_rank += score[2]

                for score, sequences in \
                        self.__player_two_states.items():
                    for seq in sequences:
                        if seq == tuple(string[i:i + 4]):
                            player_two_rank += score[2]

        return player_one_rank, player_two_rank

    def rank_rows_cols(self, dct, cols=False):
        player_one_rank = 0
        player_two_rank = 0
        for string in dct.values():
            for i in range(len(string) - 3):
                for score, sequences in \
                        self.__player_one_states.items():
                    for seq in sequences:
                        if seq == tuple(string[i:i + 4]):
                            player_one_rank += score[1 if cols else 0]

                for score, sequences in \
                        self.__player_two_states.items():
                    for seq in sequences:
                        if seq == tuple(string[i:i + 4]):
                            player_two_rank += score[1 if cols else 0]
        return player_one_rank, player_two_rank

    def get_block_locs(self, player, str_columns):
        directional_dicts = self.get_directional_strings(str_columns, True)
        block_states = self.__player_one_block_states if player \
            else self.__player_two_block_states

        block_locs_to_check = []

        for dict_index in range(len(directional_dicts)):
            for starting_loc, string in directional_dicts[dict_index].items():
                for i in range(len(string) - 3):
                    for block_state in block_states:
                        if block_state == tuple(string[i:i + 4]):
                            block_loc = block_state.index("3")
                            col = starting_loc[1] + (
                                i + block_loc if dict_index != 1 else 0)
                            expected_row = starting_loc[0] + \
                                           (i + block_loc
                                            if dict_index in [1, 3]
                                            else -i - block_loc if
                                           dict_index == 2 else 0)
                            block_locs_to_check.append((expected_row, col))
        return block_locs_to_check

    def get_block_and_win_locs(self, player, str_columns):
        directional_dicts = self.get_directional_strings(str_columns, True)
        block_states = self.__player_one_block_states if player \
            else self.__player_two_block_states
        win_states = self.__player_two_block_states if player \
            else self.__player_one_block_states

        win_locs_to_check = []
        block_locs_to_check = []

        for dict_index in range(len(directional_dicts)):
            for starting_loc, string in directional_dicts[dict_index].items():
                for i in range(len(string) - 3):
                    for win_state in win_states:
                        if win_state == tuple(string[i:i + 4]):
                            win_loc = win_state.index("3")
                            col = starting_loc[1] + (
                                i + win_loc if dict_index != 1 else 0)
                            expected_row = starting_loc[0] + \
                                           ((i + win_loc)
                                            if dict_index in [1, 3]
                                            else -(i + win_loc)
                                           if dict_index == 2
                                           else 0)
                            win_locs_to_check.append((expected_row, col))

                    for block_state in block_states:
                        if block_state == tuple(string[i:i + 4]):
                            block_loc = block_state.index("3")
                            col = starting_loc[1] + (
                                i + block_loc if dict_index != 1 else 0)
                            expected_row = starting_loc[0] + \
                                           (i + block_loc
                                            if dict_index in [1, 3]
                                            else -i - block_loc
                                           if dict_index == 2
                                           else 0)
                            block_locs_to_check.append((expected_row, col))
        return win_locs_to_check, block_locs_to_check
