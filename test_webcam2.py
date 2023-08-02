import cv2

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW) # if you have second camera you can set first parameter as 1
cap.set(cv2.CAP_PROP_FRAME_WIDTH , 640) # you should chose a value that the camera supports
cap.set(cv2.CAP_PROP_FRAME_HEIGHT , 480) # you should chose a value that the camera supports

while True:
    success,img = cap.read()
    cv2.imshow('Image',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


