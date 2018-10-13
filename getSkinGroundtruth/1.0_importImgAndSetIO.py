# -*- coding: utf-8 -*-
"""
reference:
    cv2.read:
        https://blog.gtwang.org/programming/opencv-basic-image-read-and-write-tutorial/
    cv2.resize():
        https://blog.csdn.net/JNingWei/article/details/78218837
    cv2.setMouseCallback():
        https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_mouse_handling/py_mouse_handling.html
        https://www.programcreek.com/python/example/70462/cv2.setMouseCallback
        https://blog.csdn.net/Qton_CSDN/article/details/70193884
        event:
            https://docs.opencv.org/3.1.0/d7/dfc/group__highgui.html#ga927593befdddc7e7013602bca9b079b0
    class:
        
"""
import cv2
import numpy as np
import os
#from skimage import io, transform, util

np.set_printoptions(suppress=True)
#%%
def MouseCall(event, x, y, flags, param):
    global drawing, drawArray
#    drawTable = param
    print(drawing)
    if event == cv2.EVENT_LBUTTONDOWN:
        if drawing == 0:
            drawing = 1
        print('EVENT_LBUTTONDOWN')
    elif event == cv2.EVENT_LBUTTONUP:
        if drawing == 1:
            drawing = 0
        print ('EVENT_LBUTTONUP')
    elif event == cv2.EVENT_RBUTTONDOWN:
        if drawing == 0:
            drawing = 2
        print('EVENT_RBUTTONDOWN')
    elif event == cv2.EVENT_RBUTTONUP:
        if drawing == 2:
            drawing = 0
        print ('EVENT_RBUTTONUP')
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == 1:
            drawing = 1
#            drawArray[y, x] = 1
            cv2.circle(drawArray, (x, y),brush_r , (255, 255, 255), -1) #-1:FILL
#            cv2.circle(drawArray, (x, y),brush_r , (1, 1, 1), -1) #-1:FILL
        elif drawing == 2:
#            drawArray[y, x] = 0
            cv2.circle(drawArray, (x, y),brush_r , (0, 0, 0), -1)
        print('EVENT_MOUSEMOVE')
    elif event == cv2.EVENT_MBUTTONDOWN:
        if drawing == 0:
            cv2.floodFill(drawArray, floodMap, (x, y), 255)
#            cv2.floodFill(drawArray, floodMap, (x, y), 1)
        print('EVENT_MBUTTONDOWN')
    return
#%%
imgForder = '../img_org/'

imgNameList = os.listdir(imgForder)

#讀取
#inputImg_io = io.imread(imgForder + imgNameList[0]) #完全與 cv  顛倒
inputImgName = imgNameList[0]
inputImg_cv = cv2.imread(imgForder + inputImgName, 1)
rows, cols, d = inputImg_cv.shape

#%%
#縮放
tempImg = inputImg_cv.copy()
target_cols = 800
target_rows = int((float(rows)/cols)*target_cols)
resizeImg = cv2.resize(tempImg, (target_cols, target_rows))
#%%
#視窗設定
#開白布
drawImg = resizeImg.copy()
drawArray = np.zeros((target_rows, target_cols, 1), dtype=np.uint8)
floodMap =  np.zeros([target_rows+2, target_cols+2], dtype=np.uint8) #官方要求
#使用參數
drawing = 0 # 0:沒事；1:+；2:-
#util.view_as_windows(inputImg_io, 1) #不是指視窗顯示
cv2.namedWindow(inputImgName,  cv2.WINDOW_NORMAL)
cv2.setMouseCallback(inputImgName, MouseCall)
#cv2.setMouseCallback(inputImgName,  mouseFunction)
#cv2.imshow(inputImgName, tempImg)
#%%
#切換
state = 'r'
tempImg = drawImg
brush_r = 3
showTF = True
tempFunc = lambda x : x
while (1):#state != 'q':
    cv2.imshow(inputImgName, tempFunc(tempImg))
#    print(drawing)
    state = cv2.waitKey(1) & 0xFF
    if state == ord('f'): #切換顯示
        if showTF:
            tempImg = drawImg
            showTF = False
        else:
            tempImg = drawArray
            showTF = True
        tempFunc = lambda x : x
        #cv2.imshow(inputImgName, tempImg)
#        tempImg = drawImg
#    elif state == ord('d'):
##        cv2.imshow(inputImgName, drawArray)
#        tempImg = drawArray
    elif state == ord('e'): #合併顯示
        tempFunc = lambda x : cv2.bitwise_and(drawImg,drawImg, mask=drawArray)
#        drawArrayT = drawArray[:,:,0]#.astype(np.uint8)
#        tempImg = cv2.bitwise_and(drawImg,drawImg, mask=drawArrayT)
    elif state == ord('h'): #白布重開
        drawArray = np.zeros((target_rows, target_cols, 1), dtype=np.uint8)
    elif state == ord('w'): #調大筆刷
         brush_r += 2
    elif state == ord('s'): #調小筆刷
         brush_r -= 2
         if brush_r <=0:
             brush_r = 1
     
    elif state == ord('q') or state == 27: #ESC
        break

#%%
#確認顯示
cv2.imshow(inputImgName, resizeImg)
cv2.waitKey(500)
drawArrayT = drawArray[:,:,0]#.astype(np.uint8)
temp = cv2.bitwise_and(drawImg,drawImg, mask=drawArrayT)
cv2.imshow(inputImgName, temp)
#cv2.imshow(inputImgName, tempImg)
cv2.waitKey(500)
        
    

#cv2.waitKey(500)
cv2.destroyAllWindows()
