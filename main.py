import Image
import time
import numpy as np
import Regression
import math
from queue import Queue

import serial
import time
# arduino = serial.Serial(port='COM6', baudrate=9600, timeout=.1)

# def write_read(x):
#     arduino.write(bytes(str(x), 'utf-8'))

def computeMedian(arr):
    arr.sort()
    mid = len(arr) // 2
    res = (arr[mid] + arr[~mid]) / 2
    return res

if __name__ == "__main__":
    points_x, points_y = [], []
    target_x, target_y = 0, 500
    q = Queue(maxsize = 3)
    arr = []
    sum = 0

    while Image.streamIsRunning:
        # Get Puck
        (frame, puck, width, height) = Image.getPuck()

        # Compute Regression
        x = np.array(points_x, dtype=np.uint32)
        y = np.array(points_y, dtype=np.uint32)
        
        B0, B1, reg_line = Regression.linear_regression(x, y)
        R = Regression.corr_coef(x, y)
        
        target_x = (target_y-B0)/B1

        # Get Collision
        hit = False
        if puck == None:
            target_x = width/2
            hit = False
        elif abs(R) < 0.9:
            #target_x = puck.x
            hit = True
            points_x.clear()
            points_y.clear()
        elif puck.x - 60 < 0 or puck.x + 60 > width or puck.y - 25 < 0 or puck.y + 25 > height:
            #target_x = puck.x
            hit = True
            points_x.clear()
            points_y.clear() 
        else:
            hit = False
            points_x.append(puck.x)
            points_y.append(puck.y)
        
        # Get Bounds
        if not math.isnan(target_x) and not math.isinf(target_x):
            while target_x < 0 or target_x > width:
                x_crit, y_crit = -1, -1
                if (B0 > B1*width + B0):
                    x_crit = 0
                    y_crit = B0
                else:
                    x_crit = width
                    y_crit = B1*width + B0
                B1 = -1*B1
                B0 = y_crit - B1*x_crit
                target_x = (target_y-B0)/B1
        
        # if not math.isnan(target_x) and not math.isinf(target_x):
        #     q.put(target_x)
        #     sum += target_x
        #     if (q.full()):
        #         sum -= q.get()
        #     target_x = sum/q.qsize()
        #     val = int((target_x/width)*9 + 0.5)
        #     print(val)

        arr.append(target_x)
        while len(arr) > 3:
            arr.pop(0)
        target_x = computeMedian(arr)

        if puck.y > 400:
            target_x = puck.x

        # write_read(val)
        # write_read("\0")
        time.sleep(0.02)        
        
        Image.showImage(frame, target_x, target_y, hit)