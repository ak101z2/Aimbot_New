import cv2
import numpy as np

class Puck:
    def __init__(self, LOWER_HSV, UPPER_HSV):
        self.LOWER_HSV = LOWER_HSV
        self.UPPER_HSV = UPPER_HSV

    def getPosition(self, image, threshold=0):
        if image is None: return None
        height, width, _ = image.shape
        start_row = int(height * threshold)
        frame = image[start_row:, :]

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.LOWER_HSV, self.UPPER_HSV)
        kernel = np.ones((11,11), np.float32)/25
        inverted_res = cv2.filter2D(mask,-1,kernel)
        res = cv2.bitwise_not(inverted_res)
        contours, __ = cv2.findContours(res, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                center_x = int(M["m10"] / M["m00"])
                center_y = int(M["m01"] / M["m00"])
                return (center_x, center_y + start_row)
        return (None, None)

