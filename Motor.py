import serial

class Motor:
    arduino = serial.Serial(port='COM7', baudrate=9600, timeout=.1)
    def __init__(self, motorNum, targetPosition=0):
        self.motorNum = motorNum
        self.targetPosition = targetPosition
    def getPosition(self):
        pos = self.arduino.readline()
        if pos == "b\'\'": return None
        else: 
            pos = int(pos[2:-5])
            return self.currentPosition
    def setPosition(self, targetPosition):
        self.targetPosition = targetPosition
        pos = str(self.motorNum) + str(targetPosition)
        self.arduino.write(bytes(pos, 'utf-8'))
    def __str__(self):
        return f"Current Position: {self.currentPosition}\nTarget Position: {self.targetPosition}"