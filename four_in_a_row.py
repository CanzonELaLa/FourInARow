import socket
import tkinter as t

# TODO:: REMOVE
from random import randint

from communicator import Communicator
from game import Game
from board import *
from sys import argv


if __name__ == '__main__':
    # root = t.Tk()
    # root.resizable(width=False, height=False)
    # # Finds out the IP, to be used cross-platform without special issues.
    # # (on local machine, could also use "localhost" or "127.0.0.1")
    # port = 8000
    # server = True
    # if server:
    #     GUI(root, port)
    #     root.title("Server")
    # else:
    #     GUI(root, port, socket.gethostbyname(socket.gethostname()))
    #     root.title("Client")
    # root.mainloop()

    if 3 <= len(argv) <= 4 and Game.MIN_PORT_VALUE <= int(
            argv[2]) <= Game.MAX_PORT_VALUE:
        game = Game()

    else:
        # TODO:: Write actual error message
        print("error")
