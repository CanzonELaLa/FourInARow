from board import *
from sys import argv
from random import randint

DELTA_HEIGHT = 130
DELTA_WIDTH = 180
DELTA_CELL = 109
CELL_PADDING = 13
FIRST_PLAYER = "Images/Red.gif"
SECOND_PLAYER = "Images/Blue.gif"
YOUR_TURN = "Images/Your turn.gif"
ENEMY_TURN = "Images/Enemy turn.gif"
BG_IMAGE = "Images/bg.gif"
WIN_LABEL = "Images/You win.gif"
LOSE_LABEL = "Images/You lose.gif"
CENTER_ANCHOR = "center"
NW_ANCHOR = "nw"
WIN_STATES = ["0000", "1111"]


class GUI:
    """
    Designed to handle the GUI aspects (creating a window, buttons and
    pop-ups. Also initializes the communicator object.
    """

    MESSAGE_DISPLAY_TIMEOUT = 250

    def __init__(self, player, make_move):
        """
        Initializes the GUI and connects the communicator.
        :param parent: the tkinter root.
        """
        self.__root = t.Tk()
        self.__root.resizable(width=False, height=False)

        self.__game = game
        self._canvas = t.Canvas(self.__root, width=1200, height=860)
        self._canvas.pack()
        self.__bg = t.PhotoImage(file=BG_IMAGE)
        self._canvas.create_image(0, 0, image=self.__bg, anchor="nw")
        self.__player = player
        self.__make_move = make_move

        # UI things
        self.__column_buttons = []
        self.__column_button_images = [t.PhotoImage(file="Images/button" +
                                                         str(x) + ".gif")
                                       for x in range(1, 8)]
        # TODO:: This is some ugly way of doing this
        self.__labels_images = {}
        self.__labels_images["Your Turn"] = t.PhotoImage(file=YOUR_TURN)
        self.__labels_images["Enemy Turn"] = t.PhotoImage(file=ENEMY_TURN)
        self.__labels_images["You Win"] = t.PhotoImage(file=WIN_LABEL)
        self.__labels_images["You Lose"] = t.PhotoImage(file=LOSE_LABEL)


        self.red_piece = t.PhotoImage(file=FIRST_PLAYER)
        self.blue_piece = t.PhotoImage(file=SECOND_PLAYER)

        # TODO:: Refactor to dictionary
        self.__your_label = None
        self.__enemy_label = None
        self.__place_widgets()
        # self.__game = Game()
        # self.__game.set_canvas(self._canvas)
        # self.__game.set_gui(self)
        # if len(argv) == 4:
        #     self.__game.set_current_player(self.__game.PLAYER_TWO)
        #     self.__game.set_player(self.__game.PLAYER_TWO)

    def __place_widgets(self):
        def create_add_chip_func(i):
            def add_chip_func():
                # success = \
                #     self.__game.get_board().add_chip(i, game.Game.PLAYER_ONE,
                #                                      self._canvas)
                success = self.__make_move(i)
                # Disable buttons
                # self.toggle_column_buttons(False)
                return success

            return add_chip_func

        # do yo thing
        def yo_things():
            # if self.__game.get_current_player() == game.Game.PLAYER_ONE:
            #     self.__game.set_current_player(game.Game.PLAYER_TWO)
            # else:
            #     self.__game.set_current_player(game.Game.PLAYER_ONE)
            self.__make_random_move()
            # self.toggle_column_buttons(True)

        for i in range(7):
            button = t.Button(self.__root)
            button.config(image=self.__column_button_images[i], width=94,
                          height=94)
            button.config(borderwidth=0)
            self.__column_buttons.append(button)
            button.config(command=create_add_chip_func(i))
            button.place(x=DELTA_WIDTH + CELL_PADDING +
                           (CELL_PADDING - 2) * i + DELTA_CELL * i + 2,
                         y=10)

        # self.__button = t.Button(self._parent, text="YO",
        #                          font=("Garamond", 20, "bold"),
        #                          command=lambda:
        #                          self.__communicator.send_message("YO"))
        self.__button = t.Button(self.__root, text="YO",
                                 font=("Garamond", 20, "bold"),
                                 command=yo_things)
        self.__win_button = t.Button(self.__root, text="win",
                                     command=self.show_win)
        self.__lose_button = t.Button(self.__root, text="lose",
                                      command=self.show_lose)

        # self.__button.pack()
        self.__button.place(x=0, y=60)
        self.__win_button.place(x=0, y=0)
        self.__lose_button.place(x=0, y=30)

    # TODO:: Combine these two
    def show_win(self):
        # TODO:: Change toggle so it can be used here as well
        self._canvas.delete(self.__your_label)
        self._canvas.delete(self.__enemy_label)
        self._canvas.create_image(600, 430,
                                  image=self.__labels_images["You Win"],
                                  anchor=CENTER_ANCHOR)

    def show_lose(self):
        self.disable_column_buttons()
        self._canvas.delete(self.__your_label)
        self._canvas.delete(self.__enemy_label)
        self._canvas.create_image(600, 430,
                                  image=self.__labels_images["You Lose"],
                                  anchor=CENTER_ANCHOR)

    def disable_column_buttons(self):
        for button in self.__column_buttons:
            button.config(state="disabled")

    def toggle_column_buttons(self, activate):
        if not activate:
            # Remove other label if it is still present
            self._canvas.delete(self.__your_label)
            self.disable_column_buttons()
            self.__enemy_label = \
                self._canvas.create_image(600, 430, image=self.__labels_images[
                    "Enemy Turn"], anchor=CENTER_ANCHOR)
            self.__root.after(1500,
                               lambda: self._canvas.delete(self.__enemy_label))
        else:
            # Remove other label if it is still present
            self._canvas.delete(self.__enemy_label)
            for button in self.__column_buttons:
                button.config(state="active")
            self.__your_label = \
                self._canvas.create_image(600, 430, image=self.__labels_images[
                    "Your Turn"], anchor=CENTER_ANCHOR)
            self.__root.after(1500,
                               lambda: self._canvas.delete(self.__your_label))
    #
    # def __handle_message(self, text=None):
    #     """
    #     Specifies the event handler for the message getting event in the
    #     communicator. Prints a message when invoked (and invoked by the
    #     communicator when a message is received). The message will
    #     automatically disappear after a fixed interval.
    #     :param text: the text to be printed.
    #     :return: None.
    #     """
    #     if text:
    #         self.__label["text"] = text
    #         self._parent.after(self.MESSAGE_DISPLAY_TIMEOUT,
    #                            self.__handle_message)
    #     else:
    #         self.__label["text"] = ""

    def __make_random_move(self):
        col = randint(0, 6)
        # while not self.__game.get_board().add_chip(col, game.Game.PLAYER_ONE,
        #                                            self.__game):
        while col >= 0:
            try:
                self.__make_move(col)
                col = -1
            except:
                col = randint(0, 6)

    def get_root(self):
        return self.__root

    def get_canvas(self):
        return self._canvas

    def create_chip_on_board(self, x, y, current_player):
        if current_player == self.__player:
            chip = self.red_piece
        else:
            chip = self.blue_piece

        self._canvas.create_image(x, y, image=chip,
                                  anchor=NW_ANCHOR)

    # TODO:: keeps disabling same buttons again and again because toggle
    # keeps enabling them
    def disable_illegal_button(self, col):
        self.__column_buttons[col].config(state="disabled")


