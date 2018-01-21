import socket
import tkinter as t

# TODO:: REMOVE
from random import randint

from communicator import Communicator
from game import Game
from board import *
from sys import argv


if __name__ == '__main__':
    if 3 <= len(argv) <= 4 and Game.MIN_PORT_VALUE <= int(
            argv[2]) <= Game.MAX_PORT_VALUE:
        game = Game()

    else:
        # TODO:: Write actual error message
        print("error")
