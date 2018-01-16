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
    if (len(argv) == 4 or len(argv) == 3) and 0 <= int(argv[2]) <= 65535:
        port = int(argv[2])
        ai = True if argv[1] == "ai" else False

        game = Game()
        ip = None

        if len(argv) == 4:
            ip = argv[3]

        commune = Communicator(game.get_root(), port, ip)
        commune.connect()
        commune.bind_action_to_message(game.eat_message)

    else:
        # TODO:: Write actual error message
        print("error")
