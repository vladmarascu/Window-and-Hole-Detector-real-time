# Created by Vlad Marascu for GDP ADD02 Group 2020
# 04/06/2020

import cv2 
import numpy as np 
import calibration
  
img=cv2.imread('12.jpg') # Actual object that has unknown A1_m
# Distance from camera to object is DC1 - known from ultrasound sensor


def empty(a):
  pass

cv2.namedWindow('Parameters')
cv2.resizeWindow('Parameters',640,240)
cv2.createTrackbar("Threshold 1",'Parameters',172,255,empty)
cv2.createTrackbar("Threshold 2",'Parameters',30,255,empty)
cv2.createTrackbar("Area",'Parameters',7000,30000,empty)

  
imgBlur=cv2.GaussianBlur(img,(7,7),1)

imgGray=cv2.cvtColor(imgBlur,cv2.COLOR_BGR2GRAY)
  
threshold1=cv2.getTrackbarPos("Threshold 1","Parameters")
threshold2=cv2.getTrackbarPos("Threshold 2","Parameters")
imgCanny=cv2.Canny(imgGray,threshold1,threshold2)
  
kernel = np.ones((5, 5))
imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

imgContour=img.copy()
contours, hierarchy = cv2.findContours(imgDil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)# simple-less no of points
cv2.drawContours(imgContour,contours,-1,(255,0,255),3)

for cnt in contours:
  area1 = cv2.contourArea(cnt)
  areamin=cv2.getTrackbarPos("Area","Parameters")

  if area1 > areamin:
    peri=cv2.arcLength(cnt,True)
    approx=cv2.approxPolyDP(cnt,0.02*peri,True)
    x,y,w,h=cv2.boundingRect(approx)
    cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),3) # bounding box
    cv2.putText(imgContour, "Area: " + str(int(area1)), (x, y + 40), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                        (0, 255, 0), 1)
    cv2.imshow("Contours",imgContour)

#DISTANCE CALCULATIONS

DC1=0.12 # variable distance measured by sensor [m]
PPM1=calibration.PPM*calibration.DC/DC1
print("PPM at actual distance DC1: "+ str(PPM1))

A_p1=area1 # Area in pixels, actual object
print("Actual object area in pixels: "+ str(A_p1))

A_m1 = A_p1 / PPM1 # Actual object area [m]
print("Actual object area in meters: "+ str(A_m1))

cv2.waitKey(0) 
cv2.destroyAllWindows() 