import socket
import tkinter as t

# TODO:: REMOVE
from random import randint

from communicator import Communicator
from game import Game
from board import *

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


class GUI:
    """
    Designed to handle the GUI aspects (creating a window, buttons and
    pop-ups. Also initializes the communicator object.
    """

    MESSAGE_DISPLAY_TIMEOUT = 250

    def __init__(self, parent, port, ip=None):
        """
        Initializes the GUI and connects the communicator.
        :param parent: the tkinter root.
        :param ip: the ip to connect to.
        :param port: the port to connect to.
        :param server: true if the communicator is a server, otherwise false.
        """
        self._parent = parent
        self._canvas = t.Canvas(self._parent, width=1200, height=860)
        self._canvas.pack()
        self.__bg = t.PhotoImage(file=BG_IMAGE)
        self._canvas.create_image(0, 0, image=self.__bg, anchor="nw")

        # Comuunicator class things
        self.__communicator = Communicator(parent, port, ip)
        self.__communicator.connect()
        self.__communicator.bind_action_to_message(self.__handle_message)

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
        # TODO:: Refactor to dictionary
        self.__your_label = None
        self.__enemy_label = None
        self.__place_widgets()
        self.__game = Game()
        self.__game.set_canvas(self._canvas)
        if ip is not None:
            self.__game.set_current_player(self.__game.PLAYER_TWO)
            self.__game.set_player(self.__game.PLAYER_TWO)

    def __place_widgets(self):
        def create_add_chip_func(i):
            def add_chip_func():
                # success = \
                #     self.__game.get_board().add_chip(i, game.Game.PLAYER_ONE,
                #                                      self._canvas)
                success = self.__game.make_move(i)
                # Disable buttons
                self.toggle_column_buttons(False)
                return success

            return add_chip_func

        # do yo thing
        def yo_things():
            # if self.__game.get_current_player() == game.Game.PLAYER_ONE:
            #     self.__game.set_current_player(game.Game.PLAYER_TWO)
            # else:
            #     self.__game.set_current_player(game.Game.PLAYER_ONE)
            self.__make_random_move()
            self.toggle_column_buttons(True)

        for i in range(7):
            button = t.Button(self._parent)
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
        self.__button = t.Button(self._parent, text="YO",
                                 font=("Garamond", 20, "bold"),
                                 command=yo_things)
        self.__win_button = t.Button(self._parent, text="win",
                                     command=self.show_win)
        self.__lose_button = t.Button(self._parent, text="lose",
                                      command=self.show_lose)

        # self.__button.pack()
        self.__button.place(x=0, y=60)
        self.__win_button.place(x=0, y=0)
        self.__lose_button.place(x=0, y=30)

    # TODO:: Combine these two
    def show_win(self):
        # TODO:: Change toggle so it can be used here as well
        for button in self.__column_buttons:
            button.config(state="disabled")
        self._canvas.delete(self.__your_label)
        self._canvas.delete(self.__enemy_label)
        self._canvas.create_image(600, 430,
                                  image=self.__labels_images["You Win"],
                                  anchor=CENTER_ANCHOR)

    def show_lose(self):
        for button in self.__column_buttons:
            button.config(state="disabled")
        self._canvas.delete(self.__your_label)
        self._canvas.delete(self.__enemy_label)
        self._canvas.create_image(600, 430,
                                  image=self.__labels_images["You Lose"],
                                  anchor=CENTER_ANCHOR)

    def toggle_column_buttons(self, activate):
        if not activate:
            # Remove other label if it is still present
            self._canvas.delete(self.__your_label)
            for button in self.__column_buttons:
                button.config(state="disabled")
            self.__enemy_label = \
                self._canvas.create_image(600, 430, image=self.__labels_images[
                    "Enemy Turn"], anchor=CENTER_ANCHOR)
            self._parent.after(1500,
                               lambda: self._canvas.delete(self.__enemy_label))
        else:
            # Remove other label if it is still present
            self._canvas.delete(self.__enemy_label)
            for button in self.__column_buttons:
                button.config(state="active")
            self.__your_label = \
                self._canvas.create_image(600, 430, image=self.__labels_images[
                    "Your Turn"], anchor=CENTER_ANCHOR)
            self._parent.after(1500,
                               lambda: self._canvas.delete(self.__your_label))

    def __handle_message(self, text=None):
        """
        Specifies the event handler for the message getting event in the
        communicator. Prints a message when invoked (and invoked by the
        communicator when a message is received). The message will
        automatically disappear after a fixed interval.
        :param text: the text to be printed.
        :return: None.
        """
        if text:
            self.__label["text"] = text
            self._parent.after(self.MESSAGE_DISPLAY_TIMEOUT,
                               self.__handle_message)
        else:
            self.__label["text"] = ""

    def __make_random_move(self):
        col = randint(0, 6)
        # while not self.__game.get_board().add_chip(col, game.Game.PLAYER_ONE,
        #                                            self.__game):
        while col >= 0:
            try:
                self.__game.make_move(col)
                col = -1
            except:
                col = randint(0, 6)


if __name__ == '__main__':
    root = t.Tk()
    root.resizable(width=False, height=False)
    # Finds out the IP, to be used cross-platform without special issues.
    # (on local machine, could also use "localhost" or "127.0.0.1")
    port = 8000
    server = False
    if server:
        GUI(root, port)
        root.title("Server")
    else:
        GUI(root, port, socket.gethostbyname(socket.gethostname()))
        root.title("Client")
    root.mainloop()
