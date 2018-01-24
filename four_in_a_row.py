from game import Game
from sys import argv

ILLEGAL_ARGUMENTS_MSG = "Illegal program arguments."

GAME_MODES = ["human", "ai"]

if __name__ == '__main__':
    if 3 <= len(argv) <= 4 and Game.MIN_PORT_VALUE <= int(
            argv[2]) <= Game.MAX_PORT_VALUE and argv[1] in GAME_MODES:
        game = Game()

    else:
        print(ILLEGAL_ARGUMENTS_MSG)
