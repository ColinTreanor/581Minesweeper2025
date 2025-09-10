from board import Board


def main():
    # for testing can be deleted
    board = Board()

    board.RevealSpace((1, 2))
    board.PrintActualBoard()
    print("----------------------------")
    board.PrintVisibleBoard()


main()