class Game:
    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2
    EMPTY = 3

    def __init__(self):
        if len(argv) == 3:
            self.__current_player = self.PLAYER_ONE
            self.__player = self.PLAYER_ONE
            self.__enemy_player = self.PLAYER_TWO
        else:
            self.__current_player = self.PLAYER_TWO
            self.__player = self.PLAYER_TWO
            self.__enemy_player = self.PLAYER_ONE


        self.__gui = GUI(self.__player, self.__make_move)
        self.__board = Board(self.__gui.get_canvas(),
                             self.__gui.create_chip_on_board)
        self.__win_checker = WinSearch()

        self.__gui.get_root().mainloop()

    def __make_move(self, column):
        # if self.__current_player == 0:
        #     print("server side")
        # else:
        #     print("client side")

        if not self.__board.add_chip(column,
                                     self.PLAYER_ONE if not
                                     self.__current_player else self.PLAYER_TWO):
            raise Exception("Illegal move")

        winner = self.get_winner()
        if winner == self.__player:
            self.__gui.disable_column_buttons()
            self.__gui.show_win()
        elif winner == self.__enemy_player:
            self.__gui.disable_column_buttons()
            self.__gui.show_lose()
        elif winner is self.DRAW:
            self.__gui.disable_column_buttons()
            # self.__gui.show_draw()
        elif winner is None:
            self.__toggle_player()
            self.__disable_illegal_columns()

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
        board_columns = self.__board.get_columns_as_str()
        winner = self.__win_checker.get_winner_from_columns(board_columns)
        if winner is not None:
            return winner
        else:
            if self.check_draw():
                return self.DRAW

        return None


    def get_player_at(self, row, col):
        return self.__board.get_columns()[col][row]#.get_chip_owner()

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

    def eat_message(self):
        pass

    def get_root(self):
        return self.__gui.get_root()

class WinSearch:
    # Repurposed code from ex5

    EMPTY_STRING = ""

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
                               WIN_STATES)
        return int(winner) if winner is not None else None

    # def get_states(self, columns, ):