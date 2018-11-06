# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 19:30:44 2018
#其實應該用計數而非append，之後再改，之後再改
memory 空間占用問題 要解決
 - 切分打到一半，先註解
"""
import numpy as np
import os, sys
from shutil import copyfile
from c2_1_combine2NewNPY import LoadNPY2Dict, FormatCheck
#%%
def GetNameListAndSaveDelDict(outputDict, outputNPY):
    listNameList = outputDict["namespace"]
    np.save(outputNPY, outputDict)
    del outputDict
    return listNameList
def GetPureName(orgName, nameIndex = 0):
    # .rsplit(".", 1)[0] -> npy
    # nameIndex = 0, 名字； = -1 ，編號。
    return orgName.rsplit(".", 1)[0].rsplit("_", 1)[nameIndex]
#%%
#if __name__ == "__main__":
#共同參數
outputNPYLocal = "./"
dataNPY = "dataOrg.npy" #要轉換的
#outputNPY = "output_"+dataNPY.rsplit(".",1)[0]+"_fullCut.npy"
outputNPY = "output_"+dataNPY.rsplit(".",1)[0]+"_easyCut.npy"

#boolSplitForder = False
#intDataInOneNPY = 5
#intCountOutput = 0
#%%
#讀取 data
dataDict = LoadNPY2Dict(dataNPY)
FormatCheck(dataDict)
#讀取過去或是新建檔案
while(1):
    if (outputNPY in os.listdir(outputNPYLocal)) \
    or False: #判斷有編號的切片用
        userRespon = input(outputNPY + " is exist, Do you read this?[Y/N][Y]")
        if userRespon in ["N", "n"]:
            outputNPY = input("Input a new file name:(EXIT to exit)")
            if outputNPY == "EXIT":
                print("BYE")
#                os._exit(0)#會殘餘空間
                sys.exit()
            #命名規則
            if len(outputNPY.split(".")) == 1:
                outputNPY += ".npy"
            elif outputNPY.rsplit(".",1)[-1] not in ["npy", "NPY"]:
                outputNPY += ".npy"
            continue
        outputDict = np.load(outputNPYLocal + outputNPY).item()
        break
#    elif GetPureName(outputNPY) in [GetNameListAndSaveDelDict(tmp) for tmp in os.listdir(outputNPYLocal)]:
#        intCountOutput = [GetNameListAndSaveDelDict(tmp) for tmp in os.listdir(outputNPYLocal)].count(GetPureName(outputNPY))
    else:
        print("Create new dcit.", outputNPY)
        outputDict = {}
        for indexName in ["x_","y_","namespace", "indexMax"]:
            outputDict[indexName] = []
        break
nameList = outputDict["namespace"]
np.save(outputNPYLocal + outputNPY, outputDict)
del outputDict
#%%
rows_patch   = 20
cols_patch   = 20
judgingRatio = 0.6
judgingLine  = rows_patch * cols_patch * judgingRatio

for n_index, imgName in enumerate(dataDict["namespace"]):
    print("tset", imgName, 'IN', outputNPY)
    if imgName in nameList:
        print(imgName, "exist")
        continue
    #取現有資訊
    rows_img, cols_img, d = dataDict["x_"][n_index].shape
    imgOrg = groundTruth = dataDict["x_"][n_index]
    groundTruth = dataDict["y_"][n_index]
    #儲存
    x_newPatch = []
    y_newPatch = []
    #其實應該用計數而非append，之後再改
    patchCount = 0
#    for y in range(0, rows_img): # fullCut
#        for x in range(0, cols_img):
    for y in range(0, rows_img, rows_patch): # easyCut
        for x in range(0, cols_img, cols_patch):
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
    #重新讀檔
    outputDict = np.load(outputNPYLocal + outputNPY).item()
    #儲存紀錄
    outputDict["x_"].extend(x_newPatch)
    outputDict["y_"].extend(y_newPatch)
    outputDict["namespace"].append(imgName)
    ## 各自的編號
    outputDict["indexMax"].append(patchCount if len(outputDict["indexMax"])==0 else outputDict["indexMax"][-1]+patchCount)
    print(imgName, "Done")
#    break
#轉存 NPY
    np.save(outputNPYLocal + outputNPY, outputDict)
    #
    nameList = outputDict["namespace"]
    del outputDict
    print("==")
#%%

print("Copy to", copyfile(outputNPYLocal + outputNPY, "./DONE/" + outputNPY)) #完成就備份
#%%註解
##共同參數
#dataNPY = "dataForInput.npy"
##讀取過去與否?
#if dataNPY in os.listdir("./") :#and False:
#    dataDict = np.load(dataNPY).item()
#else:
#    dataDict = {"x_":[],"y_":[],"namespace":[], "indexMax":[]}
#    """
#    x_: patch, size*size
#    y_: 該patch分為何，[ no, skin ]
#    namesapce:  imgName0,  imgName1, ...
#    indexMax:  indexMax0, indexMax1, ...
#    """
##切分
#
##設置 ground truth
#