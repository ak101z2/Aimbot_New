import serial
import time
arduino = serial.Serial(port='COM6', baudrate=9600, timeout=.1)
i = 10000
def write_read(x):
    arduino.write(bytes("2" + str(x), 'utf-8'))
    time.sleep(0.1)
    data = arduino.readline()
    return data
while i < 999999:
    #num = input("Enter a number: ") # Taking input from user
    value = write_read(i)
    print(value) # printing the value
    i = i + 1
arduino.close()