# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 11:20:00 2018

純粹讀取用
"""

import numpy as np
import os
import cv2
#%% 
#NPY在哪
npyLocal = './imgPackage/' 
dataNPY = 'dataImg-1015.npy' #存在哪
##相片在哪個資料夾 與 該資料夾在哪
#imgForderLocal = './imgPackage/'
#imgForder = 'dataImg-1015/' 
#確認資料存在
if dataNPY not in os.listdir(npyLocal) :
    raise IOError(dataNPY+" not in "+npyLocal)
else:
    dataDict = np.load(npyLocal + dataNPY).item()
    dataAmount = len(dataDict['x_'])
#%% 
maskFunc = lambda drawImg, drawArray : cv2.bitwise_and(drawImg, drawImg, mask=drawArray)
for i in range(dataAmount):
    #讀取
    imgName = dataDict['namespace'][i]
    orgImg = dataDict['x_'][i]
    groundtruth = dataDict['y_'][i].copy()*255
    #顯示
    cv2.imshow("Org_", orgImg)
    cv2.imshow("Mask_", groundtruth)
    cv2.imshow("_withMask", maskFunc(orgImg, groundtruth))
    
    #離開
    state = cv2.waitKey(0) & 0xFF
    if state == ord('q'):
        break
    
        
    cv2.destroyAllWindows()
cv2.destroyAllWindows()
    
    