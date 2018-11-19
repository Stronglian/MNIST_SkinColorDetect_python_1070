# -*- coding: utf-8 -*-
"""
@author: StrongPria
Python-图像加噪实现（Gaussian noise+salt and pepper noise）:
    https://blog.csdn.net/zh_jessica/article/details/77967650
skimage.util.random_noise:
    http://scikit-image.org/docs/dev/api/skimage.util.html#skimage.util.random_noise
"""
import numpy as np
import cv2
from skimage import util

imgName = "DSC_0875.JPG"

inputImg_cv = cv2.imread(imgName)
inputImg_noise = util.random_noise(inputImg_cv, mode='gaussian', seed=None, clip=True)
inputImg_noise *= 255
inputImg_noise.astype("int")

cv2.imwrite(imgName.split('.')[0]+"_noise"+"."+imgName.split('.')[-1], inputImg_noise)