'''
Created on May 10, 2020

@author: Zoya Samsonov
'''

import math
import random as r
mask = [4, 2, 1]


class point:
    def __init__(self, A, B, C, Classifier):
        self.Attributes = [A, B, C]
        self.Classifier = Classifier  # true/false

    def __repr__(self):
        return str(self.Attributes) + " -> " + str(self.Classifier) + "\n"


class forest:
    def __init__(self, points):
        self.points = points
        self.trees = []

    def genMTreesNPoints(self, n, m):
        for i in range(0, m):
            treePoints = getpointset(self.points, n)
            self.trees.append(treeNode(treePoints))
            print("TREE " + str(i) + "\n")
            print(self.trees[-1])

    def classify(self, test_point):
        majority_yes = 0
        majority_no = 0
        for j, t in enumerate(self.trees):
            if t.classify(test_point):
                print("Tree " + str(j) + " classifies point " +
                      str(test_point.Attributes) + " as True")
                majority_yes += 1
            else:
                print("Tree " + str(j) + " classifies point " +
                      str(test_point.Attributes) + " as False")
                majority_no += 1
        if majority_yes >= majority_no:
            print("Forest classifies point " +
                  str(test_point.Attributes) + " as True")
            return True
        else:
            print("Forest classifies point " +
                  str(test_point.Attributes) + " as False")
            return False

    def validate(self, test_point):
        classifyVal = self.classify(test_point)
        if classifyVal == test_point.Classifier:
            print("Validation: Forest matches Actual\n")
        else:
            print("Validation: Forest disagrees with Actual\n")


class treeNode:
    def __init__(self, points, parentClassifier=-1, split_options=7, tabstop=""):
        self.points = points
        self.tabstop = tabstop
        self.entropy = getEntropy(self.points)
        # using binary encoding of ABC similar to file perms in unix
        self.split_options = split_options
        self.parentClassifier = parentClassifier
        self.classifyAttribute = self.get_best_split()
        self.children = []
        self.split()

    def classify(self, test_point):
        if len(self.children) > 0:
            if test_point.Attributes[self.classifyAttribute]:
                #print("Yes on attribute " + str(self.classifyAttribute))
                return self.children[0].classify(test_point)
            else:
                #print("No on attribute " + str(self.classifyAttribute))
                return self.children[1].classify(test_point)
        else:
            majority_yes = 0
            majority_no = 0
            for p in self.points:
                if p.Classifier:
                    majority_yes += 1
                else:
                    majority_no += 1
            if majority_yes >= majority_no:
                #print(str(test_point.Attributes) + " -> True\n")
                return True
            else:
                #print(str(test_point.Attributes) + " -> False\n")
                return False

    def simsplit(self, bitmask):
        # gets Gain for a simulated split
        if bitmask & self.split_options == bitmask:
            option = mask.index(bitmask)

            points_split_pos = []
            points_split_neg = []
            for p in self.points:
                if p.Attributes[option] == 1:
                    points_split_pos.append(p)
                else:
                    points_split_neg.append(p)

            E_pos = getEntropy(points_split_pos)
            E_neg = getEntropy(points_split_neg)
            total = len(self.points)
            Info = len(points_split_pos) / total * E_pos + \
                len(points_split_neg) / total * E_neg
            return self.entropy - Info
        return 0

    def get_best_split(self):
        gains = []
        for bitmask in mask:
            gains.append(self.simsplit(bitmask))
        maxgain = max(gains)
        if maxgain == 0:
            return self.parentClassifier
        else:
            return gains.index(max(gains))  # split on max

    def split(self):
        # inefficient reuse of code, would be better to store this when calculating the best split
        if self.split_options > 0 and self.entropy > 0:
            # split if this is not a leaf
            points_split_pos = []
            points_split_neg = []
            for p in self.points:
                if p.Attributes[self.classifyAttribute] == 1:
                    points_split_pos.append(p)
                else:
                    points_split_neg.append(p)
            new_options = self.split_options - mask[self.classifyAttribute]
            self.children.append(
                treeNode(points_split_pos, self.classifyAttribute,
                         split_options=new_options, tabstop=self.tabstop + "\t"))
            self.children.append(
                treeNode(points_split_neg, self.classifyAttribute,
                         split_options=new_options, tabstop=self.tabstop + "\t"))

    def __repr__(self):
        points_repr = self.tabstop + "points: {\n"
        for p in self.points:
            points_repr += self.tabstop + "\t" + str(p)
        points_repr += self.tabstop + "}\n"
        child_repr = ""
        for c in self.children:
            child_repr += self.tabstop + "\t" + str(c)
        if len(self.children) > 0:
            return "E = " + str(self.entropy) + "\n" +\
                   self.tabstop + "Classifier = " + str(self.classifyAttribute) + "\n" +\
                   self.tabstop + "children: {\n" + \
                child_repr + self.tabstop + "}\n"
        else:
            return "E = " + str(self.entropy) + "\n" +\
                   points_repr + self.tabstop + "LEAF\n\n"


def getEntropy(points):
    # assuming binary classifier since the assignment is binary / don't want to program more than is needed
    class_positive = 0.0
    class_negative = 0.0
    total = 0.0
    for p in points:
        total += 1.0
        if p.Classifier:
            class_positive += 1.0
        else:
            class_negative += 1.0
    E_pos = 0.0
    E_neg = 0.0
    if class_positive > 0:
        E_pos = -1 * (class_positive / total) * \
            math.log((class_positive / total), 2)
    if class_negative > 0:
        E_neg = -1 * (class_negative / total) * \
            math.log((class_negative / total), 2)
    return E_pos + E_neg


def getpointset(points, n):
    newpoints = []
    for j in range(0, n):
        newpoints.append(points[r.randint(0, len(points) - 1)])
    return newpoints
