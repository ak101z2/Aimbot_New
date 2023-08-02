import serial
import time
import random

arduino = serial.Serial(port='COM8', baudrate=9600, timeout=.1)

def write(x):
    arduino.write(bytes(str(x), 'utf-8'))

val = input("Please enter your input here: ")
while val != "quit":
    write(val)
    write("\0")
    time.sleep(0.05)
    val = input("Please enter your input here: ")