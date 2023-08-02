import cv2
import numpy as np
import imutils
import Coordinates

### _____Begin Initialization_____ ###

FRAME_WIDTH_INITIAL = 640
FRAME_HEIGHT_INITIAL = 960

# FRAME_WIDTH_FINAL = 240
# FRAME_HEIGHT_FINAL = 680

FRAME_WIDTH_FINAL = 240
FRAME_HEIGHT_FINAL = 480

# vid = cv2.VideoCapture(1, cv2.CAP_DSHOW)
vid = None

### _____End Initialization_____ ###

def setFileName(filename):
    global vid
    vid = cv2.VideoCapture(filename)

def getImage():
    frame = None
    if vid.isOpened():
        ret, frame = vid.read()
        if ret:
            frame = imutils.resize(frame, width=FRAME_WIDTH_INITIAL, height=FRAME_HEIGHT_INITIAL)
    return frame

def showImage(frame, points=[]):
    if streamIsRunning() and frame is not None:
        for x, y in points:
            if x is not None and y is not None:
                x, y = int(x), int(y)
                cv2.circle(frame, (x, y), 5, (0, 0, 0), -1)
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
        img = cv2.resize(warped, (FRAME_WIDTH_FINAL, FRAME_HEIGHT_FINAL))
        return img

def streamIsRunning():
    return vid.isOpened()

if __name__ == "__main__":
    while streamIsRunning():
        img = transformImage(getImage())
        showImage(img)
