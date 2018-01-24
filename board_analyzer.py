from itertools import permutations


class BoardAnalyzer:
    """ Analyzes the board """
    # Re-purposed code from ex5

    CONCAT_STR = ""
    SCORE_LEN_ONE = 2
    SCORE_LEN_TWO = SCORE_LEN_ONE ** 2
    SCORE_LEN_THREE = SCORE_LEN_TWO ** 2
    SCORE_LEN_FOUR = 1000

    LEN_ONE_SEQ_PLAYER_ONE = ["0", "3", "3", "3"]
    LEN_TWO_SEQ_PLAYER_ONE = ["0", "0", "3", "3"]
    LEN_THREE_SEQ_PLAYER_ONE = ["0", "0", "0", "3"]
    LEN_FOUR_SEQ_PLAYER_ONE = ("0", "0", "0", "0")

    LEN_ONE_SEQ_PLAYER_TWO = ["1", "3", "3", "3"]
    LEN_TWO_SEQ_PLAYER_TWO = ["1", "1", "3", "3"]
    LEN_THREE_SEQ_PLAYER_TWO = ["1", "1", "1", "3"]
    LEN_FOUR_SEQ_PLAYER_TWO = ("1", "1", "1", "1")

    LEN_TWO_BLOCK_PLAYER_ONE = ["0", "0", "3"]
    LEN_TWO_BLOCK_PLAYER_TWO = ["1", "1", "3"]

    def __init__(self):
        # Creating scoring dicts, keys being (score for row placement,
        # col placement, diag placement)
        # Rows get max score, columns get row - 1 and diags get row // 2
        self.__player_one_states = {(self.SCORE_LEN_ONE, self.SCORE_LEN_ONE
                                     - 1, self.SCORE_LEN_ONE // 2):
                                        set(permutations(
                                            self.LEN_ONE_SEQ_PLAYER_ONE, 4)),
                                    (self.SCORE_LEN_TWO, self.SCORE_LEN_TWO
                                     - 1, self.SCORE_LEN_TWO // 2):
                                        set(permutations(
                                            self.LEN_TWO_SEQ_PLAYER_ONE, 4)),
                                    (self.SCORE_LEN_THREE, self.SCORE_LEN_THREE
                                     - 1, self.SCORE_LEN_THREE // 2):
                                        set(permutations(
                                            self.LEN_THREE_SEQ_PLAYER_ONE, 4)),
                                    (self.SCORE_LEN_FOUR,
                                     self.SCORE_LEN_FOUR,
                                     self.SCORE_LEN_FOUR):
                                        {self.LEN_FOUR_SEQ_PLAYER_ONE}}

        self.__player_two_states = {(self.SCORE_LEN_ONE, self.SCORE_LEN_ONE
                                     - 1, self.SCORE_LEN_ONE // 2):
                                        set(permutations(
                                            self.LEN_ONE_SEQ_PLAYER_TWO, 4)),
                                    (self.SCORE_LEN_TWO, self.SCORE_LEN_TWO
                                     - 1, self.SCORE_LEN_TWO // 2):
                                        set(permutations(
                                            self.LEN_TWO_SEQ_PLAYER_TWO, 4)),
                                    (self.SCORE_LEN_THREE, self.SCORE_LEN_THREE
                                     - 1, self.SCORE_LEN_THREE // 2):
                                        set(permutations(
                                            self.LEN_THREE_SEQ_PLAYER_TWO, 4)),
                                    (self.SCORE_LEN_FOUR,
                                     self.SCORE_LEN_FOUR,
                                     self.SCORE_LEN_FOUR):
                                        {self.LEN_FOUR_SEQ_PLAYER_TWO}}


        self.__player_one_block_states = self.__player_one_states[
            (self.SCORE_LEN_THREE, self.SCORE_LEN_THREE - 1,
             self.SCORE_LEN_THREE // 2)]
        self.__player_two_block_states = self.__player_two_states[
            (self.SCORE_LEN_THREE, self.SCORE_LEN_THREE - 1,
             self.SCORE_LEN_THREE // 2)]
        self.__player_one_block_two_states = set(permutations(
            self.LEN_TWO_BLOCK_PLAYER_ONE, 3))
        self.__player_two_block_two_states = set(permutations(
            self.LEN_TWO_BLOCK_PLAYER_TWO, 3))

    def get_matrix_cols(self, matrix, reverse=False):
        """ :param matrix: Matrix from which to return the rows
            :param reverse: Default is LTR, True will make it RTL
            :return: List of rows as strings
        """

        # Create the list using comprehension
        return [self.CONCAT_STR.join(row if not reverse else row[::-1])
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
                diags_dict[first_loc] = self.CONCAT_STR.join(diagonal)
            else:

                # append the list as a string to diags
                diags.append(self.CONCAT_STR.join(diagonal))

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
                    = self.CONCAT_STR.join(antidiagonal)
            else:

                # append the list as a string to antidiags
                antidiags.append(self.CONCAT_STR.join(antidiagonal))

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

    def rank_board(self, player, str_columns):
        """ :param player: Int representing the player
            :param str_columns: Board state as list of lists of strings
            :return: Score of board for said player
        """
        # Get relevent data from board state
        rows, cols, antidiags, diags = \
            self.get_directional_strings(str_columns, True)

        player_one_rank = 0
        player_two_rank = 0

        # Rank seperatly
        rows_one, rows_two = self.rank_rows_cols_diags(rows)
        cols_one, cols_two = self.rank_rows_cols_diags(cols, cols=True)
        diags_one, diags_two = self.rank_rows_cols_diags(diags, diags=True)
        antidiags_one, antidiags_two = self.rank_rows_cols_diags(antidiags,
                                                                 diags=True)

        # Add up the ranks
        player_one_rank += rows_one + cols_one + diags_one + antidiags_one
        player_two_rank += rows_two + cols_two + diags_two + antidiags_two

        # Return correct rank
        if player == 0:
            return player_one_rank - player_two_rank
        else:
            return player_two_rank - player_one_rank

    def rank_rows_cols_diags(self, dct, cols=False, diags=False):
        """ :param dct: Position: string , of every row/col/diag/antidiag
            :param cols: If dct represents cols
            :param diags: If dct represents diags/antigiads
            :return: Rank of cols/diags/antidiags/rows
        """
        player_one_rank = 0
        player_two_rank = 0
        for string in dct.values():
            for i in range(len(string) - 3):
                for score, sequences in \
                        self.__player_one_states.items():
                    for seq in sequences:
                        if seq == tuple(string[i:i + 4]):
                            if diags: index = 2
                            elif cols: index = 1
                            else: index = 0
                            player_one_rank += score[index]

                for score, sequences in \
                        self.__player_two_states.items():
                    for seq in sequences:
                        if seq == tuple(string[i:i + 4]):
                            if diags: index = 2
                            elif cols: index = 1
                            else: index = 0
                            player_two_rank += score[index]
        return player_one_rank, player_two_rank

    def get_block_and_win_locs(self, player, str_columns):
        directional_dicts = self.get_directional_strings(str_columns, True)
        block_states = self.__player_one_block_states if player \
            else self.__player_two_block_states
        block_two_states = self.__player_one_block_two_states if player \
            else self.__player_two_block_two_states
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
                                            else -(i + block_loc)
                                            if dict_index == 2
                                            else 0)
                            block_locs_to_check.append((expected_row, col))

                for j in range(len(string) - 2):

                    for block_two_state in block_two_states:
                        if block_two_state == tuple(string[j:j + 3]):
                            block_two_loc = block_two_state.index("3")
                            col = starting_loc[1] + (
                                j + block_two_loc if dict_index != 1 else 0)
                            expected_row = starting_loc[0] + \
                                           (j + block_two_loc
                                            if dict_index in [1, 3]
                                            else -(j + block_two_loc)
                                            if dict_index == 2
                                            else 0)
                            block_locs_to_check.append((expected_row, col))

        return win_locs_to_check, block_locs_to_check
