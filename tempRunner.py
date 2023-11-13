from FourConnect import *
from ABHIRAM_2021A7PS2525G import *
import time, os

CSV_FILE = "minimax_alphabeta_moveorder_3.csv"

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
            if move%2 == 1: 
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
    if numLosses == 0:
        numLosses = 1
    print(f"Total percentage of losses due to timeout: {numLossesDueToTimeOut*100/numLosses}%")
        
def playGames():
    
    NUM_ITERATIONS = 50
    NUM_WINS = 0
    NUM_LOSSES = 0
    start = time.time()
    
    numMoves = 0
    for i in range(NUM_ITERATIONS):
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
        if fourConnect.winner==1:
            NUM_LOSSES += 1
        elif fourConnect.winner==2:
            numMoves += move
            NUM_WINS += 1
            
    end = time.time()
    
    numMoves = int(numMoves / NUM_WINS)
    with open ("results.txt", "a") as f:
        f.write(f"Game tree depth = {GAME_TREE_DEPTH}\n")
        f.write(f"Total number of iterations: {NUM_ITERATIONS}\n")
        f.write(f"Total percentage of wins: {NUM_WINS*100/NUM_ITERATIONS}%\n")
        f.write(f"Total percentage of losses: {NUM_LOSSES*100/NUM_ITERATIONS}%\n")
        NUM_DRAWS = NUM_ITERATIONS - NUM_WINS - NUM_LOSSES
        f.write(f"Total percentage of draws: {NUM_DRAWS*100/NUM_ITERATIONS}%\n")
        f.write(f"Average time for each game: {(end-start)/NUM_ITERATIONS} seconds\n")
        f.write(f"Average number of moves: {numMoves}\n")
        f.write("\n")
    
    print(f"Game tree depth = {GAME_TREE_DEPTH}")
    print(f"Total number of iterations: {NUM_ITERATIONS}")
    print(f"Total percentage of wins: {NUM_WINS*100/NUM_ITERATIONS}%")
    print(f"Total percentage of losses: {NUM_LOSSES*100/NUM_ITERATIONS}%")
    NUM_DRAWS = NUM_ITERATIONS - NUM_WINS - NUM_LOSSES
    print(f"Total percentage of draws: {NUM_DRAWS*100/NUM_ITERATIONS}%")
    print(f"Average time for each game: {(end-start)/NUM_ITERATIONS} seconds")
    print(f"Average number of moves: {numMoves}")
    
def playGamesCSV():
    start = time.time()
    
    NUM_WINS = 0
    NUM_LOSSES = 0
    NUM_DRAWS = 0
    TOTAL_TIME = 0
    TOTAL_MOVES = 0
    
    if os.path.exists(CSV_FILE):
        print(f"Error: File '{CSV_FILE}' already exists. Choose a different file name.")
        return
    
    with open(CSV_FILE, "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["Game tree depth", "Winner (1/2)", "Number of moves", "Time taken (seconds)"])
        NUM_ITERATIONS = 50
        for i in range(NUM_ITERATIONS):
            start = time.time()
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
            end = time.time()
            if fourConnect.winner==None:
                NUM_DRAWS += 1
                fourConnect.winner = 0
            elif fourConnect.winner == 1:
                NUM_LOSSES += 1
            else:
                NUM_WINS += 1
                TOTAL_MOVES += move
                
            TOTAL_TIME += end-start

                
            csv_writer.writerow([GAME_TREE_DEPTH, fourConnect.winner, move, round(end-start, 3)])
        
        csv_writer.writerow([])
        
        csv_writer.writerow(["Number of wins", "Number of losses", "Number of draws", "Percentage of wins" "Average number of moves to win", "Average time for each game"])
        csv_writer.writerow([NUM_WINS, NUM_LOSSES, NUM_DRAWS, round(NUM_WINS*100/NUM_ITERATIONS, 2), round(TOTAL_MOVES/NUM_WINS, 2), round(TOTAL_TIME/NUM_ITERATIONS, 3)])
    
        print(f"Filename: {CSV_FILE}")
        print(f"Game tree depth = {GAME_TREE_DEPTH}")
        print(f"Total number of iterations: {NUM_ITERATIONS}")
        print(f"Total percentage of wins: {NUM_WINS*100/NUM_ITERATIONS}%")
        print(f"Total percentage of losses: {NUM_LOSSES*100/NUM_ITERATIONS}%")
        print(f"Total percentage of draws: {NUM_DRAWS*100/NUM_ITERATIONS}%")
        print(f"Average time for each game: {round(TOTAL_TIME/NUM_ITERATIONS, 3)} seconds")
        print(f"Average number of moves: {round(TOTAL_MOVES/NUM_WINS, 2)}")
    
            
def main():
    # RunStats()
    # playGames()
    playGamesCSV()

if __name__ == "__main__":
    main()
    