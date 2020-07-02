# Created by Vlad Marascu for GDP ADD02 Group 2020
# 04/06/2020

# Main entrance points detection script: uses the calibration.py script and returns the detected object types (windows/holes), the area in pixels and the computed area in meters.

import cv2
import calibration # load calibration.py from the same folder first to obtain PPM at a set distance
import numpy as np
 
# Initialize videostream 
#Frame width and height can be modified depending on need with cap.set function

# Each frame can be extracted separately from the capture variable (the videostream)
capture = cv2.VideoCapture(0)

# 'emptyFunction' function defined to be used by the 'Variables' Trackbar
 
def emptyFunction(a):
    pass
# Define Threshold parameters (Variables) and Trackbars for variation: area size filtering and 2 thresholds for Canny Edges
cv2.namedWindow("Variables")
cv2.resizeWindow("Variables",640,240)
cv2.createTrackbar("Thresh_1","Variables",172,255,emptyFunction) # Threshold parameter 1
cv2.createTrackbar("Thresh_2","Variables",30,255,emptyFunction) # Threshold parameter 2
cv2.createTrackbar("Area","Variables",7000,121500,emptyFunction) # Area filtering variable

# Function that takes input 'img' and returns output 'imgContour' (contours and labels drawn over original image) 
def getContours(img,imgContour):
  # Extract EXTERNAL contours from the input image, img=Dilated_img, when the function will be called
  contours, unused_var = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)# simple-less no of points
  # Draw external contours over the output image, imgContour will be a copy of img initially
  cv2.drawContours(imgContour,contours,-1,(255,0,255),3)
  # Iterate over all contours (cnt)
  for cnt in contours:
    # Calculate area of each contour (in pixels)
    area = cv2.contourArea(cnt)
    # Set an arbitraty minimum area, from Area trackbar in 'Variables' tab
    areamin=cv2.getTrackbarPos("Area","Variables")
    # Any contour with less than areamin will be ignored (reduces unwanted noise)
    if area > areamin:
      # If area is large enough, draw the contours over the output image, imgContour
      cv2.drawContours(imgContour,cnt,-1,(255,0,255),3)
       # Compute the contour perimeter / length (True=only closed contours considered)
      perimeter=cv2.arcLength(cnt,True)
      # Approximate the shape of object, contours (cnt) as input, resolution=0.01*length, True=only closed contours
      shape_approximation = cv2.approxPolyDP(cnt, 0.01*perimeter, True)# contains a number of points, used in determining shapes: length(shape_approximation)
      # Calculates minimum upright bounding rectangle for the specific point set (object)- outputs start coordinates (x,y) (top left) and rectangle dimensions (w,h)
      x,y,w,h=cv2.boundingRect(shape_approximation)
      # Draw bounding box over object: input the start coords (x,y) and end coords (x+w,y+h)
      cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),3)
      # Display number of points of an object, area in pixels and CENTER POINT
      cv2.putText(imgContour, "No. of Points: " + str(len(shape_approximation)), (x, y + 20), cv2.FONT_HERSHEY_COMPLEX, .5,
                        (0, 0, 255), 1)
      cv2.putText(imgContour, "Area [p]: " + str(int(area)), (x, y + 40), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                        (0, 0, 255), 1)
      cv2.putText(imgContour, "Center [p]: ("+ str(x+int(w/2)) +","+ str(y+int(h/2))+ ")", (x, y + 80), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)
      # If an object has 4 or 5 points, it is a window (rectangular window assumed)
      if len(shape_approximation)>=4 and len(shape_approximation)<=5:
        cv2.putText(imgContour, "Window", (x, y + 60), cv2.FONT_HERSHEY_COMPLEX, .5,
                        (0, 0, 255), 1)
        # Draw center point of window/rectangle in red
        cv2.circle(imgContour, (x+int(w/2),y+int(h/2)), radius=0, color=(0, 0, 255), thickness=5)

        # AREA IN METERS CALCULATIONS, using the calibration.py script
        DC1=0.12 # input variable distance measured by sensor [m] from drone to wall
        PPM1=calibration.PPM*calibration.DC/DC1 # PPM' at that exact distance (DC1)
        print("PPM at actual distance DC1: "+ str(PPM1))
        A_p1=area # Area in pixels of actual object
        print("Actual object area in pixels: "+ str(A_p1))
        A_m1 = A_p1 / PPM1 # REQUIRED AREA of object [m^2]
        print("Actual object area in meters: "+ str(A_m1)) # REQUIRED AREA OF ENTRY POINT DISPLAYED IN TERMINAL
        # Display area [m^2] on image
        cv2.putText(imgContour, "Area [m^2]: " + str(A_m1), (x, y + 100), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                        (0, 255, 0), 1)
      # If an object has >5 points, it is a hole (circular,elliptic,irregular shaped holes assumed)
      else: 
        cv2.putText(imgContour, "Hole", (x, y + 60), cv2.FONT_HERSHEY_COMPLEX, .5,
                        (0, 0, 255), 1)
        # Draw center point of hole in red
        cv2.circle(imgContour, (x+int(w/2),y+int(h/2)), radius=0, color=(0, 0, 255), thickness=5)

# Run for every frame in the videostream; img = each frame 
while True:
    grabbed, img = capture.read() # grab the frames and store them as img
    imgContour = img.copy() # initialize the output imgContour as a copy of img
    # Apply Gaussian Blur Filter, (9,9) kernel to smooth the image and reduce noise  
    Blur_img = cv2.GaussianBlur(img, (9, 9), 1)
    # Convert to Greyscale
    Gray_img = cv2.cvtColor(Blur_img, cv2.COLOR_BGR2GRAY)
    # Set treshold values for Canny Edge Detector, using trackbars in the 'Variables' window  
    thresh_1 = cv2.getTrackbarPos("Thresh_1", "Variables")
    thresh_2 = cv2.getTrackbarPos("Thresh_2", "Variables")
    # Apply Canny Edge Detection filter with variable thresholds, tested defaults are 172,140, can be varied
    Canny_img = cv2.Canny(Gray_img,thresh_1,thresh_2)
    # Creating convolution kernel used for Dilation  
    kernel = np.ones((5, 5))
    # Dilating the Canny Edges in order to accentuate the shape, iterations=1 for most accurate object area
    Dilated_img = cv2.dilate(Canny_img, kernel, iterations=1)
    # Use defined function to draw the boxel, labels and areas using the Dilated_img as input, for accurate detection, and the copy of img (imgContour) as the output image. Thus, the boxes, labels and areas will appear on the original un-filtered videostream live.
    getContours(Dilated_img, imgContour)
    # Display original videostream frames with contours, boxes, labels and areas
    cv2.imshow("Contours", imgContour)
    # Stop script upon pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break