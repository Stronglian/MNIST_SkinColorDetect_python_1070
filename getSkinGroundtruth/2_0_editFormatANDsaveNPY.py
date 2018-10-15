# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 21:37:27 2018
refer:
    import: (有空再讀)
        https://medium.com/pyladies-taiwan/python-%E7%9A%84-import-%E9%99%B7%E9%98%B1-3538e74f57e3
"""
import os
import numpy as np
from c1_1_with1_0ButClass import ImgGroundTrouthMAKE

def FindIndex(inputValue, inputList):
    for i, value in enumerate(inputList):
        if value == inputValue:
            outputIndex = i
            break
    return outputIndex
#if __name__ == "__main__":

#共同參數
dataNPY = 'dataOrg.npy' #存在哪
imgForder = '../img_org/' #相片在哪
#讀取過去與否?
if dataNPY in os.listdir('./') :#and False:
    dataDict = np.load(dataNPY).item()
else:
    dataDict = {'x_':[],'y_':[],'namespace':[]}
#讀取 
test = ImgGroundTrouthMAKE(imgForder)
curectImgName = test.imgName

while (1):
    print('test', curectImgName)
    if curectImgName in dataDict['namespace']:
        userRespon_redo = input(curectImgName+', 已存在，是否再處理一次[Y/N][N]')
        if userRespon_redo in ['Y', 'y']:
            #讀取舊資料，影像與groundTruth
            tempIndex = FindIndex(curectImgName, dataDict['namespace'])
            test.drawImg = dataDict['x_'][tempIndex].copy() #理論上已經有了
            tempArr = dataDict['y_'][tempIndex].copy()
            tempArr[dataDict['y_'][tempIndex]==1] = 255
            test.drawArray = tempArr
        else:
            #換下一張
            test.imgIndex += 1 
            curectImgName = test.ReadNewImg()
            if curectImgName == 'DONE':
                print(imgForder, 'is OVER.', 'END off it')
                break
            continue
    #作畫
    print('do', curectImgName)
    x_img, y_ground= test.DoHandWork_GroundTruthDrawing()
    #儲存與否
    userRespon_save = input('確認儲存?[Y/N][Y]')
    if userRespon_save in ['N', 'n']:
        print(curectImgName, 'NO SAVE')
    else:
        #儲存
        dataDict['x_'].append(x_img.copy())
        dataDict['y_'].append(y_ground.copy())
        dataDict['namespace'].append(curectImgName)
        print('SAVE', curectImgName)
    #繼續與否
    userRespon_next = input('下一張?[Y/N][Y]')
    if userRespon_next in ['N', 'n']:
        print('BYE')
        break
    else:
        #換下一張
        test.imgIndex += 1 
        curectImgName = test.ReadNewImg()
        if curectImgName == 'DONE':
            print(imgForder, 'is OVER.', 'END off it')
            break


#轉存 NPY
np.save(dataNPY, dataDict)
print(dataNPY, 'SAVED')









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
##轉存 NPY
#np.save(dataNPY, dataDict)