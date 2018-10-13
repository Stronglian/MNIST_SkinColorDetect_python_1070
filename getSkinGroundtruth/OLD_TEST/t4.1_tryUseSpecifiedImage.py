# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 03:02:43 2018

@author: Strong

https://stackoverflow.com/questions/47907409/how-to-use-the-created-cnn-model-with-new-data-in-keras
http://scikit-image.org/docs/dev/api/skimage.color.html#skimage.color.rgb2gray
"""

import keras
#from keras import backend as K

import numpy as np 
from skimage import io, transform, color
import os
#%%
img_rows, img_cols = 28, 28
num_classes = 20
#%%
def LittleBlock(inputImg, y, x, rows, cols):
#    print(x, y)
    if   (y+1 >= rows) and (x+1 >= cols):
        return 0    
    elif (y+1 >= rows):
        if (inputImg[y][x+1] >= 0.9):
#            inputImg[y][x] = 0
            return 0
    elif (x+1 >= cols):
       if (inputImg[y+1][x] >= 0.9):
#            inputImg[y][x] = 0        
            return 0   
    elif (inputImg[y+1][x] >= 0.9) and (inputImg[y][x+1] >= 0.9):
#        inputImg[y][x] = 0
        return 0
#    return inputImg
    return inputImg[y][x+1]
def WhiteBG2Black(inputImg):
    outputImg = np.zeros(inputImg.shape)
    rows, cols = inputImg.shape[:2]
    for i in range(rows):
        for j in range(cols):
            outputImg[i][j] = LittleBlock(inputImg, i, j, rows, cols)
#            if outputImg[i][j] == 0:
    
    return outputImg
#%%
## 檔案讀取
#f = np.load('intput-.npy').item()
##f = f.item()
#x_train, y_train, x_test, y_test = f['x_train'], f['y_train'], f['x_test'], f['y_test']
#
## 檔案格式
#if K.image_data_format() == 'channels_first':
#    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
#    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
#    input_shape = (1, img_rows, img_cols)
#else:
#    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
#    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
#    input_shape = (img_rows, img_cols, 1)
#
#x_train = x_train.astype('float32')
#x_test = x_test.astype('float32')
#x_train /= 255
#x_test /= 255
#print('x_train shape:', x_train.shape)
#print(x_train.shape[0], 'train samples')
#print(x_test.shape[0], 'test samples')
## convert class vectors to binary class matrices
#y_train = keras.utils.to_categorical(y_train, num_classes)
#y_test = keras.utils.to_categorical(y_test, num_classes)

loaded_model = keras.models.load_model('my_model.h5')
print("Loaded model from disk")
 
## evaluate loaded model on test data
#loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
#score = loaded_model.evaluate(x_test, y_test, verbose=0)
#print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
#%%
#資料夾
inputFolder = './img/'
editFolder = './img_edit/'
imgFilename_list = os.listdir(inputFolder)
#預計內容量
amount_img = len(imgFilename_list)#2
#檔案存取空間
arr = np.zeros((amount_img, img_rows, img_cols))

##讀取原本的
#img = io.imread('./hw5_dataset/i_testing/obj17__21.bmp')
#img = transform.resize(img, (img_rows, img_cols))
##arr = np.array()
##檔案格式
#arr[0] = img.copy()
#%%
for i, filename in enumerate(imgFilename_list):
    img = io.imread(inputFolder + filename)
    if len(img.shape) >= 3:
        #轉灰階
        img = color.rgb2grey(img)#.astype('float32')
        io.imsave(editFolder + filename.rsplit('.',1)[0] + '_toGrey' + '.bmp', img)
    if img[0][0] > 0.9:
        #把白底轉黑底
        img = WhiteBG2Black(img)
        io.imsave(editFolder + filename.rsplit('.',1)[0] + '_toGreyBGtoB' + '.bmp', img)
#    img /= 255 #讀進來就是 float
    #大小轉換
    img = transform.resize(img, (img_rows, img_cols))
    io.imsave(editFolder + filename.rsplit('.',1)[0] + '_toGreyBGtoBResize' + '.bmp', img)
    #放入陣列
    arr[i] = img.copy()
   #%% 
#送入預測與預先轉換
arr = transform.resize(arr, (amount_img, img_rows, img_cols, 1))
pred = loaded_model.predict(arr)

for j, filename in enumerate(imgFilename_list):
    max_num = 0
    max_i = 0
    for i, num in enumerate(pred[j]):
        if num > max_num:
            max_num = num
            max_i = i
    print(filename)
    print('-', max_i+1, ':', max_num) # 檔案編號是從 1 開始