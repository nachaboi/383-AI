import csv
import math


class DataSet:
    """
    This class reads the dataset from a csv file, given the file path as a string.
    It exposes the following class members:

        attributes: a list of strings representing the name of each attribute
        domains: a list of lists indicating the possible values each attribute
                 in self.attributes can take in the provided data
        examples: a list of lists, with each element representing a datapoint
    """
    def __init__(self, path_to_csv):
        with open(path_to_csv, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            self.attributes = next(csvreader)
            self.examples = [row for row in csvreader]
            self.domains = [list(set(x)) for x in zip(*self.examples)]

    def set_attrs(self, attrs):
        self.attributes = attrs

    def set_examples(self, exs):
        self.examples = exs

    def set_domains(self, doms):
        self.domains = doms


class Node:
    """
    This class represents an internal node of a decision tree.
    `test_attr` is the index of the attribute to test at this node.
    `test_name` is the human-readable name of that attribute.
    The Node stores a dictionary `self.children` that maps values of the test
    attribute to subtrees, where each subtree is either a Node or a Leaf.
    """
    def __init__(self, test_attr, test_name=None):
        self.test_attr = test_attr
        self.test_name = test_name or test_attr
        self.children = {}

    def classify(self, example):
        """Classify an example based on its test attribute value."""

        # TODO: Implement the classify function here and in the Leaf class

        return self.children[example[self.test_attr]].classify(example)

    def add_child(self, val, subtree):
        """Add a child node, which could be either a Node or a Leaf."""
        self.children[val] = subtree

    def show(self, level=1):
        """Print a human-readable representation of the tree"""
        print('Test:', self.test_name)
        for (val, subtree) in self.children.items():
            print(' ' * 4 * level, "if", self.test_name, '=', val, '==>', end=' ')
            if isinstance(subtree, Leaf):
                subtree.show()
            else:
                subtree.show(level + 1)


class Leaf:
    """A Leaf holds only a predicted class, with no test."""
    def __init__(self, pred_class):
        self.pred_class = pred_class

    def classify(self, example):
        # TODO: Implement the classify function here
        return self.pred_class

    def show(self):
        """This will be called by the Node `show` function"""
        print('Predicted class:', self.pred_class)


def learn_decision_tree(dataset, target_name, feature_names, depth_limit):
    """
    Trains a decision tree on the provided dataset.
    The `target_name` parameter is the name of the attribute to be predicted.
    The `feature_names` are the names of input attributes that should be used to split the data.
    Finally, `depth_limit` is a parameter to control overfitting by cutting off the tree after
    a certain depth and predicting the plurality class at that split.

    This function should return a decision tree learned from the data.
    """
    domains = dataset.domains
    target = dataset.attributes.index(target_name)
    features = [dataset.attributes.index(name) for name in feature_names]

    def plurality(examples):
        theSum = 0
        arr=[]
        for i in examples:
            count = 0
            thisOne = i[target]
            found = 0
            for j in arr:
                if j[0] == thisOne:
                    j[1] += 1
                    found += 1
            if found == 0:
                arr.append([thisOne, 1])
        # print(arr)

        maxval = 0
        theVal = None

        for k in arr:
            if k[1] > maxval:
                theVal = k[0]
                maxval = k[1]
            elif k[1] == maxval:
                temp = []
                if theVal != None:
                    temp.append(theVal)
                if k[0] != None:
                    temp.append(k[0])
                temp.sort()
                theVal = temp[0]
        return theVal

    def best_IG(example, attrs):
        arr = []
        for i in range(len(attrs)):
            if i != target:
                curarr = toSplit(example, attrs[i])
                gain = information_gain(example, curarr)
                arr.append([attrs[i], gain])

        maxval = 0
        theVal = None

        for k in arr:
            if k[1] > maxval:
                theVal = k[0] 
                maxval = k[1]
            elif k[1] == maxval:
                temp = []
                if theVal != None:
                    temp.append(theVal)
                if k[0] != None:
                    temp.append(k[0])
                # temp = [theVal, k[0]]
                temp.sort()
                theVal = temp[0]
        # print(dataset.attributes.index(dataset.attributes[theVal]))
        return dataset.attributes.index(dataset.attributes[theVal])

    def toSplit(example, attr):
        theLists = []

        for i in example:
            wasAdded = 0
            for j in theLists:
                if j[0][attr] == i[attr]:
                    j.append(i)
                    wasAdded += 1
            if wasAdded == 0:
                theLists.append([i])
        return theLists

    def cleaner(theList):

        yes = 0
        no = 0
        toReturn = []

        for i in theList:
            if i == "Yea":
                yes += 1
            elif i == "Nay":
                no += 1

        for i in theList:
            if i == "Yea" or i == "Nay" or i == "Democrat" or i == "Republican":
                toReturn.append(i)
            else:
                if yes > no:
                    toReturn.append("Yea")
                else:
                    toReturn.append("Nay")
        return toReturn


    def decision_tree_learning(examples, attrs, parent_examples=(), depth=0):
        """
        This function signature is written to match the pseudocode
        on p. 702 of Russell and Norvig. We recommend following that
        pseudocode to implement your decision tree.
        Note that we are adding an argument for the current depth, so you can
        keep track of the depth limit.

        This function should return the decision tree that has been learned.
        """

        # TODO: Implement the logic for learning the decision tree
        # You must also implement the entropy and information gain functions below.
        # We recommend adding your own helper functions below too, but don't remove
        # any of the provided code.

        if(depth == 0):
            return Leaf(plurality(examples))

        classes = []
        for a in examples:
            added = 0
            x = a[target]
            for b in classes:
                if b == x:
                    added += 1
            if added == 0:
                classes.append(x)

        if len(examples) == 0:
            return Leaf(plurality(parent_examples))
        
        elif len(classes) == 1:
            return Leaf(classes[0])

        elif len(attrs) == 0:
            return Leaf(plurality(examples))
        # elif
        #     return (information_gain(dataset.examples)) 
        else:
            best = best_IG(examples, attrs)
            tree = Node(best)
            domain = []
            for i in examples:
                if i[best] not in domain:
                    domain.append(i[best])
            for j in domain:
                temp = []
                for k in examples:
                    if k[best] == j:
                        temp.append(k)
                arr = []
                for l in attrs:
                    if l != best:
                        arr.append(l)
                sub = decision_tree_learning(temp, arr, examples, depth-1)
                tree.add_child(j, sub)

            return tree


    def entropy(examples):
        """Takes a list of examples and returns their entropy w.r.t. the target attribute"""

        # TODO: Implement the entropy function
        theSum = 0
        arr=[]
        for i in examples:
            count = 0
            thisOne = i[target]
            found = 0
            for j in arr:
                if j[0] == thisOne:
                    j[1] += 1
                    found += 1
            if found == 0:
                arr.append([thisOne, 1])
        # print(arr)
        for k in arr:
            prob = k[1]/len(examples)
            # print(prob)
            theSum -= prob*math.log(prob,2)
        return theSum

    def information_gain(parent, children):
        """
        Takes a `parent` set and a subset `children` of the parent.
        Returns the information gain due to splitting `children` from `parent`.
        """

        # TODO: Implement the information gain
        childSum = 0
        for i in children:
            childSum += (len(i)/len(parent)) * entropy(i)

        return entropy(parent) - childSum

    theCleaned = []
    for i in dataset.examples:
        theCleaned.append(cleaner(i))

    return decision_tree_learning(theCleaned, features, (), depth_limit)


if __name__ == '__main__':
    """
    You can use this area to test your implementation and to generate
    output for the assignment. The autograder will ignore this area.
    """

    ############################
    ###### Example usage: ######
    ############################

    data = DataSet("./congress_small.csv")

    # An example of learning a decision tree to predict party affiliation
    # based on the values of votes 4-7
    t = learn_decision_tree(
        data,
        "class",
        ["vote4", "vote5", "vote6", "vote7"],
        2
    )

    t2 = learn_decision_tree(
        data,
        "class",
        ["vote4", "vote5", "vote6", "vote7"], math.inf
    )

    print(t)
    t.show()
    t2.show()