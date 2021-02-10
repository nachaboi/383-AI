from math import inf
from agent import Agent


class MinimaxAgent(Agent):
    depth_limit = None
    eval_fn = None
    prune = None

    def __init__(self, eval_fn=None, depth_limit=inf, prune=False):
        self.depth_limit = depth_limit
        self.eval_fn = eval_fn
        self.prune = prune
    


    def select_action(self, game, state):
        # #0 is us, 1 is other
        def checkNode(game, state, current, loc):
            if loc >= self.depth_limit:
                return self.eval_fn(game, state)
            theOptions = game.get_actions(state)
            if len(theOptions) == 0:
                if current == 0:
                    return -1
                else:
                    return 1
            else:
                total = []
                if current == 0:
                    current = 1
                else:
                    current = 0

                for i in theOptions:
                    total.append(checkNode(game, game.apply_action(state, i), current, loc+1))

                #torevert
                if current == 0:
                    current = 1
                else:
                    current = 0

                if current == 0:
                    highest = -1
                    for j in total:
                        if j >= highest:
                            highest = j
                    return highest
                else:
                    lowest = 1
                    for j in total:
                        if j <= lowest:
                            lowest = j
                    return lowest

        """
        TODO: Implement the minimax algorithm
        """
        first = True
        bestMax = -1
        bestAct = None
        options = game.get_actions(state)
        for i in options:
            temp = game.apply_action(state, i)
            new = checkNode(game, temp, 1, 1)
            if first:
                bestMax = new
                bestAct = i
                first = False
            elif(new >= bestMax):
                bestMax = new
                bestAct = i
        return bestAct



    





