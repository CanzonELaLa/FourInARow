from itertools import permutations

class Board_State:
    # Re-purposed code from ex5

    EMPTY_STRING = ""

    # PLAYER_ONE_STATES = ["0003", "3000", "0030", "0300", "0033", "0330",
    #                      "0303", "3300", "3003", "3030", "3330", "3303",
    #                      "3033", "0333"]


    def __init__(self):
        self.__player_one_states = {1: permutations(["0", "3", "3", "3"], 4),
                             2: permutations(["0", "0", "3", "3"], 4),
                             3: permutations(["0", "0", "0", "3"], 4)}

        self.__player_two_states = {1: permutations(["1", "3", "3", "3"], 4),
                             2: permutations(["1", "1", "3", "3"], 4),
                             3: permutations(["1", "1", "1", "3"], 4)}

    def get_matrix_rows(self, matrix, reverse=False):
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

    def get_matrix_diagonals(self, matrix, reverse=False):
        """ :param matrix: Matrix from which to extract diagonals
            :param reverse: determines whether returned list will contain
                            right descending diagonals (if False)
                            or left ascending diagonals (if True)
            :return: List of strings of all characters. All strings will be
                     right descending diagonals or left ascending diagonals
                     based on reverse
        """

        # initializes returned antidiags list to empty list
        diags = []

        # saves the matrix row length and matrix column length
        len_rows = len(matrix)
        len_cols = len(matrix[0])

        # The indices of all characters on the same diagonal
        # of a matrix share the same difference
        # (difference < |row_length - column_length|)
        for indices_diff in range(len_rows - 1, -len_cols, -1):

            # creates a list of all characters on the same diagonal
            # based on current indices_diff
            diagonal = [matrix[i][j] for i in range(len_rows)
                        for j in range(len_cols) if indices_diff == i - j]

            # if reverse == true, reverse the list
            if reverse:
                diagonal = diagonal[::-1]

            # append the list as a string to diags
            diags.append(self.EMPTY_STRING.join(diagonal))

        return diags

    def get_matrix_antidiagonals(self, matrix, reverse=False):
        """ :param matrix: Matrix from which to extract diagonals
            :param reverse: determines whether returned list will contain
                            right ascending diagonals (if False)
                            or left descending diagonals (if True)
            :return: List of strings of all characters. All strings will be
                     right ascending diagonals or left descending diagonals
                     based on reverse
        """

        # initializes returned antidiags list to empty list
        antidiags = []

        # saves the matrix row length and matrix column length
        len_rows = len(matrix)
        len_cols = len(matrix[0])

        # The indices of all characters on the same antidiagonal
        # of a matrix share the same sum
        # (sums range from 0 to column length + row_length -1)
        for indices_sum in range(len_rows + len_cols - 1):

            # creates a list of all characters on the same antidiagonal
            # based on current indices_sum
            antidiagonal = [matrix[i][j] for j in range(len_cols)
                            for i in range(len_rows) if indices_sum == i + j]

            # if reverse == true, reverse the list
            if reverse:
                antidiagonal = antidiagonal[::-1]

            # append the list as a string to antidiags
            antidiags.append(self.EMPTY_STRING.join(antidiagonal))

        return antidiags

    def get_directional_strings(self, matrix):
        """ :param matrix: Matrix to search through
            :param directions: Relevant directions to search matrix
            :return: List of all possible rows/columns/diagonals as strings to
                     search through
        """

        directional_strings = []

        directional_strings += self.get_matrix_rows(matrix)
        directional_strings += self.get_matrix_rows(self.transpose_matrix(
            matrix))
        directional_strings += self.get_matrix_antidiagonals(matrix)
        directional_strings += self.get_matrix_diagonals(matrix)

        return directional_strings

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
        directional_strings = self.get_directional_strings(str_columns)

        player_one_rank = 0
        player_two_rank = 0

        for string in directional_strings:
            for i in range(len(string) - 3):
                for score, sequences in self.__player_one_states.items():
                    for seq in sequences:
                        if seq == string[i:i + 4]:
                            player_one_rank += score

                for score, sequences in self.__player_two_states.items():
                    for seq in sequences:
                        if seq == string[i:i + 4]:
                            player_two_rank += score

        if player == 0:
            return player_one_rank - player_two_rank
        else:
            return player_two_rank - player_one_rank