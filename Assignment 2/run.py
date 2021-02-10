from game import Game, State
from random_agent import RandomAgent
from minimax_agent import MinimaxAgent
from eval_fns import *
import random


if __name__ == '__main__':
    # g = Game(3)
    # g = Game(4)
    # g = Game(7)
    g = Game(5)

    # Example of setting a custom start state for the game
    # g.set_init_state(State(
    #     board=[[0, 0, 1], [1, 1, 1], [1, 0, 1]],
    #     min_pos=(1, 0),
    #     max_pos=(1, 1),
    #     min_to_play=True
    # ))

    # You can set the random seed to make your tests repeatable
    # random.seed(43110)

    # Create the agents to play in the game
    min_player = RandomAgent()
    # max_player = MinimaxAgent()
    max_player = MinimaxAgent(open_cells, 1, False)
    max_player2 = MinimaxAgent(my_eval_2, 1, False)

    # Run a complete game between the two players
    # g.play(min_player, max_player, verbose=True)

    # for i in range(0, 1000):
    #     g.play(min_player, max_player, verbose=False)

    # for i in range(0, 50):
    #     g.play(min_player, max_player, verbose=False)
    countOpen = 0
    countMy = 0
    for i in range(0, 50):
        if g.play(min_player, max_player, verbose=False)[0] == -1:
            countOpen += 1
        if g.play(min_player, max_player2, verbose=False)[0] == -1:
            countMy += 1
    print("open", countOpen)
    print("my1", countMy)