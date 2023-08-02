import cv2

coordinates = [(447, 87), (851, 86), (196, 574), (1140, 579)]
#coordinates = []

def initialize():
    return len(coordinates) == 0

def getCoordinates(img):
    if (len(coordinates) == 4):
        return coordinates
    def click_event(event, x, y, flags, params):
        if (len(coordinates) < 4):
            if event == cv2.EVENT_LBUTTONDOWN:
                print(f"X: {x}, Y: {y}")
                cv2.circle(img, (x, y), 2, (0, 0, 0), -1)
                cv2.putText(img, str(x) + ',' +
                            str(y), (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                            0.25, (0, 255, 0), 1)
                cv2.imshow('frame', img)
                coordinates.append((x, y))
                print(len(coordinates))
        return
    cv2.imshow('frame', img)
    cv2.setMouseCallback('frame', click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return coordinates