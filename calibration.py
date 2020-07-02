# Created by Vlad Marascu for GDP ADD02 Group 2020
# 04/06/2020

# Calibration script- use same camera/resolution as drone and take a picture of a rectangular object (known area A[m]) from a known distance DC[m] to use in the main 'Shapes from webcam.py' script.

import cv2 
import numpy as np 
  
testimg=cv2.imread('images/calibration-type1,1m.png') # import picture used for calibration
# Calibration object has known area in meters, A_m, and DC (camera-object distance)
# 'emptyFunction' function defined to be used by the 'Variables' Trackbar
def emptyFunction(a):
  pass

# Define Threshold parameters (variables) and Trackbars for variation: area size filtering and 2 thresholds for Canny Edges
cv2.namedWindow("Variables")
cv2.resizeWindow("Variables",640,240)
cv2.createTrackbar("Thresh_1","Variables",172,255,emptyFunction) # Threshold parameter 1
cv2.createTrackbar("Thresh_2","Variables",30,255,emptyFunction) # Threshold parameter 2
cv2.createTrackbar("Area","Variables",7000,121500,emptyFunction) # Area filtering variable

# Apply Gaussian Blur Filter, (9,9) kernel to smooth the image and reduce noise  
testimgBlur=cv2.GaussianBlur(testimg,(9,9),1)
# Convert to Greyscale
testimgGray=cv2.cvtColor(testimgBlur,cv2.COLOR_BGR2GRAY)
# Set treshold values for Canny Edge Detector, using trackbars in the 'Variables' window  
thresh_1=cv2.getTrackbarPos("Thresh_1","Variables")
thresh_2=cv2.getTrackbarPos("Thresh_2","Variables")
# Apply Canny Edge Detection filter with variable thresholds, tested defaults are 172,140, can be varied
testimgCanny=cv2.Canny(testimgGray,thresh_1,thresh_2)
# Creating convolution kernel used for Dilation  
kernel = np.ones((5, 5))
# Dilating the Canny Edges in order to accentuate the shape, iterations=1 for most accurate object area
testimgDil = cv2.dilate(testimgCanny, kernel, iterations=1)

# Copy test image to testimgContour
testimgContour=testimg.copy()
# Extract contours from the Dilated image, testimgDil
contours, unused_var = cv2.findContours(testimgDil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)# simple-less no of points
# Draw extracted contours over the copied original image
cv2.drawContours(testimgContour,contours,-1,(255,0,255),3)

# Iterate over all contours(cnt)
for cnt in contours:
  # Calculate area of each contour in pixels
  area = cv2.contourArea(cnt)
  # Set an arbitraty minimum area, from Area trackbar in 'Variables' tab
  areamin=cv2.getTrackbarPos("Area","Variables")
  # Any contour with less than areamin will be ignored (reduces unwanted noise)
  if area > areamin:# and area<30000:
    # Compute the contour perimeter / length (True=only closed contours considered)
    perimeter=cv2.arcLength(cnt,True)
    # Approximate the type of shape of object, contour as input, resolution=0.01*length, True=only closed
    shape_approximation=cv2.approxPolyDP(cnt,0.01*perimeter,True) # contains a number of points, used in determining shapes: length(shape_approx), not needed for calibration script; rectangular object assumed
    # Calculates minimum upright bounding rectangle for the specific point set (object)- outputs start coordinates (top left) and x-y rectangle dimensions (w,h)
    x,y,w,h=cv2.boundingRect(shape_approximation)
    # Draw bounding box over object: input the start coords (x,y) and end coords (x+w,y+h)
    cv2.rectangle(testimgContour,(x,y),(x+w,y+h),(0,255,0),3)
    # Display area value in pixels
    cv2.putText(testimgContour, "Area: " + str(int(area)), (x, y + 40), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                        (0, 255, 0), 1)
    # Display original image with contours, bounding box and area in pixels
    cv2.imshow("Contours",testimgContour)

#DISTANCE CALCULATIONS

A_p = area # Area in pixels, test object
print("Test object area in pixels: "+ str(A_p))

# Known calibration object parameters [m]
A_m = 0.007056 # known test object area in [m^2]
DC = 0.15 # known set distance [m]

# Pixels per Meters ratio at known calibration distance
PPM = A_p / A_m # PPM at set initial distance DC
print("PPM at set DC: "+ str(PPM))

cv2.waitKey(0) 
#cv2.destroyAllWindows() 