import Image
# import Motor
import numpy as np
import Puck
import pickle

# DC_MOTOR_1 = Motor.Motor(Motor.ID.DC_MOTOR_1, np.array([150, 100, 175]), np.array([200, 125, 200]))

puck = Puck.Puck(np.array([85, 0, 0]), np.array([150, 255, 255]))

if __name__ == "__main__":
    points = []
    for i in range (26, 27):
        Image.setFileName(f"data{i}.mp4")
        points.append([])
        try:
            while Image.streamIsRunning():
                img = Image.transformImage(Image.getImage())
                point = puck.getPosition(img, threshold=0.1)
                Image.showImage(img, [point])
                if point is not None and point[0] is not None and point[1] is not None:
                    if point[1] < 450:
                        points[0].append(point)
                    else:
                        break
        except:
            continue
    print(points)
    # with open('list_data.pkl', 'wb') as file:
    #     pickle.dump(points, file)