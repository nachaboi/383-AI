from assignment1.gridworld import Gridworld


def run():
    gridworld = Gridworld('gw/1.txt')
    print("Hello Gridworld!")
    print(gridworld.states)
    print(gridworld.initial_state[1])
    print(len(gridworld.states))
    # print(gridworld.states[0][1])
    print(gridworld.successors((1,1)))
    print(gridworld.cost((0,0)))

if __name__ == '__main__':
    run()
