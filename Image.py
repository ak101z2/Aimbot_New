import cv2
import numpy as np
import imutils
import Coordinates
from Puck import Puck

### _____Begin Initialization_____ ###

FRAME_WIDTH = 640*2
FRAME_HEIGHT = 960*2

#FRAME_WIDTH = 240
#FRAME_HEIGHT = 360

LOWER_HSV = np.array([30,150,75])
UPPER_HSV = np.array([50,255,255])

vid = cv2.VideoCapture('data11.mp4')

#avg_contour_area = []

#vid = cv2.VideoCapture(1, cv2.CAP_DSHOW)

### _____End Initialization_____ ###

def getImage():
    frame = None
    if vid.isOpened():
        ret, frame = vid.read()
        if ret:
            frame = imutils.resize(frame, width=FRAME_WIDTH, height=FRAME_HEIGHT)
            #frame = cv2.rotate(frame, cv2.ROTATE_180)
    return frame

def showImage(frame, x, y, hit):
    if streamIsRunning() and frame is not None:
        cv2.line(frame, (0, y), (FRAME_WIDTH, y), (255, 0, 255), 1)
        try:
            cv2.circle(frame, (int(x), int(y)), 5, (255, 0, 255), -1)
        except:
            pass
        if hit:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            vid.release()
            quit()
    else:
        cv2.destroyAllWindows()
        vid.release()
        quit()

def order_points(pts):
	rect = np.zeros((4, 2), dtype = "float32")
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
	return rect

def transformImage(image):
    if image is not None:
        coord = Coordinates.getCoordinates(image)
        coordinates = np.array(coord, dtype=np.float32)
        rect = order_points(coordinates)
        (tl, tr, br, bl) = rect
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype = "float32")
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        return (warped, maxWidth, maxHeight)

def getPuck():
    (frame, width, height) = transformImage(getImage())
    #print(width, height)
    #frame = getImage()
    frame = imutils.resize(frame, width=width, height=height)
    cX, cY = -1, -1
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, LOWER_HSV, UPPER_HSV)
    mask = imutils.resize(mask, width=width, height=height)
    kernel = np.ones((15,15), np.float32)/25
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
        cv2.putText(frame, f"({cX}, {cY})", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
        #print(cv2.contourArea(contour))
        #avg_contour_area.append(cv2.contourArea(contour))
        #print(sum(avg_contour_area)/len(avg_contour_area))
    #showImage(frame)
    return (frame, Puck(cX, cY), width, height)

def streamIsRunning():
    return vid.isOpened()