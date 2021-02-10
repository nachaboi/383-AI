class Node:
	def __init__(self, cur, pred):
		self.cur = cur
		self.pred = pred
	def getCur(self):
		return self.cur
	def getPred(self):
		return self.pred

node = Node((5,6),None)
node1 = Node((4,2),node)
print(node1.getPred().getPred())

curNode = node1

while curNode.getPred() is not None:
	print(curNode.getCur())
	curNode = curNode.getPred()
print(curNode.getCur())