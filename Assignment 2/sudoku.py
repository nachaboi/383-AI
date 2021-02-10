from constraint import *

class assoc():
	def __init__(self, tuple, num):
		self.tuple = tuple
		self.num = num
problems = []

problem1 = [assoc((0,1),9), assoc((0,7),5), assoc((1,4),8), assoc((1,7),3), assoc((1,8),6),
assoc((2,0),4), assoc((2,3),5), assoc((2,7),7), assoc((3,1),5), assoc((3,2),4), assoc((3,3),3),
assoc((4,0),3), assoc((4,4),7), assoc((4,8),4), assoc((5,5),4), assoc((5,6),7), assoc((5,7),6),
assoc((6,1),2), assoc((6,5),3), assoc((6,8),5), assoc((7,0),1), assoc((7,1),4), assoc((7,4),2),
assoc((8,1),6), assoc((8,7),9)]
problems.append(problem1)

problem2 = [assoc((0,1),9), assoc((0,7),5), assoc((1,4),8), assoc((1,7),3), assoc((1,8),6),
assoc((2,0),4), assoc((2,3),5), assoc((2,7),7), assoc((3,1),5), assoc((3,2),4), assoc((3,3),3),
assoc((4,0),3), assoc((4,4),7), assoc((4,8),4), assoc((5,5),4), assoc((5,6),7), assoc((5,7),6),
assoc((6,1),2), assoc((6,5),1), assoc((6,8),5), assoc((7,0),1), assoc((7,1),4), assoc((7,4),2),
assoc((8,1),6), assoc((8,7),9)]
problems.append(problem2)

problem3 = [assoc((0,1),9), assoc((0,7),5), assoc((1,4),8), assoc((1,7),3), assoc((1,8),6),
assoc((2,0),4), assoc((2,3),5), assoc((2,7),7), assoc((3,1),5), assoc((3,2),4), assoc((3,3),3),
assoc((4,0),3), assoc((4,4),7), assoc((4,8),4), assoc((5,5),4), assoc((5,6),7), assoc((5,7),6),
assoc((6,1),2), assoc((6,5),7), assoc((6,8),5), assoc((7,0),1), assoc((7,1),4), assoc((7,4),2),
assoc((8,1),6), assoc((8,7),9)]
problems.append(problem3)

problem4 = [assoc((0,1),9), assoc((0,7),5), assoc((1,4),8), assoc((1,7),3), assoc((1,8),6),
assoc((2,0),4), assoc((2,3),5), assoc((2,7),7), assoc((3,1),5), assoc((3,2),4), assoc((3,3),3),
assoc((4,0),3), assoc((4,4),7), assoc((4,8),4), assoc((5,5),4), assoc((5,6),7), assoc((5,7),6),
assoc((6,1),2), assoc((6,5),6), assoc((6,8),5), assoc((7,0),1), assoc((7,1),4), assoc((7,4),2),
assoc((8,1),6), assoc((8,7),9)]
problems.append(problem4)

problem5 = [assoc((0,1),9), assoc((0,7),5), assoc((1,4),8), assoc((1,7),3), assoc((1,8),6),
assoc((2,0),4), assoc((2,3),5), assoc((2,7),7), assoc((3,1),5), assoc((3,2),4), assoc((3,3),3),
assoc((4,0),3), assoc((4,4),7), assoc((4,8),4), assoc((5,5),4), assoc((5,6),7), assoc((5,7),6),
assoc((6,1),2), assoc((6,5),8), assoc((6,8),5), assoc((7,0),1), assoc((7,1),4), assoc((7,4),2),
assoc((8,1),6), assoc((8,7),9)]
problems.append(problem5)

problem6 = [assoc((0,1),9), assoc((0,7),5), assoc((1,4),8), assoc((1,7),3), assoc((1,8),6),
assoc((2,0),4), assoc((2,3),5), assoc((2,7),7), assoc((3,1),5), assoc((3,2),4), assoc((3,3),3),
assoc((4,0),3), assoc((4,4),7), assoc((4,8),4), assoc((5,5),4), assoc((5,6),7), assoc((5,7),6),
assoc((6,1),2), assoc((6,5),9), assoc((6,8),5), assoc((7,0),1), assoc((7,1),4), assoc((7,4),2),
assoc((8,1),6), assoc((8,7),9)]
problems.append(problem6)


for curProb in problems:
	problem = Problem(RecursiveBacktrackingSolver())
	board = [ (row, col) for row in range(9) for col in range(9) ]

	for i in board:
		hadIt = False
		for j in curProb:
			if i == j.tuple:
				problem.addVariable(i, [j.num])
				hadIt = True
				break
		if not hadIt:
			problem.addVariable(i, range(1,10))

	for a in range(9):
		rows = []
		for b in range(9):
			rows.append((a,b))
		problem.addConstraint(AllDifferentConstraint(), rows)
		cols = []
		for c in range(9):
			cols.append((c,a))
		problem.addConstraint(AllDifferentConstraint(), cols)

	theRow = 0
	theCol = 0
	while theRow < 9:
		theCol = 0
		while theCol < 9:
			curSub = []
			for a in range(theRow, theRow+3):
				for b in range(theCol, theCol+3):
					curSub.append((a,b))
			problem.addConstraint(AllDifferentConstraint(), curSub)
			theCol += 3
		theRow +=3

	print(len(problem.getSolutions()))
