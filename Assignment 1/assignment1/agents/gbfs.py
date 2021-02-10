from .agent import Agent

import queue
import math

class GBFS(Agent):
    def search(self, gridworld):
        class Node:
            def __init__(self, cur, pred):
                self.cur = cur
                self.pred = pred
            def getCur(self):
                return self.cur
            def getPred(self):
                return self.pred

        def getHeur(coord):
            a = gridworld.goal_state
            x1 = abs(a[0] - coord[0])
            y1 = abs(a[1] - coord[1])
            return math.sqrt((x1 * x1) + (y1 * y1))

        frontier = []
        semiFront = []
        explored = []
        nodes_expanded = 0
        cost = 0

        frontier.append(Node(gridworld.initial_state, None))

        if gridworld.initial_state == gridworld.goal_state:
            return gridworld.initial_state, 1, 0
        while len(frontier) > 0:
            curState = frontier.pop(0)
            explored.append(curState.getCur())
            curLoc = curState.getCur()
            if curLoc == gridworld.goal_state:
                listed = []
                curNode = curState
                while curNode.getPred() is not None:
                    listed.insert(0, curNode.getCur())
                    cost += gridworld.cost(curNode.getCur())
                    curNode = curNode.getPred()
                listed.insert(0,curNode.getCur())
                # cost += gridworld.cost(curNode.getCur())
                return listed, cost, nodes_expanded
            else:
                nodes_expanded += 1
                suc = gridworld.successors(curLoc)
                # print(curLoc)
                # print(suc)
                for i in suc:
                    if i not in explored and i not in semiFront:
                        frontier.append(Node(i, curState))
                        semiFront.append(i)
                frontier.sort(key=lambda x: getHeur(x.cur))
        return None, None, None






