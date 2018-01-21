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
    FIRST_PLAYER_WIN_CHIP = "Images/white_chip_glow.png"
    SECOND_PLAYER_WIN_CHIP = "Images/black_chip_glow.png"
    YOUR_TURN = "Images/Your turn.gif"
    ENEMY_TURN = "Images/Enemy turn.gif"
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
        # TODO:: This is some ugly way of doing this
        self.__labels_images = \
            {"Your Turn": t.PhotoImage(file=self.YOUR_TURN),
             "Enemy Turn": t.PhotoImage(file=self.ENEMY_TURN),
             "You Win": t.PhotoImage(file=self.WIN_LABEL),
             "You Lose": t.PhotoImage(file=self.LOSE_LABEL),
             "Draw": t.PhotoImage(file=self.DRAW_LABEL)}

        self.white_piece = t.PhotoImage(file=self.OWN_PLAYER_CHIP)
        self.black_piece = t.PhotoImage(file=self.OTHER_PLAYER_CHIP)
        self.red_piece_glowing = t.PhotoImage(file=self.FIRST_PLAYER_WIN_CHIP)
        self.blue_piece_glowing = t.PhotoImage(
            file=self.SECOND_PLAYER_WIN_CHIP)

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
            if self.__ai_flag:
                button.config(state="disabled")

                # self.__button = t.Button(self._parent, text="YO",
                #                          font=("Garamond", 20, "bold"),
                #                          command=lambda:
                #                          self.__communicator.send_message("YO"))

                # TODO:: These next lines are for mockup, remove them afterwards
                # self.__button = t.Button(self.__root, text="rand move",
                #                          font=("Garamond", 12, "bold"),
                #                          command=yo_things)
                #
                # # self.__button.pack()
                # self.__button.place(x=0, y=00)

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
        if winning_player == self.__player:
            self._canvas.create_image(self.CANVAS_WIDTH / 2,
                                      self.CANVAS_HEIGHT / 2,
                                      image=self.__labels_images["You Win"],
                                      anchor=self.CENTER_ANCHOR)
        elif winning_player == game.Game.DRAW:
            self._canvas.create_image(self.CANVAS_WIDTH / 2,
                                      self.CANVAS_HEIGHT / 2,
                                      image=self.__labels_images["Draw"],
                                      anchor=self.CENTER_ANCHOR)
        elif winning_player != self.__player:
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
        if not self.__ai_flag:
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
                                  lambda: self._canvas.delete(
                                      self.__enemy_label))
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
                                  lambda: self._canvas.delete(
                                      self.__your_label))

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
                chip = self.white_piece
            else:
                chip = self.black_piece

        if not win:  # Create chip and animate it falling
            id = self._canvas.create_image(x, 10 + self.DELTA_CELL, image=chip,
                                           anchor=self.NW_ANCHOR)
            # can change 10 to 10  + DELTA_CELL to start IN THE BOARD
            # instead of atop it

            animate = self.__get_animation_func(id, y, self.STARTING_SPEED,
                                                winning_chips, board, winner)
            animate(0)
        else:  # Set chips to glowing ones
            self._canvas.create_image(x, y, image=chip,
                                      anchor=self.NW_ANCHOR)

    def __get_animation_func(self, obj_id, final_y, vel, winning_chips,
                             board, winner):
        def animate_fall(time_elapsed):
            # self._canvas.move(obj_id, 0,
            #                   vel + acceleration ** 2 /
            #                   self.ACCEL_NORMALIZATION)
            self._canvas.move(obj_id, 0,
                              vel * time_elapsed +
                              self.ACCELERATION * time_elapsed ** 2)
            x0, y0 = self._canvas.coords(obj_id)
            if y0 >= final_y:
                self._canvas.coords(obj_id, x0, final_y)
                self.lock_buttons_for_animation(False)
                if winning_chips is not None:
                    on_win_condition(winning_chips, winner)
            else:
                time_elapsed += self.ANIMATION_REFRESH * \
                                self.ACCEL_NORMALIZATION
                self._canvas.after(self.ANIMATION_REFRESH, animate_fall,
                                   time_elapsed)

        def on_win_condition(winning_chips, winner):
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

        self.lock_buttons_for_animation(True)
        return animate_fall

    def lock_buttons_for_animation(self, flag):
        if flag:
            self.lock = True
            self.disable_column_buttons(False)
            # self.__button.config(state="disabled")
            return
        elif self.__get_current_player == self.__player:
            self.disable_column_buttons(True)
        self.lock = False
        # self.__button.config(state="active")

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
