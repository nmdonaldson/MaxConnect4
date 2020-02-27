import sys
import copy as cpy
from MaxConnect4Game import *

# Plays one move of a game
def singleMove(currentGame, depth):
    # If the gameboard is full, end the game
    if currentGame.pieces == 42:
        print('BOARD FULL\n \nGame Over!\n')
        sys.exit(0)

    # Computer makes a move
    boardCopy = cpy.deepcopy(currentGame.gameBoard)
    currentGame.playSelection(currentGame.CPUTurn(boardCopy, depth, currentGame.currentTurn, -sys.maxsize, sys.maxsize)[0])

    # Prints the game state after the CPU's turn
    currentGame.printBoard()

    currentGame.player1Score, currentGame.player2Score = currentGame.countScore(currentGame.gameBoard)
    print("Score: Player 1 =", currentGame.player1Score, "Player 2 =", currentGame.player2Score)

    currentGame.printToFile()
    currentGame.gameFile.close()

# Allows the player to play against the computer
def interactiveGame(currentGame, depth):
    # Matches the CPU's turn # with the one in the file
    if currentGame.currentTurn == 1:
        currentGame.currentTurn = 2
    else:
        currentGame.currentTurn = 1

    # Runs until the board is filled
    while currentGame.pieces < 42:
        validChoice = 0
        
        # Forces the player to make a valid choice
        while not validChoice:
            # Player makes a move
            print("  1 2 3 4 5 6 7  ")
            currentGame.printBoard()
            choice = input("Choose a space to drop your piece into: ")
            validChoice = currentGame.playSelection(int(choice) - 1)
        
        # Computer makes a move
        boardCopy = cpy.deepcopy(currentGame.gameBoard)
        currentGame.playSelection(currentGame.CPUTurn(boardCopy, depth, currentGame.currentTurn, -sys.maxsize, sys.maxsize)[0])

        # Updates the score/scoreboard
        currentGame.player1Score, currentGame.player2Score = currentGame.countScore(currentGame.gameBoard)
        print("Score: Player 1 =", currentGame.player1Score, "Player 2 =", currentGame.player2Score)

    currentGame.printBoard()
    currentGame.player1Score, currentGame.player2Score = currentGame.countScore(currentGame.gameBoard)
    print("Score: Player 1 =", currentGame.player1Score, "Player 2 =", currentGame.player2Score)
    print('BOARD FULL\n \nGame Over!\n')
    sys.exit(0)


# Manages start/end of game and arguments
def main(argv):
    # Checks for the correct number of arguments
    if len(argv) != 5:
        print('Four command line arguments are needed: ')
        print('Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % argv[0])
        print('or: %s one-move [input_file] [output_file] [depth]' % argv[0])
        sys.exit(2)
    
    game_mode, inFile = argv[1:3]
    currentGame = maxConnect4Game()

    # Checks the gamemode argument
    if not game_mode == 'interactive' and not game_mode == 'one-move':
        print(game_mode, "is an unrecognized game mode")
        sys.exit(2)

    # Opens the input file
    try:
        currentGame.gameFile = open(inFile, 'r')
    except IOError:
        sys.exit("\nError opening input file", inFile, "\nCheck file name")
    
    # Read the initial game status from the file and save into data structure
    file_lines = list(currentGame.gameFile)
    currentGame.gameBoard = [[int(character) for character in line[0:7]] for line in file_lines[0:-1]]
    currentGame.currentTurn = int(file_lines[-1][0])
    currentGame.gameFile.close()

    print('\nMaxConnect-4 game\nGame state before move:')
    currentGame.printBoard()

    # Update game variables based on the starting board
    currentGame.pieceCount()
    currentGame.countScore(currentGame.gameBoard)
    print("Score: Player 1 =", currentGame.player1Score, "Player 2 =", currentGame.player2Score)

    # If the gamemode is interactive, play that. Otherwise, play for one move only
    if game_mode == 'interactive':
        interactiveGame(currentGame, int(argv[-1]))
    else:
        # Set up the output file
        outFile = argv[3]
        try:
            currentGame.gameFile = open(outFile, 'w')
        except:
            sys.exit('Error opening output file:', outFile)
        singleMove(currentGame, int(argv[-1]))

if __name__ == '__main__':
    main(sys.argv)