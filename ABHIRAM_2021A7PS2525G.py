#!/usr/bin/env python3
from FourConnect import * # See the FourConnect.py file
import csv
import math
import random 
# import os, sys


CSV_FILE = "testcase.csv"

# The total depth of the game tree
GAME_TREE_DEPTH = 4

# The maximum number of moves allowed for the game tree player
MAX_ALLOWED_NUM_OF_MOVES = 5

# Which player plays first, 0 - Myopic player starts, 1 - GameTree Player starts
# FIRST_PLAYER = 1

"Constants used in file, do not change these values"

# What is the value of each piece
EMPTY = 0
MYOPIC_PIECE = 1
GAMETREE_PIECE = 2

# The total number of rows and columns
ROW_COUNT = 6
COLUMN_COUNT = 7

# The size of the window to evaluate
WINDOW_LENGTH = 4
    
    
class GameTreePlayer:
    
    def __init__(self):
        pass
    
    # Check if the column has been fully filled or not
    def isValidColumn(self, board, col):
        return board[0][col] == 0
 
    # Drop a piece to that particular cell
    def dropPiece(self, board, row, col, piece):
        board[row][col] = piece
    
    # Gets the lowest open position (0) in a specified column 
    def getNextOpenRow(self, board, col):
        for r in range(ROW_COUNT-1, 0, -1):
            if board[r][col] == 0:
                return r
    
    # Checks if move will be a winning move
    def winning_move(self, board, piece):
        # Check horizontal locations for win
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    return True
                
        return False
    
    # Evaluate the score (heurestic evaluation score)
    def evaluateWindow(self, window, piece):
        score = 0
        opp_piece = MYOPIC_PIECE
        if piece == MYOPIC_PIECE:
            opp_piece = GAMETREE_PIECE

        # Score for each window, higher score is better
        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2
            
        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 4
        # elif window.count(opp_piece) == 4:
        #     score -= 100

        # elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
        #     score -= 10

        return score
    
    def heuristicEvalFunction(self, board, piece):
        score = 0
        # Score center column
        center_array = [int(board[i][COLUMN_COUNT//2]) for i in range(ROW_COUNT)]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Score Horizontal
        for r in range(ROW_COUNT):
            row_array = [int(board[r][c]) for c in range(COLUMN_COUNT)]
            for c in range(COLUMN_COUNT-3):
                window = row_array[c:c+WINDOW_LENGTH]
                score += self.evaluateWindow(window, piece)

        # Score Vertical
        for c in range(COLUMN_COUNT):
            col_array = [int(board[r][c]) for r in range(ROW_COUNT)]
            for r in range(ROW_COUNT-3):
                window = col_array[r:r+WINDOW_LENGTH]
                score += self.evaluateWindow(window, piece)

        # Score principal diagonal
        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
                score += self.evaluateWindow(window, piece)

        # Check secondary diagonal
        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
                score += self.evaluateWindow(window, piece)

        return score

    # Get all the valid locations where a piece can be inserted
    def getValidLocations(self, board):
        valid_locations = []
        for col in range(COLUMN_COUNT):
            if self.isValidColumn(board, col):
                valid_locations.append(col)
        return valid_locations
    
    # Checks if the game has reached a terminal state
    def isTerminalNode(self, board):
        return self.winning_move(board, MYOPIC_PIECE) or self.winning_move(board, GAMETREE_PIECE) or len(self.getValidLocations(board)) == 0
    
    # def myopicPlayerActionWrapper(self, board):
    #     tempBoard = FourConnect()
    #     tempBoard.SetCurrentState(board)
        
    #     # Redirecting output so it doesn't print anything
    #     old_stdout = sys.stdout # backup current stdout
    #     sys.stdout = open(os.devnull, "w")
        
    #     tempBoard.MyopicPlayerAction()
        
    #     sys.stdout = old_stdout # reset old stdout
    
    #     return tempBoard.GetCurrentState()
    
    # Minimax Algorithm in alpha-beta pruning
    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.getValidLocations(board)
        is_terminal = self.isTerminalNode(board)
        
        
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winning_move(board, GAMETREE_PIECE):
                    return (None, 100000000000000)
                elif self.winning_move(board, MYOPIC_PIECE):
                    return (None, -10000000000000)
                else:
                    return (None, 0)
            else:
                return (None, self.heuristicEvalFunction(board, GAMETREE_PIECE))
            
        if maximizingPlayer:
            value = -math.inf
            best_column = None  # Initialize to None
            for col in valid_locations:
                row = self.getNextOpenRow(board, col)
                if row is not None:  # Check if the row is not None
                    b_copy = copy.deepcopy(board)         
                    self.dropPiece(b_copy, row, col, GAMETREE_PIECE)
                    _, new_score = self.minimax(b_copy, depth - 1, alpha, beta, False)
                    if new_score > value:
                        value = new_score
                        best_column = col

                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break

            if best_column is None:
                best_column = random.choice(valid_locations)  # Handle the case when no valid columns are found

            return best_column, value
        else:  # Minimizing player
            value = math.inf
            best_column = None  # Initialize to None
            for col in valid_locations:
                row = self.getNextOpenRow(board, col)
                if row is not None:  # Check if the row is not None
                    b_copy = copy.deepcopy(board)      
                    self.dropPiece(b_copy, row, col, MYOPIC_PIECE)
                    _, new_score = self.minimax(b_copy, depth - 1, alpha, beta, True)
                    if new_score < value:
                        value = new_score
                        best_column = col

                    beta = min(beta, value)
                    if alpha >= beta:
                        break
            
            
            # b_copy = self.myopicPlayerActionWrapper(board)  
            # _, new_score = self.minimax(b_copy, depth - 1, alpha, beta, True)
            # if new_score < value:
            #     value = new_score
                
            # beta = min(beta, value)
            
            if best_column is None:
                best_column = random.choice(valid_locations)  # Handle the case when no valid columns are found

            return best_column, value

    
    def FindBestAction(self,currentState):
        """
        Modify this function to search the GameTree instead of getting input from the keyboard.
        The currentState of the game is passed to the function.
        currentState[0][0] refers to the top-left corner position.
        currentState[5][6] refers to the bottom-right corner position.
        Action refers to the column in which you decide to put your coin. The actions (and columns) are numbered from left to right.
        Action 0 is refers to the left-most column and action 6 refers to the right-most column.
        """
        
        # bestAction = input("Take action (0-6) : ")
        # bestAction = int(bestAction)
        # return bestAction
        
        col = 0
        col, _ = self.minimax(currentState, GAME_TREE_DEPTH, -math.inf, math.inf, True)
        return col
        
    

def LoadTestcaseStateFromCSVfile():
    testcaseState=list()

    with open(CSV_FILE, 'r') as read_obj: 
        csvReader = csv.reader(read_obj)
        for csvRow in csvReader:
            row = [int(r) for r in csvRow]
            testcaseState.append(row)
    return testcaseState


def PlayGame():
    fourConnect = FourConnect()
    fourConnect.PrintGameState()
    gameTree = GameTreePlayer()
    
    move=0
    while move<42: #At most 42 moves are possible
        if move%2 == 0: #Myopic player always moves first
            fourConnect.MyopicPlayerAction()
        else:
            currentState = fourConnect.GetCurrentState()
            gameTreeAction = gameTree.FindBestAction(currentState)
            fourConnect.GameTreePlayerAction(gameTreeAction)
        fourConnect.PrintGameState()
        move += 1
        if fourConnect.winner!=None:
            break
    
    """
    You can add your code here to count the number of wins average number of moves etc.
    You can modify the PlayGame() function to play multiple games if required.
    """
    if fourConnect.winner==None:
        print("Game is drawn.")
    else:
        print("Winner : Player {0}\n".format(fourConnect.winner))
    print("Moves : {0}".format(move))

def RunTestCase():
    """
    This procedure reads the state in testcase.csv file and start the game.
    Player 2 moves first. Player 2 must win in 5 moves to pass the testcase; Otherwise, the program fails to pass the testcase.
    """
    
    fourConnect = FourConnect()
    gameTree = GameTreePlayer()
    testcaseState = LoadTestcaseStateFromCSVfile()
    fourConnect.SetCurrentState(testcaseState)
    fourConnect.PrintGameState()

    move=0
    while move<MAX_ALLOWED_NUM_OF_MOVES: #Player 2 must win in allowed number of moves
        if move%2 == 1: # Assumed that myopic player already made first move 
            fourConnect.MyopicPlayerAction()
        else:
            currentState = fourConnect.GetCurrentState()
            gameTreeAction = gameTree.FindBestAction(currentState)
            fourConnect.GameTreePlayerAction(gameTreeAction)
        fourConnect.PrintGameState()
        move += 1
        if fourConnect.winner!=None:
            break
    
    print("Roll no : 2021A7PS2525G") #Put your roll number here
    
    if fourConnect.winner==2:
        print("Player 2 has won. Testcase passed.")
    else:
        print(f"Player 2 could not win in {MAX_ALLOWED_NUM_OF_MOVES} moves. Testcase failed.")
    print("Moves : {0}".format(move))
    

def main():
    
    # PlayGame()
    """
    You can modify PlayGame function for writing the report
    Modify the FindBestAction in GameTreePlayer class to implement Game tree search.
    You can add functions to GameTreePlayer class as required.
    """

    """
        The above code (PlayGame()) must be COMMENTED while submitting this program.
        The below code (RunTestCase()) must be UNCOMMENTED while submitting this program.
        Output should be your rollnumber and the bestAction.
        See the code for RunTestCase() to understand what is expected.
    """
    
    RunTestCase()


if __name__=='__main__':
    main()
