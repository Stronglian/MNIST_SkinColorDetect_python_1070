# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 19:30:44 2018

"""
import numpy as np
import os
from c2_1_combineTewNPY import LoadNPY2Var, FormatCheck
#%%


#%%
#if __name__ == "__main__":
#共同參數
dataNPY = "dataOrg.npy" #要轉換的
outputNPY = "output0_all.npy"
#讀取
dataDict = LoadNPY2Var(dataNPY)
FormatCheck(dataDict)
#讀取過去
while(1):
    if outputNPY in os.listdir('./') :#and False:
        userRespon = input(outputNPY+" is exist, Do you read this?[Y/N][Y]")
        if userRespon in ['N', 'n']:
            outputNPY = input('Input a new file name:')
            #命名規則
            if len(outputNPY.split('.')) == 1:
                outputNPY += '.npy'
            elif outputNPY.split('.')[-1] not in ['.npy', '.NPY']:
                outputNPY += '.npy'
            continue
        outputDict = np.load(outputNPY).item()
        break
    else:
        print('Create new dcit')
        outputDict = {}
        for indexName in ['x_','y_','namespace', 'indexMax']:
            outputDict[indexName] = []
        break
#%%
rows_patch   = 20
cols_patch   = 20
judgingRatio = 0.6
judgingLine  = rows_patch * cols_patch * judgingRatio

for n_index, imgName in enumerate(dataDict['namespace']):
    print('tset', imgName)
    if imgName in outputDict['namespace']:
        print(imgName, "exist")
        continue
    #取現有資訊
    rows_img, cols_img, d = dataDict['x_'][n_index].shape
    imgOrg = groundTruth = dataDict['x_'][n_index]
    groundTruth = dataDict['y_'][n_index]
    #儲存
    x_newPatch = []
    y_newPatch = []
    #其實應該用計數而非append
    patchCount = 0
    for y in range(0, rows_img):#, rows_patch): #):#
        for x in range(0, cols_img):#, cols_patch):
            patchTmp_Img = imgOrg[y:y+rows_patch, x:x+cols_patch].copy()
            patchTmp_Truth = groundTruth[y:y+rows_patch, x:x+cols_patch].copy()
            x_newPatch.append(patchTmp_Img)
#            y_newPatch.append([[] for i in range(2)])
            if patchTmp_Truth.sum() > judgingLine:
                #屬於膚色
                y_newPatch.append([ 0, 1])
            else:
                y_newPatch.append([ 1, 0])
            patchCount +=1
#            break
#        break
    #儲存紀錄
    outputDict['x_'].append(x_newPatch)
    outputDict['y_'].append(y_newPatch)
    outputDict['namespace'].append(imgName)
    outputDict['indexMax'].append(patchCount if len(outputDict['indexMax'])==0 else outputDict['indexMax'][-1]+patchCount)
    print(imgName, "Done")
#    break

#轉存 NPY
np.save(outputNPY, outputDict)
#%%註解
##共同參數
#dataNPY = 'dataForInput.npy'
##讀取過去與否?
#if dataNPY in os.listdir('./') :#and False:
#    dataDict = np.load(dataNPY).item()
#else:
#    dataDict = {'x_':[],'y_':[],'namespace':[], 'indexMax':[]}
#    """
#    x_: patch, size*size
#    y_: 該patch分為何，[skin, no]    
#    namesapce:  imgName0,  imgName1, ...
#    indexMax:  indexMax0, indexMax1, ...
#    """
##切分
#
##設置 ground truth
#
