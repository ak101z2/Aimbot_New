import cv2
import numpy as np
import imutils

class Camera:

    LOWER_HSV = np.array([30,150,75])
    UPPER_HSV = np.array([50,255,255])

    def __init__(self, name, width, height):
        self.name = name
        
        if isinstance(name, int):
            self.vid = cv2.VideoCapture(name, cv2.CAP_DSHOW)
        else:
            self.vid = cv2.VideoCapture(name)
        
        self.width = width
        self.height = height

    def __getImage(self):
        frame = None
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                frame = imutils.resize(frame, width=self.width, height=self.height)
                #frame = cv2.rotate(frame, cv2.ROTATE_180)
        return frame

    def getWarpedImage(self):
        pass

    def showImage(self, frame):
        if self.streamIsRunning() and cv2.waitKey(25) & 0xFF != ord('q'):
            cv2.imshow(self.name, frame)
        else:
            cv2.destroyAllWindows()
            self.vid.release()
            quit()

    def streamIsRunning(self):
        return self.vid.isOpened()