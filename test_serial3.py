import serial
import time
arduino = serial.Serial(port='COM6', baudrate=9600, timeout=.1)

def write_read(x):
    arduino.write(bytes(str(x), 'utf-8'))
    #time.sleep(0.1)
    data = arduino.readline()
    return data

#num = input("Enter a number: ") # Taking input from user
while True:
    #num = input("Enter a number: ") # Taking input from user
    #for ledPin in range(8, 14):
    value = write_read(4)
    print(value) # printing the value

arduino.close()