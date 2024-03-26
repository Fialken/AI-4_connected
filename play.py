import time
from Game4InLine import Game4InLine as G4Line
from MCTS import MCTS

BOARD_SIZE_STANDARD = True #make it 'False' if u want to play 4InLine with a board diff from 6x7
TIME_MCTS = 5 #time for search with mcts

def result(game,col):
    res=game.isFinished(col)
    if res:
        if res==2:
            print(f"Draw")
        else:
            print(f"{game.pieces[game.turn-1]} won")
        return True
    return False


def main(): #func for the game
    #in case user decides to play with a different board size from 6x7
    if BOARD_SIZE_STANDARD: game=G4Line(6,7)
    else: 
        r,c=map(int,input("Min board size: 5x5\nBoard size: (rows,cols) ").split())
        if(r<=4 or c<=4): game=G4Line(6,7)
        else: game=G4Line(r,c) 
    print(f"Board:\n{game}")
    
    #if user want to play vs AI (and which AI, when MCTS is implemented)
    Ai_playing = input("Play with AI [y\\n]: ")
    while Ai_playing!='y' and Ai_playing!='n':
        Ai_playing = input(f"Invalid choice\nPlay with AI [y\\n]: ")

    which_AI = 0
    if Ai_playing == "y":
      which_AI = int(input("A*: 1    MCTS: 2\nChoose (1 or 2): "))
    while which_AI != 1 and which_AI != 2:
        which_AI = int(input("Invalid choice\nA*: 1    MCTS: 2\nChoose (1 or 2): "))
    print("")


    #main loop
    while True: 
        #Human play       
        print(f"player {game.turn%2 +1} ('{game.pieces[game.turn%2]}') turn")

        column_played = int(input("Column to place: ")) - 1
        while (column_played > game.cols-1 or column_played < 0) or game.placed[column_played] >= game.rows :
            print("Impossible move")
            column_played = int(input("Column to place: ")) - 1

        game.play(column_played)
        print(f"Board:\n{game}")
        
        
        if result(game,column_played):
            break


        #AI play
        if which_AI == 1: #A*
            column_played=game.A_star(lambda state,col: G4Line.heuristic_points(state,col)+ G4Line.heuristic_extra(state,col))
            game.play(column_played)
            print(f"AI play: {column_played+1}")


        elif which_AI == 2: #MCTS
            tree = MCTS(game)
            tree.search(TIME_MCTS) 
            column_played = tree.best_move()
            n_simulations, run_time= tree.statistic()
            game.play(column_played)
            print(f"AI play: {column_played+1}")
            print(f"Num simulations = {n_simulations} in {run_time:.5f}seg")


        print(f"Board:\n{game}")
        if Ai_playing == 'y':
            if result(game,column_played):
                break


def main_A_star():
    start_time = time.time()
    game=G4Line(6,7)
    #main loop
    while True: 
        time.sleep(0.5)       
        print(f"AI {game.turn%2 +1} ('{game.pieces[game.turn%2]}') turn")
        
        #AI play 
        column_played=game.A_star(lambda state,col: G4Line.heuristic_points(state,col)+ G4Line.heuristic_extra(state,col))
        game.play(column_played)
        print(f"AI play: {column_played+1}")
        print(f"Board:\n{game}")

        if result(game,column_played):
            break

    print(f"game took {(time.time()-start_time):.0f} seg and {game.round} rounds")


def main_mcts():
    start_time = time.time()
    game=G4Line(6,7)
    #main loop
    while True:        
        print(f"AI {game.turn%2 +1} ('{game.pieces[game.turn%2]}') turn")
        
        #AI play 
        tree = MCTS(game)
        tree.search(TIME_MCTS) 
        column_played = tree.best_move()
        n_simulations, run_time= tree.statistic()

        print(f"AI {game.turn%2 +1} play: {column_played+1}")
        print(f"Num simulations = {n_simulations} in {run_time:.2f}seg")
        game.play(column_played)
        print(f"Board:\n{game}")

        if result(game,column_played):
            break

    print(f"game took {(time.time()-start_time):.0f} seg and {game.round} rounds")



if __name__ == "__main__":
    qual = int(input(f"Qual modo:\n1: Player vs AI ou PvP\n2: A* vs A*\n3: MCTS vs MCTS\nEscolha: "))
    if qual == 1:
        main()
    elif qual == 2:
        main_A_star()
    elif qual == 3:    
        main_mcts()