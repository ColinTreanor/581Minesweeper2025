from board import Board


def main():
    # for testing can be deleted
    board = Board()

    board.startGame(5, (5, 5))
    board.RevealSpace((1, 2))
    board.PrintActualBoard()
    print("----------------------------")
    board.PrintVisibleBoard()


main()