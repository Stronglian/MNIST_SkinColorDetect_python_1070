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

#if __name__ == "__main__":
#讀取 
imgForder = '../img_org/'
#test = ImgGroundTrouthMAKE(imgForder)
#x_img, y_temp= test.DoHandWork_GroundTruthDrawing()
#共同參數
dataNPY = 'data.npy'
#讀取過去與否?
if dataNPY in os.listdir('./') :#and False:
    dataDict = np.load(dataNPY).item()
else:
    dataDict = {'x_':[],'y_':[],'namespace':[], 'indexMax':[]}
    """
    x_: patch, size*size
    y_: 該patch分為何，[skin, no]    
    namesapce:  imgName0,  imgName1, ...
    indexMax:  indexMax0, indexMax1, ...
    """
#切分

#設置 ground truth

#轉存 NPY
np.save(dataNPY, dataDict)