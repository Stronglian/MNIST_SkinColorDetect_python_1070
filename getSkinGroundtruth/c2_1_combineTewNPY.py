# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 18:16:15 2018
"""
import numpy as np
import os

def LoadNPY2Var(dataNPY, folderLocal = './'):
    assert dataNPY in os.listdir(folderLocal) #and False:
    dataDict = np.load(dataNPY).item()
    return dataDict
def FormatCheck(dataDict):
    for tmp in ['x_', 'y_', 'namespace']:
        if tmp not in dataDict.keys():
            print(tmp, 'not in Dict')
            raise AssertionError
    countList = np.array([len(dataDict[tmp]) for tmp in dataDict.keys() ])
#    print(countList == countList[0])
    if not all(countList == countList[0]):
        print('數量不符合')
        raise AssertionError
    return

if __name__ == "__main__":
    #公用
    varList = ['x_', 'y_', 'namespace']
    #兩個數組
    dataNPY_0 = 'dataOrg.npy' #存在哪
    dataNPY_1 = 'dataOrg - CO.npy' #存在哪
    #讀取
    dataDcit_0 = LoadNPY2Var(dataNPY_0)
    dataDcit_1 = LoadNPY2Var(dataNPY_1)
    #確認數量
    FormatCheck(dataDcit_0)
    FormatCheck(dataDcit_1)
    #獲取主資訊，確認比對
    for i in range(len(dataDcit_1['namespace'])):
        imgName = dataDcit_1['namespace'][i]
        if imgName in dataDcit_0['namespace']:
            print(imgName, "IN, continue")
            continue
            #或是做 兩者比對
        else:
            dataDcit_0['x_'].append(dataDcit_1['x_'][i].copy())
            dataDcit_0['y_'].append(dataDcit_1['y_'][i].copy())
            dataDcit_0['namespace'].append(dataDcit_1['namespace'][i])
    #儲存
    np.save(dataNPY_0, dataDcit_0)
    print(dataNPY_0, 'SAVED')
    #更名
    os.rename(dataNPY_1, "DONE_" + dataNPY_1)
    print(dataNPY_1, "rename to", "DONE_" + dataNPY_1)