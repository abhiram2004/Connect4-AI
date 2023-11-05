from FourConnect import *
from ABHIRAM_2021A7PS2525G import *

def RunStats():
    """
    This procedure reads the state in testcase.csv file and start the game.
    Player 2 moves first. Player 2 must win in 5 moves to pass the testcase; Otherwise, the program fails to pass the testcase.
    """
    numOfWins = 0
    numLossesDueToTimeOut = 0
    NUM_ITERATIONS = 100
    
    for i in range(NUM_ITERATIONS):
        fourConnect = FourConnect()
        gameTree = GameTreePlayer()
        testcaseState = LoadTestcaseStateFromCSVfile()
        fourConnect.SetCurrentState(testcaseState)
        fourConnect.PrintGameState()

        move=0
        while move<MAX_ALLOWED_NUM_OF_MOVES: #Player 2 must win in allowd number of moves
            if move%2 == FIRST_PLAYER: 
                fourConnect.MyopicPlayerAction()
            else:
                currentState = fourConnect.GetCurrentState()
                gameTreeAction = gameTree.FindBestAction(currentState)
                fourConnect.GameTreePlayerAction(gameTreeAction)
            fourConnect.PrintGameState()
            move += 1
            if fourConnect.winner!=None:
                break

        
        if fourConnect.winner==2:
            numOfWins += 1
        else:
            if move == MAX_ALLOWED_NUM_OF_MOVES:
                numLossesDueToTimeOut += 1
    
    print(f"Game tree depth = {GAME_TREE_DEPTH}")
    print(f"Max allowed number of moves = {MAX_ALLOWED_NUM_OF_MOVES}")
    print(f"Total number of iterations: {NUM_ITERATIONS}")
    print(f"Total percentage of wins: {numOfWins*100/NUM_ITERATIONS}%")
    numLosses = NUM_ITERATIONS - numOfWins
    print(f"Total percentage of losses due to timeout: {numLossesDueToTimeOut*100/numLosses}%")
        

def main():
    RunStats()

if __name__ == "__main__":
    main()
    