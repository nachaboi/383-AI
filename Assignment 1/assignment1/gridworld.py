class Gridworld:
    states = None
    initial_state = None
    goal_state = None

    def __init__(self, filename):
        with open(filename) as file:
            self.states = [list(line) for line in file.read().splitlines()]
            for y, line in enumerate(self.states):
                for x, value in enumerate(line):
                    if value.isnumeric():
                        line[x] = int(value)
                    if value == 's':
                        self.initial_state = (x, y)
                    if value == 'g':
                        self.goal_state = (x, y)

    def successors(self, state):
        # TODO
        x1 = state[0]
        y1 = state[1]

        theList = []

        numrows = len(self.states)
        numcols = len(self.states[0])

        if x1 < 0  or x1 > numcols - 1:
            return
        if y1 < 0 or y1 > numrows - 1:
            return

        if x1+1 <= numcols -1 and self.states[y1][x1+1] != '#':
            theList.append((x1+1, y1))
        if y1+1 <= numrows -1 and self.states[y1+1][x1] != '#':
            theList.append((x1, y1+1))
        if x1-1 >= 0 and self.states[y1][x1-1] != '#':
            theList.append((x1-1, y1))
        if y1-1 >= 0 and self.states[y1-1][x1] != '#':
            theList.append((x1, y1-1))

        return theList

    def cost(self, state):
        # TODO
        x1 = state[0]
        y1 = state[1]

        numrows = len(self.states)
        numcols = len(self.states[0])

        if x1 < 0  or x1 > numcols - 1:
            return
        if y1 < 0 or y1 > numrows - 1:
            return

        if self.states[y1][x1] == '#':
            return
        if self.states[y1][x1] == 's' or self.states[y1][x1] == 'g':
            return 1
        else:
            return int(self.states[y1][x1])





