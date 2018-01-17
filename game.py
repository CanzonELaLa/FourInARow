from board import *
from sys import argv
from random import randint
from time import sleep









# WIN_LABEL = "Images/You win.gif"
# LOSE_LABEL = "Images/You lose.gif"
# DRAW_LABEL = "Images/Draw.gif"
# BG_IMAGE = "Images/bg.gif"
# FIRST_PLAYER_CHIP = "Images/Red.gif"
# SECOND_PLAYER_CHIP = "Images/Blue.gif"
# FIRST_PLAYER_WIN_CHIP = "Images/Red_glow.gif"
# SECOND_PLAYER_WIN_CHIP = "Images/Blue_glow.gif"


class GUI:
    """
    Designed to handle the GUI aspects (creating a window, buttons and
    pop-ups. Also initializes the communicator object.
    """

    ANIMATION_REFRESH = 20

    DELTA_HEIGHT = 130
    DELTA_WIDTH = 180
    DELTA_CELL = 109
    CELL_PADDING = 13

    COLUMN_BUTTON_SIZE = 92
    CANVAS_HEIGHT = 860
    CANVAS_WIDTH = 1200
    LABEL_LIFE_TIME_MS = 1500
    ACCEL_NORMALIZATION = 2

    FIRST_PLAYER_CHIP = "Images/white_chip.png"
    SECOND_PLAYER_CHIP = "Images/black_chip.png"
    FIRST_PLAYER_WIN_CHIP = "Images/white_chip_glow.png"
    SECOND_PLAYER_WIN_CHIP = "Images/black_chip_glow.png"
    YOUR_TURN = "Images/Your turn.gif"
    ENEMY_TURN = "Images/Enemy turn.gif"
    BG_IMAGE = "Images/bg.png"
    WIN_LABEL = "Images/You win.png"
    LOSE_LABEL = "Images/You lose.png"
    DRAW_LABEL = "Images/Draw.png"

    CENTER_ANCHOR = "center"
    NW_ANCHOR = "nw"

    MESSAGE_DISPLAY_TIMEOUT = 250

    def __init__(self, player, make_move, get_current_player, get_player):
        """
        Initializes the GUI and connects the communicator.
        :param parent: the tkinter root.
        """
        self.__root = t.Tk()
        self.__root.resizable(width=False, height=False)
        self._canvas = t.Canvas(self.__root, width=self.CANVAS_WIDTH,
                                height=self.CANVAS_HEIGHT)
        self._canvas.pack()
        self.__bg = t.PhotoImage(file=self.BG_IMAGE)
        self._canvas.create_image(0, 0, image=self.__bg, anchor="nw")
        self.__player = player
        self.__make_move = make_move
        self.__get_player = get_player
        self.__get_current_player = get_current_player

        # UI things
        self.__column_buttons = []
        self.__column_button_images = [t.PhotoImage(
            file="Images/button_images/button" + str(x) + ".png")
                                       for x in range(1, 8)]
        # TODO:: This is some ugly way of doing this
        self.__labels_images = {}
        self.__labels_images["Your Turn"] = t.PhotoImage(file=self.YOUR_TURN)
        self.__labels_images["Enemy Turn"] = t.PhotoImage(file=self.ENEMY_TURN)
        self.__labels_images["You Win"] = t.PhotoImage(file=self.WIN_LABEL)
        self.__labels_images["You Lose"] = t.PhotoImage(file=self.LOSE_LABEL)
        self.__labels_images["Draw"] = t.PhotoImage(file=self.DRAW_LABEL)

        self.red_piece = t.PhotoImage(file=self.FIRST_PLAYER_CHIP)
        self.blue_piece = t.PhotoImage(file=self.SECOND_PLAYER_CHIP)
        self.red_piece_glowing = t.PhotoImage(file=self.FIRST_PLAYER_WIN_CHIP)
        self.blue_piece_glowing = t.PhotoImage(file=self.SECOND_PLAYER_WIN_CHIP)

        # TODO:: Refactor to dictionary
        self.__your_label = None
        self.__enemy_label = None
        self.__place_widgets()
        self.lock = False
        # self.__game = Game()
        # self.__game.set_canvas(self._canvas)
        # self.__game.set_gui(self)
        # if len(argv) == 4:
        #     self.__game.set_current_player(self.__game.PLAYER_TWO)
        #     self.__game.set_player(self.__game.PLAYER_TWO)

    def __place_widgets(self):
        def create_add_chip_func(j):
            def add_chip_func():
                # success = \
                #     self.__game.get_board().add_chip(i, game.Game.PLAYER_ONE,
                #                                      self._canvas)
                success = self.__make_move(j)
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
            button.config(image=self.__column_button_images[i],
                          width=self.COLUMN_BUTTON_SIZE,
                          height=self.COLUMN_BUTTON_SIZE)
            button.config(borderwidth=0)
            button.config(relief="raised")
            self.__column_buttons.append(button)
            button.config(command=create_add_chip_func(i))
            button.place(x=self.DELTA_WIDTH + self.CELL_PADDING +
                           (self.CELL_PADDING - 2) * i + self.DELTA_CELL * i,
                         y=10)

        # self.__button = t.Button(self._parent, text="YO",
        #                          font=("Garamond", 20, "bold"),
        #                          command=lambda:
        #                          self.__communicator.send_message("YO"))

        # TODO:: These next lines are for mockup, remove them afterwards
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

    # TODO:: START REMOVE
    def show_win(self):
        self._canvas.delete(self.__your_label)
        self._canvas.delete(self.__enemy_label)
        self._canvas.create_image(self.CANVAS_WIDTH / 2,
                                  self.CANVAS_HEIGHT / 2,
                                  image=self.__labels_images["You Win"],
                                  anchor=self.CENTER_ANCHOR)

    def show_lose(self):
        self.disable_column_buttons()
        self._canvas.delete(self.__your_label)
        self._canvas.delete(self.__enemy_label)
        self._canvas.create_image(self.CANVAS_WIDTH / 2,
                                  self.CANVAS_HEIGHT / 2,
                                  image=self.__labels_images["You Lose"],
                                  anchor=self.CENTER_ANCHOR)

    def show_draw(self):
        self.disable_column_buttons()
        self._canvas.delete(self.__your_label)
        self._canvas.delete(self.__enemy_label)
        self._canvas.create_image(self.CANVAS_WIDTH / 2,
                                  self.CANVAS_HEIGHT / 2,
                                  image=self.__labels_images["Draw"],
                                  anchor=self.CENTER_ANCHOR)
    # TODO:: END REMOVE

    def show_game_over_label(self, winning_player):
        # TODO:: Change toggle so it can be used here as well
        self.disable_column_buttons()
        self._canvas.delete(self.__your_label)
        self._canvas.delete(self.__enemy_label)
        if winning_player == self.__get_player():
            self._canvas.create_image(self.CANVAS_WIDTH / 2,
                                      self.CANVAS_HEIGHT / 2,
                                      image=self.__labels_images["You Win"],
                                      anchor=self.CENTER_ANCHOR)
        elif winning_player == Game.DRAW:
            self._canvas.create_image(self.CANVAS_WIDTH / 2,
                                      self.CANVAS_HEIGHT / 2,
                                      image=self.__labels_images["Draw"],
                                      anchor=self.CENTER_ANCHOR)
        elif winning_player != self.__get_player():
            self._canvas.create_image(self.CANVAS_WIDTH / 2,
                                      self.CANVAS_HEIGHT / 2,
                                      image=self.__labels_images["You Lose"],
                                      anchor=self.CENTER_ANCHOR)

    def disable_column_buttons(self, enable=False):
        for button in self.__column_buttons:
            if enable:
                button.config(state="active")
            else:
                button.config(state="disabled")

    def toggle_column_buttons(self, activate):
        if not activate:
            # Remove other label if it is still present
            self._canvas.delete(self.__your_label)
            self.disable_column_buttons()
            self.__enemy_label = \
                self._canvas.create_image(self.CANVAS_WIDTH / 2,
                                          self.CANVAS_HEIGHT / 2,
                                          image=self.__labels_images[
                                              "Enemy Turn"],
                                          anchor=self.CENTER_ANCHOR)
            self.__root.after(self.LABEL_LIFE_TIME_MS,
                              lambda: self._canvas.delete(self.__enemy_label))
        else:
            # Remove other label if it is still present
            self._canvas.delete(self.__enemy_label)
            for button in self.__column_buttons:
                button.config(state="active")
            self.__your_label = \
                self._canvas.create_image(self.CANVAS_WIDTH / 2,
                                          self.CANVAS_HEIGHT / 2,
                                          image=self.__labels_images[
                                              "Your Turn"],
                                          anchor=self.CENTER_ANCHOR)
            self.__root.after(self.LABEL_LIFE_TIME_MS,
                              lambda: self._canvas.delete(self.__your_label))

    # TODO:: This is a mockup function
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

    def create_chip_on_board(self, x, y, current_player, win=False,
                             winning_chips=None, board=None, winner=None):
        if win:
            if current_player == self.__player:
                chip = self.red_piece_glowing
            else:
                chip = self.blue_piece_glowing
        else:
            if current_player == self.__player:
                chip = self.red_piece
            else:
                chip = self.blue_piece

        # self._canvas.create_image(x, y, image=chip,
        #                           anchor=NW_ANCHOR)
        if not win:  # Create chip and animate it falling
            id = self._canvas.create_image(x, 10, image=chip,
                                           anchor=self.NW_ANCHOR)
            # can change 10 to 10  + DELTA_CELL to start IN THE BOARD
            # instead of atop it

            animate = self.__get_animation_func(id, y, 10, winning_chips,
                                                board, winner)
            animate(1)
        else:  # Set chips to glowing ones
            self._canvas.create_image(x, y, image=chip,
                                      anchor=self.NW_ANCHOR)

    def __get_animation_func(self, obj_id, final_y, vel, winning_chips,
                             board, winner):
        self.lock_buttons_for_animation(True)

        def animate_fall(acceleration):
            self._canvas.move(obj_id, 0,
                              vel + acceleration ** 2 /
                              self.ACCEL_NORMALIZATION)
            x0, y0 = self._canvas.coords(obj_id)
            if y0 >= final_y:
                self._canvas.coords(obj_id, x0, final_y)
                self.lock_buttons_for_animation(False)
                if winning_chips is not None:
                    self.color_winning_chips(self.__get_current_player(),
                                             winning_chips, board)
                    if winner == self.__player:
                        self.disable_column_buttons()
                        # self.show_win()
                        self.show_game_over_label(winner)
                    else:
                        self.disable_column_buttons()
                        # self.show_lose()
                        self.show_game_over_label(winner)
            else:
                self._canvas.after(self.ANIMATION_REFRESH, animate_fall,
                                   acceleration + 1)

        return animate_fall

    def lock_buttons_for_animation(self, flag):
        if flag:
            self.lock = True
            self.disable_column_buttons(False)
            self.__button.config(state="disabled")
            return
        elif self.__get_current_player == self.__get_player():
            self.disable_column_buttons(True)
        self.lock = False
        self.__button.config(state="active")

    # TODO:: keeps disabling same buttons again and again because toggle
    # keeps enabling them
    def disable_illegal_button(self, col):
        self.__column_buttons[col].config(state="disabled")

    def color_winning_chips(self, player, chips, board):
        # TODO:: Make it so that the coloring happens only after animation end.
        for x, y in chips:
            cell = board.get_cell_at(x, y)
            self.create_chip_on_board(cell.get_location()[0],
                                      cell.get_location()[1], player, True)


