from board import *
from communicator import *
from sys import argv
from GUI import GUI


# WIN_LABEL = "Images/You win.gif"
# LOSE_LABEL = "Images/You lose.gif"
# DRAW_LABEL = "Images/Draw.gif"
# BG_IMAGE = "Images/bg.gif"
# FIRST_PLAYER_CHIP = "Images/Red.gif"
# SECOND_PLAYER_CHIP = "Images/Blue.gif"
# FIRST_PLAYER_WIN_CHIP = "Images/Red_glow.gif"
# SECOND_PLAYER_WIN_CHIP = "Images/Blue_glow.gif"

class Game:
    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2
    EMPTY = 3
    MIN_PORT_VALUE = 1000
    MAX_PORT_VALUE = 65535

    WINNING_SEQ_LENGTH = 4

    ILLEGAL_MOVE = "Illegal move"
    INVALID_MESSAGE = "Invalid message received"
    INVALID_GAME_STATE = "Invalid game state"
    CHECK_WINNER_FLAG_INDEX = 29
    ADD_CHIP_FAILED = "Failed to add chip to specified column"
    COMMUNICATOR_MESSAGE_1 = "CHIP_DATA: "
    COMMUNICATOR_MESSAGE_2 = "CHECK_WINNER: "

    def __init__(self):

        # if server mode is on (no IP address provided)
        if len(argv) == 3:
            self.__player = self.PLAYER_ONE
            self.__enemy_player = self.PLAYER_TWO
            self.__current_player = self.__player
        else:
            self.__player = self.PLAYER_TWO
            self.__enemy_player = self.PLAYER_ONE
            self.__current_player = self.__enemy_player


        self.__gui = GUI(self.__player, self.__make_move,
                         self.get_current_player, self.get_player)

        if self.__player == self.PLAYER_TWO:
            self.__gui.disable_column_buttons()

        self.__board = Board(self.__gui.get_canvas())
        self.__win_checker = WinSearch()
        self.__game_over = False


        # TODO:: Ugly code, find a workaround
        self.__last_inserted_chip = None


        port = int(argv[2])
        ai = True if argv[1] == "ai" else False  # currently not in use
        ip = None

        if len(argv) == 4:
            ip = argv[3]

        self.__communicator = Communicator(self.__gui.get_root(), port, ip)
        self.__communicator.connect()
        self.__communicator.bind_action_to_message(self.eat_message)


        self.__gui.get_root().mainloop()

    def __make_move(self, column):
        # if game over flag on, returns
        if self.__game_over:
            return

        # attempts to place chip in column
        success, row = self.__board.check_add_chip(column,
                                                   self.PLAYER_ONE if not
                                                   self.__current_player else
                                                   self.PLAYER_TWO)
        if not success:
            raise Exception(self.ILLEGAL_MOVE)

        self.__last_inserted_chip = column, row

        if self.__current_player == self.__player:
            self.__communicator.send_message(self.COMMUNICATOR_MESSAGE_1
                                             + str(column) + "," + str(row)
                                             + " " + self.COMMUNICATOR_MESSAGE_2
                                             + "1" if not self.__game_over else
                                             "0")

        self.__check_winner(column, row)


    def __check_winner(self, column, row):
        winner, winning_chips = self.__find_connected_and_winner(column, row)
        x, y = self.__board.get_chip_location(column, row)
        if winner is None:
            self.__gui.create_chip_on_board(x, y, self.__current_player)
            self.__toggle_player()
            self.__disable_illegal_columns()
        else:
            self.__game_over = True
            if winner == self.DRAW:
                self.__gui.create_chip_on_board(x, y, self.__current_player)
                self.__gui.disable_column_buttons()
                self.__gui.show_game_over_label(self.DRAW)
            else:
                self.__gui.create_chip_on_board(x, y, self.__current_player,
                                                winning_chips=winning_chips,
                                                board=self.__board,
                                                winner=winner)
            # if winner == self.__player:
            #     self.__game_over = True
            #     self.__gui.disable_column_buttons()
            #     self.__gui.show_win()
            # elif winner == self.__enemy_player:
            #     self.__game_over = True
            #     self.__gui.disable_column_buttons()
            #     self.__gui.show_lose()

    def __find_connected_and_winner(self, column, row):
        columns = self.__board.get_columns()
        # Check column
        lst = []
        for j in range(row, min(row + self.WINNING_SEQ_LENGTH,
                                len(columns[column]))):
            if columns[column][j] == self.__current_player:
                lst.append((column, j))

        if len(lst) == self.WINNING_SEQ_LENGTH:
            return self.__current_player, lst

        # Check row
        rows = self.__win_checker.transpose_matrix(self.__board.get_columns())

        for j in range(len(rows[row]) - 3):
            flag = True
            for i in range(self.WINNING_SEQ_LENGTH):
                if rows[row][j + i] != self.__current_player:
                    flag = False
                    break

            if flag:
                return self.__current_player, [(k, row) for k in
                                               range(j, j +
                                                     self.WINNING_SEQ_LENGTH
                                                     )]

        # Check diagonal
        for indices_diff in range(len(rows) - 1, -len(columns), -1):
            lst = []
            for i in range(len(rows)):
                for j in range(len(columns)):
                    if indices_diff == i - j:
                        if columns[j][i] == self.__current_player:
                            lst.append((j, i))
                        else:
                            lst.clear()

                if len(lst) == self.WINNING_SEQ_LENGTH:
                    return self.__current_player, lst

        # Check anti-diagonal
        for indices_sum in range(len(rows) + len(columns) - 1):
            lst = []
            for i in range(len(rows)):
                for j in range(len(columns)):
                    if indices_sum == i + j:
                        if columns[j][i] == self.__current_player:
                            lst.append((j, i))
                        else:
                            lst.clear()

                if len(lst) == self.WINNING_SEQ_LENGTH:
                    return self.__current_player, lst

        if self.check_draw():
            return self.DRAW, None

        return None, None

    def __disable_illegal_columns(self):
        columns = self.__board.get_columns()
        for i in range(len(columns)):
            illegal_column = True
            for cell in columns[i]:
                if cell == self.EMPTY:
                    illegal_column = False
                    break
            if illegal_column:
                self.__gui.disable_illegal_button(i)

    def check_draw(self):
        board_columns = self.__board.get_columns()
        draw_flag = True
        for col in range(len(board_columns)):
            for row in range(len(board_columns[col])):
                if board_columns[col][row] == self.EMPTY:
                    draw_flag = False

        return draw_flag

    def __toggle_player(self):
        self.__current_player = self.PLAYER_TWO \
            if self.__current_player == self.PLAYER_ONE \
            else self.PLAYER_ONE

        flag = self.__current_player == self.__player

        self.__gui.toggle_column_buttons(flag)

    def get_winner(self):
        # board_columns = self.__board.get_columns_as_str()
        # winner = self.__win_checker.get_winner_from_columns(board_columns)
        # if winner is not None:
        #     return winner
        # else:
        #     if self.check_draw():
        #         return self.DRAW
        #
        # return None
        return self.__find_connected_and_winner(
            self.__last_inserted_chip[0], self.__last_inserted_chip[1])[0]

    def get_player_at(self, row, col):
        return self.__board.get_columns()[col][row]  # .get_chip_owner()

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

    def set_gui(self, gui):
        self.__gui = gui

    def eat_message(self, message):
        if len(message) != 30:
            raise Exception(self.INVALID_MESSAGE)

        column = int(message[11])
        expected_row = int(message[13])

        success, row = self.__board.check_add_chip(column, self.PLAYER_ONE
                                                   if not self.__current_player
                                                   else self.PLAYER_TWO)

        assert row == expected_row

        if success:
            check_winner_flag = message[self.CHECK_WINNER_FLAG_INDEX]
            if check_winner_flag:
                self.__check_winner(column, row)

        else:
            raise Exception(self.ADD_CHIP_FAILED)

    def get_root(self):
        return self.__gui.get_root()


class WinSearch:
    # Re-purposed code from ex5

    EMPTY_STRING = ""
    WIN_STATES = ["0000", "1111"]

    def __init__(self):
        pass

    def get_matrix_rows(self, matrix, reverse=False):
        """ :param matrix: Matrix from which to return the rows
            :param reverse: Default is LTR, True will make it RTL
            :return: List of rows as strings
        """

        # Create the list using comprehension
        return [self.EMPTY_STRING.join(row if not reverse else row[::-1])
                for row in matrix]

    def transpose_matrix(self, matrix):
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

    def get_winner(self, directional_strings, word_list):
        for string in directional_strings:
            for i in range(len(string)):
                for word in word_list:
                    if word == string[i:i + len(word)]:
                        return word[0]
        return None

    def get_winner_from_columns(self, columns):
        winner = self.get_winner(self.get_directional_strings(columns),
                                 self.WIN_STATES)
        return int(winner) if winner is not None else None

    # def get_states(self, columns, ):
