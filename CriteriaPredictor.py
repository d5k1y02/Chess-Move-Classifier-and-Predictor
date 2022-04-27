# -*- coding: utf-8 -*-
"""

@author: Desmond Yancey
"""
import os
import numpy as np
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.metrics import ConfusionMatrixDisplay
from joblib import dump, load
import tensorflow as tf
from keras import initializers 





def read_position(file):
    pos_str = file.read()
    pos_str = pos_str.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace("'", '').replace('\n', ',').replace(' ', '')
    pos_str = pos_str.strip(',')
    arr = pos_str.split(',')
    tdarr = []
    i = 0
    tdarr = np.zeros(0)
    while(i < 128):
        sarr = np.zeros(8)
        if(arr[i] == 'p'):
            sarr[0] = 1
        elif(arr[i] == 'r'):
            sarr[1] = 1
        elif(arr[i] == 'n'):
            sarr[2] = 1
        elif(arr[i] == 'b'):
            sarr[3] = 1
        elif(arr[i] == 'q'):
            sarr[4] = 1
        elif(arr[i] == 'k'):
            sarr[5] = 1
        i+=1
        if(arr[i]) == 'b':
            sarr[6] = 1
        if(arr[-1] == 1):
            sarr[7] = 1
        i+=1
        tdarr = np.concatenate((tdarr, sarr))
    return tdarr

def get_labels(file_name):
    file = open(file_name)
    labels = []
    for line in file.readlines():
        labels.append(int(line.split(',')[1].strip('\n')))
    return labels

def get_positions(path):
    positions = []
    for filename in os.listdir(path):
        with open(path + filename, 'r') as f:
            positions.append(read_position(f))
    return positions

def train_nn_keras():
    X_train = np.array(get_positions("./chessdataset/train/"))
    y_train = np.array(get_labels("chess_labels_train.csv"))
    X_test = np.array(get_positions("./chessdataset/test/"))
    y_test = np.array(get_labels("chess_labels_test.csv"))
    y_train_tf = tf.keras.utils.to_categorical(y_train-1, num_classes = 6)
    y_test_tf = tf.keras.utils.to_categorical(y_test-1, num_classes = 6)
    train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train_tf))
    test_dataset = tf.data.Dataset.from_tensor_slices((X_test, y_test_tf))

    BATCH_SIZE = 10
    SHUFFLE_BUFFER_SIZE = 100

    train_dataset = train_dataset.shuffle(SHUFFLE_BUFFER_SIZE).batch(BATCH_SIZE)
    test_dataset = test_dataset.batch(BATCH_SIZE)

    # x = tf.keras.Input(shape = (64,8))
    # y = tf.keras.layers.Dense(6, activation='softmax')(x)
    # model = tf.keras.Model(x, y)
    my_init = initializers.RandomUniform(minval = -0.05, maxval = 0.05, seed = None) 
    model = tf.keras.Sequential([
    tf.keras.layers.Dense(512, activation='relu', kernel_initializer = my_init),
    tf.keras.layers.Dense(64, activation='sigmoid'),
    tf.keras.layers.Dense(6, activation = tf.keras.activations.softmax)
    ])

    model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.1),
                loss= 'categorical_crossentropy',
                metrics=['categorical_accuracy'])

    model.fit(train_dataset, epochs=50)
    model.summary()
    print(model.evaluate(test_dataset))
    predictions = model.predict(X_test)
    y_pred = []
    for l in predictions:
        max = l[0]
        label = 0
        for p in range(len(l)):
            if l[p] > max:
                max = l[p]
                label = p
        y_pred.append(label)
    #matrix = metrics.confusion_matrix(y_test.argmax(axis=1), y_pred.argmax(axis=1))

    ConfusionMatrixDisplay.from_predictions(y_test,y_pred)
    plt.show()

def train_tree_classifier():
    X_train = np.array(get_positions("./chessdataset/train/"))
    y_train = get_labels("chess_labels_train.csv")
    

    #d1, d2, d3, d4 = X_train.shape
    #X_train2 = X_train.reshape((d1, d2*d3*d4))
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X_train, y_train)
    print(clf.score(X_test, y_test))
    dump(clf, 'tree1400-1600ELO.joblib')
    return 

X_test = np.array(get_positions("./chessdataset/test/"))
y_test = get_labels("chess_labels_test.csv")



#d1, d2, d3, d4 = X_test.shape
#X_test2 = X_test.reshape((d1, d2*d3*d4))

#train_tree_classifier()
train_nn_keras()
#clf = load('tree1400-1600ELO.joblib')
# text_representation = tree.export_text(clf)
# print(text_representation)
#print(clf.score(X_test, y_test))