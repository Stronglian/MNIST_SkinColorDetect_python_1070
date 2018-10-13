# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 18:06:19 2018
為了用floodFill 把 groundtruth 轉換成 uint8 再轉回
"""
import cv2
import numpy as np
import os
#from skimage import io, transform, util
np.set_printoptions(suppress=True)
#%%
class ImgGroundTrouthMAKE():
    """ one img first"""
    def __init__(self, imgForder, imgIndex = 0):
        #影像庫資訊
        self.__imgForder__ = imgForder
        self.imgNameList = os.listdir(imgForder)
        #先讀一張
        self.imgIndex = imgIndex
        self.ReadNewimg(imgIndex)
#        #共用參數
#        self.drawing = 0
        return
    def ReadNewimg(self, imgIndex = None ):
        """新的影像"""
        if not type(imgIndex) == type(0):#imgIndex == None or 
            imgIndex = self.imgIndex
        assert imgIndex < len(self.imgNameList)
        self.imgName = self.imgNameList[imgIndex]
        inputImg_cv = cv2.imread(self.__imgForder__ + self.imgName, 1)
        print('ReadNewimg', self.imgName)
        rows, cols, d = inputImg_cv.shape
        #縮放
        tempImg = inputImg_cv.copy()
        self.target_cols = 800
        self.target_rows = int((float(rows)/cols)*self.target_cols)
        self.resizeImg = cv2.resize(tempImg, (self.target_cols, self.target_rows))
        #專用白布
        self.drawImg = self.resizeImg.copy()
        self.drawArray = np.zeros((self.target_rows, self.target_cols, 1), dtype=np.uint8)
        return
    def MouseCall(self, event, x, y, flags, param):
        """ 給視窗呼叫 setMouseCallback 用
        左鍵:增加；右鍵:減少；中鍵:填滿"""
        floodMap = param
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.drawing == 0:
                self.drawing = 1
#            print('EVENT_LBUTTONDOWN')
        elif event == cv2.EVENT_RBUTTONDOWN:
            if self.drawing == 0:
                self.drawing = 2
#            print('EVENT_RBUTTONDOWN')
        elif event == cv2.EVENT_LBUTTONUP:
            if self.drawing == 1:
                self.drawing = 0
#            print ('EVENT_LBUTTONUP')
        elif event == cv2.EVENT_RBUTTONUP:
            if self.drawing == 2:
                self.drawing = 0
#            print ('EVENT_RBUTTONUP')
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing == 1:
                cv2.circle(self.drawArray, (x, y), self.brush_r, (255, 255, 255), -1)
            elif self.drawing == 2:
                cv2.circle(self.drawArray, (x, y), self.brush_r, (0, 0, 0), -1)
#            print('EVENT_MOUSEMOVE')
        elif event == cv2.EVENT_MBUTTONDOWN:
            if self.drawing == 0:
                cv2.floodFill(self.drawArray, floodMap, (x, y), 255)
#            print('EVENT_MBUTTONDOWN')
        return
    def DoHandWork_GroundTruthDrawing(self):
        """手繪皮膚"""
        #使用參數
        self.drawing = 0
        self.brush_r = 3
        showTF = True #切換共用
        tempFunc = lambda x : x
        state = 'r' #畫圖狀態
        floodMap =  np.zeros([self.target_rows+2, self.target_cols+2], dtype=np.uint8) #官方要求
        #設定視窗
        cv2.namedWindow(self.imgName,  cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(self.imgName, self.MouseCall, floodMap)
        #主要動作
        tempImg = self.drawImg
        while (1):#state != ord('q'):
            cv2.imshow(self.imgName, tempFunc(tempImg))
            state = cv2.waitKey(1) & 0xFF
            if state == ord('r'): #切換顯示
                tempImg = self.drawImg if showTF else self.drawArray
                showTF = False if showTF else True
                tempFunc = lambda x : x
            elif state == ord('e'): #合併顯示
                tempFunc = (lambda x : cv2.bitwise_and(self.drawImg, self.drawImg, mask=self.drawArray)) \
                if showTF else (lambda x : x)
                showTF = False if showTF else True
                tempImg = self.drawImg
            elif state == ord('w'): #調整筆刷 - 大
                 self.brush_r += 2
            elif state == ord('s'): #調整筆刷 - 小
                 self.brush_r -= 2
                 if self.brush_r <=0:
                     self.brush_r = 1
            elif state == ord('h'): #白布重開
                self.drawArray = np.zeros((self.target_rows, self.target_cols, 1), dtype=np.uint8)
                tempImg = self.drawArray
            elif state == ord('q') or state == 27: #ESC #DONE
                break
        
        #確認顯示
        cv2.imshow(self.imgName, self.resizeImg)
        cv2.waitKey(500)
        cv2.imshow(self.imgName, self.drawArray)
        cv2.waitKey(500)
        drawArrayT = self.drawArray[:,:,0].astype(np.uint8)
        temp = cv2.bitwise_and(self.resizeImg, self.resizeImg, mask=drawArrayT)
        cv2.imshow(self.imgName, temp)
        cv2.waitKey(500)
        #cv2.waitKey(500)
#        cv2.destroyAllWindows()
        #儲存確認
        userReson = input('reDo?[Y/N][N]')
        if userReson in ['Y','y']:
            return self.DoHandWork_GroundTruthDrawing()
        #轉換輸出
        self.drawArray[self.drawArray == 255] = 1
        cv2.destroyAllWindows()
        return self.resizeImg, self.drawArray
#%%
if __name__ == "__main__":
    
    imgForder = '../img_org/'
#    imgNameList = os.listdir(imgForder)
    test = ImgGroundTrouthMAKE(imgForder)
    x_img, y_groundtruth = test.DoHandWork_GroundTruthDrawing()
