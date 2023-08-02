import cv2
import imutils

FRAME_WIDTH = 640
FRAME_HEIGHT = 960

# coordinates = [(616, 466), (182, 468), (254, 94), (439, 89)]
coordinates = [(204, 211), (468, 215), (10, 620), (619, 636)]
# coordinates = []

vid = cv2.VideoCapture(1, cv2.CAP_DSHOW)

def getImage():
    frame = None
    if vid.isOpened():
        ret, frame = vid.read()
        if ret:
            frame = imutils.resize(frame, width=FRAME_WIDTH, height=FRAME_HEIGHT)
    return frame

def initialize():
    return len(coordinates) == 0

def getCoordinates(img):
    if (len(coordinates) == 4):
        return coordinates
    def click_event(event, x, y, flags, params):
        if (len(coordinates) < 4):
            if event == cv2.EVENT_LBUTTONDOWN:
                print(f"X: {x}, Y: {y}")
                cv2.circle(img, (x, y), 2, (0, 0, 0), -1)
                cv2.putText(img, str(x) + ',' +
                            str(y), (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                            0.25, (0, 255, 0), 1)
                cv2.imshow('frame', img)
                coordinates.append((x, y))
                print(len(coordinates))
        return
    cv2.imshow('frame', img)
    cv2.setMouseCallback('frame', click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return coordinates

if __name__ == "__main__":
    while vid.isOpened():
        getCoordinates(getImage())