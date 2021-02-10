from .agent import Agent

import queue

class BFS(Agent):
    def search(self, gridworld):
        class Node:
            def __init__(self, cur, pred):
                self.cur = cur
                self.pred = pred
            def getCur(self):
                return self.cur
            def getPred(self):
                return self.pred
        frontier = queue.Queue()
        semiFront = []
        explored = []
        nodes_expanded = 0
        cost = 0

        frontier.put(Node(gridworld.initial_state, None))

        if gridworld.initial_state == gridworld.goal_state:
            return gridworld.initial_state, 1, 0

        while not frontier.empty():
            curState = frontier.get()
            explored.append(curState.getCur())
            curLoc = curState.getCur()
            nodes_expanded += 1
            for i in gridworld.successors(curLoc):
                if i not in explored and i not in semiFront:
                    if i == gridworld.goal_state:
                        listed = []
                        curNode = Node(i, curState)
                        while curNode.getPred() is not None:
                            listed.insert(0, curNode.getCur())
                            cost += gridworld.cost(curNode.getCur())
                            curNode = curNode.getPred()
                        listed.insert(0,curNode.getCur())
                        # cost += gridworld.cost(curNode.getCur())
                        return listed, cost, nodes_expanded
                    else:
                        frontier.put(Node(i, curState))
                        semiFront.append(i)
        return None, None, None




