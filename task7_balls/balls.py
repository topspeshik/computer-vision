from time import sleep

import cv2
import numpy as np
import random

ballBlue = [98, 232, 120]
lower = np.array([ballBlue[0] - 15, ballBlue[1] - 50, 0])
higher = np.array([ballBlue[0] + 15, ballBlue[1] + 50, 255])

ballRed = [180, 230, 178]
lower1 = np.array([ballRed[0] - 15, ballRed[1] - 15, 0])
higher1 = np.array([ballRed[0] + 15, ballRed[1] + 15, 255])

ballGreen = [63, 132, 170]
lower2 = np.array([ballGreen[0] - 15, ballGreen[1] - 15, 0])
higher2 = np.array([ballGreen[0] + 15, ballGreen[1] + 15, 255])

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)

cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)


def createMask(lower, higher):
    mask1 = cv2.inRange(hsv, lower, higher)
    mask1 = cv2.erode(mask1, None, iterations=2)
    mask1 = cv2.dilate(mask1, None, iterations=2)
    return mask1


rgbComp = []
randNum = [1, 2, 3]
rgbComp.append(random.choice(randNum))
randNum.remove(rgbComp[0])
rgbComp.append(random.choice(randNum))
randNum.remove(rgbComp[1])
rgbComp.append(random.choice(randNum))
rggb = {}
rggb = {3: "red", 2: "green", 1: "blue"}

r = 3
g = 2
b = 1
while cam.isOpened():
    ret, frame = cam.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask1 = createMask(lower, higher)

    contours1, _ = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x1 = 0

    if len(contours1) > 0:
        c = max(contours1, key=cv2.contourArea)
        (x1, y1), radius = cv2.minEnclosingCircle(c)
        if radius > 10:
            cv2.circle(frame, (int(x1), int(y1)), int(radius), (0, 255, 255), 2)

    mask2 = createMask(lower1, higher1)

    contours2, _ = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x2 = 0

    if len(contours2) > 0:
        c = max(contours2, key=cv2.contourArea)
        (x2, y2), radius = cv2.minEnclosingCircle(c)
        if radius > 10:
            cv2.circle(frame, (int(x2), int(y2)), int(radius), (0, 255, 255), 2)

    mask3 = createMask(lower2, higher2)
    contours3, _ = cv2.findContours(mask3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x3 = 0

    if len(contours3) > 0:
        c = max(contours3, key=cv2.contourArea)
        (x3, y3), radius = cv2.minEnclosingCircle(c)
        if radius > 10:
            cv2.circle(frame, (int(x3), int(y3)), int(radius), (0, 255, 255), 2)

    comp = "red, green, blue"

    rgb = []

    if x1 > x2 and x3 > x1 and x2 * x1 * x3 != 0:
        rgb = [3, 1, 2]
    # red, green, blue
    elif x2 > x1 and x1 > x3 and x2 * x1 * x3 != 0:
        rgb = [2, 1, 3]
    # blue, green, red
    elif x1 < x3 and x2 > x3 and x2 * x1 * x3 != 0:
        rgb = [1, 2, 3]
    # blue, red, green
    elif x1 < x2 and x3 > x2 and x2 * x1 * x3 != 0:
        rgb = [1, 3, 2]
    # green, blue, red
    elif x2 < x1 and x2 > x3 and x2 * x1 * x3 != 0:
        rgb = [2, 1, 3]
    # red, green, blue
    elif x2 < x3 and x3 < x1 and x2 * x1 * x3 != 0:
        rgb = [3, 2, 1]

    print(rggb[rgbComp[0]], rggb[rgbComp[1]], rggb[rgbComp[2]])

    if len(rgb) != 0 and rgbComp[0] == rgb[0] and rgbComp[1] == rgb[1] and rgbComp[2] == rgb[2]:
        randNum = [1, 2, 3]
        rgbComp = []
        rgbComp.append(random.choice(randNum))
        randNum.remove(rgbComp[0])
        rgbComp.append(random.choice(randNum))
        randNum.remove(rgbComp[1])
        rgbComp.append(random.choice(randNum))
        print("Вы угадали")
        sleep(2)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

    cv2.imshow("Camera", frame)

cam.release()
cv2.destroyAllWindows()
