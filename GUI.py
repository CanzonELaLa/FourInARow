import tkinter as t
import game
from random import randint


class GUI:
    """
    Designed to handle the GUI aspects (creating a window, buttons and
    pop-ups. Also initializes the communicator object.
    """

    # Animation constants
    ANIMATION_REFRESH = 41
    ACCEL_NORMALIZATION = 0.025
    ACCELERATION = 9
    STARTING_SPEED = 0
    BLINK_TIMER = 500

    # Positioning constants
    DELTA_HEIGHT = 130
    DELTA_WIDTH = 180
    DELTA_CELL = 109
    CELL_PADDING = 13
    CENTER_ANCHOR = "center"
    NW_ANCHOR = "nw"

    # Main gui constants
    COLUMN_BUTTON_SIZE = 92
    CANVAS_HEIGHT = 860
    CANVAS_WIDTH = 1200
    LABEL_LIFE_TIME_MS = 1500

    # File constants
    OWN_PLAYER_CHIP = "Images/white_chip.png"
    OTHER_PLAYER_CHIP = "Images/black_chip.png"
    OWN_PLAYER_WIN_CHIP = "Images/white_chip_glow.png"
    OTHER_PLAYER_WIN_CHIP = "Images/black_chip_glow.png"
    YOUR_TURN = "Images/Your turn.png"
    ENEMY_TURN = "Images/Enemy turn.png"
    BG_IMAGE = "Images/bg2.png"
    WIN_LABEL = "Images/You win.png"
    LOSE_LABEL = "Images/You lose.png"
    DRAW_LABEL = "Images/Draw.png"

    def __init__(self, player, make_move, get_current_player, ai):
        """ Initialized the GUI
            :param player: 0 or 1 depending on client/server
            :param make_move: func that makes a move on the board
            :param get_current_player: Func that gets the current player of
                                       the Game.
            :param ai: Whether or not the player is ai
        """
        self.__ai_flag = ai

        # Create the Tk and canvas, set the background image
        self.__root = t.Tk()
        self.__root.resizable(width=False, height=False)
        self._canvas = t.Canvas(self.__root, width=self.CANVAS_WIDTH,
                                height=self.CANVAS_HEIGHT)
        self._canvas.pack()
        self.__bg = t.PhotoImage(file=self.BG_IMAGE)
        self._canvas.create_image(0, 0, image=self.__bg, anchor="nw")
        self.__player = player
        self.__make_move = make_move
        self.__get_current_player = get_current_player

        # Create UI buttons and labels
        self.__column_buttons = []
        self.__column_button_images = [t.PhotoImage(
            file="Images/button_images/button" + str(x) + ".png")
            for x in range(1, 8)]

        self.__labels_images = \
            {"Your Turn": t.PhotoImage(file=self.YOUR_TURN),
             "Enemy Turn": t.PhotoImage(file=self.ENEMY_TURN),
             "You Win": t.PhotoImage(file=self.WIN_LABEL),
             "You Lose": t.PhotoImage(file=self.LOSE_LABEL),
             "Draw": t.PhotoImage(file=self.DRAW_LABEL)}

        self.white_piece = t.PhotoImage(file=self.OWN_PLAYER_CHIP)
        self.black_piece = t.PhotoImage(file=self.OTHER_PLAYER_CHIP)
        self.white_piece_glowing = t.PhotoImage(file=self.OWN_PLAYER_WIN_CHIP)
        self.black_piece_glowing = t.PhotoImage(
            file=self.OTHER_PLAYER_WIN_CHIP)

        # TODO:: Refactor to dictionary
        self.__your_label = None
        self.__enemy_label = None
        self.__place_widgets()
        self.lock = False

    def __place_widgets(self):
        """
        Placed buttons and labels on board
        """

        def create_add_chip_func(j):
            """ :param j: Column number
                :return: Function to call make_move with number stored in
                         memory
            """
            return lambda: self.__make_move(j)

        # Create the 7 buttons
        for i in range(7):
            button = t.Button(self.__root)
            button.config(image=self.__column_button_images[i],
                          width=self.COLUMN_BUTTON_SIZE,
                          height=self.COLUMN_BUTTON_SIZE,
                          borderwidth=0, relief="raised",
                          command=create_add_chip_func(i))
            button.place(x=self.DELTA_WIDTH + self.CELL_PADDING +
                           (self.CELL_PADDING - 2) * i + self.DELTA_CELL * i,
                         y=10)
            self.__column_buttons.append(button)
            if self.__ai_flag:  # If the AI is playing, disable the buttons
                button.config(state="disabled")

    def show_game_over_label(self, winning_player):
        """  :param winning_player: Player identifying int """
        # TODO:: Change toggle so it can be used here as well

        # Disable the buttons and delete turn labels
        self.disable_column_buttons()
        self._canvas.delete(self.__your_label)
        self._canvas.delete(self.__enemy_label)

        # Decide which label to show and show it
        image = None
        if winning_player == self.__player:
            image = self.__labels_images["You Win"]
        elif winning_player == game.Game.DRAW:
            image = self.__labels_images["Draw"]
        elif winning_player != self.__player:
            image = self.__labels_images["You Lose"]

        self._canvas.create_image(self.CANVAS_WIDTH / 2, -20, anchor="n",
                                  image=image)

    def disable_column_buttons(self, enable=False):
        """ :param enable: Enable/Disable the buttons """
        for button in self.__column_buttons:
            if button is not None:  # Check if button is still there
                if enable:
                    button.config(state="active")
                else:
                    button.config(state="disabled")

    def end_turn_switch_player(self, own_turn):
        """ :param own_turn: Whether or not this is the player's turn """
        if not own_turn:  # If own turn ended
            # Remove other label if it is still present
            self._canvas.delete(self.__your_label)

            # Toggle the buttons
            self.disable_column_buttons()

            # Create label
            self.__enemy_label = \
                self._canvas.create_image(self.CANVAS_WIDTH / 2,
                                          self.CANVAS_HEIGHT / 2,
                                          image=self.__labels_images[
                                              "Enemy Turn"],
                                          anchor=self.CENTER_ANCHOR)

            # Set destroy time for label
            self.__root.after(self.LABEL_LIFE_TIME_MS,
                              lambda: self._canvas.delete(
                                  self.__enemy_label))
        else:  # If own turn starts
            # Remove other label if it is still present
            self._canvas.delete(self.__enemy_label)

            # Toggle the buttons
            if not self.__ai_flag:  # Don't enable if AI is playing
                self.disable_column_buttons(True)

            # Create label
            self.__your_label = \
                self._canvas.create_image(self.CANVAS_WIDTH / 2,
                                          self.CANVAS_HEIGHT / 2,
                                          image=self.__labels_images[
                                              "Your Turn"],
                                          anchor=self.CENTER_ANCHOR)

            # Set destroy time for label
            self.__root.after(self.LABEL_LIFE_TIME_MS,
                              lambda: self._canvas.delete(
                                  self.__your_label))

    # TODO:: Fallback ai in case of w.c.s.
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
        """ Getter for root """
        return self.__root

    def get_canvas(self):
        """ Getter for canvas """
        return self._canvas

    def create_chip_on_board(self, x, y, current_player, win=False,
                             winning_chips=None, board=None, winner=None):
        """ :param x: Width pixel location
            :param y: Height pixel location
            :param current_player: Chip's owner
            :param win: Whether or not this is for a win/lose condition
                        (disable animation)
            :param winning_chips: List of winning chips to switch to glowing
            :param board: Board reference for location references later on
            :param winner: Winner of game """
        if win:  # Win condition
            if current_player == self.__player:
                chip = self.white_piece_glowing
            else:
                chip = self.black_piece_glowing
        else:  # Still playing
            if current_player == self.__player:
                chip = self.white_piece
            else:
                chip = self.black_piece

        if not win:  # Create chip and animate it falling
            chip_widget = self._canvas.create_image(x, 10 + self.DELTA_CELL,
                                                    image=chip,
                                                    anchor=self.NW_ANCHOR)
            # can change 10 to 10  + DELTA_CELL to start IN THE BOARD
            # instead of atop it

            # Animate the chip falling
            self.__get_animation_func(chip_widget, y,
                                      self.STARTING_SPEED,
                                      winning_chips, board, winner)(0)

        else:  # Set chips to glowing ones, no animation
            return self._canvas.create_image(x, y, image=chip,
                                             anchor=self.NW_ANCHOR)

    def __get_animation_func(self, obj_id, final_y, vel, winning_chips,
                             board, winner):
        """ Creates an animation function with stored data
            :param obj_id: What widget to animate
            :param final_y: Final height
            :param vel: Starting velocity
            :param winning_chips: Chips to animate if any are needed
            :param board: Board for references later on
            :param winner: Winner to pass on
            :return: Animation function """

        def animate_fall(time_elapsed):
            """ Recursive function for animation
                :param time_elapsed: Time since start animation """

            # Move the obj down by realistic amount given time elapsed
            self._canvas.move(obj_id, 0,
                              vel * time_elapsed +
                              self.ACCELERATION * time_elapsed ** 2)

            # Get current position of obj
            x0, y0 = self._canvas.coords(obj_id)
            if y0 >= final_y:  # If final place has been reached
                # Set the final location
                self._canvas.coords(obj_id, x0, final_y)

                # Unlock buttons
                self.lock_buttons_for_animation(False)

                # Lock illegal buttons
                if board is not None:
                    self.disable_illegal_columns(board)

                # If this is a winning move, make proper chips glow and show
                # label
                if winning_chips is not None:
                    on_win_condition(winning_chips, winner)
            else:  # Continue animation
                time_elapsed += self.ANIMATION_REFRESH * \
                                self.ACCEL_NORMALIZATION
                self._canvas.after(self.ANIMATION_REFRESH, animate_fall,
                                   time_elapsed)

        def on_win_condition(winning_chips, winner):
            """ :param winning_chips: Winning chips to make glow
                :param winner: Who won the game """
            # Show winner label
            self.show_game_over_label(winner)

            # Color all relevant chips
            self.color_winning_chips(winner,
                                     winning_chips, board)

            # Destroy all remaining buttons
            for button in self.__column_buttons:
                if button is not None:
                    button.destroy()

        # Lock buttons for animation
        self.lock_buttons_for_animation(True)
        return animate_fall

    def lock_buttons_for_animation(self, flag):
        """ :param flag: Lock or unlock """
        if flag:
            self.lock = True
            self.disable_column_buttons()
            return
        elif self.__get_current_player() == self.__player and not \
                self.__ai_flag:
            self.disable_column_buttons(enable=True)
        self.lock = False

    def disable_illegal_columns(self, board):
        """ Check full columns and disable their buttons """
        columns = board.get_columns()
        for i in range(len(columns)):
            illegal_column = True
            for cell in columns[i]:
                if cell == game.Game.EMPTY:
                    # Will reach here if column is not full
                    illegal_column = False
                    break
            if illegal_column:
                self.disable_illegal_button(i)

    # TODO:: keeps disabling same buttons again and again because toggle
    # keeps enabling them
    def disable_illegal_button(self, col):
        """ :param col: Button column to disable """
        button = self.__column_buttons[col]
        # Destroy the button as it is not needed anymore
        if button is not None:
            button.destroy()
            # Since we are iterating over this list, I must keep it at the
            # same length, thus inserting None instead of destroyed button
            self.__column_buttons[col] = None

    def color_winning_chips(self, player, chips, board):
        """ :param player: Winning player
            :param chips: List of chips to make glow
            :param board: Board reference """
        chip_widgets = []
        for x, y in chips:
            cell = board.get_cell_at(x, y)
            chip_widgets.append(
                self.create_chip_on_board(cell.get_location()[0],
                                          cell.get_location()[1], player,
                                          True))

        def get_animate(chip):
            """ Gets blinking animation for chips
                :param chip: List of chip ids
                :return: func of blinking """

            def animate_up():
                """ Raises chip to top """
                self._canvas.lift(chip)
                self._canvas.after(200, animate_down)

            def animate_down():
                """ Lowers chip to bottom """
                self._canvas.lower(chip)
                self._canvas.after(self.BLINK_TIMER, animate_up)

            return animate_down

        def blink(chips_widgets):
            """ Start blinking animation """
            for chip in chips_widgets:
                self._canvas.after(self.BLINK_TIMER, get_animate(chip))

        blink(chip_widgets)
