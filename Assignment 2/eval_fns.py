"""
Evaluation functions for use with Minimax search.
We have supplied you with one example function to get started.
An evaluation function should return an estimate of the utility of a state.
Thus, it should be high when max is winning and low when min is winning, and
it should be bounded by the terminal utilities +1 and -1.
Any evaluation function should return the utility when given a terminal state.
Keep these criteria in mind when writing your evaluation functions.
"""


def open_cells(game, state):
    """
    Estimates utility from the number of open cells next to the current player.
    More open cells is preferable to fewer.
    """
    if game.is_terminal(state):
        return game.utility(state)
    else:
        # the number of open cells next to the current player
        open_cells = {cell for (cell, _) in game.get_actions(state)}

        # there are at best 8 open cells, so score is near 1 when things are
        # "good" for the current player, and near 0 when things are "bad"
        score = len(open_cells) / 8
        return -score if state.min_to_play else score


def my_eval_1(game, state):
    """
    Write your own evaluation function here.
    Your functions must take two arguments, a game and a state.

    Hint: Think about why open_cells is not a very good evaluation function!
    How might you improve it?
    """
    if game.is_terminal(state):
        return game.utility(state)

    else:
        coord = (-1, -1)
        if state.min_to_play:
            coord = state.min_pos
        else:
            coord = state.max_pos
        count = 0


        #can go left
        if coord[0] -1 >= 0:
            #can go up
            if coord[1]-1 >= 0:
                #top left
                if state.board[coord[1]-1][coord[0]-1] == 0:
                    count += 1
            #side left
            if state.board[coord[1]][coord[0]-1] == 0:
                count += 1
            #can go down
            if coord[1]+1 <= len(state.board) - 1:
                #bottom left
                if state.board[coord[1]+1][coord[0]-1]:
                    count += 1
        #can go right
        if coord[0] + 1 <= len(state.board) - 1:
            #can go up
            if coord[1]-1 >= 0:
                #top mid
                if state.board[coord[1]-1][coord[0]+1] == 0:
                    count += 1
            #side right
            if state.board[coord[1]][coord[0]+1] == 0:
                count += 1
            #can go down
            if coord[1]+1 <= len(state.board) - 1:
                #bottom right
                if state.board[coord[1]+1][coord[0]+1]:
                    count += 1
        #mid
        #can go up
        if coord[1]-1 >= 0:
                #top mid
                if state.board[coord[1]-1][coord[0]] == 0:
                    count += 1
        #can go down
        if coord[1]+1 <= len(state.board) - 1:
                #bottom mid
                if state.board[coord[1]+1][coord[0]]:
                    count += 1
        score = count/8
        return -score if state.min_to_play else score


def my_eval_2(game, state):
    """
    Write your second evaluation function here.
    """
    a = open_cells(game, state)
    b = my_eval_1(game, state)

    return (a+b)/2

    


def my_best(game, state):
    """
    Call whichever one of your two functions you think is better
    and return the result here.
    """
    return my_eval_2(game, state)
