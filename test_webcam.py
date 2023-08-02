# import the opencv library
import numpy
import cv2
import imutils
  
  
# define a video capture object
vid = cv2.VideoCapture("test2.mp4")
  
while(vid.isOpened()):
    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    frame = imutils.resize(frame, width=320, height=180)
    cv2.line(frame, (93, 0), (0, 142), (255, 0, 0), 1)
    cv2.line(frame, (219, 0), (319, 153), (255, 0, 0), 1) 
    cv2.line(frame, (0, 143), (320, 143), (255, 0, 0), 1)

    # Display the resulting frame
    cv2.imshow('frame', frame)
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
