from board import *
from communicator import *
from sys import argv
from GUI import GUI
from ai import AI


class Game:
    """
        Game class, handles gamplay, gui and communicator
    """
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
        """ Initializes the game class """
        # If server mode is on (no IP address provided)
        if len(argv) == 3:
            self.__player = self.PLAYER_ONE
            self.__enemy_player = self.PLAYER_TWO
            self.__current_player = self.__player
        else:
            self.__player = self.PLAYER_TWO
            self.__enemy_player = self.PLAYER_ONE
            self.__current_player = self.__enemy_player

        self.__ai_flag = False
        if argv[1] == "ai":
            self.__ai = AI()
            self.__ai_flag = True

        # Create gui
        self.__gui = GUI(self.__player, self.__make_move,
                         self.get_current_player, self.__ai_flag)

        # If this is the client, disable buttons until player turn
        if self.__player == self.PLAYER_TWO:
            self.__gui.disable_column_buttons()

        # Create board
        self.__board = Board(self.get_current_player)
        self.__game_over = False

        # TODO:: Ugly code, find a workaround
        self.__last_inserted_chip = None

        # Parse data for communicator
        port = int(argv[2])
        ip = None

        if len(argv) == 4:
            ip = argv[3]

        self.__communicator = Communicator(self.__gui.get_root(), port, ip)
        self.__communicator.connect()
        self.__communicator.bind_action_to_message(self.parse_message_from_enemy)

        # If AI and server start the game
        if self.__ai_flag and self.__player == 0:
            self.__ai.find_legal_move(self, self.__make_move)

        # Start the gui and game
        self.__gui.get_root().mainloop()

    def __make_move(self, column):
        """ :param column: Column in whivh to place chip """

        # if game over flag on, returns
        if self.__game_over:
            return

        # attempts to place chip in column
        success, row = self.__board.check_legal_move_get_row(column,
                                                             self.PLAYER_ONE if not
                                                   self.__current_player else
                                                   self.PLAYER_TWO)
        if not success:
            raise Exception(self.ILLEGAL_MOVE)

        # Store move for other functions
        self.__last_inserted_chip = column, row

        # Relay move to enemy
        self.__communicator.send_message(self.COMMUNICATOR_MESSAGE_1
                                         + str(column) + "," + str(row)
                                         + " " + self.COMMUNICATOR_MESSAGE_2
                                         + "1" if not self.__game_over else
                                         "0")

        self.__check_winner(column, row)

    def __check_winner(self, column, row):
        """ :param column: Column of newest chip
            :param row: Row of newest chip """

        # Get data if a winning state was reached
        winner, winning_chips = self.__board.find_connected_and_winner(column,
                                                                       row)

        # Get pixel location for newest chip
        x, y = self.__board.get_chip_location(column, row)
        if winner is None:  # If game is still ongoing
            # Create the chip on board
            self.__gui.create_chip_on_board(x, y, self.__current_player,
                                            board=self.__board)

            # Toggle player in class members
            self.__toggle_player()

            # Disable full columns
            self.__gui.disable_illegal_columns(self.__board)

        else:  # Game ended
            self.__game_over = True
            if winner == self.DRAW:
                self.__gui.create_chip_on_board(x, y, self.__current_player,
                                                board=self.__board)
                self.__gui.disable_column_buttons()
                self.__gui.show_game_over_label(self.DRAW)
            else:
                self.__gui.create_chip_on_board(x, y, self.__current_player,
                                                winning_chips=winning_chips,
                                                board=self.__board,
                                                winner=winner)

    # def __disable_illegal_columns(self):
    #     """ Check full columns and disable their buttons """
    #     columns = self.__board.get_columns()
    #     for i in range(len(columns)):
    #         illegal_column = True
    #         for cell in columns[i]:
    #             if cell == self.EMPTY:
    #                 # Will reach here if column is not full
    #                 illegal_column = False
    #                 break
    #         if illegal_column:
    #             self.__gui.disable_illegal_button(i)

    def __toggle_player(self):
        """ Toggles members in the class, also make gui show switching of
            turns """
        self.__current_player = self.PLAYER_TWO \
            if self.__current_player == self.PLAYER_ONE \
            else self.PLAYER_ONE

        flag = self.__current_player == self.__player

        self.__gui.end_turn_switch_player(flag)

    def get_winner(self):
        """ Gets the winner if there is one.
            This function is not used by the game """
        return self.__board.find_connected_and_winner(
            self.__last_inserted_chip[0], self.__last_inserted_chip[1])[0]

    def get_player_at(self, row, col):
        """ :param row: Row to check
            :param col: Column to check
            :return: Player at place
        """
        player = int(self.__board.get_columns()[col][row])
        return None if player == self.EMPTY else player

    def get_current_player(self):
        """ Getter for current player """
        return self.__current_player

    def get_board(self):
        """ Getter for board """
        return self.__board

    def set_current_player(self, player):
        """ Setter for current player """
        self.__current_player = player

    def set_player(self, player):
        """ Setter for player """
        self.__player = player

    def get_player(self):
        """ Getter for player """
        return self.__player

    def set_gui(self, gui):
        """ Setter for gui """
        self.__gui = gui

    def parse_message_from_enemy(self, message):
        """ :param message: Message received from enemy """
        if len(message) != 30:  # Check message of corect length
            raise Exception(self.INVALID_MESSAGE)

        # Parse data from message
        column = int(message[11])
        expected_row = int(message[13])

        # Update board and check if same row was returned
        success, row = self.__board.check_legal_move_get_row(column,
                                                             self.PLAYER_ONE
            if not self.__current_player else self.PLAYER_TWO)

        # Assert it
        assert row == expected_row

        if success:
            # Update member
            self.__last_inserted_chip = column, row
            check_winner_flag = message[self.CHECK_WINNER_FLAG_INDEX]
            if check_winner_flag:
                self.__check_winner(column, row)

        else:
            raise Exception(self.ADD_CHIP_FAILED)

        self.__gui.disable_illegal_columns(self.__board)

        # If the AI is playing, make another move
        if self.__ai_flag and not self.__game_over:
            self.__ai.find_legal_move(self, self.__make_move)

    def get_root(self):
        """ Getter for root """
        return self.__gui.get_root()

    def get_last_inserted_chip(self):
        """ Getter for last inserted chip """
        return self.__last_inserted_chip
