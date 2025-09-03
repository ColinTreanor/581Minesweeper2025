from minesweeper import minesweeper

def main():
    game = minesweeper(10)  
    game.PlaceMines()       
    print(game)
    print(game.DebugBoard())

if __name__ == "__main__":
    main()