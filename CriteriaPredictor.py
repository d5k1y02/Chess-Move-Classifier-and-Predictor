# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 16:29:06 2021
This code is primarily based on the code from https://github.com/pytorch/tutorials/blob/master/beginner_source/basics/data_tutorial.py
@author: Desmond
"""
import os
import pandas as pd
from torchvision.io import read_image
from torch.utils.data import Dataset
import torch 
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import tensorflow as tf
from ast import literal_eval
import numpy as np
import matplotlib.pyplot as plt
from torchvision.transforms import ToTensor, Lambda

# Hyper-parameters
input_size = 128
hidden_size = 60
num_classes = 8
num_epochs = 10
batch_size = 24
learning_rate = 0.001

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
arr_csv_train = "chess_labels_train.csv"
arr_csv_test = "chess_labels_test.csv"
pos_dir = "./"

def read_position(position):
    file = open(position, "r")
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

class ChessDataset(Dataset):
    def __init__(self, annotations_file, pos_dir, transform=None, target_transform=None):
        self.pos_labels = pd.read_csv(annotations_file)
        self.pos_dir = pos_dir
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.pos_labels)

    def __getitem__(self, idx):
        pos_path = os.path.join(self.pos_dir, self.pos_labels.iloc[idx, 0])
        position = read_position(pos_path)
        label = self.pos_labels.iloc[idx, 1]
        if self.transform:
            position = self.transform(position)
        if self.target_transform:
            label = self.target_transform(label)
        sample = position, label
        return sample

# dataset


train_dataset = ChessDataset(arr_csv_train, pos_dir, transforms.ToTensor(), Lambda(lambda y: torch.zeros(8, dtype=torch.float).scatter_(0, torch.tensor(y), value=1)))

test_dataset = ChessDataset(arr_csv_test, pos_dir, transforms.ToTensor(), Lambda(lambda y: torch.zeros(8, dtype=torch.float).scatter_(0, torch.tensor(y), value=1)))


# Data loader
train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
                                           batch_size=batch_size, 
                                           shuffle=True)

test_loader = torch.utils.data.DataLoader(dataset=test_dataset,
                                          batch_size=batch_size, 
                                          shuffle=False)

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size) 
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)  
    
    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out
    
model_NN = NeuralNet(input_size, hidden_size, num_classes).to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model_NN.parameters(), lr=learning_rate, weight_decay=0.00001)



# Train the model_NN
total_step = len(train_loader)

for epoch in range(num_epochs):
    for i, (positions, labels) in enumerate(train_loader):  
        # Move tensors to the configured device
        positions = positions.reshape(-1, 8*8*2).to(device)
        labels = labels.to(device)
        
        # Forward pass
        outputs = model_NN(positions.float())
        loss = criterion(outputs, torch.max(labels, 1)[1])
        
        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if (i+1) % 100 == 0:
            print ('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}' 
                   .format(epoch+1, num_epochs, i+1, total_step, loss.item()))
            
# Test the model_NN
# In test phase, we don't need to compute gradients (for memory efficiency)
with torch.no_grad():
    correct = 0
    total = 0
    for positions, labels in test_loader:
        positions = positions.reshape(-1, 8*8*2).to(device)
        labels = labels.to(device)
        outputs = model_NN(positions.float())
        _, predicted = torch.max(outputs.data, 0)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    print('Accuracy of the network: {} %'.format(100 * correct / total))

# Save the model_NN checkpoint
torch.save(model_NN.state_dict(), 'model_NN.ckpt')