class Game:
    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2
    EMPTY = 3

    LENGTH_OF_WINNING_SEQ = 4

    ILLEGAL_MOVE = "Illegal move"

    def __init__(self):
        if len(argv) == 3:
            self.__current_player = self.PLAYER_ONE
            self.__player = self.PLAYER_ONE
            self.__enemy_player = self.PLAYER_TWO
        else:
            self.__current_player = self.PLAYER_TWO
            self.__player = self.PLAYER_TWO
            self.__enemy_player = self.PLAYER_ONE

        self.__gui = GUI(self.__player, self.__make_move,
                         self.get_current_player, self.get_player)
        self.__board = Board(self.__gui.get_canvas(),
                             self.__gui.create_chip_on_board)
        self.__win_checker = WinSearch()
        self.__game_over = False

        # TODO:: Ugly code, find a workaround
        self.__last_inserted_chip = None

        self.__gui.get_root().mainloop()

    def __make_move(self, column):
        success, row = self.__board.check_add_chip(column,
                                                   self.PLAYER_ONE if not
                                                   self.__current_player else
                                                   self.PLAYER_TWO)
        if not success:
            raise Exception(self.ILLEGAL_MOVE)

        self.__last_inserted_chip = column, row

        winner, winning_chips = self.__find_connected_and_winner(column, row)
        x, y = self.__board.get_chip_location(column, row)

        if winner is None:
            self.__gui.create_chip_on_board(x, y, self.__current_player)
            self.__toggle_player()
            self.__disable_illegal_columns()
        elif winner == self.DRAW:
            self.__gui.create_chip_on_board(x, y, self.__current_player)
            self.__game_over = True
            self.__gui.disable_column_buttons()
            # self.__gui.show_draw()
            # self.__gui.show_game_over_label(self.DRAW)
        else:
            self.__game_over = True
            self.__gui.create_chip_on_board(x, y, self.__current_player,
                                            winning_chips=winning_chips,
                                            board=self.__board, winner=winner)
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
        for j in range(row, min(row + self.LENGTH_OF_WINNING_SEQ,
                                len(columns[column]))):
            if columns[column][j] == self.__current_player:
                lst.append((column, j))

        if len(lst) == self.LENGTH_OF_WINNING_SEQ:
            return self.__current_player, lst

        # Check row
        rows = self.__win_checker.transpose_matrix(self.__board.get_columns())

        for j in range(len(rows[row]) - 3):
            flag = True
            for i in range(self.LENGTH_OF_WINNING_SEQ):
                if rows[row][j + i] != self.__current_player:
                    flag = False
                    break

            if flag:
                return self.__current_player, [(k, row) for k in
                                               range(j, j +
                                                     self.LENGTH_OF_WINNING_SEQ
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

                if len(lst) == self.LENGTH_OF_WINNING_SEQ:
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

                if len(lst) == self.LENGTH_OF_WINNING_SEQ:
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

    def eat_message(self):
        pass

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
