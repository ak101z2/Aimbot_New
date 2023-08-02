import sys

import pygame

from pygame.locals import *
pygame.init()
#pygame.display.set_caption('game base')
#screen = pygame.display.set_mode((500, 500), 0, 32)
#clock = pygame.time.Clock()

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
    print(joystick.get_name())

#my_square = pygame.Rect(50, 50, 50, 50)
#my_square_color = 0
#colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
motion = [0, 0]

import serial
import time
import random

arduino = serial.Serial(port='COM8', baudrate=9600, timeout=.1)

def write(x):
    arduino.write(bytes(str(x), 'utf-8'))

def mapRange(value, inMin, inMax, outMin, outMax):
    return outMin + (((value - inMin) / (inMax - inMin)) * (outMax - outMin))

while True:

    # screen.fill((0, 0, 0))

    # pygame.draw.rect(screen, colors[my_square_color], my_square)
    # if abs(motion[0]) < 0.1:
    #     motion[0] = 0
    # if abs(motion[1]) < 0.1:
    #     motion[1] = 0
    # my_square.x += motion[0] * 10
    # my_square.y += motion[1] * 10

    for event in pygame.event.get():
        # if event.type == JOYBUTTONDOWN:
        #     print(event)
        #     if event.button == 0:
        #         my_square_color = (my_square_color + 1) % len(colors)
        # if event.type == JOYBUTTONUP:
        #     print(event)
        if event.type == JOYAXISMOTION:
            #print(event)
            if event.axis < 2:
                motion[event.axis] = event.value
                if event.axis == 0:
                    num = round(event.value*1000)
                    num = round(mapRange(num, -1000, 1000, 45, 90))
                    num = "{:03d}".format(num)
                    print(num)
                    # num = mapRange(num, -1000, 1000, -255, 255)
                    # num = round(num)
                    # if num < 0:
                    #     num = abs(num) + 255
                    # value = "{:03d}".format(num)
                    # print(value)
                    write(num)
                    write("\0")


                    # if num > 0 and num < 999:
                    #     value = "0" + "{:03d}".format(abs(num))
                    #     print(value)
                    #     # write(value)
                    #     # write("\0")
                    # elif num < 0 and num > -999:
                    #     value = "-" + "{:03d}".format(abs(num)) 
                    #     print(value)
                        # write(value)
                        # write("\0")
                    # time.sleep(0.05)
        # if event.type == JOYHATMOTION:
        #     print(event)
        # if event.type == JOYDEVICEADDED:
        #     joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        #     for joystick in joysticks:
        #         print(joystick.get_name())
        # if event.type == JOYDEVICEREMOVED:
        #     joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        # if event.type == QUIT:
        #     pygame.quit()
        #     sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    # pygame.display.update()
    # clock.tick(60)