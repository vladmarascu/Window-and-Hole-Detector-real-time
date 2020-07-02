import cv2
import numpy as np

#img=cv2.imread('ipaddraw1.jpg') # change for any picture
img=cv2.imread('images/type2,2m.png') # change for any picture

def empty(a):
  pass

cv2.namedWindow('Parameters')
cv2.resizeWindow('Parameters',640,240)
cv2.createTrackbar("Threshold 1",'Parameters',172,255,empty)
cv2.createTrackbar("Threshold 2",'Parameters',30,255,empty)
cv2.createTrackbar("Area",'Parameters',7000,30000,empty)

def getContours(img,imgContour):
  contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)# simple-less no of points
  cv2.drawContours(imgContour,contours,-1,(255,0,255),3)

  for cnt in contours:

    area = cv2.contourArea(cnt)
    areamin=cv2.getTrackbarPos("Area","Parameters")

    if area > areamin:

      cv2.drawContours(imgContour,cnt,-1,(255,0,255),3)
      peri=cv2.arcLength(cnt,True)
      approx=cv2.approxPolyDP(cnt,0.02*peri,True)
      #print(len(approx))
      x,y,w,h=cv2.boundingRect(approx)
      cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),3) # bounding box

      #cv2.putText(imgContour, "Points: " + str(len(approx)), (x, y + 20), cv2.FONT_HERSHEY_COMPLEX, .5,
      #                  (0, 0, 255), 1)
      #cv2.putText(imgContour, "Area [p]: " + str(int(area)), (x+20, y + 50), cv2.FONT_HERSHEY_COMPLEX, 1,
      #                  (0, 0, 255), 1)
      cv2.putText(imgContour, "Area [m^2]: 0.399" , (x+20, y - 20), cv2.FONT_HERSHEY_COMPLEX, 1,
                        (0, 0, 255), 1)
      cv2.putText(imgContour, "Center: ("+ str(x+int(w/2)) +","+ str(y+int(h/2))+ ")", (x+20, y - 55), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
      #print("Center point (x,y) is: " +"("+ str(x+int(w/2)) +","+ str(y+int(h/2))+ ")")

      if len(approx)>=4 and len(approx)<=6:
        cv2.putText(imgContour, "Window", (x+20, y - 85), cv2.FONT_HERSHEY_COMPLEX, 1,
                        (0, 0, 255), 1)
        cv2.circle(imgContour, (x+int(w/2),y+int(h/2)), radius=0, color=(0, 0, 255), thickness=5)
        #print("Center point (x,y) is: " +"("+ str(x+int(w/2)) +","+ str(y+int(h/2))+ ")")

      else: 
        cv2.putText(imgContour, "Hole", (x, y + 60), cv2.FONT_HERSHEY_COMPLEX, .5,
                        (0, 0, 255), 1)
        cv2.circle(imgContour, (x+int(w/2),y+int(h/2)), radius=0, color=(0, 0, 255), thickness=5)
        #print("Center point (x,y) is: " +"("+ str(x+int(w/2)) +","+ str(y+int(h/2))+ ")")
    
      

while True:

  imgContour=img.copy()

  imgBlur=cv2.GaussianBlur(img,(7,7),1)

  imgGray=cv2.cvtColor(imgBlur,cv2.COLOR_BGR2GRAY)
  
  threshold1=cv2.getTrackbarPos("Threshold 1","Parameters")
  threshold2=cv2.getTrackbarPos("Threshold 2","Parameters")
  imgCanny=cv2.Canny(imgGray,threshold1,threshold2)
  
  kernel = np.ones((5, 5))
  imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

  getContours(imgDil,imgContour)

  #cv2.imshow("Original",img)
  #cv2.imshow("Blur",imgBlur)
  #cv2.imshow("Gray",imgGray)
  #cv2.imshow("Canny",imgCanny)
  #cv2.imshow("Dilation",imgDil)
  cv2.imshow("Contours",imgContour)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

