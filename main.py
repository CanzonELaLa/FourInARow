import socket
import tkinter as t

from communicator import Communicator


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
        self._canvas = t.Canvas(self._parent, width=300, height=300)
        self._canvas.pack()
        self.__communicator = Communicator(parent, port, ip)
        self.__communicator.connect()
        self.__communicator.bind_action_to_message(self.__handle_message)
        self.__place_widgets()

    def __place_widgets(self):
        self.__button = t.Button(self._parent, text="YO",
                                 font=("Garamond", 20, "bold"),
                                 command=lambda: self.__communicator.
                                 send_message("YO"))
        self.__button.pack()
        self.__button.place(x=120, y=120)
        self.__label = t.Label(self._parent, text="", fg="red",
                               font=("Garamond", 40, "bold"))
        self.__label.pack()
        self.__label.place(x=109, y=200)

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
