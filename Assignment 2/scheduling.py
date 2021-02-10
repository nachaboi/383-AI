from constraint import *

problem = Problem()


problem.addVariable("234", [0,1])
problem.addVariable("248", [0,1])
problem.addVariable("388", [0,1])
problem.addVariable("622", [0,1])
problem.addVariable("400", [0,1])
problem.addVariable("457", [0,1])
problem.addVariable("126", [0,1])
problem.addVariable("383", [0,1])
problem.addVariable("635", [0,1])


def func(a, b, d, e, f):
	if a+b == 2:
		return True
	if a+d == 2:
		return True
	if e+f == 2:
		return True

problem.addConstraint((func), ["234","248","388","622","457"])
problem.addConstraint(MinSumConstraint(1), ["388","622","400"])
problem.addConstraint(MinSumConstraint(1), ["457","383","126"])
problem.addConstraint(MinSumConstraint(1), ["388","635"])

#388 shows in 1, 2, 4
#622 shows in 1,2
#457 shows 1,3

def func388(a, b, c, d, e, h, i):
	if c == 1:
		#if using it for 1
		if a+c == 2:
			#nothing else can cover for it
			if a+b < 2 and d+e < 2:
				#if were using it for 2 also
				if d+h < 1:
					return False
				#if were using it for 4 also
				if i < 1:
					return False
		#if using it for 2
		if d+h == 0:
			#if were using it for 2 also
			if a+b < 2 or d+e < 2:
				return True
			#if were using it for 4 also
			if i < 1:
				return True
		if i < 1:
			if a+b < 2 or d+e < 2:
				return True
			if d+h == 0:
				return True
	return True
problem.addConstraint((func388), ["234","248","388","622","457","400","635"])

def func622(a, b, c, d, e, h):
	if d == 1:
		#if using it for 1
		if d+e == 2:
			if a+b < 2 and a+c < 2:
				if c+h < 1:
					return False
		if c+h == 0:
			if a+b < 2 and a+c < 2:
				return False
	return True
problem.addConstraint((func622),["234","248","388","622","457","400"])

def func457(a, b, c, d, e, g, h):
	if e == 1:
		if d+e == 2:
			if a+b < 2 and a+c < 2:
				if g+h < 1:
					return False
		if g+h==0:
			if a+b < 2 and a+c < 2:
				return False
	return True
problem.addConstraint((func457),["234","248","388","622","457","383","126"])


problem.addConstraint(MaxSumConstraint(1), ["388","622","635"])
problem.addConstraint(MaxSumConstraint(1), ["234","126"])
problem.addConstraint(MaxSumConstraint(1), ["457","383"])

problem.addConstraint(MinSumConstraint(1), ["635"])
problem.addConstraint(MinSumConstraint(1), ["234"])

print(len(problem.getSolutions()))