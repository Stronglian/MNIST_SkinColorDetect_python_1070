# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 23:44:47 2018

@author: Strong
"""

import numpy as np
import json
from keras.datasets import mnist

def LoadJSON(nameJSON):#, nameDict):
    #讀取
    try:
        with open(nameJSON, 'r') as inputfile:
            nameDict = json.load(inputfile)
    except FileNotFoundError:
        nameDict = dict() #{name:{filename:{"id":,"date":},},}
    return nameDict

def DumpJSON(nameJSON, nameDict):
    with open(nameJSON, 'w') as outfile:
        json.dump(nameDict, outfile)
    return

def LoadNPY(nameNPY, shape = None):
    try:
        nameArr = np.load(nameNPY)
    except FileNotFoundError:
        nameArr = np.zeros(shape)
    return nameArr

def SaveNPY(nameNPY, nameArr):
    np.save(nameNPY, nameArr)
    return

if __name__ == "__main__":
    
#    arr = LoadNPY('./mnist.npz')
#    dic = LoadJSON('C:/Users/Strong/.keras/keras.json')
    
#    print(np.array(arr))
#    print(dic)
    
    (x_train, y_train), (x_test, y_test) = mnist.load_data()