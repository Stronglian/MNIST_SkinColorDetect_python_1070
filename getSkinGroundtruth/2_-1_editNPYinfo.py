# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 01:49:52 2018

@author: Strong
"""
import numpy as np

dataNPY = 'dataOrg.npy' #存在哪

dataDict = np.load(dataNPY).item()

#轉存 NPY
np.save(dataNPY, dataDict)