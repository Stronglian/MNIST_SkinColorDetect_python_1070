# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 03:02:43 2018

@author: Strong

Save and Load Your Keras Deep Learning Models:
    https://machinelearningmastery.com/save-load-keras-deep-learning-models/
"""

import keras
import numpy as np 
from keras import backend as K

img_rows, img_cols = 28, 28
num_classes = 20

# 檔案讀取
f = np.load('intput-.npy').item()
#f = f.item()
x_train, y_train, x_test, y_test = f['x_train'], f['y_train'], f['x_test'], f['y_test']

# 檔案格式
if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')
# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

### load json and create model # from website
##json_file = open('model.json', 'r')
##loaded_model_json = json_file.read()
##json_file.close()
##loaded_model = keras.models.model_from_json(loaded_model_json)
### load weights into new model
##loaded_model.load_weights("model.h5")
loaded_model = keras.models.load_model('my_model.h5')
print("Loaded model from disk")
 
# evaluate loaded model on test data
loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
score = loaded_model.evaluate(x_test, y_test, verbose=0)
print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
