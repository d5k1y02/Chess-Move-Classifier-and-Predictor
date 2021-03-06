# -*- coding: utf-8 -*-
"""

@author: Desmond Yancey
"""
import os
import numpy as np
from sklearn import tree



def read_position(file):
    pos_str = file.read()
    pos_str = pos_str.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace("'", '').replace('\n', ',').replace(' ', '')
    pos_str = pos_str.strip(',')
    arr = pos_str.split(',')
    i = 0
    j = 1
    tdarr = np.zeros((8,8,2))
    for k in range(8):
        for l in range(8):
            tdarr[l][k][0] = ord(arr[i])
            tdarr[l][k][1] = ord(arr[j])
            i+=2
            j+=2
    return tdarr

def get_labels(file_name):
    file = open(file_name)
    labels = []
    for line in file.readlines():
        labels.append(line.split(',')[1].strip('\n'))
    return labels

def get_positions(path):
    positions = []
    for filename in os.listdir(path):
        with open(path + filename, 'r') as f:
            positions.append(read_position(f))
    return positions


def use_tree_classifier():
    X_train = np.array(get_positions("./chessdataset/train/"))
    X_test = np.array(get_positions("./chessdataset/test/"))
    y_train = get_labels("chess_labels_train.csv")
    y_test = get_labels("chess_labels_test.csv")
    d1, d2, d3, d4 = X_train.shape
    X_train2 = X_train.reshape((d1, d2*d3*d4))

    d1, d2, d3, d4 = X_test.shape
    X_train2 = X_test.reshape((d1, d2*d3*d4))


    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X_train2, y_train)
    print(clf.score(X_train2, y_test))
    return 

use_tree_classifier()
