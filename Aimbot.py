import cv2
import numpy as np
import imutils

from Puck import Puck
# from Motor import Motor

### _____Begin Initialization_____ ###

FRAME_WIDTH = 270
FRAME_HEIGHT = 480

LOWER_HSV = np.array([30,150,75])
UPPER_HSV = np.array([50,255,255])

#vid = cv2.VideoCapture(1, cv2.CAP_DSHOW)

### _____End Initialization_____ ###

def getImage(vid):
    if vid.isOpened():
        ret, frame = vid.read()
        if ret:
            frame = imutils.resize(frame, width=FRAME_WIDTH, height=FRAME_HEIGHT)
            #frame = cv2.rotate(frame, cv2.ROTATE_180)
            return frame
    return None

def getPuck(frame, vid):
    cX, cY = None, None
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, LOWER_HSV, UPPER_HSV)
    mask = imutils.resize(mask, width=FRAME_WIDTH, height=FRAME_HEIGHT)
    kernel = np.ones((15,15),np.float32)/25
    res = cv2.filter2D(mask,-1,kernel)
    contours, __ = cv2.findContours(res, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    max_contour_size = 0
    contour = None
    if len(contours) > 0:
        for c in contours:
            if cv2.contourArea(c) > max_contour_size:
                contour = c
        M = cv2.moments(contour) 
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
        cv2.putText(frame, f"({cX}, {cY})", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 1)
        return Puck(cX, cY) 
    cv2.imshow('frame', frame)
    cv2.imwrite('img.png', frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        vid.release()
    return None

vid = cv2.VideoCapture('data1.mp4')
# vid.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
# vid.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

while vid.isOpened():
    getPuck(getImage(vid), vid)

cv2.destroyAllWindows()
vid.release()

