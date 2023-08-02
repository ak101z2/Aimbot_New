import cv2
import time
import serial
import numpy as np
from enum import Enum

arduino = serial.Serial(port='COM7', baudrate=115200, timeout=.1)

def write(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)

class ID(Enum):
    DC_MOTOR_1 = 1
    DC_MOTOR_2 = 2
    SERVO_MOTOR = 3

class Direction(Enum):
    RIGHT = FORWARD = 1
    LEFT = BACKWARD = -1

class Motor:
    def __init__(self, id, LOWER_HSV, UPPER_HSV):
        self.id = id
        self.LOWER_HSV = LOWER_HSV
        self.UPPER_HSV = UPPER_HSV

    def getPosition(self, frame, lower_bound=0, upper_bound=0):
        # height, width = frame.shape[:2]
        if lower_bound != 0 and upper_bound != 0:
            frame = frame[lower_bound:upper_bound, :]
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.LOWER_HSV, self.UPPER_HSV)
        kernel = np.ones((15,15), np.float32)/25
        res = cv2.filter2D(mask,-1,kernel)
        contours, __ = cv2.findContours(res, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        max_contour_size = 0
        motor_contour = None
        for contour in contours:
            if cv2.contourArea(contour) > max_contour_size:
                max_contour_size = cv2.contourArea(contour)
                motor_contour = contour
        if motor_contour is not None:
            M = cv2.moments(motor_contour) 
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            return (cX, cY + lower_bound)
        else:
            return (None, None)
        
    def move(self, speed, direction):
        write(str(self.id.value))
        write(str(speed))
        print(self.id.value, speed)