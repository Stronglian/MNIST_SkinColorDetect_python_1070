# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 01:49:52 2018

@author: Strong
"""
import numpy as np

dataNPY = './imgPackage/data_img_1015.npy' #存在哪

dataDict = np.load(dataNPY).item()

#刪除 指定 index
#index_assign = 6
#dataDict['x_'].pop(index_assign)
#dataDict['y_'].pop(index_assign)
#dataDict['namespace'].pop(index_assign)

##轉存 NPY
np.save(dataNPY, dataDict)