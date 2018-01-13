import socket
import tkinter as t

from communicator import Communicator

DELTA_HEIGHT = 130
DELTA_WIDTH = 180
DELTA_CELL = 109
CELL_PADDING = 13
DEFAULT_STATE = "EMPTY"
FIRST_PLAYER = "Images/Red.gif"
SECOND_PLAYER = "Images/Blue.gif"
YOUR_TURN = "Images/Your turn.gif"
ENEMY_TURN = "Images/Enemy turn.gif"
BOARD_IMAGE = "Images/Board.gif"
BG_IMAGE = "Images/bg.gif"
WIN_LABEL = "Images/You win.gif"
LOSE_LABEL = "Images/You lose.gif"


class Cell:
    def __init__(self, location, board):
        self.__width_delta = location[0]
        self.__height_delta = location[1]
        self.__chip = Chip(DEFAULT_STATE)
        self.__location = location
        self.__board = board

    def get_location(self):
        return self.__location

    def set_chip(self, player):
        self.__chip.set_player(player)

    def get_chip(self):
        return self.__chip


class Board:
    def __init__(self, canvas, size=(7, 6)):
        self.__width = size[0]
        self.__canvas = canvas
        self.__height = size[1]
        self.__columns = []
        self.red_piece = t.PhotoImage(file=FIRST_PLAYER)
        self.blue_piece = t.PhotoImage(file=SECOND_PLAYER)

        for i in range(7):
            column = []
            for j in range(6):
                column.append(Cell((DELTA_WIDTH + CELL_PADDING +
                                    (CELL_PADDING - 2) * i + DELTA_CELL * i,
                                    DELTA_HEIGHT + CELL_PADDING +
                                    (CELL_PADDING - 2) * j + DELTA_CELL * j),
                                   self))
            # column.reverse()
            self.__columns.append(column)

    def add_chip(self, column, player):
        if self.__columns is None:
            return False
        row = -1
        for i in range(len(self.__columns[column]) - 1, 0, -1):
            if self.__columns[column][i].get_chip().get_player() == \
                    DEFAULT_STATE:
                row = i
                self.__columns[column][i].get_chip().set_player(player)
                break
        if row == -1:
            return False

        cell = self.__columns[column][row]

        self.__set_cell(player, column, row)
        if player == "first":
            chip = self.red_piece
        else:
            chip = self.blue_piece

        self.__canvas.create_image(cell.get_location()[0],
                                   cell.get_location()[1], image=chip,
                                   anchor="nw")
        return True

    def __set_cell(self, player, column, row):
        self.__columns[column][row].get_chip().set_player(player)

    def get_columns(self):
        return self.__columns


class Chip:
    def __init__(self, player):
        self.__player = player

    def get_player(self):
        return self.__player

    def set_player(self, player):
        self.__player = player


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
        # self.__board_image = t.PhotoImage(file=BOARD_IMAGE)
        # self._canvas.create_image(DELTA_WIDTH, DELTA_HEIGHT,
        #                           image=self.__board_image, anchor="nw")
        self.__bg = t.PhotoImage(file=BG_IMAGE)
        self._canvas.create_image(0, 0, image=self.__bg, anchor="nw")
        self.__board = Board(self._canvas)
        self.__communicator = Communicator(parent, port, ip)
        self.__communicator.connect()
        self.__communicator.bind_action_to_message(self.__handle_message)
        self.__column_buttons = []
        self.__column_buttons_flag = True
        self.__column_button_images = [t.PhotoImage(file="Images/button" +
                                                         str(x) + ".gif")
                                       for x in
                                       range(1,8)]
        self.__labels = {}
        self.__labels["Your Turn"] = t.PhotoImage(file=YOUR_TURN)
        self.__labels["Enemy Turn"] = t.PhotoImage(file=ENEMY_TURN)
        self.__labels["You Win"] = t.PhotoImage(file=WIN_LABEL)
        self.__labels["You Lose"] = t.PhotoImage(file=LOSE_LABEL)
        self.__your_label = None
        self.__enemy_label = None
        self.__place_widgets()

    def __place_widgets(self):
        def create_add_chip_func(i):
            def add_chip_func():
                self.__toggle_column_buttons()
                return self.__board.add_chip(i, "first")

            return add_chip_func

        self.__button_image = t.PhotoImage(file=FIRST_PLAYER)
        self.__button1_image = t.PhotoImage(file="Images/button1.gif")
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
                                 command=self.__toggle_column_buttons)
        self.__win_button = t.Button(self._parent, text="win",
                                     command=self.__show_win)
        self.__lose_button = t.Button(self._parent, text="lose",
                                      command=self.__show_lose)

        # self.__button.pack()
        self.__button.place(x=0, y=60)
        self.__win_button.place(x=0, y=0)
        self.__lose_button.place(x=0, y=30)

    def __show_win(self):
        for button in self.__column_buttons:
            button.config(state="disabled")
        if self.__your_label:
            self._canvas.delete(self.__your_label)
        if self.__enemy_label:
            self._canvas.delete(self.__enemy_label)
        self._canvas.create_image(600, 430, image=self.__labels["You Win"],
                                  anchor="center")

    def __show_lose(self):
        for button in self.__column_buttons:
            button.config(state="disabled")
        if self.__your_label:
            self._canvas.delete(self.__your_label)
        if self.__enemy_label:
            self._canvas.delete(self.__enemy_label)
        self._canvas.create_image(600, 430, image=self.__labels["You Lose"],
                                  anchor="center")

    def __toggle_column_buttons(self, flag=None):
        def remove_enemy_label():
            self._canvas.delete(self.__enemy_label)
            self.__enemy_label = None

        def remove_your_label():
            self._canvas.delete(self.__your_label)
            self.__your_label = None

        if flag is not None:
            self.__column_buttons_flag = flag

        if self.__column_buttons_flag:
            if self.__your_label:
                self._canvas.delete(self.__your_label)
            self.__column_buttons_flag = False
            for button in self.__column_buttons:
                button.config(state="disabled")
            self.__enemy_label = \
                self._canvas.create_image(600, 430, image=self.__labels[
                    "Enemy Turn"], anchor="center")
            self._parent.after(1500,
                               lambda: remove_enemy_label())
        else:
            if self.__enemy_label:
                self._canvas.delete(self.__enemy_label)
            self.__column_buttons_flag = True
            for button in self.__column_buttons:
                button.config(state="active")
            self.__your_label = \
                self._canvas.create_image(600, 430, image=self.__labels[
                    "Your Turn"], anchor="center")
            self._parent.after(1500,
                               lambda: remove_your_label())

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
