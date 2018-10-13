# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 23:44:47 2018

@author: Strong

x : 圖片
y : 標籤
train : 丟進 model裡的
test : 訓練 model 正確性的
"""
"""
http://scikit-image.org/docs/dev/api/skimage.transform.html
numpy load npy with dict:
    https://stackoverflow.com/questions/8361561/recover-dict-from-0-d-numpy-array
"""
#%%
import numpy as np
import json
import os
#from PIL import Image
from skimage import io, transform#, util
#%%
# input image dimensions
img_rows, img_cols = 28, 28
#%%
def LoadJSON(nameJSON):#, nameDict):
    #讀取
    try:
        with open(nameJSON, 'r') as inputfile:
            nameDict = json.load(inputfile)
    except FileNotFoundError:
        nameDict = dict() #{name:{filename:{"id":,"date":},},}
    return nameDict
#%%
def DumpJSON(nameJSON, nameDict):
    with open(nameJSON, 'w') as outfile:
        json.dump(nameDict, outfile)
    return

def LoadNPY(nameNPY, shape = None):
    try:
#        with np.load(nameNPY) as inputfile:
#            nameArr = inputfile.copy()
        nameArr = np.load(nameNPY)
    except FileNotFoundError:
        nameArr = np.zeros(shape)
    return nameArr

def SaveNPY(nameNPY, nameArr):
    np.save(nameNPY, nameArr)
    return
#%%
def MakeImgAndLabel(folder, typeNum, y_nameSpace, imgShape ):
    
    nameList = os.listdir(folder)
    
#    x_ = np.zeros((len(nameList),  numType))
    y_ = np.zeros((len(nameList)), dtype=np.int)
    
    tempList_x = list()
    for i, filename in enumerate(nameList):
        ### x
        img = io.imread(folder + filename)
        img = transform.resize(img, imgShape)
        img = (img * 255) // 1
        tempList_x.append(img)
        ### y
#        ##### 直接用編號
#        num = int(filename.split('_')[0].split('j')[1])
#        y_[i][num-1] = 1
#        ##### 檔名辨識
#        filenameLabel = filename.split('_')[0]
#        for numTemp, labelTemp in enumerate( y_nameSpace ):
#            if labelTemp == filenameLabel:
#                y_[i][numTemp] = 1
#                break
        
        num = int(filename.split('_')[0].split('j')[1])
        y_[i] = num-1
        
    x_ = np.array(tempList_x)
    
    return x_, y_

#%%
if __name__ == "__main__":
    
    databaseLoca = './hw5_dataset/'
    testFolder = 'i_testing/'
    trainFolder = 'j_training/'
    
    testImgnameList = os.listdir(databaseLoca + testFolder)
#    trainImgnameList = os.listdir(databaseLoca + trainFolder)
    
    # type number
    numType = len(testImgnameList)
    #out put dict
    outputDict = dict()
    # y array
#    y_test =  np.zeros((len(testImgnameList)), dtype=np.int)
#    y_train = np.zeros((len(trainImgnameList)), dtype=np.int)
    # define y type and 陣列位置
#    ##### 以讀取順序
#    y_nameSpace = list()
#    for filename in testImgnameList:
#        temp = filename.split('_')[0]
#        y_nameSpace.append(temp)
#    outputDict['y_nameSpace'] = np.array( y_nameSpace )
    ##### 以數字順序，可以直接用編號放array
    y_nameSpace = ['obj'+str(i) for i in range(1, 20+1)]
    outputDict['y_nameSpace'] = np.array( y_nameSpace )
    
    # make image(x), label(y) list
    ## test: 
#    tempList_x = list()
#    for i, filename in enumerate(testImgnameList):
#        ### x
#        img = io.imread(databaseLoca + testFolder + filename)
#        img = transform.resize(img, (img_rows, img_cols))
#        img *= 255
#        tempList_x.append(img)
#        ### y
#        ##### 直接用編號
#        num = int(filename.split('_')[0].split('j')[1])
#        y_test[i] = num - 1
#        
#    x_test = np.array(tempList_x)
    # 包成 function
    x_test, y_test = MakeImgAndLabel(databaseLoca + testFolder, 
                                     numType, 
                                     y_nameSpace, (img_rows, img_cols), 
                                     )
    outputDict['x_test'] = x_test
    outputDict['y_test'] = y_test
    
    ## train:
#    tempList_x = list()
#    for i, filename in enumerate(trainImgnameList):
#        ### x
#        img = io.imread(databaseLoca + trainFolder + filename)
#        img = transform.resize(img, (img_rows, img_cols))
#        img *= 255
#        tempList_x.append(img)
#        ### y
#        ##### 直接用編號
#        num = int(filename.split('_')[0].split('j')[1])
#        
#        y_train[i] = num - 1
        
#    x_train = np.array(tempList_x)
    # 包成 function
    x_train, y_train = MakeImgAndLabel(databaseLoca + trainFolder, 
                                     numType, 
                                     y_nameSpace, (img_rows, img_cols), 
                                     )
    outputDict['x_train'] = x_train
    outputDict['y_train'] = y_train
    
    #儲存
    SaveNPY('intput-.npy', outputDict)
    
    #讀取
    f = np.load('intput-.npy')
#    x_train, y_train, x_test, y_test = f['x_train'], f['y_train'], f['x_test'], f['y_test']
#    print(f.item()['y_test'])
    f = f.item()    
    st_x_train, st_y_train, st_x_test, st_y_test = f['x_train'], f['y_train'], f['x_test'], f['y_test']
#    f.close()

