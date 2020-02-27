import copy as cpy
import random
import sys

ROW_COUNT = 6
COL_COUNT = 7

class maxConnect4Game:
    def __init__(self):
        self.gameBoard = [[0 for i in range(7)] for j in range(6)]
        self.currentTurn = 1
        self.player1Score = 0
        self.player2Score = 0
        self.pieces = 0
        self.gameFile = None
        random.seed()

    # Counts the number of pieces in play
    def pieceCount(self):
        self.pieces = sum(1 for row in self.gameBoard for piece in row if piece)

    # Outputs the state of the board to the console
    def printBoard(self):
        print('-----------------')
        for rowItem in range(ROW_COUNT):
            print("|", end='')
            for columnItem in range(COL_COUNT):
                print(" ", end='')
                print(self.gameBoard[rowItem][columnItem], end='')
            print(" |")
        print('-----------------')

    # Outputs the game status to a file
    def printToFile(self):
        for row in range(ROW_COUNT):
            for col in range(COL_COUNT):
                self.gameFile.write(str(self.gameBoard[row][col]))
            self.gameFile.write("\n")
        self.gameFile.write(str(self.currentTurn))
    
    # Place the current player's piece in its proper column
    def playSelection(self, column):
        if column < 0 or column >= COL_COUNT:
            print("Please choose a valid column.")
            return 0
        # If there is not a piece on the topmost row, then place one on the lowest unoccupied row
        elif not self.gameBoard[0][column]:
            for i in range(ROW_COUNT - 1, -1, -1):
                if not self.gameBoard[i][column]:
                    self.gameBoard[i][column] = self.currentTurn
                    self.pieces += 1
                    
                    # Swaps the turn to the next player
                    if self.currentTurn == 1:
                        self.currentTurn = 2
                    else:
                        self.currentTurn = 1
                    return 1
        print("Please choose a valid column.")
        return 0
    
    # Scores the utility of 4-slot cells on the board
    def score(self, slot, turn):
        slotScore = 0
        # Groups of 4 are worth a ton of utility to encourage it
        if slot.count(turn) == 4 :
            slotScore += 100
        # The program rewards creating groups of fewer than 4 as well, but not by much
        elif slot.count(turn) == 3:
            if slot.count(0) == 1:
                slotScore += slot.count(turn) * 3
        elif slot.count(turn) == 2:
            if slot.count(0) == 2:
                slotScore += slot.count(turn) * 2
        elif slot.count(turn) == 1:
            if slot.count(0) == 3:
                slotScore += slot.count(turn)

        # If the opponent has the advantage in this slot (3 pieces), discourage it
        if turn == 1:
            if slot.count(2) == 3 and slot.count(0) == 1:
                slotScore -= slot.count(turn) * 2
        else:
            if slot.count(1) == 3 and slot.count(0) == 1:
                slotScore -= slot.count(turn) * 2
        return slotScore

    # Measures the "utility" of a piece's position on the board.
    # Heuristic: Adjacent pieces incur a higher score, the more there are next to each other, the better
    def utilMeasure(self, board, turn):
        util = 0

        # Scores the piece horizontally
        for i in range(ROW_COUNT):
            rowElements = [element for element in board[i]]
            for j in range(COL_COUNT - 3):
                slot = rowElements[j:j + 4]
                util += self.score(slot, turn)

        # Scores the piece vertically (using the transpose of the board)
        transposeBoard = [*zip(*board)]
        for i in range(COL_COUNT):
            colElements = [element for element in transposeBoard[i]]
            for j in range(ROW_COUNT - 3):
                slot = colElements[j:j + 4]
                util += self.score(slot, turn)
                
        # Scores the piece diagonally
        for i in range(ROW_COUNT - 3):
            for j in range(COL_COUNT - 3):
                slot = [board[i + z][j + z] for z in range(4)]
                util += self.score(slot, turn)
                slot = [board[i + 3 - z][j + z] for z in range(4)]
                util += self.score(slot, turn)
        return util

    # AI takes a turn using depth-limited minimax search with alpha-beta pruning
    # References used: https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning and the lecture material
    def CPUTurn(self, board, depth, turn, alpha, beta):
        validMoves = self.getValidMoves(board)
        # If the depth limit is reached or there are no valid moves left, return the heuristic value of the moves
        if depth == 0 or len(validMoves) == 0:
            if len(validMoves) == 0:
                return self.countScore(board)
            elif turn == 1:
                return None, self.utilMeasure(board, turn)
            else:
                return None, self.utilMeasure(board, turn)
        
        # If it is the max player's turn, expand each choice available to them
        if turn == 1:
            utility = -sys.maxsize
            choice = random.choice(validMoves)
            # For each available selection (child of this node), compare values
            for column in validMoves:
                boardCopy = cpy.deepcopy(board)
                row = self.getNextTile(board, column)
                boardCopy[row][column] = turn
                newUtil = self.CPUTurn(boardCopy, depth - 1, 2, alpha, beta)[1]
                # Gets the maximum found value from the children nodes
                if utility < newUtil:
                    choice = column
                    utility = newUtil
                # Discards this section of the search tree if it can be pruned
                alpha = max(alpha, utility)
                if alpha >= beta:
                    break
            return choice, utility
        
        # If it is the min. player's turn, expand the nodes available to them
        else:
            utility = sys.maxsize
            choice = random.choice(validMoves)
            # For each available selection (child of this node), compare values
            for column in validMoves:
                row = self.getNextTile(board, column)
                boardCopy = cpy.deepcopy(board)
                boardCopy[row][column] = turn
                newUtil = self.CPUTurn(boardCopy, depth - 1, 1, alpha, beta)[1]
                # Gets the minimum found value from the children nodes
                if newUtil < utility:
                    choice = column
                    utility = newUtil
                beta = min(beta, utility)
                # Discards this section of the search tree if it can be pruned
                if alpha >= beta:
                    break
            return choice, utility

    # Returns the lowest available row
    def getNextTile(self, board, col):
        for i in range(ROW_COUNT - 1, -1, -1):
            if not board[i][col]:
                return i
        
    # Checks topmost row of board for any open spaces where pieces can be placed
    def getValidMoves(self, board):
        temp = board[0]
        validMoves = []
        for i in range(COL_COUNT):
            if not temp[i]:
                validMoves.append(i)
        # Returns list of indicies of each playable slot
        return validMoves
        
    # Counts the scores between both players
    def countScore(self, board):
        player1Score = 0
        player2Score = 0
        # Check horizontally
        for row in board:
            # Check player 1
            if row[0:4] == [1]*4:
                player1Score += 1
            if row[1:5] == [1]*4:
                player1Score += 1
            if row[2:6] == [1]*4:
                player1Score += 1
            if row[3:7] == [1]*4:
                player1Score += 1
            # Check player 2
            if row[0:4] == [2]*4:
                player2Score += 1
            if row[1:5] == [2]*4:
                player2Score += 1
            if row[2:6] == [2]*4:
                player2Score += 1
            if row[3:7] == [2]*4:
                player2Score += 1

        # Check vertically
        for j in range(COL_COUNT):
            # Check player 1
            if (board[0][j] == 1 and board[1][j] == 1 and
                   board[2][j] == 1 and board[3][j] == 1):
                player1Score += 1
            if (board[1][j] == 1 and board[2][j] == 1 and
                   board[3][j] == 1 and board[4][j] == 1):
                player1Score += 1
            if (board[2][j] == 1 and board[3][j] == 1 and
                   board[4][j] == 1 and board[5][j] == 1):
                player1Score += 1
            # Check player 2
            if (board[0][j] == 2 and board[1][j] == 2 and
                   board[2][j] == 2 and board[3][j] == 2):
                player2Score += 1
            if (board[1][j] == 2 and board[2][j] == 2 and
                   board[3][j] == 2 and board[4][j] == 2):
                player2Score += 1
            if (board[2][j] == 2 and board[3][j] == 2 and
                   board[4][j] == 2 and board[5][j] == 2):
                player2Score += 1

        # Check diagonally

        # Check player 1
        if (board[2][0] == 1 and board[3][1] == 1 and
               board[4][2] == 1 and board[5][3] == 1):
            player1Score += 1
        if (board[1][0] == 1 and board[2][1] == 1 and
               board[3][2] == 1 and board[4][3] == 1):
            player1Score += 1
        if (board[2][1] == 1 and board[3][2] == 1 and
               board[4][3] == 1 and board[5][4] == 1):
            player1Score += 1
        if (board[0][0] == 1 and board[1][1] == 1 and
               board[2][2] == 1 and board[3][3] == 1):
            player1Score += 1
        if (board[1][1] == 1 and board[2][2] == 1 and
               board[3][3] == 1 and board[4][4] == 1):
            player1Score += 1
        if (board[2][2] == 1 and board[3][3] == 1 and
               board[4][4] == 1 and board[5][5] == 1):
            player1Score += 1
        if (board[0][1] == 1 and board[1][2] == 1 and
               board[2][3] == 1 and board[3][4] == 1):
            player1Score += 1
        if (board[1][2] == 1 and board[2][3] == 1 and
               board[3][4] == 1 and board[4][5] == 1):
            player1Score += 1
        if (board[2][3] == 1 and board[3][4] == 1 and
               board[4][5] == 1 and board[5][6] == 1):
            player1Score += 1
        if (board[0][2] == 1 and board[1][3] == 1 and
               board[2][4] == 1 and board[3][5] == 1):
            player1Score += 1
        if (board[1][3] == 1 and board[2][4] == 1 and
               board[3][5] == 1 and board[4][6] == 1):
            player1Score += 1
        if (board[0][3] == 1 and board[1][4] == 1 and
               board[2][5] == 1 and board[3][6] == 1):
            player1Score += 1

        if (board[0][3] == 1 and board[1][2] == 1 and
               board[2][1] == 1 and board[3][0] == 1):
            player1Score += 1
        if (board[0][4] == 1 and board[1][3] == 1 and
               board[2][2] == 1 and board[3][1] == 1):
            player1Score += 1
        if (board[1][3] == 1 and board[2][2] == 1 and
               board[3][1] == 1 and board[4][0] == 1):
            player1Score += 1
        if (board[0][5] == 1 and board[1][4] == 1 and
               board[2][3] == 1 and board[3][2] == 1):
            player1Score += 1
        if (board[1][4] == 1 and board[2][3] == 1 and
               board[3][2] == 1 and board[4][1] == 1):
            player1Score += 1
        if (board[2][3] == 1 and board[3][2] == 1 and
               board[4][1] == 1 and board[5][0] == 1):
            player1Score += 1
        if (board[0][6] == 1 and board[1][5] == 1 and
               board[2][4] == 1 and board[3][3] == 1):
            player1Score += 1
        if (board[1][5] == 1 and board[2][4] == 1 and
               board[3][3] == 1 and board[4][2] == 1):
            player1Score += 1
        if (board[2][4] == 1 and board[3][3] == 1 and
               board[4][2] == 1 and board[5][1] == 1):
            player1Score += 1
        if (board[1][6] == 1 and board[2][5] == 1 and
               board[3][4] == 1 and board[4][3] == 1):
            player1Score += 1
        if (board[2][5] == 1 and board[3][4] == 1 and
               board[4][3] == 1 and board[5][2] == 1):
            player1Score += 1
        if (board[2][6] == 1 and board[3][5] == 1 and
               board[4][4] == 1 and board[5][3] == 1):
            player1Score += 1

        # Check player 2
        if (board[2][0] == 2 and board[3][1] == 2 and
               board[4][2] == 2 and board[5][3] == 2):
            player2Score += 1
        if (board[1][0] == 2 and board[2][1] == 2 and
               board[3][2] == 2 and board[4][3] == 2):
            player2Score += 1
        if (board[2][1] == 2 and board[3][2] == 2 and
               board[4][3] == 2 and board[5][4] == 2):
            player2Score += 1
        if (board[0][0] == 2 and board[1][1] == 2 and
               board[2][2] == 2 and board[3][3] == 2):
            player2Score += 1
        if (board[1][1] == 2 and board[2][2] == 2 and
               board[3][3] == 2 and board[4][4] == 2):
            player2Score += 1
        if (board[2][2] == 2 and board[3][3] == 2 and
               board[4][4] == 2 and board[5][5] == 2):
            player2Score += 1
        if (board[0][1] == 2 and board[1][2] == 2 and
               board[2][3] == 2 and board[3][4] == 2):
            player2Score += 1
        if (board[1][2] == 2 and board[2][3] == 2 and
               board[3][4] == 2 and board[4][5] == 2):
            player2Score += 1
        if (board[2][3] == 2 and board[3][4] == 2 and
               board[4][5] == 2 and board[5][6] == 2):
            player2Score += 1
        if (board[0][2] == 2 and board[1][3] == 2 and
               board[2][4] == 2 and board[3][5] == 2):
            player2Score += 1
        if (board[1][3] == 2 and board[2][4] == 2 and
               board[3][5] == 2 and board[4][6] == 2):
            player2Score += 1
        if (board[0][3] == 2 and board[1][4] == 2 and
               board[2][5] == 2 and board[3][6] == 2):
            player2Score += 1

        if (board[0][3] == 2 and board[1][2] == 2 and
               board[2][1] == 2 and board[3][0] == 2):
            player2Score += 1
        if (board[0][4] == 2 and board[1][3] == 2 and
               board[2][2] == 2 and board[3][1] == 2):
            player2Score += 1
        if (board[1][3] == 2 and board[2][2] == 2 and
               board[3][1] == 2 and board[4][0] == 2):
            player2Score += 1
        if (board[0][5] == 2 and board[1][4] == 2 and
               board[2][3] == 2 and board[3][2] == 2):
            player2Score += 1
        if (board[1][4] == 2 and board[2][3] == 2 and
               board[3][2] == 2 and board[4][1] == 2):
            player2Score += 1
        if (board[2][3] == 2 and board[3][2] == 2 and
               board[4][1] == 2 and board[5][0] == 2):
            player2Score += 1
        if (board[0][6] == 2 and board[1][5] == 2 and
               board[2][4] == 2 and board[3][3] == 2):
            player2Score += 1
        if (board[1][5] == 2 and board[2][4] == 2 and
               board[3][3] == 2 and board[4][2] == 2):
            player2Score += 1
        if (board[2][4] == 2 and board[3][3] == 2 and
               board[4][2] == 2 and board[5][1] == 2):
            player2Score += 1
        if (board[1][6] == 2 and board[2][5] == 2 and
               board[3][4] == 2 and board[4][3] == 2):
            player2Score += 1
        if (board[2][5] == 2 and board[3][4] == 2 and
               board[4][3] == 2 and board[5][2] == 2):
            player2Score += 1
        if (board[2][6] == 2 and board[3][5] == 2 and
               board[4][4] == 2 and board[5][3] == 2):
            player2Score += 1
        return player1Score, player2Score