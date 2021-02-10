import csv
import math
import numpy as np
from sklearn.cluster import KMeans

def to_numerical(votes):
    return [1 if (vote == 'Yea' or vote == 'Aye' or vote == 'Present') else 0 for vote in votes]

def to_string(votes):
    """
        Implement the inverse of to_numerical here.
        (hint: Change this if you make changes to to_numerical.)
    """
    return ["Yea" if vote == 1 else "Nay" for vote in votes]

class CongressionalKMeans():
    def __init__(self, path_to_csv, k, seed=0):
        """
        A model for clustering members of congress based on 
        their voting records. Complete this constructor in order
        to load the voting records from the file given by
        path_to_csv.
        (hint 1: See get_votes for the desired format.)
        (hint 2: Use to_binary function to convert data into numeric format 
                 appropriate for k-means clustering)
        (hint 3: You can use the DataSet constructor in tree.py for inspiration,
                 but you will need to do some things differently. You also do not
                 need all of the attributes, only the voting record.)

        Args:
            path_to_csv (str): The path to a congressional data set
            k (int): The number of clusters to fit
            seed (int): The random seed
        """
        np.random.seed(seed)
        self.k = k
        #selfadded
        self.kmeans = KMeans(n_clusters=k, n_init=10, max_iter=300, random_state=0, init="random")
        with open(path_to_csv, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            ##### TODO complete the constructor #####
            next(csvreader)
            # self.examples = to_numerical(self.examples)
            tempList = [row for row in csvreader]

            newList = []
            party = []
            for i in tempList:
                thisList = []
                toDel = 0
                for j in i:
                    if toDel <=3:
                        toDel += 1
                    if toDel == 4:
                        party.append(j)
                        toDel +=1
                    else:
                        thisList.append(j)
                thisList = to_numerical(thisList)
                newList.append(thisList)

            self.examples = newList
            self.theParty = party

    def getParty(self):
        return self.theParty

    def get_votes(self):
        """
        Returns an (N, M) numpy array containing all votes 2018,
        where N is the number of congresspeople and M is the number 
        of resolutions. Each vote should have a numerical value. (See to_numerical)
        (hint: You shouldn't have to do anything accept access an
               instance variable in this function. All of the work
               should be done in the constructor)
        """
        return np.array(self.examples)

    def fit(self):
        """
        Fit the dataset using k-means clustering.
        (hint: Store any variables you need for other parts
               of the assignment as instance variables. No return
               value is necessary.)
        """

        self.kmeans.fit(self.examples)

    

    def predict(self, i):
        """
        Predict the cluster for the i-th congressperson.
        Return a single number representing the cluster ID.
        (hint 1: you must call fit() first)
        (hint 2: see the documentation for sklearn.cluster.KMeans.predict())
        (hint 3: remember to store anything you need in fit())

        Args:
            i (int): The index of the congressperson to predict.

        Returns:
            (int): The cluster that the i-th congressperson belongs to.
        """
        self.fit()
        arr = self.kmeans.predict(self.examples, None)
        return arr[i]



    def get_cluster_center(self, i):
        """
        Return a numpy array of size (N,) containing center of the i-th cluster.
        (hint: see the documentation for sklearn.cluster.KMeans.cluster_centers_)
        """
        return self.kmeans.cluster_centers_[i]

    def get_median_voter(self, i):
        """
        Return an numpy array of size (N,) containing the the most likely
        vote for each vote for the given cluster.
        (hint: Use np.round on the cluster center to convert votes to 0 or 1 (or other values that you use).)
        """

        return np.round(self.get_cluster_center(i))


if __name__ == '__main__':
    """
    You can use this area to test your implementation and to generate
    output for the assignment. The autograder will ignore this area.
    """
    kmeans = CongressionalKMeans('congress_data.csv', 2)
    print(kmeans.get_votes())
    kmeans.fit()
    print("new")
    print(kmeans.get_votes())

    print(kmeans.predict(0))
    print(kmeans.predict(2))
    print(kmeans.get_cluster_center(1))
    print(np.round(kmeans.get_cluster_center(1),2))

    print(kmeans.get_median_voter(1))

    # count = 0
    # demCount = 0
    # correctDemCount = 0
    # repCount = 0
    # correctRepCount = 0
    # print("here",kmeans.getParty())
    # badPeople = []
    # for i in kmeans.getParty():

    #     if i == "Democrat":
    #         demCount += 1
    #         if kmeans.predict(count) == 1:
    #             correctDemCount += 1
    #         else:
    #             badPeople.append(count)
    #     elif i == "Republican":
    #         repCount += 1
    #         if kmeans.predict(count) == 0:
    #             correctRepCount += 1
    #         else:
    #             badPeople.append(count)
    #     count += 1
    # print(demCount)
    # print(correctDemCount)
    # print(repCount)
    # print(correctRepCount)
    # print(badPeople)

    count = 0
    misMatch = 0
    total = 0
    first = kmeans.get_median_voter(0)
    second = kmeans.get_median_voter(1)
    print(first)
    for i in range(0,419):
        if abs(first[i]) != abs(second[i]):
            misMatch += 1
        total += 1
        count += 1
    print(misMatch)
    print(total)
