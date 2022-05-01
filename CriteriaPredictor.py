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
    X_train_s = []
    y_train_s = []
    max_class = 2300
    class0 = 0
    class1 = 0
    class2 = 0
    class3 = 0
    class4 = 0
    class5 = 0
    for i in range(len(y_train)):
        if(y_train[i] == 0):
            class0 += 1
            if(class0 <= max_class):
                X_train_s.append(X_train[i])
                y_train_s.append(y_train[i])
        elif(y_train[i] == 1):
            class1 += 1
            if(class1 <= max_class):
                X_train_s.append(X_train[i])
                y_train_s.append(y_train[i])
        elif(y_train[i] == 2):
            class2 += 1
            if(class2 <= max_class):
                X_train_s.append(X_train[i])
                y_train_s.append(y_train[i])
        elif(y_train[i] == 3):
            class3 += 1
            if(class3 <= max_class):
                X_train_s.append(X_train[i])
                y_train_s.append(y_train[i])
        elif(y_train[i] == 4):
            class4 += 1
            if(class4 <= max_class):
                X_train_s.append(X_train[i])
                y_train_s.append(y_train[i])
        elif(y_train[i] == 5):
            class5 += 1
            if(class5 <= max_class):
                X_train_s.append(X_train[i])
                y_train_s.append(y_train[i])
          
    X_train_s = np.array(X_train_s)
    y_train_s = np.array(y_train_s)
    X_test = np.array(get_positions("./chessdataset/test/"))
    y_test = np.array(get_labels("chess_labels_test.csv"))
    y_train_tf = tf.keras.utils.to_categorical(y_train_s, num_classes = 6)
    y_test_tf = tf.keras.utils.to_categorical(y_test, num_classes = 6)
    train_dataset = tf.data.Dataset.from_tensor_slices((X_train_s, y_train_tf))
    test_dataset = tf.data.Dataset.from_tensor_slices((X_test, y_test_tf))

    print("class0: ", (y_train_s == 0).sum())
    print("class1: ", (y_train_s == 1).sum())
    print("class2: ", (y_train_s == 2).sum())
    print("class3: ", (y_train_s == 3).sum())
    print("class4: ", (y_train_s == 4).sum())
    print("class5: ", (y_train_s == 5).sum())

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
    tf.keras.layers.Dense(64),
    tf.keras.layers.Dense(6, activation = tf.keras.activations.softmax)
    ])

    model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.1),
                loss= 'categorical_crossentropy',
                metrics=['categorical_accuracy'])

    model.fit(train_dataset, epochs=40)
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

    tf.keras.models.save_model(
    model,
    './',
    overwrite=True,
    include_optimizer=True,
)
    

def train_tree_classifier():
    X_train = np.array(get_positions("./chessdataset/train/"))
    y_train = get_labels("chess_labels_train.csv")
    

    #d1, d2, d3, d4 = X_train.shape
    #X_train2 = X_train.reshape((d1, d2*d3*d4))
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X_train, y_train)
    print(clf.score(X_test, y_test))
    dump(clf, 'guillotree.joblib')
    return 

X_train = np.array(get_positions("./chessdataset/train/"))
X_test = np.array(get_positions("./chessdataset/test/"))
y_test = get_labels("chess_labels_test.csv")
y_train = get_labels("chess_labels_train.csv")


#d1, d2, d3, d4 = X_test.shape
#X_test2 = X_test.reshape((d1, d2*d3*d4))

#train_tree_classifier()
#train_tree_classifier()
train_nn_keras()
#clf = load('guillotree.joblib')
# text_representation = tree.export_text(clf)
# print(text_representation)
#print(clf.predict(X_test))
# predictions = clf.predict(X_test)

# ConfusionMatrixDisplay.from_predictions(y_test,predictions)
# plt.show()
# print(clf.score(X_test, y_test))