import sys
import time
import Motor
import serial
import pygame
from pygame.locals import *

pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)

def map_range(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

dc1 = dc2 = servo = dc1_prev = dc2_prev = servo_prev = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYHATMOTION:
            dpad = event.value
            if dpad == (0, 1):
                print("Up")
                servo = 20
            elif dpad == (0, -1):
                print("Down")
                servo = -20
            else:
                servo = 0
        if event.type == JOYBUTTONDOWN:
            dc1 = dc2 = 4
            Motor.write(str(4))
            continue
        if event.type == JOYAXISMOTION:
            dc1 = joystick.get_axis(0)
            dc2 = joystick.get_axis(2)
            dc1 = int(map_range(dc1, -1, 1, -150, 150))
            dc2 = int(map_range(dc2, -1, 1, -75, 75))
        
        if dc1 != dc1_prev:
            Motor.write(str(1))
            Motor.write(str(dc1))
        if dc2 != dc2_prev: 
            Motor.write(str(2))
            Motor.write(str(dc2))
        if servo != servo_prev: 
            Motor.write(str(3))
            Motor.write(str(servo))
        
        dc1_prev = dc1
        dc2_prev = dc2
        servo_prev = servo

        print(dc1, dc2, servo)